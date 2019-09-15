from flask_restful import fields
from .company_fields import company_fields

job_fields = {
    'id': fields.Integer,
    'company': fields.Nested(company_fields),
    'title': fields.String,
    'category': fields.String,
    'description': fields.String,
    'type': fields.String,
    'state': fields.String,
    'n_positions': fields.Integer,
    'duration': fields.String,
    'start_date': fields.DateTime,
    'expiry_date': fields.DateTime,
    'city': fields.String,
    'compensation': fields.String,
}

jobs_fields = {
    'total_jobs': fields.Integer,
    'jobs': fields.List(fields.Nested(job_fields))
}
