#!/bin/bash
hook(){
if (( hook1_aktiv == "1" )); then
	if (( uberschuss > hook1ein_watt )); then
		if [ ! -e ramdisk/hook1aktiv ]; then
			touch ramdisk/hook1aktiv
			curl -s --connect-timeout 5 $hook1ein_url > /dev/null
			echo "$date WebHook 1 aktiviert" >> ramdisk/ladestatus.log

			if [[ $debug == "1" ]]; then
				echo "Gerät 1 aktiviert"
			fi
			if ((pushbenachrichtigung == "1")); then
				./runs/pushover.sh "Gerät 1 eingeschaltet bei $uberschuss"
			fi
		fi

	fi
	if [ -e ramdisk/hook1aktiv  ]; then
		if test $(find "ramdisk/hook1aktiv" -mmin +$hook1_dauer); then
			if (( uberschuss < hook1aus_watt )); then
				rm ramdisk/hook1aktiv
				curl -s --connect-timeout 5 $hook1aus_url > /dev/null
				echo "$date WebHook 1 deaktiviert" >> ramdisk/ladestatus.log
				if [[ $debug == "1" ]]; then
					echo "Gerät 1 deaktiviert"
				fi
				if ((pushbenachrichtigung == "1")); then
					./runs/pushover.sh "Gerät 1 ausgeschaltet bei $uberschuss"
				fi
			fi	
		fi

	fi
fi
if (( hook2_aktiv == "1" )); then
	if (( uberschuss > hook2ein_watt )); then
		if [ ! -e ramdisk/hook2aktiv ]; then
			touch ramdisk/hook2aktiv
			curl -s --connect-timeout 5 $hook2ein_url > /dev/null
			echo "$date WebHook 2 aktiviert" >> ramdisk/ladestatus.log

			if [[ $debug == "1" ]]; then
				echo "Gerät 2 aktiviert"
			fi
			if ((pushbenachrichtigung == "1")); then
				./runs/pushover.sh "Gerät 2 eingeschaltet bei $uberschuss"
			fi
		fi

	fi
	if [ -e ramdisk/hook2aktiv  ]; then
		if test $(find "ramdisk/hook2aktiv" -mmin +$hook2_dauer); then
			if (( uberschuss < hook2aus_watt )); then
				rm ramdisk/hook2aktiv
				curl -s --connect-timeout 5 $hook2aus_url > /dev/null
				echo "$date WebHook 2 deaktiviert" >> ramdisk/ladestatus.log
				if [[ $debug == "1" ]]; then
					echo "Gerät 2 deaktiviert"
				fi
				if ((pushbenachrichtigung == "1")); then
					./runs/pushover.sh "Gerät 2 ausgeschaltet bei $uberschuss"
				fi
			fi
		fi	

	fi
fi
if (( hook3_aktiv == "1" )); then
	if (( uberschuss > hook3ein_watt )); then
		if [ ! -e ramdisk/hook3aktiv ]; then
			touch ramdisk/hook3aktiv
			curl -s --connect-timeout 5 $hook3ein_url > /dev/null
			echo "$date WebHook 3 aktiviert" >> ramdisk/ladestatus.log

			if [[ $debug == "1" ]]; then
				echo "Gerät 3 aktiviert"
			fi
			if ((pushbenachrichtigung == "1")); then
				./runs/pushover.sh "Gerät 3 eingeschaltet bei $uberschuss"
			fi
		fi

	fi
	if [ -e ramdisk/hook3aktiv  ]; then
		if test $(find "ramdisk/hook3aktiv" -mmin +$hook3_dauer); then
			if (( uberschuss < hook3aus_watt )); then
				rm ramdisk/hook3aktiv
				curl -s --connect-timeout 5 $hook3aus_url > /dev/null
				echo "$date WebHook 3 deaktiviert" >> ramdisk/ladestatus.log
	
				if [[ $debug == "1" ]]; then
					echo "Gerät 3 deaktiviert"
				fi
				if ((pushbenachrichtigung == "1")); then
					./runs/pushover.sh "Gerät 3 ausgeschaltet bei $uberschuss"
				fi
			fi
		fi
	fi	
fi
if (( verbraucher1_aktiv == "1")); then
	echo "1" > /var/www/html/openWB/ramdisk/verbraucher1vorhanden
	if [[ $verbraucher1_typ == "http" ]]; then
		verbraucher1_watt=$(curl --connect-timeout 2 -s $verbraucher1_urlw &)
		rekwh='^[-+]?[0-9]+\.?[0-9]*$'
		if ! [[ $verbraucher1_watt =~ $rekwh ]] ; then
	   		verbraucher1_watt="0"
		fi
		echo $verbraucher1_watt > /var/www/html/openWB/ramdisk/verbraucher1_watt
		verbraucher1_wh=$(curl --connect-timeout 2 -s $verbraucher1_urlh &)
		if ! [[ $verbraucher1_wh =~ $rekwh ]] ; then
	   		verbraucher1_wh="0"
		fi
		echo $verbraucher1_wh > /var/www/html/openWB/ramdisk/verbraucher1_wh
	fi
	if [[ $verbraucher1_typ == "mpm3pm" ]]; then
		if [[ $verbraucher1_source == *"dev"* ]]; then
			sudo python modules/verbraucher/mpm3pmlocal.py 1 $verbraucher1_source $verbraucher1_id &
		else
			sudo python modules/verbraucher/mpm3pmremote.py 1 $verbraucher1_source $verbraucher1_id &
		fi
	fi	
fi














}


