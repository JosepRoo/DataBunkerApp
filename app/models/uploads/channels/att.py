from app import Database
from app.models.brands.brand import Brand
from app.models.brands.constants import COLLECTION as BRAND_COLLECTION
from app.models.categories.category import Category
from app.models.channels.channels import Channel
from app.models.logs.log import Log
from app.models.products.product import COLLECTION as PRODUCT_COLLECTION
from app.models.products.product import Product
from app.models.uploads.base_upload import BaseUpload

from bs4 import BeautifulSoup
import datetime
import hashlib
import requests


class ATT(BaseUpload):
    URL = "https://www.whistleout.com.mx/CellPhones/Carriers/ATT/Personal/att-prepago-200?contract=0&phone=Apple-iPhone-X-64GB&phoneprice=Outright"

    @classmethod
    def build_tree(cls):
        response = requests.get(cls.URL)
        replacers = ["\n", " ", "$", "Equipo", ","]
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all("div", {"class": "[ row has-hover-bg ] [ pad-y-3 bor-b-1 ]"})
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        channel = cls.get_channel()
        category, upsert = cls.upsert_category(channel._id)
        if upsert:
            category.save_to_mongo(category.get_collection())
        brands_to_insert = list()
        products_to_insert = list()
        length = 0
        for item in elements:
            product = item.find("h4", {"class": "mar-0"}).text.replace("\r\n", "").strip()
            price = item.find("div", {"class": "[ col-xs-8 ] [ col-sm-4 ] [ pad-y-3 text-center ]"}).text
            for rep in replacers:
                price = price.replace(rep, "")
            brand = product.split(' ')[0]
            brand, insert = cls.upsert_brand(brand, category._id)
            if insert:
                brands_to_insert.append(brand.json(date_to_string=False))
            upc = hashlib.md5(product.encode('utf-8')).hexdigest()[:16]
            image = item.find("img")['src']
            sub_elements = {'date': now, 'value': float(price)}
            product, upsert = cls.upsert_product(upc, channel._id, image=image, sub_elements=sub_elements,
                                                 product=product)
            if upsert:
                products_to_insert.append(product.json(date_to_string=False))
            length += 1
        if brands_to_insert:
            Database.insert_many(BRAND_COLLECTION, brands_to_insert)
        if products_to_insert:
            Database.insert_many(PRODUCT_COLLECTION, products_to_insert)

    @staticmethod
    def get_channel():
        return Channel.get_by_name("ATT")

    @staticmethod
    def upsert_category(channel_id):
        category = Category.get_by_name("Celulares", channel_id)
        insert = False
        if category is None:
            category = Category("Celulares", channel_id)
            insert = True
        return category, insert

    @staticmethod
    def upsert_brand(brand_name, category_id):
        brand = Brand.get_by_name(brand_name, category_id)
        insert = False
        if brand is None:
            brand = Brand(brand, category_id)
            insert = True
        return brand, insert

    @staticmethod
    def upsert_product(product_upc, channel_id, **kwargs):
        product = Product.get_by_UPC(product_upc, channel_id)
        insert = False
        if product is None:
            product = Product(product, channel_id, **kwargs)
            insert = True
        elif not product.is_duplicated_date(kwargs['sub_elements']['date']):
            product.sub_elements.append(Log(**kwargs['sub_elements']))
            product.update_mongo(product.get_collection())
        return product, insert
