from flask_restful import fields

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