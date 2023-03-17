#!/bin/bash
#set -e

#####
#
# File: regel.sh
#
# Copyright 2018 Kevin Wieland, David Meder-Marouelli
#
#  This file is part of openWB.
#
#     openWB is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     openWB is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with openWB.  If not, see <https://www.gnu.org/licenses/>.
#
#####
OPENWBBASEDIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

set -o pipefail
cd "$OPENWBBASEDIR"

source helperFunctions.sh

if pidof -x -o $$ "${BASH_SOURCE[0]}"
then
	openwbDebugLog "MAIN" 0 "Previous regulation loop still running. Skipping."
	exit
fi

if [ -e ramdisk/updateinprogress ] && [ -e ramdisk/bootinprogress ]; then
	updateinprogress=$(<ramdisk/updateinprogress)
	bootinprogress=$(<ramdisk/bootinprogress)
	if (( updateinprogress == "1" )); then
		openwbDebugLog "MAIN" 0 "Update in progress"
		exit 0
	elif (( bootinprogress == "1" )); then
		openwbDebugLog "MAIN" 0 "Boot in progress"
		exit 0
	fi
else
	openwbDebugLog "MAIN" 0 "Ramdisk not set up. Maybe we are still booting."
	exit 0
fi

########### Laufzeit protokolieren
startregel=$(date +%s)
function cleanup()
{
	local endregel=$(date +%s)
	local t=$((endregel-startregel))

	if [ "$t" -le "7" ] ; then   # 1..7 Ok
		openwbDebugLog "MAIN" 2 "**** Regulation loop needs $t seconds"
	elif [ "$t" -le "8" ] ; then # 8 Warning
		openwbDebugLog "MAIN" 0 "**** WARNING **** Regulation loop needs $t seconds"
	else                         # 9,10,... Fatal
		openwbDebugLog "MAIN" 0 "**** FATAL *********************************"
		openwbDebugLog "MAIN" 0 "**** FATAL Regulation loop needs $t seconds"
		openwbDebugLog "MAIN" 0 "**** FATAL *********************************"
	fi
}
trap cleanup EXIT
########### End Laufzeit protokolieren

#config file einlesen
. /var/www/html/openWB/loadconfig.sh

openwbDebugLog "MAIN" 1 "**** Regulation loop start ****"

declare -r IsFloatingNumberRegex='^-?[0-9.]+$'

if (( slavemode == 1)); then
	randomSleep=$(<ramdisk/randomSleepValue)
	if [[ -z $randomSleep ]] || [[ "${randomSleep}" == "0" ]] || ! [[ "${randomSleep}" =~ $IsFloatingNumberRegex ]]; then
		randomSleep=`shuf --random-source=/dev/urandom -i 0-3 -n 1`.`shuf --random-source=/dev/urandom -i 0-9 -n 1`
		openwbDebugLog "MAIN" 0 "slavemode=$slavemode: ramdisk/randomSleepValue missing or 0 - creating new one containing $randomSleep"
		echo "$randomSleep" > ramdisk/randomSleepValue
	fi

	openwbDebugLog "MAIN" 1 "Slave mode regulation spread: Waiting ${randomSleep}s"

	sleep "$randomSleep"

	# repeat setting of startregel as we do not want to account for the randomization sleep time
	startregel=$(date +%s)

	openwbDebugLog "MAIN" 1 "Slave mode regulation spread: Wait end"
fi

source minundpv.sh
source nurpv.sh
source auslademodus.sh
source sofortlademodus.sh
source goecheck.sh
source loadvars.sh
source graphing.sh
source nachtladen.sh
source zielladen.sh
source evsedintest.sh
source hook.sh
source u1p3p.sh
source nrgkickcheck.sh
source rfidtag.sh
source leds.sh
source slavemode.sh

date=$(date)
re='^-?[0-9]+$'
if [[ $isss == "1" ]]; then
	heartbeat=$(<ramdisk/heartbeat)
	heartbeat=$((heartbeat+10))
	echo $heartbeat > ramdisk/heartbeat
	mosquitto_pub -r -t "openWB/system/Uptime" -m "$(uptime)"
	mosquitto_pub -r -t "openWB/system/Timestamp" -m "$(date +%s)"
	mosquitto_pub -r -t "openWB/system/Date" -m "$(date)"
	exit 0
fi

#doppelte Ausfuehrungsgeschwindigkeit
if [[ $dspeed == "1" ]]; then
	if [ -e ramdisk/5sec ]; then
		sleep 5 && ./regel.sh >> /var/log/openWB.log 2>&1 &
		rm ramdisk/5sec
	else
		echo 0 > ramdisk/5sec
	fi
fi
if [[ $dspeed == "2" ]]; then

	if [ -e ramdisk/5sec ]; then
		rm ramdisk/5sec
		exit 0
	else
		echo 0 > ramdisk/5sec
	fi
fi

# process autolock
./processautolock.sh &

#ladelog ausfuehren
./ladelog.sh &
graphtimer=$(<ramdisk/graphtimer)
if (( graphtimer < 5 )); then
	graphtimer=$((graphtimer+1))
	echo $graphtimer > ramdisk/graphtimer
else
	graphtimer=0
	echo $graphtimer > ramdisk/graphtimer
fi
#######################################

if (( displayaktiv == 1 )); then
	execdisplay=$(<ramdisk/execdisplay)
	if (( execdisplay == 1 )); then
		export DISPLAY=:0 && xset s "$displaysleep" && xset dpms "$displaysleep" "$displaysleep" "$displaysleep"
		echo 0 > ramdisk/execdisplay
	fi
fi


#######################################
# check rfid
#moved in loadvars

#goe mobility check
goecheck

# nrgkick mobility check
nrgkickcheck

#load charging vars
startloadvars=$(date +%s)
loadvars
endloadvars=$(date +%s)
timeloadvars=$((endloadvars-startloadvars))
openwbDebugLog "MAIN" 1 "Zeit zum abfragen aller Werte $timeloadvars Sekunden"

if (( u1p3paktiv == 1 )); then
	blockall=$(<ramdisk/blockall)
	if (( blockall == 1 )); then
		openwbDebugLog "MAIN" 1 "Phasen Umschaltung noch aktiv... beende"
		exit 0
	fi
fi
if (( lp1enabled == 0)); then
	if (( ladeleistunglp1 > 100 )) || (( llalt > 0 )); then
		runs/set-current.sh 0 m
	fi
fi
if (( lp2enabled == 0)); then
	if (( ladeleistunglp2 > 100 )) || (( llalts1 > 0 )); then
		runs/set-current.sh 0 s1
	fi
fi
if (( lp3enabled == 0)); then
	if (( ladeleistunglp3 > 100 )) || (( llalts2 > 0 )); then
		runs/set-current.sh 0 s2
	fi
fi
if (( lp4enabled == 0)); then
	if (( ladeleistunglp4 > 100 )) || (( llaltlp4 > 0 )); then
		runs/set-current.sh 0 lp4
	fi
fi
if (( lp5enabled == 0)); then
	if (( ladeleistunglp5 > 100 )) || (( llaltlp5 > 0 )); then
		runs/set-current.sh 0 lp5
	fi
fi
if (( lp6enabled == 0)); then
	if (( ladeleistunglp6 > 100 )) || (( llaltlp6 > 0 )); then
		runs/set-current.sh 0 lp6
	fi
fi
if (( lp7enabled == 0)); then
	if (( ladeleistunglp7 > 100 )) || (( llaltlp7 > 0 )); then
		runs/set-current.sh 0 lp7
	fi
fi
if (( lp8enabled == 0)); then
	if (( ladeleistunglp8 > 100 )) || (( llaltlp8 > 0 )); then
		runs/set-current.sh 0 lp8
	fi
fi

#EVSE DIN Modbus test
evsedintest

#u1p3p switch
u1p3pswitch

#hooks - externe geraete
hook

#Graphing
graphing

if (( cpunterbrechunglp1 == 1 )); then
	if (( plugstat == 1 )) && (( lp1enabled == 1 )); then
		if (( llalt > 5 )); then
			if (( ladeleistung < 100 )); then
				cpulp1waraktiv=$(<ramdisk/cpulp1waraktiv)
				cpulp1counter=$(<ramdisk/cpulp1counter)
				if (( cpulp1counter > 5 )); then
					if (( cpulp1waraktiv == 0 )); then
						openwbDebugLog "MAIN" 0 "CP Unterbrechung an LP1 wird durchgeführt"
						if [[ $evsecon == "simpleevsewifi" ]]; then
							curl --silent --connect-timeout "$evsewifitimeoutlp1" -s "http://$evsewifiiplp1/interruptCp" > /dev/null
						elif [[ $evsecon == "ipevse" ]]; then
							openwbDebugLog "MAIN" 0 "Dauer der Unterbrechung: ${cpunterbrechungdauerlp1}s"
							python runs/cpuremote.py -a "$evseiplp1" -i 4 -d "$cpunterbrechungdauerlp1"
						elif [[ $evsecon == "extopenwb" ]]; then
							mosquitto_pub -r -t openWB/set/isss/Cpulp1 -h $chargep1ip -m "1"
						else
							openwbDebugLog "MAIN" 0 "Dauer der Unterbrechung: ${cpunterbrechungdauerlp1}s"
							sudo python runs/cpulp1.py -d "$cpunterbrechungdauerlp1"
						fi
						echo 1 > ramdisk/cpulp1waraktiv
						date +%s > ramdisk/cpulp1timestamp # Timestamp in epoch der CP Unterbrechung
					fi
				else
					cpulp1counter=$((cpulp1counter+1))
					echo $cpulp1counter > ramdisk/cpulp1counter
				fi
			else
				echo 0 > ramdisk/cpulp1waraktiv
				echo 0 > ramdisk/cpulp1counter
			fi
		fi
	else
		echo 0 > ramdisk/cpulp1waraktiv
		echo 0 > ramdisk/cpulp1counter
	fi
fi

if (( cpunterbrechunglp2 == 1 )); then
	if (( plugstatlp2 == 1 )) && (( lp2enabled == 1 )); then
		if (( llalts1 > 5 )); then
			if (( ladeleistunglp2 < 100 )); then
				cpulp2waraktiv=$(<ramdisk/cpulp2waraktiv)
				cpulp2counter=$(<ramdisk/cpulp2counter)
				if (( cpulp2counter > 5 )); then
					if (( cpulp2waraktiv == 0 )); then
						openwbDebugLog "MAIN" 0 "CP Unterbrechung an LP2 wird durchgeführt"
						if [[ $evsecons1 == "simpleevsewifi" ]]; then
							curl --silent --connect-timeout "$evsewifitimeoutlp2" -s "http://$evsewifiiplp2/interruptCp" > /dev/null
						elif [[ $evsecons1 == "ipevse" ]]; then
							openwbDebugLog "MAIN" 0 "Dauer der Unterbrechung: ${cpunterbrechungdauerlp2}s"
							python runs/cpuremote.py -a "$evseiplp2" -i 7 -d "$cpunterbrechungdauerlp2"
						elif [[ $evsecons1 == "extopenwb" ]]; then
							mosquitto_pub -r -t openWB/set/isss/Cpulp1 -h $chargep2ip -m "1"
						else
							openwbDebugLog "MAIN" 0 "Dauer der Unterbrechung: ${cpunterbrechungdauerlp2}s"
							sudo python runs/cpulp2.py -d "$cpunterbrechungdauerlp2"
						fi
						echo 1 > ramdisk/cpulp2waraktiv
						date +%s > ramdisk/cpulp2timestamp # Timestamp in epoch der CP Unterbrechung
					fi
				else
					cpulp2counter=$((cpulp2counter+1))
					echo $cpulp2counter > ramdisk/cpulp2counter
				fi
			else
				echo 0 > ramdisk/cpulp2waraktiv
				echo 0 > ramdisk/cpulp2counter
			fi
		fi
	else
		echo 0 > ramdisk/cpulp2waraktiv
		echo 0 > ramdisk/cpulp2counter
	fi
fi

if [[ $dspeed == "3" ]]; then
	if [ -e ramdisk/5sec ]; then
		regeltimer=$(<ramdisk/5sec)
		if (( regeltimer < 5 )); then
			regeltimer=$((regeltimer+1))
			echo $regeltimer > ramdisk/5sec
			exit 0
		else
			regeltimer=0
			echo $regeltimer > ramdisk/5sec
		fi
	else
		echo 0 > ramdisk/5sec
	fi
fi

if (( ledsakt == 1 )); then
	ledsteuerung
fi

#Prüft ob der RSE (Rundsteuerempfängerkontakt) geschlossen ist, wenn ja wird die Ladung pausiert.
if (( rseenabled == 1 )); then
	rsestatus=$(<ramdisk/rsestatus)
	rseaktiv=$(<ramdisk/rseaktiv)
	if (( rsestatus == 1 )); then
		echo "RSE Kontakt aktiv, pausiere Ladung" > ramdisk/lastregelungaktiv
		if (( rseaktiv == 0 )); then
			openwbDebugLog "CHARGESTAT" 0 "RSE Kontakt aktiviert, ändere Lademodus auf Stop"
			echo "$lademodus" > ramdisk/rseoldlademodus
			echo 3 > ramdisk/lademodus
			mosquitto_pub -r -t openWB/global/ChargeMode -m "3"
			echo 1 > ramdisk/rseaktiv
		fi
	else
		if (( rseaktiv == 1 )); then
			openwbDebugLog "CHARGESTAT" 0 "RSE Kontakt deaktiviert, setze auf alten Lademodus zurück"
			rselademodus=$(<ramdisk/rseoldlademodus)
			echo "$rselademodus" > ramdisk/lademodus
			mosquitto_pub -r -t openWB/global/ChargeMode -m "$rselademodus"
			echo 0 > ramdisk/rseaktiv
		fi
	fi
fi

#evse modbus check
evsemodbustimer=$(<ramdisk/evsemodbustimer)
if (( evsemodbustimer < 30 )); then
	evsemodbustimer=$((evsemodbustimer+1))
	echo $evsemodbustimer > ramdisk/evsemodbustimer
else
	evsemodbustimer=0
	echo $evsemodbustimer > ramdisk/evsemodbustimer
	evsemodbuscheck
fi

# Slave Mode, openWB als Ladepunkt nutzen

if (( slavemode == 1 )); then
	openwbisslave
fi

#Lademodus 3 == Aus
if (( lademodus == 3 )); then
	auslademodus
fi

#loadsharing check
if [[ $loadsharinglp12 == "1" ]]; then
	if (( loadsharingalp12 == 16 )); then
		agrenze=8
		aagrenze=16
		if (( current > 16 )); then
			current=16
		fi
	else
		agrenze=16
		aagrenze=32
	fi
	tcurrent=$(( llalt + llalts1 ))
	if (( tcurrent > aagrenze )); then
		#detect charging cars
		if (( lla1 > 1 )); then
			lp1c=1
			if (( lla2 > 1 )); then
				lp1c=2
			fi
		else
			lp1c=0
		fi
		if (( llas11 > 1 )); then
			lp2c=1
			if (( llas12 > 1 )); then
				lp2c=2
			fi
		else
			lp2c=0
		fi
		chargingphases=$(( lp1c + lp2c ))
		if (( chargingphases > 2 )); then
			runs/set-current.sh "$agrenze" all
			openwbDebugLog "CHARGESTAT" 0 "Alle Ladepunkte, Loadsharing LP1-LP2 aktiv. Setze Ladestromstärke auf $agrenze"
			exit 0
		fi
	fi
fi


#########################################
#Regelautomatiken

if (( zielladenaktivlp1 == 1 )); then
	ziellademodus
fi

####################
# Nachtladung bzw. Ladung bis SOC x% nachts von x bis x Uhr
prenachtlademodus

#######################
#Ladestromstarke berechnen
anzahlphasen=$(</var/www/html/openWB/ramdisk/anzahlphasen)
if ((anzahlphasen > 9)); then
	anzahlphasen=1
fi
llphasentest=3
openwbDebugLog "PV" 0 "Alte Anzahl genutzter Phasen= $anzahlphasen"
#Anzahl genutzter Phasen ermitteln, wenn ladestrom kleiner 3 (nicht vorhanden) nutze den letzten bekannten wert
if ((llalt > 3)); then
	anzahlphasen=0
	if ((lla1 >= llphasentest)); then
		anzahlphasen=$((anzahlphasen + 1))
	fi
	if ((lla2 >= llphasentest)); then
		anzahlphasen=$((anzahlphasen + 1))
	fi
	if ((lla3 >= llphasentest)); then
		anzahlphasen=$((anzahlphasen + 1))
	fi
	echo "$anzahlphasen" >/var/www/html/openWB/ramdisk/anzahlphasen
	echo "$anzahlphasen" >/var/www/html/openWB/ramdisk/lp1anzahlphasen
	openwbDebugLog "PV" 0 "LP1 Anzahl Phasen während Ladung= $anzahlphasen"
else
	if ((plugstat == 1)) && ((lp1enabled == 1)); then
		if [ ! -f /var/www/html/openWB/ramdisk/anzahlphasen ]; then
			echo 1 >/var/www/html/openWB/ramdisk/anzahlphasen
		fi
		if ((u1p3paktiv == 1)); then
			anzahlphasen=$(</var/www/html/openWB/ramdisk/u1p3pstat)
		else
			if [ -f /var/www/html/openWB/ramdisk/lp1anzahlphasen ]; then
				anzahlphasen=$(</var/www/html/openWB/ramdisk/lp1anzahlphasen)
			else
				anzahlphasen=$(</var/www/html/openWB/ramdisk/anzahlphasen)
			fi
		fi
	else
		anzahlphasen=0
	fi
	openwbDebugLog "PV" 0 "LP1 Anzahl Phasen während keiner Ladung= $anzahlphasen"
fi
if ((lastmanagement == 1)); then
	if ((llas11 > 3)); then
		lp2anzahlphasen=0
		if ((llas11 >= llphasentest)); then
			anzahlphasen=$((anzahlphasen + 1 ))
			lp2anzahlphasen=$((lp2anzahlphasen + 1 ))
		fi
		if ((llas12 >= llphasentest)); then
			anzahlphasen=$((anzahlphasen + 1 ))
			lp2anzahlphasen=$((lp2anzahlphasen + 1 ))
		fi
		if ((llas13 >= llphasentest)); then
			anzahlphasen=$((anzahlphasen + 1 ))
			lp2anzahlphasen=$((lp2anzahlphasen + 1 ))
		fi
		echo "$anzahlphasen" >/var/www/html/openWB/ramdisk/anzahlphasen
		echo "$lp2anzahlphasen" >/var/www/html/openWB/ramdisk/lp2anzahlphasen
		openwbDebugLog "PV" 0 "LP2 Anzahl Phasen während Ladung= $lp2anzahlphasen"
	else
		if ((plugstatlp2 == 1)) && ((lp2enabled == 1)); then
			if [ ! -f /var/www/html/openWB/ramdisk/anzahlphasen ]; then
				echo 1 >/var/www/html/openWB/ramdisk/anzahlphasen
			fi
			if ((u1p3plp2aktiv == 1)); then
				lp2anzahlphasen=$(</var/www/html/openWB/ramdisk/u1p3pstat)
				anzahlphasen=$((lp2anzahlphasen + anzahlphasen))
			else
				if [ ! -f /var/www/html/openWB/ramdisk/lp2anzahlphasen ]; then
					echo 1 >/var/www/html/openWB/ramdisk/lp2anzahlphasen
					anzahlphasen=$((anzahlphasen + 1 ))
				else
					lp2anzahlphasen=$(</var/www/html/openWB/ramdisk/lp2anzahlphasen)
					anzahlphasen=$((lp2anzahlphasen + anzahlphasen))
				fi
			fi
		else
			lp2anzahlphasen=0
		fi
		openwbDebugLog "PV" 0 "LP2 Anzahl Phasen während keiner Ladung= $lp2anzahlphasen"
	fi
fi
if ((lastmanagements2 == 1)); then
	if ((llas21 > 3)); then
		if ((llas21 >= llphasentest)); then
			anzahlphasen=$((anzahlphasen + 1 ))
		fi
		if ((llas22 >= llphasentest)); then
			anzahlphasen=$((anzahlphasen + 1 ))
		fi
		if ((llas23 >= llphasentest)); then
			anzahlphasen=$((anzahlphasen + 1 ))
		fi
		echo "$anzahlphasen" >/var/www/html/openWB/ramdisk/anzahlphasen
	fi
fi
if ((anzahlphasen < 1)) || ((anzahlphasen > 24)); then
	openwbDebugLog "PV" 1 "Ungueltige Anzahl Phasen: $anzahlphasen, setze auf '1'"
	anzahlphasen=1
	echo "$anzahlphasen" >/var/www/html/openWB/ramdisk/anzahlphasen
fi
openwbDebugLog "PV" 0 "Gesamt Anzahl Phasen= $anzahlphasen"

########################
# Sofort Laden
if (( lademodus == 0 )); then
	sofortlademodus
fi

########################
# Berechnung für PV Regelung
if [[ $nurpv70dynact == "1" ]]; then
	nurpv70status=$(<ramdisk/nurpv70dynstatus)
	if [[ $nurpv70status == "1" ]]; then
		uberschuss=$((uberschuss - nurpv70dynw))
		# Schwelle zum Beginn der Ladung
		mindestuberschuss=0
		# Schwelle zum Beenden der Ladung
		abschaltuberschuss=-1500
		#abschaltuberschuss=$((minimalapv * 230 * anzahlphasen))
		openwbDebugLog "MAIN" 1 "PV 70% aktiv! derzeit genutzter Überschuss $uberschuss"
		openwbDebugLog "PV" 0 "70% Grenze aktiv. Alter Überschuss: $((uberschuss + nurpv70dynw)), Neuer verfügbarer Uberschuss: $uberschuss"
	fi
fi

mindestuberschussphasen=$((mindestuberschuss * anzahlphasen))
wattkombiniert=$((ladeleistung + uberschuss))
#PV Regelmodus
if [[ $pvbezugeinspeisung == "0" ]]; then
	pvregelungm="0"
	schaltschwelle=$(echo "(230*$anzahlphasen)" | bc)
fi
if [[ $pvbezugeinspeisung == "1" ]]; then
	pvregelungm=$(echo "(230*$anzahlphasen*-1)" | bc)
	schaltschwelle="0"
fi
if [[ $pvbezugeinspeisung == "2" ]]; then
	pvregelungm=$offsetpv
	schaltschwelle=$((schaltschwelle + offsetpv))
fi
openwbDebugLog "PV" 0 "Schaltschwelle: $schaltschwelle, zum runterregeln: $pvregelungm"
# Debug Ausgaben
openwbDebugLog "MAIN" 1 "anzahlphasen $anzahlphasen"
openwbDebugLog "MAIN" 2 "uberschuss $uberschuss wattbezug $wattbezug ladestatus $ladestatus llsoll $llalt pvwatt $pvwatt mindestuberschussphasen $mindestuberschussphasen wattkombiniert $wattkombiniert schaltschwelle $schaltschwelle"
########################
#Min Ladung + PV Uberschussregelung lademodus 1
if (( lademodus == 1 )); then
	minundpvlademodus
fi
########################
#NUR PV Uberschussregelung lademodus 2
# wenn evse aus und $mindestuberschuss vorhanden, starte evse mit 6A Ladestromstaerke (1320 - 3960 Watt je nach Anzahl Phasen)
if (( lademodus == 2 )); then
	nurpvlademodus
fi

#Lademodus 4 == SemiAus
if (( lademodus == 4 )); then
	semiauslademodus
fi
