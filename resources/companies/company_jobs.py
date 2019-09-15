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
    JOB_STATES
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

    @marshal_with(dict(error_message=fields.String, **job_fields))
    def patch(self, company_id, job_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('description')
        parser.add_argument('state')
        parser.add_argument('n_positions', type=int)
        parser.add_argument('duration')
        parser.add_argument('start_date', type=int)
        parser.add_argument('expiry_date', type=int)
        parser.add_argument('compensation')
        parser.add_argument('city')
        job_args = {key: val for key, val in parser.parse_args().items() if val is not None}
        if len(job_args) == 0:
            error_dict = {
                'error_message': f'Empty payload',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        if 'state' in job_args and job_args.get('state') not in JOB_STATES:
            error_dict = {
                'error_message': f'Invalid state {job_args.get("state")}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        try:
            job = Job.get(id=job_id)
            if job.company.id != int(company_id):
                error_dict = {
                    'error_message': f'Job with id {job_id} does not exist for company {company_id}',
                }
                LOGGER.error(error_dict)
                return error_dict, 400
            for key, val in job_args.items():
                setattr(job, key, val)
            job.save()
            return job
        except DoesNotExist:
            error_dict = {
                'error_message': f'Job with id {job_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

    @marshal_with(dict(error_message=fields.String, **job_fields))
    def delete(self, company_id, job_id):
        pass


class CompanyJobsResource(Resource):
    @marshal_with(dict(error_message=fields.String, **job_fields))
    def post(self, company_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('description', required=True)
        parser.add_argument('category')
        parser.add_argument('state', default='NEW')
        parser.add_argument('type', required=True)
        parser.add_argument('n_positions', required=True, type=int)
        parser.add_argument('duration', required=True)
        parser.add_argument('start_date', type=int)
        parser.add_argument('expiry_date', type=int)
        parser.add_argument('compensation', required=True)
        parser.add_argument('city')
        job_args = parser.parse_args()

        # check company exists
        try:
            company = Company.get(id=company_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Company with id {company_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        # if company.has_address() is False:
        #     error_dict = {
        #         'error_message': f'Account for company with id {company_id} does not have an address.',
        #     }
        #     LOGGER.error(error_dict)
        #     return error_dict, 403

        # if company.is_active() is False:
        #     error_dict = {
        #         'error_message': f'Account for company with id {company_id} is not active.',
        #     }
        #     LOGGER.error(error_dict)
        #     return error_dict, 403

        # check type is valid
        if job_args.get('type') not in JOB_TYPES:
            error_dict = {
                'error_message': f'Unknown type: {job_args.get("type")}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        # convert timestamps to datetime
        # job_args['start_date'] = datetime.datetime.fromtimestamp(job_args.get('start_date'))
        # job_args['expiry_date'] = datetime.datetime.fromtimestamp(job_args.get('expiry_date'))

        # if city is none use city in address by default
        if job_args.get('city') is None or job_args.get('city') == '':
            job_args['city'] = company.city

        try:
            return Job.create(company=company_id, **job_args)
        except IntegrityError as e:
            error_dict = {
                'error_message': e,
            }
            LOGGER.error(error_dict)
            return error_dict, 400

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

        jobs = company.jobs.where(Job.state != 'DELETED')
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
