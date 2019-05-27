from .student import Student


def add_student_resources(api):
    api.add_resource(
        Student,
        '/api/student',
        '/api/student/'
    )
