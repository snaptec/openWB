#!/bin/bash
. /var/www/html/openWB/openwb.conf
tintervallladen=$(( soc_tesla_intervallladen * 6 ))
tintervall=$(( soc_tesla_intervall * 6 ))
teslatimer=$(</var/www/html/openWB/ramdisk/soctimer)
cd /var/www/html/openWB/modules/soc_tesla
ladeleistung=$(</var/www/html/openWB/ramdisk/llaktuell)

if (( ladeleistung > 1000 )); then
	if (( teslatimer < tintervallladen )); then
		teslatimer=$((teslatimer+1))
		echo $teslatimer > /var/www/html/openWB/ramdisk/soctimer
	else
		re='^-?[0-9]+$'
		soclevel=$(sudo python /var/www/html/openWB/modules/soc_tesla/tsoc.py $soc_tesla_username $soc_tesla_password | jq .battery_level)
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > /var/www/html/openWB/ramdisk/soc
			fi
		fi
		echo 0 > /var/www/html/openWB/ramdisk/soctimer
	fi
else
	if (( teslatimer < tintervall )); then
		teslatimer=$((teslatimer+1))
		echo $teslatimer > /var/www/html/openWB/ramdisk/soctimer
	else
		re='^-?[0-9]+$'
		soclevel=$(sudo python /var/www/html/openWB/modules/soc_tesla/tsoc.py $soc_tesla_username $soc_tesla_password | jq .battery_level)
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > /var/www/html/openWB/ramdisk/soc
			fi
		fi
		echo 0 > /var/www/html/openWB/ramdisk/soctimer
	fi
fi


