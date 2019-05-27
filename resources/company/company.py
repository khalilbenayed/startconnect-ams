from flask_restful import (
    Resource,
    fields,
    marshal_with,
    reqparse,
)
from models import Company

student_fields = {
    'id': fields.String,
    'company_name': fields.String,
    'email': fields.String,
    'password': fields.String,
    'address_1': fields.String,
    'address_2': fields.String,
    'city': fields.String,
    'province': fields.String,
    'zipcode': fields.String,
    'country': fields.String,
    'phone': fields.String,
    'state': fields.String,
}


class CompanyResource(Resource):
    @marshal_with(student_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('company_name', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('address_1', required=True)
        parser.add_argument('address_2', required=False)
        parser.add_argument('city', required=True)
        parser.add_argument('province', required=True)
        parser.add_argument('zipcode', required=True)
        parser.add_argument('country', required=True)
        parser.add_argument('phone', required=True)
        parser.add_argument('state', default='TEST')
        company_args = parser.parse_args()
        return Company.create(**company_args)
