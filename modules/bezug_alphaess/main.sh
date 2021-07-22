#!/bin/bash
if [[ $alphav123 == "1" ]]; then
	python /var/www/html/openWB/modules/bezug_alphaess/readv123.py
else
	python /var/www/html/openWB/modules/bezug_alphaess/readalpha.py
fi

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
