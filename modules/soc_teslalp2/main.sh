#!/bin/bash
. /var/www/html/openWB/openwb.conf
tintervallladen=$(( soc_teslalp2_intervallladen * 6 ))
tintervall=$(( soc_teslalp2_intervall * 6 ))
teslatimer=$(</var/www/html/openWB/ramdisk/soctimer1)
cd /var/www/html/openWB/modules/soc_teslalp2
ladeleistung=$(</var/www/html/openWB/ramdisk/llaktuells1)

if (( ladeleistung > 1000 )); then
	if (( teslatimer < tintervallladen )); then
		teslatimer=$((teslatimer+1))
		echo $teslatimer > /var/www/html/openWB/ramdisk/soctimer1
	else
		re='^-?[0-9]+$'
		soclevel=$(sudo python /var/www/html/openWB/modules/soc_teslalp2/tsoc.py $soc_teslalp2_username $soc_teslalp2_password | jq .battery_level)
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > /var/www/html/openWB/ramdisk/soc1
			fi
		fi
		echo 0 > /var/www/html/openWB/ramdisk/soctimer1
	fi
else
	if (( teslatimer < tintervall )); then
		teslatimer=$((teslatimer+1))
		echo $teslatimer > /var/www/html/openWB/ramdisk/soctimer1
	else
		re='^-?[0-9]+$'
		soclevel=$(sudo python /var/www/html/openWB/modules/soc_teslalp2/tsoc.py $soc_tesla_username $soc_tesla_password | jq .battery_level)
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > /var/www/html/openWB/ramdisk/soc1
			fi
		fi
		echo 0 > /var/www/html/openWB/ramdisk/soctimer1
	fi
fi


