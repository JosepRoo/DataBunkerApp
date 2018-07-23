from app.models.products.product import Product as ProductModel
from app.common.database import Database

Database.initialize()

ProductModel.send_email_alerts()
