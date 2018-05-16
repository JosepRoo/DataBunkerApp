class Privilege:
    def __init__(self, channels=list(), categories=list(), brands=list(), products=list()):
        self.channels = channels
        self.categories = categories
        self.brands = brands
        self.products = products

    def get_sub_privileges(self, type):
        ids = list()
        if type == 'channels':
