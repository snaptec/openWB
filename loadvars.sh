#!/bin/bash
loadvars(){
	#reload mqtt vars
	renewmqtt=$(</var/www/html/openWB/ramdisk/renewmqtt)
	if (( renewmqtt == 1 )); then
		echo 0 > /var/www/html/openWB/ramdisk/renewmqtt
		echo 01 | tee ramdisk/mqtt*
	fi

	#get temp vars
	sofortll=$(<ramdisk/lp1sofortll)
	sofortlls1=$(<ramdisk/lp2sofortll)
	sofortlls2=$(<ramdisk/lp3sofortll)
	sofortlllp4=$(<ramdisk/lp4sofortll)
	sofortlllp5=$(<ramdisk/lp5sofortll)
	sofortlllp6=$(<ramdisk/lp6sofortll)
	sofortlllp7=$(<ramdisk/lp7sofortll)
	sofortlllp8=$(<ramdisk/lp8sofortll)

	#get oldvars for mqtt
	opvwatt=$(<ramdisk/mqttpvwatt)
	owattbezug=$(<ramdisk/mqttwattbezug)
	ollaktuell=$(<ramdisk/mqttladeleistunglp1)
	ohausverbrauch=$(<ramdisk/mqtthausverbrauch)
	ollkombiniert=$(<ramdisk/llkombiniert)
	ollaktuells1=$(<ramdisk/mqttladeleistungs1)
	ollaktuells2=$(<ramdisk/mqttladeleistungs2)
	ospeicherleistung=$(<ramdisk/mqttspeicherleistung)
	oladestatus=$(<ramdisk/mqttlastladestatus)
	olademodus=$(<ramdisk/mqttlastlademodus)
	osoc=$(<ramdisk/mqttsoc)
	osoc1=$(<ramdisk/mqttsoc1)
	ostopchargeafterdisclp1=$(<ramdisk/mqttstopchargeafterdisclp1)
	ostopchargeafterdisclp2=$(<ramdisk/mqttstopchargeafterdisclp2)
	ostopchargeafterdisclp3=$(<ramdisk/mqttstopchargeafterdisclp3)
	ostopchargeafterdisclp4=$(<ramdisk/mqttstopchargeafterdisclp4)
	ostopchargeafterdisclp5=$(<ramdisk/mqttstopchargeafterdisclp5)
	ostopchargeafterdisclp6=$(<ramdisk/mqttstopchargeafterdisclp6)
	ostopchargeafterdisclp7=$(<ramdisk/mqttstopchargeafterdisclp7)
	ostopchargeafterdisclp8=$(<ramdisk/mqttstopchargeafterdisclp8)
	ospeichersoc=$(<ramdisk/mqttspeichersoc)
	ladestatus=$(</var/www/html/openWB/ramdisk/ladestatus)
	odailychargelp1=$(<ramdisk/mqttdailychargelp1)
	odailychargelp2=$(<ramdisk/mqttdailychargelp2)
	odailychargelp3=$(<ramdisk/mqttdailychargelp3)
	oaktgeladens1=$(<ramdisk/mqttaktgeladens1)
	oaktgeladens2=$(<ramdisk/mqttaktgeladens2)
	oaktgeladen=$(<ramdisk/mqttaktgeladen)
	orestzeitlp1=$(<ramdisk/mqttrestzeitlp1)
	orestzeitlp2=$(<ramdisk/mqttrestzeitlp2)
	orestzeitlp3=$(<ramdisk/mqttrestzeitlp3)
	ogelrlp1=$(<ramdisk/mqttgelrlp1)
	ogelrlp2=$(<ramdisk/mqttgelrlp2)
	ogelrlp3=$(<ramdisk/mqttgelrlp3)
	olastregelungaktiv=$(<ramdisk/lastregelungaktiv)
	ohook1aktiv=$(<ramdisk/hook1akt)
	ohook2aktiv=$(<ramdisk/hook2akt)
	ohook3aktiv=$(<ramdisk/hook3akt)
	lp1enabled=$(<ramdisk/lp1enabled)
	lp2enabled=$(<ramdisk/lp2enabled)
	lp3enabled=$(<ramdisk/lp3enabled)
	lp4enabled=$(<ramdisk/lp4enabled)
	lp5enabled=$(<ramdisk/lp5enabled)
	lp6enabled=$(<ramdisk/lp6enabled)
	lp7enabled=$(<ramdisk/lp7enabled)
	lp8enabled=$(<ramdisk/lp8enabled)

	version=$(<web/version)
	# EVSE DIN Plug State
	declare -r IsNumberRegex='^[0-9]+$'
	if [[ $evsecon == "modbusevse" ]]; then
		if [[ "$modbusevseid" == 0 ]]; then
			if [ -f /var/www/html/openWB/ramdisk/evsemodulconfig ]; then
				modbusevsesource=$(<ramdisk/evsemodulconfig)
				modbusevseid=1
			else
				if [[ -e "/dev/ttyUSB0" ]]; then
					echo "/dev/ttyUSB0" > ramdisk/evsemodulconfig
				else
					echo "/dev/serial0" > ramdisk/evsemodulconfig
				fi
				modbusevsesource=$(<ramdisk/evsemodulconfig)
				modbusevseid=1

			fi
		fi
		evseplugstate=$(sudo python runs/readmodbus.py $modbusevsesource $modbusevseid 1002 1)
		if [ -z "${evseplugstate}" ] || ! [[ "${evseplugstate}" =~ $IsNumberRegex ]]; then
			# EVSE read returned empty or non-numeric value --> use last state for this loop
			evseplugstate=$(</var/www/html/openWB/ramdisk/evseplugstate)
			openwbDebugLog "MAIN" 0 "Modbus EVSE read CP1 issue - using previous state '${evseplugstate}'"
		else
			echo $evseplugstate > /var/www/html/openWB/ramdisk/evseplugstate
		fi
		ladestatuslp1=$(</var/www/html/openWB/ramdisk/ladestatus)
		if [ "$evseplugstate" -ge "0" ] && [ "$evseplugstate" -le "10" ] ; then
			if [[ $evseplugstate > "1" ]]; then
				plugstat=$(</var/www/html/openWB/ramdisk/plugstat)
				if [[ $plugstat == "0" ]] ; then
					if [[ $pushbplug == "1" ]] && [[ $ladestatuslp1 == "0" ]] && [[ $pushbenachrichtigung == "1" ]] ; then
						message="Fahrzeug eingesteckt. Ladung startet bei erfüllter Ladebedingung automatisch."
						/var/www/html/openWB/runs/pushover.sh "$message"
					fi
					if [[ $displayconfigured == "1" ]] && [[ $displayEinBeimAnstecken == "1" ]] ; then
						export DISPLAY=:0 && xset dpms force on && xset dpms $displaysleep $displaysleep $displaysleep
					fi
					echo 20000 > /var/www/html/openWB/ramdisk/soctimer
				fi
				echo 1 > /var/www/html/openWB/ramdisk/plugstat
				plugstat=1
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstat
				plugstat=0
			fi
			if [[ $evseplugstate > "2" ]] && [[ $ladestatuslp1 == "1" ]] && [[ $lp1enabled == "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestat
				chargestat=1
			else
				echo 0 > /var/www/html/openWB/ramdisk/chargestat
				chargestat=0
			fi
		fi
	else
		pluggedin=$(</var/www/html/openWB/ramdisk/pluggedin)
		if [ "$pluggedin" -gt "0" ]; then
			if [[ $pushbplug == "1" ]] && [[ $ladestatuslp1 == "0" ]] && [[ $pushbenachrichtigung == "1" ]] ; then
				message="Fahrzeug eingesteckt. Ladung startet bei erfüllter Ladebedingung automatisch."
				/var/www/html/openWB/runs/pushover.sh "$message"
			fi
			if [[ $displayconfigured == "1" ]] && [[ $displayEinBeimAnstecken == "1" ]] ; then
				export DISPLAY=:0 && xset dpms force on && xset dpms $displaysleep $displaysleep $displaysleep
			fi
			echo 20000 > /var/www/html/openWB/ramdisk/soctimer
			echo 0 > /var/www/html/openWB/ramdisk/pluggedin
		fi

		plugstat=$(<ramdisk/plugstat)
		chargestat=$(<ramdisk/chargestat)
	fi
	if [[ $evsecon == "ipevse" ]]; then
		evseplugstatelp1=$(sudo python runs/readipmodbus.py $evseiplp1 $evseidlp1 1002 1)
		if [ -z "${evseplugstate}" ] || ! [[ "${evseplugstate}" =~ $IsNumberRegex ]]; then
			evseplugstate=$(</var/www/html/openWB/ramdisk/evseplugstate)
			openwbDebugLog "MAIN" 0 "IP EVSE read CP1 issue - using previous state '${evseplugstate}'"
		else
			echo $evseplugstate > /var/www/html/openWB/ramdisk/evseplugstate
		fi
		ladestatuslp1=$(</var/www/html/openWB/ramdisk/ladestatus)
		if [[ $evseplugstatelp1 > "1" ]]; then
			echo 1 > /var/www/html/openWB/ramdisk/plugstat
		else
			echo 0 > /var/www/html/openWB/ramdisk/plugstat
		fi
		if [[ $evseplugstatelp1 > "2" ]] && [[ $ladestatuslp1 == "1" ]] && [[ $lp1enabled == "1" ]]; then
			echo 1 > /var/www/html/openWB/ramdisk/chargestat
		else
			echo 0 > /var/www/html/openWB/ramdisk/chargestat
		fi
	fi

	if [[ $lastmanagement == "1" ]]; then
		ConfiguredChargePoints=2
		if [[ $evsecons1 == "modbusevse" ]]; then
			evseplugstatelp2=$(sudo python runs/readmodbus.py $evsesources1 $evseids1 1002 1)
			if [ -z "${evseplugstatelp2}" ] || ! [[ "${evseplugstatelp2}" =~ $IsNumberRegex ]]; then
				evseplugstatelp2=$(</var/www/html/openWB/ramdisk/evseplugstatelp2)
				openwbDebugLog "MAIN" 0 "Modbus EVSE read CP2 issue - using previous state '${evseplugstatelp2}'"
			else
				echo $evseplugstatelp2 > /var/www/html/openWB/ramdisk/evseplugstatelp2
			fi
			ladestatuss1=$(</var/www/html/openWB/ramdisk/ladestatuss1)
			if [[ $evseplugstatelp2 > "0" ]] && [[ $evseplugstatelp2 < "7" ]] ; then
				if [[ $evseplugstatelp2 > "1" ]]; then
					plugstat2=$(</var/www/html/openWB/ramdisk/plugstats1)

					if [[ $plugstat2 == "0" ]] ; then
						if [[ $displayconfigured == "1" ]] && [[ $displayEinBeimAnstecken == "1" ]] ; then
							export DISPLAY=:0 && xset dpms force on && xset dpms $displaysleep $displaysleep $displaysleep
						fi
						echo 20000 > /var/www/html/openWB/ramdisk/soctimer1
					fi
					echo 1 > /var/www/html/openWB/ramdisk/plugstats1
					plugstat2=1
					plugstats1=$plugstat2
				else
					echo 0 > /var/www/html/openWB/ramdisk/plugstats1
					plugstat2=0
					plugstats1=$plugstat2
				fi
				if [[ $evseplugstatelp2 > "2" ]] && [[ $ladestatuss1 == "1" ]] ; then
					echo 1 > /var/www/html/openWB/ramdisk/chargestats1
				else
					echo 0 > /var/www/html/openWB/ramdisk/chargestats1
				fi

			fi
		fi
		if [[ $evsecons1 == "slaveeth" ]]; then
			evseplugstatelp2=$(sudo python runs/readslave.py 1002 1)
			if [ -z "${evseplugstatelp2}" ] || ! [[ "${evseplugstatelp2}" =~ $IsNumberRegex ]]; then
				evseplugstatelp2=$(</var/www/html/openWB/ramdisk/evseplugstatelp2)
				openwbDebugLog "MAIN" 0 "Slaveeth EVSE read CP2 issue - using previous state '${evseplugstatelp2}'"
			else
				echo $evseplugstatelp2 > /var/www/html/openWB/ramdisk/evseplugstatelp2
			fi
			ladestatuss1=$(</var/www/html/openWB/ramdisk/ladestatuss1)

			if [[ $evseplugstatelp2 > "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/plugstats1
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstats1
			fi
			if [[ $evseplugstatelp2 > "2" ]] && [[ $ladestatuss1 == "1" ]] ; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestats1
			else
				echo 0 > /var/www/html/openWB/ramdisk/chargestats1
			fi
		fi
		if [[ $evsecons1 == "ipevse" ]]; then
			evseplugstatelp2=$(sudo python runs/readipmodbus.py $evseiplp2 $evseidlp2 1002 1)
			if [ -z "${evseplugstatelp2}" ] || ! [[ "${evseplugstatelp2}" =~ $IsNumberRegex ]]; then
				evseplugstatelp2=$(</var/www/html/openWB/ramdisk/evseplugstatelp2)
				openwbDebugLog "MAIN" 0 "IP EVSE read CP2 issue - using previous state '${evseplugstatelp2}'"
			else
				echo $evseplugstatelp2 > /var/www/html/openWB/ramdisk/evseplugstatelp2
			fi
			ladestatuslp2=$(</var/www/html/openWB/ramdisk/ladestatuss1)

			if [[ $evseplugstatelp2 > "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/plugstats1
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstats1
			fi
			if [[ $evseplugstatelp2 > "2" ]] && [[ $ladestatuslp2 == "1" ]] && [[ $lp2enabled == "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestats1
			else
				echo 0 > /var/www/html/openWB/ramdisk/chargestats1
			fi
		fi
		plugstatlp2=$(<ramdisk/plugstats1)
		chargestatlp2=$(<ramdisk/chargestats1)
	else
		plugstatlp2=$(<ramdisk/plugstats1)
		chargestatlp2=$(<ramdisk/chargestats1)
		ConfiguredChargePoints=1
	fi

	if [[ $lastmanagements2 == "1" ]]; then
		ConfiguredChargePoints=3
		if [[ $evsecons2 == "ipevse" ]]; then
			evseplugstatelp3=$(sudo python runs/readipmodbus.py $evseiplp3 $evseidlp3 1002 1)
			if [ -z "${evseplugstatelp3}" ] || ! [[ "${evseplugstatelp3}" =~ $IsNumberRegex ]]; then
				evseplugstatelp3=$(</var/www/html/openWB/ramdisk/evseplugstatelp3)
				openwbDebugLog "MAIN" 0 "IP EVSE read CP3 issue - using previous state '${evseplugstatelp3}'"
			else
				echo $evseplugstatelp3 > /var/www/html/openWB/ramdisk/evseplugstatelp3
			fi
			ladestatuslp3=$(</var/www/html/openWB/ramdisk/ladestatuss2)

			if [[ $evseplugstatelp3 > "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/plugstatlp3
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstatlp3
			fi
			if [[ $evseplugstatelp3 > "2" ]] && [[ $ladestatuslp3 == "1" ]] && [[ $lp3enabled == "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestatlp3
			else
				echo 0 > /var/www/html/openWB/ramdisk/chargestatlp3
			fi
		fi


		if [[ $evsecons2 == "modbusevse" ]]; then
			evseplugstatelp3=$(sudo python runs/readmodbus.py $evsesources2 $evseids2 1002 1)
			if [ -z "${evseplugstatelp3}" ] || ! [[ "${evseplugstatelp3}" =~ $IsNumberRegex ]]; then
				evseplugstatelp3=$(</var/www/html/openWB/ramdisk/evseplugstatelp3)
				openwbDebugLog "MAIN" 0 "Modbus EVSE read CP3 issue - using previous state '${evseplugstatelp3}'"
			else
				echo $evseplugstatelp3 > /var/www/html/openWB/ramdisk/evseplugstatelp3
			fi
			ladestatuss2=$(</var/www/html/openWB/ramdisk/ladestatuss2)
			if [[ $evseplugstatelp3 > "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/plugstatlp3
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstatlp3
			fi
			if [[ $evseplugstatelp3 > "2" ]] && [[ $ladestatuss2 == "1" ]] ; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestatlp3
			else
					echo 0 > /var/www/html/openWB/ramdisk/chargestatlp3
			fi
		fi
		plugstatlp3=$(<ramdisk/plugstatlp3)
		chargestatlp3=$(<ramdisk/chargestatlp3)
	else
		plugstatlp3=$(<ramdisk/plugstatlp3)
		chargestatlp3=$(<ramdisk/chargestatlp3)
	fi

	if [[ $lastmanagementlp4 == "1" ]]; then
		ConfiguredChargePoints=4
		if [[ $evseconlp4 == "ipevse" ]]; then
			evseplugstatelp4=$(sudo python runs/readipmodbus.py $evseiplp4 $evseidlp4 1002 1)
			if [ -z "${evseplugstatelp4}" ] || ! [[ "${evseplugstatelp4}" =~ $IsNumberRegex ]]; then
				# EVSE read returned empty or non-numeric value --> use last state for this loop
				evseplugstatelp4=$(</var/www/html/openWB/ramdisk/evseplugstatelp4)
				openwbDebugLog "MAIN" 0 "IP EVSE read CP4 issue - using previous state '${evseplugstatelp4}'"
			else
				echo $evseplugstatelp4 > /var/www/html/openWB/ramdisk/evseplugstatelp4
			fi
			ladestatuslp4=$(</var/www/html/openWB/ramdisk/ladestatuslp4)

			if [[ $evseplugstatelp4 > "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/plugstatlp4
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstatlp4
			fi
			if [[ $evseplugstatelp4 > "2" ]] && [[ $ladestatuslp4 == "1" ]] && [[ $lp4enabled == "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestatlp4
			else
				echo 0 > /var/www/html/openWB/ramdisk/chargestatlp4
			fi
		fi
	fi

	if [[ $lastmanagementlp5 == "1" ]]; then
		ConfiguredChargePoints=5
		if [[ $evseconlp5 == "ipevse" ]]; then
			evseplugstatelp5=$(sudo python runs/readipmodbus.py $evseiplp5 $evseidlp5 1002 1)
			if [ -z "${evseplugstatelp5}" ] || ! [[ "${evseplugstatelp5}" =~ $IsNumberRegex ]]; then
				# EVSE read returned empty or non-numeric value --> use last state for this loop
				evseplugstatelp5=$(</var/www/html/openWB/ramdisk/evseplugstatelp5)
				openwbDebugLog "MAIN" 0 "IP EVSE read CP5 issue - using previous state '${evseplugstatelp5}'"
			else
				echo $evseplugstatelp5 > /var/www/html/openWB/ramdisk/evseplugstatelp5
			fi
			ladestatuslp5=$(</var/www/html/openWB/ramdisk/ladestatuslp5)

			if [[ $evseplugstatelp5 > "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/plugstatlp5
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstatlp5
			fi
			if [[ $evseplugstatelp5 > "2" ]] && [[ $ladestatuslp5 == "1" ]] && [[ $lp5enabled == "1" ]] ; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestatlp5
			else
				echo 0 > /var/www/html/openWB/ramdisk/chargestatlp5
			fi
		fi
	fi

	if [[ $lastmanagementlp6 == "1" ]]; then
		ConfiguredChargePoints=6
		if [[ $evseconlp6 == "ipevse" ]]; then
			evseplugstatelp6=$(sudo python runs/readipmodbus.py $evseiplp6 $evseidlp6 1002 1)
			if [ -z "${evseplugstatelp6}" ] || ! [[ "${evseplugstatelp6}" =~ $IsNumberRegex ]]; then
				# EVSE read returned empty or non-numeric value --> use last state for this loop
				evseplugstatelp6=$(</var/www/html/openWB/ramdisk/evseplugstatelp6)
				openwbDebugLog "MAIN" 0 "IP EVSE read CP6 issue - using previous state '${evseplugstatelp6}'"
			else
				echo $evseplugstatelp6 > /var/www/html/openWB/ramdisk/evseplugstatelp6
			fi
			ladestatuslp6=$(</var/www/html/openWB/ramdisk/ladestatuslp6)

			if [[ $evseplugstatelp6 > "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/plugstatlp6
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstatlp6
			fi
			if [[ $evseplugstatelp6 > "2" ]] && [[ $ladestatuslp6 == "1" ]] && [[ $lp6enabled == "1" ]] ; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestatlp6
			else
				echo 0 > /var/www/html/openWB/ramdisk/chargestatlp6
			fi
		fi
	fi

	if [[ $lastmanagementlp7 == "1" ]]; then
		ConfiguredChargePoints=7
		if [[ $evseconlp7 == "ipevse" ]]; then
			evseplugstatelp7=$(sudo python runs/readipmodbus.py $evseiplp7 $evseidlp7 1002 1)
			if [ -z "${evseplugstatelp7}" ] || ! [[ "${evseplugstatelp7}" =~ $IsNumberRegex ]]; then
				# EVSE read returned empty or non-numeric value --> use last state for this loop
				evseplugstatelp7=$(</var/www/html/openWB/ramdisk/evseplugstatelp7)
				openwbDebugLog "MAIN" 0 "IP EVSE read CP7 issue - using previous state '${evseplugstatelp7}'"
			else
				echo $evseplugstatelp7 > /var/www/html/openWB/ramdisk/evseplugstatelp7
			fi
			ladestatuslp7=$(</var/www/html/openWB/ramdisk/ladestatuslp7)

			if [[ $evseplugstatelp7 > "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/plugstatlp7
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstatlp7
			fi
			if [[ $evseplugstatelp7 > "2" ]] && [[ $ladestatuslp7 == "1" ]] && [[ $lp7enabled == "1" ]] ; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestatlp7
			else
				echo 0 > /var/www/html/openWB/ramdisk/chargestatlp7
			fi
		fi
	fi

	if [[ $lastmanagementlp8 == "1" ]]; then
		ConfiguredChargePoints=8
		if [[ $evseconlp8 == "ipevse" ]]; then
			evseplugstatelp8=$(sudo python runs/readipmodbus.py $evseiplp8 $evseidlp8 1002 1)
			if [ -z "${evseplugstatelp8}" ] || ! [[ "${evseplugstatelp8}" =~ $IsNumberRegex ]]; then
				# EVSE read returned empty or non-numeric value --> use last state for this loop
				evseplugstatelp4=$(</var/www/html/openWB/ramdisk/evseplugstatelp8)
				openwbDebugLog "MAIN" 0 "IP EVSE read CP8 issue - using previous state '${evseplugstatelp8}'"
			else
				echo $evseplugstatelp8 > /var/www/html/openWB/ramdisk/evseplugstatelp8
			fi
			ladestatuslp8=$(</var/www/html/openWB/ramdisk/ladestatuslp8)

			if [[ $evseplugstatelp8 > "1" ]]; then
				echo 1 > /var/www/html/openWB/ramdisk/plugstatlp8
			else
				echo 0 > /var/www/html/openWB/ramdisk/plugstatlp8
			fi
			if [[ $evseplugstatelp8 > "2" ]] && [[ $ladestatuslp8 == "1" ]] && [[ $lp8enabled == "1" ]] ; then
				echo 1 > /var/www/html/openWB/ramdisk/chargestatlp8
			else
				echo 0 > /var/www/html/openWB/ramdisk/chargestatlp8
			fi
		fi
	fi

	echo $ConfiguredChargePoints > ramdisk/ConfiguredChargePoints
	# Lastmanagement var check age
	if test $(find "ramdisk/lastregelungaktiv" -mmin +2); then
		echo " " > ramdisk/lastregelungaktiv
	fi

	# Werte für die Berechnung ermitteln
	lademodus=$(</var/www/html/openWB/ramdisk/lademodus)
	if [ -z "$lademodus" ] ; then
		mosquitto_pub -r -t "openWB/set/ChargeMode" -m "$bootmodus"
		lademodus=$bootmodus
	fi
	llalt=$(cat /var/www/html/openWB/ramdisk/llsoll)
	llaltlp1=$llalt

	#PV Leistung ermitteln
	if [[ $pvwattmodul != "none" ]]; then
		pv1vorhanden="1"
		echo 1 > /var/www/html/openWB/ramdisk/pv1vorhanden
		pvwatt=$(modules/$pvwattmodul/main.sh || true)
		if ! [[ $pvwatt =~ $re ]] ; then
			pvwatt="0"
		fi
		pv1watt=$pvwatt
		echo $pv1watt > ramdisk/pv1watt
	else
		pv1vorhanden="0"
		echo 0 > /var/www/html/openWB/ramdisk/pv1vorhanden
		pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
	fi
	if [[ $pv2wattmodul != "none" ]]; then
		pv2vorhanden="1"
		echo 1 > /var/www/html/openWB/ramdisk/pv2vorhanden
		pv2watt=$(modules/$pv2wattmodul/main.sh || true)
		echo $pv2watt > ramdisk/pv2watt
		pvwatt=$(( pvwatt + pv2watt ))
		pvkwh=$(</var/www/html/openWB/ramdisk/pvkwh)
		pv2kwh=$(</var/www/html/openWB/ramdisk/pv2kwh)
		pvallwh=$(echo "$pvkwh + $pv2kwh" |bc)
		#echo $pvallkwh > /var/www/html/openWB/ramdisk/pvkwh
		echo $pvallwh > /var/www/html/openWB/ramdisk/pvallwh
		echo $pvwatt > /var/www/html/openWB/ramdisk/pvallwatt
		if ! [[ $pvwatt =~ $re ]] ; then
			pvwatt="0"
		fi
	else
		pvkwh=$(</var/www/html/openWB/ramdisk/pvkwh)
		pv2vorhanden="0"
		echo 0 > /var/www/html/openWB/ramdisk/pv2vorhanden
		echo $pvkwh > /var/www/html/openWB/ramdisk/pvallwh
		echo $pvwatt > /var/www/html/openWB/ramdisk/pvallwatt
	fi

	#Speicher werte
	if [[ $speichermodul != "none" ]] ; then
		timeout 5 modules/$speichermodul/main.sh || true
		speicherleistung=$(</var/www/html/openWB/ramdisk/speicherleistung)
		speicherleistung=$(echo $speicherleistung | sed 's/\..*$//')
		speichersoc=$(</var/www/html/openWB/ramdisk/speichersoc)
		speichersoc=$(echo $speichersoc | sed 's/\..*$//')
		speichervorhanden="1"
		echo 1 > /var/www/html/openWB/ramdisk/speichervorhanden
		if [[ $speichermodul == "speicher_e3dc" ]] ; then
			pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
			echo 1 > /var/www/html/openWB/ramdisk/pv1vorhanden
			pv1vorhanden="1"

		fi
		if [[ $speichermodul == "speicher_sonneneco" ]] ; then
			pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
			echo 1 > /var/www/html/openWB/ramdisk/pv1vorhanden
			pv1vorhanden="1"
		fi
	else
		speichervorhanden="0"
		echo 0 > /var/www/html/openWB/ramdisk/speichervorhanden
	fi
	llphaset=3

	#Ladeleistung ermitteln
	if [[ $ladeleistungmodul != "none" ]]; then
		timeout 10 modules/$ladeleistungmodul/main.sh || true
		llkwh=$(</var/www/html/openWB/ramdisk/llkwh)
		llkwhges=$llkwh
		lla1=$(cat /var/www/html/openWB/ramdisk/lla1)
		lla2=$(cat /var/www/html/openWB/ramdisk/lla2)
		lla3=$(cat /var/www/html/openWB/ramdisk/lla3)
		lla1=$(echo $lla1 | sed 's/\..*$//')
		lla2=$(echo $lla2 | sed 's/\..*$//')
		lla3=$(echo $lla3 | sed 's/\..*$//')
		llv1=$(cat /var/www/html/openWB/ramdisk/llv1)
		llv2=$(cat /var/www/html/openWB/ramdisk/llv2)
		llv3=$(cat /var/www/html/openWB/ramdisk/llv3)
		ladeleistung=$(cat /var/www/html/openWB/ramdisk/llaktuell)
		ladeleistunglp1=$ladeleistung
		if ! [[ $lla1 =~ $re ]] ; then
			lla1="0"
		fi
		if ! [[ $lla2 =~ $re ]] ; then
			lla2="0"
		fi

		if ! [[ $lla3 =~ $re ]] ; then
			lla3="0"
		fi

		lp1phasen=0
		if [ $lla1 -ge $llphaset ]; then
			lp1phasen=$((lp1phasen + 1 ))
		fi
		if [ $lla2 -ge $llphaset ]; then
			lp1phasen=$((lp1phasen + 1 ))
		fi
		if [ $lla3 -ge $llphaset ]; then
			lp1phasen=$((lp1phasen + 1 ))
		fi
		echo $lp1phasen > /var/www/html/openWB/ramdisk/lp1phasen
		if ! [[ $ladeleistung =~ $re ]] ; then
			ladeleistung="0"
		fi
		ladestatus=$(</var/www/html/openWB/ramdisk/ladestatus)

	else
		lla1=0
		lla2=0
		lla3=0
		ladeleistung=0
		llkwh=0
		llkwhges=$llkwh
	fi

	#zweiter ladepunkt
	if [[ $lastmanagement == "1" ]]; then
		if [[ $socmodul1 != "none" ]]; then
			modules/$socmodul1/main.sh &
			soc1=$(</var/www/html/openWB/ramdisk/soc1)
			tmpsoc1=$(</var/www/html/openWB/ramdisk/tmpsoc1)
			if ! [[ $soc1 =~ $re ]] ; then
				soc1=$tmpsoc1
			else
				echo $soc1 > /var/www/html/openWB/ramdisk/tmpsoc1
			fi
			soc1vorhanden=1
			echo 1 > /var/www/html/openWB/ramdisk/soc1vorhanden
		else
			echo 0 > /var/www/html/openWB/ramdisk/soc1vorhanden
			soc1=0
			soc1vorhanden=0
		fi
		timeout 10 modules/$ladeleistungs1modul/main.sh || true
		llkwhs1=$(</var/www/html/openWB/ramdisk/llkwhs1)
		llkwhges=$(echo "$llkwhges + $llkwhs1" |bc)
		llalts1=$(cat /var/www/html/openWB/ramdisk/llsolls1)
		ladeleistungs1=$(cat /var/www/html/openWB/ramdisk/llaktuells1)
		ladeleistunglp2=$ladeleistungs1
		llas11=$(cat /var/www/html/openWB/ramdisk/llas11)
		llas12=$(cat /var/www/html/openWB/ramdisk/llas12)
		llas13=$(cat /var/www/html/openWB/ramdisk/llas13)
		llas11=$(echo $llas11 | sed 's/\..*$//')
		llas12=$(echo $llas12 | sed 's/\..*$//')
		llas13=$(echo $llas13 | sed 's/\..*$//')
		ladestatuss1=$(</var/www/html/openWB/ramdisk/ladestatuss1)
		if ! [[ $ladeleistungs1 =~ $re ]] ; then
		ladeleistungs1="0"
		fi
		ladeleistung=$(( ladeleistung + ladeleistungs1 ))
		echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
		lp2phasen=0
		if [ $llas11 -ge $llphaset ]; then
			lp2phasen=$((lp2phasen + 1 ))
		fi
		if [ $llas12 -ge $llphaset ]; then
			lp2phasen=$((lp2phasen + 1 ))
		fi
		if [ $llas13 -ge $llphaset ]; then
			lp2phasen=$((lp2phasen + 1 ))
		fi
		echo $lp2phasen > /var/www/html/openWB/ramdisk/lp2phasen
	else
		echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
		ladeleistunglp2=0
		soc1vorhanden=0
	fi

	#dritter ladepunkt
	if [[ $lastmanagements2 == "1" ]]; then
		timeout 10 modules/$ladeleistungs2modul/main.sh || true
		llkwhs2=$(</var/www/html/openWB/ramdisk/llkwhs2)
		llkwhges=$(echo "$llkwhges + $llkwhs2" |bc)
		llalts2=$(cat /var/www/html/openWB/ramdisk/llsolls2)
		ladeleistungs2=$(cat /var/www/html/openWB/ramdisk/llaktuells2)
		ladeleistunglp3=$ladeleistungs2
		llas21=$(cat /var/www/html/openWB/ramdisk/llas21)
		llas22=$(cat /var/www/html/openWB/ramdisk/llas22)
		llas23=$(cat /var/www/html/openWB/ramdisk/llas23)
		llas21=$(echo $llas21 | sed 's/\..*$//')
		llas22=$(echo $llas22 | sed 's/\..*$//')
		llas23=$(echo $llas23 | sed 's/\..*$//')
		lp3phasen=0
		if [ $llas21 -ge $llphaset ]; then
			lp3phasen=$((lp3phasen + 1 ))
		fi
		if [ $llas22 -ge $llphaset ]; then
			lp3phasen=$((lp3phasen + 1 ))
		fi
		if [ $llas23 -ge $llphaset ]; then
			lp3phasen=$((lp3phasen + 1 ))
		fi
		echo $lp3phasen > /var/www/html/openWB/ramdisk/lp3phasen
		ladestatuss2=$(</var/www/html/openWB/ramdisk/ladestatuss2)
		if ! [[ $ladeleistungs2 =~ $re ]] ; then
		ladeleistungs2="0"
		fi
		ladeleistung=$(( ladeleistung + ladeleistungs2 ))
		echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
	else
		echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
		ladeleistungs2="0"
		ladeleistunglp3=0
	fi

	#vierter ladepunkt
	if [[ $lastmanagementlp4 == "1" ]]; then
		if [[ "$evseconlp4" == "extopenwb" ]]; then
			timeout 3 modules/extopenwb/main.sh 4 $chargep4ip $chargep4cp || true
		else
			timeout 3 modules/mpm3pmlllp4/main.sh || true
		fi
		llkwhlp4=$(</var/www/html/openWB/ramdisk/llkwhlp4)
		llkwhges=$(echo "$llkwhges + $llkwhlp4" |bc)
		llaltlp4=$(cat /var/www/html/openWB/ramdisk/llsolllp4)
		ladeleistunglp4=$(cat /var/www/html/openWB/ramdisk/llaktuelllp4)
		lla1lp4=$(cat /var/www/html/openWB/ramdisk/lla1lp4)
		lla2lp4=$(cat /var/www/html/openWB/ramdisk/lla2lp4)
		lla3lp4=$(cat /var/www/html/openWB/ramdisk/lla3lp4)
		lla1lp4=$(echo $lla1lp4 | sed 's/\..*$//')
		lla2lp4=$(echo $lla2lp4 | sed 's/\..*$//')
		lla3lp4=$(echo $lla3lp4 | sed 's/\..*$//')
		lp4phasen=0
		if [ $lla1lp4 -ge $llphaset ]; then
			lp4phasen=$((lp4phasen + 1 ))
		fi
		if [ $lla2lp4 -ge $llphaset ]; then
			lp4phasen=$((lp4phasen + 1 ))
		fi
		if [ $lla3lp4 -ge $llphaset ]; then
			lp4phasen=$((lp4phasen + 1 ))
		fi
		echo $lp4phasen > /var/www/html/openWB/ramdisk/lp4phasen
		ladestatuslp4=$(</var/www/html/openWB/ramdisk/ladestatuslp4)
		if ! [[ $ladeleistunglp4 =~ $re ]] ; then
		ladeleistunglp4="0"
		fi
		ladeleistung=$(( ladeleistung + ladeleistunglp4 ))
	else
		ladeleistunglp4=0
	fi

	#fünfter ladepunkt
	if [[ $lastmanagementlp5 == "1" ]]; then
		if [[ "$evseconlp5" == "extopenwb" ]]; then
			timeout 3 modules/extopenwb/main.sh 5 $chargep5ip $chargep5cp || true
		else
			timeout 3 modules/mpm3pmlllp5/main.sh || true
		fi
		llkwhlp5=$(</var/www/html/openWB/ramdisk/llkwhlp5)
		llkwhges=$(echo "$llkwhges + $llkwhlp5" |bc)
		llaltlp5=$(cat /var/www/html/openWB/ramdisk/llsolllp5)
		ladeleistunglp5=$(cat /var/www/html/openWB/ramdisk/llaktuelllp5)
		lla1lp5=$(cat /var/www/html/openWB/ramdisk/lla1lp5)
		lla2lp5=$(cat /var/www/html/openWB/ramdisk/lla2lp5)
		lla3lp5=$(cat /var/www/html/openWB/ramdisk/lla3lp5)
		lla1lp5=$(echo $lla1lp5 | sed 's/\..*$//')
		lla2lp5=$(echo $lla2lp5 | sed 's/\..*$//')
		lla3lp5=$(echo $lla3lp5 | sed 's/\..*$//')
		lp5phasen=0
		if [ $lla1lp5 -ge $llphaset ]; then
			lp5phasen=$((lp5phasen + 1 ))
		fi
		if [ $lla2lp5 -ge $llphaset ]; then
			lp5phasen=$((lp5phasen + 1 ))
		fi
		if [ $lla3lp5 -ge $llphaset ]; then
			lp5phasen=$((lp5phasen + 1 ))
		fi
		echo $lp5phasen > /var/www/html/openWB/ramdisk/lp5phasen
		ladestatuslp5=$(</var/www/html/openWB/ramdisk/ladestatuslp5)
		if ! [[ $ladeleistunglp5 =~ $re ]] ; then
		ladeleistunglp5="0"
		fi
		ladeleistung=$(( ladeleistung + ladeleistunglp5 ))
	else
		ladeleistunglp5=0
	fi

	#sechster ladepunkt
	if [[ $lastmanagementlp6 == "1" ]]; then
		if [[ "$evseconlp6" == "extopenwb" ]]; then
			timeout 3 modules/extopenwb/main.sh 6 $chargep6ip $chargep6cp || true
		else
			timeout 3 modules/mpm3pmlllp6/main.sh || true
		fi
		llkwhlp6=$(</var/www/html/openWB/ramdisk/llkwhlp6)
		llkwhges=$(echo "$llkwhges + $llkwhlp6" |bc)
		llaltlp6=$(cat /var/www/html/openWB/ramdisk/llsolllp6)
		ladeleistunglp6=$(cat /var/www/html/openWB/ramdisk/llaktuelllp6)
		lla1lp6=$(cat /var/www/html/openWB/ramdisk/lla1lp6)
		lla2lp6=$(cat /var/www/html/openWB/ramdisk/lla2lp6)
		lla3lp6=$(cat /var/www/html/openWB/ramdisk/lla3lp6)
		lla1lp6=$(echo $lla1lp6 | sed 's/\..*$//')
		lla2lp6=$(echo $lla2lp6 | sed 's/\..*$//')
		lla3lp6=$(echo $lla3lp6 | sed 's/\..*$//')
		lp6phasen=0
		if [ $lla1lp6 -ge $llphaset ]; then
			lp6phasen=$((lp6phasen + 1 ))
		fi
		if [ $lla2lp6 -ge $llphaset ]; then
			lp6phasen=$((lp6phasen + 1 ))
		fi
		if [ $lla3lp6 -ge $llphaset ]; then
			lp6phasen=$((lp6phasen + 1 ))
		fi
		echo $lp6phasen > /var/www/html/openWB/ramdisk/lp6phasen
		ladestatuslp6=$(</var/www/html/openWB/ramdisk/ladestatuslp6)
		if ! [[ $ladeleistunglp6 =~ $re ]] ; then
		ladeleistunglp6="0"
		fi
		ladeleistung=$(( ladeleistung + ladeleistunglp6 ))
	else
		ladeleistunglp6=0
	fi

	#siebter ladepunkt
	if [[ $lastmanagementlp7 == "1" ]]; then
		if [[ "$evseconlp7" == "extopenwb" ]]; then
			timeout 3 modules/extopenwb/main.sh 7 $chargep7ip $chargep7cp || true
		else
			timeout 3 modules/mpm3pmlllp7/main.sh || true
		fi
		llkwhlp7=$(</var/www/html/openWB/ramdisk/llkwhlp7)
		llkwhges=$(echo "$llkwhges + $llkwhlp7" |bc)
		llaltlp7=$(cat /var/www/html/openWB/ramdisk/llsolllp7)
		ladeleistunglp7=$(cat /var/www/html/openWB/ramdisk/llaktuelllp7)
		lla1lp7=$(cat /var/www/html/openWB/ramdisk/lla1lp7)
		lla2lp7=$(cat /var/www/html/openWB/ramdisk/lla2lp7)
		lla3lp7=$(cat /var/www/html/openWB/ramdisk/lla3lp7)
		lla1lp7=$(echo $lla1lp7 | sed 's/\..*$//')
		lla2lp7=$(echo $lla2lp7 | sed 's/\..*$//')
		lla3lp7=$(echo $lla3lp7 | sed 's/\..*$//')
		ladestatuslp7=$(</var/www/html/openWB/ramdisk/ladestatuslp7)
		if ! [[ $ladeleistunglp7 =~ $re ]] ; then
		ladeleistunglp7="0"
		fi
		ladeleistung=$(( ladeleistung + ladeleistunglp7 ))
		lp7phasen=0
		if [ $lla1lp7 -ge $llphaset ]; then
			lp7phasen=$((lp7phasen + 1 ))
		fi
		if [ $lla2lp7 -ge $llphaset ]; then
			lp7phasen=$((lp7phasen + 1 ))
		fi
		if [ $lla3lp7 -ge $llphaset ]; then
			lp7phasen=$((lp7phasen + 1 ))
		fi
		echo $lp7phasen > /var/www/html/openWB/ramdisk/lp7phasen
	else
		ladeleistunglp7=0
	fi
	#achter ladepunkt
	if [[ $lastmanagementlp8 == "1" ]]; then
		if [[ "$evseconlp8" == "extopenwb" ]]; then
			timeout 3 modules/extopenwb/main.sh 8 $chargep8ip $chargep8cp || true
		else
			timeout 3 modules/mpm3pmlllp8/main.sh || true
		fi

		llkwhlp8=$(</var/www/html/openWB/ramdisk/llkwhlp8)
		llkwhges=$(echo "$llkwhges + $llkwhlp8" |bc)
		llaltlp8=$(cat /var/www/html/openWB/ramdisk/llsolllp8)
		ladeleistunglp8=$(cat /var/www/html/openWB/ramdisk/llaktuelllp8)
		lla1lp8=$(cat /var/www/html/openWB/ramdisk/lla1lp8)
		lla2lp8=$(cat /var/www/html/openWB/ramdisk/lla2lp8)
		lla3lp8=$(cat /var/www/html/openWB/ramdisk/lla3lp8)
		lla1lp8=$(echo $lla1lp8 | sed 's/\..*$//')
		lla2lp8=$(echo $lla2lp8 | sed 's/\..*$//')
		lla3lp8=$(echo $lla3lp8 | sed 's/\..*$//')
		lp8phasen=0
		if [ $lla1lp8 -ge $llphaset ]; then
			lp8phasen=$((lp8phasen + 1 ))
		fi
		if [ $lla2lp8 -ge $llphaset ]; then
			lp8phasen=$((lp8phasen + 1 ))
		fi
		if [ $lla3lp8 -ge $llphaset ]; then
			lp8phasen=$((lp8phasen + 1 ))
		fi
		echo $lp8phasen > /var/www/html/openWB/ramdisk/lp8phasen
		ladestatuslp8=$(</var/www/html/openWB/ramdisk/ladestatuslp8)
		if ! [[ $ladeleistunglp8 =~ $re ]] ; then
		ladeleistunglp8="0"
		fi
		ladeleistung=$(( ladeleistung + ladeleistunglp8 ))
	else
		ladeleistunglp8=0
	fi

	echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
	echo $llkwhges > ramdisk/llkwhges

	#Schuko-Steckdose an openWB
	if [[ $standardSocketInstalled == "1" ]]; then

		timeout 10 modules/sdm120modbusSocket/main.sh || true
		socketkwh=$(</var/www/html/openWB/ramdisk/socketkwh)
		socketp=$(cat /var/www/html/openWB/ramdisk/socketp)
		socketa=$(cat /var/www/html/openWB/ramdisk/socketa)
		socketa=$(echo $socketa | sed 's/\..*$//')
		socketv=$(cat /var/www/html/openWB/ramdisk/socketv)
		if ! [[ $socketa =~ $re ]] ; then
			socketa="0"
		fi
	fi

	#Wattbezug
	if [[ $wattbezugmodul != "none" ]]; then
		wattbezug=$(modules/$wattbezugmodul/main.sh || true)
		if ! [[ $wattbezug =~ $re ]] ; then
			wattbezug="0"
		fi
		wattbezugint=$(printf "%.0f\n" $wattbezug)
		#evu glaettung
		if (( evuglaettungakt == 1 )); then
			if (( evuglaettung > 20 )); then
				ganzahl=$(( evuglaettung / 10 ))
				for ((i=ganzahl;i>=1;i--)); do
					i2=$(( i + 1 ))
					cp ramdisk/glaettung$i ramdisk/glaettung$i2
				done
				echo $wattbezug > ramdisk/glaettung1
				for ((i=1;i<=ganzahl;i++)); do
					glaettung=$(<ramdisk/glaettung$i)
					glaettungw=$(( glaettung + glaettungw))
				done
				glaettungfinal=$((glaettungw / ganzahl))
				echo $glaettungfinal > ramdisk/glattwattbezug
				wattbezug=$glaettungfinal
			fi
		fi
		#uberschuss zur berechnung
		uberschuss=$(printf "%.0f\n" $((-wattbezug)))
		if [[ $speichervorhanden == "1" ]]; then
			if [[ $speicherpveinbeziehen == "1" ]]; then
				if (( speicherleistung > 0 )); then
					if (( speichersoc > speichersocnurpv )); then
						speicherww=$((speicherleistung + speicherwattnurpv))
						uberschuss=$((uberschuss + speicherww))
					else
						speicherww=$((speicherleistung - speichermaxwatt))
						uberschuss=$((uberschuss + speicherww))
					fi
				fi
			fi
		fi
		evua1=$(cat /var/www/html/openWB/ramdisk/bezuga1)
		evua2=$(cat /var/www/html/openWB/ramdisk/bezuga2)
		evua3=$(cat /var/www/html/openWB/ramdisk/bezuga3)
		evua1=$(echo $evua1 | sed 's/\..*$//')
		evua2=$(echo $evua2 | sed 's/\..*$//')
		evua3=$(echo $evua3 | sed 's/\..*$//')
		[[ $evua1 =~ $re ]] || evua1="0"
		[[ $evua2 =~ $re ]] || evua2="0"
		[[ $evua3 =~ $re ]] || evua3="0"
		evuas=($evua1 $evua2 $evua3)
		maxevu=${evuas[0]}
		lowevu=${evuas[0]}
		for v in "${evuas[@]}"; do
			if (( v < lowevu )); then lowevu=$v; fi;
			if (( v > maxevu )); then maxevu=$v; fi;
		done
		schieflast=$(( maxevu - lowevu ))
		echo $schieflast > /var/www/html/openWB/ramdisk/schieflast
	else
		uberschuss=$((-pvwatt - hausbezugnone - ladeleistung))
		echo $((-uberschuss)) > /var/www/html/openWB/ramdisk/wattbezug
		wattbezugint=$((-uberschuss))
		wattbezug=$wattbezugint
	fi

	# Abschaltbare Smartdevices zum Ueberschuss rechnen
	echo $uberschuss > /var/www/html/openWB/ramdisk/ueberschuss_org
	wattabs=$(cat /var/www/html/openWB/ramdisk/devicetotal_watt)
	uberschuss=$((uberschuss + wattabs))
	echo $uberschuss > /var/www/html/openWB/ramdisk/ueberschuss_mitsmart

	#Soc ermitteln
	if [[ $socmodul != "none" ]]; then
		socvorhanden=1
		echo 1 > /var/www/html/openWB/ramdisk/socvorhanden
		if (( stopsocnotpluggedlp1 == 1 )); then
			soctimer=$(</var/www/html/openWB/ramdisk/soctimer)
			# if (( plugstat == 1 )); then
			if [ $plugstat -eq 1 -o $soctimer -eq 20005 ]; then # force soc update button sends 20005
				modules/$socmodul/main.sh &
				soc=$(</var/www/html/openWB/ramdisk/soc)
				tmpsoc=$(</var/www/html/openWB/ramdisk/tmpsoc)
				if ! [[ $soc =~ $re ]] ; then
					soc=$tmpsoc
				else
					echo $soc > /var/www/html/openWB/ramdisk/tmpsoc
				fi
			else
				echo 600 > /var/www/html/openWB/ramdisk/soctimer
				soc=$(</var/www/html/openWB/ramdisk/soc)
			fi
		else
			modules/$socmodul/main.sh &
			soc=$(</var/www/html/openWB/ramdisk/soc)
			tmpsoc=$(</var/www/html/openWB/ramdisk/tmpsoc)
			if ! [[ $soc =~ $re ]] ; then
				soc=$tmpsoc
			else
				echo $soc > /var/www/html/openWB/ramdisk/tmpsoc
			fi
		fi
	else
		socvorhanden=0
		echo 0 > /var/www/html/openWB/ramdisk/socvorhanden
		soc=0
	fi

	if [ -s "ramdisk/device1_watt" ]; then shd1_w=$(<ramdisk/device1_watt); else shd1_w=0; fi
	if [ -s "ramdisk/device2_watt" ]; then shd2_w=$(<ramdisk/device2_watt); else shd2_w=0; fi
	if [ -s "ramdisk/device3_watt" ]; then shd3_w=$(<ramdisk/device3_watt); else shd3_w=0; fi
	if [ -s "ramdisk/device4_watt" ]; then shd4_w=$(<ramdisk/device4_watt); else shd4_w=0; fi
	if [ -s "ramdisk/device5_watt" ]; then shd5_w=$(<ramdisk/device5_watt); else shd5_w=0; fi
	if [ -s "ramdisk/device6_watt" ]; then shd6_w=$(<ramdisk/device6_watt); else shd6_w=0; fi
	if [ -s "ramdisk/device7_watt" ]; then shd7_w=$(<ramdisk/device7_watt); else shd7_w=0; fi
	if [ -s "ramdisk/device8_watt" ]; then shd8_w=$(<ramdisk/device8_watt); else shd8_w=0; fi
	if [ -s "ramdisk/device9_watt" ]; then shd9_w=$(<ramdisk/device9_watt); else shd9_w=0; fi
	if [ -s "ramdisk/devicetotal_watt_hausmin" ]; then shdall_w=$(<ramdisk/devicetotal_watt_hausmin); else shdall_w=0; fi
	if [ -s "ramdisk/device1_temp0" ]; then shd1_t0=$(<ramdisk/device1_temp0); else shd1_t0=0; fi
	if [ -s "ramdisk/device1_temp1" ]; then shd1_t1=$(<ramdisk/device1_temp1); else shd1_t1=0; fi
	if [ -s "ramdisk/device1_temp2" ]; then shd1_t2=$(<ramdisk/device1_temp2); else shd1_t2=0; fi
	if [ -s "ramdisk/verbraucher1_watt" ]; then verb1_w=$(<ramdisk/verbraucher1_watt); else verb1_w=0; fi
	verb1_w=$(printf "%.0f\n" $verb1_w)
	if [ -s "ramdisk/verbraucher2_watt" ]; then verb2_w=$(<ramdisk/verbraucher2_watt); else verb2_w=0; fi
	verb2_w=$(printf "%.0f\n" $verb2_w)
	if [ -s "ramdisk/verbraucher3_watt" ]; then verb3_w=$(<ramdisk/verbraucher3_watt); else verb3_w=0; fi
	verb3_w=$(printf "%.0f\n" $verb3_w)

	#hausverbrauch=$((wattbezugint - pvwatt - ladeleistung - speicherleistung - shd1_w - shd2_w - shd3_w - shd4_w - shd5_w - shd6_w - shd7_w - shd8_w - shd9_w - verb1_w - verb2_w - verb3_w))
	hausverbrauch=$((wattbezugint - pvwatt - ladeleistung - speicherleistung - shdall_w - verb1_w - verb2_w - verb3_w))
	if (( hausverbrauch < 0 )); then
		if [ -f /var/www/html/openWB/ramdisk/hausverbrauch.invalid ]; then
			hausverbrauchinvalid=$(</var/www/html/openWB/ramdisk/hausverbrauch.invalid)
			let hausverbrauchinvalid+=1
		else
			hausverbrauchinvalid=1
		fi
		echo "$hausverbrauchinvalid" > /var/www/html/openWB/ramdisk/hausverbrauch.invalid
		if (( hausverbrauchinvalid < 3 )); then
			hausverbrauch=$(</var/www/html/openWB/ramdisk/hausverbrauch)
		else
			hausverbrauch=0
		fi
	else
		echo "0" > /var/www/html/openWB/ramdisk/hausverbrauch.invalid
	fi
	echo $hausverbrauch > /var/www/html/openWB/ramdisk/hausverbrauch
	fronius_sm_bezug_meterlocation=$(</var/www/html/openWB/ramdisk/fronius_sm_bezug_meterlocation)
	usesimbezug=0
	if [[ $wattbezugmodul == "bezug_e3dc" ]] || [[ $wattbezugmodul == "bezug_huawei" ]] || [[ $wattbezugmodul == "bezug_carlogavazzilan" ]]|| [[ $wattbezugmodul == "bezug_siemens" ]] || [[ $wattbezugmodul == "bezug_solarwatt" ]]|| [[ $wattbezugmodul == "bezug_rct" ]]|| [[ $wattbezugmodul == "bezug_sungrow" ]] || [[ $wattbezugmodul == "bezug_powerdog" ]] || [[ $wattbezugmodul == "bezug_varta" ]] || [[ $wattbezugmodul == "bezug_lgessv1" ]] || [[ $wattbezugmodul == "bezug_kostalpiko" ]] || [[ $wattbezugmodul == "bezug_kostalplenticoreem300haus" ]] || [[ $wattbezugmodul == "bezug_sbs25" ]] || [[ $wattbezugmodul == "bezug_solarlog" ]] || [[ $wattbezugmodul == "bezug_sonneneco" ]] || [[ $fronius_sm_bezug_meterlocation == "1" ]]; then
		usesimbezug=1
	fi
	if [[ $usesimbezug == "1" ]]; then
		ra='^-?[0-9]+$'
		watt2=$(</var/www/html/openWB/ramdisk/wattbezug)
		if [[ -e /var/www/html/openWB/ramdisk/bezugwatt0pos ]]; then
			importtemp=$(</var/www/html/openWB/ramdisk/bezugwatt0pos)
		else
			importtemp=$(timeout 4 mosquitto_sub -t openWB/evu/WHImported_temp)
			if ! [[ $importtemp =~ $ra ]] ; then
				importtemp="0"
			fi
			openwbDebugLog "MAIN" 0 "loadvars read openWB/evu/WHImported_temp from mosquito $importtemp"
			echo $importtemp > /var/www/html/openWB/ramdisk/bezugwatt0pos
		fi
		if [[ -e /var/www/html/openWB/ramdisk/bezugwatt0neg ]]; then
			exporttemp=$(</var/www/html/openWB/ramdisk/bezugwatt0neg)
		else
			exporttemp=$(timeout 4 mosquitto_sub -t openWB/evu/WHExport_temp)
			if ! [[ $exporttemp =~ $ra ]] ; then
				exporttemp="0"
			fi
			openwbDebugLog "MAIN" 0 "loadvars read openWB/evu/WHExport_temp from mosquito $exporttemp"
			echo $exporttemp > /var/www/html/openWB/ramdisk/bezugwatt0neg
		fi
		sudo python /var/www/html/openWB/runs/simcount.py $watt2 bezug bezugkwh einspeisungkwh
		importtemp1=$(</var/www/html/openWB/ramdisk/bezugwatt0pos)
		exporttemp1=$(</var/www/html/openWB/ramdisk/bezugwatt0neg)
		if [[ $importtemp !=  $importtemp1 ]]; then
			mosquitto_pub -t openWB/evu/WHImported_temp -r -m "$importtemp1"
		fi
		if [[ $exporttemp !=  $exporttemp1 ]]; then
			mosquitto_pub -t openWB/evu/WHExport_temp -r -m "$exporttemp1"
		fi
		# sim bezug end
	fi

	usesimpv=0
	if [[ $pvwattmodul == "none" ]] && [[ $speichermodul == "speicher_e3dc" ]]; then
		usesimpv=1
	fi
	if [[ $speichermodul == "speicher_kostalplenticore" ]] && [[ $pvwattmodul == "wr_plenticore" ]]; then
		usesimpv=1
	fi
	if [[ $speichermodul == "speicher_solaredge" ]] && [[ $pvwattmodul == "wr_solaredge" ]]; then
		usesimpv=1
	fi
	if [[ $pvwattmodul == "wr_fronius" ]] && [[ $speichermodul == "speicher_fronius" ]]; then
		usesimpv=1
	fi
	if [[ $pvwattmodul == "wr_fronius" ]] && [[ $wrfroniusisgen24 == "1" ]]; then
		usesimpv=1
	fi
	if [[ $pvwattmodul == "wr_kostalpiko" ]] || [[ $pvwattmodul == "wr_siemens" ]] || [[ $pvwattmodul == "wr_rct" ]]|| [[ $pvwattmodul == "wr_solarwatt" ]] || [[ $pvwattmodul == "wr_shelly" ]] || [[ $pvwattmodul == "wr_sungrow" ]] || [[ $pvwattmodul == "wr_huawei" ]] || [[ $pvwattmodul == "wr_powerdog" ]] || [[ $pvwattmodul == "wr_lgessv1" ]]|| [[ $pvwattmodul == "wr_kostalpikovar2" ]] || [[ $pvwattmodul == "wr_alphaess" ]]; then
		usesimpv=1
	fi
	if [[ $usesimpv == "1" ]]; then
		ra='^-?[0-9]+$'
		watt3=$(</var/www/html/openWB/ramdisk/pvwatt)
		if [[ -e /var/www/html/openWB/ramdisk/pvwatt0pos ]]; then
			importtemp=$(</var/www/html/openWB/ramdisk/pvwatt0pos)
		else
			importtemp=$(timeout 4 mosquitto_sub -t openWB/pv/WHImported_temp)
			if ! [[ $importtemp =~ $ra ]] ; then
				importtemp="0"
			fi
			openwbDebugLog "MAIN" 0 "loadvars read openWB/pv/WHImported_temp from mosquito $importtemp"
			echo $importtemp > /var/www/html/openWB/ramdisk/pvwatt0pos
		fi
		if [[ -e /var/www/html/openWB/ramdisk/pvwatt0neg ]]; then
			exporttemp=$(</var/www/html/openWB/ramdisk/pvwatt0neg)
		else
			exporttemp=$(timeout 4 mosquitto_sub -t openWB/pv/WHExport_temp)
			if ! [[ $exporttemp =~ $ra ]] ; then
				exporttemp="0"
			fi
			openwbDebugLog "MAIN" 0 "loadvars read openWB/pv/WHExport_temp from mosquito $exporttemp"
			echo $exporttemp > /var/www/html/openWB/ramdisk/pvwatt0neg
		fi
		sudo python /var/www/html/openWB/runs/simcount.py $watt3 pv pvposkwh pvkwh
		importtemp1=$(</var/www/html/openWB/ramdisk/pvwatt0pos)
		exporttemp1=$(</var/www/html/openWB/ramdisk/pvwatt0neg)
		if [[ $importtemp !=  $importtemp1 ]]; then
			mosquitto_pub -t openWB/pv/WHImported_temp -r -m "$importtemp1"
		fi
		if [[ $exporttemp !=  $exporttemp1 ]]; then
			mosquitto_pub -t openWB/pv/WHExport_temp -r -m "$exporttemp1"
		fi
		# sim pv end
	fi

	if [[ $speichermodul == "speicher_e3dc" ]] || [[ $speichermodul == "speicher_huawei" ]] || [[ $speichermodul == "speicher_tesvoltsma" ]] || [[ $speichermodul == "speicher_solarwatt" ]] || [[ $speichermodul == "speicher_rct" ]]|| [[ $speichermodul == "speicher_sungrow" ]]|| [[ $speichermodul == "speicher_alphaess" ]] || [[ $speichermodul == "speicher_siemens" ]]|| [[ $speichermodul == "speicher_lgessv1" ]] || [[ $speichermodul == "speicher_bydhv" ]] || [[ $speichermodul == "speicher_kostalplenticore" ]] || [[ $speichermodul == "speicher_powerwall" ]] || [[ $speichermodul == "speicher_sbs25" ]] || [[ $speichermodul == "speicher_solaredge" ]] || [[ $speichermodul == "speicher_sonneneco" ]] || [[ $speichermodul == "speicher_varta" ]] || [[ $speichermodul == "speicher_saxpower" ]] || [[ $speichermodul == "speicher_victron" ]] || [[ $speichermodul == "speicher_fronius" ]] ; then
		ra='^-?[0-9]+$'
		watt2=$(</var/www/html/openWB/ramdisk/speicherleistung)
		if [[ -e /var/www/html/openWB/ramdisk/speicherwatt0pos ]]; then
			importtemp=$(</var/www/html/openWB/ramdisk/speicherwatt0pos)
		else
			importtemp=$(timeout 4 mosquitto_sub -t openWB/housebattery/WHImported_temp)
			if ! [[ $importtemp =~ $ra ]] ; then
				importtemp="0"
			fi
			openwbDebugLog "MAIN" 0 "loadvars read openWB/housebattery/WHImported_temp from mosquito $importtemp"
			echo $importtemp > /var/www/html/openWB/ramdisk/speicherwatt0pos
		fi
		if [[ -e /var/www/html/openWB/ramdisk/speicherwatt0neg ]]; then
			exporttemp=$(</var/www/html/openWB/ramdisk/speicherwatt0neg)
		else
			exporttemp=$(timeout 4 mosquitto_sub -t openWB/housebattery/WHExport_temp)
			if ! [[ $exporttemp =~ $ra ]] ; then
				exporttemp="0"
			fi
			openwbDebugLog "MAIN" 0 "loadvars read openWB/housebattery/WHExport_temp from mosquito $exporttemp"
			echo $exporttemp > /var/www/html/openWB/ramdisk/speicherwatt0neg
		fi
		sudo python /var/www/html/openWB/runs/simcount.py $watt2 speicher speicherikwh speicherekwh
		importtemp1=$(</var/www/html/openWB/ramdisk/speicherwatt0pos)
		exporttemp1=$(</var/www/html/openWB/ramdisk/speicherwatt0neg)
		if [[ $importtemp !=  $importtemp1 ]]; then
			mosquitto_pub -t openWB/housebattery/WHImported_temp -r -m "$importtemp1"
		fi
		if [[ $exporttemp !=  $exporttemp1 ]]; then
			mosquitto_pub -t openWB/housebattery/WHExport_temp -r -m "$exporttemp1"
		fi
		# sim speicher end
	fi

	if [[ $verbraucher1_aktiv == "1" ]] && [[ $verbraucher1_typ == "shelly" ]]; then
		ra='^-?[0-9]+$'
		watt3=$(</var/www/html/openWB/ramdisk/verbraucher1_watt)
		if [[ -e /var/www/html/openWB/ramdisk/verbraucher1watt0pos ]]; then
			importtemp=$(</var/www/html/openWB/ramdisk/verbraucher1watt0pos)
		else
			importtemp=$(timeout 4 mosquitto_sub -t openWB/Verbraucher/1/WH1Imported_temp)
			if ! [[ $importtemp =~ $ra ]] ; then
				importtemp="0"
			fi
			openwbDebugLog "MAIN" 0 "loadvars read openWB/Verbraucher/1/WHImported_temp from mosquito $importtemp"
			echo $importtemp > /var/www/html/openWB/ramdisk/verbraucher1watt0pos
		fi
		if [[ -e /var/www/html/openWB/ramdisk/verbraucher1watt0neg ]]; then
			exporttemp=$(</var/www/html/openWB/ramdisk/verbraucher1watt0neg)
		else
			exporttemp=$(timeout 4 mosquitto_sub -t openWB/verbraucher/1/WH1Export_temp)
			if ! [[ $exporttemp =~ $ra ]] ; then
				exporttemp="0"
			fi
			openwbDebugLog "MAIN" 0 "loadvars read openWB/verbraucher/1/WHExport_temp from mosquito $exporttemp"
			echo $exporttemp > /var/www/html/openWB/ramdisk/verbraucher1watt0neg
		fi
		sudo python /var/www/html/openWB/runs/simcount.py $watt3 verbraucher1 verbraucher1_wh verbraucher1_whe
		importtemp1=$(</var/www/html/openWB/ramdisk/verbraucher1watt0pos)
		exporttemp1=$(</var/www/html/openWB/ramdisk/verbraucher1watt0neg)
		if [[ $importtemp !=  $importtemp1 ]]; then
			mosquitto_pub -t openWB/verbraucher/1/WHImported_temp -r -m "$importtemp1"
		fi
		if [[ $exporttemp !=  $exporttemp1 ]]; then
			mosquitto_pub -t openWB/verbraucher/1/WHExport_temp -r -m "$exporttemp1"
		fi
		# sim verbraucher end
	fi

	#Uhrzeit
	date=$(date)
	H=$(date +%H)
	if [[ $debug == "1" ]]; then
		echo "$(tail -1500 /var/www/html/openWB/ramdisk/openWB.log)" > /var/www/html/openWB/ramdisk/openWB.log
	fi
	if [[ $speichermodul != "none" ]] ; then
		openwbDebugLog "MAIN" 1 "speicherleistung $speicherleistung speichersoc $speichersoc"
	fi
	if (( $etprovideraktiv == 1 )) ; then
		openwbDebugLog "MAIN" 1 "etproviderprice $etproviderprice etprovidermaxprice $etprovidermaxprice"
	fi
	openwbDebugLog "MAIN" 1 "pv1watt $pv1watt pv2watt $pv2watt pvwatt $pvwatt ladeleistung $ladeleistung llalt $llalt nachtladen $nachtladen nachtladen $nachtladens1 minimalA $minimalstromstaerke maximalA $maximalstromstaerke"
	openwbDebugLog "MAIN" 1 "$(echo -e lla1 "$lla1"'\t'llv1 "$llv1"'\t'llas11 "$llas11" llas21 "$llas21" mindestuberschuss "$mindestuberschuss" abschaltuberschuss "$abschaltuberschuss" lademodus "$lademodus")"
	openwbDebugLog "MAIN" 1 "$(echo -e lla2 "$lla2"'\t'llv2 "$llv2"'\t'llas12 "$llas12" llas22 "$llas22" sofortll "$sofortll" hausverbrauch "$hausverbrauch"  wattbezug "$wattbezug" uberschuss "$uberschuss")"
	openwbDebugLog "MAIN" 1 "$(echo -e lla3 "$lla3"'\t'llv3 "$llv3"'\t'llas13 "$llas13" llas23 "$llas23" soclp1 $soc soclp2 $soc1)"
	openwbDebugLog "MAIN" 1 "EVU 1:${evuv1}V/${evua1}A 2: ${evuv2}V/${evua2}A 3: ${evuv3}V/${evua3}A"
	openwbDebugLog "MAIN" 1 "$(echo -e lp1enabled "$lp1enabled"'\t'lp2enabled "$lp2enabled"'\t'lp3enabled "$lp3enabled")"
	openwbDebugLog "MAIN" 1 "$(echo -e plugstatlp1 "$plugstat"'\t'plugstatlp2 "$plugstatlp2"'\t'plugstatlp3 "$plugstatlp3")"
	openwbDebugLog "MAIN" 1 "$(echo -e chargestatlp1 "$chargestat"'\t'chargestatlp2 "$chargestatlp2"'\t'chargestatlp3 "$chargestatlp3")"
	if [[ $standardSocketInstalled == "1" ]]; then
		openwbDebugLog "MAIN" 1 "socketa $socketa socketp $socketp socketkwh $socketkwh socketv $socketv"
	fi

	tempPubList=""

	if [[ "$opvwatt" != "$pvwatt" ]]; then
		tempPubList="${tempPubList}\nopenWB/pv/W=${pvwatt}"
		echo $pvwatt > ramdisk/mqttpvwatt
	fi
	if [[ "$owattbezug" != "$wattbezug" ]]; then
		tempPubList="${tempPubList}\nopenWB/evu/W=${wattbezug}"
		echo $wattbezug > ramdisk/mqttwattbezug
	fi
	if [[ "$ollaktuell" != "$ladeleistunglp1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/W=${ladeleistunglp1}"
		echo $ladeleistunglp1 > ramdisk/mqttladeleistunglp1
	fi
	if [[ "$oladestatus" != "$ladestatus" ]]; then
		tempPubList="${tempPubList}\nopenWB/ChargeStatus=${ladelestatus}"
		echo $ladestatus > ramdisk/mqttlastladestatus
	fi
	# TODO: wann wird der Lademodus geändert?
	if [[ "$olademodus" != "$lademodus" ]]; then
		tempPubList="${tempPubList}\nopenWB/global/ChargeMode=${lademodus}"
		echo $lademodus > ramdisk/mqttlastlademodus
	fi
	if [[ "$ohausverbrauch" != "$hausverbrauch" ]]; then
		tempPubList="${tempPubList}\nopenWB/global/WHouseConsumption=${hausverbrauch}"
		echo $hausverbrauch > ramdisk/mqtthausverbrauch
	fi
	if [[ "$ollaktuells1" != "$ladeleistungs1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/W=${ladeleistungs1}"
		echo $ladeleistungs1 > ramdisk/mqttladeleistungs1
	fi
	if [[ "$ollaktuells2" != "$ladeleistungs2" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/3/W=${ladeleistungs2}"
		echo $ladeleistungs2 > ramdisk/mqttladeleistungs2
	fi
	if [[ "$ollkombiniert" != "$ladeleistung" ]]; then
		tempPubList="${tempPubList}\nopenWB/global/WAllChargePoints=${ladeleistung}"
		echo $ladeleistung > ramdisk/mqttladeleistung
	fi
	if [[ "$ospeicherleistung" != "$speicherleistung" ]]; then
		tempPubList="${tempPubList}\nopenWB/housebattery/W=${speicherleistung}"
		echo $speicherleistung > ramdisk/mqttspeicherleistung
	fi
	if [[ "$ospeichersoc" != "$speichersoc" ]]; then
		tempPubList="${tempPubList}\nopenWB/housebattery/%Soc=${speichersoc}"
		echo $speichersoc > ramdisk/mqttspeichersoc
	fi
	if [[ "$osoc" != "$soc" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/%Soc=${soc}"
		echo $soc > ramdisk/mqttsoc
	fi
	if [[ "$osoc1" != "$soc1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/%Soc=${soc1}"
		echo $soc1 > ramdisk/mqttsoc1
	fi
	if [[ "$ostopchargeafterdisclp1" != "$stopchargeafterdisclp1" ]]; then
		tempPubList="${tempPubList}\nopenWB/config/get/lp/1/stopchargeafterdisc=${stopchargeafterdisclp1}"
		echo $stopchargeafterdisclp1 > ramdisk/mqttstopchargeafterdisclp1
	fi
	if [[ "$ostopchargeafterdisclp2" != "$stopchargeafterdisclp2" ]]; then
		tempPubList="${tempPubList}\nopenWB/config/get/lp/2/stopchargeafterdisc=${stopchargeafterdisclp2}"
		echo $stopchargeafterdisclp2 > ramdisk/mqttstopchargeafterdisclp2
	fi
	if [[ "$ostopchargeafterdisclp3" != "$stopchargeafterdisclp3" ]]; then
		tempPubList="${tempPubList}\nopenWB/config/get/lp/3/stopchargeafterdisc=${stopchargeafterdisclp3}"
		echo $stopchargeafterdisclp3 > ramdisk/mqttstopchargeafterdisclp3
	fi
	if [[ "$ostopchargeafterdisclp4" != "$stopchargeafterdisclp4" ]]; then
		tempPubList="${tempPubList}\nopenWB/config/get/lp/4/stopchargeafterdisc=${stopchargeafterdisclp4}"
		echo $stopchargeafterdisclp4 > ramdisk/mqttstopchargeafterdisclp4
	fi
	if [[ "$ostopchargeafterdisclp5" != "$stopchargeafterdisclp5" ]]; then
		tempPubList="${tempPubList}\nopenWB/config/get/lp/5/stopchargeafterdisc=${stopchargeafterdisclp5}"
		echo $stopchargeafterdisclp5 > ramdisk/mqttstopchargeafterdisclp5
	fi
	if [[ "$ostopchargeafterdisclp6" != "$stopchargeafterdisclp6" ]]; then
		tempPubList="${tempPubList}\nopenWB/config/get/lp/6/stopchargeafterdisc=${stopchargeafterdisclp6}"
		echo $stopchargeafterdisclp6 > ramdisk/mqttstopchargeafterdisclp6
	fi
	if [[ "$ostopchargeafterdisclp7" != "$stopchargeafterdisclp7" ]]; then
		tempPubList="${tempPubList}\nopenWB/config/get/lp/7/stopchargeafterdisc=${stopchargeafterdisclp7}"
		echo $stopchargeafterdisclp7 > ramdisk/mqttstopchargeafterdisclp7
	fi
	if [[ "$ostopchargeafterdisclp8" != "$stopchargeafterdisclp8" ]]; then
		tempPubList="${tempPubList}\nopenWB/config/get/lp/8/stopchargeafterdisc=${stopchargeafterdisclp8}"
		echo $stopchargeafterdisclp8 > ramdisk/mqttstopchargeafterdisclp8
	fi
	if [[ $rfidakt == "1" ]]; then
		rfid
	fi

	csvfile="/var/www/html/openWB/web/logging/data/daily/$(date +%Y%m%d).csv"
	first=$(head -n 1 "$csvfile")
	last=$(tail -n 1 "$csvfile")
	dailychargelp1=$(echo "$(echo "$first" | cut -d , -f 5) $(echo "$last" | cut -d , -f 5)" | awk '{printf "%0.2f", ($2 - $1)/1000}')
	dailychargelp2=$(echo "$(echo "$first" | cut -d , -f 6) $(echo "$last" | cut -d , -f 6)" | awk '{printf "%0.2f", ($2 - $1)/1000}')
	dailychargelp3=$(echo "$(echo "$first" | cut -d , -f 7) $(echo "$last" | cut -d , -f 7)" | awk '{printf "%0.2f", ($2 - $1)/1000}')

	restzeitlp1=$(<ramdisk/restzeitlp1)
	restzeitlp2=$(<ramdisk/restzeitlp2)
	restzeitlp3=$(<ramdisk/restzeitlp3)
	gelrlp1=$(<ramdisk/gelrlp1)
	gelrlp2=$(<ramdisk/gelrlp2)
	gelrlp3=$(<ramdisk/gelrlp3)

	lastregelungaktiv=$(<ramdisk/lastregelungaktiv)
	hook1aktiv=$(<ramdisk/hook1akt)
	hook2aktiv=$(<ramdisk/hook2akt)
	hook3aktiv=$(<ramdisk/hook3akt)
	if [[ "$odailychargelp1" != "$dailychargelp1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/kWhDailyCharged=${dailychargelp1}"
		echo $dailychargelp1 > ramdisk/mqttdailychargelp1
	fi
	if [[ "$odailychargelp2" != "$dailychargelp2" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/kWhDailyCharged=${dailychargelp2}"
		echo $dailychargelp2 > ramdisk/mqttdailychargelp2
	fi
	if [[ "$odailychargelp3" != "$dailychargelp3" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/3/kWhDailyCharged=${dailychargelp3}"
		echo $dailychargelp3 > ramdisk/mqttdailychargelp3
	fi
	if [[ "$orestzeitlp1" != "$restzeitlp1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/TimeRemaining=${restzeitlp1}"
		echo $restzeitlp1 > ramdisk/mqttrestzeitlp1
	fi
	if [[ "$orestzeitlp2" != "$restzeitlp2" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/TimeRemaining=${restzeitlp2}"
		echo $restzeitlp2 > ramdisk/mqttrestzeitlp2
	fi
	if [[ "$orestzeitlp3" != "$restzeitlp3" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/3/TimeRemaining=${restzeitlp3}"
		echo $restzeitlp3 > ramdisk/mqttrestzeitlp3
	fi
	if [[ "$ogelrlp1" != "$gelrlp1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/kmCharged=${gelrlp1}"
		echo $gelrlp1 > ramdisk/mqttgelrlp1
	fi
	if [[ "$ogelrlp2" != "$gelrlp2" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/kmCharged=${gelrlp2}"
		echo $gelrlp2 > ramdisk/mqttgelrlp2
	fi
	if [[ "$ogelrlp3" != "$gelrlp3" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/3/kmCharged=${gelrlp3}"
		echo $gelrlp3 > ramdisk/mqttgelrlp3
	fi
	ohook1_aktiv=$(<ramdisk/mqtthook1_aktiv)
	if [[ "$ohook1_aktiv" != "$hook1_aktiv" ]]; then
		tempPubList="${tempPubList}\nopenWB/hook/1/boolHookConfigured=${hook1_aktiv}"
		echo $ > ramdisk/mqtthook1_aktiv
	fi
	ohook2_aktiv=$(<ramdisk/mqtthook2_aktiv)
	if [[ "$ohook2_aktiv" != "$hook2_aktiv" ]]; then
		tempPubList="${tempPubList}\nopenWB/hook/2/boolHookConfigured=${hook2_aktiv}"
		echo $ > ramdisk/mqtthook2_aktiv
	fi
	ohook3_aktiv=$(<ramdisk/mqtthook3_aktiv)
	if [[ "$ohook3_aktiv" != "$hook3_aktiv" ]]; then
		tempPubList="${tempPubList}\nopenWB/hook/3/boolHookConfigured=${hook3_aktiv}"
		echo $ > ramdisk/mqtthook3_aktiv
	fi

	if (( ohook1aktiv != hook1aktiv )); then
		tempPubList="${tempPubList}\nopenWB/boolHook1Active=${hook1aktiv}"
		echo $hook1aktiv > ramdisk/mqtthook1aktiv
	fi
	if (( ohook2aktiv != hook2aktiv )); then
		tempPubList="${tempPubList}\nopenWB/boolHook2Active=${hook2aktiv}"
		echo $hook2aktiv > ramdisk/mqtthook2aktiv
	fi
	if (( ohook3aktiv != hook3aktiv )); then
		tempPubList="${tempPubList}\nopenWB/boolHook3Active=${hook3aktiv}"
		echo $hook3aktiv > ramdisk/mqtthook3aktiv
	fi
	oversion=$(<ramdisk/mqttversion)
	if [[ $oversion != $version ]]; then
		tempPubList="${tempPubList}\nopenWB/system/Version=${version}"
		echo -n "$version" > ramdisk/mqttversion
	fi

	ocp1config=$(<ramdisk/mqttCp1Configured)
	if [[ "$ocp1config" != "1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/boolChargePointConfigured=1"
		echo 1 > ramdisk/mqttCp1Configured
	fi

	olastmanagement=$(<ramdisk/mqttlastmanagement)
	if [[ "$olastmanagement" != "$lastmanagement" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/boolChargePointConfigured=${lastmanagement}"
		echo $lastmanagement > ramdisk/mqttlastmanagement
	fi
	osoc1vorhanden=$(<ramdisk/mqttsoc1vorhanden)
	if [[ "$osoc1vorhanden" != "$soc1vorhanden" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/boolSocConfigured=${soc1vorhanden}"
		echo $soc1vorhanden > ramdisk/mqttsoc1vorhanden
	fi
	osocvorhanden=$(<ramdisk/mqttsocvorhanden)
	if [[ "$osocvorhanden" != "$socvorhanden" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/boolSocConfigured=${socvorhanden}"
		echo $socvorhanden > ramdisk/mqttsocvorhanden
	fi

	olastmanagements2=$(<ramdisk/mqttlastmanagements2)
	if [[ "$olastmanagements2" != "$lastmanagements2" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/3/boolChargePointConfigured=${lastmanagements2}"
		echo $lastmanagements2 > ramdisk/mqttlastmanagements2
	fi
	olastmanagementlp4=$(<ramdisk/mqttlastmanagementlp4)
	if [[ "$olastmanagementlp4" != "$lastmanagementlp4" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/4/boolChargePointConfigured=${lastmanagementlp4}"
		echo $lastmanagementlp4 > ramdisk/mqttlastmanagementlp4
	fi
	olastmanagementlp5=$(<ramdisk/mqttlastmanagementlp5)
	if [[ "$olastmanagementlp5" != "$lastmanagementlp5" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/5/boolChargePointConfigured=${lastmanagementlp5}"
		echo $lastmanagementlp5 > ramdisk/mqttlastmanagementlp5
	fi
	olastmanagementlp6=$(<ramdisk/mqttlastmanagementlp6)
	if [[ "$olastmanagementlp6" != "$lastmanagementlp6" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/6/boolChargePointConfigured=${lastmanagementlp6}"
		echo $lastmanagementlp6 > ramdisk/mqttlastmanagementlp6
	fi
	olastmanagementlp7=$(<ramdisk/mqttlastmanagementlp7)
	if [[ "$olastmanagementlp7" != "$lastmanagementlp7" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/7/boolChargePointConfigured=${lastmanagementlp7}"
		echo $lastmanagementlp7 > ramdisk/mqttlastmanagementlp7
	fi
	olastmanagementlp8=$(<ramdisk/mqttlastmanagementlp8)
	if [[ "$olastmanagementlp8" != "$lastmanagementlp8" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/8/boolChargePointConfigured=${lastmanagementlp8}"
		echo $lastmanagementlp8 > ramdisk/mqttlastmanagementlp8
	fi
	olademstat=$(<ramdisk/mqttlademstat)
	if [[ "$olademstat" != "$lademstat" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/boolDirectModeChargekWh=${lademstat}"
		echo $lademstat > ramdisk/mqttlademstat
	fi
	olademstats1=$(<ramdisk/mqttlademstats1)
	if [[ "$olademstats1" != "$lademstats1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/boolDirectModeChargekWh=${lademstats1}"
		echo $lademstats1 > ramdisk/mqttlademstats1
	fi
	olademstats2=$(<ramdisk/mqttlademstats2)
	if [[ "$olademstats2" != "$lademstats2" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/3/boolDirectModeChargekWh=${lademstats2}"
		echo $lademstats2 > ramdisk/mqttlademstats2
	fi
	olademstatlp4=$(<ramdisk/mqttlademstatlp4)
	if [[ "$olademstatlp4" != "$lademstatlp4" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/4/boolDirectModeChargekWh=${lademstatlp4}"
		echo $lademstatlp4 > ramdisk/mqttlademstatlp4
	fi
	olademstatlp5=$(<ramdisk/mqttlademstatlp5)
	if [[ "$olademstatlp5" != "$lademstatlp5" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/5/boolDirectModeChargekWh=${lademstatlp5}"
		echo $lademstatlp5 > ramdisk/mqttlademstatlp5
	fi
	olademstatlp6=$(<ramdisk/mqttlademstatlp6)
	if [[ "$olademstatlp6" != "$lademstatlp6" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/6/boolDirectModeChargekWh=${lademstatlp6}"
		echo $lademstatlp6 > ramdisk/mqttlademstatlp6
	fi
	olademstatlp7=$(<ramdisk/mqttlademstatlp7)
	if [[ "$olademstatlp7" != "$lademstatlp7" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/7/boolDirectModeChargekWh=${lademstatlp7}"
		echo $lademstatlp7 > ramdisk/mqttlademstatlp7
	fi
	olademstatlp8=$(<ramdisk/mqttlademstatlp8)
	if [[ "$olademstatlp8" != "$lademstatlp8" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/8/boolDirectModeChargekWh=${lademstatlp8}"
		echo $lademstatlp8 > ramdisk/mqttlademstatlp8
	fi

	osofortsocstatlp1=$(<ramdisk/mqttsofortsocstatlp1)
	if [[ "$osofortsocstatlp1" != "$sofortsocstatlp1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/boolDirectChargeModeSoc=${sofortsocstatlp1}"
		echo $sofortsocstatlp1 > ramdisk/mqttsofortsocstatlp1
	fi

	osofortsocstatlp2=$(<ramdisk/mqttsofortsocstatlp2)
	if [[ "$osofortsocstatlp2" != "$sofortsocstatlp2" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/boolDirectChargeModeSoc=${sofortsocstatlp2}"
		echo $sofortsocstatlp2 > ramdisk/mqttsofortsocstatlp2
	fi
	#osofortsocstatlp3=$(<ramdisk/mqttsofortsocstatlp3)
	#if (( osofortsocstatlp3 != sofortsocstatlp3 )); then
	#	tempPubList="${tempPubList}\nopenWB/boolsofortlademodussoclp3=${sofortsocstatlp3}"
	#	echo $sofortsocstatlp3 > ramdisk/mqttsofortsocstatlp3
	#fi
	#osofortsoclp3=$(<ramdisk/mqttsofortsoclp3)
	#if (( osofortsoclp3 != sofortsoclp3 )); then
	#	tempPubList="${tempPubList}\nopenWB/percentsofortlademodussoclp3=${sofortsoclp3}"
	#	echo $sofortsoclp3 > ramdisk/mqttsofortsoclp3
	#fi
	ospeichervorhanden=$(<ramdisk/mqttspeichervorhanden)
	if (( ospeichervorhanden != speichervorhanden )); then
		tempPubList="${tempPubList}\nopenWB/housebattery/boolHouseBatteryConfigured=${speichervorhanden}"
		echo $speichervorhanden > ramdisk/mqttspeichervorhanden
	fi
	opv1vorhanden=$(<ramdisk/mqttpv1vorhanden)
	if (( opv1vorhanden != pv1vorhanden )); then
		tempPubList="${tempPubList}\nopenWB/pv/1/boolPVConfigured=${pv1vorhanden}"
		echo $pv1vorhanden > ramdisk/mqttpv1vorhanden
	fi
	opv2vorhanden=$(<ramdisk/mqttpv2vorhanden)
	if (( opv2vorhanden != pv2vorhanden )); then
		tempPubList="${tempPubList}\nopenWB/pv/2/boolPVConfigured=${pv2vorhanden}"
		echo $pv2vorhanden > ramdisk/mqttpv2vorhanden
	fi
	olp1name=$(<ramdisk/mqttlp1name)
	if [[ "$olp1name" != "$lp1name" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/strChargePointName=${lp1name}"
		echo $lp1name > ramdisk/mqttlp1name
	fi
	olp2name=$(<ramdisk/mqttlp2name)
	if [[ "$olp2name" != "$lp2name" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/strChargePointName=${lp2name}"
		echo $lp2name > ramdisk/mqttlp2name
	fi
	olp3name=$(<ramdisk/mqttlp3name)
	if [[ "$olp3name" != "$lp3name" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/3/strChargePointName=${lp3name}"
		echo $lp3name > ramdisk/mqttlp3name
	fi
	olp4name=$(<ramdisk/mqttlp4name)
	if [[ "$olp4name" != "$lp4name" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/4/strChargePointName=${lp4name}"
		echo $lp4name > ramdisk/mqttlp4name
	fi
	olp5name=$(<ramdisk/mqttlp5name)
	if [[ "$olp5name" != "$lp5name" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/5/strChargePointName=${lp5name}"
		echo $lp5name > ramdisk/mqttlp5name
	fi
	olp6name=$(<ramdisk/mqttlp6name)
	if [[ "$olp6name" != "$lp6name" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/6/strChargePointName=${lp6name}"
		echo $lp6name > ramdisk/mqttlp6name
	fi
	olp7name=$(<ramdisk/mqttlp7name)
	if [[ "$olp7name" != "$lp7name" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/7/strChargePointName=${lp7name}"
		echo $lp7name > ramdisk/mqttlp7name
	fi
	olp8name=$(<ramdisk/mqttlp8name)
	if [[ "$olp8name" != "$lp8name" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/8/strChargePointName=${lp8name}"
		echo $lp8name > ramdisk/mqttlp8name
	fi
	ozielladenaktivlp1=$(<ramdisk/mqttzielladenaktivlp1)
	if [[ "$ozielladenaktivlp1" != "$zielladenaktivlp1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/boolFinishAtTimeChargeActive=${zielladenaktivlp1}"
		echo $zielladenaktivlp1 > ramdisk/mqttzielladenaktivlp1
	fi
	onachtladen=$(<ramdisk/mqttnachtladen)
	if [[ "$onachtladen" != "$nachtladen" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/boolChargeAtNight=${nachtladen}"
		echo $nachtladen > ramdisk/mqttnachtladen
	fi
	onachtladens1=$(<ramdisk/mqttnachtladens1)
	if [[ "$onachtladens1" != "$nachtladens1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/boolChargeAtNight=${nachtladens1}"
		echo $nachtladens1 > ramdisk/mqttnachtladens1
	fi
	onlakt_sofort=$(<ramdisk/mqttnlakt_sofort)
	if [[ "$onlakt_sofort" != "$nlakt_sofort" ]]; then
		tempPubList="${tempPubList}\nopenWB/boolChargeAtNight_direct=${nlakt_sofort}"
		echo $nlakt_sofort > ramdisk/mqttnlakt_sofort
	fi
	onlakt_nurpv=$(<ramdisk/mqttnlakt_nurpv)
	if [[ "$onlakt_nurpv" != "$nlakt_nurpv" ]]; then
		tempPubList="${tempPubList}\nopenWB/boolChargeAtNight_nurpv=${nlakt_nurpv}"
		echo $nlakt_nurpv > ramdisk/mqttnlakt_nurpv
	fi
	onlakt_minpv=$(<ramdisk/mqttnlakt_minpv)
	if [[ "$onlakt_minpv" != "$nlakt_minpv" ]]; then
		tempPubList="${tempPubList}\nopenWB/boolChargeAtNight_minpv=${nlakt_minpv}"
		echo $nlakt_minpv > ramdisk/mqttnlakt_minpv
	fi

	onlakt_standby=$(<ramdisk/mqttnlakt_standby)
	if [[ "$onlakt_standby" != "$nlakt_standby" ]]; then
		tempPubList="${tempPubList}\nopenWB/boolChargeAtNight_standby=${nlakt_standby}"
		echo $nlakt_standby > ramdisk/mqttnlakt_standby
	fi
	ohausverbrauchstat=$(<ramdisk/mqtthausverbrauchstat)
	if [[ "$ohausverbrauchstat" != "$hausverbrauchstat" ]]; then
		tempPubList="${tempPubList}\nopenWB/boolDisplayHouseConsumption=${hausverbrauchstat}"
		echo $hausverbrauchstat > ramdisk/mqtthausverbrauchstat
	fi
	oheutegeladen=$(<ramdisk/mqttheutegeladen)
	if [[ "$oheutegeladen" != "$heutegeladen" ]]; then
		tempPubList="${tempPubList}\nopenWB/boolDisplayDailyCharged=${heutegeladen}"
		echo $heutegeladen > ramdisk/mqttheutegeladen
	fi
	oevuglaettungakt=$(<ramdisk/mqttevuglaettungakt)
	if [[ "$oevuglaettungakt" != "$evuglaettungakt" ]]; then
		tempPubList="${tempPubList}\nopenWB/boolEvuSmoothedActive=${evuglaettungakt}"
		echo $evuglaettungakt > ramdisk/mqttevuglaettungakt
	fi
	onurpv70dynact=$(<ramdisk/mqttnurpv70dynact)
	if [[ "$onurpv70dynact" != "$nurpv70dynact" ]]; then
		tempPubList="${tempPubList}\nopenWB/pv/bool70PVDynActive=${nurpv70dynact}"
		tempPubList="${tempPubList}\nopenWB/config/get/pv/nurpv70dynact=${nurpv70dynact}"
		echo $nurpv70dynact > ramdisk/mqttnurpv70dynact
	fi
	onurpv70dynw=$(<ramdisk/mqttnurpv70dynw)
	if [[ "$onurpv70dynw" != "$nurpv70dynw" ]]; then
		tempPubList="${tempPubList}\nopenWB/pv/W70PVDyn=${nurpv70dynw}"
		tempPubList="${tempPubList}\nopenWB/config/get/pv/nurpv70dynw=${nurpv70dynw}"
		echo $nurpv70dynw > ramdisk/mqttnurpv70dynw
	fi

	overbraucher1_name=$(<ramdisk/mqttverbraucher1_name)
	if [[ "$overbraucher1_name" != "$verbraucher1_name" ]]; then
		tempPubList="${tempPubList}\nopenWB/Verbraucher/1/Name=${verbraucher1_name}"
		echo $verbraucher1_name > ramdisk/mqttverbraucher1_name
	fi
	overbraucher1_aktiv=$(<ramdisk/mqttverbraucher1_aktiv)
	if [[ "$overbraucher1_aktiv" != "$verbraucher1_aktiv" ]]; then
		tempPubList="${tempPubList}\nopenWB/Verbraucher/1/Configured=${verbraucher1_aktiv}"
		echo $verbraucher1_aktiv > ramdisk/mqttverbraucher1_aktiv
	fi
	overbraucher2_aktiv=$(<ramdisk/mqttverbraucher2_aktiv)
	if [[ "$overbraucher2_aktiv" != "$verbraucher2_aktiv" ]]; then
		tempPubList="${tempPubList}\nopenWB/Verbraucher/2/Configured=${verbraucher2_aktiv}"
		echo $verbraucher2_aktiv > ramdisk/mqttverbraucher2_aktiv
	fi

	overbraucher2_name=$(<ramdisk/mqttverbraucher2_name)
	if [[ "$overbraucher2_name" != "$verbraucher2_name" ]]; then
		tempPubList="${tempPubList}\nopenWB/Verbraucher/2/Name=${verbraucher2_name}"
		echo $verbraucher2_name > ramdisk/mqttverbraucher2_name
	fi

	ospeicherpveinbeziehen=$(<ramdisk/mqttspeicherpveinbeziehen)
	if [[ "$ospeicherpveinbeziehen" != "$speicherpveinbeziehen" ]]; then
		tempPubList="${tempPubList}\nopenWB/config/get/pv/priorityModeEVBattery=${speicherpveinbeziehen}"
		echo $speicherpveinbeziehen > ramdisk/mqttspeicherpveinbeziehen
	fi
	oetprovideraktiv=$(<ramdisk/mqttetprovideraktiv)
	if [[ "$oetprovideraktiv" != "$etprovideraktiv" ]]; then
		tempPubList="${tempPubList}\nopenWB/global/awattar/boolAwattarEnabled=${etprovideraktiv}"
		echo $etprovideraktiv > ramdisk/mqttetprovideraktiv
	fi
	oetprovider=$(<ramdisk/mqttetprovider)
	if [[ "$oetprovider" != "$etprovider" ]]; then
		tempPubList="${tempPubList}\nopenWB/global/ETProvider/modulePath=${etprovider}"
		echo $etprovider > ramdisk/mqttetprovider
	fi
	oetproviderprice=$(<ramdisk/mqttetproviderprice)
	etproviderprice=$(<ramdisk/etproviderprice)
	if [[ "$oetproviderprice" != "$etproviderprice" ]]; then
		tempPubList="${tempPubList}\nopenWB/global/awattar/ActualPriceForCharging=${etproviderprice}"
		echo $etproviderprice > ramdisk/mqttetproviderprice
	fi
	oetprovidermaxprice=$(<ramdisk/mqttetprovidermaxprice)
	etprovidermaxprice=$(<ramdisk/etprovidermaxprice)
	if [[ "$oetprovidermaxprice" != "$etprovidermaxprice" ]]; then
		tempPubList="${tempPubList}\nopenWB/global/awattar/MaxPriceForCharging=${etprovidermaxprice}"
		echo $etprovidermaxprice > ramdisk/mqttetprovidermaxprice
	fi
	odurchslp1=$(<ramdisk/mqttdurchslp1)
	if [[ "$odurchslp1" != "$durchslp1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/energyConsumptionPer100km=${durchslp1}"
		echo $durchslp1 > ramdisk/mqttdurchslp1
	fi
	odurchslp2=$(<ramdisk/mqttdurchslp2)
	if [[ "$odurchslp2" != "$durchslp2" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/energyConsumptionPer100km=${durchslp2}"
		echo $durchslp2 > ramdisk/mqttdurchslp2
	fi
	odurchslp3=$(<ramdisk/mqttdurchslp3)
	if [[ "$odurchslp3" != "$durchslp3" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/3/energyConsumptionPer100km=${durchslp3}"
		echo $durchslp3 > ramdisk/mqttdurchslp3
	fi
	# publish last RFID scans as CSV with timestamp
	timestamp="$(date +%s)"

	orfidlp1=$(<ramdisk/mqttrfidlp1)
	arfidlp1=$(<ramdisk/rfidlp1)
	if [[ "$orfidlp1" != "$arfidlp1" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/1/lastRfId=${arfidlp1}"
		echo $arfidlp1 > ramdisk/mqttrfidlp1
	fi

	orfidlp2=$(<ramdisk/mqttrfidlp2)
	arfidlp2=$(<ramdisk/rfidlp2)
	if [[ "$orfidlp2" != "$arfidlp2" ]]; then
		tempPubList="${tempPubList}\nopenWB/lp/2/lastRfId=${arfidlp2}"
		echo $arfidlp2 > ramdisk/mqttrfidlp2
	fi

	orfidlast=$(<ramdisk/mqttrfidlasttag)
	arfidlast=$(<ramdisk/rfidlasttag)
	if [[ "$orfidlast" != "$arfidlast" ]]; then
		tempPubList="${tempPubList}\nopenWB/system/lastRfId=${arfidlast}"
		echo $arfidlast > ramdisk/mqttrfidlasttag
	fi

	ouiplast=$(<ramdisk/mqttupdateinprogress)
	auiplast=$(<ramdisk/updateinprogress)
	if [[ "$ouiplast" != "$auiplast" ]]; then
		tempPubList="${tempPubList}\nopenWB/system/updateInProgress=${auiplast}"
		echo $auiplast > ramdisk/mqttupdateinprogress
	fi

	arandomSleep=$(<ramdisk/randomSleepValue)
	orandomSleepValue=$(<ramdisk/mqttRandomSleepValue)
	if [[ "$orandomSleepValue" != "$arandomSleep" ]]; then
		tempPubList="${tempPubList}\nopenWB/system/randomSleep=${arandomSleep}"
		echo $arandomSleep > ramdisk/mqttRandomSleepValue
	fi

	declare -A mqttconfvar
	mqttconfvar["config/get/pv/minFeedinPowerBeforeStart"]=mindestuberschuss
	mqttconfvar["config/get/pv/maxPowerConsumptionBeforeStop"]=abschaltuberschuss
	mqttconfvar["config/get/pv/stopDelay"]=abschaltverzoegerung
	mqttconfvar["config/get/pv/startDelay"]=einschaltverzoegerung
	mqttconfvar["config/get/pv/minCurrentMinPv"]=minimalampv
	mqttconfvar["config/get/pv/lp/1/minCurrent"]=minimalapv
	mqttconfvar["config/get/pv/lp/2/minCurrent"]=minimalalp2pv
	mqttconfvar["config/get/pv/lp/1/minSocAlwaysToChargeTo"]=minnurpvsoclp1
	mqttconfvar["config/get/pv/lp/1/maxSocToChargeTo"]=maxnurpvsoclp1
	mqttconfvar["config/get/pv/lp/1/minSocAlwaysToChargeToCurrent"]=minnurpvsocll
	mqttconfvar["config/get/pv/chargeSubmode"]=pvbezugeinspeisung
	mqttconfvar["config/get/pv/regulationPoint"]=offsetpv
	mqttconfvar["config/get/pv/boolShowPriorityIconInTheme"]=speicherpvui
	mqttconfvar["config/get/pv/minBatteryChargePowerAtEvPriority"]=speichermaxwatt
	mqttconfvar["config/get/pv/minBatteryDischargeSocAtBattPriority"]=speichersocnurpv
	mqttconfvar["config/get/pv/batteryDischargePowerAtBattPriority"]=speicherwattnurpv
	mqttconfvar["config/get/pv/socStartChargeAtMinPv"]=speichersocminpv
	mqttconfvar["config/get/pv/socStopChargeAtMinPv"]=speichersochystminpv
	mqttconfvar["config/get/pv/boolAdaptiveCharging"]=adaptpv
	mqttconfvar["config/get/pv/adaptiveChargingFactor"]=adaptfaktor
	mqttconfvar["config/get/pv/nurpv70dynact"]=nurpv70dynact
	mqttconfvar["config/get/pv/nurpv70dynw"]=nurpv70dynw
	mqttconfvar["config/get/global/maxEVSECurrentAllowed"]=maximalstromstaerke
	mqttconfvar["config/get/global/minEVSECurrentAllowed"]=minimalstromstaerke
	mqttconfvar["config/get/global/dataProtectionAcknoledged"]=datenschutzack
	mqttconfvar["config/get/u1p3p/sofortPhases"]=u1p3psofort
	mqttconfvar["config/get/u1p3p/standbyPhases"]=u1p3pstandby
	mqttconfvar["config/get/u1p3p/nurpvPhases"]=u1p3pnurpv
	mqttconfvar["config/get/u1p3p/minundpvPhases"]=u1p3pminundpv
	mqttconfvar["config/get/u1p3p/nachtPhases"]=u1p3pnl
	mqttconfvar["config/get/u1p3p/isConfigured"]=u1p3paktiv
	mqttconfvar["config/get/sofort/lp/1/energyToCharge"]=lademkwh
	mqttconfvar["config/get/sofort/lp/2/energyToCharge"]=lademkwhs1
	mqttconfvar["config/get/sofort/lp/3/energyToCharge"]=lademkwhs2
	mqttconfvar["config/get/sofort/lp/4/energyToCharge"]=lademkwhlp4
	mqttconfvar["config/get/sofort/lp/5/energyToCharge"]=lademkwhlp5
	mqttconfvar["config/get/sofort/lp/6/energyToCharge"]=lademkwhlp6
	mqttconfvar["config/get/sofort/lp/7/energyToCharge"]=lademkwhlp7
	mqttconfvar["config/get/sofort/lp/8/energyToCharge"]=lademkwhlp8
	mqttconfvar["config/get/sofort/lp/1/socToChargeTo"]=sofortsoclp1
	mqttconfvar["config/get/sofort/lp/2/socToChargeTo"]=sofortsoclp2
	mqttconfvar["config/get/sofort/lp/1/chargeLimitation"]=msmoduslp1
	mqttconfvar["config/get/sofort/lp/2/chargeLimitation"]=msmoduslp2
	mqttconfvar["config/get/sofort/lp/3/chargeLimitation"]=msmoduslp3
	mqttconfvar["config/get/sofort/lp/4/chargeLimitation"]=msmoduslp4
	mqttconfvar["config/get/sofort/lp/5/chargeLimitation"]=msmoduslp5
	mqttconfvar["config/get/sofort/lp/6/chargeLimitation"]=msmoduslp6
	mqttconfvar["config/get/sofort/lp/7/chargeLimitation"]=msmoduslp7
	mqttconfvar["config/get/sofort/lp/8/chargeLimitation"]=msmoduslp8
	mqttconfvar["config/get/pv/lp/1/socLimitation"]=stopchargepvatpercentlp1
	mqttconfvar["config/get/pv/lp/2/socLimitation"]=stopchargepvatpercentlp2
	mqttconfvar["config/get/pv/lp/1/maxSoc"]=stopchargepvpercentagelp1
	mqttconfvar["config/get/pv/lp/2/maxSoc"]=stopchargepvpercentagelp2
	mqttconfvar["global/rfidConfigured"]=rfidakt
	mqttconfvar["system/priceForKWh"]=preisjekwh
	mqttconfvar["system/wizzardDone"]=wizzarddone
	mqttconfvar["config/get/display/chartEvuMinMax"]=displayevumax
	mqttconfvar["config/get/display/chartBatteryMinMax"]=displayspeichermax
	mqttconfvar["config/get/display/chartPvMax"]=displaypvmax
	mqttconfvar["config/get/display/showHouseConsumption"]=displayhausanzeigen
	mqttconfvar["config/get/display/chartHouseConsumptionMax"]=displayhausmax
	mqttconfvar["config/get/display/chartLp/1/max"]=displaylp1max
	mqttconfvar["config/get/display/chartLp/2/max"]=displaylp2max
	mqttconfvar["config/get/display/chartLp/3/max"]=displaylp3max
	mqttconfvar["config/get/display/chartLp/4/max"]=displaylp4max
	mqttconfvar["config/get/display/chartLp/5/max"]=displaylp5max
	mqttconfvar["config/get/display/chartLp/6/max"]=displaylp6max
	mqttconfvar["config/get/display/chartLp/7/max"]=displaylp7max
	mqttconfvar["config/get/display/chartLp/8/max"]=displaylp8max
	mqttconfvar["config/get/global/slaveMode"]=slavemode

	for mq in "${!mqttconfvar[@]}"; do
		theval=${!mqttconfvar[$mq]}
		declare o${mqttconfvar[$mq]}
		declare ${mqttconfvar[$mq]}

		tempnewname=${mqttconfvar[$mq]}

		tempoldname=o${mqttconfvar[$mq]}
		tempoldname=$(<ramdisk/mqtt"${mqttconfvar[$mq]}")
		tempnewname="${mqttconfvar[$mq]}"
		if [[ "$tempoldname" != "$theval" ]]; then
			tempPubList="${tempPubList}\nopenWB/${mq}=${theval}"
			echo $theval > ramdisk/mqtt${mqttconfvar[$mq]}
		fi
	done

	tempPubList="${tempPubList}\nopenWB/system/Uptime=$(uptime)"
	tempPubList="${tempPubList}\nopenWB/system/Date=$(date)"
	tempPubList="${tempPubList}\nopenWB/system/Timestamp=${timestamp}"
	#declare -a pvarray=("speichersocminpv" "speichersochystminpv" "mindestuberschuss" "abschaltuberschuss" "abschaltverzoegerung" "einschaltverzoegerung" "minimalampv" "minimalampv" "minimalalp2pv" "minnurpvsoclp1" "minnurpvsocll" "pvbezugeinspeisung" "offsetpv" "speicherpvui" "speichermaxwatt" "speichersocnurpv" "speicherwattnurpv" "adaptpv" "adaptfaktor")
	#for val in ${pvarray[@]}; do
	#	declare o$val
	#	ramdiskvar=$(<ramdisk/mqtt"$val")
	#	actualvar=${!val}
	#	tempname=$val
	#	if [[ "$ramdiskvar" != "$actualvar" ]]; then
	#		tempPubList="${tempPubList}\nopenWB/config/get/pv/${val}=${actualvar}"
	#		echo $actualvar > ramdisk/mqtt$val
	#	fi
	#done
	echo -e $tempPubList | python3 runs/mqttpub.py -q 0 -r &
	runs/pubmqtt.sh &

}
