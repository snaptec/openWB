#!/bin/bash

if (( pv2kitversion == 1 )); then
	python /var/www/html/openWB/modules/wr2_ethlovato/readsdm.py  
else
	python /var/www/html/openWB/modules/wr2_ethlovato/readlovato.py  
fi

pv2watt=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pv2watt
