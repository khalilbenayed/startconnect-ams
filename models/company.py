from datetime import datetime

from models.base_model import BaseModel
from peewee import (
    AutoField,
    IntegerField,
    CharField,
    DateTimeField
)

COMPANY_STATES = {'NOT_VERIFIED', 'ACTIVE', 'INACTIVE'}


class Company(BaseModel):
    """
    Model class for the companies table.

    :param company_name: Name of the companies
    :param email: Email of the companies
    :param address_1: address_1 of the companies
    :param address_2: address_2 of the companies
    :param city: city of the companies
    :param province: province of the companies
    :param zipcode: zipcode of the companies
    :param country: country of the companies
    :param phone: phone of the companies
    :param password: Password of the companies
    :param state: State of the companies. Should be an enum value of the above
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
    state = CharField(default='NOT_VERIFIED')
    created_at = DateTimeField(default=datetime.now())
    modified_at = DateTimeField(default=datetime.now())
