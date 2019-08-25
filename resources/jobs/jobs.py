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
    Job,
    JOB_TYPES,
)
from resources.companies.companies import company_fields

LOGGER = logging.getLogger('job_resource')

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


class JobResource(Resource):
    @marshal_with(dict(error_message=fields.String, **job_fields))
    def get(self, job_id):
        try:
            return Job.get(id=job_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Job with id `{job_id}` does not exist.',
            }
            LOGGER.error(error_dict)
            return error_dict, 400


class JobsResource(Resource):
    @marshal_with(dict(error_message=fields.String, **jobs_fields))
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page_number', type=int)
        parser.add_argument('number_of_jobs_per_page', type=int)
        parser.add_argument('type')
        args = parser.parse_args()

        jobs = Job.select()
        if args.get('type') is not None:
            if args.get('type') not in JOB_TYPES:
                error_dict = {
                    'error_message': f'Unknown type: {args.get("type")}',
                }
                LOGGER.error(error_dict)
                return error_dict, 400
            jobs = jobs.where(Job.type == args.get('type'))
        total_jobs = len(jobs)
        if args.get('page_number') is not None and args.get('number_of_jobs_per_page') is not None:
            jobs = jobs.paginate(args.get('page_number'), args.get('number_of_jobs_per_page'))
        return {
            'total_jobs': total_jobs,
            'jobs': jobs
        }
