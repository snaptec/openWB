#!/bin/bash

openwbModulePublishState() {
	# $1: Modultyp (EVU, LP, EVSOC, PV, BAT)
	# $2: Status (0=Ok, 1=Warning, 2=Error)
	# $3: Meldung (String)
	# $4: Index (bei LP und PV und EVSOC)
	case $1 in
		"EVU")
			if (( $# != 3 )); then
				echo "openwbPublishStatus: Wrong number of arguments: EVU $#"
			else
				mosquitto_pub -t "openWB/set/evu/faultState" -r -m "$2"
				mosquitto_pub -t "openWB/set/evu/faultStr" -r -m "$3"
			fi
			;;
		"LP")
			if (( $# != 4 )); then
				echo "openwbPublishStatus: Wrong number of arguments: LP $#"
			else
				mosquitto_pub -t "openWB/set/lp/${4}/faultState" -r -m "$2"
				mosquitto_pub -t "openWB/set/lp/${4}/faultStr" -r -m "$3"
			fi
			;;
		"EVSOC")
			if (( $# != 4 )); then
				echo "openwbPublishStatus: Wrong number of arguments: EVSOC $#"
			else
				mosquitto_pub -t "openWB/set/lp/${4}/socFaultState" -r -m "$2"
				mosquitto_pub -t "openWB/set/lp/${4}/socFaultStr" -r -m "$3"
			fi
			;;
		"PV")
			if (( $# != 4 )); then
				echo "openwbPublishStatus: Wrong number of arguments: PV $#"
			else
				mosquitto_pub -t "openWB/set/pv/${4}/faultState" -r -m "$2"
				mosquitto_pub -t "openWB/set/pv/${4}/faultStr" -r -m "$3"
			fi
			;;
		"BAT")
			if (( $# != 3 )); then
				echo "openwbPublishStatus: Wrong number of arguments: BAT $#"
			else
				mosquitto_pub -t "openWB/set/houseBattery/faultState" -r -m "$2"
				mosquitto_pub -t "openWB/set/houseBattery/faultStr" -r -m "$3"
			fi
			;;
		*)
			echo "openwbPublishStatus: Unknown module type: $1"
			;;
	esac
}
export -f openwbModulePublishState

openwbDebugLog() {
	# $1: Channel (MAIN=default, EVSOC, PV, MQTT, RFID, SMARTHOME, CHARGESTAT)
	# $2: Level (0=Info, 1=Regelwerte , 2=Berechnungsgrundlage)
	# $3: Meldung (String)
	LOGFILE="/var/log/openWB.log"
	timestamp=$(date +"%Y-%m-%d %H:%M:%S")

	if [[ -z "$debug" ]]; then
		# enable all levels as global $debug is not set up yet
		DEBUGLEVEL=2
	else
		DEBUGLEVEL=$debug
	fi
	# echo "LVL: $2 DEBUG: $debug DEBUGLEVEL: $DEBUGLEVEL" >> $LOGFILE
	if (( $2 <= DEBUGLEVEL )); then
		case $1 in
			"EVSOC")
				LOGFILE="/var/www/html/openWB/ramdisk/soc.log"
				;;
			"PV")
				LOGFILE="/var/www/html/openWB/ramdisk/nurpv.log"
				;;
			"MQTT")
				LOGFILE="/var/www/html/openWB/ramdisk/mqtt.log"
				;;
			"RFID")
				LOGFILE="/var/www/html/openWB/ramdisk/rfid.log"
				;;
			"SMARTHOME")
				LOGFILE="/var/www/html/openWB/ramdisk/smarthome.log"
				;;
			"CHARGESTAT")
				LOGFILE="/var/www/html/openWB/ramdisk/ladestatus.log"
				;;
			*)
				# MAIN
				LOGFILE="/var/log/openWB.log"
				;;
		esac
		if (( DEBUGLEVEL > 0 )); then
			echo "$timestamp: PID: $$: $3 (LV$2) at $(caller 0)" >> $LOGFILE
		else
			echo "$timestamp: PID: $$: $3 (LV$2)" >> $LOGFILE
		fi
	fi
}
export -f openwbDebugLog

# Enable all python scripts to import from the "package"-directory without fiddling with sys.path individually
SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
export PYTHONPATH="$SCRIPT_DIR/packages"
