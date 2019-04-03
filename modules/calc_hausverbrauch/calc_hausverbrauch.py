#!/usr/bin/python
# coding: utf8

#########################################################
#
#liest Werte PV-Leistung, Speicherleistung, EVU und EV
#aus ramdisk und berechnet daraus den Verbrauch
#bzw. Überschuss des Hauses (nicht PV-Anlage!!)
#
#2019 Michael Ortenstein, Kevin Wieland
#This file is part of openWB
#
#########################################################

#//TODO: import auf Notwendigkeit prüfen
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii

#//TODO: EV mit berechnen

#zuerst Werte aus ramdisk lesen
with open('/var/www/html/openWB/ramdisk/pvwatt', 'r') as f:
    pvwatt = int(f.read())
with open('/var/www/html/openWB/ramdisk/wattbezug', 'r') as f:
    wattbezug = int(f.read())
with open('/var/www/html/openWB/ramdisk/speicherleistung', 'r') as f:
    speicherleistung = int(f.read())

#dann Hausverbrauch berechnen
hausverbrauch = -1 * (pvwatt + speicherleistung +wattbezug)

#und in ramdisk schreiben
with open('/var/www/html/openWB/ramdisk/hausverbrauch', 'w') as f:
    f.write(str(hausverbrauch))
