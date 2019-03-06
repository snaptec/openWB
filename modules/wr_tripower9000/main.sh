#!/bin/bash
. /var/www/html/openWB/openwb.conf


if [[ $wrsma2ip != "none" ]] && [[ $wrsma3ip != "none" ]] && [[ $wrsma4ip != "none" ]]; then
	sudo python /var/www/html/openWB/modules/wr_tripower90004.py $tri9000ip $wrsma2ip $wrsma3ip $wrsma4ip
else
	if  [[ $wrsma2ip != "none" ]] && [[ $wrsma3ip != "none" ]]; then
		sudo python /var/www/html/openWB/modules/wr_tripower90003.py $tri9000ip $wrsma2ip $wrsma3ip 
	else
		if  [[ $wrsma2ip != "none" ]] && [[ $wrsma3ip != "none" ]]; then
			sudo python /var/www/html/openWB/modules/wr_tripower90002.py $tri9000ip $wrsma2ip 
		else
			sudo python /var/www/html/openWB/modules/wr_tripower9000.py $tri9000ip
		fi
	fi
fi





pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
ekwh=$(</var/www/html/openWB/ramdisk/pvkwh)


pvkwhk=$(echo "scale=3;$ekwh / 1000" |bc)
echo $pvkwhk > ramdisk/pvkwhk





