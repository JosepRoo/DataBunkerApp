import datetime

from app.models.brands.brand import Brand
from app.models.categories.category import Category
from app.models.channels.channels import Channel
from app.models.logs.log import Log
from app.models.products.product import Product


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
        for channel in self.keys():
            channel_exists = Channel.get_by_name(channel)
            if not channel_exists:
                channel_exists = Channel(channel)
                channel_exists.save_to_mongo(Channel.get_collection_by_name(channel_exists.__class__.__name__),
                                             "sub_elements")
            for category in self[channel]:
                category_exists = Category.get_by_name_and_parent_id(category, channel_exists._id)
                if not category_exists:
                    category_exists = Category(category, channel_exists._id)
                    category_exists.save_to_mongo(Category.get_collection_by_name(category_exists.__class__.__name__),
                                                  "sub_elements")
                for brand in self[channel][category]:
                    brand_exists = Brand.get_by_name_and_parent_id(brand,category_exists._id)
                    if not brand_exists:
                        brand_exists = Brand(brand, category_exists._id)
                        brand_exists.save_to_mongo(Brand.get_collection_by_name(brand_exists.__class__.__name__),
                                                   "sub_elements")
                    for product in self[channel][category][brand]:
                        log = self[channel][category][brand][product]
                        product_name, product_upc = product.split("||")
                        product_exists = Product.get_by_UPC(product_upc)
                        if not product_exists:
                            product_exists = Product(product_upc, product_name, brand_exists._id, [log, ])
                        elif not product_exists.is_duplicated_date(
                                datetime.datetime.strptime(log['date'], "%Y-%m-%d %H:%M")):
                            product_exists.sub_elements.append(Log(**log))
                        else:
                            continue
                        product_exists.update_mongo(
                            Product.get_collection_by_name(product_exists.__class__.__name__))
