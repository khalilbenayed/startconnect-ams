from datetime import datetime

from models import (
    BaseModel,
    Student,
)
from peewee import (
    AutoField,
    IntegerField,
    CharField,
    DateTimeField,
    ForeignKeyField,
)

DOCUMENT_TYPES = {'RESUME', 'TRANSCRIPT', 'COVER_LETTER'}
DOCUMENT_STATES = {'VALID', 'DELETED'}


class StudentDocument(BaseModel):
    id = AutoField()  # Primary key
    student = ForeignKeyField(Student, backref='documents')
    document_type = CharField()
    document_name = CharField()
    document_key = CharField(unique=True)
    state = CharField()
    created_at = DateTimeField(default=datetime.now())
    modified_at = DateTimeField(default=datetime.now())
