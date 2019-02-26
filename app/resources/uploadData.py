from flask import request
from flask_restful import Resource

from app import Response
from app.common.tree import Tree


class UploadData(Resource):
    def post(self):
        try:
            json = request.get_json(force=True)
            tree = Tree(json)
            result = tree.save_to_mongo()
            result['message'] = "La informacion se subio exitosamente"
            result['success'] = True
        except Exception as e:
            return Response(
                message=f"Ocurrio un error al subir informacion, notificar al administrador:\n{str(e)}").json(), 500
        return result, 200
