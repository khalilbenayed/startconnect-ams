import logging
from peewee import (
    IntegrityError,
    DoesNotExist,
)
from flask_restful import (
    Resource,
    fields,
    marshal_with,
    reqparse,
)
from models import Company
from utils.password_utils import verify_password

LOGGER = logging.getLogger('company_resource')


company_fields = {
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

companies_fields = {
    'companies': fields.List(fields.Nested(company_fields))
}


class CompanyLoginResource(Resource):
    @marshal_with(dict(error_message=fields.String, **company_fields))
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        login_args = parser.parse_args()
        try:
            company = Company.get(email=login_args.get('email'))
        except DoesNotExist:
            error_dict = {
                'error_message': 'No company with this email exists',
            }
            LOGGER.error(error_dict)
            return error_dict, 404
        is_password_correct = verify_password(company.password, login_args.get('password'))
        if is_password_correct:
            return company
        else:
            error_dict = {
                'error_message': 'Incorrect password',
            }
            LOGGER.error(error_dict)
            return error_dict, 401


class CompanyResource(Resource):
    @marshal_with(dict(error_message=fields.String, **company_fields))
    def get(self, company_id):
        try:
            return Company.get(id=company_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Company with id {company_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400


class CompaniesResource(Resource):
    @marshal_with(dict(error_message=fields.String, **company_fields))
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
        try:
            return Company.create(**company_args)
        except IntegrityError:
            error_dict = {
                'error_message': f'Company with email {company_args.get("email")} already exists',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

    @marshal_with(dict(error_message=fields.String, **companies_fields))
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit')
        args = parser.parse_args()
        companies = Company.select().limit(args.get('limit'))
        return {'companies': companies}
