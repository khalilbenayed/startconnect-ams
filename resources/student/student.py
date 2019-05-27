from flask_restful import (
    Resource,
    fields,
    marshal_with,
    reqparse,
)
from models import Student

student_fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'state': fields.String
}


class Student(Resource):
    @marshal_with(student_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True)
        parser.add_argument('last_name', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('state', default='TEST')
        student_args = parser.parse_args()
        return Student.create(**student_args)
