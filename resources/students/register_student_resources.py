from .students import StudentsResource


def add_student_resources(api):
    api.add_resource(
        StudentsResource,
        '/api/students',
        '/api/students/'
    )
