from app.models.basemodel import BaseModel


class BaseUpload(BaseModel):
    URL = ''

    @staticmethod
    def build_tree():
        pass


    @staticmethod
    def get_channel():
        pass

    @staticmethod
    def upsert_category(channel_id):
        pass

    @staticmethod
    def upsert_brand(brand_name, category_id):
        pass