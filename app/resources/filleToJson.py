from flask_restful import Resource
from app.common.fileToJson import FileToJSON as FTJModel


class FileToJSON(Resource):
    def get(self):
        file_name = r"C:\Users\pauli\Downloads\wm_03May2018.csv"
        fileObject =FTJModel(file_name)
        return fileObject.fromCsv()
