import datetime

from app.models.elements.errors import ElementNotFound

__author__ = "Luis Ricardo Gutierrez Luna"

from app.models.elements.subelements.brands.brand import Brand
from app.models.elements.subelements.categories.category import Category
from app.models.elements.channels.channel import Channel
from app.models.logs.log import Log


class Tree(dict):
    """A tree implementation using python's autovivification feature."""

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

    # cast a (nested) dict to a (nested) Tree class
    def __init__(self, data={}):
        for k, data in data.items():
            if isinstance(data, dict):
                self[k] = type(self)(data)
            else:
                self[k] = data

    def save_to_mongo(self):
        from app.models.users.user import User
        from app.models.elements.subelements.products.product import Product
        result = {
            "channels": {
                "success": 0,
                "failed": list(),
                "messages": list()
            },
            "categories": {
                "success": 0,
                "failed": list(),
                "messages": list()
            },
            "brands": {
                "success": 0,
                "failed": list(),
                "messages": list()
            },
            "products": {
                "success": list(),
                "failed": list(),
                "skipped": list(),
                "messages": list()
            }
        }
        admin = User.get_by_email("admin@data-bunker.com")
        add_channels = list()
        date = datetime.datetime.now()
        for channel in self.keys():
            channel_exists = Channel.objects(name=channel).first()
            try:
                if not channel_exists:
                    channel_exists = Channel(name=channel)
                    channel_exists.save()
                    add_channels.append(channel_exists)
                result['channels']['success'] += 1
            except Exception as e:
                result['channels']['failed'].append({
                    "name": channel,
                    "categories_skipped": len(self[channel])
                })
                result['channels']['messages'].append(str(e))
                continue

            for category in self[channel]:
                try:
                    category_exists = Category.objects(name=category, parentElementId=channel_exists._id).first()
                    if not category_exists:
                        category_exists = Category(name=category, parentElementId=channel_exists._id)
                        category_exists.save()
                    result['categories']['success'] += 1
                except Exception as e:
                    result['categories']['failed'].append({
                        "name": category,
                        "brands_skipped": len(self[channel][category])
                    })
                    result['categories']['messages'].append(str(e))
                    continue
                for brand in self[channel][category]:
                    try:
                        brand_exists = Brand.objects(name=brand, parentElementId=category_exists._id).first()
                        if not brand_exists:
                            brand_exists = Brand(name=brand, parentElementId=category_exists._id,
                                                 grandParentId=channel_exists._id)
                            brand_exists.save()
                        result['brands']['success'] += 1
                    except Exception as e:
                        result['brands']['failed'].append({
                            "name": brand,
                            "products_skipped": len(self[channel][category][brand])
                        })
                        result['brand']['messages'].append(str(e))
                        continue
                    for product in self[channel][category][brand]:
                        log = self[channel][category][brand][product]
                        flds = ['name', 'UPC', 'image', 'discount_price','item_characteristics', 'link',
                                'sku_description', 'subcategory', 'subcategory2']
                        values = product.split("||")
                        dct = dict(zip(flds, values))
                        product_upc = dct.get('UPC')
                        if log.get('value') is None or log.get('date') is None:
                            log['value'], log['date'] = 'err', 'err'
                            raise ElementNotFound("bad config of log")

                        log["value"] = float(str(log['value']).strip("$ \t"))
                        log['created_date'] = datetime.datetime.now()
                        new_date = log['date']
                        log['date'] = datetime.datetime.strptime(log['date'], "%Y-%m-%d")
                        try:

                            product_exists = Product.get_by_UPC(product_upc, channel_exists._id)
                            if not product_exists:
                                product_exists = Product(sub_elements=[log],
                                                         grandParentId=category_exists._id,
                                                         greatGrandParentId=channel_exists._id,
                                                         parentElementId=brand_exists._id,
                                                         **dct)
                            elif not product_exists.is_duplicated_date(new_date):
                                product_exists.sub_elements.append(Log(**log))
                                if product_exists.image is None:
                                    product_exists.image = dct.get('image')
                            else:
                                log['date'] = log['date'].strftime("%Y-%m-%d %H:%M:%S")
                                log['created_date'] = log['created_date'].strftime("%Y-%m-%d %H:%M:%S")
                                result['products']['skipped'].append({
                                    "upc": product_upc,
                                    "log": log
                                })
                                continue
                            product_exists.save()
                            log['date'] = log['date'].strftime("%Y-%m-%d %H:%M:%S")
                            log['created_date'] = log['created_date'].strftime("%Y-%m-%d %H:%M:%S")
                            result['products']['success'].append({
                                "upc": product_upc,
                                "log": log,
                            })
                        except IndexError as e:
                            result['products']['failed'].append({
                                "upc": product_upc,
                                "log": ["err", "err"],
                            })
                            result['products']['messages'].append(str(e))
        result['products']['skipped_qty'] = result['products']['skipped']
        for channel in add_channels:
            admin.add_privilege("channel", channel._id)
        return result

    def split_into_categories(self):
        categories_list = list()
        for channel in self:
            for category in self.get(channel):
                temp = Tree()
                temp[channel][category] = self[channel][category]
                categories_list.append(temp)

        return categories_list

    def split_into_brands(self):
        brands_list = list()
        for channel in self:
            for category in self.get(channel):
                for brand in self.get(channel).get(category):
                    temp = Tree()
                    temp[channel][category][brand] = self[channel][category][brand]
                    brands_list.append(temp)

        return brands_list
