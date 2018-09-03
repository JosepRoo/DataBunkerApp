import datetime


class Log:
    def __init__(self, value, date, created_date=None):
        self.value = value
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M") if type(date) == str else date
        self.created_date = created_date if created_date else datetime.datetime.now()

    def json(self, exclude=None, date_to_string=True):
        if date_to_string:
            if exclude:
                return {attrib: self.__getattribute__(attrib).strftime("%Y-%m-%d %H:%M")
                        if type(self.__getattribute__(attrib)) is datetime.datetime
                        else self.__getattribute__(attrib)
                        for attrib in self.__dict__.keys() if attrib not in exclude}

            return {attrib: self.__getattribute__(attrib).strftime("%Y-%m-%d %H:%M")
                    if type(self.__getattribute__(attrib)) is datetime.datetime
                    else self.__getattribute__(attrib)
                    for attrib in self.__dict__.keys()}
        else:
            if exclude:
                return {attrib: self.__getattribute__(attrib)
                        for attrib in self.__dict__.keys() if attrib not in exclude}
            return {attrib: self.__getattribute__(attrib)
                    for attrib in self.__dict__.keys()}

    def __repr__(self):
        return f"{self.__class__.__name__} date={self.date}, value={self.value}"