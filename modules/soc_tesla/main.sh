#!/bin/bash
TOKENPASSWORD='#TokenInUse#'
response=''

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CONFIGFILE="$OPENWBBASEDIR/openwb.conf"
CHARGEPOINT=$1
MYLOGFILE="$RAMDISKDIR/soc.log"

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_tesla: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

# for developement only
# debug=1

case $CHARGEPOINT in
	2)
		# second charge point
		socintervallladen=$(( soc_teslalp2_intervallladen * 6 ))
		socintervall=$(( soc_teslalp2_intervall * 6 ))
		ladeleistung=$(<$RAMDISKDIR/llaktuells1)
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		passwordConfigText="soc_teslalp2_password"
		mfaPasscodeConfigText="soc_teslalp2_mfapasscode"
		carnumber=$soc_teslalp2_carnumber
		tokensfile="$MODULEDIR/tokens.lp2"
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		socintervallladen=$(( soc_tesla_intervallladen * 6 ))
		socintervall=$(( soc_tesla_intervall * 6 ))
		ladeleistung=$(<$RAMDISKDIR/llaktuell)
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		passwordConfigText="soc_tesla_password"
		mfaPasscodeConfigText="soc_tesla_mfapasscode"
		carnumber=$soc_tesla_carnumber
		tokensfile="$MODULEDIR/tokens.lp1"
		;;
esac

password="${!passwordConfigText}"
mfapasscode="${!mfaPasscodeConfigText}"

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

soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"
if (( ladeleistung > 1000 )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Car is charging"
	if (( soctimer < socintervallladen )); then
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		incrementTimer
	else
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
		echo 0 > $soctimerfile
		bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.tesla.soc" "$CHARGEPOINT" "$tokensfile" "$carnumber" "1" >> "$OPENWBBASEDIR/ramdisk/soc.log" 2>&1
	fi
else
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Car is not charging"
	if (( soctimer < socintervall )); then
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		incrementTimer
	else
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
		echo 0 > $soctimerfile
		bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.tesla.soc" "$CHARGEPOINT" "$tokensfile" "$carnumber" "" >> "$OPENWBBASEDIR/ramdisk/soc.log" 2>&1
	fi
fi
