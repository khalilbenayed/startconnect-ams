import logging
from peewee import (
    IntegrityError,
)
from flask_restful import (
    Resource,
    fields,
    marshal_with,
    reqparse,
)
from models import Student

student_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'state': fields.String,
    'error_message': fields.String,
}
LOGGER = logging.getLogger('student_resource')


class StudentsResource(Resource):
    @marshal_with(student_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True)
        parser.add_argument('last_name', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('state', default='TEST')
        student_args = parser.parse_args()
        try:
            return Student.create(**student_args)
        except IntegrityError:
            error_dict = {
                'error_message': 'Student with email `{}` already exists'.format(student_args.get('email')),
            }
            LOGGER.error(error_dict)
            return error_dict, 400
