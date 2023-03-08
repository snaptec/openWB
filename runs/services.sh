#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

declare -F "openwbDebugLog" > /dev/null || . "$OPENWBBASEDIR/helperFunctions.sh"
[[ -z "$debug" ]] && . "$OPENWBBASEDIR/loadconfig.sh"

. "$OPENWBBASEDIR/runs/rfid/rfidHelper.sh"
. "$OPENWBBASEDIR/runs/pushButtons/pushButtonsHelper.sh"
. "$OPENWBBASEDIR/runs/rse/rseHelper.sh"

stop() {
	openwbDebugLog "MAIN" 0 "Stopping OpenWB services"
	local service_pattern='^python.*/(modbusserver|smarthomehandler|smarthomemq|mqttsub|isss|buchse|legacy_run_server|rseDaemon|pushButtonsDaemon|rfidDaemon|readrfid)\.py'
	sudo pkill -f "$service_pattern"
	# Wait until all services terminated (max 10 seconds)
	pgrep -f "$service_pattern" | timeout 10 xargs -n1 -I'{}' tail -f --pid="{}" /dev/null
	openwbDebugLog "MAIN" 0 "OpenWB services stopped"
}


start() {
	openwbDebugLog "MAIN" 0 "Starting OpenWB services"


	openwbDebugLog "MAIN" 1 "Starting modbus server..."
	if pgrep -f '^python.*/modbusserver.py' > /dev/null
	then
		openwbDebugLog "MAIN" 1 "modbus tcp server already running"
	else
		openwbDebugLog "MAIN" 0 "modbus tcp server not running! restarting process"
		sudo nohup python3 "$OPENWBBASEDIR/runs/modbusserver/modbusserver.py" >> "$OPENWBBASEDIR/ramdisk/openWB.log" 2>&1 &
	fi


	openwbDebugLog "MAIN" 1 "Starting MQTT handler..."
	if pgrep -f '^python.*/mqttsub.py' > /dev/null
	then
		openwbDebugLog "MAIN" 1 "mqtt handler is already running"
	else
		openwbDebugLog "MAIN" 0 "mqtt handler not running! restarting process"
		nohup python3 "$OPENWBBASEDIR/runs/mqttsub.py" >> "$OPENWBBASEDIR/ramdisk/openWB.log" 2>&1 &
	fi


	openwbDebugLog "MAIN" 1 "Starting smart home handler..."
	if pgrep -f '^python.*/smarthomemq.py' > /dev/null
	then
		openwbDebugLog "MAIN" 1 "smart home handler is already running"
	else
		openwbDebugLog "MAIN" 0 "smart home handler not running! restarting process"
		nohup python3 "$OPENWBBASEDIR/runs/smarthomemq.py" >> "$OPENWBBASEDIR/ramdisk/smarthome.log" 2>&1 &
	fi


	openwbDebugLog "MAIN" 1 "Starting legacy run server..."
	pgrep -f "$OPENWBBASEDIR/packages/legacy_run_server.py" > /dev/null
	if [ $? == 1 ]
	then
		openwbDebugLog "MAIN" 0 "legacy run server is not running. Restarting process"
		bash "$OPENWBBASEDIR/packages/legacy_run_server.sh"
	else
		openwbDebugLog "MAIN" 1 "legacy run server is already running"
	fi


	if (( isss == 1 )) || [[ "$evsecon" == "daemon" ]] || [[ "$evsecon" == "buchse" ]]; then
		if [[ "$evsecon" == "buchse" ]]; then
			isss_mode="socket"
		elif [[ $lastmanagement == 1 ]]; then
			isss_mode="duo"
		else
			isss_mode="daemon"
		fi
		prev_isss_mode=$(< $OPENWBBASEDIR/ramdisk/isss_mode)

		openwbDebugLog "MAIN" 1 "external openWB, daemon mode or socket mode configured"
		if pgrep -f '^python.*/isss.py' > /dev/null && [[ $prev_isss_mode == $isss_mode ]];
		then
			openwbDebugLog "MAIN" 1 "isss handler already running"
		else
			openwbDebugLog "MAIN" 0 "Start/restart isss handler in mode $isss_mode."
			if [ -f /home/pi/ppbuchse ]; then
				ppbuchse=$(< /home/pi/ppbuchse)
				re='^[0-9]+$'
				if ! [[ $ppbuchse =~ $re ]] ; then
					openwbDebugLog "MAIN" 0 "Invalid value in ppbuchse. Set ppbuchse to 32."
					ppbuchse=32
				fi
			else
				ppbuchse=32
			fi
			nohup python3 "$OPENWBBASEDIR/runs/isss.py" "$isss_mode" "$ppbuchse">>"$OPENWBBASEDIR/ramdisk/isss.log" 2>&1 &
		fi
		echo "$isss_mode" > $OPENWBBASEDIR/ramdisk/isss_mode
	else
		openwbDebugLog "MAIN" 1 "external openWB, daemon mode or socket mode not configured; checking network setup"
		local ethstate=$(</sys/class/net/eth0/carrier)
		if (( ethstate == 1 )); then
			sudo ifconfig eth0:0 "$virtual_ip_eth0" netmask 255.255.255.0 up
			if [ -d /sys/class/net/wlan0 ]; then
				sudo ifconfig wlan0:0 "$virtual_ip_wlan0" netmask 255.255.255.0 down
				local wlanstate=$(</sys/class/net/wlan0/carrier)
				if (( wlanstate == 1 )); then
					sudo systemctl stop hostapd
					sudo systemctl stop dnsmasq
				fi
			fi
		else
			if [ -d /sys/class/net/wlan0 ]; then
				sudo ifconfig wlan0:0 "$virtual_ip_wlan0" netmask 255.255.255.0 up
			fi
			sudo ifconfig eth0:0 "$virtual_ip_eth0" netmask 255.255.255.0 down
		fi
		# kill obsolete isss handler
		sudo pkill -f '^python.*/isss.py'
	fi

	rseSetup "$rseenabled" 0

	pushButtonsSetup "$ladetaster" 0

	rfidSetup "$rfidakt" 0 "$rfidlist"
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		stop
		start
		;;
	*)
		echo "Usage: ${BASH_SOURCE[0]} {start|stop|restart}"
		exit 1
esac
