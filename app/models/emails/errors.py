class EmailErrors(Exception):
    def __init__(self, message):
        self.message = message


class FailedToSendEmail(EmailErrors):
    pass


