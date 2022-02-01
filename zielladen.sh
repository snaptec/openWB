#!/bin/bash

ziellademodus(){

	#verbleibende Zeit berechnen
	dateaktuell=$(date '+%Y-%m-%d %H:%M')
	epochdateaktuell=$(date -d "$dateaktuell" +"%s")
	zielladenkorrektura=$(</var/www/html/openWB/ramdisk/zielladenkorrektura)
	ladestatus=$(</var/www/html/openWB/ramdisk/ladestatus)
	epochdateziel=$(date -d "$zielladenuhrzeitlp1" +"%s")
	zeitdiff=$(( epochdateziel - epochdateaktuell ))
	minzeitdiff=$(( zeitdiff / 60 ))

	# zu ladende Menge ermitteln
	soc=$(</var/www/html/openWB/ramdisk/soc)
	zuladendersoc=$(( zielladensoclp1 - soc ))
	akkuglp1wh=$(( akkuglp1 * 1000 ))
	zuladendewh=$(( akkuglp1wh / 100 * zuladendersoc ))

	#ladeleistung ermitteln
	lademaxwh=$(( zielladenmaxalp1 * zielladenphasenlp1 * 230 ))

	wunschawh=$(( zielladenalp1 * zielladenphasenlp1 * 230 ))
	#ladezeit ermitteln
	if (( llalt > 5 )); then
		wunschawh=$(( llalt * zielladenphasenlp1 * 230 ))
	fi
	moeglichewh=$(( wunschawh / 60 * minzeitdiff ))

	openwbDebugLog "MAIN" 1 "Zielladen aktiv: $wunschawh gewünschte Lade Wh, $lademaxwh maximal mögliche Wh, $zuladendewh zu ladende Wh, $moeglichewh mögliche ladbare Wh bis Zieluhrzeit"
	diffwh=$(( zuladendewh - moeglichewh ))

	#vars
	ladungdurchziel=$(<ramdisk/ladungdurchziel)
	if (( zuladendewh <= 0 )); then
		if (( ladestatus == 1 )); then
			echo 0 > ramdisk/ladungdurchziel
			echo 0 > ramdisk/zielladenkorrektura
			sed -e "s/zielladenaktivlp1=.*/zielladenaktivlp1=0/" openwb.conf > ramdisk/openwb.conf	&& mv ramdisk/openwb.conf openwb.conf && chmod 777 openwb.conf
			runs/set-current.sh 0 m
		fi
	else
		if (( zuladendewh > moeglichewh )); then
			if (( ladestatus == 0 )); then
				runs/set-current.sh $zielladenalp1 m
				openwbDebugLog "MAIN" 1 "setzte Soctimer hoch zum Abfragen des aktuellen SoC"
				echo 20000 > /var/www/html/openWB/ramdisk/soctimer
				echo 1 > ramdisk/ladungdurchziel
				exit 0
			else
				if (( diffwh > 1000 )); then
					if test $(find /var/www/html/openWB/ramdisk/zielladenkorrektura -mmin +10); then
						zielladenkorrektura=$(( zielladenkorrektura + 1 ))
						echo $zielladenkorrektura > ramdisk/zielladenkorrektura
						zielneu=$(( zielladenalp1 + zielladenkorrektura ))
						if (( zielneu > zielladenmaxalp1)); then
							zielneu=$zielladenmaxalp1
						fi
						runs/set-current.sh $zielneu m
						exit 0
					fi
				fi
			fi
		else
			if (( ladestatus == 1 )); then
				if (( diffwh < -1000 )); then
					if test $(find /var/www/html/openWB/ramdisk/zielladenkorrektura -mmin +10); then
						zielladenkorrektura=$(( zielladenkorrektura - 1 ))
						echo $zielladenkorrektura > ramdisk/zielladenkorrektura
						zielneu=$(( zielladenalp1 + zielladenkorrektura ))
						if (( zielneu < minimalstromstaerke )); then
							zielneu=$minimalstromstaerke
						fi
						runs/set-current.sh $zielneu m
						exit 0
					fi
				fi
			fi
		fi
	fi
	if (( ladungdurchziel == 1 )); then
		exit 0
	fi
}
