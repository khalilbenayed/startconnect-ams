from .companies import CompaniesResource


def add_company_resources(api):
    api.add_resource(
        CompaniesResource,
        '/api/companies',
        '/api/companies/'
    )
