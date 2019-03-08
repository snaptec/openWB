#!/bin/bash

u1p3pswitch(){

if (( u1p3paktiv == 1 )); then
	u1p3pstat=$(<ramdisk/u1p3pstat)
	if (( debug == 1 )); then
		echo "automatische Umschaltung aktiv"
	fi
	if (( ladestatus == 0)); then
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
	
	
	
fi












}

