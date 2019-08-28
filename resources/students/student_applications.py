import logging
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
    Job,
    Application
)
from resources.students.students import student_fields
from resources.students.student_documents import document_fields
from resources.companies.company_jobs import job_fields
from utils.document_utils import create_document


LOGGER = logging.getLogger('application_resource')

application_fields = {
    'id': fields.Integer,
    'student': fields.Nested(student_fields),
    'job': fields.Nested(job_fields),
    'resume': fields.Nested(document_fields),
    'cover_letter': fields.Nested(document_fields),
    'transcript': fields.Nested(document_fields),
    'state': fields.String,
    'created_at': fields.DateTime
}

applications_fields = {
    'total_applications': fields.Integer,
    'applications': fields.List(fields.Nested(document_fields))
}


class StudentApplicationResource(Resource):
    @marshal_with(dict(error_message=fields.String, **application_fields))
    def get(self, student_id, application_id):
        pass


class StudentApplicationsResource(Resource):
    @marshal_with(dict(error_message=fields.String, **applications_fields))
    def get(self, student_id):
        pass

    @marshal_with(dict(error_message=fields.String, **application_fields))
    def post(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument('job_id', required=True)
        parser.add_argument('resume_id', type=int)
        parser.add_argument('cover_letter_id', type=int)
        parser.add_argument('transcript_id', type=int)
        parser.add_argument('resume', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('cover_letter', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('transcript', type=werkzeug.datastructures.FileStorage, location='files')
        application_args = parser.parse_args()

        job_id = application_args.get('job_id')
        resume_id = application_args.get('resume_id')
        cover_letter_id = application_args.get('cover_letter_id')
        transcript_id = application_args.get('transcript_id')

        # check student exists
        try:
            student = Student.get(id=student_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Student with id {student_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        # check job exists
        try:
            job = Job.get(id=job_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Job with id {job_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        # student didn't already apply for the same job
        count_applications = (Application
                              .select()
                              .where((Application.job == job_id) & (Application.student == student_id))
                              .count())
        if count_applications != 0:
            error_dict = {
                'error_message': f'Student {student_id} already applied for job {job_id}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        resume, cover_letter, transcript = None, None, None
        if resume_id is None:
            resume_file = application_args.get('resume')
            if resume_file is None:
                error_dict = {
                    'error_message': f'Cannot apply without resume',
                }
                LOGGER.error(error_dict)
                return error_dict, 400

            try:
                resume = create_document(student_id, resume_file, 'resume')
            except IntegrityError as e:
                error_dict = {
                    'error_message': f'error creating resume: {e}',
                }
                LOGGER.error(error_dict)
                return error_dict, 400
        else:
            try:
                resume = StudentDocument.get(id=resume_id)
            except DoesNotExist:
                error_dict = {
                    'error_message': f'Document with id {resume_id} does not exist',
                }
                LOGGER.error(error_dict)
                return error_dict, 400

        if cover_letter_id is None:
            cover_letter_file = application_args.get('cover_letter')
            if cover_letter_file is not None:
                try:
                    cover_letter = create_document(student_id, cover_letter_file, 'cover_letter')
                except IntegrityError as e:
                    error_dict = {
                        'error_message': f'error creating cover letter: {e}',
                    }
                    LOGGER.error(error_dict)
                    return error_dict, 400
        else:
            try:
                cover_letter = StudentDocument.get(id=cover_letter_id)
            except DoesNotExist:
                error_dict = {
                    'error_message': f'Document with id {cover_letter_id} does not exist',
                }
                LOGGER.error(error_dict)
                return error_dict, 400

        if transcript_id is None:
            transcript_file = application_args.get('transcript')
            if transcript_file is None:
                try:
                    transcript = create_document(student_id, transcript_file, 'transcript')
                except IntegrityError as e:
                    error_dict = {
                        'error_message': f'error creating transcript: {e}',
                    }
                    LOGGER.error(error_dict)
                    return error_dict, 400
        else:
            try:
                transcript = StudentDocument.get(id=transcript_id)
            except DoesNotExist:
                error_dict = {
                    'error_message': f'Document with id {transcript_id} does not exist',
                }
                LOGGER.error(error_dict)
                return error_dict, 400

        try:
            return Application.create(
                student=student_id,
                job=job.id,
                resume=resume.id,
                cover_letter=cover_letter.id if cover_letter is not None else None,
                transcript=transcript.id if transcript is not None else None,
                state='New'
            )
        except IntegrityError as e:
            error_dict = {
                'error_message': e,
            }
            LOGGER.error(error_dict)
            return error_dict, 400
