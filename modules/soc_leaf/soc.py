#!/usr/bin/env
# coding=utf-8

import pycarwings2
import time
import logging
import sys

username    = sys.argv[1]
password    = sys.argv[2]
chargepoint = sys.argv[3]
region      = 'NE'

# init filenames
if( int(chargepoint) == 2 ):
    soctimerFile = '/var/www/html/openWB/ramdisk/soctimer1'
    socFile = '/var/www/html/openWB/ramdisk/soc1'
else:
    soctimerFile = '/var/www/html/openWB/ramdisk/soctimer'
    socFile = '/var/www/html/openWB/ramdisk/soc'

logging.basicConfig(stream=sys.stdout, filename='/var/www/html/openWB/ramdisk/soc.log', level=5, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') #

def getNissanSession():
    logging.debug("LP%s: login = %s, region = %s" % (chargepoint, username, region))

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

    logging.debug("LP%s: Battery status %s" % (chargepoint, bat_percent))

    f = open(socFile, 'w')
    f.write(str(bat_percent))
    f.close()

    return bat_percent

def requestSoc(leaf):
    '''
    Fordert den asynchron Server auf, den Ladezustand vom Auto abzufragen.
    Das Ergebnis kann nach einigem Warten mit readSoc() abgefragt werden
    '''
    logging.debug("LP%s: Request SoC Update" % (chargepoint))

    key = leaf.request_update()
    status = leaf.get_status_from_update(key)
    # Currently the nissan servers eventually return status 200 from get_status_from_update(), previously
    # they did not, and it was necessary to check the date returned within get_latest_battery_status().
    sleepsecs = 20
    while status is None:
        logging.debug("Waiting {0} seconds".format(sleepsecs))
        time.sleep(sleepsecs)
        status = leaf.get_status_from_update(key)
    logging.debug("LP%s: Finished updating" % (chargepoint))


leaftimer = open(soctimerFile, 'r')
leaftimer = int(leaftimer.read())

if ( leaftimer < 180 ):
    leaftimer += 1
    logging.debug("LP%s: Update soctimer to %s" % (chargepoint, str(leaftimer)))
    f = open(soctimerFile, 'w')
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
    logging.debug("LP%s: Update soctimer to 0" % (chargepoint))
    f = open(soctimerFile, 'w')
    f.write(str(0))
    f.close()
