#!/usr/bin/env python

import pycarwings2
import time
from configparser import ConfigParser
import logging
import sys

logging.basicConfig(stream=sys.stdout)


username = sys.argv[1]
password = sys.argv[2]
region = 'NE'


def update_battery_status(leaf, wait_time=1):
    key = leaf.request_update()
    status = leaf.get_status_from_update(key)
    # Currently the nissan servers eventually return status 200 from get_status_from_update(), previously
    # they did not, and it was necessary to check the date returned within get_latest_battery_status().
    while status is None:
        time.sleep(wait_time)
        status = leaf.get_status_from_update(key)
    return status


def print_info(info):
    f = open('/var/www/html/openWB/ramdisk/soc1', 'w')
    f.write(str(info.state_of_charge))
    f.close()
# Main program

logging.debug("login = %s, password = %s, region = %s" % (username, password, region))

s = pycarwings2.Session(username, password, region)
leaf = s.get_leaf()

# Give the nissan servers a bit of a delay so that we don't get stale data
time.sleep(1)

leaf_info = leaf.get_latest_battery_status()
start_date = leaf_info.answer["BatteryStatusRecords"]["OperationDateAndTime"]
print_info(leaf_info)

