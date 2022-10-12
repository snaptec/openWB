#!/bin/bash
OPENWBBASEDIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"

ziellademodus(){

	#verbleibende Zeit berechnen
	dateaktuell=$(date '+%Y-%m-%d %H:%M')
	epochdateaktuell=$(date -d "$dateaktuell" +"%s")
	zielladenkorrektura=$(<"$RAMDISKDIR/zielladenkorrektura")
	ladestatus=$(<"$RAMDISKDIR/ladestatus")
	epochdateziel=$(date -d "$zielladenuhrzeitlp1" +"%s")
	zeitdiff=$(( epochdateziel - epochdateaktuell ))
	minzeitdiff=$(( zeitdiff / 60 ))
	wirkungsgrad=${wirkungsgradlp1:-100}

	# zu ladende Menge ermitteln
	soc=$(<"$RAMDISKDIR/soc")
	zuladendersoc=$(( zielladensoclp1 - soc ))
	akkuglp1wh=$(( akkuglp1 * 1000 ))
	zuladendewh=$(( akkuglp1wh * zuladendersoc / wirkungsgrad ))

	#ladeleistung ermitteln
	lademaxwh=$(( zielladenmaxalp1 * zielladenphasenlp1 * 230 ))

	wunschawh=$(( zielladenalp1 * zielladenphasenlp1 * 230 ))
	#ladezeit ermitteln
	if (( llalt > 5 )); then
		wunschawh=$(( llalt * zielladenphasenlp1 * 230 ))
	fi
	moeglichewh=$(( wunschawh * minzeitdiff / 60 ))

	openwbDebugLog "MAIN" 1 "Zielladen aktiv: $wunschawh gewünschte Lade Wh, $lademaxwh maximal mögliche Wh, $zuladendewh zu ladende Wh, $moeglichewh mögliche ladbare Wh bis Zieluhrzeit"
	diffwh=$(( zuladendewh - moeglichewh ))

	#vars
	ladungdurchziel=$(<"$RAMDISKDIR/ladungdurchziel")
	if (( zuladendewh <= 0 )); then
		if (( ladestatus == 1 )); then
			echo 0 > "$RAMDISKDIR/ladungdurchziel"
			echo 0 > "$RAMDISKDIR/zielladenkorrektura"
			sed -i 's/^\(zielladenaktivlp1=\).*/\10/' "$OPENWBBASEDIR/openwb.conf"
			"$OPENWBBASEDIR/runs/set-current.sh" 0 m
		fi
	else
		if (( zuladendewh > moeglichewh )); then
			if (( ladestatus == 0 )); then
				"$OPENWBBASEDIR/runs/set-current.sh" "$zielladenalp1" m
				openwbDebugLog "MAIN" 1 "setzte Soctimer hoch zum Abfragen des aktuellen SoC"
				echo 20000 > "$RAMDISKDIR/soctimer"
				echo 1 > "$RAMDISKDIR/ladungdurchziel"
				exit 0
			else
				if (( diffwh > 1000 )); then
					if test $(find "$RAMDISKDIR/zielladenkorrektura" -mmin +10); then
						zielladenkorrektura=$(( zielladenkorrektura + 1 ))
						echo $zielladenkorrektura > "$RAMDISKDIR/zielladenkorrektura"
						zielneu=$(( zielladenalp1 + zielladenkorrektura ))
						if (( zielneu > zielladenmaxalp1)); then
							zielneu=$zielladenmaxalp1
						fi
						"$OPENWBBASEDIR/runs/set-current.sh" "$zielneu" m
						exit 0
					fi
				fi
			fi
		else
			if (( ladestatus == 1 )); then
				if (( diffwh < -1000 )); then
					if test $(find "$RAMDISKDIR/zielladenkorrektura" -mmin +10); then
						zielladenkorrektura=$(( zielladenkorrektura - 1 ))
						echo $zielladenkorrektura > "$RAMDISKDIR/zielladenkorrektura"
						zielneu=$(( zielladenalp1 + zielladenkorrektura ))
						if (( zielneu < minimalstromstaerke )); then
							zielneu=$minimalstromstaerke
						fi
						"$OPENWBBASEDIR/runs/set-current.sh" "$zielneu" m
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
