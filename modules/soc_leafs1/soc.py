#!/usr/bin/env
# coding=utf-8

import pycarwings2
import time
import logging
import sys


logging.basicConfig(stream=sys.stdout, filename='/var/www/html/openWB/ramdisk/socleaf.log', level=5, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') #


username = sys.argv[1]
password = sys.argv[2]
region = 'NE'

leaftimer = open('/var/www/html/openWB/ramdisk/soctimer', 'r')
leaftimer = int(leaftimer.read())

def getNissanSession():
    logging.debug("login = %s, password = %s, region = %s" % (username, password, region))

    s = pycarwings2.Session(username, password, region)
    leaf = s.get_leaf()

    # Give the nissan servers a bit of a delay so that we don't get stale data
    time.sleep(1)

    return leaf

def readSoc(leaf):
    '''
    Frägt den aktuellen Ladezustand vom Server ab. Das Auto selbst wird dabei nicht gefragt.
    :return: (int) Ladezustand in Prozent
    '''

    leaf_info = leaf.get_latest_battery_status()
    bat_percent = int(leaf_info.battery_percent)

    logging.debug("Battery status %s" % (bat_percent))

    f = open('/var/www/html/openWB/ramdisk/soc', 'w')
    f.write(str(bat_percent))
    f.close()

    return bat_percent


def requestSoc(leaf):
    '''
    Fordert den asynchron Server auf, den Ladezustand vom Auto abzufragen.
    Das Ergebnis kann nach einigem Warten mit readSoc() abgefragt werden
    '''
    logging.debug("Request SoC Update")

    key = leaf.request_update()
    status = leaf.get_status_from_update(key)
    # Currently the nissan servers eventually return status 200 from get_status_from_update(), previously
    # they did not, and it was necessary to check the date returned within get_latest_battery_status().
    sleepsecs = 20
    while status is None:
        logging.debug("Waiting {0} seconds".format(sleepsecs))
        time.sleep(sleepsecs)
        status = leaf.get_status_from_update(key)
    logging.debug("Finished updating")


if ( leaftimer < 180 ):
    leaftimer += 1
    f = open('/var/www/html/openWB/ramdisk/soctimer', 'w')
    logging.debug("Update soctimer to " + str(leaftimer))
    f.write(str(leaftimer))
    f.close()
    if ( leaftimer == 10 ):
        leaf = getNissanSession()

        # Vor requestSoc einmal readSoc aufrufen, sonst ermittelt requestSoc keinen neuen Wert
        readSoc(leaf)

        # Give the nissan servers a bit of a delay so that we don't get stale data
        time.sleep(1)
        requestSoc(leaf)

        # Give the nissan servers a bit of a delay so that we don't get stale data
        time.sleep(1)

        # Hinterher noch den aktualisierten Wert abfragen
        readSoc(leaf)
else:
    logging.debug("Update soctimer to 0")
    f = open('/var/www/html/openWB/ramdisk/soctimer', 'w')
    f.write(str(0))
    f.close()
