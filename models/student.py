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
    Model class for the students table.

    :param first_name: First name of the students
    :param last_name: Last name of the students
    :param email: Email of the students
    :param password: Password of the students
    :param state: State of the students. Should be an enum value of the above
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
