from app.models.elements.element import Element


class Category(Element):
    def __init__(self, name, parentElementId, sub_elements=None, _id=None):
        Element.__init__(self, name, sub_elements, _id)
        self.parentElementId = parentElementId
