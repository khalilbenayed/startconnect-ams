from .company import CompanyResource


def add_company_resources(api):
    api.add_resource(
        CompanyResource,
        '/api/company',
        '/api/company/'
    )
