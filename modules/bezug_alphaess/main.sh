#!/bin/bash
sudo python /var/www/html/openWB/modules/bezug_alphaess/readalpha.py
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug

