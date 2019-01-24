from datetime import datetime
from dataclasses import dataclass
from mongoengine import *

from app.models.baseEmbeddedDocument import BaseEmbeddedDocument


@dataclass(init=False, eq=False)
class Log(BaseEmbeddedDocument):
    value: float = FloatField(required=True)
    date: datetime = DateTimeField(required=True)
    created_date: datetime = DateTimeField(default=lambda: datetime.now())

    def __eq__(self, other):
        return True if self.date == other.date else False

    def eq_date(self, date: datetime):
        return True if self.date == date else False
