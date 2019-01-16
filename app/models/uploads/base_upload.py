from app.models.basemodel import BaseModel
from app.models.elements.subelements.brands.brand import Brand
from app.models.elements.subelements.categories.category import Category
from app.models.elements.channels import Channel
from app.models.logs.log import Log
from app.models.elements.subelements.products.product import Product


class BaseUpload(BaseModel):
    URL = ''

    @staticmethod
    def build_tree():
        pass


    @staticmethod
    def get_channel(channel_name):
        return Channel.get_by_name(channel_name)
    @staticmethod
    def upsert_category(channel_id, category_name):
        category = Category.get_by_name(category_name, channel_id)
        insert = False
        if category is None:
            category = Category(category_name, channel_id)
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
    def upsert_product(product_upc, channel_id, **kwargs) -> (Product, bool):
        product = Product.get_by_UPC(product_upc, channel_id)
        insert = False
        updated = 0
        if product is None:
            kwargs['sub_elements'] = [kwargs['sub_elements']]
            product = Product(product_upc, greatGrandParentId=channel_id, **kwargs)
            insert = True
        elif not product.is_duplicated_date(kwargs['sub_elements']['date']):
            product.sub_elements.append(Log(**kwargs['sub_elements']))
            product.update_mongo(product.get_collection())
            updated = 1
        return product, insert, updated