import psutil
from db_modell import Kuehlvarianten, Log, db_create_table
from peewee import fn
import datetime
import time
from subprocess import Popen
from sys import argv
from pprint import pprint
from telegram_api.telegram_bot_api import Bot
import os
import toml

MESSINTERVALL = 5  # in Sekunden


def load_config():
    configfile = os.path.join(SKRIPTPFAD, "config.toml")
    with open(configfile) as conffile:
        config = toml.loads(conffile.read())
    return config


SKRIPTPFAD = os.path.abspath(os.path.dirname(__file__))
CONFIG = load_config()


def eingabe_anfordern(text):
    while True:
        eingabe = input(text)
        if not eingabe:
            print("Bitte Eingabe vornehmen")
        else:
            break
    return eingabe


def kuehlvariante_holen_db(kuehlvariante):
    erg = Kuehlvarianten.select(Kuehlvarianten.id).where(Kuehlvarianten.variante == kuehlvariante)
    if erg.count() == 0:
        max_id = Kuehlvarianten.select(fn.max(Kuehlvarianten.id)).scalar()
        if max_id is None:
            max_id = 0
        Kuehlvarianten.insert(id=max_id + 1, variante=kuehlvariante).execute()
        erg = kuehlvariante_holen_db(kuehlvariante)
    return erg


def messung_starten():
    datensatz = {"ts": datetime.datetime.now(),
                 "cpu_temp": psutil.sensors_temperatures()["cpu-thermal"][0].current,
                 "cpu_takt": psutil.cpu_freq().current}
    return datensatz


def messung_eintragen(kuehlvariante, datensatz, last):
    Log.insert(ts=datensatz["ts"],
               variante=kuehlvariante,
               last=last,
               cpu_temp=datensatz["cpu_temp"],
               cpu_takt=datensatz["cpu_takt"])
    pprint(datensatz)


def messen_im_idle(kuehlvariante_id, dauer_idle):
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).total_seconds() < dauer_idle:
        datensatz = messung_starten()
        messung_eintragen(kuehlvariante_id, datensatz, False)
        time.sleep(MESSINTERVALL)


def messen_unter_last(kuehlvarante_id, dauer_last):
    befehl = "stress -c 4 -i 1 -m 1 -t {}s".format(dauer_last)
    prozess = Popen(befehl, shell=True)
    while prozess.poll() is None:
        datensatz = messung_starten()
        messung_eintragen(kuehlvarante_id, datensatz, True)
        time.sleep(MESSINTERVALL)


def main():
    db_create_table()
    try:
        kuehlvariante = argv[1]
    except IndexError:
        kuehlvariante = eingabe_anfordern("Welche Kühlvariante wird verwendet: ")
    kuehlvariante_id = kuehlvariante_holen_db(kuehlvariante)
    for ablauf in CONFIG["ablauf"]:
        if ablauf[0]:
            messen_unter_last(kuehlvariante_id, ablauf[1])
        else:
            messen_im_idle(kuehlvariante_id, ablauf[1])
    if CONFIG["token"] is not None:
        bot = Bot(CONFIG["token"])
        for id_ in CONFIG["telegramids"]:
            bot.send_message(id_, "Durchlauf fertig")


if __name__ == "__main__":
    main()
