
class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistsError(UserError):
    pass


class InvalidLogin(UserError):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class FavoriteAlreadyAdded(UserError):
    pass


class FavoriteNotFound(UserError):
    pass

