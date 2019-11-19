#!/bin/bash
loadvars(){
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
opvwatt=$(<ramdisk/pvwatt)
owattbezug=$(<ramdisk/wattbezug)
ollaktuell=$(<ramdisk/llaktuell)
ohausverbrauch=$(<ramdisk/hausverbrauch)
ollkombiniert=$(<ramdisk/llkombiniert)
ollaktuells1=$(<ramdisk/llaktuells1)
ollaktuells2=$(<ramdisk/llaktuells2)
ospeicherleistung=$(<ramdisk/speicherleistung)
oladestatus=$(<ramdisk/mqttlastladestatus)
olademodus=$(<ramdisk/mqttlastlademodus)
osoc=$(<ramdisk/soc)
osoc1=$(<ramdisk/soc1)
ospeichersoc=$(<ramdisk/speichersoc)
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
# EVSE DIN Plug State
if [[ $evsecon == "modbusevse" ]]; then
	evseplugstate=$(sudo python runs/readmodbus.py $modbusevsesource $modbusevseid 1002 1)
	ladestatuslp1=$(</var/www/html/openWB/ramdisk/ladestatus)
	if [ "$evseplugstate" -ge "0" ] && [ "$evseplugstate" -le "10" ] ; then
		if [[ $evseplugstate > "1" ]]; then
			plugstat=$(</var/www/html/openWB/ramdisk/plugstat)
			if [[ $plugstat == "0" ]] && [[ $pushbplug == "1" ]] && [[ $ladestatuslp1 == "0" ]] && [[ $pushbenachrichtigung == "1" ]] ; then
				message="Fahrzeug eingesteckt. Ladung startet bei erfüllter Ladebedingung automatisch."
				/var/www/html/openWB/runs/pushover.sh "$message"
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

fi
if [[ $evsecon == "ipevse" ]]; then
	evseplugstatelp1=$(sudo python runs/readipmodbus.py $evseiplp1 $evseidlp1 1002 1)
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
	if [[ $evsecons1 == "modbusevse" ]]; then
		evseplugstatelp2=$(sudo python runs/readmodbus.py $evsesources1 $evseids1 1002 1)
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
	if [[ $evsecons1 == "slaveeth" ]]; then
		evseplugstatelp2=$(sudo python runs/readslave.py 1002 1)
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
fi
if [[ $lastmanagementlp4 == "1" ]]; then
	if [[ $evseconlp4 == "ipevse" ]]; then
		evseplugstatelp4=$(sudo python runs/readipmodbus.py $evseiplp4 $evseidlp4 1002 1)
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
	if [[ $evseconlp5 == "ipevse" ]]; then
		evseplugstatelp5=$(sudo python runs/readipmodbus.py $evseiplp5 $evseidlp5 1002 1)
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
	if [[ $evseconlp6 == "ipevse" ]]; then
		evseplugstatelp6=$(sudo python runs/readipmodbus.py $evseiplp6 $evseidlp6 1002 1)
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
	if [[ $evseconlp7 == "ipevse" ]]; then
		evseplugstatelp7=$(sudo python runs/readipmodbus.py $evseiplp7 $evseidlp7 1002 1)
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
	if [[ $evseconlp8 == "ipevse" ]]; then
		evseplugstatelp8=$(sudo python runs/readipmodbus.py $evseiplp8 $evseidlp8 1002 1)
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

# Lastmanagement var check age
if test $(find "ramdisk/lastregelungaktiv" -mmin +2); then
       echo "" > ramdisk/lastregelungaktiv
fi

# Werte für die Berechnung ermitteln
lademodus=$(</var/www/html/openWB/ramdisk/lademodus)
llalt=$(cat /var/www/html/openWB/ramdisk/llsoll)
#PV Leistung ermitteln
if [[ $pvwattmodul != "none" ]]; then
	pvwatt=$(modules/$pvwattmodul/main.sh || true)
	if ! [[ $pvwatt =~ $re ]] ; then
		pvwatt="0"
	fi
else
	pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
fi

#Speicher werte
if [[ $speichermodul != "none" ]] ; then
	timeout 5 modules/$speichermodul/main.sh || true
	speicherleistung=$(</var/www/html/openWB/ramdisk/speicherleistung)
	speichersoc=$(</var/www/html/openWB/ramdisk/speichersoc)
	speichersoc=$(echo $speichersoc | sed 's/\..*$//')
	speichervorhanden="1"
	echo 1 > /var/www/html/openWB/ramdisk/speichervorhanden
	if [[ $speichermodul == "speicher_alphaess" ]] ; then
		pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
	fi
else
	speichervorhanden="0"
	echo 0 > /var/www/html/openWB/ramdisk/speichervorhanden
fi

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
		timeout 10 modules/$socmodul1/main.sh || true
		soc1=$(</var/www/html/openWB/ramdisk/soc1)
		if ! [[ $soc1 =~ $re ]] ; then
		 soc1="0"
		fi
		echo 1 > /var/www/html/openWB/ramdisk/soc1vorhanden
	else
		echo 0 > /var/www/html/openWB/ramdisk/soc1vorhanden
		soc1=0
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
else
	echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
	ladeleistunglp2=0
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
	timeout 3 modules/mpm3pmlllp4/main.sh || true
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
	timeout 3 modules/mpm3pmlllp5/main.sh || true
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
	timeout 3 modules/mpm3pmlllp6/main.sh || true
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
	timeout 3 modules/mpm3pmlllp7/main.sh || true
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
else
	ladeleistunglp7=0
fi
#achter ladepunkt
if [[ $lastmanagementlp8 == "1" ]]; then
	timeout 3 modules/mpm3pmlllp8/main.sh || true
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


#Wattbezug
if [[ $wattbezugmodul != "none" ]]; then
	wattbezug=$(modules/$wattbezugmodul/main.sh || true)
	if ! [[ $wattbezug =~ $re ]] ; then
		wattbezug="0"
	fi
	#evu glaettung
	if (( evuglaettungakt == 1 )); then
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
	#uberschuss zur berechnung
	wattbezugint=$(printf "%.0f\n" $wattbezug)
	uberschuss=$((wattbezugint * -1))
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
	if ! [[ $evua1 =~ $re ]] ; then
		evua1="0"
	fi
	if ! [[ $evua2 =~ $re ]] ; then
		evua2="0"
	fi
	if ! [[ $evua3 =~ $re ]] ; then
		evua3="0"
	fi
	evuas=($evua1 $evua2 $evua3)
	maxevu=${evuas[0]}
	for v in "${evuas[@]}"; do
		if (( v > maxevu )); then maxevu=$v; fi;
			done
	lowevu=${evuas[0]}
	for v in "${evuas[@]}"; do
		if (( v < lowevu )); then lowevu=$v; fi;
			done
	schieflast=$(( maxevu - lowevu ))
	echo $schieflast > /var/www/html/openWB/ramdisk/schieflast
else
	wattbezug=$pvwatt
	wattbezugint=$(printf "%.0f\n" $wattbezug)
	wattbezugint=$(echo "($wattbezugint+$hausbezugnone+$ladeleistung)" |bc)
	echo "$wattbezugint" > /var/www/html/openWB/ramdisk/wattbezug
	uberschuss=$((wattbezugint * -1))

fi

#Soc ermitteln
if [[ $socmodul != "none" ]]; then
	if (( stopsocnotpluggedlp1 == 1 )); then
		if (( plugstat == 1 )); then
			timeout 10 modules/$socmodul/main.sh || true
			soc=$(</var/www/html/openWB/ramdisk/soc)
			if ! [[ $soc =~ $re ]] ; then
				soc="0"
			fi
		else
			echo 600 > /var/www/html/openWB/ramdisk/soctimer
			soc=$(</var/www/html/openWB/ramdisk/soc)
		fi
	else
		timeout 10 modules/$socmodul/main.sh || true
		soc=$(</var/www/html/openWB/ramdisk/soc)
		if ! [[ $soc =~ $re ]] ; then
			soc="0"
		fi
	fi
else
	soc=0
fi
hausverbrauch=$((wattbezugint - pvwatt - ladeleistung - speicherleistung))
echo $hausverbrauch > /var/www/html/openWB/ramdisk/hausverbrauch
#Uhrzeit
date=$(date)
H=$(date +%H)
if [[ $debug == "1" ]]; then
	echo "$(tail -20000 /var/www/html/openWB/ramdisk/openWB.log)" > /var/www/html/openWB/ramdisk/openWB.log
	date
	if [[ $speichermodul != "none" ]] ; then
		echo speicherleistung $speicherleistung speichersoc $speichersoc
	fi
	echo pvwatt $pvwatt ladeleistung "$ladeleistung" llalt "$llalt" nachtladen "$nachtladen" nachtladen "$nachtladens1" minimalA "$minimalstromstaerke" maximalA "$maximalstromstaerke"
	echo lla1 "$lla1" llas11 "$llas11" llas21 "$llas21" mindestuberschuss "$mindestuberschuss" abschaltuberschuss "$abschaltuberschuss" lademodus "$lademodus"
	echo lla2 "$lla2" llas12 "$llas12" llas22 "$llas22" sofortll "$sofortll" wattbezugint "$wattbezugint" wattbezug "$wattbezug" uberschuss "$uberschuss"
	echo lla3 "$lla3" llas13 "$llas13" llas23 "$llas23" soclp1 $soc soclp2 $soc1
	echo evua 1 "$evua1" 2 "$evua2" 3 "$evua3"
	echo lp1enabled "$lp1enabled" lp2enabled "$lp2enabled" lp3enabled "$lp3enabled"
	echo plugstatlp1 "$plugstat" plugstatlp2 "$plugstatlp2" chargestatlp1 "$chargestat" chargestatlp2 "$chargestatlp2"


fi

tempPubList=""

if (( opvwatt != pvwatt )); then
	tempPubList="${tempPubList}\nopenWB/pv/W=${pvwatt}"
fi
if (( owattbezug != wattbezug )); then
	tempPubList="${tempPubList}\nopenWB/evu/W=${wattbezug}"
fi
if (( ollaktuell != ladeleistunglp1 )); then
	tempPubList="${tempPubList}\nopenWB/lp1/W=${ladeleistunglp1}"
fi
if (( oladestatus != ladestatus )); then
	tempPubList="${tempPubList}\nopenWB/ChargeStatus=${ladelestatus}"
	echo $ladestatus > ramdisk/mqttlastladestatus
fi
if (( olademodus != lademodus )); then
	mosquitto_pub -t openWB/ChargeMode -m "$lademodus"
	echo $lademodus > ramdisk/mqttlastlademodus
fi
if (( ohausverbrauch != hausverbrauch )); then
	tempPubList="${tempPubList}\nopenWB/WHouseConsumption=${hausverbrauch}"
fi
if (( ollaktuells1 != ladeleistungs1 )); then
	tempPubList="${tempPubList}\nopenWB/lp2/W=${ladeleistungs1}"
fi
if (( ollaktuells2 != ladeleistungs2 )); then
	tempPubList="${tempPubList}\nopenWB/lp3/W=${ladeleistungs2}"
fi
if (( ollkombiniert != ladeleistung )); then
	tempPubList="${tempPubList}\nopenWB/WAllChargePoints=${ladeleistung}"
fi
if (( ospeicherleistung != speicherleistung )); then
	tempPubList="${tempPubList}\nopenWB/housebattery/W=${speicherleistung}"
fi
if (( ospeichersoc != speichersoc )); then
	tempPubList="${tempPubList}\nopenWB/housebattery/%Soc=${speichersoc}"
fi
if (( osoc != soc )); then
	tempPubList="${tempPubList}\nopenWB/lp1/%Soc=${soc}"
fi
if (( osoc1 != soc1 )); then
	tempPubList="${tempPubList}\nopenWB/lp2/%Soc=${soc1}"
fi

dailychargelp1=$(curl -s -X POST -d "dailychargelp1call=loadfile" http://127.0.0.1:/openWB/web/tools/dailychargelp1.php | jq -r .text)
dailychargelp2=$(curl -s -X POST -d "dailychargelp2call=loadfile" http://127.0.0.1:/openWB/web/tools/dailychargelp2.php | jq -r .text)
dailychargelp3=$(curl -s -X POST -d "dailychargelp3call=loadfile" http://127.0.0.1:/openWB/web/tools/dailychargelp3.php | jq -r .text)
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
	tempPubList="${tempPubList}\nopenWB/lp1/kWhDailyCharged=${dailychargelp1}"
	echo $dailychargelp1 > ramdisk/mqttdailychargelp1
fi
if [[ "$odailychargelp2" != "$dailychargelp2" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp2/kWhDailyCharged=${dailychargelp2}"
	echo $dailychargelp2 > ramdisk/mqttdailychargelp2
fi
if [[ "$odailychargelp3" != "$dailychargelp3" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp3/kWhDailyCharged=${dailychargelp3}"
	echo $dailychargelp3 > ramdisk/mqttdailychargelp3
fi
if [[ "$orestzeitlp1" != "$restzeitlp1" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp1/TimeRemaining=${restzeitlp1}"
	echo $restzeitlp1 > ramdisk/mqttrestzeitlp1
fi
if [[ "$orestzeitlp2" != "$restzeitlp2" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp2/TimeRemaining=${restzeitlp2}"
	echo $restzeitlp2 > ramdisk/mqttrestzeitlp2
fi
if [[ "$orestzeitlp3" != "$restzeitlp3" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp3/TimeRemaining=${restzeitlp3}"
	echo $restzeitlp3 > ramdisk/mqttrestzeitlp3
fi
if (( ogelrlp1 != gelrlp1 )); then
	tempPubList="${tempPubList}\nopenWB/lp1/kmCharged=${gelrlp1}"
	echo $gelrlp1 > ramdisk/mqttgelrlp1
fi
if (( ogelrlp2 != gelrlp2 )); then
	tempPubList="${tempPubList}\nopenWB/lp2/kmCharged=${gelrlp2}"
	echo $gelrlp2 > ramdisk/mqttgelrlp2
fi
if (( ogelrlp3 != gelrlp3 )); then
	tempPubList="${tempPubList}\nopenWB/lp3/kmCharged=${gelrlp3}"
	echo $gelrlp3 > ramdisk/mqttgelrlp3
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
ominimalstromstaerke=$(<ramdisk/mqttminimalstromstaerke)
if (( ominimalstromstaerke != minimalstromstaerke )); then
	tempPubList="${tempPubList}\nopenWB/AMinimalAmpsConfigured=${minimalstromstaerke}"
	echo $minimalstromstaerke > ramdisk/mqttminimalstromstaerke
fi
omaximalstromstaerke=$(<ramdisk/mqttmaximalstromstaerke)
if (( omaximalstromstaerke != maximalstromstaerke )); then
	tempPubList="${tempPubList}\nopenWB/AMaximalAmpsConfigured=${maximalstromstaerke}"
	echo $maximalstromstaerke > ramdisk/mqttmaximalstromstaerke
fi
osofortll=$(<ramdisk/mqttsofortll)
if (( osofortll != sofortll )); then
	tempPubList="${tempPubList}\nopenWB/lp1/ADirectModeAmps=${sofortll}"
	echo $sofortll > ramdisk/mqttsofortll
fi
osofortlls1=$(<ramdisk/mqttsofortlls1)
if (( osofortlls1 != sofortlls1 )); then
	tempPubList="${tempPubList}\nopenWB/lp2/ADirectModeAmps=${sofortlls1}"
	echo $sofortlls1 > ramdisk/mqttsofortlls1
fi
osofortlls2=$(<ramdisk/mqttsofortlls2)
if (( osofortlls2 != sofortlls2 )); then
	tempPubList="${tempPubList}\nopenWB/lp3/ADirectModeAmps=${sofortlls2}"
	echo $sofortlls2 > ramdisk/mqttsofortlls2
fi
osofortlllp4=$(<ramdisk/mqttsofortlllp4)
if (( osofortlllp4 != sofortlllp4 )); then
	tempPubList="${tempPubList}\nopenWB/lp4/ADirectModeAmps=${sofortlllp4}"
	echo $sofortlllp4 > ramdisk/mqttsofortlllp4
fi
osofortlllp5=$(<ramdisk/mqttsofortlllp5)
if (( osofortlllp5 != sofortlllp5 )); then
	tempPubList="${tempPubList}\nopenWB/lp5/ADirectModeAmps=${sofortlllp5}"
	echo $sofortlllp5 > ramdisk/mqttsofortlllp5
fi
osofortlllp6=$(<ramdisk/mqttsofortlllp6)
if (( osofortlllp6 != sofortlllp6 )); then
	tempPubList="${tempPubList}\nopenWB/lp6/ADirectModeAmps=${sofortlllp6}"
	echo $sofortlllp6 > ramdisk/mqttsofortlllp6
fi
osofortlllp7=$(<ramdisk/mqttsofortlllp7)
if (( osofortlllp7 != sofortlllp7 )); then
	tempPubList="${tempPubList}\nopenWB/lp7/ADirectModeAmps=${sofortlllp7}"
	echo $sofortlllp7 > ramdisk/mqttsofortlllp7
fi
osofortlllp8=$(<ramdisk/mqttsofortlllp8)
if (( osofortlllp8 != sofortlllp8 )); then
	tempPubList="${tempPubList}\nopenWB/lp8/ADirectModeAmps=${sofortlllp8}"
	echo $sofortlllp8 > ramdisk/mqttsofortlllp8
fi

olastmanagement=$(<ramdisk/mqttlastmanagement)
if [[ "$olastmanagement" != "$lastmanagement" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp2/boolChargePointConfigured=${lastmanagement}"
	echo $lastmanagement > ramdisk/mqttlastmanagement
fi
olastmanagements2=$(<ramdisk/mqttlastmanagements2)
if [[ "$olastmanagements2" != "$lastmanagements2" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp3/boolChargePointConfigured=${lastmanagements2}"
	echo $lastmanagements2 > ramdisk/mqttlastmanagements2
fi
olastmanagementlp4=$(<ramdisk/mqttlastmanagementlp4)
if [[ "$olastmanagementlp4" != "$lastmanagementlp4" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp4/boolChargePointConfigured=${lastmanagementlp4}"
	echo $lastmanagementlp4 > ramdisk/mqttlastmanagementlp4
fi
olastmanagementlp5=$(<ramdisk/mqttlastmanagementlp5)
if [[ "$olastmanagementlp5" != "$lastmanagementlp5" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp5/boolChargePointConfigured=${lastmanagementlp5}"
	echo $lastmanagementlp5 > ramdisk/mqttlastmanagementlp5
fi
olastmanagementlp6=$(<ramdisk/mqttlastmanagementlp6)
if [[ "$olastmanagementlp6" != "$lastmanagementlp6" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp6/boolChargePointConfigured=${lastmanagementlp6}"
	echo $lastmanagementlp6 > ramdisk/mqttlastmanagementlp6
fi
olastmanagementlp7=$(<ramdisk/mqttlastmanagementlp7)
if [[ "$olastmanagementlp7" != "$lastmanagementlp7" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp7/boolChargePointConfigured=${lastmanagementlp7}"
	echo $lastmanagementlp7 > ramdisk/mqttlastmanagementlp7
fi
olastmanagementlp8=$(<ramdisk/mqttlastmanagementlp8)
if [[ "$olastmanagementlp8" != "$lastmanagementlp8" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp8/boolChargePointConfigured=${lastmanagementlp8}"
	echo $lastmanagementlp8 > ramdisk/mqttlastmanagementlp8
fi
olademstat=$(<ramdisk/mqttlademstat)
if [[ "$olademstat" != "$lademstat" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp1/boolDirectModeChargekWh=${lademstat}"
	echo $lademstat > ramdisk/mqttlademstat
fi
olademstats1=$(<ramdisk/mqttlademstats1)
if [[ "$olademstats1" != "$lademstats1" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp2/boolDirectModeChargekWh=${lademstats1}"
	echo $lademstats1 > ramdisk/mqttlademstats1
fi
olademstats2=$(<ramdisk/mqttlademstats2)
if [[ "$olademstats2" != "$lademstats2" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp3/boolDirectModeChargekWh=${lademstats2}"
	echo $lademstats2 > ramdisk/mqttlademstats2
fi
olademkwh=$(<ramdisk/mqttlademkwh)
if (( olademkwh != lademkwh )); then
	tempPubList="${tempPubList}\nopenWB/lp1/kWhDirectModeToChargekWh=${lademkwh}"
	echo $lademkwh > ramdisk/mqttlademkwh
fi
olademkwhs1=$(<ramdisk/mqttlademkwhs1)
if (( olademkwhs1 != lademkwhs1 )); then
	tempPubList="${tempPubList}\nopenWB/lp2/kWhDirectModeToChargekWh=${lademkwhs1}"
	echo $lademkwhs1 > ramdisk/mqttlademkwhs1
fi
olademkwhs2=$(<ramdisk/mqttlademkwhs2)
if (( olademkwhs2 != lademkwhs2 )); then
	tempPubList="${tempPubList}\nopenWB/lp3/kWhDirectModeToChargekWh=${lademkwhs2}"
	echo $lademkwhs2 > ramdisk/mqttlademkwhs2
fi
osofortsocstatlp1=$(<ramdisk/mqttsofortsocstatlp1)
if [[ "$osofortsocstatlp1" != "$sofortsocstatlp1" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp1/boolDirectChargeModeSoc=${sofortsocstatlp1}"
	echo $sofortsocstatlp1 > ramdisk/mqttsofortsocstatlp1
fi
osofortsoclp1=$(<ramdisk/mqttsofortsoclp1)
if [[ "$osofortsoclp1" != "$sofortsoclp1" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp1/PercentDirectChargeModeSoc=${sofortsoclp1}"
	echo $sofortsoclp1 > ramdisk/mqttsofortsoclp1
fi
osofortsocstatlp2=$(<ramdisk/mqttsofortsocstatlp2)
if [[ "$osofortsocstatlp2" != "$sofortsocstatlp2" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp2/boolDirectChargeModeSoc=${sofortsocstatlp2}"
	echo $sofortsocstatlp2 > ramdisk/mqttsofortsocstatlp2
fi
osofortsoclp2=$(<ramdisk/mqttsofortsoclp2)
if [[ "$osofortsoclp2" != "$sofortsoclp2" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp2/percentDirectChargeModeSoc=${sofortsoclp2}"
	echo $sofortsoclp2 > ramdisk/mqttsofortsoclp2
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
omsmoduslp1=$(<ramdisk/mqttmsmoduslp1)
if [[ "$omsmoduslp1" != "$msmoduslp1" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp1/boolDirectChargeMode_none_kwh_soc=${msmoduslp1}"
	echo $msmoduslp1 > ramdisk/mqttmsmoduslp1
fi
omsmoduslp2=$(<ramdisk/mqttmsmoduslp2)
if [[ "$omsmoduslp2" != "$msmoduslp2" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp2/boolDirectChargeMode_none_kwh_soc=${msmoduslp2}"
	echo $msmoduslp2 > ramdisk/mqttmsmoduslp2
fi
ospeichervorhanden=$(<ramdisk/mqttspeichervorhanden)
if (( ospeichervorhanden != speichervorhanden )); then
	tempPubList="${tempPubList}\nopenWB/housebattery/boolHouseBatteryConfigured=${speichervorhanden}"
	echo $speichervorhanden > ramdisk/mqttspeichervorhanden
fi
olp1name=$(<ramdisk/mqttlp1name)
if [[ "$olp1name" != "$lp1name" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp1/strChargePointName=${lp1name}"
	echo $lp1name > ramdisk/mqttlp1name
fi
olp2name=$(<ramdisk/mqttlp2name)
if [[ "$olp2name" != "$lp2name" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp2/strChargePointName=${lp2name}"
	echo $lp2name > ramdisk/mqttlp2name
fi
olp3name=$(<ramdisk/mqttlp3name)
if [[ "$olp3name" != "$lp3name" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp3/strChargePointName=${lp3name}"
	echo $lp3name > ramdisk/mqttlp3name
fi
olp4name=$(<ramdisk/mqttlp4name)
if [[ "$olp4name" != "$lp4name" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp4/strChargePointName=${lp4name}"
	echo $lp4name > ramdisk/mqttlp4name
fi
olp5name=$(<ramdisk/mqttlp5name)
if [[ "$olp5name" != "$lp5name" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp5/strChargePointName=${lp5name}"
	echo $lp5name > ramdisk/mqttlp5name
fi
olp6name=$(<ramdisk/mqttlp6name)
if [[ "$olp6name" != "$lp6name" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp6/strChargePointName=${lp6name}"
	echo $lp6name > ramdisk/mqttlp6name
fi
olp7name=$(<ramdisk/mqttlp7name)
if [[ "$olp7name" != "$lp7name" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp7/strChargePointName=${lp7name}"
	echo $lp7name > ramdisk/mqttlp7name
fi
olp8name=$(<ramdisk/mqttlp8name)
if [[ "$olp8name" != "$lp8name" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp8/strChargePointName=${lp8name}"
	echo $lp8name > ramdisk/mqttlp8name
fi
ozielladenaktivlp1=$(<ramdisk/mqttzielladenaktivlp1)
if [[ "$ozielladenaktivlp1" != "$zielladenaktivlp1" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp1/boolFinishAtTimeChargeActive=${zielladenaktivlp1}"
	echo $zielladenaktivlp1 > ramdisk/mqttzielladenaktivlp1
fi
onachtladen=$(<ramdisk/mqttnachtladen)
if [[ "$onachtladen" != "$nachtladen" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp1/boolChargeAtNight=${nachtladen}"
	echo $nachtladen > ramdisk/mqttnachtladen
fi
onachtladens1=$(<ramdisk/mqttnachtladens1)
if [[ "$onachtladens1" != "$nachtladens1" ]]; then
	tempPubList="${tempPubList}\nopenWB/lp2/boolChargeAtNight=${nachtladens1}"
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

onlakt_standby=$(<ramdisk/mqttnlakt_sofort)
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
ographliveam=$(<ramdisk/mqttgraphliveam)
if [[ "$ographliveam" != "$graphliveam" ]]; then
	tempPubList="${tempPubList}\nopenWB/boolGraphLiveAM=${graphliveam}"
	echo $graphliveam > ramdisk/mqttgraphliveam
fi
ospeicherpvui=$(<ramdisk/mqttspeicherpvui)
if [[ "$ospeicherpvui" != "$speicherpvui" ]]; then
	tempPubList="${tempPubList}\nopenWB/boolDisplayHouseBatteryPriority=${speicherpvui}"
	echo $speicherpvui > ramdisk/mqttspeicherpvui
fi
tempPubList="${tempPubList}\nopenWB/system/Uptime=$(uptime)"
tempPubList="${tempPubList}\nopenWB/system/Date=$(date)"
tempPubList="${tempPubList}\nopenWB/system/Timestamp=$(date +%s)"

echo -e $tempPubList | python3 runs/mqttpub.py -q 0 -r &

}
