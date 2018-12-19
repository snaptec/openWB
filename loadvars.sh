#!/bin/bash
loadvars(){
#Speicher werte
if [[ $speichermodul != "none" ]] ; then
	timeout 5 modules/$speichermodul/main.sh || true
	speicherleistung=$(</var/www/html/openWB/ramdisk/speicherleistung)
	speichervorhanden="1"
	echo 1 > /var/www/html/openWB/ramdisk/speichervorhanden
else
	speichervorhanden="0"
	echo 0 > /var/www/html/openWB/ramdisk/speichervorhanden
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

else
	lla1=0
	lla2=0
	lla3=0
	ladeleistung=800
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
	else
		soc1=0
	fi
	timeout 10 modules/$ladeleistungs1modul/main.sh || true
	llkwhs1=$(</var/www/html/openWB/ramdisk/llkwhs1)
	llkwhges=$(echo "$llkwhges + $llkwhs1" |bc)
	llalts1=$(cat /var/www/html/openWB/ramdisk/llsolls1)
	ladeleistungs1=$(cat /var/www/html/openWB/ramdisk/llaktuells1)
	llas11=$(cat /var/www/html/openWB/ramdisk/llas11)
	llas12=$(cat /var/www/html/openWB/ramdisk/llas12)
	llas13=$(cat /var/www/html/openWB/ramdisk/llas13)
	llas11=$(echo $llas11 | sed 's/\..*$//')
	llas12=$(echo $llas12 | sed 's/\..*$//')
	llas13=$(echo $llas13 | sed 's/\..*$//')
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
	#uberschuss zur berechnung
	wattbezugint=$(printf "%.0f\n" $wattbezug)
	uberschuss=$((wattbezugint * -1))
	if [[ $speichervorhanden == "1" ]]; then
	if [[ $speicherpveinbeziehen == "1" ]]; then
		if (( speicherleistung > 0 )); then
			uberschuss=$((uberschuss + speicherleistung))
			wattbezugint=$((wattbezugint - speicherleistung))
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
#Uhrzeit
	date=$(date)
	H=$(date +%H)
	if [[ $debug == "1" ]]; then
                date
		echo pvwatt $pvwatt ladeleistung "$ladeleistung" llalt "$llalt" nachtladen "$nachtladen" minimalA "$minimalstromstaerke" maximalA "$maximalstromstaerke"
		echo lla1 "$lla1" llas11 "$llas11" llas21 "$llas21" mindestuberschuss "$mindestuberschuss" abschaltuberschuss "$abschaltuberschuss"
		echo lla2 "$lla2" llas12 "$llas12" llas22 "$llas22" sofortll "$sofortll" wattbezug $wattbezug uberschuss $uberschuss
		echo lla3 "$lla3" llas13 "$llas13" llas23 "$llas23" soclp1 $soc soclp2 $soc1
		echo evua 1 "$evua1" 2 "$evua2" 3 "$evua3"
       	fi

}
