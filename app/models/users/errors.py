from app.models.baseError import BaseError


class UserError(BaseError):
    pass


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

