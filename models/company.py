from datetime import datetime

from models.base_model import BaseModel
from peewee import (
    AutoField,
    IntegerField,
    CharField,
    DateTimeField
)

COMPANY_STATES = ['TEST', 'ACTIVE', 'INACTIVE']


class Company(BaseModel):
    """
    Model class for the company table.

    :param company_name: Name of the company
    :type company_name: str

    :param email: Email of the company
    :type email: str

    :param address_1: address_1 of the company
    :type address_1: str

    :param address_2: address_2 of the company
    :type address_2: str

    :param city: city of the company
    :type city: str

    :param province: province of the company
    :type province: str

    :param zipcode: zipcode of the company
    :type zipcode: str

    :param country: country of the company
    :type country: str

    :param phone: phone of the company
    :type phone: str

    :param password: Password of the company
    :type password: str

    :param state: State of the company. Should be an enum value of the above
    :type state: str

    :param created_at: Time of creation of the row
    :type created_at: str

    :param modified_at: Time of last modification of the row
    :type modified_at: str
    """
    id = AutoField()  # Primary key
    company_name = CharField()
    email = CharField(unique=True)
    password = CharField()
    address_1 = CharField()
    address_2 = CharField(null=True)
    city = CharField()
    province = CharField()
    zipcode = CharField()
    country = CharField()
    phone = CharField()
    state = CharField(default='TEST')
    created_at = DateTimeField(default=datetime.now())
    modified_at = DateTimeField(default=datetime.now())
