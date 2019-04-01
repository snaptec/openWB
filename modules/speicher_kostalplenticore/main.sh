#!/bin/bash
. /var/www/html/openWB/openwb.conf

sudo python /var/www/html/openWB/modules/speicher_kostalplenticore/read_kostalplenticorebatt.py $kostalplenticoreip

