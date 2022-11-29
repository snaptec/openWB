#!/bin/bash

u1p3pswitch() {

	if ((u1p3paktiv == 1)); then
		u1p3pstat=$(<ramdisk/u1p3pstat)
		nachtladenstate=$(<ramdisk/nachtladenstate)       # "Nachtladen" LP1
		nachtladen2state=$(<ramdisk/nachtladen2state)     # "Morgensladen" LP1
		nachtladenstates1=$(<ramdisk/nachtladenstates1)   # "Nachtladen" LP2
		nachtladen2states1=$(<ramdisk/nachtladen2states1) # "Morgensladen" LP2
		if [ -z "$u1p3schaltparam" ]; then
			u1p3schaltparam=8
		fi
		uhwaittime=$((u1p3schaltparam * 60))
		urwaittime=$(((16 - u1p3schaltparam) * 60))
		openwbDebugLog "MAIN" 1 "automatische Umschaltung aktiv"
		openwbDebugLog "MAIN" 1 "Timing Umschaltung: $uhwaittime / $urwaittime"
		if ((ladestatus == 0)); then
			if ((nachtladenstate == 1)) || ((nachtladen2state == 1)) || ((nachtladenstates1 == 1)) || ((nachtladen2states1 == 1)); then
				if ((u1p3pstat != u1p3pnl)); then
					openwbDebugLog "MAIN" 1 "Nachtladen derzeit $u1p3pstat Phasen, auf $u1p3pnl konfiguriert, aendere..."
					if ((u1p3pnl == 3)); then
						runs/u1p3pcheck.sh 3
					else
						runs/u1p3pcheck.sh 1
					fi
					openwbDebugLog "MAIN" 1 "auf $u1p3pnl Phasen geaendert"
				fi
			else
				if ((lademodus == 0)); then
					if ((u1p3pstat != u1p3psofort)); then
						openwbDebugLog "MAIN" 1 "Sofortladen derzeit $u1p3pstat Phasen, auf $u1p3psofort konfiguriert, aendere..."
						if ((u1p3psofort == 3)); then
							runs/u1p3pcheck.sh 3
						else
							runs/u1p3pcheck.sh 1
						fi
						openwbDebugLog "MAIN" 1 "auf $u1p3psofort Phasen geaendert"
					fi
				fi
				if ((lademodus == 1)); then
					if ((u1p3pstat != u1p3pminundpv)); then
						if ((u1p3pminundpv == 4)); then
							if ((u1p3pstat == 0)); then
								runs/u1p3pcheck.sh 1
							fi
							if ((u1p3pstat == 3)); then
								urcounter=$(</var/www/html/openWB/ramdisk/urcounter)
								if ((urcounter < urwaittime)); then
									if ((urcounter < urwaittime - 60)); then
										urcounter=$((urwaittime - 60))
									fi
									urcounter=$((urcounter + 10))
									echo $urcounter >/var/www/html/openWB/ramdisk/urcounter
								else
									runs/u1p3pcheck.sh 1
									openwbDebugLog "MAIN" 1 "Min PV Laden derzeit $u1p3pstat Phasen, auf 1 Nur PV konfiguriert, aendere..."
									echo 0 >/var/www/html/openWB/ramdisk/urcounter
								fi
							fi
						else
							openwbDebugLog "MAIN" 1 "Min PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pminundpv konfiguriert, aendere..."
							if ((u1p3pnurpv == 3)); then
								runs/u1p3pcheck.sh 3
							else
								runs/u1p3pcheck.sh 1
							fi
							openwbDebugLog "MAIN" 1 "auf $u1p3pminundpv Phasen geaendert"
						fi
					fi
				fi
				if ((lademodus == 2)); then
					if ((u1p3pstat != u1p3pnurpv)); then
						if ((u1p3pnurpv == 4)); then
							if ((u1p3pstat == 0)); then
								runs/u1p3pcheck.sh 1
							fi
							if ((u1p3pstat == 3)); then
								urcounter=$(</var/www/html/openWB/ramdisk/urcounter)
								if ((urcounter < urwaittime)); then
									if ((urcounter < urwaittime - 60)); then
										urcounter=$((urwaittime - 60))
									fi
									urcounter=$((urcounter + 10))
									echo $urcounter >/var/www/html/openWB/ramdisk/urcounter
								else
									runs/u1p3pcheck.sh 1
									openwbDebugLog "MAIN" 1 "Nur PV Laden derzeit $u1p3pstat Phasen, auf 1 Nur PV konfiguriert, aendere..."
									echo 0 >/var/www/html/openWB/ramdisk/urcounter
								fi
							fi
						else
							openwbDebugLog "MAIN" 1 "Nur PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pnurpv konfiguriert, aendere..."
							if ((u1p3pnurpv == 3)); then
								runs/u1p3pcheck.sh 3
							else
								runs/u1p3pcheck.sh 1
							fi
							openwbDebugLog "MAIN" 1 "auf $u1p3pnurpv Phasen geaendert"
						fi
					fi
				fi
				if ((lademodus == 4)); then
					if ((u1p3pstat != u1p3pstandby)); then
						openwbDebugLog "MAIN" 1 "Standby Laden derzeit $u1p3pstat Phasen, auf $u1p3pstandby konfiguriert, aendere..."
						if ((u1p3pstandby == 3)); then
							runs/u1p3pcheck.sh 3
						else
							runs/u1p3pcheck.sh 1
						fi
						openwbDebugLog "MAIN" 1 "auf $u1p3pstandby Phasen geaendert"
					fi
				fi
				if ((lademodus == 3)); then
					if ((u1p3pstat != u1p3pstandby)); then
						openwbDebugLog "MAIN" 1 "Stop Laden derzeit $u1p3pstat Phasen, auf $u1p3pstandby konfiguriert, aendere..."
						if ((u1p3pstandby == 3)); then
							runs/u1p3pcheck.sh 3
						else
							runs/u1p3pcheck.sh 1
						fi
						openwbDebugLog "MAIN" 1 "auf $u1p3pstandby Phasen geaendert"
					fi
				fi
			fi
		else
			if ((nachtladenstate == 1)) || ((nachtladen2state == 1)) || ((nachtladenstates1 == 1)) || ((nachtladen2states1 == 1)); then
				if ((u1p3pstat != u1p3pnl)); then
					openwbDebugLog "MAIN" 1 "Nachtladen derzeit $u1p3pstat Phasen, auf $u1p3pnl konfiguriert, unterbreche Ladung und aendere..."
					echo 1 >ramdisk/blockall
					runs/u1p3pcheck.sh stop
					sleep 5
					if ((u1p3pnl == 3)); then
						runs/u1p3pcheck.sh 3
					else
						runs/u1p3pcheck.sh 1
					fi
					sleep 1
					runs/u1p3pcheck.sh start
					echo 0 >ramdisk/blockall
					openwbDebugLog "MAIN" 1 "auf $u1p3pnl Phasen geaendert"
				fi
			else
				if ((lademodus == 0)); then
					if ((u1p3pstat != u1p3psofort)); then
						openwbDebugLog "MAIN" 1 "Sofortladen derzeit $u1p3pstat Phasen, auf $u1p3psofort konfiguriert, unterbreche Ladung und aendere..."
						echo 1 >ramdisk/blockall
						runs/u1p3pcheck.sh stop
						sleep 5
						if ((u1p3psofort == 3)); then
							runs/u1p3pcheck.sh 3
						else
							runs/u1p3pcheck.sh 1
						fi
						sleep 1
						runs/u1p3pcheck.sh start
						echo 0 >ramdisk/blockall
						openwbDebugLog "MAIN" 1 "auf $u1p3psofort Phasen geaendert"
					fi
				fi
				if ((lademodus == 1)); then
					if ((u1p3pstat != u1p3pminundpv)); then
						if ((u1p3pminundpv == 4)); then
							oldll=$(<ramdisk/llsoll)
							if ((u1p3pstat == 1)); then
								if [[ $schieflastaktiv == "1" ]]; then
									maximalstromstaerke=$schieflastmaxa
								fi
								if ((ladeleistung < 100)); then
									if ((uberschuss > ((3 * mindestuberschuss) + 1000))); then
										openwbDebugLog "MAIN" 1 "Min PV Laden derzeit $u1p3pstat Phasen, auf MinPV Automatik konfiguriert, aendere auf 3 Phasen da viel Überschuss vorhanden..."
										echo 1 >ramdisk/blockall
										runs/u1p3pcheck.sh stop
										sleep 8
										runs/u1p3pcheck.sh 3
										sleep 20
										runs/u1p3pcheck.sh startslow
										(sleep 25 && echo 0 >ramdisk/blockall) &
										openwbDebugLog "MAIN" 1 "auf 3 Phasen MinPV Automatik geaendert"
									fi
								fi
								if ((oldll == maximalstromstaerke)); then
									uhcounter=$(</var/www/html/openWB/ramdisk/uhcounter)
									if ((uhcounter < uhwaittime)); then
										if ((maximalstromstaerke == 16)); then
											if ((uberschuss > 500)); then
												uhcounter=$((uhcounter + 10))
												echo $uhcounter >/var/www/html/openWB/ramdisk/uhcounter
												openwbDebugLog "MAIN" 1 "Umschaltcounter Erhoehung auf $uhcounter erhoeht fuer Min PV Automatik Phasenumschaltung, genug uberschuss fuer 3 Phasen Ladung"
											else
												openwbDebugLog "MAIN" 1 "Umschaltcounter nicht erhöht fuer Min PV Automatik Phasenumschaltung, fehlender uberschuss fuer 3 Phasen Ladung"
											fi
										else
											uhcounter=$((uhcounter + 10))
											echo $uhcounter >/var/www/html/openWB/ramdisk/uhcounter
											openwbDebugLog "MAIN" 1 "Umschaltcounter Erhoehung auf $uhcounter erhoeht fuer Min PV Automatik Phasenumschaltung"
										fi
									else
										openwbDebugLog "MAIN" 1 "Min PV Laden derzeit $u1p3pstat Phasen, auf MinPV Automatik konfiguriert, unterbreche Ladung und  aendere auf 3 Phasen..."
										echo 1 >ramdisk/blockall
										runs/u1p3pcheck.sh stop
										sleep 8
										runs/u1p3pcheck.sh 3
										sleep 20
										runs/u1p3pcheck.sh startslow
										(sleep 25 && echo 0 >ramdisk/blockall) &
										openwbDebugLog "MAIN" 1 "auf 3 Phasen MinPV Automatik geaendert"
										echo 0 >/var/www/html/openWB/ramdisk/uhcounter
									fi
								else
									echo 0 >/var/www/html/openWB/ramdisk/uhcounter
								fi
							else
								if ((ladeleistung < 100)); then
									if ((uberschuss < (3 * mindestuberschuss))); then
										echo 0 >/var/www/html/openWB/ramdisk/urcounter
										echo 1 >ramdisk/blockall
										runs/u1p3pcheck.sh stop
										sleep 8
										runs/u1p3pcheck.sh 1
										sleep 20
										runs/u1p3pcheck.sh startslow
										(sleep 25 && echo 0 >ramdisk/blockall) &
										openwbDebugLog "MAIN" 1 "auf 1 Phasen MinPV Automatik geaendert da geringerer Überschuss"
									fi
								fi
								if ((oldll == minimalampv)) && ((ladeleistung > 100)); then
									urcounter=$(</var/www/html/openWB/ramdisk/urcounter)
									if ((urcounter < urwaittime)); then
										urcounter=$((urcounter + 10))
										echo $urcounter >/var/www/html/openWB/ramdisk/urcounter
										openwbDebugLog "MAIN" 1 "Umschaltcounter Reduzierung auf $urcounter erhoeht fuer Min PV Automatik Phasenumschaltung"
									else
										echo 0 >/var/www/html/openWB/ramdisk/urcounter
										echo 1 >ramdisk/blockall
										runs/u1p3pcheck.sh stop
										sleep 8
										runs/u1p3pcheck.sh 1
										sleep 20
										runs/u1p3pcheck.sh startslow
										(sleep 25 && echo 0 >ramdisk/blockall) &
										openwbDebugLog "MAIN" 1 "auf 1 Phasen MinPV Automatik geaendert"
									fi
								else
									echo 0 >/var/www/html/openWB/ramdisk/urcounter
								fi
							fi
						else
							openwbDebugLog "MAIN" 1 "Min PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pminundpv konfiguriert, unterbreche Ladung und  aendere..."
							echo 1 >ramdisk/blockall
							runs/u1p3pcheck.sh stop
							sleep 5
							if ((u1p3pminundpv == 3)); then
								runs/u1p3pcheck.sh 3
							else
								runs/u1p3pcheck.sh 1
							fi
							sleep 1
							runs/u1p3pcheck.sh start
							echo 0 >ramdisk/blockall
							openwbDebugLog "MAIN" 1 "auf $u1p3pminundpv Phasen geaendert"
						fi
					fi
				fi
				if ((lademodus == 2)); then
					if ((u1p3pstat != u1p3pnurpv)); then
						if ((u1p3pnurpv == 4)); then
							oldll=$(<ramdisk/llsoll)
							if ((u1p3pstat == 1)); then
								if [[ $schieflastaktiv == "1" ]]; then
									maximalstromstaerke=$schieflastmaxa
								fi
								if ((ladeleistung < 100)); then
									if ((uberschuss > ((3 * mindestuberschuss) + 1000))); then
										openwbDebugLog "MAIN" 1 "Nur PV Laden derzeit $u1p3pstat Phasen, auf NurPV Automatik konfiguriert, aendere auf 3 Phasen da viel Überschuss vorhanden..."
										echo 1 >ramdisk/blockall
										runs/u1p3pcheck.sh stop
										sleep 8
										runs/u1p3pcheck.sh 3
										sleep 20
										runs/u1p3pcheck.sh startslow
										(sleep 25 && echo 0 >ramdisk/blockall) &
										openwbDebugLog "MAIN" 1 "auf 3 Phasen NurPV Automatik geaendert"
									fi
								fi
								if ((oldll == maximalstromstaerke)); then
									uhcounter=$(</var/www/html/openWB/ramdisk/uhcounter)
									if ((uhcounter < uhwaittime)); then
										uhcounter=$((uhcounter + 10))
										echo $uhcounter >/var/www/html/openWB/ramdisk/uhcounter
										openwbDebugLog "MAIN" 1 "Umschaltcounter Erhoehung auf $uhcounter erhoeht fuer PV Automatik Phasenumschaltung"
									else
										openwbDebugLog "MAIN" 1 "Nur PV Laden derzeit $u1p3pstat Phasen, auf NurPV Automatik konfiguriert, unterbreche Ladung und  aendere auf 3 Phasen..."
										echo 1 >ramdisk/blockall
										runs/u1p3pcheck.sh stop
										sleep 8
										runs/u1p3pcheck.sh 3
										sleep 20
										runs/u1p3pcheck.sh startslow
										(sleep 25 && echo 0 >ramdisk/blockall) &
										openwbDebugLog "MAIN" 1 "auf 3 Phasen NurPV Automatik geaendert"
										echo 0 >/var/www/html/openWB/ramdisk/uhcounter
									fi
								else
									echo 0 >/var/www/html/openWB/ramdisk/uhcounter
								fi
							else
								if ((ladeleistung < 100)); then
									if ((uberschuss < (3 * mindestuberschuss))); then
										echo 0 >/var/www/html/openWB/ramdisk/urcounter
										echo 1 >ramdisk/blockall
										runs/u1p3pcheck.sh stop
										sleep 8
										runs/u1p3pcheck.sh 1
										sleep 20
										runs/u1p3pcheck.sh startslow
										(sleep 25 && echo 0 >ramdisk/blockall) &
										openwbDebugLog "MAIN" 1 "auf 1 Phasen NurPV Automatik geaendert da geringerer Überschuss"
									fi
								fi
								if ((oldll == minimalapv)) && ((ladeleistung > 100)); then
									urcounter=$(</var/www/html/openWB/ramdisk/urcounter)
									if ((urcounter < urwaittime)); then
										urcounter=$((urcounter + 10))
										echo $urcounter >/var/www/html/openWB/ramdisk/urcounter
										openwbDebugLog "MAIN" 1 "Umschaltcounter Reduzierung auf $urcounter erhoeht fuer PV Automatik Phasenumschaltung"
									else
										echo 0 >/var/www/html/openWB/ramdisk/urcounter
										echo 1 >ramdisk/blockall
										runs/u1p3pcheck.sh stop
										sleep 8
										runs/u1p3pcheck.sh 1
										sleep 20
										runs/u1p3pcheck.sh startslow
										(sleep 25 && echo 0 >ramdisk/blockall) &
										openwbDebugLog "MAIN" 1 "auf 1 Phasen NurPV Automatik geaendert"
									fi
								else
									echo 0 >/var/www/html/openWB/ramdisk/urcounter
								fi
							fi
						else
							openwbDebugLog "MAIN" 1 "Nur PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pnurpv konfiguriert, unterbreche Ladung und  aendere..."
							echo 1 >ramdisk/blockall
							runs/u1p3pcheck.sh stop
							sleep 5
							if ((u1p3pnurpv == 3)); then
								runs/u1p3pcheck.sh 3
							else
								runs/u1p3pcheck.sh 1
							fi
							sleep 1
							runs/u1p3pcheck.sh start
							echo 0 >ramdisk/blockall
							openwbDebugLog "MAIN" 1 "auf $u1p3pnurpv Phasen geaendert"
						fi
					fi
				fi
				if ((lademodus == 4)); then
					if ((u1p3pstat != u1p3pstandby)); then
						openwbDebugLog "MAIN" 1 "Standby Laden derzeit $u1p3pstat Phasen, auf $u1p3pstandby konfiguriert, unterbreche Ladung und aendere..."
						echo 1 >ramdisk/blockall
						runs/u1p3pcheck.sh stop
						sleep 5
						if ((u1p3pstandby == 3)); then
							runs/u1p3pcheck.sh 3
						else
							runs/u1p3pcheck.sh 1
						fi
						sleep 1
						runs/u1p3pcheck.sh start
						echo 0 >ramdisk/blockall
						openwbDebugLog "MAIN" 1 "auf $u1p3pstandby Phasen geaendert"
					fi
				fi
			fi
		fi
	fi

}
