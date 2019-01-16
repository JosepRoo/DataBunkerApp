from datetime import datetime
from dataclasses import dataclass
from mongoengine import *

from app.models.baseEmbeddedDocument import BaseEmbeddedDocument


@dataclass
class Log(BaseEmbeddedDocument):
    value: float = FloatField(required=True)
    date: datetime = DateTimeField(required=True)
    created_date: datetime = DateTimeField(default=lambda: datetime.now())