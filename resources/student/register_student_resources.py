from .student import StudentResource


def add_student_resources(api):
    api.add_resource(
        StudentResource,
        '/api/student',
        '/api/student/'
    )
