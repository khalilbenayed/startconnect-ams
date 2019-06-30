from datetime import datetime

from models import (
    BaseModel,
    Company,
)
from peewee import (
    AutoField,
    IntegerField,
    CharField,
    DateTimeField,
    ForeignKeyField,
)

JOB_STATES = {'NEW'}
JOB_TYPES = {'VOLUNTEER', 'CONTRACT', 'PAID_INTERNSHIP'}


class Job(BaseModel):
    id = AutoField()  # Primary key
    company = ForeignKeyField(Company, backref='jobs')
    title = CharField()
    category = CharField()
    description = CharField()
    type = CharField()
    state = CharField()
    n_positions = IntegerField()
    duration = IntegerField()
    start_date = DateTimeField()
    expiry_date = DateTimeField()
    quote = IntegerField(null=True)
    hourly_wage = IntegerField(null=True)
    weekly_hours = IntegerField(null=True)
    total_hours = IntegerField(null=True)
    due_date = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now())
    modified_at = DateTimeField(default=datetime.now())
