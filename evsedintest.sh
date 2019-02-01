#!/bin/bash

evsedintest() {

evsedintestlp1=$(<ramdisk/evsedintestlp1)
if [[ $evsedintestlp1 == "ausstehend" ]]; then
	if [[ $evsecon == "modbusevse"  || $evsecon == "masterethframer"]]; then
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
			sudo python runs/evsewritembusdev.py $modbusevsesource $modbusevseid 1000 9
			sleep 1
			evsedinstat=$(sudo python runs/readmodbus.py $modbusevsesource $modbusevseid 1000 1)
			if [[ $evsedinstat == "[9]" ]]; then
				echo "EVSE LP1 Prüfung erfolgreich"
				echo "erfolgreich" > ramdisk/evsedintestlp1
			else
				echo "EVSE LP1 Prüfung NICHt erfolgreich"
				echo "Fehler" > ramdisk/evsedintestlp1
			fi
			sleep 1
			sudo python runs/evsewritembusdev.py $modbusevsesource $modbusevseid 1000 0
			sleep 1
		fi
		if [[ $evsecon == "masterethframer" ]]; then
			sudo python runs/evsewritembusethframerdev.py 192.168.193.18 1 1000 9
			sleep 1
			evsedinstat=$(sudo python runs/readmodbusethframer.py 192.168.193.18 1 1000 1)
			if [[ $evsedinstat == "[9]" ]]; then
				echo "EVSE LP1 Prüfung erfolgreich"
				echo "erfolgreich" > ramdisk/evsedintestlp1
			else
				echo "EVSE LP1 Prüfung NICHt erfolgreich"
				echo "Fehler" > ramdisk/evsedintestlp1
			fi
			sleep 1
			sudo python runs/evsewritembusethframerdev.py 192.168.193.18 1 1000 0
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
		sudo python runs/evsewritembusdev.py $evsesources1 $evseids1 1000 9

		sleep 1

		evsedinstat=$(sudo python runs/readmodbus.py $evsesources1 $evseids1 1000 1)

		if [[ $evsedinstat == "[9]" ]]; then
			echo "EVSE LP2 Prüfung erfolgreich"
			echo "erfolgreich" > ramdisk/evsedintestlp2
		else
			echo "EVSE LP2 Prüfung NICHt erfolgreich"
			echo "Fehler" > ramdisk/evsedintestlp2
		fi
		sleep 1
		sudo python runs/evsewritembusdev.py $evsesources1 $evseids1 1000 0
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
		sudo python runs/evsewritembusdev.py $evsesources2 $evseids2 1000 9

		sleep 1

		evsedinstat=$(sudo python runs/readmodbus.py $evsesources2 $evseids2 1000 1)

		if [[ $evsedinstat == "[9]" ]]; then
			echo "EVSE LP3 Prüfung erfolgreich"
			echo "erfolgreich" > ramdisk/evsedintestlp3
		else
			echo "EVSE LP3 Prüfung NICHt erfolgreich"
			echo "Fehler" > ramdisk/evsedintestlp3
		fi
		sleep 1
		sudo python runs/evsewritembusdev.py $evsesources2 $evseids2 1000 0
		sleep 1
	else
		echo "$evsecons2 konfiguriert" > ramdisk/evsedintestlp3
	fi
exit 0
fi

}

evsemodbuscheck() {
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
	evsedinstat=$(sudo python runs/readmodbus.py $modbusevsesource $modbusevseid 1000 1)
	sleep 1
	if [[ $evsedinstat == "[$llalt]" ]]; then
		if [[ $debug == "1" ]]; then
			echo "LP1 Modbus $llalt korrekt"
		fi
	else
		if [[ $debug == "1" ]]; then
			echo "LP1 Modbus $llalt nicht korrekt"
		fi
		sudo python runs/evsewritembusdev.py $modbusevsesource $modbusevseid 1000 $llalt
	fi
fi
if (( lastmanagement == 1 )); then 
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
		evsedinstat=$(sudo python runs/readmodbus.py $evsesources1 $evseids1 1000 1)
		sleep 1
		if [[ $evsedinstat == "[$llalts1]" ]]; then
			if [[ $debug == "1" ]]; then
				echo "LP2 Modbus $llalts1 korrekt"
			fi
		else
			if [[ $debug == "1" ]]; then
				echo "LP2 Modbus $llalts1 nichtkorrekt"
			fi
			sudo python runs/evsewritembusdev.py $evsesources1 $evseids1 1000 $llalts1
		fi
	fi
	if (( lastmanagements2 == 1 )); then
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
			evsedinstat=$(sudo python runs/readmodbus.py $evsesources2 $evseids2 1000 1)
			if [[ $evsedinstat == "[$llalts2]" ]]; then
				if [[ $debug == "1" ]]; then
					echo "LP3 Modbus $llalts2 korrekt"
				fi
			else
				if [[ $debug == "1" ]]; then
					echo "LP3 Modbus $llalts2 nicht korrekt"
				fi
				sudo python runs/evsewritembusdev.py $evsesources2 $evseids2 1000 $llalts2
			fi
		fi
	fi
fi

}
