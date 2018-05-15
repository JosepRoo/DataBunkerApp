import csv
import datetime
__author__ = "Luis Ricardo Gutierrez Luna"
from app.common.tree import Tree


class FileToJSONException(Exception):
    def __init__(self, message):
        self.message = message


class FileToJSON:
    def __init__(self, file_name):
        self.file_name = file_name

    def fromCsv(self):
        if "csv" not in self.file_name:
            raise FileToJSONException("File not of type CSV")
        else:
            file = open(self.file_name)
            fileReader = FileToJSON.csv_reader(file)
            next(fileReader, None)
            tree = Tree()
            for row in fileReader:
                if row[6].strip() == '' or not row[6].strip():
                    row[6] = 'Sin Marca'
                if row[8].strip() == '' or not row[8].strip() or row[5].strip() == '' or not row[5].strip():
                    continue
                tree[row[1]][row[2]][row[6]][row[5] + "||" + row[8]] = {
                    "date": row[3], "value": float(row[7].strip("$"))}
            return tree

    @staticmethod
    def csv_reader(file_obj):
        """
        Read a csv file
        """
        #dialect = csv.Sniffer().sniff(file_obj.read(1024))
        file_obj.seek(0)
        #reader = csv.reader(file_obj, dialect)
        reader = csv.reader(file_obj, delimiter=',')
        return reader
