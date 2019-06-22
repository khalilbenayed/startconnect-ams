from .jobs import (
    JobsResource,
    JobResource,
)


def add_job_resources(api):
    api.add_resource(
        JobsResource,
        '/api/companies/<string:company_id>/jobs',
        '/api/companies/<string:company_id>/jobs/'
    )
    api.add_resource(
        JobResource,
        '/api/companies/<string:company_id>/jobs/<string:job_id>',
        '/api/companies/<string:company_id>/jobs/<string:job_id>/',
    )
