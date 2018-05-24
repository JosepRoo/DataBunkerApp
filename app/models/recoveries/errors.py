class RecoveryError(Exception):
    def __init__(self, message):
        self.message = message


class UnableToRecoverPassword(RecoveryError):
    pass