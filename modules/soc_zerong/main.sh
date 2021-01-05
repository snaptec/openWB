#!/bin/bash

CHARGEPOINT=$1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer1"
		socfile="/var/www/html/openWB/ramdisk/soc1"
		zintervallladen=$(( soc_zeronglp2_intervallladen * 6 ))
		zintervall=$(( soc_zeronglp2_intervall * 6 ))
		username=$soc_zeronglp2_username
		password=$soc_zeronglp2_password
		;;
	*)
		# defaults to first charge point for backward compatibility
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer"
		socfile="/var/www/html/openWB/ramdisk/soc"
		zintervallladen=$(( soc_zerong_intervallladen * 6 ))
		zintervall=$(( soc_zerong_intervall * 6 ))
		username=$soc_zerong_username
		password=$soc_zerong_password
		;;
esac

zerotimer=$(<$soctimerfile)
#ladeleistung=$(</var/www/html/openWB/ramdisk/llaktuell)
zerounitnumber=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_units -d format=json -d pass=$password -d user=$username | jq '.[].unitnumber')
ischarging=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$username -d pass=$password -d unitnumber=$zerounitnumber | jq '.[].charging')

if (( $ischarging != 0 )); then
	if (( zerotimer < zintervallladen )); then
		zerotimer=$((zerotimer+1))
		echo $zerotimer > $soctimerfile
	else
		re='^-?[0-9]+$'
		soclevel=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$username -d pass=$password -d unitnumber=$zerounitnumber | jq '.[].soc')
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > $socfile
			fi
		fi
		echo 0 > $soctimerfile
	fi
else
	if (( zerotimer < zintervall )); then
		zerotimer=$((zerotimer+1))
		echo $zerotimer > $soctimerfile
	else
		re='^-?[0-9]+$'
		soclevel=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$username -d pass=$password -d unitnumber=$zerounitnumber | jq '.[].soc')
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > $socfile
			fi
		fi
		echo 0 > $soctimerfile
	fi
fi
