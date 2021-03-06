import logging
from peewee import (
    IntegrityError,
    DoesNotExist,
)
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
    Application,
    APPLICATION_STATES
)
from resources.fields import (
    application_fields,
    applications_fields
)

LOGGER = logging.getLogger('application_resource')


class StudentApplicationResource(Resource):
    @marshal_with(dict(error_message=fields.String, **application_fields))
    def get(self, student_id, application_id):
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
            return Application.get(id=application_id, student=student_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Application with id `{application_id}` does not exist'
                                 f' for student with id {student_id}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

    @marshal_with(dict(error_message=fields.String, **application_fields))
    def patch(self, student_id, application_id):
        parser = reqparse.RequestParser()
        parser.add_argument('state')
        application_args = parser.parse_args()
        state = application_args.get('state')

        if state is None:
            error_dict = {
                'error_message': f'Empty payload',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        if state not in APPLICATION_STATES:
            error_dict = {
                'error_message': f'Invalid state {state}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400
        try:
            application = Application.get(id=application_id, student=student_id)
            application.state = state
            application.save()
            return application
        except DoesNotExist:
            error_dict = {
                'error_message': f'Application with id `{application_id}` does not exist'
                                 f' for student with id {student_id}',
            }
            LOGGER.error(error_dict)
            return error_dict, 400


class StudentApplicationsResource(Resource):
    @marshal_with(dict(error_message=fields.String, **applications_fields))
    def get(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument('page_number', type=int)
        parser.add_argument('number_of_documents_per_page', type=int)
        args = parser.parse_args()

        # check student exists
        try:
            student = Student.get(id=student_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Student with id {student_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        applications = student.applications
        total_applications = len(applications)
        if args.get('page_number') is not None and args.get('number_of_documents_per_page') is not None:
            applications = applications.paginate(
                args.get('page_number'),
                args.get('number_of_documents_per_page'))
        return {
            'total_applications': total_applications,
            'applications': applications
        }

    @marshal_with(dict(error_message=fields.String, **application_fields))
    def post(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument('job_id', required=True)
        parser.add_argument('resume_id', type=int, required=True)
        parser.add_argument('cover_letter_id', type=int)
        parser.add_argument('transcript_id', type=int)
        application_args = parser.parse_args()

        job_id = application_args.get('job_id')
        resume_id = application_args.get('resume_id')
        cover_letter_id = application_args.get('cover_letter_id')
        transcript_id = application_args.get('transcript_id')

        # check student exists and is active
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

        # check job exists and is new
        try:
            job = Job.get(id=job_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Job with id {job_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        if job.is_new() is False:
            error_dict = {
                'error_message': f'Job with id {job_id} is expired or deleted.',
            }
            LOGGER.error(error_dict)
            return error_dict, 403

        # check company is active
        if job.company.is_active() is False:
            error_dict = {
                'error_message': f'Account for company with id {job.company.id} is not active.',
            }
            LOGGER.error(error_dict)
            return error_dict, 403


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

        try:
            resume = StudentDocument.get(id=resume_id)
        except DoesNotExist:
            error_dict = {
                'error_message': f'Document with id {resume_id} does not exist',
            }
            LOGGER.error(error_dict)
            return error_dict, 400

        if cover_letter_id is not None:
            try:
                StudentDocument.get(id=cover_letter_id)
            except DoesNotExist:
                error_dict = {
                    'error_message': f'Document with id {cover_letter_id} does not exist',
                }
                LOGGER.error(error_dict)
                return error_dict, 400

        if transcript_id is not None:
            try:
                StudentDocument.get(id=transcript_id)
            except DoesNotExist:
                error_dict = {
                    'error_message': f'Document with id {transcript_id} does not exist',
                }
                LOGGER.error(error_dict)
                return error_dict, 400

        try:
            return Application.create(
                student=student.id,
                job=job.id,
                resume=resume.id,
                cover_letter=cover_letter_id,
                transcript=transcript_id,
                state='NEW'
            )
        except IntegrityError as e:
            error_dict = {
                'error_message': e,
            }
            LOGGER.error(error_dict)
            return error_dict, 400
