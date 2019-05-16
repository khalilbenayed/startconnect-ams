from models import (
    pg_db as database,
    Student,
)


def open_database_connection():
    database.connect()


def close_database_connection():
    database.connect()


def create_tables():
    database.create_tables([Student])
