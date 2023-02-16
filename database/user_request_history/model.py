"""
    Модуль создания моделей БД -history
"""

import datetime
from peewee import *
from config import DB_HISTORY

db = SqliteDatabase(DB_HISTORY)


class BaseModel(Model):

    class Meta:
        database = db


class User(BaseModel):

    user_id = IntegerField(null=False)
    user_name = CharField(max_length=30)
    time_use = DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d')

    class Meta:
        table_name = 'users'


class Command(BaseModel):

    select_command = CharField(max_length=100)
    query_data = TextField(null=True)
    response = TextField(null=True)
    user = ForeignKeyField(User)

    class Meta:
        table_name = 'commands'
