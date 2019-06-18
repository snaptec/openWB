#!/bin/bash
. /var/www/html/openWB/openwb.conf


if  [[ $e3dc2ip != "none" ]]; then
	sudo python /var/www/html/openWB/modules/speicher_e3dc/e3dc.py $e3dcip $e3dc2ip 
else
	sudo python /var/www/html/openWB/modules/speicher_e3dc/e3dc.py $e3dcip
fi

