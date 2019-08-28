import uuid
from models import StudentDocument

def create_document(student_id, document, document_type, document_default_name=None):
    # check file extension is pdf
    document_name, extension = document.filename.rsplit('.', 1)
    if extension.lower() != 'pdf':
        raise Exception(f'Document type is not pdf: {extension.lower()}')

    if document_default_name is not None:
        document_name = document_default_name

    document_key = uuid.uuid1()
    document.filename = f'{document_key}.pdf'
    document_entity = StudentDocument.create(
        student=student_id,
        document_name=document_name,
        document_type=document_type,
        document_key=document.filename
    )

    # save file (rn in filesystem)
    # TODO: S3 bucket
    document.save(f'tmp/{document.filename}')
    document.close()

    return document_entity
