#!/bin/bash

evsedintest() {

evsedintestlp1=$(<ramdisk/evsedintestlp1)
if [[ $evsedintestlp1 == "ausstehend" ]]; then
	if [[ $evsecon == "modbusevse" ]]; then

		if [[ $modbusevsesource = *virtual* ]]
		then
			if ps ax |grep -v grep |grep "socat pty,link=$modbusevsesource,raw tcp:$modbusevselanip:26" > /dev/null
			then
				echo "test" > /dev/null
			else
				sudo socat pty,link=$modbusevsesource,raw tcp:$modbusevselanip:26 &
			fi
		else
			echo "echo" > /dev/null
		fi


		sleep 1
		sudo python runs/evsewritembusdev.py $modbusevsesource $modbusevseid 1000 17

		sleep 1

		evsedinstat=$(sudo python runs/readmodbus.py $modbusevsesource $modbusevseid 1000 1)

		if [[ $evsedinstat == "[17]" ]]; then
			echo "EVSE LP1 Prüfung erfolgreich"
			echo "erfolgreich" > ramdisk/evsedintestlp1
		else
			echo "EVSE LP1 Prüfung NICHt erfolgreich"
			echo "Fehler" > ramdisk/evsedintestlp1
		fi
		sleep 1
		sudo python runs/evsewritembusdev.py $modbusevsesource $modbusevseid 1000 17
		sleep 1
	else
		echo "$evsecon konfiguriert" > ramdisk/evsedintestlp1
	fi
exit 0
fi
evsedintestlp2=$(<ramdisk/evsedintestlp2)
if [[ $evsedintestlp2 == "ausstehend" ]]; then
	if [[ $evsecons1 == "modbusevse" ]]; then

		if [[ $evsesources1 = *virtual* ]]
		then
			if ps ax |grep -v grep |grep "socat pty,link=$evsesources1,raw tcp:$evselanips1:26" > /dev/null
			then
				echo "test" > /dev/null
			else
				sudo socat pty,link=$evsesources1,raw tcp:$evselanips1:26 &
			fi
		else
			echo "echo" > /dev/null
		fi


		sleep 1
		sudo python runs/evsewritembusdev.py $evsesources1 $evseids1 1000 17

		sleep 1

		evsedinstat=$(sudo python runs/readmodbus.py $evsesources1 $evseids1 1000 1)

		if [[ $evsedinstat == "[17]" ]]; then
			echo "EVSE LP2 Prüfung erfolgreich"
			echo "erfolgreich" > ramdisk/evsedintestlp2
		else
			echo "EVSE LP2 Prüfung NICHt erfolgreich"
			echo "Fehler" > ramdisk/evsedintestlp2
		fi
		sleep 1
		sudo python runs/evsewritembusdev.py $evsesources1 $evseids1 1000 17
		sleep 1
	else
		echo "$evsecons1 konfiguriert" > ramdisk/evsedintestlp2
	fi
exit 0
fi
evsedintestlp3=$(<ramdisk/evsedintestlp3)
if [[ $evsedintestlp3 == "ausstehend" ]]; then
	if [[ $evsecons2 == "modbusevse" ]]; then

		if [[ $evsesources2 = *virtual* ]]
		then
			if ps ax |grep -v grep |grep "socat pty,link=$evsesources2,raw tcp:$evselanips2:26" > /dev/null
			then
				echo "test" > /dev/null
			else
				sudo socat pty,link=$evsesources2,raw tcp:$evselanips2:26 &
			fi
		else
			echo "echo" > /dev/null
		fi


		sleep 1
		sudo python runs/evsewritembusdev.py $evsesources2 $evseids2 1000 17

		sleep 1

		evsedinstat=$(sudo python runs/readmodbus.py $evsesources2 $evseids2 1000 1)

		if [[ $evsedinstat == "[17]" ]]; then
			echo "EVSE LP3 Prüfung erfolgreich"
			echo "erfolgreich" > ramdisk/evsedintestlp3
		else
			echo "EVSE LP3 Prüfung NICHt erfolgreich"
			echo "Fehler" > ramdisk/evsedintestlp3
		fi
		sleep 1
		sudo python runs/evsewritembusdev.py $evsesources2 $evseids2 1000 17
		sleep 1
	else
		echo "$evsecons2 konfiguriert" > ramdisk/evsedintestlp3
	fi
exit 0
fi












}
