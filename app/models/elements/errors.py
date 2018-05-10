class ElementErrors(Exception):
    def __init__(self, message):
        self.message = message


class ElementNotFound(ElementErrors):
    pass