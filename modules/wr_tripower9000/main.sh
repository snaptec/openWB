#!/bin/bash
. /var/www/html/openWB/openwb.conf

if [[ $wrsmawebbox == "1" ]]; then
	rekwh='^[-+]?[0-9]+\.?[0-9]*$'
	boxout=$(curl --silent --connect-timeout 3 -H "Content-Type: application/json" -X POST -d RPC='{"version": "1.0","proc": "GetPlantOverview","id": "1","format": "JSON"}' http://$tri9000ip/rpc)
	if [[ $? == "0" ]] ; then
		pvwatt=$(echo $boxout | jq -r '.result.overview[0].value ')
		pvkwh=$(echo $boxout | jq -r '.result.overview[2].value ')
		pvwh=$(( pvkwh * 1000 ))
		if [[ $pvwh =~ $rekwh ]]; then
			echo $pvwh > /var/www/html/openWB/ramdisk/pvkwh
			echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwhk
		fi
		if [[ $pvkwh =~ $rekwh ]]; then
			echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
		fi
	fi




else
	if [[ $wrsma2ip != "none" ]] && [[ $wrsma3ip != "none" ]] && [[ $wrsma4ip != "none" ]]; then
		sudo python /var/www/html/openWB/modules/wr_tripower9000/tri90004.py $tri9000ip $wrsma2ip $wrsma3ip $wrsma4ip
	else
		if  [[ $wrsma2ip != "none" ]] && [[ $wrsma3ip != "none" ]]; then
			sudo python /var/www/html/openWB/modules/wr_tripower9000/tri90003.py $tri9000ip $wrsma2ip $wrsma3ip 
		else
			if  [[ $wrsma2ip != "none" ]]; then
				sudo python /var/www/html/openWB/modules/wr_tripower9000/tri90002.py $tri9000ip $wrsma2ip 
			else
				sudo python /var/www/html/openWB/modules/wr_tripower9000/tri9000.py $tri9000ip
			fi
		fi
	fi
fi




pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
ekwh=$(</var/www/html/openWB/ramdisk/pvkwh)


pvkwhk=$(echo "scale=3;$ekwh / 1000" |bc)
echo $pvkwhk > ramdisk/pvkwhk





