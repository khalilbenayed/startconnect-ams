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
    :type first_name: str

    :param last_name: Last name of the student
    :type last_name: str

    :param email: Email of the student
    :type email: str

    :param password: Password of the student
    :type password: str

    :param state: State of the student. Should be an enum value of the above
    :type state: str

    :param created: Time of creation of the row
    :type created: str
    """
    id = AutoField()  # Primary key
    first_name = CharField()
    last_name = CharField()
    password = CharField()
    email = CharField()
    state = CharField(default='TEST')
    created_at = DateTimeField(default=datetime.now())
    modified_at = DateTimeField(default=datetime.now())
