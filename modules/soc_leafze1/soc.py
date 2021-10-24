#!/usr/bin/env
# coding=utf-8

import time
import logging
import sys
import os

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


leaftimer = open(soctimerFile, 'r')
leaftimer = int(leaftimer.read())

if ( leaftimer < 180 ):
    leaftimer += 1
    logging.debug("LP%s: Update soctimer to %s" % (chargepoint, str(leaftimer)))
    f = open(soctimerFile, 'w')
    f.write(str(leaftimer))
    f.close()
    if ( leaftimer == 10 ):

       cmd = '/var/www/html/openWB/modules/soc_leafze1/nissanconnect_soc.exe -v --username=' + username + ' --password=' + password + ' --socfile=' + socFile
       logging.debug("Running: %s" % (cmd))
       os.system(cmd)

else:
    logging.debug("LP%s: Update soctimer to 0" % (chargepoint))
    f = open(soctimerFile, 'w')
    f.write(str(0))
    f.close()
