from __future__ import annotations
import datetime
import uuid
from dataclasses import dataclass

from mongoengine.base import BaseDict
from mongoengine.base.datastructures import BaseList
from mongoengine import *


@dataclass(init=False)
class BaseEmbeddedDocument(EmbeddedDocument):
    meta = {'allow_inheritance': True,
            'abstract': True}

    # TODO for futue development move this to utils to cply with DRY to cply with DRY
    def json(self, exclude: set = None, date_to_string: bool = True) -> dict:
        """
        Transforms a Python object to a dictionary to be able to send as JSON.
        if exclude is set, it will not add the fields set on exclude on the resultant json,
        if date_to_string is True it will transform Datetime obejct to strings, if is false they will remain as objects
        :param exclude: set
        :param date_to_string: bool
        :return: dict
        """
        result = dict()
        for attrib in self._data:
            if (exclude is not None and attrib in exclude) or attrib == '_cls':
                continue
            attrib_value = self.__getattribute__(attrib)
            # print(self.__class__.__name__, attrib, type(attrib_value))
            if type(attrib_value) is list or type(attrib_value) is BaseList:
                result[attrib] = list()
                for element in attrib_value:
                    if type(element) is datetime.datetime and date_to_string:
                        result[attrib].append(element.strftime("%Y-%m-%d %H:%M"))
                    elif not isinstance(element, str) and not isinstance(element, int) and not isinstance(element,
                                                                                                          datetime.datetime):
                        result[attrib].append(element.json(date_to_string=date_to_string, exclude=exclude))
                    else:
                        result[attrib].append(element)
            elif type(attrib_value) is None:
                result[attrib] = attrib_value
            elif type(attrib_value) is datetime.datetime and date_to_string:
                result[attrib] = attrib_value.strftime("%Y-%m-%d %H:%M")
            elif type(attrib_value) not in [str, int, float, dict, set, list, bool, BaseDict]:
                result[attrib] = attrib_value.json(date_to_string=date_to_string, exclude=exclude)
            else:
                result[attrib] = attrib_value
        # print(result)
        return result

    # TODO for futue development move this to utils to cply with DRY
    @classmethod
    def get_by_id(cls, _id: str) -> BaseEmbeddedDocument or None:
        """
        Returns the user object with the given id, or raises an exception if that user was not found
        :param _id: id of the user to find
        :return: user object
        """
        obj = cls.objects(_id=_id)
        if obj:
            return obj[0]

    # TODO for futue development move this to utils to cply with DRY
    @classmethod
    def fn_update_object_util(cls, primary_value: str, data: dict,
                              exclude_data: set = None, update: bool = False) -> BaseEmbeddedDocument:
        obj = cls.get_by_id(primary_value)
        if exclude_data is not None:
            [data.pop(key, None) for key in exclude_data]
        for key, value in data.items():
            if value is None:
                continue
            setattr(obj, key, value)
        if update:
            obj.save()
        return obj
