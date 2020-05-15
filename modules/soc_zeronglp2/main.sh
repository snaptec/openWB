#!/bin/bash

zintervallladen=$(( soc_zeronglp2_intervallladen * 6 ))
zintervall=$(( soc_zeronglp2_intervall * 6 ))
zerotimer=$(</var/www/html/openWB/ramdisk/soctimer1)
#ladeleistung=$(</var/www/html/openWB/ramdisk/llaktuell)
zerounitnumber=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_units -d format=json -d pass=$soc_zeronglp2_password -d user=$soc_zeronglp2_username | jq '.[].unitnumber')
ischarging=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$soc_zeronglp2_username -d pass=$soc_zeronglp2_password -d unitnumber=$zerounitnumber | jq '.[].charging')

if (( $ischarging != 0 )); then
	if (( zerotimer < zintervallladen )); then
		zerotimer=$((zerotimer+1))
		echo $zerotimer > /var/www/html/openWB/ramdisk/soctimer1
	else
		re='^-?[0-9]+$'
		soclevel=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$soc_zeronglp2_username -d pass=$soc_zeronglp2_password -d unitnumber=$zerounitnumber | jq '.[].soc')
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > /var/www/html/openWB/ramdisk/soc1
			fi
		fi
		echo 0 > /var/www/html/openWB/ramdisk/soctimer1
	fi
else
	if (( zerotimer < zintervall )); then
		zerotimer=$((zerotimer+1))
		echo $zerotimer > /var/www/html/openWB/ramdisk/soctimer1
	else
		re='^-?[0-9]+$'
		soclevel=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$soc_zeronglp2_username -d pass=$soc_zeronglp2_password -d unitnumber=$zerounitnumber | jq '.[].soc')
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > /var/www/html/openWB/ramdisk/soc1
			fi
		fi
		echo 0 > /var/www/html/openWB/ramdisk/soctimer1
	fi
fi
