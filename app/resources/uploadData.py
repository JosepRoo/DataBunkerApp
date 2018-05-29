from flask import request
from flask_restful import Resource

from app import Response
from app.common.tree import Tree


class UploadData(Resource):
    def post(self):
        try:
            json = request.get_json(force=True)
            tree = Tree(json)
            tree.save_to_mongo()
        except:
            return Response(message="Ocurrio un error al subir informacion, notificar al administrador").json()
        return Response(success=True,message="La informacion se subio exitosamente").json()