from models import (
    pg_db as database,
    Student,
    Company,
    Job,
    StudentDocument,
    Application,
)


def open_database_connection():
    database.connect()


def close_database_connection():
    database.connect()


def create_tables():
    database.create_tables([
        Student,
        Company,
        Job,
        StudentDocument,
        Application,
    ])
