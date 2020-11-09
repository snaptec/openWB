#!/bin/bash

u1p3pswitch(){

if (( u1p3paktiv == 1 )); then
	u1p3pstat=$(<ramdisk/u1p3pstat)
	nachtladenstate=$(<ramdisk/nachtladenstate)
	nachtladen2state=$(<ramdisk/nachtladen2state)
	if (( debug == 1 )); then
		echo "automatische Umschaltung aktiv"
	fi
	if (( ladestatus == 0)); then
		if (( nachtladenstate == 1 )) || (( nachtladen2state == 1 )); then
			if (( u1p3pstat != u1p3pnl )); then
				if (( debug == 1 )); then
					echo "Nachtladen derzeit $u1p3pstat Phasen, auf $u1p3pnl konfiguriert, aendere..."
				fi
				if (( u1p3pnl == 3 )); then
					runs/u1p3pcheck.sh 3
				else
					runs/u1p3pcheck.sh 1
				fi
				if (( debug == 1 )); then
					echo "auf $u1p3pnl Phasen geaendert"
				fi

			fi
		else
			if (( lademodus == 0 )); then
				if (( u1p3pstat != u1p3psofort )); then
					if (( debug == 1 )); then
						echo "Sofortladen derzeit $u1p3pstat Phasen, auf $u1p3psofort konfiguriert, aendere..."
					fi
					if (( u1p3psofort == 3 )); then
						runs/u1p3pcheck.sh 3
					else
						runs/u1p3pcheck.sh 1
					fi
					if (( debug == 1 )); then
						echo "auf $u1p3psofort Phasen geaendert"
					fi

				fi
			fi
			if (( lademodus == 1 )); then
				if (( u1p3pstat != u1p3pminundpv )); then
					if (( u1p3pminundpv == 4 )); then
						if (( u1p3pstat == 0 )); then
							runs/u1p3pcheck.sh 1
						fi
						if (( u1p3pstat == 3 )); then
							urcounter=$(</var/www/html/openWB/ramdisk/urcounter)
							if (( urcounter < 600 )); then
								if (( urcounter < 540 )); then
									urcounter=540
								fi
								urcounter=$((urcounter + 10))
								echo $urcounter > /var/www/html/openWB/ramdisk/urcounter
							else
								runs/u1p3pcheck.sh 1
								if (( debug == 1 )); then
									echo "Min PV Laden derzeit $u1p3pstat Phasen, auf 1 Nur PV konfiguriert, aendere..."
								fi
								echo 0 > /var/www/html/openWB/ramdisk/urcounter

							fi
						fi
					else
						if (( debug == 1 )); then
							echo "Min PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pminundpv konfiguriert, aendere..."
						fi
						if (( u1p3pnurpv == 3 )); then
							runs/u1p3pcheck.sh 3 
						else
							runs/u1p3pcheck.sh 1
						fi
						if (( debug == 1 )); then
							echo "auf $u1p3pminundpv Phasen geaendert"
						fi
					fi
				fi		
			fi
			if (( lademodus == 2 )); then
				if (( u1p3pstat != u1p3pnurpv )); then
					if (( u1p3pnurpv == 4 )); then
						if (( u1p3pstat == 0 )); then
							runs/u1p3pcheck.sh 1
						fi
						if (( u1p3pstat == 3 )); then
							urcounter=$(</var/www/html/openWB/ramdisk/urcounter)
							if (( urcounter < 600 )); then
								if (( urcounter < 540 )); then
									urcounter=540
								fi
								urcounter=$((urcounter + 10))
								echo $urcounter > /var/www/html/openWB/ramdisk/urcounter
							else
								runs/u1p3pcheck.sh 1
								if (( debug == 1 )); then
									echo "Nur PV Laden derzeit $u1p3pstat Phasen, auf 1 Nur PV konfiguriert, aendere..."
								fi
								echo 0 > /var/www/html/openWB/ramdisk/urcounter

							fi
						fi
					else
						if (( debug == 1 )); then
							echo "Nur PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pnurpv konfiguriert, aendere..."
						fi
						if (( u1p3pnurpv == 3 )); then
							runs/u1p3pcheck.sh 3 
						else
							runs/u1p3pcheck.sh 1
						fi
						if (( debug == 1 )); then
							echo "auf $u1p3pnurpv Phasen geaendert"
						fi
					fi
				fi		
			fi
			if (( lademodus == 4 )); then
				if (( u1p3pstat != u1p3pstandby )); then
					if (( debug == 1 )); then
						echo "Standby Laden derzeit $u1p3pstat Phasen, auf $u1p3pstandby konfiguriert, aendere..."
					fi
					if (( u1p3pstandby == 3 )); then
						runs/u1p3pcheck.sh 3 
					else
						runs/u1p3pcheck.sh 1
					fi
					if (( debug == 1 )); then
						echo "auf $u1p3pstandby Phasen geaendert"
					fi

				fi		
			fi
			if (( lademodus == 3 )); then
				if (( u1p3pstat != u1p3pstandby )); then
					if (( debug == 1 )); then
						echo "Stop Laden derzeit $u1p3pstat Phasen, auf $u1p3pstandby konfiguriert, aendere..."
					fi
					if (( u1p3pstandby == 3 )); then
						runs/u1p3pcheck.sh 3 
					else
						runs/u1p3pcheck.sh 1
					fi
					if (( debug == 1 )); then
						echo "auf $u1p3pstandby Phasen geaendert"
					fi

				fi		
			fi
		fi
	else
		if (( nachtladenstate == 1 )) || (( nachtladen2state == 1 )); then
			if (( u1p3pstat != u1p3pnl )); then
				if (( debug == 1 )); then
					echo "Nachtladen derzeit $u1p3pstat Phasen, auf $u1p3pnl konfiguriert, unterbreche Ladung und aendere..."
				fi
				echo 1 > ramdisk/blockall
				runs/u1p3pcheck.sh stop
				sleep 5
				if (( u1p3pnl == 3 )); then
					runs/u1p3pcheck.sh 3 
				else
					runs/u1p3pcheck.sh 1
				fi
				sleep 1
				runs/u1p3pcheck.sh start
				echo 0 > ramdisk/blockall
				if (( debug == 1 )); then
					echo "auf $u1p3pnl Phasen geaendert"
				fi
			fi
		else
			if (( lademodus == 0 )); then
				if (( u1p3pstat != u1p3psofort )); then
					if (( debug == 1 )); then
						echo "Sofortladen derzeit $u1p3pstat Phasen, auf $u1p3psofort konfiguriert, unterbreche Ladung und aendere..."
					fi
					echo 1 > ramdisk/blockall
					runs/u1p3pcheck.sh stop
					sleep 5
					if (( u1p3psofort == 3 )); then
						runs/u1p3pcheck.sh 3 
					else
						runs/u1p3pcheck.sh 1
					fi
					sleep 1
					runs/u1p3pcheck.sh start
					echo 0 > ramdisk/blockall
					if (( debug == 1 )); then
						echo "auf $u1p3psofort Phasen geaendert"
					fi
				fi
			fi
			if (( lademodus == 1 )); then
				if (( u1p3pstat != u1p3pminundpv )); then
					if (( u1p3pminundpv == 4 )); then
						oldll=$(<ramdisk/llsoll)
						if (( u1p3pstat == 1 )); then
							if [[ $schieflastaktiv == "1" ]]; then
								maximalstromstaerke=$schieflastmaxa
							fi
							if (( ladeleistung < 100 )); then
								if (( uberschuss > 7000 )); then
									if (( debug == 1 )); then
										echo "Min PV Laden derzeit $u1p3pstat Phasen, auf MinPV Automatik konfiguriert, aendere auf 3 Phasen da viel Überschuss vorhanden..."
									fi
									echo 1 > ramdisk/blockall
									runs/u1p3pcheck.sh stop
									sleep 8
									runs/u1p3pcheck.sh 3 
									sleep 20
									runs/u1p3pcheck.sh startslow
									(sleep 25 && echo 0 > ramdisk/blockall)&
									if (( debug == 1 )); then
										echo "auf 3 Phasen MinPV Automatik geaendert"
									fi
								fi
							fi
							if (( oldll == maximalstromstaerke )); then
								uhcounter=$(</var/www/html/openWB/ramdisk/uhcounter)
								if (( uhcounter < 600 )); then
									uhcounter=$((uhcounter + 10))
									echo $uhcounter > /var/www/html/openWB/ramdisk/uhcounter
									if (( debug == 1 )); then
										echo "Umschaltcounter Erhoehung auf $uhcounter erhoeht fuer Min PV Automatik Phasenumschaltung"
									fi
								else
									if (( debug == 1 )); then
										echo "Min PV Laden derzeit $u1p3pstat Phasen, auf MinPV Automatik konfiguriert, unterbreche Ladung und  aendere auf 3 Phasen..."
									fi
									echo 1 > ramdisk/blockall
									runs/u1p3pcheck.sh stop
									sleep 8
									runs/u1p3pcheck.sh 3 
									sleep 20
									runs/u1p3pcheck.sh startslow
									(sleep 25 && echo 0 > ramdisk/blockall)&
									if (( debug == 1 )); then
										echo "auf 3 Phasen MinPV Automatik geaendert"
									fi
									echo 0 > /var/www/html/openWB/ramdisk/uhcounter
								fi
							else
								echo 0 > /var/www/html/openWB/ramdisk/uhcounter
							fi
						else
							if (( ladeleistung < 100 )); then
								if (( uberschuss < 5000 )); then
									echo 0 > /var/www/html/openWB/ramdisk/urcounter
									echo 1 > ramdisk/blockall
									runs/u1p3pcheck.sh stop
									sleep 8
									runs/u1p3pcheck.sh 1 
									sleep 20
									runs/u1p3pcheck.sh startslow
									(sleep 25 && echo 0 > ramdisk/blockall)&
									if (( debug == 1 )); then
										echo "auf 1 Phasen MinPV Automatik geaendert da geringerer Überschuss"
									fi
								fi
							fi

							if (( oldll == minimalampv )); then
								urcounter=$(</var/www/html/openWB/ramdisk/urcounter)
								if (( urcounter < 500 )); then
									urcounter=$((urcounter + 10))
									echo $urcounter > /var/www/html/openWB/ramdisk/urcounter
									if (( debug == 1 )); then
										echo "Umschaltcounter Reduzierung auf $urcounter erhoeht fuer Min PV Automatik Phasenumschaltung"
									fi

								else
									echo 0 > /var/www/html/openWB/ramdisk/urcounter
									echo 1 > ramdisk/blockall
									runs/u1p3pcheck.sh stop
									sleep 8
									runs/u1p3pcheck.sh 1 
									sleep 20
									runs/u1p3pcheck.sh startslow
									(sleep 25 && echo 0 > ramdisk/blockall)&
									if (( debug == 1 )); then
										echo "auf 1 Phasen MinPV Automatik geaendert"
									fi
								fi
							else
								echo 0 > /var/www/html/openWB/ramdisk/urcounter
							fi		
						fi
					else
						if (( debug == 1 )); then
							echo "Min PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pminundpv konfiguriert, unterbreche Ladung und  aendere..."
						fi
						echo 1 > ramdisk/blockall
						runs/u1p3pcheck.sh stop
						sleep 5
						if (( u1p3pminundpv == 3 )); then
							runs/u1p3pcheck.sh 3 	
						else
							runs/u1p3pcheck.sh 1 
						fi
						sleep 1
						runs/u1p3pcheck.sh start
						echo 0 > ramdisk/blockall
						if (( debug == 1 )); then
							echo "auf $u1p3pminundpv Phasen geaendert"
						fi
					fi
				fi		
			fi
			if (( lademodus == 2 )); then
				if (( u1p3pstat != u1p3pnurpv )); then
					if (( u1p3pnurpv == 4 )); then
						oldll=$(<ramdisk/llsoll)
						if (( u1p3pstat == 1 )); then
							if [[ $schieflastaktiv == "1" ]]; then
								maximalstromstaerke=$schieflastmaxa
							fi
							if (( ladeleistung < 100 )); then
								if (( uberschuss > 7000 )); then
									if (( debug == 1 )); then
										echo "Nur PV Laden derzeit $u1p3pstat Phasen, auf NurPV Automatik konfiguriert, aendere auf 3 Phasen da viel Überschuss vorhanden..."
									fi
									echo 1 > ramdisk/blockall
									runs/u1p3pcheck.sh stop
									sleep 8
									runs/u1p3pcheck.sh 3 
									sleep 20
									runs/u1p3pcheck.sh startslow
									(sleep 25 && echo 0 > ramdisk/blockall)&
									if (( debug == 1 )); then
										echo "auf 3 Phasen NurPV Automatik geaendert"
									fi
								fi
							fi
							if (( oldll == maximalstromstaerke )); then
								uhcounter=$(</var/www/html/openWB/ramdisk/uhcounter)
								if (( uhcounter < 600 )); then
									uhcounter=$((uhcounter + 10))
									echo $uhcounter > /var/www/html/openWB/ramdisk/uhcounter
									if (( debug == 1 )); then
										echo "Umschaltcounter Erhoehung auf $uhcounter erhoeht fuer PV Automatik Phasenumschaltung"
									fi
								else
									if (( debug == 1 )); then
										echo "Nur PV Laden derzeit $u1p3pstat Phasen, auf NurPV Automatik konfiguriert, unterbreche Ladung und  aendere auf 3 Phasen..."
									fi
									echo 1 > ramdisk/blockall
									runs/u1p3pcheck.sh stop
									sleep 8
									runs/u1p3pcheck.sh 3 
									sleep 20
									runs/u1p3pcheck.sh startslow
									(sleep 25 && echo 0 > ramdisk/blockall)&
									if (( debug == 1 )); then
										echo "auf 3 Phasen NurPV Automatik geaendert"
									fi
									echo 0 > /var/www/html/openWB/ramdisk/uhcounter
								fi
							else
								echo 0 > /var/www/html/openWB/ramdisk/uhcounter
							fi
						else
							if (( ladeleistung < 100 )); then
								if (( uberschuss < 5000 )); then
									echo 0 > /var/www/html/openWB/ramdisk/urcounter
									echo 1 > ramdisk/blockall
									runs/u1p3pcheck.sh stop
									sleep 8
									runs/u1p3pcheck.sh 1 
									sleep 20
									runs/u1p3pcheck.sh startslow
									(sleep 25 && echo 0 > ramdisk/blockall)&
									if (( debug == 1 )); then
										echo "auf 1 Phasen NurPV Automatik geaendert da geringerer Überschuss"
									fi
								fi
							fi

							if (( oldll == minimalapv )); then
								urcounter=$(</var/www/html/openWB/ramdisk/urcounter)
								if (( urcounter < 500 )); then
									urcounter=$((urcounter + 10))
									echo $urcounter > /var/www/html/openWB/ramdisk/urcounter
									if (( debug == 1 )); then
										echo "Umschaltcounter Reduzierung auf $urcounter erhoeht fuer PV Automatik Phasenumschaltung"
									fi

								else
									echo 0 > /var/www/html/openWB/ramdisk/urcounter
									echo 1 > ramdisk/blockall
									runs/u1p3pcheck.sh stop
									sleep 8
									runs/u1p3pcheck.sh 1 
									sleep 20
									runs/u1p3pcheck.sh startslow
									(sleep 25 && echo 0 > ramdisk/blockall)&
									if (( debug == 1 )); then
										echo "auf 1 Phasen NurPV Automatik geaendert"
									fi
								fi
							else
								echo 0 > /var/www/html/openWB/ramdisk/urcounter
							fi		
						fi
					else
						if (( debug == 1 )); then
							echo "Nur PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pnurpv konfiguriert, unterbreche Ladung und  aendere..."
						fi
						echo 1 > ramdisk/blockall
						runs/u1p3pcheck.sh stop
						sleep 5
						if (( u1p3pnurpv == 3 )); then
							runs/u1p3pcheck.sh 3 	
						else
							runs/u1p3pcheck.sh 1 
						fi
						sleep 1
						runs/u1p3pcheck.sh start
						echo 0 > ramdisk/blockall
						if (( debug == 1 )); then
							echo "auf $u1p3pnurpv Phasen geaendert"
						fi
					fi
				fi		
			fi
			if (( lademodus == 4 )); then
				if (( u1p3pstat != u1p3pstandby )); then
					if (( debug == 1 )); then
						echo "Standby Laden derzeit $u1p3pstat Phasen, auf $u1p3pstandby konfiguriert, unterbreche Ladung und aendere..."
					fi
					echo 1 > ramdisk/blockall
					runs/u1p3pcheck.sh stop
					sleep 5

					if (( u1p3pstandby == 3 )); then
						runs/u1p3pcheck.sh 3 	
					else
						runs/u1p3pcheck.sh 1 
					fi
					sleep 1
					runs/u1p3pcheck.sh start
					echo 0 > ramdisk/blockall
					if (( debug == 1 )); then
						echo "auf $u1p3pstandby Phasen geaendert"
					fi
				fi		
			fi
		fi
	fi
fi

}
