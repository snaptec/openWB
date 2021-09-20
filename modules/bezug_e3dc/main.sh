#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/counter/e3dc.py "${e3dcip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
