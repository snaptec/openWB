#!/bin/bash
loadvars(){

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
oplugstat=$(<ramdisk/mqttlastplugstat)
ochargestat=$(<ramdisk/mqttlastchargestat)
oplugstats1=$(<ramdisk/mqttlastplugstats1)
ochargestats1=$(<ramdisk/mqttlastchargestats1)
ladestatus=$(</var/www/html/openWB/ramdisk/ladestatus)
odailychargelp1=$(<ramdisk/mqttdailychargelp1)
odailychargelp2=$(<ramdisk/mqttdailychargelp2)
odailychargelp3=$(<ramdisk/mqttdailychargelp3)
oaktgeladens1=$(<ramdisk/mqttaktgeladens1)
oaktgeladens2=$(<ramdisk/mqttaktgeladens2)
oaktgeladen=$(<ramdisk/mqttaktgeladen)
ollsoll=$(<ramdisk/mqttllsoll)
ollsolls1=$(<ramdisk/mqttllsolls1)
ollsolls2=$(<ramdisk/mqttllsolls2)
orestzeitlp1=$(<ramdisk/mqttrestzeitlp1)
orestzeitlp2=$(<ramdisk/mqttrestzeitlp2)
orestzeitlp3=$(<ramdisk/mqttrestzeitlp3)
ogelrlp1=$(<ramdisk/mqttgelrlp1)
ogelrlp2=$(<ramdisk/mqttgelrlp2)
ogelrlp3=$(<ramdisk/mqttgelrlp3)
opluggedchargedkwhlp1=$(<ramdisk/pluggedladungbishergeladen)
opluggedchargedkwhlp2=$(<ramdisk/pluggedladungbishergeladenlp2)
olastregelungaktiv=$(<ramdisk/lastregelungaktiv)
ohook1aktiv=$(<ramdisk/hook1akt)
ohook2aktiv=$(<ramdisk/hook2akt)
ohook3aktiv=$(<ramdisk/hook3akt)







# EVSE DIN Plug State
if [[ $evsecon == "modbusevse" ]]; then
	evseplugstate=$(sudo python runs/readmodbus.py $modbusevsesource $modbusevseid 1002 1)
	if [ "$evseplugstate" -ge "0" ] && [ "$evseplugstate" -le "10" ] ; then
		if [[ $evseplugstate > "1" ]]; then
			plugstat=$(</var/www/html/openWB/ramdisk/plugstat)
			if [[ $plugstat == "0" ]] && [[ $pushbplug == "1" ]] && [[ $ladestatus == "0" ]] && [[ $pushbenachrichtigung == "1" ]] ; then
				message="Fahrzeug eingesteckt. Ladung startet bei erfüllter Ladebedingung automatisch."
				/var/www/html/openWB/runs/pushover.sh "$message"
			fi
				echo 1 > /var/www/html/openWB/ramdisk/plugstat
				plugstat=1
		else
			echo 0 > /var/www/html/openWB/ramdisk/plugstat
			plugstat=0
		fi
		if [[ $evseplugstate > "2" ]] && [[ $ladestatus == "1" ]] ; then
			echo 1 > /var/www/html/openWB/ramdisk/chargestat
			chargestat=1
		else
			echo 0 > /var/www/html/openWB/ramdisk/chargestat
			chargestat=0
		fi
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
fi
#dritter ladepunkt
if [[ $lastmanagements2 == "1" ]]; then
	timeout 10 modules/$ladeleistungs2modul/main.sh || true
	llkwhs2=$(</var/www/html/openWB/ramdisk/llkwhs2)
	llkwhges=$(echo "$llkwhges + $llkwhs2" |bc)
	llalts2=$(cat /var/www/html/openWB/ramdisk/llsolls2)
	ladeleistungs2=$(cat /var/www/html/openWB/ramdisk/llaktuells2)
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
fi
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
	timeout 10 modules/$socmodul/main.sh || true
	soc=$(</var/www/html/openWB/ramdisk/soc)
	if ! [[ $soc =~ $re ]] ; then
	 soc="0"
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
fi
if (( opvwatt != pvwatt )); then
	mosquitto_pub -t openWB/pv/W -r -m "$pvwatt"
fi
if (( owattbezug != wattbezug )); then
	mosquitto_pub -t openWB/evu/W -r -m "$wattbezug"
fi
if (( ollaktuell != ladeleistunglp1 )); then
	mosquitto_pub -t openWB/lp1/W -r -m "$ladeleistunglp1"
fi
if (( oladestatus != ladestatus )); then
	mosquitto_pub -t openWB/chargestatus -m "$ladestatus"
	echo $ladestatus > ramdisk/mqttlastladestatus
fi
if (( olademodus != lademodus )); then
	mosquitto_pub -t openWB/chargemode -m "$lademodus"
	echo $lademodus > ramdisk/mqttlastlademodus
fi
if (( ohausverbrauch != hausverbrauch )); then
	mosquitto_pub -t openWB/Whouseconsumption -r -m "$hausverbrauch"
fi
if (( ollaktuells1 != ladeleistungs1 )); then
	mosquitto_pub -t openWB/lp2/W -r -m "$ladeleistungs1"
fi
if (( ollaktuells2 != ladeleistungs2 )); then
	mosquitto_pub -t openWB/lp3/W -r -m "$ladeleistungs2"
fi
if (( ollkombiniert != ladeleistung )); then
	mosquitto_pub -t openWB/Wallchargepoints -r -m "$ladeleistung"
fi
if (( ospeicherleistung != speicherleistung )); then
	mosquitto_pub -t openWB/housebattery/W -r -m "$speicherleistung"
fi
if (( ospeichersoc != speichersoc )); then
	mosquitto_pub -t openWB/housebattery/%soc -r -m "$speichersoc"
fi
if (( osoc != soc )); then
	mosquitto_pub -t openWB/lp1/%soc -r -m "$soc"
fi
if (( osoc1 != soc1 )); then
	mosquitto_pub -t openWB/lp2/%soc -r -m "$soc1"
fi
plugstat=$(<ramdisk/plugstat)
chargestat=$(<ramdisk/chargestat)
plugstats1=$(<ramdisk/plugstats1)
chargestats1=$(<ramdisk/chargestats1)
if (( oplugstat != plugstat )); then
	mosquitto_pub -t openWB/lp1/boolplugstat -r -m "$plugstat"
	echo $plugstat > ramdisk/mqttlastplugstat

fi
if (( oplugstats1 != plugstats1 )); then
	mosquitto_pub -t openWB/lp2/boolplugstat -r -m "$plugstats1"
	echo $plugstats1 > ramdisk/mqttlastplugstats1
fi
if (( ochargestats1 != chargestats1 )); then
	mosquitto_pub -t openWB/lp2/boolchargestat -r -m "$chargestats1"
	echo $chargestats1 > ramdisk/mqttlastchargestats1
fi
if (( ochargestat != chargestat )); then
	mosquitto_pub -t openWB/lp1/boolchargestat -r -m "$chargestat"
	echo $chargestat > ramdisk/mqttlastchargestat
fi
dailychargelp1=$(curl -s -X POST -d "dailychargelp1call=loadfile" http://127.0.0.1:/openWB/web/tools/dailychargelp1.php | jq -r .text)
dailychargelp2=$(curl -s -X POST -d "dailychargelp2call=loadfile" http://127.0.0.1:/openWB/web/tools/dailychargelp2.php | jq -r .text)
dailychargelp3=$(curl -s -X POST -d "dailychargelp3call=loadfile" http://127.0.0.1:/openWB/web/tools/dailychargelp3.php | jq -r .text)
aktgeladens1=$(<ramdisk/aktgeladens1)
aktgeladens2=$(<ramdisk/aktgeladens2)
aktgeladen=$(<ramdisk/aktgeladen)
llsoll=$(<ramdisk/llsoll)
llsolls1=$(<ramdisk/llsolls1)
llsolls2=$(<ramdisk/llsolls2)
restzeitlp1=$(<ramdisk/restzeitlp1)
restzeitlp2=$(<ramdisk/restzeitlp2)
restzeitlp3=$(<ramdisk/restzeitlp3)
gelrlp1=$(<ramdisk/gelrlp1)
gelrlp2=$(<ramdisk/gelrlp2)
gelrlp3=$(<ramdisk/gelrlp3)
pluggedchargedkwhlp1=$(<ramdisk/pluggedladungbishergeladen)
pluggedchargedkwhlp2=$(<ramdisk/pluggedladungbishergeladenlp2)
lastregelungaktiv=$(<ramdisk/lastregelungaktiv)
hook1aktiv=$(<ramdisk/hook1akt)
hook2aktiv=$(<ramdisk/hook2akt)
hook3aktiv=$(<ramdisk/hook3akt)
if [[ "$odailychargelp1" != "$dailychargelp1" ]]; then
	mosquitto_pub -t openWB/lp1/kWhdailycharged -r -m "$dailychargelp1"
	echo $dailychargelp1 > ramdisk/mqttdailychargelp1
fi
if [[ "$odailychargelp2" != "$dailychargelp2" ]]; then
	mosquitto_pub -t openWB/lp2/kWhdailycharged -r -m "$dailychargelp2"
	echo $dailychargelp2 > ramdisk/mqttdailychargelp2
fi
if [[ "$odailychargelp3" != "$dailychargelp3" ]]; then
	mosquitto_pub -t openWB/lp3/kWhdailycharged -r -m "$dailychargelp3"
	echo $dailychargelp3 > ramdisk/mqttdailychargelp3
fi
if [[ "$oaktgeladen" != "$aktgeladen" ]]; then
	mosquitto_pub -t openWB/lp1/kWhactualcharged -r -m "$aktgeladen"
	echo $aktgeladen > ramdisk/mqttaktgeladen
fi
if [[ "$oaktgeladens1" != "$aktgeladens1" ]]; then
	mosquitto_pub -t openWB/lp2/kWhactualcharged -r -m "$aktgeladens1"
	echo $aktgeladens1 > ramdisk/mqttaktgeladens1
fi
if [[ "$oaktgeladens2" != "$aktgeladens2" ]]; then
	mosquitto_pub -t openWB/lp3/kWhactualcharged -r -m "$aktgeladens2"
	echo $aktgeladens2 > ramdisk/mqttaktgeladens2
fi
if (( ollsoll != llsoll )); then
	mosquitto_pub -t openWB/lp1/Aconfigured -r -m "$llsoll"
	echo $llsoll > ramdisk/mqttllsoll
fi
if (( ollsolls1 != llsolls1 )); then
	mosquitto_pub -t openWB/lp2/Aconfigured -r -m "$llsolls1"
	echo $llsolls1 > ramdisk/mqttllsolls1
fi
if (( ollsolls2 != llsolls2 )); then
	mosquitto_pub -t openWB/lp3/Aconfigured -r -m "$llsolls2"
	echo $llsolls2 > ramdisk/mqttllsolls2
fi
if [[ "$orestzeitlp1" != "$restzeitlp1" ]]; then
	mosquitto_pub -t openWB/lp1/timeremaining -r -m "$restzeitlp1"
	echo $restzeitlp1 > ramdisk/mqttrestzeitlp1
fi
if [[ "$orestzeitlp2" != "$restzeitlp2" ]]; then
	mosquitto_pub -t openWB/lp2/timeremaining -r -m "$restzeitlp2"
	echo $restzeitlp2 > ramdisk/mqttrestzeitlp2
fi
if [[ "$orestzeitlp3" != "$restzeitlp3" ]]; then
	mosquitto_pub -t openWB/lp3/timeremaining -r -m "$restzeitlp3"
	echo $restzeitlp3 > ramdisk/mqttrestzeitlp3
fi
if (( ogelrlp1 != gelrlp1 )); then
	mosquitto_pub -t openWB/lp1/kmcharged -r -m "$gelrlp1"
	echo $gelrlp1 > ramdisk/mqttgelrlp1
fi
if (( ogelrlp2 != gelrlp2 )); then
	mosquitto_pub -t openWB/lp2/kmcharged -r -m "$gelrlp2"
	echo $gelrlp2 > ramdisk/mqttgelrlp2
fi
if (( ogelrlp3 != gelrlp3 )); then
	mosquitto_pub -t openWB/lp3/kmcharged -r -m "$gelrlp3"
	echo $gelrlp3 > ramdisk/mqttgelrlp3
fi
if (( opluggedchargedkwhlp1 != pluggedchargedkwhlp1 )); then
	mosquitto_pub -t openWB/lp1/kWhchargedsinceplugged -r -m "$pluggedchargedkwhlp1"
	echo $pluggedchargedkwhlp1 > ramdisk/mqttpluggedchargedkwhlp1
fi
if [[ "$opluggedchargedkwhlp2" != "$pluggedchargedkwhlp2" ]]; then
	mosquitto_pub -t openWB/lp2/kWhchargedsinceplugged -r -m "$pluggedchargedkwhlp2"
	echo $pluggedchargedkwhlp2 > ramdisk/mqttpluggedchargedkwhlp2
fi
if (( ohook1aktiv != hook1aktiv )); then
	mosquitto_pub -t openWB/boolhook1active -r -m "$hook1aktiv"
	echo $hook1aktiv > ramdisk/mqtthook1aktiv
fi
if (( ohook2aktiv != hook2aktiv )); then
	mosquitto_pub -t openWB/boolhook2active -r -m "$hook2aktiv"
	echo $hook2aktiv > ramdisk/mqtthook2aktiv
fi
if (( ohook3aktiv != hook3aktiv )); then
	mosquitto_pub -t openWB/boolhook3active -r -m "$hook3aktiv"
	echo $hook3aktiv > ramdisk/mqtthook3aktiv
fi
ominimalstromstaerke=$(<ramdisk/mqttminimalstromstaerke)
if (( ominimalstromstaerke != minimalstromstaerke )); then
	mosquitto_pub -t openWB/Aminimalampsconfigured -r -m "$minimalstromstaerke"
	echo $minimalstromstaerke > ramdisk/mqttminimalstromstaerke
fi
omaximalstromstaerke=$(<ramdisk/mqttmaximalstromstaerke)
if (( omaximalstromstaerke != maximalstromstaerke )); then
	mosquitto_pub -t openWB/Amaximalampsconfigured -r -m "$maximalstromstaerke"
	echo $maximalstromstaerke > ramdisk/mqttmaximalstromstaerke
fi
osofortll=$(<ramdisk/mqttsofortll)
if (( osofortll != sofortll )); then
	mosquitto_pub -t openWB/lp1/Adirectmodeamps -r -m "$sofortll"
	echo $sofortll > ramdisk/mqttsofortll
fi
osofortlls1=$(<ramdisk/mqttsofortlls1)
if (( osofortlls1 != sofortlls1 )); then
	mosquitto_pub -t openWB/lp2/Adirectmodeamps -r -m "$sofortlls1"
	echo $sofortlls1 > ramdisk/mqttsofortlls1
fi
osofortlls2=$(<ramdisk/mqttsofortlls2)
if (( osofortlls2 != sofortlls2 )); then
	mosquitto_pub -t openWB/lp3/directmodeamps -r -m "$sofortlls2"
	echo $sofortlls2 > ramdisk/mqttsofortlls2
fi
olastmanagement=$(<ramdisk/mqttlastmanagement)
if [[ "$olastmanagement" != "$lastmanagement" ]]; then
	mosquitto_pub -t openWB/lp2/boolchargepointconfigured -r -m "$lastmanagement"
	echo $lastmanagement > ramdisk/mqttlastmanagement
fi
olastmanagements2=$(<ramdisk/mqttlastmanagements2)
if [[ "$olastmanagements2" != "$lastmanagements2" ]]; then
	mosquitto_pub -t openWB/lp3/boolchargepointconfigured -r -m "$lastmanagements2"
	echo $lastmanagements2 > ramdisk/mqttlastmanagements2
fi
olademstat=$(<ramdisk/mqttlademstat)
if [[ "$olademstat" != "$lademstat" ]]; then
	mosquitto_pub -t openWB/lp1/booldirectmodechargekWh -r -m "$lademstat"
	echo $lademstat > ramdisk/mqttlademstat
fi
olademstats1=$(<ramdisk/mqttlademstats1)
if [[ "$olademstats1" != "$lademstats1" ]]; then
	mosquitto_pub -t openWB/lp2/booldirectmodechargekWh -r -m "$lademstats1"
	echo $lademstats1 > ramdisk/mqttlademstats1
fi
olademstats2=$(<ramdisk/mqttlademstats2)
if [[ "$olademstats2" != "$lademstats2" ]]; then
	mosquitto_pub -t openWB/lp3/booldirectmodechargekWh -r -m "$lademstats2"
	echo $lademstats2 > ramdisk/mqttlademstats2
fi
olademkwh=$(<ramdisk/mqttlademkwh)
if (( olademkwh != lademkwh )); then
	mosquitto_pub -t openWB/lp1/kWhdirectmodetochargekWh -r -m "$lademkwh"
	echo $lademkwh > ramdisk/mqttlademkwh
fi
olademkwhs1=$(<ramdisk/mqttlademkwhs1)
if (( olademkwhs1 != lademkwhs1 )); then
	mosquitto_pub -t openWB/lp2/kWhdirectmodetochargekWh -r -m "$lademkwhs1"
	echo $lademkwhs1 > ramdisk/mqttlademkwhs1
fi
olademkwhs2=$(<ramdisk/mqttlademkwhs2)
if (( olademkwhs2 != lademkwhs2 )); then
	mosquitto_pub -t openWB/lp3/kWhdirectmodetochargekWh -r -m "$lademkwhs2"
	echo $lademkwhs2 > ramdisk/mqttlademkwhs2
fi
osofortsocstatlp1=$(<ramdisk/mqttsofortsocstatlp1)
if [[ "$osofortsocstatlp1" != "$sofortsocstatlp1" ]]; then
	mosquitto_pub -t openWB/lp1/booldirectchargemodesoc -r -m "$sofortsocstatlp1"
	echo $sofortsocstatlp1 > ramdisk/mqttsofortsocstatlp1
fi
osofortsoclp1=$(<ramdisk/mqttsofortsoclp1)
if [[ "$osofortsoclp1" != "$sofortsoclp1" ]]; then
	mosquitto_pub -t openWB/lp1/percentdirectchargemodesoc -r -m "$sofortsoclp1"
	echo $sofortsoclp1 > ramdisk/mqttsofortsoclp1
fi
osofortsocstatlp2=$(<ramdisk/mqttsofortsocstatlp2)
if [[ "$osofortsocstatlp2" != "$sofortsocstatlp2" ]]; then
	mosquitto_pub -t openWB/lp2/booldirectchargemodesoc -r -m "$sofortsocstatlp2"
	echo $sofortsocstatlp2 > ramdisk/mqttsofortsocstatlp2
fi
osofortsoclp2=$(<ramdisk/mqttsofortsoclp2)
if [[ "$osofortsoclp2" != "$sofortsoclp2" ]]; then
	mosquitto_pub -t openWB/lp2/percentdirectchargemodesoc -r -m "$sofortsoclp2"
	echo $sofortsoclp2 > ramdisk/mqttsofortsoclp2
fi
#osofortsocstatlp3=$(<ramdisk/mqttsofortsocstatlp3)
#if (( osofortsocstatlp3 != sofortsocstatlp3 )); then
#	mosquitto_pub -t openWB/boolsofortlademodussoclp3 -r -m "$sofortsocstatlp3"
#	echo $sofortsocstatlp3 > ramdisk/mqttsofortsocstatlp3
#fi
#osofortsoclp3=$(<ramdisk/mqttsofortsoclp3)
#if (( osofortsoclp3 != sofortsoclp3 )); then
#	mosquitto_pub -t openWB/percentsofortlademodussoclp3 -r -m "$sofortsoclp3"
#	echo $sofortsoclp3 > ramdisk/mqttsofortsoclp3
#fi
omsmoduslp1=$(<ramdisk/mqttmsmoduslp1)
if [[ "$omsmoduslp1" != "$msmoduslp1" ]]; then
	mosquitto_pub -t openWB/lp1/booldirectchargemode_none_kwh_soc -r -m "$msmoduslp1"
	echo $msmoduslp1 > ramdisk/mqttmsmoduslp1
fi
omsmoduslp2=$(<ramdisk/mqttmsmoduslp2)
if [[ "$omsmoduslp2" != "$msmoduslp2" ]]; then
	mosquitto_pub -t openWB/lp2/booldirectchargemode_none_kwh_soc -r -m "$msmoduslp2"
	echo $msmoduslp2 > ramdisk/mqttmsmoduslp2
fi
ospeichervorhanden=$(<ramdisk/mqttspeichervorhanden)
if (( ospeichervorhanden != speichervorhanden )); then
	mosquitto_pub -t openWB/housebattery/boolhousebatteryconfigured -r -m "$speichervorhanden"
	echo $speichervorhanden > ramdisk/mqttspeichervorhanden
fi
olp1name=$(<ramdisk/mqttlp1name)
if [[ "$olp1name" != "$lp1name" ]]; then
	mosquitto_pub -t openWB/lp1/strchargepointname -r -m "$lp1name"
	echo $lp1name > ramdisk/mqttlp1name
fi
olp2name=$(<ramdisk/mqttlp2name)
if [[ "$olp2name" != "$lp2name" ]]; then
	mosquitto_pub -t openWB/lp2/strchargepointname -r -m "$lp2name"
	echo $lp2name > ramdisk/mqttlp2name
fi
olp3name=$(<ramdisk/mqttlp3name)
if [[ "$olp3name" != "$lp3name" ]]; then
	mosquitto_pub -t openWB/lp3/strchargepointname -r -m "$lp3name"
	echo $lp3name > ramdisk/mqttlp3name
fi
ozielladenaktivlp1=$(<ramdisk/mqttzielladenaktivlp1)
if [[ "$ozielladenaktivlp1" != "$zielladenaktivlp1" ]]; then
	mosquitto_pub -t openWB/lp1/boolfinishattimechargeactive -r -m "$zielladenaktivlp1"
	echo $zielladenaktivlp1 > ramdisk/mqttzielladenaktivlp1
fi
onachtladen=$(<ramdisk/mqttnachtladen)
if [[ "$onachtladen" != "$nachtladen" ]]; then
	mosquitto_pub -t openWB/lp1/boolchargeatnight -r -m "$nachtladen"
	echo $nachtladen > ramdisk/mqttnachtladen
fi
onachtladens1=$(<ramdisk/mqttnachtladens1)
if [[ "$onachtladens1" != "$nachtladens1" ]]; then
	mosquitto_pub -t openWB/lp2/boolchargeatnight -r -m "$nachtladens1"
	echo $nachtladens1 > ramdisk/mqttnachtladens1
fi
onlakt_sofort=$(<ramdisk/mqttnlakt_sofort)
if [[ "$onlakt_sofort" != "$nlakt_sofort" ]]; then
	mosquitto_pub -t openWB/boolchargeatnight_direct -r -m "$nlakt_sofort"
	echo $nlakt_sofort > ramdisk/mqttnlakt_sofort
fi
onlakt_nurpv=$(<ramdisk/mqttnlakt_nurpv)
if [[ "$onlakt_nurpv" != "$nlakt_nurpv" ]]; then
	mosquitto_pub -t openWB/boolchargeatnight_nurpv -r -m "$nlakt_nurpv"
	echo $nlakt_nurpv > ramdisk/mqttnlakt_nurpv
fi
onlakt_minpv=$(<ramdisk/mqttnlakt_minpv)
if [[ "$onlakt_minpv" != "$nlakt_minpv" ]]; then
	mosquitto_pub -t openWB/boolchargeatnight_minpv -r -m "$nlakt_minpv"
	echo $nlakt_minpv > ramdisk/mqttnlakt_minpv
fi

onlakt_standby=$(<ramdisk/mqttnlakt_sofort)
if [[ "$onlakt_standby" != "$nlakt_standby" ]]; then
	mosquitto_pub -t openWB/boolchargeatnight_standby -r -m "$nlakt_standby"
	echo $nlakt_standby > ramdisk/mqttnlakt_standby
fi
ohausverbrauchstat=$(<ramdisk/mqtthausverbrauchstat)
if [[ "$ohausverbrauchstat" != "$hausverbrauchstat" ]]; then
	mosquitto_pub -t openWB/booldisplayhouseconsumption -r -m "$hausverbrauchstat"
	echo $hausverbrauchstat > ramdisk/mqtthausverbrauchstat
fi
oheutegeladen=$(<ramdisk/mqttheutegeladen)
if [[ "$oheutegeladen" != "$heutegeladen" ]]; then
	mosquitto_pub -t openWB/booldisplaydailycharged -r -m "$heutegeladen"
	echo $heutegeladen > ramdisk/mqttheutegeladen
fi
oevuglaettungakt=$(<ramdisk/mqttevuglaettungakt)
if [[ "$oevuglaettungakt" != "$evuglaettungakt" ]]; then
	mosquitto_pub -t openWB/boolevusmoothedactive -r -m "$evuglaettungakt"
	echo $evuglaettungakt > ramdisk/mqttevuglaettungakt
fi
ographliveam=$(<ramdisk/mqttgraphliveam)
if [[ "$ographliveam" != "$graphliveam" ]]; then
	mosquitto_pub -t openWB/boolgraphliveam -r -m "$graphliveam"
	echo $graphliveam > ramdisk/mqttgraphliveam
fi
ospeicherpvui=$(<ramdisk/mqttspeicherpvui)
if [[ "$ospeicherpvui" != "$speicherpvui" ]]; then
	mosquitto_pub -t openWB/booldisplayhousebatterypriority -r -m "$speicherpvui"
	echo $speicherpvui > ramdisk/mqttspeicherpvui
fi
oevua1=$(<ramdisk/mqttevua1)
if [[ "$oevua1" != "$evua1" ]]; then
	mosquitto_pub -t openWB/evu/Aphase1 -r -m "$evua1"
	echo $evua1 > ramdisk/mqttevua1
fi
oevua2=$(<ramdisk/mqttevua2)
if [[ "$oevua2" != "$evua2" ]]; then
	mosquitto_pub -t openWB/evu/Aphase2 -r -m "$evua2"
	echo $evua2 > ramdisk/mqttevua2
fi
oevua3=$(<ramdisk/mqttevua3)
if [[ "$oevua3" != "$evua3" ]]; then
	mosquitto_pub -t openWB/evu/Aphase3 -r -m "$evua3"
	echo $evua3 > ramdisk/mqttevua3
fi

}
