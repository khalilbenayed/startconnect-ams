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

LOGGER = logging.getLogger('student_resource')

student_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'state': fields.String,
}

students_fields = {
    'students': fields.List(fields.Nested(student_fields))
}


class StudentsResource(Resource):
    @marshal_with(dict(error_message=fields.String, **student_fields))
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

    @marshal_with(dict(error_message=fields.String, **students_fields))
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit')
        args = parser.parse_args()
        students_query = Student.select().limit(args.get('limit'))
        students = [
            {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'state': student.state,
            } for student in students_query
        ]
        return {'students': students}
