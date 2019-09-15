from .companies import (
    CompaniesResource,
    CompanyResource,
    CompanyLoginResource,
)
from .company_jobs import (
    CompanyJobResource,
    CompanyJobsResource,
)
from .company_job_applications import (
    CompanyJobApplicationResource,
    CompanyJobApplicationsResource
)


def add_company_resources(api):
    api.add_resource(
        CompaniesResource,
        '/api/companies',
        '/api/companies/'
    )
    api.add_resource(
        CompanyResource,
        '/api/companies/<string:company_id>',
        '/api/companies/<string:company_id>/'
    )
    api.add_resource(
        CompanyLoginResource,
        '/api/companies/login',
        '/api/companies/login/'
    )
    api.add_resource(
        CompanyJobsResource,
        '/api/companies/<string:company_id>/jobs',
        '/api/companies/<string:company_id>/jobs/'
    )
    api.add_resource(
        CompanyJobResource,
        '/api/companies/<string:company_id>/jobs/<string:job_id>',
        '/api/companies/<string:company_id>/jobs/<string:job_id>/'
    )
    api.add_resource(
        CompanyJobApplicationsResource,
        '/api/companies/<string:company_id>/jobs/<string:job_id>/applications',
        '/api/companies/<string:company_id>/jobs/<string:job_id>/applications/'
    )
    api.add_resource(
        CompanyJobApplicationResource,
        '/api/companies/<string:company_id>/jobs/<string:job_id>/applications/<string:application_id>',
        '/api/companies/<string:company_id>/jobs/<string:job_id>/applications/<string:application_id>/'
    )
