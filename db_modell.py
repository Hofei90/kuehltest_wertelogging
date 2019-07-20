
import os
import peewee


SKRIPTPFAD = os.path.abspath(os.path.dirname(__file__))
DB = peewee.SqliteDatabase(os.path.join(SKRIPTPFAD, "kuehltest_log.db3"))


class BaseModel(peewee.Model):
    class Meta:
        database = DB


class Kuehlvarianten(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    variante = peewee.TextField()


class Log(BaseModel):
    ts = peewee.DateTimeField(primary_key=True)
    variante = peewee.IntegerField()
    last = peewee.BooleanField()
    cpu_temp = peewee.FloatField()
    cpu_takt = peewee.FloatField()
    vcgencmd_temp = peewee.FloatField()
    vcgencmd_takt = peewee.FloatField()


def db_create_table():
    DB.create_tables([Kuehlvarianten, Log])
