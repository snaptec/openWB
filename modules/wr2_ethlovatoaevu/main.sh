#!/bin/bash

if (( pv2kitversion == 1 )); then
	python /var/www/html/openWB/modules/wr2_ethlovatoaevu/readsdm.py  
else
	python /var/www/html/openWB/modules/wr2_ethlovatoaevu/readlovato.py  
fi

pvwatt2=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pvwatt2
