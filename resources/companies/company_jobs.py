import logging
import datetime
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
    'duration': fields.Integer,
    'start_date': fields.DateTime,
    'expiry_date': fields.DateTime,
    'quote': fields.Integer,
    'hourly_wage': fields.Integer,
    'weekly_hours': fields.Integer,
    'total_hours': fields.Integer,
    'due_date': fields.DateTime,
}

jobs_fields = {
    'total_jobs': fields.Integer,
    'jobs': fields.List(fields.Nested(job_fields))
}


class CompanyJobResource(Resource):
    @marshal_with(dict(error_message=fields.String, **job_fields))
    def get(self, company_id, job_id):
        # check company exists
        try:
            Company.get(id=company_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Company with id {company_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        try:
            return Job.get(id=job_id, company=company_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Job with id `{job_id}` does not exist for company with id {company_id}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400


class CompanyJobsResource(Resource):
    @marshal_with(dict(error_message=fields.String, **job_fields))
    def post(self, company_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('description', required=True)
        parser.add_argument('category', required=True)
        parser.add_argument('state', default='NEW')
        parser.add_argument('type', required=True)
        parser.add_argument('n_positions', required=True, type=int)
        parser.add_argument('duration', required=True, type=int)
        parser.add_argument('start_date', required=True, type=int)
        parser.add_argument('expiry_date', required=True, type=int)
        parser.add_argument('quote', type=int)
        parser.add_argument('hourly_wage', type=int)
        parser.add_argument('weekly_hours', type=int)
        parser.add_argument('total_hours', type=int)
        parser.add_argument('due_date', type=int)
        job_args = parser.parse_args()

        # check company exists
        try:
            Company.get(id=company_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Company with id {company_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        # check type is valid
        if job_args.get('type') not in JOB_TYPES:
            error_dict = {
                'error_message': f'Unknown type: {job_args.get("type")}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        # convert timestamps to datetime
        job_args['start_date'] = datetime.datetime.fromtimestamp(job_args.get('start_date'))
        job_args['expiry_date'] = datetime.datetime.fromtimestamp(job_args.get('expiry_date'))

        # check extra parameters by job type
        if job_args.get('type') == 'CONTRACT':
            # require quote, total hours and due date
            if not ('quote' in job_args and 'total_hours' in job_args and 'due_date' in job_args):
                error_dict = {
                    'error_message': 'Must specify quote, total hours and due date for contract jobs.',
                }
                LOGGER.error(error_dict)
                return error_dict, 400
            job_args['due_date'] = datetime.datetime.fromtimestamp(job_args.get('due_date'))
        elif job_args.get('type') == 'PAID_INTERNSHIP':
            # require hourly wage and weekly hours
            if not ('hourly_wage' in job_args and 'weekly_hours' in job_args):
                error_dict = {
                    'error_message': 'Must specify hourly wage and weekly hours for internship jobs.',
                }
                LOGGER.error(error_dict)
                return error_dict, 400

        return Job.create(company=company_id, **job_args)

    @marshal_with(dict(error_message=fields.String, **jobs_fields))
    def get(self, company_id):
        parser = reqparse.RequestParser()
        parser.add_argument('page_number', type=int)
        parser.add_argument('number_of_jobs_per_page', type=int)
        parser.add_argument('type')
        args = parser.parse_args()

        # check company exists
        try:
            company = Company.get(id=company_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Company with id {company_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        jobs = company.jobs
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
