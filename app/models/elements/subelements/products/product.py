from datetime import datetime, timedelta
from dataclasses import dataclass
from mongoengine import *

from app.common.database import Database
from app.common.utils import Utils
from app.models.elements.channels.channel import Channel
from app.models.elements.errors import ElementNotFound
from app.models.elements.subelements.brands.brand import Brand
from app.models.elements.subelements.categories.category import Category
from app.models.elements.subelements.subelement import SubElement
from app.models.emails.email import Email
from app.models.emails.errors import EmailErrors, FailedToSendEmail
from app.models.logs.log import Log
from app.models.elements.subelements.products.constants import COLLECTION


@dataclass(init=False)
class Product(SubElement):
    parentElementId: Brand = ReferenceField(Brand, required=True)
    grandParentId: Category = ReferenceField(Category, required=True)
    greatGrandParentId: Channel = ReferenceField(Channel, required=True)
    UPC: str = StringField(required=True)
    image: str = StringField()
    discount_price: str = StringField()
    item_characteristics: str = StringField()
    link: str = StringField()
    sku_description: str = StringField()
    subcategory: str = StringField()
    subcategory2: str = StringField()
    sub_elements: list = ListField(EmbeddedDocumentField(Log), default=lambda: list())
    meta = {'collection': COLLECTION}

    @classmethod
    def get_by_UPC(cls, upc, channel_id):
        product = cls.objects(UPC=upc, greatGrandParentId=channel_id)
        if len(product) >= 1:
            return product[0]

    def is_duplicated_date(self, new_date: str):
        if list(filter(lambda x: x.date.strftime("%Y-%m-%d") == new_date[:10], self.sub_elements)):
            return True
        return False

    @staticmethod
    def get_average(element_id, begin_date, end_date):
        first_date = datetime.strptime(begin_date, "%Y-%m-%d")
        last_date = datetime.strptime(end_date, "%Y-%m-%d")
        last_date = last_date + timedelta(days=1)
        expressions = list()
        expressions.append({'$match': {'_id': element_id}})
        expressions.append({'$unwind': '$sub_elements'})
        expressions.append(
            {'$project': {'sub_elements.date': 1, 'sub_elements.value': 1,
                          'day': {'$dayOfMonth': '$sub_elements.date'},
                          'month': {'$month': '$sub_elements.date'}}})
        expressions.append({'$match': {'sub_elements.date': {'$gte': first_date, '$lte': last_date}}})
        expressions.append({'$group': {'_id': '$sub_elements.date',
                                       'average': {'$avg': '$sub_elements.value'}}})
        expressions.append({'$sort': {'_id': 1}})
        result = list(Database.aggregate(COLLECTION, expressions))
        for element in result:
            element["_id"] = element["_id"].strftime("%Y/%m/%d")
        return result

    @classmethod
    def get_element(cls, element_id):
        element = cls.objects(_id=element_id)
        if element:
            if len(element.sub_elements) >= 2:
                element.sub_elements = [element.sub_elements[-2], element.sub_elements[-1]]
            else:
                element.sub_elements = [0, element.sub_elements[-1]]
            return element
        raise ElementNotFound("El elemento con el id y tipo dado no fue encontrado")

    @staticmethod
    def send_email_alerts():
        emails = Product.build_email_products()
        for email in emails:
            # alert_email = Email(to='areyna@sitsolutions.org', subject='Notificación de productos favoritos')
            alert_email = Email(to=email, subject='Notificación de productos favoritos')

            emails_text = "Nuestro sistema ha detectado que los siguientes productos han bajado de precio:\n"
            for product in emails[email]:
                emails_text += f"\t{product.get('name')} cambió de ${product.get('yesterday')}" \
                    f"a ${product.get('today')}\n"
            emails_text += "\nEntra a estos enlaces para revisar el detalle de tus productos:\n"
            for product in emails[email]:
                emails_text += f"\tcomparador.data-bunker.com.mx/elements/product/{product.get('_id')}\n"

            emails_html = """\
            <html>
            <head>Alerta de favoritos</head>
            <body>
            <h3>Nuestro sistema ha detectado que los siguientes productos han bajado de precio:</h3>"""
            for product in emails[email]:
                emails_html += f"""<p>{product.get('name')} cambió de ${product.get('yesterday')}
                                    a ${product.get('today')}</p>"""
                image = product.get('image').replace('\\', '')
                emails_html += f"<img src={image} alt='Producto' />"
            emails_html += """<p>Entra a estos enlaces para revisar el detalle de tus productos:</p>"""
            for product in emails[email]:
                emails_html += f"""<p>comparador.data-bunker.com.mx/opt/#/app/product/{product.get('_id')}</p>"""

            alert_email.text(emails_text)
            alert_email.html(emails_html)
            try:
                alert_email.send()
            except EmailErrors as e:
                raise FailedToSendEmail(e)

    @staticmethod
    def build_email_products():
        expressions = list()
        expressions.append({"$project": {"_id": 1}})
        product_ids = list(Database.aggregate('products', expressions))
        expressions = list()
        expressions.append({"$match": {}})
        expressions.append({"$project": {"_id": "$email", "favoritos": "$favorites"}})
        user_favourites = list(Database.aggregate('users', expressions))
        product_subscribers = []
        for item in product_ids:
            arr = list(filter(lambda x: item['_id'] in x['favoritos'], user_favourites))
            if arr:
                product_subscribers.append({"_id": item['_id'], "emails": [user.get('_id') for user in arr]})
        expressions = list()
        expressions.append({"$match": {"_id": {"$in": [product.get('_id') for product in product_subscribers]}}})
        selected_products = list(Database.aggregate('products', expressions))
        return Product.find_cheaper_products(selected_products, product_subscribers)

    @staticmethod
    def find_cheaper_products(selected_products, product_subscribers):
        cheaper_products = {}
        for element in selected_products:
            logs = element.get('sub_elements')[::-1]
            first_date = logs.pop(0)
            while logs[0].get('date').day == first_date.get('date').day:
                logs.pop(0)
            today_price = first_date.get('value')
            yesterday_price = logs[0].get('value')
            if today_price < yesterday_price:
                for product in product_subscribers:
                    if product.get('_id') == element.get('_id'):
                        for email in product.get('emails'):
                            product_detail = {'_id': element.get('_id'),
                                              'name': element.get('name'),
                                              'yesterday': yesterday_price,
                                              'today': today_price,
                                              'image': element.get('image')}
                            if email not in cheaper_products:
                                cheaper_products[email] = [product_detail]
                            else:
                                cheaper_products[email].append(product_detail)
        return cheaper_products

    @staticmethod
    def build_products_report(product_ids, begin_date, end_date, field_name, user):
        allowed_products = Product.find_allowed_products(user, field_name, product_ids)
        first_date = datetime.strptime(begin_date, "%Y-%m-%d")
        last_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

        expressions = list()
        expressions.append({'$match': {'_id': {'$in': allowed_products}}})
        expressions.append({'$lookup':
            {
                'from': 'channels',
                'localField': 'greatGrandParentId',
                'foreignField': '_id',
                'as': 'channel'
            }})
        expressions.append({'$lookup':
            {
                'from': 'categories',
                'localField': 'grandParentId',
                'foreignField': '_id',
                'as': 'category'
            }})
        expressions.append({'$lookup':
            {
                'from': 'brands',
                'localField': 'parentElementId',
                'foreignField': '_id',
                'as': 'brand'
            }})
        expressions.append({'$project':
                                {"_id": 0, 'UPC': 1,
                                 'Canal': {'$arrayElemAt': ['$channel.name', 0]},
                                 'Categoría': {'$arrayElemAt': ['$category.name', 0]},
                                 'Marca': {'$arrayElemAt': ['$brand.name', 0]},
                                 'Nombre': '$name',
                                 'sub_elements':
                                     {"$filter":
                                          {"input": "$sub_elements", "as": "sub_elements", "cond":
                                              {"$and": [
                                                  {"$gte": ["$$sub_elements.date", first_date]},
                                                  {"$lte": ["$$sub_elements.date", last_date]}
                                              ]}}}}})
        expressions.append({'$project': {"sub_elements.created_date": 0}})
        expressions.append({"$sort": {"sub_elements.date": 1}})
        result = list(Database.aggregate('products', expressions))
        if not result:
            raise ElementNotFound("El reporte generó cero datos. Intente con otra fecha.")

        dates_range = [dt.strftime("%Y-%m-%d") for dt in
                       Utils.date_range(first_date, last_date - timedelta(days=1))]

        for i in range(len(result)):
            log_dates = {datetime.strftime(log.get('date'), "%Y-%m-%d"): log.get('value') for log in
                         result[i].get('sub_elements')}
            for date in dates_range:
                if date not in log_dates:
                    result[i][date] = 0
                else:
                    result[i][date] = log_dates.get(date)
            del result[i]['sub_elements']

        date = datetime.now().strftime("%Y%m%d%H%M%S")
        return Utils.generate_report(result, f'ReporteProductos_{date}.xlsx', "Productos")

    @classmethod
    def build_upc_channels_report(cls, email, to_excel=False):
        from app.models.users.user import User
        user = User.get_by_email(email)
        allowed_products = cls.find_allowed_products(user)
        expressions = list()
        expressions.append({'$match': {'$or': [{'_id': {'$in': allowed_products}},
                                               {'greatGrandParentId': user.channel_id}]}})
        expressions.append({'$lookup':
            {
                'from': 'channels',
                'localField': 'greatGrandParentId',
                'foreignField': '_id',
                'as': 'channel'
            }})
        expressions.append({'$project': {'_id': 0, 'UPC': 1, 'Nombre': '$name',
                                         'Canal': {'$arrayElemAt': ['$channel.name', 0]},
                                         'last_price': {
                                             '$cond': {'if': {'$eq': [{'$size': '$sub_elements'}, 0]}, 'then': 0.0,
                                                       'else': {'$arrayElemAt': ['$sub_elements.value', -1]}}}}})
        expressions.append({'$group': {'_id': {'UPC': '$UPC'},
                                       'channels': {'$push': {'k': '$Canal', 'v': '$last_price'}},
                                       'Nombre': {'$first': '$Nombre'}}})
        expressions.append({'$project': {'_id': 0,
                                         'UPC': '$_id.UPC',
                                         'Nombre': '$Nombre',
                                         'Canales': {'$arrayToObject': '$channels'}}})
        expressions.append({'$addFields': {'Canales.UPC': '$UPC', 'Canales.Nombre': '$Nombre'}})
        expressions.append({'$replaceRoot': {'newRoot': '$Canales'}})
        expressions.append({'$sort': {'UPC': 1}})
        expressions.append({'$sort': {'Nombre': 1}})
        result = list(Database.aggregate('products', expressions))
        channel_names = [x.get('name') for x in list(
            Database.find('channels', {'_id': {'$in': user.privileges.channels}}))]

        if not to_excel:
            for i in result:
                for name in channel_names:
                    if name not in i.keys():
                        i[name] = 0
        else:
            user_channel = Channel.get_by_id(user.channel_id)
            percentages_dict = {channel + " %": 0 for channel in channel_names}
            for i in result:
                user_channel_value = float(i.get(user_channel.name, 0))
                for name in channel_names:
                    if name not in i.keys():
                        i[name] = 0
                        percentages_dict[name + " %"] = 0.0
                    else:
                        try:
                            percentages_dict[name + " %"] = 100 * float(i[name]) / user_channel_value
                        except ZeroDivisionError:
                            percentages_dict[name + " %"] = 0.0

                i.update(percentages_dict)
            date = datetime.now().strftime("%Y%m%d%H%M%S")
            return Utils.generate_report(result, f'ReporteComparador_{date}.xlsx', "Productos")
        return result

    # @staticmethod
    # def find_allowed_products(user_id, element_level=None, elements_id=None):
    #     user_products = list()
    #     expressions = list()
    #     expressions.append({"$match": {"_id": user_id}})
    #     expressions.append({"$project": {"_id": 0, "privileges": "$privileges.privilege_tree"}})
    #     expressions.append({"$replaceRoot": {"newRoot": "$privileges"}})
    #     result = list(Database.aggregate(USERS, expressions))
    #     print(element_level, elements_id)
    #     for element in result:
    #         for channel in element:
    #             if element[channel] == 1:
    #                 if element_level == 'greatGrandParentId' and channel not in elements_id:
    #                     continue
    #                 elif element_level in ['grandParentId', 'parentElement_id', '_id']:
    #                     user_products.extend(
    #                         [product.get('_id') for product in
    #                          Database.find_ids(COLLECTION,
    #                                            {'greatGrandParentId': channel, element_level: {'$in': elements_id}})])
    #                     continue
    #                 user_products.extend(
    #                     [product.get('_id') for product in
    #                      Database.find_ids(COLLECTION, {'greatGrandParentId': channel})])
    #                 continue
    #             for category in element[channel]:
    #                 if element[channel][category] == 1:
    #                     if element_level == 'grandParentId' and category not in elements_id:
    #                         continue
    #                     elif element_level in ['parentElement_id', '_id']:
    #                         user_products.extend(
    #                             [product.get('_id') for product in
    #                              Database.find_ids(COLLECTION, {'grandParentId': category,
    #                                                             element_level: {'$in': elements_id}})])
    #                         continue
    #                     user_products.extend(
    #                         [product.get('_id') for product in
    #                          Database.find_ids(COLLECTION, {'grandParentId': category})])
    #                     continue
    #                 for brand in element[channel][category]:
    #                     if element[channel][category][brand] == 1:
    #                         if element_level == 'parentElementId' and brand not in elements_id:
    #                             continue
    #                         elif element_level == '_id':
    #                             user_products.extend(
    #                                 [product.get('_id') for product in
    #                                  Database.find_ids(COLLECTION, {'parentElementId': brand,
    #                                                                 element_level: {'$in': elements_id}})])
    #                             continue
    #                         user_products.extend([product.get('_id') for product in
    #                                               Database.find_ids(COLLECTION, {'parentElementId': brand})])
    #                         continue
    #                     user_products.extend([product for product in element[channel][category][brand]])
    #     return user_products

    @staticmethod
    def find_allowed_products(user: "User", element_level=None, elements_ids: list = None):
        privs = user.privileges
        pipe = {}
        if element_level is None:
            if privs.channels:
                pipe['greatGrandParentId__in'] = privs.channels
            if privs.categories:
                pipe['grandParentId__in'] = privs.cateogries
            if privs.brands:
                pipe['parentElementId__in'] = privs.brands
            if privs.products:
                pipe['_id__in'] = privs.products
            string = ""
            for k, v in pipe.items():
                string += f'Q({k}={v}) | '
            products = Product.objects(eval(string[:-2]))
        elif element_level == 'greatGrandParentId':
            products = Product.objects(greatGrandParentId__in=list(set(elements_ids + privs.channels)))
        elif element_level == 'grandParentId':
            products = Product.objects(Q(greatGrandParentId__in=privs.channels, grandParentId__in=elements_ids) |
                                       Q(grandParentId__in=list(set(elements_ids + privs.categories))))
        elif element_level == 'parentElementId':
            products = Product.objects(Q(greatGrandParentId__in=privs.channels, parentElementId__in=elements_ids) |
                                       Q(grandParentId__in=privs.categories, parentElementId__in=elements_ids) |
                                       Q(parentElementId__in=list(set(elements_ids + privs.brands))))

        elif element_level == '_id':
            products = Product.objects(Q(greatGrandParentId__in=privs.channels, _id__in=elements_ids) |
                                       Q(grandParentId__in=privs.categories, _id__in=elements_ids) |
                                       Q(parentElementId__in=privs.categories, _id__in=elements_ids) |
                                       Q(_id__in=list(set(elements_ids + privs.brands))))
        else:
            return list()
        return [prod._id for prod in products.only("_id")]
