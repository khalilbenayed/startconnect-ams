from .companies import (
    CompaniesResource,
    CompanyResource,
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
