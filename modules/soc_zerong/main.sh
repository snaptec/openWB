#!/bin/bash
zintervallladen=$(( soc_zerong_intervallladen * 6 ))
zintervall=$(( soc_zerong_intervall * 6 ))
zerotimer=$(</var/www/html/openWB/ramdisk/soctimer)
#ladeleistung=$(</var/www/html/openWB/ramdisk/llaktuell)
zerounitnumber=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_units -d format=json -d pass=$soc_zerong_password -d user=$soc_zerong_username | jq '.[].unitnumber')
ischarging=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$soc_zerong_username -d pass=$soc_zerong_password -d unitnumber=$zerounitnumber | jq '.[].charging')

if (( $ischarging != 0 )); then
	if (( zerotimer < zintervallladen )); then
		zerotimer=$((zerotimer+1))
		echo $zerotimer > /var/www/html/openWB/ramdisk/soctimer
	else
		re='^-?[0-9]+$'
		soclevel=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$soc_zerong_username -d pass=$soc_zerong_password -d unitnumber=$zerounitnumber | jq '.[].soc')
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > /var/www/html/openWB/ramdisk/soc
			fi
		fi
		echo 0 > /var/www/html/openWB/ramdisk/soctimer
	fi
else
	if (( zerotimer < zintervall )); then
		zerotimer=$((zerotimer+1))
		echo $zerotimer > /var/www/html/openWB/ramdisk/soctimer
	else
		re='^-?[0-9]+$'
		soclevel=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$soc_zerong_username -d pass=$soc_zerong_password -d unitnumber=$zerounitnumber | jq '.[].soc')
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > /var/www/html/openWB/ramdisk/soc
			fi
		fi
		echo 0 > /var/www/html/openWB/ramdisk/soctimer
	fi
fi
