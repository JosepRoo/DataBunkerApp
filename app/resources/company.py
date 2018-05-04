from flask_restful import Resource, reqparse

from app.common.response import Response
from app.models.companies.company import Company as CompanyModel
from app.models.companies.errors import CompanyError


class Company(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def get(self, _id=None):
        if _id:
            return CompanyModel.get_company_by_id(_id).get_users().json(), 200
        return {"companies": [company.get_users().json() for company in CompanyModel.get_all_companies()]}, 200

    def post(self, _id=None):
        data = Company.parser.parse_args()
        try:
            company = CompanyModel.register(data)
            return company.json(), 200
        except CompanyError as e:
            return Response(message=e.message).json()

    def delete(self, _id):
        company = CompanyModel.get_company_by_id(_id)
        company.delete_company()
        return Response(success=True, message="Empresa {} borrada".format(company.name))

