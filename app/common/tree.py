from app.models.elements.errors import ElementNotFound

__author__ = "Luis Ricardo Gutierrez Luna"

import datetime

from app.models.brands.brand import Brand
from app.models.categories.category import Category
from app.models.channels.channels import Channel
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
        from app.models.products.product import Product
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
        for channel in self.keys():
            channel_exists = Channel.get_by_name(channel)
            try:
                if not channel_exists:
                    channel_exists = Channel(channel)
                    channel_exists.save_to_mongo(Channel.get_collection_by_name(channel_exists.__class__.__name__),
                                                 "sub_elements")
                    admin.add_privilege("channel", channel_exists._id)
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
                    category_exists = Category.get_by_name_and_parent_id(category, channel_exists._id)
                    if not category_exists:
                        category_exists = Category(category, channel_exists._id)
                        category_exists.save_to_mongo(
                            Category.get_collection_by_name(category_exists.__class__.__name__),
                            "sub_elements")
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
                        brand_exists = Brand.get_by_name_and_parent_id(brand, category_exists._id)
                        if not brand_exists:
                            brand_exists = Brand(brand, category_exists._id)
                            brand_exists.save_to_mongo(Brand.get_collection_by_name(brand_exists.__class__.__name__),
                                                       "sub_elements")
                        result['brands']['success'] += 1
                    except Exception as e:
                        result['brands']['failed'].append({
                            "name": brand,
                            "products_skipped": len(self[channel][category][brand])
                        })
                        result['brand']['messages'].append(str(e))
                        continue
                    for product in self[channel][category][brand]:
                        try:
                            log = self[channel][category][brand][product]
                            product_name, product_upc, product_image = product.split("||")
                            if log.get('value') is None or log.get('date') is None:
                                log['value'], log['date'] = 'err', 'err'
                                raise ElementNotFound("bad config of log")

                            log["value"] = float(log['value'].strip("$ \t"))
                            product_exists = Product.get_by_UPC(product_upc, channel_exists._id)
                            if not product_exists:
                                product_exists = Product(UPC=product_upc, name=product_name,
                                                         parentElementId=brand_exists._id, sub_elements=[log],
                                                         image=product_image, grandParentId=category_exists._id,
                                                         greatGrandParentId=channel_exists._id)
                            elif not product_exists.is_duplicated_date(log['date']):
                                product_exists.sub_elements.append(Log(**log))
                                if product_exists.image is None:
                                    product_exists.image = product_image
                            else:
                                result['products']['skipped'].append({
                                    "upc": product_upc,
                                    "log": log
                                })
                                continue
                            product_exists.update_mongo(
                                Product.get_collection_by_name(product_exists.__class__.__name__))
                            result['products']['success'].append({
                                "upc": product_upc,
                                "log": log,
                            })
                        except Exception as e:
                            if log.get('value') is None or log.get('date') is None:
                                log = dict()
                                log['value'], log['date'] = 'err', 'err'
                            result['products']['failed'].append({
                                "upc": product_upc,
                                "log": log,
                            })
                            result['products']['messages'].append(str(e))
        result['products']['skipped_qty'] = result['products']['skipped']
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