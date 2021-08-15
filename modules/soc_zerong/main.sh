#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_zerong: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		ladeleistung=$(<$RAMDISKDIR/llaktuells1)
		zintervallladen=$(( soc_zeronglp2_intervallladen * 6 ))
		zintervall=$(( soc_zeronglp2_intervall * 6 ))
		username=$soc_zeronglp2_username
		password=$soc_zeronglp2_password
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		ladeleistung=$(<$RAMDISKDIR/llaktuell)
		zintervallladen=$(( soc_zerong_intervallladen * 6 ))
		zintervall=$(( soc_zerong_intervall * 6 ))
		username=$soc_zerong_username
		password=$soc_zerong_password
		;;
esac

incrementTimer(){
	case $dspeed in
		1)
			# Regelgeschwindigkeit 10 Sekunden
			ticksize=1
			;;
		2)
			# Regelgeschwindigkeit 20 Sekunden
			ticksize=2
			;;
		3)
			# Regelgeschwindigkeit 60 Sekunden
			ticksize=1
			;;
		*)
			# Regelgeschwindigkeit unbekannt
			ticksize=1
			;;
	esac
	soctimer=$((soctimer+$ticksize))
	echo $soctimer > $soctimerfile
}

getAndWriteSoc(){
	echo 0 > $soctimerfile
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
	zerounitnumber=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_units -d format=json -d pass=$password -d user=$username | jq '.[].unitnumber')
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Unitnumber: $zerounitnumber"
	re='^-?[0-9]+$'
	soclevel=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$username -d pass=$password -d unitnumber=$zerounitnumber | jq '.[].soc')
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC from Server: $soclevel"
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > $socfile
		else
			openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Ignoring SoC of 0%"
		fi
	else
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: SoC is invalid!"
	fi
}

soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"

# zerounitnumber=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_units -d format=json -d pass=$password -d user=$username | jq '.[].unitnumber')
# ischarging=$(curl -s --http2 -G https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit -d format=json -d user=$username -d pass=$password -d unitnumber=$zerounitnumber | jq '.[].charging')

if (( ladeleistung > 500 )); then
	if (( soctimer < zintervallladen )); then
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Charging, but nothing to do yet. Incrementing timer."
		incrementTimer
	else
		getAndWriteSoc
	fi
else
	if (( soctimer < zintervall )); then
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		incrementTimer
	else
		getAndWriteSoc
	fi
fi
