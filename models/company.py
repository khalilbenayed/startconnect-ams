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
    :param email: Email of the company
    :param address_1: address_1 of the company
    :param address_2: address_2 of the company
    :param city: city of the company
    :param province: province of the company
    :param zipcode: zipcode of the company
    :param country: country of the company
    :param phone: phone of the company
    :param password: Password of the company
    :param state: State of the company. Should be an enum value of the above
    :param created_at: Time of creation of the row
    :param modified_at: Time of last modification of the row
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
