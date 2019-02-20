#!/bin/bash
hook(){
if (( hook1_aktiv == "1" )); then
	if (( uberschuss > hook1ein_watt )); then
		if [ ! -e ramdisk/hook1aktiv ]; then
			touch ramdisk/hook1aktiv
			curl -s --connect-timeout 5 $hook1ein_url > /dev/null
			if [[ $debug == "1" ]]; then
				echo "Gerät 1 aktiviert"
			fi
			if ((pushbenachrichtigung == "1")); then
				./runs/pushover.sh "Gerät 1 eingeschaltet bei $uberschuss"
			fi
		fi

	fi
	if (( uberschuss < hook1aus_watt )); then
		if [ -e ramdisk/hook1aktiv ]; then
			rm ramdisk/hook1aktiv
			curl -s --connect-timeout 5 $hook1aus_url > /dev/null
			if [[ $debug == "1" ]]; then
				echo "Gerät 1 deaktiviert"
			fi
			if ((pushbenachrichtigung == "1")); then
				./runs/pushover.sh "Gerät 1 ausgeschaltet bei $uberschuss"
			fi

		fi
	fi	
fi













}


