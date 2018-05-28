from flask import request
from flask_restful import Resource

from app import Response
from app.common.tree import Tree


class UploadData(Resource):
    def post(self):
        json = request.json
        tree = Tree(json)
        try:
            tree.save_to_mongo()
        except:
            return Response(message="La informacion esta en un formato no valido intentelo nuevamente").json()
        return Response(success=True,message="La informacion se subio exitosamente").json()