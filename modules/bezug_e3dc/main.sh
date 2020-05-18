#!/bin/bash

sudo python /var/www/html/openWB/modules/bezug_e3dc/e3dc.py $e3dcip
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
