from .companies import (
    CompaniesResource,
    CompanyResource,
    CompanyLoginResource,
)
from .company_jobs import (
    CompanyJobResource,
    CompanyJobsResource,
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
        '/api/companies/<string:company_id>/jobs/<string:job_id>/',
    )
