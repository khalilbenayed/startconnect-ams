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
from models import (
    Company,
    COMPANY_STATES,
)
from utils.password_utils import verify_password

LOGGER = logging.getLogger('company_resource')


company_fields = {
    'id': fields.Integer,
    'company_name': fields.String,
    'email': fields.String,
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

    @marshal_with(dict(error_message=fields.String, **company_fields))
    def patch(self, company_id):
        parser = reqparse.RequestParser()
        parser.add_argument('company_name')
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('address_1')
        parser.add_argument('address_2')
        parser.add_argument('city')
        parser.add_argument('province')
        parser.add_argument('zipcode')
        parser.add_argument('country')
        parser.add_argument('phone')
        parser.add_argument('state')
        company_args = {key: val for key, val in parser.parse_args().items() if val is not None}
        if len(company_args) == 0:
            error_dict = {
                'error_message': f'Empty payload',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        if 'state' in company_args and company_args.get('state') not in COMPANY_STATES:
            error_dict = {
                'error_message': f'Invalid state {company_args.get("state")}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        try:
            company = Company.get(id=company_id)
            for key, val in company_args.items():
                setattr(company, key, val)
            company.save()
            return company
        except DoesNotExist:
            error_dict = {
                'error_message': f'Company with id {company_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

    @marshal_with(dict(error_message=fields.String, **company_fields))
    def delete(self, company_id):
        pass


class CompaniesResource(Resource):
    @marshal_with(dict(error_message=fields.String, **company_fields))
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('company_name', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('address_1')
        parser.add_argument('address_2')
        parser.add_argument('city')
        parser.add_argument('province')
        parser.add_argument('zipcode')
        parser.add_argument('country')
        parser.add_argument('phone')
        parser.add_argument('state', default='NOT_VERIFIED')
        company_args = parser.parse_args()
        if company_args.get('state') not in COMPANY_STATES:
            error_dict = {
                'error_message': f'Invalid state {company_args.get("state")}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        try:
            return Company.create(**company_args)
        except IntegrityError as e:
            error_dict = {
                'error_message': e,
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        except Exception as e:
            LOGGER.error(e)

    @marshal_with(dict(error_message=fields.String, **companies_fields))
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit')
        parser.add_argument('email')
        args = parser.parse_args()
        companies = Company.select()
        if args.get('email') is not None:
            companies = companies.where(Company.email == args.get('email'))
        companies = companies.limit(args.get('limit'))
        return {'companies': companies}
