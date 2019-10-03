from flask_restful import fields
from .student_fields import student_fields

document_fields = {
    'id': fields.Integer,
    'student': fields.Nested(student_fields),
    'document_name': fields.String,
    'document_type': fields.String,
    'document_key': fields.String,
    'state': fields.String
}

documents_fields = {
    'total_documents': fields.Integer,
    'documents': fields.List(fields.Nested(document_fields))
}
