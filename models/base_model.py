import yaml
import os
from peewee import (
    PostgresqlDatabase,
    Model
)


with open("config.yaml") as cfg_file:
    cfg = yaml.load(cfg_file, Loader=yaml.Loader).get(os.environ['ENV'])
    db_cfg = cfg.get('postgres')


pg_db = PostgresqlDatabase(
    db_cfg.get('name'),
    user=db_cfg.get('user'),
    password=db_cfg.get('password'),
    host=db_cfg.get('host'),
    port=db_cfg.get('port'))


class BaseModel(Model):
    class Meta:
        database = pg_db
