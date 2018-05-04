

class CompanyError(Exception):
    def __init__(self, message):
        self.message = message


class CompanyAlreadyExists(CompanyError):
    pass