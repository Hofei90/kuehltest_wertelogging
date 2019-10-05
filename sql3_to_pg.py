import peewee
import db_modell as db

user = input("PGUser eingeben:")
pw = input("Passwort eingeben: ")
DB = peewee.PostgresqlDatabase("kuehltest", user=user, password=pw)


class BaseModel(peewee.Model):
    class Meta:
        database = DB


class Kuehlvarianten(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    variante = peewee.TextField()


class Log(BaseModel):
    ts = peewee.DateTimeField(primary_key=True)
    nummer = peewee.IntegerField(null=True)
    fake_ts = peewee.DateTimeField(null=True)
    variante = peewee.IntegerField()
    last = peewee.BooleanField()
    cpu_temp = peewee.FloatField()
    cpu_takt = peewee.FloatField()
    vcgencmd_temp = peewee.FloatField()
    vcgencmd_takt = peewee.FloatField()


def db_create_table():
    DB.create_tables([Kuehlvarianten, Log])


def main():
    db_create_table()
    kuehlvarianten = db.Kuehlvarianten.select().dicts()
    for data in kuehlvarianten:
        try:
            Kuehlvarianten.create(**data)
        except peewee.IntegrityError:
            continue
    log = db.Log.select().dicts()
    for data in log:
        try:
            Log.create(**data)
        except peewee.IntegrityError:
            continue


if __name__ == "__main__":
    main()
