from .signup import SignUp


def add_student_resources(api):
    api.add_resource(
        SignUp,
        '/api/student/signup',
        '/api/student/signup/'
    )
