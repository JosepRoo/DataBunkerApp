import datetime

from app import Database


class Log:
    def __init__(self, value, date, created_date=None):
        self.value = value
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M") if type(date) == str else date
        self.created_date = created_date if created_date else datetime.datetime.now()

    def json(self, exclude=None):
        if exclude:
            return {attrib: [element.json() for element in self.__getattribute__(attrib)]
                    if type(self.__getattribute__(attrib)) is list
                    else self.__getattribute__(attrib).strftime("%Y-%m-%d %H:%M")
                    if type(self.__getattribute__(attrib)) is datetime.datetime
                    else self.__getattribute__(attrib)
                    for attrib in self.__dict__.keys() if attrib not in exclude}

        return {attrib: [element.json() for element in self.__getattribute__(attrib)]
                if type(self.__getattribute__(attrib)) is list
                else self.__getattribute__(attrib).strftime("%Y-%m-%d %H:%M")
                if type(self.__getattribute__(attrib)) is datetime.datetime
                else self.__getattribute__(attrib)
                for attrib in self.__dict__.keys()}