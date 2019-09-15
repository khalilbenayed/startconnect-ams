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

JOB_STATES = {'NEW', 'EXPIRED', 'DELETED'}
JOB_TYPES = {'VOLUNTEER', 'CONTRACT', 'INTERNSHIP'}


class Job(BaseModel):
    id = AutoField()  # Primary key
    company = ForeignKeyField(Company, backref='jobs')
    title = CharField()
    category = CharField(null=True)
    description = CharField()
    type = CharField()
    state = CharField()
    n_positions = IntegerField()
    duration = CharField()
    start_date = DateTimeField(null=True)
    expiry_date = DateTimeField(null=True)
    compensation = CharField()
    city = CharField()
    created_at = DateTimeField(default=datetime.now())
    modified_at = DateTimeField(default=datetime.now())

    def is_new(self):
        return self.state == 'NEW'
