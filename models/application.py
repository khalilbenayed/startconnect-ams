from datetime import datetime

from models import (
    BaseModel,
    Student,
    Job,
    StudentDocument
)
from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
)

APPLICATION_STATES = {'NEW'}


class Application(BaseModel):
    id = AutoField()  # Primary key
    student = ForeignKeyField(Student, backref='applications')
    job = ForeignKeyField(Job, backref='applications')
    resume = ForeignKeyField(StudentDocument)
    cover_letter = ForeignKeyField(StudentDocument, null=True)
    transcript = ForeignKeyField(StudentDocument, null=True)
    state = CharField()
    created_at = DateTimeField(default=datetime.now())
    modified_at = DateTimeField(default=datetime.now())
