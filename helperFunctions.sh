#!/bin/bash

openwbPublishModuleState() {
	# $1: Modultyp (EVU, LP, EVSOC, PV, BAT)
	# $2: Status (0=Ok, 1=Warning, 2=Error)
	# $3: Meldung (String)
	# $4: Index (bei LP und PV)
	case $1 in
		"EVU")
			if (( $# != 3 )); then
				echo "openwbPublishStatus: Wrong number of arguments: EVU $#"
			else
				mosquitto_pub -t openWB/set/evu/faultState -r -m "$2"
				mosquitto_pub -t openWB/set/evu/faultStr -r -m "$3"
			fi
			;;
		"LP")
			if (( $# != 4 )); then
				echo "openwbPublishStatus: Wrong number of arguments: LP $#"
			else
				mosquitto_pub -t openWB/set/lp/${4}/faultState -r -m "$2"
				mosquitto_pub -t openWB/set/lp/${4}/faultStr -r -m "$3"
			fi
			;;
		"EVSOC")
			if (( $# != 4 )); then
				echo "openwbPublishStatus: Wrong number of arguments: EVSOC $#"
			else
				mosquitto_pub -t openWB/set/lp/${4}/socFaultState -r -m "$2"
				mosquitto_pub -t openWB/set/lp/${4}/socFaultStr -r -m "$3"
			fi
			;;
		"PV")
			if (( $# != 4 )); then
				echo "openwbPublishStatus: Wrong number of arguments: PV $#"
			else
				mosquitto_pub -t openWB/set/pv/${4}/faultState -r -m "$2"
				mosquitto_pub -t openWB/set/pv/${4}/faultStr -r -m "$3"
			fi
			;;
		"BAT")
			if (( $# != 3 )); then
				echo "openwbPublishStatus: Wrong number of arguments: BAT $#"
			else
				mosquitto_pub -t openWB/set/houseBattery/faultState -r -m "$2"
				mosquitto_pub -t openWB/set/houseBattery/faultStr -r -m "$3"
			fi
			;;
		*)
			echo "openwbPublishStatus: Unknown module type: $1"
			;;
	esac
}
