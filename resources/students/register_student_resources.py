from .students import (
    StudentsResource,
    StudentResource,
    StudentLoginResource,
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
    api.add_resource(
        StudentLoginResource,
        '/api/students/login',
        '/api/students/login/'
    )
