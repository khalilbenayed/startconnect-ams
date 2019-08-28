from .students import (
    StudentsResource,
    StudentResource,
    StudentLoginResource,
)
from .student_documents import (
    StudentDocumentsResource,
    StudentDocumentResource
)
from .student_applications import (
    StudentApplicationResource,
    StudentApplicationsResource
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
    api.add_resource(
        StudentDocumentsResource,
        '/api/students/<string:student_id>/student_documents',
        '/api/students/<string:student_id>/student_documents/'
    )
    api.add_resource(
        StudentDocumentResource,
        '/api/students/<string:student_id>/student_documents/<string:document_id>',
        '/api/students/<string:student_id>/student_documents/<string:document_id>/'
    )
    api.add_resource(
        StudentApplicationsResource,
        '/api/students/<string:student_id>/student_applications',
        '/api/students/<string:student_id>/student_applications/'
    )
    api.add_resource(
        StudentApplicationResource,
        '/api/students/<string:student_id>/student_applications/<string:application_id>',
        '/api/students/<string:student_id>/student_applications/<string:application_id>/'
    )
