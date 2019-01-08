#!/bin/bash
sofortlademodus(){

	aktgeladen=$(<ramdisk/aktgeladen)
	#mit einem Ladepunkt
	if [[ $lastmanagement == "0" ]]; then
		if (( sofortsocstatlp1 == "1" )); then
			if (( soc >= sofortsoclp1 )); then
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then

					runs/set-current.sh 0 all
					if [[ $debug == "1" ]]; then
						echo "Beende Sofort Laden da $sofortsoclp1 % erreicht"
					fi

				fi
			exit 0
			fi	
		fi
		if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
			if (( lademstat == "1" )); then
				if (( $(echo "$aktgeladen > $lademkwh" |bc -l) )); then
					if [[ $debug == "1" ]]; then
	       	             			echo "Sofort ladung beendet da $lademkwh kWh lademenge erreicht"
	     				fi
				else
					runs/set-current.sh $minimalstromstaerke all
					if [[ $debug == "1" ]]; then
		        		       	echo starte sofort Ladeleistung von $minimalstromstaerke aus
        				fi
					exit 0
				fi
			else
				runs/set-current.sh $minimalstromstaerke all
				if [[ $debug == "1" ]]; then
		        	       	echo starte sofort Ladeleistung von $minimalstromstaerke aus
        			fi
				exit 0
			fi
		fi
		if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
			if (( lademstat == "1" )) && (( $(echo "$aktgeladen > $lademkwh" |bc -l) )); then
				runs/set-current.sh 0 m
				if [[ $debug == "1" ]]; then
		        	       	echo "Beende Sofort Laden da  $lademkwh kWh erreicht"
        			fi

			else
				if (( evua1 < lastmaxap1 )) && (( evua2 < lastmaxap2 )) &&  (( evua3 < lastmaxap3 )); then
					if (( ladeleistung < 500 )); then
						if (( llalt > minimalstromstaerke )); then
	        	                        	llneu=$((llalt - 1 ))
	        	                        	runs/set-current.sh $llneu m
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung reudziert auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
	        	                        	exit 0
						fi
						if (( llalt == minimalstromstaerke )); then
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
							exit 0
						fi
						if (( llalt < minimalstromstaerke )); then
							llneu=$((llalt + 1 ))
							runs/set-current.sh $llneu m
							if [[ $debug == "1" ]]; then
	       		             				echo "Sofort ladung erhöht auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
	     						fi
							exit 0
						fi
					else
						if (( llalt == sofortll )); then
							if [[ $debug == "1" ]]; then
	       		        	     			echo "Sofort ladung erreicht bei $sofortll A"
	     						fi
							exit 0
						fi
						if (( llalt > maximalstromstaerke )); then
							llneu=$((llalt - 1 ))
							runs/set-current.sh "$llneu" m
							if [[ $debug == "1" ]]; then
	       			             			echo "Sofort ladung auf $llneu reduziert, über eingestellter max A $maximalstromstaerke"
	     						fi
							exit 0
						fi
						if (( llalt < sofortll)); then
							evudiff1=$((lastmaxap1 - evua1 ))
							evudiff2=$((lastmaxap2 - evua2 ))
							evudiff3=$((lastmaxap3 - evua3 ))
							evudiffmax=($evudiff1 $evudiff2 $evudiff3)
							maxdiff=0
							for v in "${evudiffmax[@]}"; do
								if (( v > maxdiff )); then maxdiff=$v; fi;
							done
							llneu=$((llalt + maxdiff))
							if (( llneu > sofortll )); then
								llneu=$sofortll
							fi
							runs/set-current.sh "$llneu" m
			                		if [[ $debug == "1" ]]; then
	       		             				echo "Sofort ladung um $maxdiff A Differenz auf $llneu A erhoeht, kleiner als sofortll $sofortll"
	     						fi
							exit 0
						fi
						if (( llalt > sofortll)); then
							llneu=$sofortll
							runs/set-current.sh "$llneu" m
				                	if [[ $debug == "1" ]]; then
	       			             			echo "Sofort ladung von $llalt A llalt auf $llneu A reduziert, größer als sofortll $sofortll"
	     						fi
							exit 0
						fi
					fi
				else
					evudiff1=$((evua1 - lastmaxap1 ))
					evudiff2=$((evua2 - lastmaxap2 ))
					evudiff3=$((evua3 - lastmaxap3 ))
					evudiffmax=($evudiff1 $evudiff2 $evudiff3)
					maxdiff=0
					for v in "${evudiffmax[@]}"; do
						if (( v > maxdiff )); then maxdiff=$v; fi;
					done
					maxdiff=$((maxdiff + 1 ))
					llneu=$((llalt - maxdiff))
					if (( llneu < minimalstromstaerke )); then
						llneu=$minimalstromstaerke
						if [[ $debug == "1" ]]; then
							echo Differenz groesser als minimalstromstaerke, setze auf minimal A $minimalstromstaerke
						fi
					fi
					runs/set-current.sh "$llneu" m
	        		        if [[ $debug == "1" ]]; then
       	        		     		echo "Sofort ladung um $maxdiff auf $llneu reduziert"
     					fi
					exit 0
				fi
			fi
		fi
	else
		#mit mehr als einem ladepunkt
		aktgeladens1=$(<ramdisk/aktgeladens1)
		if (( evua1 < lastmaxap1 )) && (( evua2 < lastmaxap2 )) &&  (( evua3 < lastmaxap3 )); then
			evudiff1=$((lastmaxap1 - evua1 ))
			evudiff2=$((lastmaxap2 - evua2 ))
			evudiff3=$((lastmaxap3 - evua3 ))
			evudiffmax=($evudiff1 $evudiff2 $evudiff3)
			maxdiff=${evudiffmax[0]}
			for v in "${evudiffmax[@]}"; do
				if [[ "$v" -lt "$maxdiff" ]]; then
					maxdiff="$v"
				fi
			done
			maxdiff=$((maxdiff - 1 ))
			#Ladepunkt 1
			if (( sofortsocstatlp1 == "1" )); then
				if (( soc > sofortsoclp1 )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
						runs/set-current.sh 0 m
						if [[ $debug == "1" ]]; then
			        		       	echo "Beende Sofort Laden da $sofortsoclp1 % erreicht"
       						fi
					fi
				else
					if (( ladeleistung < 500 )); then
						if (( llalt > minimalstromstaerke )); then
							llneu=$((llalt - 1 ))
							runs/set-current.sh "$llneu" m
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 reudziert auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
						if (( llalt == minimalstromstaerke )); then
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
						if (( llalt < minimalstromstaerke )); then
							llneu=$minimalstromstaerke
							runs/set-current.sh "$llneu" m
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 erhöht auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
					else
						if (( llalt == sofortll )); then
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 erreicht bei $sofortll A"
							fi
						fi
						if (( llalt > maximalstromstaerke )); then
							llneu=$((llalt - 1 ))
							runs/set-current.sh "$llneu" m
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 auf $llneu reduziert, über eingestellter max A $maximalstromstaerke"
							fi
						else
							if (( llalt < sofortll)); then

								llneu=$((llalt + maxdiff))
								if (( llneu > sofortll )); then
									llneu=$sofortll
								fi
								runs/set-current.sh "$llneu" m
								if [[ $debug == "1" ]]; then
									echo "Sofort ladung Ladepunkt 1 um $maxdiff A Differenz auf $llneu A erhoeht, war kleiner als sofortll $sofortll"
								fi
							fi
							if (( llalt > sofortll)); then
								llneu=$sofortll
								runs/set-current.sh "$llneu" m
								if [[ $debug == "1" ]]; then
									echo "Sofort ladung Ladepunkt 1 von $llalt A llalt auf $llneu A reduziert, war größer als sofortll $sofortll"
								fi
							fi
						fi
					fi
				fi

			else	

			if (( lademstat == "1" )) && (( $(echo "$aktgeladen > $lademkwh" |bc -l) )); then
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
					runs/set-current.sh 0 m
					if [[ $debug == "1" ]]; then
	       				       	echo "Beende Sofort Laden an Ladepunkt 1 da  $lademkwh kWh erreicht"
       					fi
				fi
			else
				if (( ladeleistung < 500 )); then
					if (( llalt > minimalstromstaerke )); then
	                                	llneu=$((llalt - 1 ))
	                                	runs/set-current.sh "$llneu" m
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 reudziert auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
	                                fi
					if (( llalt == minimalstromstaerke )); then
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
					fi
					if (( llalt < minimalstromstaerke )); then
						llneu=$minimalstromstaerke
						runs/set-current.sh "$llneu" m
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 erhöht auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
					fi
				else
					if (( llalt == sofortll )); then
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 erreicht bei $sofortll A"
		     				fi
					fi
					if (( llalt > maximalstromstaerke )); then
						llneu=$((llalt - 1 ))
						runs/set-current.sh "$llneu" m
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 auf $llneu reduziert, über eingestellter max A $maximalstromstaerke"
		     				fi
					else
						if (( llalt < sofortll)); then

							llneu=$((llalt + maxdiff))
							if (( llneu > sofortll )); then
								llneu=$sofortll
							fi
							runs/set-current.sh "$llneu" m
			                		if [[ $debug == "1" ]]; then
		       	             				echo "Sofort ladung Ladepunkt 1 um $maxdiff A Differenz auf $llneu A erhoeht, war kleiner als sofortll $sofortll"
		     					fi
						fi
						if (( llalt > sofortll)); then
							llneu=$sofortll
							runs/set-current.sh "$llneu" m
			                		if [[ $debug == "1" ]]; then
		       	             				echo "Sofort ladung Ladepunkt 1 von $llalt A llalt auf $llneu A reduziert, war größer als sofortll $sofortll"
		     					fi
						fi
					fi
				fi
				
			fi
			fi
			
			#Ladepunkt 2
			if (( sofortsocstatlp2 == 1 )); then
				if (( soc1 > sofortsoclp2 )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						runs/set-current.sh 0 s1
						if [[ $debug == "1" ]]; then
			        		       	echo "Beende Sofort Laden an Ladepunkt 2 da  $sofortsoclp2 % erreicht"
       						fi
					fi
				else
					if (( ladeleistungs1 < 500 )); then
						if (( llalts1 > minimalstromstaerke )); then
							llneus1=$((llalts1 - 1 ))
							runs/set-current.sh "$llneus1" s1
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 reudziert auf $llneus1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
						if (( llalts1 == minimalstromstaerke )); then
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
						if (( llalts1 < minimalstromstaerke )); then
							llneus1=$minimalstromstaerke
							runs/set-current.sh "$llneus1" s1
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 erhöht auf $llneus1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
					else
						if (( llalts1 == sofortlls1 )); then
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 erreicht bei $sofortlls1 A"
							fi
						fi
						if (( llalts1 > maximalstromstaerke )); then
							llneus1=$((llalts1 - 1 ))
							runs/set-current.sh "$llneus1" s1
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 auf $llneus1 reduziert, über eingestellter max A $maximalstromstaerke"
							fi
						else
							if (( llalts1 < sofortlls1)); then
								llneus1=$((llalts1 + maxdiff))
								if (( llneus1 > sofortlls1 )); then
									llneus1=$sofortlls1
								fi
								runs/set-current.sh "$llneus1" s1
								if [[ $debug == "1" ]]; then
									echo "Sofort ladung Ladepunkt 2 um $maxdiff A Differenz auf $llneus1 A erhoeht, war kleiner als sofortll $sofortlls1"
								fi
							fi
							if (( llalts1 > sofortlls1)); then
								llneus1=$sofortlls1
								runs/set-current.sh "$llneus1" s1
								if [[ $debug == "1" ]]; then
									echo "Sofort ladung Ladepunkt 2 von $llalts1 A llalt auf $llneus1 A reduziert, war größer als sofortll $sofortlls1"
								fi
							fi
						fi
					fi
				fi
			else	
			if (( lademstats1 == "1" )) && (( $(echo "$aktgeladens1 > $lademkwhs1" |bc -l) )); then
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
					runs/set-current.sh 0 s1
					if [[ $debug == "1" ]]; then
	       				       	echo "Beende Sofort Laden an Ladepunkt 2 da  $lademkwhs1 kWh erreicht"
       					fi
				fi
			else
				if (( ladeleistungs1 < 500 )); then
					if (( llalts1 > minimalstromstaerke )); then
        	                        	llneus1=$((llalts1 - 1 ))
        	                        	runs/set-current.sh "$llneus1" s1
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 reudziert auf $llneus1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
        	                        fi
					if (( llalts1 == minimalstromstaerke )); then
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
					fi
					if (( llalts1 < minimalstromstaerke )); then
						llneus1=$minimalstromstaerke
						runs/set-current.sh "$llneus1" s1
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 erhöht auf $llneus1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
					fi
				else
					if (( llalts1 == sofortlls1 )); then
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 erreicht bei $sofortlls1 A"
		     				fi
					fi
					if (( llalts1 > maximalstromstaerke )); then
						llneus1=$((llalts1 - 1 ))
						runs/set-current.sh "$llneus1" s1
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 auf $llneus1 reduziert, über eingestellter max A $maximalstromstaerke"
		     				fi
					else
						if (( llalts1 < sofortlls1)); then
							llneus1=$((llalts1 + maxdiff))
							if (( llneus1 > sofortlls1 )); then
								llneus1=$sofortlls1
							fi
							runs/set-current.sh "$llneus1" s1
			                		if [[ $debug == "1" ]]; then
		       	             				echo "Sofort ladung Ladepunkt 2 um $maxdiff A Differenz auf $llneus1 A erhoeht, war kleiner als sofortll $sofortlls1"
		     					fi
						fi
						if (( llalts1 > sofortlls1)); then
							llneus1=$sofortlls1
							runs/set-current.sh "$llneus1" s1
			                		if [[ $debug == "1" ]]; then
	       		             				echo "Sofort ladung Ladepunkt 2 von $llalts1 A llalt auf $llneus1 A reduziert, war größer als sofortll $sofortlls1"
	     						fi
						fi
					fi
				fi
			fi
			fi
			
			#Ladepunkt 3
			if [[ $lastmanagements2 == "1" ]]; then
				aktgeladens2=$(<ramdisk/aktgeladens2)
				if (( lademstats2 == "1" )) && (( $(echo "$aktgeladens2 > $lademkwhs2" |bc -l) )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
						runs/set-current.sh 0 s2
						if [[ $debug == "1" ]]; then
		       				       	echo "Beende Sofort Laden an Ladepunkt 3 da  $lademkwhs2 kWh erreicht"
       						fi
					fi
				else
					if (( ladeleistungs2 < 500 )); then
						if (( llalts2 > minimalstromstaerke )); then
			                                	llneus2=$((llalts2 - 1 ))
	                                	runs/set-current.sh "$llneus2" s2
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 reudziert auf $llneus2 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
		                                fi
						if (( llalts2 == minimalstromstaerke )); then
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
						fi
						if (( llalts2 < minimalstromstaerke )); then
							llneus2=$minimalstromstaerke
							runs/set-current.sh "$llneus2" s2
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 erhöht auf $llneus2 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
						fi
					else
						if (( llalts2 == sofortlls2 )); then
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 erreicht bei $sofortlls2 A"
			     				fi
						fi
						if (( llalts2 > maximalstromstaerke )); then
							llneus2=$((llalts2 - 1 ))
							runs/set-current.sh "$llneus2" s2
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 auf $llneus2 reduziert, über eingestellter max A $maximalstromstaerke"
			     				fi
						else
							if (( llalts2 < sofortlls2)); then
								llneus2=$((llalts2 + maxdiff))
								if (( llneus2 > sofortlls2 )); then
									llneus2=$sofortlls2
								fi
								runs/set-current.sh "$llneus2" s2
				                		if [[ $debug == "1" ]]; then
		       		             				echo "Sofort ladung Ladepunkt 3 um $maxdiff A Differenz auf $llneus2 A erhoeht, war kleiner als sofortll $sofortlls2"
		     						fi
							fi
							if (( llalts2 > sofortlls2)); then
								llneus2=$sofortlls2
								runs/set-current.sh "$llneus2" s2
		        	        			if [[ $debug == "1" ]]; then
	       	        	     					echo "Sofort ladung Ladepunkt 3 von $llalts2 A llalt auf $llneus2 A reduziert, war größer als sofortll $sofortlls2"
	     							fi
							fi
						fi
					fi
				fi
			fi
			exit 0
			else
				evudiff1=$((evua1 - lastmaxap1 ))
				evudiff2=$((evua2 - lastmaxap2 ))
				evudiff3=$((evua3 - lastmaxap3 ))
				evudiffmax=($evudiff1 $evudiff2 $evudiff3)
				maxdiff=0
				for v in "${evudiffmax[@]}"; do
					if (( v > maxdiff )); then maxdiff=$v; fi;
				done
				maxdiff=$((maxdiff + 1 ))
				llneu=$((llalt - maxdiff))
				llneus1=$((llalts1 - maxdiff))
				if [[ $lastmanagements2 == "1" ]]; then
					llneus2=$((llalts2 - maxdiff))
				fi
				if (( llneu < minimalstromstaerke )); then
					llneu=$minimalstromstaerke
					if [[ $debug == "1" ]]; then
						echo Ladepunkt 1 Differenz groesser als minimalstromstaerke, setze auf minimal A $minimalstromstaerke
					fi
				fi
				if (( llneus1 < minimalstromstaerke )); then
					llneus1=$minimalstromstaerke
					if [[ $debug == "1" ]]; then
						echo Ladepunkt 2 Differenz groesser als minimalstromstaerke, setze auf minimal A $minimalstromstaerke
					fi
				fi
				if [[ $lastmanagements2 == "1" ]]; then
					if (( llneus2 < minimalstromstaerke )); then
						llneus2=$minimalstromstaerke
						if [[ $debug == "1" ]]; then
						echo Ladepunkt 3 Differenz groesser als minimalstromstaerke, setze auf minimal A $minimalstromstaerke
						fi
					fi
				fi
				if (( sofortsocstatlp2 == 1)); then
				if (( soc >= sofortsoclp1 )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
						runs/set-current.sh 0 m
						if [[ $debug == "1" ]]; then
		        			       	echo "Beende Sofort Laden da $sofortsoclp1 % erreicht"
						fi
					fi
				else	
					if (( lademstat == "1" )) && (( $(echo "$aktgeladen > $lademkwh" |bc -l) )); then
						if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
							runs/set-current.sh 0 m
							if [[ $debug == "1" ]]; then
		       					       	echo "Beende Sofort Laden an Ladepunkt 1 da  $lademkwh kWh erreicht"
       							fi
						fi
					else
						runs/set-current.sh "$llneu" m
					fi
				fi
				if (( soc1 >= sofortsoclp2 )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						runs/set-current.sh 0 s1
						if [[ $debug == "1" ]]; then
		        		       	echo "Beende Sofort Laden an Ladepunkt 2 da  $sofortsoclp2 % erreicht"
       						fi
					fi
				fi
				fi
					
				if (( lademstats1 == "1" )) && (( $(echo "$aktgeladens1 > $lademkwhs1" |bc -l) )); then
						if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
							runs/set-current.sh 0 s1
							if [[ $debug == "1" ]]; then
		       					       	echo "Beende Sofort Laden an Ladepunkt 2 da  $lademkwhs1 kWh erreicht"
       							fi
						fi
				else
						runs/set-current.sh "$llneus1" s1
				fi
				
				if [[ $lastmanagements2 == "1" ]]; then
					aktgeladens2=$(<ramdisk/aktgeladens2)
					if (( lademstats2 == "1" )) && (( $(echo "$aktgeladens2 > $lademkwhs2" |bc -l) )); then
						if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
							runs/set-current.sh 0 s2
							if [[ $debug == "1" ]]; then
		       					       	echo "Beende Sofort Laden an Ladepunkt 3 da  $lademkwhs2 kWh erreicht"
       							fi
						fi
					else
						runs/set-current.sh "$llneus2" s2
					fi
				fi
		        	if [[ $debug == "1" ]]; then
       		        		echo "Sofort ladung um $maxdiff auf $llneu reduziert"
     				fi
				exit 0
				
			fi
		fi
	}
