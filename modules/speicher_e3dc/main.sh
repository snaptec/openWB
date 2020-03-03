#!/bin/bash
. /var/www/html/openWB/openwb.conf

if [[ $pvwattmodul != "none" ]]; then
	pvwattold=$(</var/www/html/openWB/ramdisk/pvwatt)
fi
if  [[ $e3dc2ip != "none" ]]; then
	sudo python /var/www/html/openWB/modules/speicher_e3dc/e3dcfarm.py $e3dcip $e3dc2ip 
else
	#wenn keine Antwort ersetze leeren Wert durch eine 0
	ra='^-?[0-9]+$'
	if [[ -e /var/www/html/openWB/ramdisk/speicherwatt0pos ]]; then
	 importtemp=$(</var/www/html/openWB/ramdisk/speicherwatt0pos)
	else
	 importtemp=$(timeout 2 mosquitto_sub -t openWB/housebattery/WHImported_temp)
	 	if ! [[ $importtemp =~ $ra ]] ; then
		 importtemp="0"
	 fi
	 dtime=$(date +"%T")
	 echo " $dtime e3dc read openWB/housebattery/WHImported_temp from mosquito $importtemp"
	 	echo $importtemp > /var/www/html/openWB/ramdisk/speicherwatt0pos
	fi
	if [[ -e /var/www/html/openWB/ramdisk/speicherwatt0neg ]]; then
	 exporttemp=$(</var/www/html/openWB/ramdisk/speicherwatt0neg)
	else
	 exporttemp=$(timeout 2 mosquitto_sub -t openWB/housebattery/WHExport_temp)
	 	if ! [[ $exporttemp =~ $ra ]] ; then
		 exporttemp="0"
	 fi
	 	dtime=$(date +"%T")
	 echo " $dtime e3dc read openWB/housebattery/WHExport_temp from mosquito $exporttemp"
	 	echo $exporttemp > /var/www/html/openWB/ramdisk/speicherwatt0neg
	fi
	sudo python /var/www/html/openWB/modules/speicher_e3dc/e3dc.py $e3dcip
	importtemp1=$(</var/www/html/openWB/ramdisk/speicherwatt0pos)
	exporttemp1=$(</var/www/html/openWB/ramdisk/speicherwatt0neg)
	if [[ $importtemp !=  $importtemp1 ]]; then
		mosquitto_pub -t openWB/housebattery/WHImported_temp -r -m "$importtemp1"
	fi
	if [[ $exporttemp !=  $exporttemp1 ]]; then
		mosquitto_pub -t openWB/housebattery/WHExport_temp -r -m "$exporttemp1"
	fi
fi
if [[ $pvwattmodul != "none" ]]; then
	pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
	newpvwatt=$(( pvwattold + pvwatt ))
	echo $newpvwatt > /var/www/html/openWB/ramdisk/pvwatt
fi
