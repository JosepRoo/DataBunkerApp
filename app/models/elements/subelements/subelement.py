from __future__ import annotations
from dataclasses import dataclass

from mongoengine import *

# clase base de todos los elementos (canales,categorias,marcas,productos y logs)
from app.models.elements.element import Element


@dataclass(init=False)
class SubElement(Element):
    parentElementId: str = ReferenceField(Element, required=True)
    meta = {'allow_inheritance': True,
            'abstract': True}
