import logging
import uuid
import werkzeug
from peewee import (
    IntegrityError,
    DoesNotExist,
)
from flask import send_from_directory
from flask_restful import (
    Resource,
    fields,
    marshal_with,
    reqparse,
)
from models import (
    Student,
    StudentDocument,
    DOCUMENT_TYPES,
)
from resources.students.students import student_fields
from utils.document_utils import create_document


LOGGER = logging.getLogger('student_document_resource')

document_fields = {
    'id': fields.Integer,
    'student': fields.Nested(student_fields),
    'document_name': fields.String,
    'document_type': fields.String,
    'document_key': fields.String
}

documents_fields = {
    'total_documents': fields.Integer,
    'documents': fields.List(fields.Nested(document_fields))
}


class StudentDocumentResource(Resource):
    def get(self, student_id, document_id):
        # check student exists
        try:
            Student.get(id=student_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Student with id {student_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        try:
            student_document = StudentDocument.get(id=document_id, student=student_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Document with id `{document_id}` does not exist for student with id {student_id}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        return send_from_directory('tmp/', student_document.document_name, as_attachment=True)


class StudentDocumentsResource(Resource):
    @marshal_with(dict(error_message=fields.String, **document_fields))
    def post(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument('document', type=werkzeug.datastructures.FileStorage, location='files', required=True)
        parser.add_argument('document_type', required=True)
        parser.add_argument('document_name')
        document_args = parser.parse_args()

        # check student exists
        try:
            student = Student.get(id=student_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Student with id {student_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        if student.is_active() is False:
            error_dict = {
                'error_message': f'Account for student with id {student_id} is not active.',
            }
            LOGGER.error(error_dict)
            return error_dict, 403

        document = document_args.get('document')
        try:
            return create_document(
                student_id,
                document,
                document_args.get('document_type'),
                document_args.get('document_name')
            )
        except IntegrityError as e:
            error_dict = {
                'error_message': e,
            }
            LOGGER.error(error_dict)
            return error_dict, 400

    @marshal_with(dict(error_message=fields.String, **documents_fields))
    def get(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument('page_number', type=int)
        parser.add_argument('number_of_documents_per_page', type=int)
        parser.add_argument('document_type')
        args = parser.parse_args()

        # check company exists
        try:
            student = Student.get(id=student_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Student with id {student_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        documents = student.documents
        if args.get('type') is not None:
            if args.get('type') not in DOCUMENT_TYPES:
                error_dict = {
                    'error_message': f'Unknown type: {args.get("type")}',
                }
                LOGGER.error(error_dict)
                return error_dict, 400
            documents = documents.where(StudentDocument.type == args.get('type'))
        total_documents = len(documents)
        if args.get('page_number') is not None and args.get('number_of_documents_per_page') is not None:
            documents = documents.paginate(
                args.get('page_number'),
                args.get('number_of_documents_per_page'))
        return {
            'total_documents': total_documents,
            'documents': documents
        }
