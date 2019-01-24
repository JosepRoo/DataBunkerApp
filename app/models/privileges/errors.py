class PrivilegeErrors(Exception):
    def __init__(self, message):
        self.message = message


class WrongElementType(PrivilegeErrors):
    pass


class WrongPrivilegeAssignment(PrivilegeErrors):
    pass


class PrivilegeDoesNotExist(PrivilegeErrors):
    pass
