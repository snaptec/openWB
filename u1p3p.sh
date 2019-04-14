#!/bin/bash

u1p3pswitch(){

if (( u1p3paktiv == 1 && evsecon == "modbusevse" )); then
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
					sudo python runs/trigclose.py
					echo 3 > ramdisk/u1p3pstat
				else
					sudo python runs/trigopen.py
					echo 1 > ramdisk/u1p3pstat
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
						sudo python runs/trigclose.py
						echo 3 > ramdisk/u1p3pstat
					else
						sudo python runs/trigopen.py
						echo 1 > ramdisk/u1p3pstat
					fi
					if (( debug == 1 )); then
						echo "auf $u1p3psofort Phasen geaendert"
					fi

				fi
			fi
			if (( lademodus == 1 )); then
				if (( u1p3pstat != u1p3pminundpv )); then
					if (( debug == 1 )); then
						echo "Min+PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pminundpv konfiguriert, aendere..."
					fi
					if (( u1p3pminundpv == 3 )); then
						sudo python runs/trigclose.py
						echo 3 > ramdisk/u1p3pstat
					else
						sudo python runs/trigopen.py
						echo 1 > ramdisk/u1p3pstat
					fi
					if (( debug == 1 )); then
						echo "auf $u1p3pminundpv Phasen geaendert"
					fi

				fi		
			fi
			if (( lademodus == 2 )); then
				if (( u1p3pstat != u1p3pnurpv )); then
					if (( debug == 1 )); then
						echo "Nur PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pnurpv konfiguriert, aendere..."
					fi
					if (( u1p3pnurpv == 3 )); then
						sudo python runs/trigclose.py
						echo 3 > ramdisk/u1p3pstat
					else
						sudo python runs/trigopen.py
						echo 1 > ramdisk/u1p3pstat
					fi
					if (( debug == 1 )); then
						echo "auf $u1p3pnurpv Phasen geaendert"
					fi

				fi		
			fi
			if (( lademodus == 4 )); then
				if (( u1p3pstat != u1p3pstandby )); then
					if (( debug == 1 )); then
						echo "Standby Laden derzeit $u1p3pstat Phasen, auf $u1p3pstandby konfiguriert, aendere..."
					fi
					if (( u1p3pstandby == 3 )); then
						sudo python runs/trigclose.py
						echo 3 > ramdisk/u1p3pstat
					else
						sudo python runs/trigopen.py
						echo 1 > ramdisk/u1p3pstat
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
				oldll=$(<ramdisk/llsoll)
				runs/set-current.sh 0 m
				sleep 5
				if (( u1p3pnl == 3 )); then
					sudo python runs/trigclose.py
					echo 3 > ramdisk/u1p3pstat
				else
					sudo python runs/trigopen.py
					echo 1 > ramdisk/u1p3pstat
				fi
				sleep 1
				runs/set-current.sh $oldll m
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
					oldll=$(<ramdisk/llsoll)
					runs/set-current.sh 0 m
					sleep 5
					if (( u1p3psofort == 3 )); then
						sudo python runs/trigclose.py
						echo 3 > ramdisk/u1p3pstat
					else
						sudo python runs/trigopen.py
						echo 1 > ramdisk/u1p3pstat
					fi
					sleep 1
					runs/set-current.sh $oldll m
					echo 0 > ramdisk/blockall
					if (( debug == 1 )); then
						echo "auf $u1p3psofort Phasen geaendert"
					fi
				fi
			fi
			if (( lademodus == 1 )); then
				if (( u1p3pstat != u1p3pminundpv )); then
					if (( debug == 1 )); then
						echo "Min+PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pminundpv konfiguriert, unterbreche Ladung und aendere..."
					fi
					echo 1 > ramdisk/blockall
					oldll=$(<ramdisk/llsoll)
					runs/set-current.sh 0 m
					sleep 5
					if (( u1p3pminundpv == 3 )); then
						sudo python runs/trigclose.py
						echo 3 > ramdisk/u1p3pstat
					else
						sudo python runs/trigopen.py
						echo 1 > ramdisk/u1p3pstat
					fi
					sleep 1
					runs/set-current.sh $oldll m
					echo 0 > ramdisk/blockall
					if (( debug == 1 )); then
						echo "auf $u1p3pminundpv Phasen geaendert"
					fi

				fi		
			fi
			if (( lademodus == 2 )); then
				if (( u1p3pstat != u1p3pnurpv )); then
					if (( debug == 1 )); then
						echo "Nur PV Laden derzeit $u1p3pstat Phasen, auf $u1p3pnurpv konfiguriert, unterbreche Ladung und  aendere..."
					fi
					echo 1 > ramdisk/blockall
					oldll=$(<ramdisk/llsoll)
					runs/set-current.sh 0 m
					sleep 5
					if (( u1p3pnurpv == 3 )); then
						sudo python runs/trigclose.py
						echo 3 > ramdisk/u1p3pstat
					else
						sudo python runs/trigopen.py
						echo 1 > ramdisk/u1p3pstat
					fi
					sleep 1
					runs/set-current.sh $oldll m
					echo 0 > ramdisk/blockall
					if (( debug == 1 )); then
						echo "auf $u1p3pnurpv Phasen geaendert"
					fi

				fi		
			fi
			if (( lademodus == 4 )); then
				if (( u1p3pstat != u1p3pstandby )); then
					if (( debug == 1 )); then
						echo "Standby Laden derzeit $u1p3pstat Phasen, auf $u1p3pstandby konfiguriert, unterbreche Ladung und aendere..."
					fi
					echo 1 > ramdisk/blockall
					oldll=$(<ramdisk/llsoll)
					runs/set-current.sh 0 m
					sleep 5

					if (( u1p3pstandby == 3 )); then
						sudo python runs/trigclose.py
						echo 3 > ramdisk/u1p3pstat
					else
						sudo python runs/trigopen.py
						echo 1 > ramdisk/u1p3pstat
					fi
					sleep 1
					runs/set-current.sh $oldll m
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
