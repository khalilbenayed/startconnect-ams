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
    Student,
    STUDENT_STATES,
)
from utils.password_utils import verify_password
from resources.fields import (
    student_fields,
    students_fields,
)

LOGGER = logging.getLogger('student_resource')


class StudentLoginResource(Resource):
    @marshal_with(dict(error_message=fields.String, **student_fields))
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        login_args = parser.parse_args()
        try:
            student = Student.get(email=login_args.get('email'))
        except DoesNotExist:
            error_dict = {
                'error_message': 'No student with this email exists',
            }
            LOGGER.error(error_dict)
            return error_dict, 404
        is_password_correct = verify_password(student.password, login_args.get('password'))
        print(login_args.get('password'))
        if is_password_correct:
            return student
        else:
            error_dict = {
                'error_message': 'Incorrect password',
            }
            LOGGER.error(error_dict)
            return error_dict, 401


class StudentResource(Resource):
    @marshal_with(dict(error_message=fields.String, **student_fields))
    def get(self, student_id):
        try:
            return Student.get(id=student_id)
        except DoesNotExist:
            error_dict = {
                'error_message': 'Student with id `{}` does not exist'.format(student_id),
            }
            LOGGER.error(error_dict)
            return error_dict, 400

    @marshal_with(dict(error_message=fields.String, **student_fields))
    def patch(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('state')
        student_args = {key: val for key, val in parser.parse_args().items() if val is not None}
        if len(student_args) == 0:
            error_dict = {
                'error_message': f'Empty payload',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        if 'state' in student_args and student_args.get('state') not in STUDENT_STATES:
            error_dict = {
                'error_message': f'Invalid state {student_args.get("state")}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        try:
            student = Student.get(id=student_id)
            for key, val in student_args.items():
                setattr(student, key, val)
            student.save()
            return student
        except DoesNotExist:
            error_dict = {
                'error_message': f'Student with id {student_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

    @marshal_with(dict(error_message=fields.String, **student_fields))
    def delete(self, student_id):
        pass


class StudentsResource(Resource):
    @marshal_with(dict(error_message=fields.String, **student_fields))
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True)
        parser.add_argument('last_name', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('state', default='ACTIVE')
        student_args = parser.parse_args()
        if student_args.get('state') not in STUDENT_STATES:
            error_dict = {
                'error_message': f'Invalid state {student_args.get("state")}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        try:
            return Student.create(**student_args)
        except IntegrityError as e:
            error_dict = {
                'error_message': e,
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        except Exception as e:
            LOGGER.error(e)

    @marshal_with(dict(error_message=fields.String, **students_fields))
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit')
        parser.add_argument('email')
        args = parser.parse_args()
        students = Student.select()
        if args.get('email') is not None:
            students = students.where(Student.email == args.get('email'))
        students = students.limit(args.get('limit'))
        return {'students': students}
