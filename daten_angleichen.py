from db_modell import Log, Kuehlvarianten, db_create_table
import datetime


def main():
    db_create_table()
    varianten = Kuehlvarianten.select()
    datensaetze_sortiert = []
    for variante in varianten:
        datensaetze = []
        for datensatz in Log.select().where(Log.variante == variante.id):
            datensaetze.append(datensatz)
        datensaetze_sortiert.append(datensaetze)

    for datensaetze in datensaetze_sortiert:
        for nr, datensatz in enumerate(datensaetze):
            if datensatz.nummer is None:
                datensatz.nummer = nr
                datensatz.save()
            # if datensatz.fake_ts is None:
            ts = datetime.datetime(year=2019, month=7, day=21,
                                   hour=0, minute=0, second=0, microsecond=0)
            delta = datetime.timedelta(seconds=nr * 5)
            ts = ts + delta
            datensatz.fake_ts = ts
            datensatz.save()


if __name__ == "__main__":
    main()
