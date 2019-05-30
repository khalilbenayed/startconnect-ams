from .students import (
    StudentsResource,
    StudentResource,
)


def add_student_resources(api):
    api.add_resource(
        StudentsResource,
        '/api/students',
        '/api/students/'
    )
    api.add_resource(
        StudentResource,
        '/api/students/<string:student_id>',
        '/api/students/<string:student_id>/'
    )
