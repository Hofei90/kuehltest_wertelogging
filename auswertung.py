from db_modell import Log, Kuehlvarianten, db_create_table
import datetime

NOW = datetime.datetime.now()


def varianten_auslesen():
    varianten = Kuehlvarianten.select().dicts()
    return varianten


def anzahl_messungen_last_ermitteln(variante):
    anzahl = Log.select().where(Log.variante == variante["id"], Log.last == True).count()
    return anzahl - 1


def takte_ok_ermitteln(variante):
    takte_ok = Log.select().where(Log.variante == variante["id"], Log.last == True,
                                  Log.vcgencmd_takt > 1400).count()

    return takte_ok


def taktdurchschnitt_berechnen(variante):
    takte = Log.select().where(Log.variante == variante["id"], Log.last == True).execute()
    takte_durchschnitt = [takt.vcgencmd_takt for takt in takte]
    takte_durchschnitt.pop(0)
    takte_durchschnitt = sum(takte_durchschnitt) / len(takte_durchschnitt)
    return takte_durchschnitt


def main():
    varianten = varianten_auslesen()
    for variante in varianten:
        anzahl_messungen_last = anzahl_messungen_last_ermitteln(variante)
        takte_ok = takte_ok_ermitteln(variante)
        if takte_ok > anzahl_messungen_last:
            takte_ok = anzahl_messungen_last
        print(variante["variante"])
        print("{}%".format(round(takte_ok / anzahl_messungen_last * 100, 2)))
        print(round(taktdurchschnitt_berechnen(variante), 2))
        print("-" * 30)


if __name__ == "__main__":
    main()
