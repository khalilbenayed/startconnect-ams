from .jobs import (
    JobsResource,
    JobResource,
)


def add_job_resources(api):
    api.add_resource(
        JobsResource,
        '/api/jobs',
        '/api/jobs/'
    )
    api.add_resource(
        JobResource,
        '/api/jobs/<string:job_id>',
        '/api/jobs/<string:job_id>/',
    )
