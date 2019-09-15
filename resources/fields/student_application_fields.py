from flask_restful import fields
from .student_document_fields import document_fields
from .student_fields import student_fields
from .company_job_fields import job_fields

application_fields = {
    'id': fields.Integer,
    'student': fields.Nested(student_fields),
    'job': fields.Nested(job_fields),
    'resume': fields.Nested(document_fields),
    'cover_letter': fields.Nested(document_fields, allow_null=True),
    'transcript': fields.Nested(document_fields, allow_null=True),
    'state': fields.String,
    'created_at': fields.DateTime
}

applications_fields = {
    'total_applications': fields.Integer,
    'applications': fields.List(fields.Nested(application_fields))
}