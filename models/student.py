from datetime import datetime

from models.base_model import BaseModel
from peewee import (
    AutoField,
    IntegerField,
    CharField,
    DateTimeField
)

STUDENT_STATES = ['TEST', 'ACTIVE', 'INACTIVE']


class Student(BaseModel):
    """
    Model class for the student table.

    :param first_name: First name of the student
    :param last_name: Last name of the student
    :param email: Email of the student
    :param password: Password of the student
    :param state: State of the student. Should be an enum value of the above
    :param created: Time of creation of the row
    """
    id = AutoField()  # Primary key
    first_name = CharField()
    last_name = CharField()
    password = CharField()
    email = CharField(unique=True)
    state = CharField(default='TEST')
    created_at = DateTimeField(default=datetime.now())
    modified_at = DateTimeField(default=datetime.now())
