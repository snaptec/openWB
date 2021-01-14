#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1

socDebug=$debug
# for developement only
socDebug=1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		zintervallladen=$(( soc_zeronglp2_intervallladen * 6 ))
		zintervall=$(( soc_zeronglp2_intervall * 6 ))
		username=$soc_zeronglp2_username
		password=$soc_zeronglp2_password
		;;
	*)
		# defaults to first charge point for backward compatibility
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		zintervallladen=$(( soc_zerong_intervallladen * 6 ))
		zintervall=$(( soc_zerong_intervall * 6 ))
		username=$soc_zerong_username
		password=$soc_zerong_password
		;;
esac

zerotimer=$(<$soctimerfile)
#ladeleistung=$(<$RAMDISKDIR/llaktuell)
zerounitnumber=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_units -d format=json -d pass=$password -d user=$username | jq '.[].unitnumber')
ischarging=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$username -d pass=$password -d unitnumber=$zerounitnumber | jq '.[].charging')

if (( $ischarging != 0 )); then
	if (( zerotimer < zintervallladen )); then
		zerotimer=$((zerotimer+1))
		echo $zerotimer > $soctimerfile
	else
		echo 0 > $soctimerfile
		re='^-?[0-9]+$'
		soclevel=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$username -d pass=$password -d unitnumber=$zerounitnumber | jq '.[].soc')
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > $socfile
			fi
		fi
	fi
else
	if (( zerotimer < zintervall )); then
		zerotimer=$((zerotimer+1))
		echo $zerotimer > $soctimerfile
	else
		echo 0 > $soctimerfile
		re='^-?[0-9]+$'
		soclevel=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$username -d pass=$password -d unitnumber=$zerounitnumber | jq '.[].soc')
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > $socfile
			fi
		fi
	fi
fi
