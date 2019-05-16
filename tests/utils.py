import yaml
from functools import wraps
from peewee import PostgresqlDatabase
from models import (
    Student,
)


MODELS = (Student, )


with open("config.yaml") as cfg_file:
    cfg = yaml.load(cfg_file, Loader=yaml.Loader).get('test')
    db_cfg = cfg.get('postgres')


test_db = PostgresqlDatabase(
    db_cfg.get('name'),
    user=db_cfg.get('user'),
    password=db_cfg.get('password'),
    host=db_cfg.get('host'),
    port=db_cfg.get('port'))


# Bind the given models to the db for the duration of wrapped block.
def use_test_database(fn):
    @wraps(fn)
    def inner(self):
        with test_db.bind_ctx(MODELS):
            test_db.create_tables(MODELS)
            try:
                fn(self)
            finally:
                test_db.drop_tables(MODELS)
    return inner