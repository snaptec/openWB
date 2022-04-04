#!/bin/bash
TOKENPASSWORD='#TokenInUse#'
response=''

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
DMOD="EVSOC"
CONFIGFILE="$OPENWBBASEDIR/openwb.conf"
CHARGEPOINT=$1
MYLOGFILE="$RAMDISKDIR/soc.log"

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_tesla: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. "$OPENWBBASEDIR/loadconfig.sh"
	# load helperFunctions
	. "$OPENWBBASEDIR/helperFunctions.sh"
fi

# for developement only
# debug=1

case $CHARGEPOINT in
	2)
		# second charge point
		socintervallladen=$(( soc_teslalp2_intervallladen * 6 ))
		socintervall=$(( soc_teslalp2_intervall * 6 ))
		ladeleistung=$(<"$RAMDISKDIR/llaktuells1")
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		username=$soc_teslalp2_username
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
		ladeleistung=$(<"$RAMDISKDIR/llaktuell")
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		username=$soc_tesla_username
		passwordConfigText="soc_tesla_password"
		mfaPasscodeConfigText="soc_tesla_mfapasscode"
		carnumber=$soc_tesla_carnumber
		tokensfile="$MODULEDIR/tokens.lp1"
		;;
esac

getAndWriteSoc(){
	re='^-?[0-9]+$'
	# response=$(python $MODULEDIR/teslajson.py --email="$username" --tokens_file="$tokensfile" --vid="$carnumber" --json get data)
	response=$(python3 "$MODULEDIR/tesla.py" --email="$username" --tokensfile="$tokensfile" --vehicle="$carnumber" --data="vehicles/#/vehicle_data" --logprefix="Lp$CHARGEPOINT" 2>>"$MYLOGFILE")
	# current state of car
	state=$(echo "$response" | jq .state)
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: State: $state"
	soclevel=$(echo "$response" | jq .charge_state.battery_level)
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC: $soclevel"

	if  [[ $soclevel =~ $re ]] ; then
		if (( soclevel != 0 )) ; then
			echo "$soclevel" > "$socfile"
		fi
	fi
}

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
	soctimer=$((soctimer + ticksize))
	echo $soctimer > "$soctimerfile"
}

clearPassword(){
	openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Removing password from config."
	sed -i "s/^$passwordConfigText=.*/$passwordConfigText=''/" "$CONFIGFILE"
}

setTokenPassword(){
	openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Writing token password to config."
	sed -i "s/^$passwordConfigText=.*/$passwordConfigText='$TOKENPASSWORD'/" "$CONFIGFILE"
	sed -i "s/^$mfaPasscodeConfigText=.*/$mfaPasscodeConfigText=XXX/" "$CONFIGFILE"
}

checkToken(){
	returnValue=0

	# check if token is present
	if [ ! -f "$tokensfile" ]; then
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: No token found."
		openwbModulePublishState "EVSOC" 0 "Keine Zugangsdaten eingetragen" $CHARGEPOINT
		returnValue=2
	fi

	return "$returnValue"
}

wakeUpCar(){
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Waking up car."
	counter=0
	until [ $counter -ge 12 ]; do
		# response=$(python $MODULEDIR/teslajson.py --email="$username" --tokens_file="$tokensfile" --vid="$carnumber" --json do wake_up)
		response=$(python3 "$MODULEDIR/tesla.py" --email="$username" --tokensfile="$tokensfile" --vehicle="$carnumber" --command="vehicles/#/wake_up" --logprefix="Lp$CHARGEPOINT" 2>>"$MYLOGFILE")
		state=$(echo "$response" | jq .state)
		if [ "$state" = "\"online\"" ]; then
			break
		fi
		counter=$((counter+1))
		sleep 5
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Loop: $counter State: $state"
	done
	openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Car state after wakeup: $state"
	if [ "$state" = "\"online\"" ]; then
		return 0
	else
		return 1
	fi
}

soctimer=$(<"$soctimerfile")
openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: timer = $soctimer"
if (( ladeleistung > 1000 )); then
	openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Car is charging"
	if (( soctimer < socintervallladen )); then
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		incrementTimer
	else
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Requesting SoC"
		echo 0 > "$soctimerfile"
		checkToken
		checkResult=$?
		if [ "$checkResult" == 0 ]; then
			# car cannot be asleep while charging
			getAndWriteSoc
			checkResult=$?
			if [ "$checkResult" == 0 ]; then
				openwbModulePublishState "EVSOC" 0 "Erfolgreich" $CHARGEPOINT
			fi
		fi
	fi
else
	openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Car is not charging"
	if (( soctimer < socintervall )); then
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		incrementTimer
	else
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Requesting SoC"
		echo 0 > "$soctimerfile"
		checkToken
		checkResult=$?
		if [ "$checkResult" == 0 ]; then
			# todo: do not always wake car
			wakeUpCar
			wakeUpResult=$?
			if [ $wakeUpResult -eq 0 ]; then
				openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Update SoC"
			else
				openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Car not online after timeout. SoC will be outdated!"
				openwbModulePublishState "EVSOC" 1 "WakeUp fehlgeschlagen" $CHARGEPOINT
			fi
			getAndWriteSoc
			checkResult=$?
			if [ "$checkResult" == 0 ]; then
				openwbModulePublishState "EVSOC" 0 "Erfolgreich" $CHARGEPOINT
			fi
		fi
	fi
fi
