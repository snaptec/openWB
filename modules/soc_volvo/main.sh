#!/bin/bash

soctimer=$(</var/www/html/openWB/ramdisk/soctimer)
cd /var/www/html/openWB/modules/soc_volvo
if (( soctimer < 60 )); then
	soctimer=$((soctimer+1))
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer
else
	re='^-?[0-9]+$'
	soclevel=$(python3 voc -u $socuser -p $socpass dashboard |grep 'Battery level' | cut -f2 -d":" |sed 's/[^0-9]*//g')
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > /var/www/html/openWB/ramdisk/soc
		fi
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
	fi

fi


