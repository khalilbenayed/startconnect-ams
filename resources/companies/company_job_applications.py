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
    Application,
)
from resources.fields import (
    application_fields,
    applications_fields
)

LOGGER = logging.getLogger('application_resource')

class CompanyJobApplicationResource(Resource):
    @marshal_with(dict(error_message=fields.String, **application_fields))
    def get(self, company_id, job_id, application_id):
        # check job exists
        try:
            Job.get(id=job_id, company=company_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Job with id {job_id} does not exist for company {company_id}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        try:
            return Application.get(id=application_id, job=job_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Application with id `{application_id}` does not exist'
                                 f' for job with id {job_id}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400


class CompanyJobApplicationsResource(Resource):
    @marshal_with(dict(error_message=fields.String, **applications_fields))
    def get(self, company_id, job_id):
        parser = reqparse.RequestParser()
        parser.add_argument('page_number', type=int)
        parser.add_argument('number_of_applications_per_page', type=int)
        args = parser.parse_args()

        # check job exists
        try:
            job = Job.get(id=job_id, company=company_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Job with id {job_id} does not exist for company {company_id}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        applications = job.applications.where(Application.state != 'CANCELLED')
        total_applications = len(applications)
        if args.get('page_number') is not None and args.get('number_of_applications_per_page') is not None:
            applications = applications.paginate(
                args.get('page_number'),
                args.get('number_of_documents_per_page'))
        return {
            'total_applications': total_applications,
            'applications': applications
        }

