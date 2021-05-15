#!/bin/bash
monthlyfile="/var/www/html/openWB/web/logging/data/ladelog/$(date +%Y%m).csv"
if [ ! -f $monthlyfile ]; then
	echo $monthlyfile
fi
ladeleistung=$(<ramdisk/llaktuell)
llkwh=$(<ramdisk/llkwh)
soc=$(<ramdisk/soc)
soc1=$(<ramdisk/soc1)
nachtladenstate=$(</var/www/html/openWB/ramdisk/nachtladenstate)
nachtladen2state=$(</var/www/html/openWB/ramdisk/nachtladen2state)
rfidlp1=$(<ramdisk/rfidlp1)
rfidlp1=$( cut -d ',' -f 1 <<< "$rfidlp1" )
rfidlp2=$(<ramdisk/rfidlp2)
rfidlp2=$( cut -d ',' -f 1 <<< "$rfidlp2" )
rfidlp3=$(<ramdisk/rfidlp3)
rfidlp4=$(<ramdisk/rfidlp4)
rfidlp5=$(<ramdisk/rfidlp5)
rfidlp6=$(<ramdisk/rfidlp6)
rfidlp7=$(<ramdisk/rfidlp7)
rfidlp8=$(<ramdisk/rfidlp8)

if (( nachtladenstate == 0 )) && (( nachtladen2state == 0 )); then # Weder Nachtladen (nachtladestate) noch  Morgens laden (nachtladen2state) aktiv? nutze lademodus.
	lmodus=$(</var/www/html/openWB/ramdisk/lademodus)
else # Nachtladen oder Morgens laden ist aktiv, lademodus 7 setzen
	lmodus=7
fi
if [ -e ramdisk/loglademodus ]; then
	lademodus=$(</var/www/html/openWB/ramdisk/loglademodus)
	loglademodus=$lademodus
fi
if (( soc > 0 )); then
	soctext=$(echo ", bei $soc %SoC")
else
	soctext=$(echo ".")
fi
if (( soc1 > 0 )); then
	soctext1=$(echo ", bei $soc1 %SoC")
else
	soctext1=$(echo ".")
fi
plugstat=$(<ramdisk/plugstat)
if (( plugstat == 1 )); then
	pluggedladungaktlp1=$(<ramdisk/pluggedladungaktlp1)
	if (( pluggedladungaktlp1 == 0 )); then
		echo $llkwh > ramdisk/pluggedladunglp1startkwh
		echo 1 > ramdisk/pluggedladungaktlp1
	fi
	if (( stopchargeafterdisclp1 == 1 )); then
		boolstopchargeafterdisclp1=$(<ramdisk/boolstopchargeafterdisclp1)
		if (( boolstopchargeafterdisclp1 == 0 )); then
			echo 1 > ramdisk/boolstopchargeafterdisclp1
		fi
	fi
	pluggedladunglp1startkwh=$(<ramdisk/pluggedladunglp1startkwh)
	pluggedladungbishergeladen=$(echo "scale=2;($llkwh - $pluggedladunglp1startkwh)/1" |bc | sed 's/^\./0./')
	echo $pluggedladungbishergeladen > ramdisk/pluggedladungbishergeladen
	echo 0 > ramdisk/pluggedtimer1
else
	pluggedtimer1=$(<ramdisk/pluggedtimer1)
	if (( pluggedtimer1 < 3 )); then
		pluggedtimer1=$((pluggedtimer1 + 1))
		echo $pluggedtimer1 > ramdisk/pluggedtimer1
	else
		echo 0 > ramdisk/pluggedladungaktlp1
		if (( stopchargeafterdisclp1 == 1 )); then
			boolstopchargeafterdisclp1=$(<ramdisk/boolstopchargeafterdisclp1)
			if (( boolstopchargeafterdisclp1 == 1 )); then
				echo 0 > ramdisk/boolstopchargeafterdisclp1
				mosquitto_pub -r -t "openWB/set/lp/1/ChargePointEnabled" -m "0"
			fi
		fi
	fi
fi

if (( ladeleistung > 100 )); then
	if [ -e ramdisk/ladeustart ]; then
		ladelstart=$(<ramdisk/ladelstart)
		bishergeladen=$(echo "scale=2;($llkwh - $ladelstart)/1" |bc | sed 's/^\./0./')
		echo $bishergeladen > ramdisk/aktgeladen
		gelrlp1=$(echo "scale=2;$bishergeladen / $durchslp1 * 100" |bc)
		gelrlp1=${gelrlp1%.*}
		echo $gelrlp1 > ramdisk/gelrlp1
		restzeitlp1=$(echo "scale=6;($lademkwh - $bishergeladen)/ $ladeleistung * 1000 * 60" |bc)
		restzeitlp1=${restzeitlp1%.*}
		echo $restzeitlp1 > ramdisk/restzeitlp1m
		if (( restzeitlp1 > 60 )); then
			restzeitlp1h=$((restzeitlp1 / 60))
			restzeitlp1r=$((restzeitlp1 % 60))
			echo "$restzeitlp1h H $restzeitlp1r Min" > ramdisk/restzeitlp1
		else
			echo "$restzeitlp1 Min" > ramdisk/restzeitlp1
		fi
	else
		echo 1 > ramdisk/ladungaktivlp1
		touch ramdisk/ladeustart
		echo -e $(date +%d.%m.%y-%H:%M) > ramdisk/ladeustart
		echo -e $(date +%s) > ramdisk/ladeustarts
		echo $lmodus > ramdisk/loglademodus
		echo $llkwh > ramdisk/ladelstart
		if ((pushbenachrichtigung == "1")) ; then
			if ((pushbstartl == "1")) ; then
				./runs/pushover.sh "$lp1name Ladung gestartet$soctext"
			fi
		fi
		openwbDebugLog "CHARGESTAT" 0 "LP1, Ladung gestartet."
	fi
	echo 0 > ramdisk/llog1
else
	llog1=$(<ramdisk/llog1)
	if (( llog1 < 5 )); then
		llog1=$((llog1 + 1))
		echo $llog1 > ramdisk/llog1
	else
		if [ -e ramdisk/ladeustart ]; then
			echo 0 > ramdisk/ladungaktivlp1
			echo "--" > ramdisk/restzeitlp1
			ladelstart=$(<ramdisk/ladelstart)
			ladeustarts=$(<ramdisk/ladeustarts)
			bishergeladen=$(echo "scale=2;($llkwh - $ladelstart)/1" |bc | sed 's/^\./0./')
			start=$(<ramdisk/ladeustart)
			jetzt=$(date +%d.%m.%y-%H:%M)
			jetzts=$(date +%s)
			ladedauer=$(((jetzts - ladeustarts) / 60 ))
			ladedauers=$((jetzts - ladeustarts))
			ladegeschw=$(echo "scale=2;$bishergeladen * 60 * 60 / $ladedauers" |bc)
			gelrlp1=$(echo "scale=2;$bishergeladen / $durchslp1 * 100" |bc)
			gelrlp1=${gelrlp1%.*}
			if (( ladedauer > 60 )); then
				ladedauerh=$((ladedauer / 60))
				laderest=$((ladedauer % 60))
				sed -i '1i'$start,$jetzt,$gelrlp1,$bishergeladen,$ladegeschw,$ladedauerh' H '$laderest' Min,1',$loglademodus,$rfidlp1 $monthlyfile
				if ((pushbenachrichtigung == "1")) ; then
					if ((pushbstopl == "1")) ; then
						./runs/pushover.sh "$lp1name Ladung gestoppt. $bishergeladen kWh in $ladedauerh H $laderest Min mit durchschnittlich $ladegeschw kW geladen$soctext"
					fi
				fi
			else
				sed -i '1i'$start,$jetzt,$gelrlp1,$bishergeladen,$ladegeschw,$ladedauer' Min,1',$loglademodus,$rfidlp1 $monthlyfile
				if ((pushbenachrichtigung == "1")) ; then
					if ((pushbstopl == "1")) ; then
						./runs/pushover.sh "$lp1name Ladung gestoppt. $bishergeladen kWh in $ladedauer Min mit durchschnittlich $ladegeschw kW geladen$soctext"
					fi
				fi
			fi
			openwbDebugLog "CHARGESTAT" 0 "LP1, Ladung gestoppt"
			rm ramdisk/ladeustart
		fi
	fi
fi

if (( lastmanagement == 1 )); then
	ladeleistungs1=$(<ramdisk/llaktuells1)
	llkwhs1=$(<ramdisk/llkwhs1)
	plugstatlp2=$(<ramdisk/plugstats1)
	if (( plugstatlp2 == 1 )); then
		pluggedladungaktlp2=$(<ramdisk/pluggedladungaktlp2)
		if (( pluggedladungaktlp2 == 0 )); then
			echo $llkwhs1 > ramdisk/pluggedladunglp2startkwh
			echo 1 > ramdisk/pluggedladungaktlp2
		fi
		pluggedladunglp2startkwh=$(<ramdisk/pluggedladunglp2startkwh)
		pluggedladungbishergeladenlp2=$(echo "scale=2;($llkwhs1 - $pluggedladunglp2startkwh)/1" |bc | sed 's/^\./0./')
		echo $pluggedladungbishergeladenlp2 > ramdisk/pluggedladungbishergeladenlp2
		echo 0 > ramdisk/pluggedtimer2
		if (( stopchargeafterdisclp2 == 1 )); then
			boolstopchargeafterdisclp2=$(<ramdisk/boolstopchargeafterdisclp2)
			if (( boolstopchargeafterdisclp2 == 0 )); then
				echo 1 > ramdisk/boolstopchargeafterdisclp2
			fi
		fi
	else
		pluggedtimer2=$(<ramdisk/pluggedtimer2)
		if (( pluggedtimer2 < 3 )); then
			pluggedtimer2=$((pluggedtimer2 + 1))
			echo $pluggedtimer2 > ramdisk/pluggedtimer2
		else
			echo 0 > ramdisk/pluggedladungaktlp2
			if (( stopchargeafterdisclp2 == 1 )); then
				boolstopchargeafterdisclp2=$(<ramdisk/boolstopchargeafterdisclp2)
				if (( boolstopchargeafterdisclp2 == 1 )); then
					echo 0 > ramdisk/boolstopchargeafterdisclp2
					mosquitto_pub -r -t "openWB/set/lp/2/ChargePointEnabled" -m "0"
				fi
			fi
		fi
	fi

	if (( ladeleistungs1 > 100 )); then
		if [ -e ramdisk/ladeustarts1 ]; then

			ladelstarts1=$(<ramdisk/ladelstarts1)
			bishergeladens1=$(echo "scale=2;($llkwhs1 - $ladelstarts1)/1" |bc | sed 's/^\./0./')
			echo $bishergeladens1 > ramdisk/aktgeladens1
			gelrlp2=$(echo "scale=2;$bishergeladens1 / $durchslp2 * 100" |bc)
			gelrlp2=${gelrlp2%.*}
			echo $gelrlp2 > ramdisk/gelrlp2
			restzeitlp2=$(echo "scale=6;($lademkwhs1 - $bishergeladens1)/ $ladeleistungs1 * 1000 * 60" |bc)
			restzeitlp2=${restzeitlp2%.*}
			echo $restzeitlp2 > ramdisk/restzeitlp2m

			if (( restzeitlp2 > 60 )); then
				restzeitlp2h=$((restzeitlp2 / 60))
				restzeitlp2r=$((restzeitlp2 % 60))
				echo "$restzeitlp2h H $restzeitlp2r Min" > ramdisk/restzeitlp2
			else
				echo "$restzeitlp2 Min" > ramdisk/restzeitlp2
			fi
		else
			if ((pushbenachrichtigung == "1")) ; then
				if ((pushbstartl == "1")) ; then
					./runs/pushover.sh "$lp2name Ladung gestartet$soctext1"
				fi
			fi
			openwbDebugLog "CHARGESTAT" 0 "LP2, Ladung gestartet"

			echo 1 > ramdisk/ladungaktivlp2
			touch ramdisk/ladeustarts1
			echo $lmodus > ramdisk/loglademodus
			echo -e $(date +%d.%m.%y-%H:%M) > ramdisk/ladeustarts1
			echo -e $(date +%s) > ramdisk/ladeustartss1
			echo $llkwhs1 > ramdisk/ladelstarts1
		fi
		echo 0 > ramdisk/llogs1
	else
		llogs1=$(<ramdisk/llogs1)
		if (( llogs1 < 5 )); then
			llogs1=$((llogs1 + 1))
			echo $llogs1 > ramdisk/llogs1
		else
			if [ -e ramdisk/ladeustarts1 ]; then
				echo 0 > ramdisk/ladungaktivlp2
				echo "--" > ramdisk/restzeitlp2
				ladelstarts1=$(<ramdisk/ladelstarts1)
				ladeustartss1=$(<ramdisk/ladeustartss1)
				bishergeladens1=$(echo "scale=2;($llkwhs1 - $ladelstarts1)/1" |bc | sed 's/^\./0./')
				starts1=$(<ramdisk/ladeustarts1)
				jetzts1=$(date +%d.%m.%y-%H:%M)
				jetztss1=$(date +%s)
				ladedauers1=$(((jetztss1 - ladeustartss1) / 60 ))
				ladedauerss1=$((jetztss1 - ladeustartss1))
				ladegeschws1=$(echo "scale=2;$bishergeladens1 * 60 * 60 / $ladedauerss1" |bc)
				gelrlp2=$(echo "scale=2;$bishergeladens1 / $durchslp2 * 100" |bc)
				gelrlp2=${gelrlp2%.*}
				if (( ladedauers1 > 60 )); then
					ladedauerhs1=$((ladedauers1 / 60))
					laderests1=$((ladedauers1 % 60))
					sed -i '1i'$starts1,$jetzts1,$gelrlp2,$bishergeladens1,$ladegeschws1,$ladedauerhs1' H '$laderests1' Min,2',$loglademodus,$rfidlp2 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp2name Ladung gestoppt. $bishergeladens1 kWh in $ladedauerhs1 H $laderests1 Min mit durchschnittlich $ladegeschws1 kW geladen$soctext1"
						fi
					fi
				else
					sed -i '1i'$starts1,$jetzts1,$gelrlp2,$bishergeladens1,$ladegeschws1,$ladedauers1' Min,2',$loglademodus,$rfidlp2 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp2name Ladung gestoppt. $bishergeladens1 kWh in $ladedauers1 Min mit durchschnittlich $ladegeschws1 kW geladen$soctext1"
						fi
					fi
				fi
				openwbDebugLog "CHARGESTAT" 0 "LP2, Ladung gestoppt"
				rm ramdisk/ladeustarts1
			fi
		fi
	fi
fi

if (( lastmanagements2 == 1 )); then
	ladeleistungs2=$(<ramdisk/llaktuells2)
	llkwhs2=$(<ramdisk/llkwhs2)
	plugstatlp3=$(<ramdisk/plugstatlp3)
	if (( plugstatlp3 == 1 )); then
		pluggedladungaktlp3=$(<ramdisk/pluggedladungaktlp3)
		if (( pluggedladungaktlp3 == 0 )); then
			echo $llkwhs2 > ramdisk/pluggedladunglp3startkwh
			echo 1 > ramdisk/pluggedladungaktlp3
		fi
		pluggedladunglp3startkwh=$(<ramdisk/pluggedladunglp3startkwh)
		pluggedladungbishergeladenlp3=$(echo "scale=2;($llkwhs2 - $pluggedladunglp3startkwh)/1" |bc | sed 's/^\./0./')
		echo $pluggedladungbishergeladenlp3 > ramdisk/pluggedladungbishergeladenlp3
		echo 0 > ramdisk/pluggedtimer3
		if (( stopchargeafterdisclp3 == 1 )); then
			boolstopchargeafterdisclp3=$(<ramdisk/boolstopchargeafterdisclp3)
			if (( boolstopchargeafterdisclp3 == 0 )); then
				echo 1 > ramdisk/boolstopchargeafterdisclp3
			fi
		fi
	else
		pluggedtimer3=$(<ramdisk/pluggedtimer3)
		if (( pluggedtimer3 < 3 )); then
			pluggedtimer3=$((pluggedtimer3 + 1))
			echo $pluggedtimer3 > ramdisk/pluggedtimer3
		else
			echo 0 > ramdisk/pluggedladungaktlp3

			if (( stopchargeafterdisclp3 == 1 )); then
				boolstopchargeafterdisclp3=$(<ramdisk/boolstopchargeafterdisclp3)
				if (( boolstopchargeafterdisclp3 == 1 )); then
					echo 0 > ramdisk/boolstopchargeafterdisclp3
					mosquitto_pub -r -t "openWB/set/lp/3/ChargePointEnabled" -m "0"
				fi
			fi
		fi
	fi

	if (( ladeleistungs2 > 100 )); then
		if [ -e ramdisk/ladeustarts2 ]; then

			ladelstarts2=$(<ramdisk/ladelstarts2)
			bishergeladens2=$(echo "scale=2;($llkwhs2 - $ladelstarts2)/1" |bc | sed 's/^\./0./')
			echo $bishergeladens2 > ramdisk/aktgeladens2
			gelrlp3=$(echo "scale=2;$bishergeladens2 / $durchslp3 * 100" |bc)
			gelrlp3=${gelrlp3%.*}
			echo $gelrlp3 > ramdisk/gelrlp3
			restzeitlp3=$(echo "scale=6;($lademkwhs2 - $bishergeladens2)/ $ladeleistungs2 * 1000 * 60" |bc)
			restzeitlp3=${restzeitlp3%.*}
			echo $restzeitlp3 > ramdisk/restzeitlp3m
			if (( restzeitlp3 > 60 )); then
				restzeitlp3h=$((restzeitlp3 / 60))
				restzeitlp3r=$((restzeitlp3 % 60))
				echo "$restzeitlp3h H $restzeitlp3r Min" > ramdisk/restzeitlp3
			else
				echo "$restzeitlp3 Min" > ramdisk/restzeitlp3
			fi
		else
			if ((pushbenachrichtigung == "1")) ; then
				if ((pushbstartl == "1")) ; then
					./runs/pushover.sh "$lp3name Ladung gestartet"
				fi
			fi
			openwbDebugLog "CHARGESTAT" 0 "LP3, Ladung gestartet"

			echo 1 > ramdisk/ladungaktivlp3
			touch ramdisk/ladeustarts2
			echo $lmodus > ramdisk/loglademodus
			echo -e $(date +%d.%m.%y-%H:%M) > ramdisk/ladeustarts2
			echo -e $(date +%s) > ramdisk/ladeustartss2
			echo $llkwhs2 > ramdisk/ladelstarts2
		fi
		echo 0 > ramdisk/llogs2
	else
		llogs2=$(<ramdisk/llogs2)
		if (( llogs2 < 5 )); then
			llogs2=$((llogs2 + 1))
			echo $llogs2 > ramdisk/llogs2
		else
			if [ -e ramdisk/ladeustarts2 ]; then
				echo 0 > ramdisk/ladungaktivlp3
				echo "--" > ramdisk/restzeitlp3
				ladelstarts2=$(<ramdisk/ladelstarts2)
				ladeustartss2=$(<ramdisk/ladeustartss2)
				bishergeladens2=$(echo "scale=2;($llkwhs2 - $ladelstarts2)/1" |bc | sed 's/^\./0./')
				starts2=$(<ramdisk/ladeustarts2)
				jetzts2=$(date +%d.%m.%y-%H:%M)
				jetztss2=$(date +%s)
				ladedauers2=$(((jetztss2 - ladeustartss2) / 60 ))
				ladedauerss2=$((jetztss2 - ladeustartss2))
				ladegeschws2=$(echo "scale=2;$bishergeladens2 * 60 * 60 / $ladedauerss2" |bc)
				gelrlp3=$(echo "scale=2;$bishergeladens2 / $durchslp3 * 100" |bc)
				gelrlp3=${gelrlp3%.*}

				if (( ladedauers2 > 60 )); then
					ladedauerhs2=$((ladedauers2 / 60))
					laderests2=$((ladedauers2 % 60))
					sed -i '1i'$starts2,$jetzts2,$gelrlp3,$bishergeladens2,$ladegeschws2,$ladedauerhs2' H '$laderests2' Min,3',$lademodus,$rfidlp3 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp3name Ladung gestoppt. $bishergeladens2 kWh in $ladedauerhs2 H $laderests2 Min mit durchschnittlich $ladegeschws2 kW geladen."
						fi
					fi
				else
					sed -i '1i'$starts2,$jetzts2,$gelrlp3,$bishergeladens2,$ladegeschws2,$ladedauers2' Min,3',$lademodus,$rfidlp3 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp3name Ladung gestoppt. $bishergeladens2 kWh in $ladedauers2 Min mit durchschnittlich $ladegeschws2 kW geladen."
						fi
					fi

				fi
				openwbDebugLog "CHARGESTAT" 0 "LP3, Ladung gestoppt"

				rm ramdisk/ladeustarts2
			fi
		fi
	fi
fi

if (( lastmanagementlp4 == 1 )); then
	ladeleistunglp4=$(<ramdisk/llaktuelllp4)
	llkwhlp4=$(<ramdisk/llkwhlp4)
	plugstatlp4=$(<ramdisk/plugstatlp4)
	if (( plugstatlp4 == 1 )); then
		pluggedladungaktlp4=$(<ramdisk/pluggedladungaktlp4)
		if (( pluggedladungaktlp4 == 0 )); then
			echo $llkwhlp4 > ramdisk/pluggedladunglp4startkwh
			echo 1 > ramdisk/pluggedladungaktlp4
		fi
		pluggedladunglp4startkwh=$(<ramdisk/pluggedladunglp4startkwh)
		pluggedladungbishergeladenlp4=$(echo "scale=2;($llkwhlp4 - $pluggedladunglp4startkwh)/1" |bc | sed 's/^\./0./')
		echo $pluggedladungbishergeladenlp4 > ramdisk/pluggedladungbishergeladenlp4
		echo 0 > ramdisk/pluggedtimerlp4
		if (( stopchargeafterdisclp4 == 1 )); then
			boolstopchargeafterdisclp4=$(<ramdisk/boolstopchargeafterdisclp4)
			if (( boolstopchargeafterdisclp4 == 0 )); then
				echo 1 > ramdisk/boolstopchargeafterdisclp4
			fi
		fi
	else
		pluggedtimerlp4=$(<ramdisk/pluggedtimerlp4)
		if (( pluggedtimerlp4 < 6 )); then
			pluggedtimerlp4=$((pluggedtimerlp4 + 1))
			echo $pluggedtimerlp4 > ramdisk/pluggedtimerlp4
		else
			echo 0 > ramdisk/pluggedladungaktlp4
			if (( stopchargeafterdisclp4 == 1 )); then
				boolstopchargeafterdisclp4=$(<ramdisk/boolstopchargeafterdisclp4)
				if (( boolstopchargeafterdisclp4 == 1 )); then
					echo 0 > ramdisk/boolstopchargeafterdisclp4
					mosquitto_pub -r -t "openWB/set/lp/4/ChargePointEnabled" -m "0"
				fi
			fi
		fi
	fi

	if (( ladeleistunglp4 > 100 )); then
		if [ -e ramdisk/ladeustartlp4 ]; then

			ladelstartlp4=$(<ramdisk/ladelstartlp4)
			bishergeladenlp4=$(echo "scale=2;($llkwhlp4 - $ladelstartlp4)/1" |bc | sed 's/^\./0./')
			echo $bishergeladenlp4 > ramdisk/aktgeladenlp4
			gelrlp4=$(echo "scale=2;$bishergeladenlp4 / $durchslp4 * 100" |bc)
			gelrlp4=${gelrlp4%.*}
			echo $gelrlp4 > ramdisk/gelrlp4
			restzeitlp4=$(echo "scale=6;($lademkwhlp4 - $bishergeladenlp4)/ $ladeleistunglp4 * 1000 * 60" |bc)
			restzeitlp4=${restzeitlp4%.*}
			echo $restzeitlp4 > ramdisk/restzeitlp4m
			if (( restzeitlp4 > 60 )); then
				restzeitlp4h=$((restzeitlp4 / 60))
				restzeitlp4r=$((restzeitlp4 % 60))
				echo "$restzeitlp4h H $restzeitlp4r Min" > ramdisk/restzeitlp4
			else
				echo "$restzeitlp4 Min" > ramdisk/restzeitlp4
			fi
		else
			if ((pushbenachrichtigung == "1")) ; then
				if ((pushbstartl == "1")) ; then
					./runs/pushover.sh "$lp4name Ladung gestartet"
				fi
			fi
			openwbDebugLog "CHARGESTAT" 0 "LP4, Ladung gestartet"

			echo 1 > ramdisk/ladungaktivlp4
			touch ramdisk/ladeustartlp4
			echo $lmodus > ramdisk/loglademodus
			echo -e $(date +%d.%m.%y-%H:%M) > ramdisk/ladeustartlp4
			echo -e $(date +%s) > ramdisk/ladeustartslp4
			echo $llkwhlp4 > ramdisk/ladelstartlp4
		fi
		echo 0 > ramdisk/lloglp4
	else
		lloglp4=$(<ramdisk/lloglp4)
		if (( lloglp4 < 5 )); then
			lloglp4=$((lloglp4 + 1))
			echo $lloglp4 > ramdisk/lloglp4
		else
			if [ -e ramdisk/ladeustartlp4 ]; then
				echo 0 > ramdisk/ladungaktivlp4
				echo "--" > ramdisk/restzeitlp4
				ladelstartlp4=$(<ramdisk/ladelstartlp4)
				ladeustartslp4=$(<ramdisk/ladeustartslp4)
				bishergeladenlp4=$(echo "scale=2;($llkwhlp4 - $ladelstartlp4)/1" |bc | sed 's/^\./0./')
				startlp4=$(<ramdisk/ladeustartlp4)
				jetztlp4=$(date +%d.%m.%y-%H:%M)
				jetztslp4=$(date +%s)
				ladedauerlp4=$(((jetztslp4 - ladeustartslp4) / 60 ))
				ladedauerslp4=$((jetztslp4 - ladeustartslp4))
				ladegeschwlp4=$(echo "scale=2;$bishergeladenlp4 * 60 * 60 / $ladedauerslp4" |bc)
				gelrlp4=$(echo "scale=2;$bishergeladenlp4 / $durchslp4 * 100" |bc)
				gelrlp4=${gelrlp4%.*}

				if (( ladedauerlp4 > 60 )); then
					ladedauerhlp4=$((ladedauerlp4 / 60))
					laderestlp4=$((ladedauerlp4 % 60))
					sed -i '1i'$startlp4,$jetztlp4,$gelrlp4,$bishergeladenlp4,$ladegeschwlp4,$ladedauerhlp4' H '$laderestlp4' Min,4',$lademodus,$rfidlp4 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp4name Ladung gestoppt. $bishergeladenlp4 kWh in $ladedauerhlp4 H $laderestlp4 Min mit durchschnittlich $ladegeschwlp4 kW geladen."
						fi
					fi

				else
					sed -i '1i'$startlp4,$jetztlp4,$gelrlp4,$bishergeladenlp4,$ladegeschwlp4,$ladedauerlp4' Min,4',$lademodus,$rfidlp4 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp4name Ladung gestoppt. $bishergeladenlp4 kWh in $ladedauerlp4 Min mit durchschnittlich $ladegeschwlp4 kW geladen."
						fi
					fi

				fi
				openwbDebugLog "CHARGESTAT" 0 "LP4, Ladung gestoppt"

				rm ramdisk/ladeustartlp4
			fi
		fi
	fi
fi

if (( lastmanagementlp5 == 1 )); then
	ladeleistunglp5=$(<ramdisk/llaktuelllp5)
	llkwhlp5=$(<ramdisk/llkwhlp5)
	plugstatlp5=$(<ramdisk/plugstatlp5)
	if (( plugstatlp5 == 1 )); then
		pluggedladungaktlp5=$(<ramdisk/pluggedladungaktlp5)
		if (( pluggedladungaktlp5 == 0 )); then
			echo $llkwhlp5 > ramdisk/pluggedladunglp5startkwh
			echo 1 > ramdisk/pluggedladungaktlp5
		fi
		pluggedladunglp5startkwh=$(<ramdisk/pluggedladunglp5startkwh)
		pluggedladungbishergeladenlp5=$(echo "scale=2;($llkwhlp5 - $pluggedladunglp5startkwh)/1" |bc | sed 's/^\./0./')
		echo $pluggedladungbishergeladenlp5 > ramdisk/pluggedladungbishergeladenlp5
		echo 0 > ramdisk/pluggedtimerlp5
		if (( stopchargeafterdisclp5 == 1 )); then
			boolstopchargeafterdisclp5=$(<ramdisk/boolstopchargeafterdisclp5)
			if (( boolstopchargeafterdisclp5 == 0 )); then
				echo 1 > ramdisk/boolstopchargeafterdisclp5
			fi
		fi
	else
		pluggedtimerlp5=$(<ramdisk/pluggedtimerlp5)
		if (( pluggedtimerlp5 < 6 )); then
			pluggedtimerlp5=$((pluggedtimerlp5 + 1))
			echo $pluggedtimerlp5 > ramdisk/pluggedtimerlp5
		else
			echo 0 > ramdisk/pluggedladungaktlp5
			if (( stopchargeafterdisclp5 == 1 )); then
				boolstopchargeafterdisclp5=$(<ramdisk/boolstopchargeafterdisclp5)
				if (( boolstopchargeafterdisclp5 == 1 )); then
					echo 0 > ramdisk/boolstopchargeafterdisclp5
					mosquitto_pub -r -t "openWB/set/lp/5/ChargePointEnabled" -m "0"
				fi
			fi
		fi
	fi
	if (( ladeleistunglp5 > 60 )); then
		if [ -e ramdisk/ladeustartlp5 ]; then

			ladelstartlp5=$(<ramdisk/ladelstartlp5)
			bishergeladenlp5=$(echo "scale=2;($llkwhlp5 - $ladelstartlp5)/1" |bc | sed 's/^\./0./')
			echo $bishergeladenlp5 > ramdisk/aktgeladenlp5
			gelrlp5=$(echo "scale=2;$bishergeladenlp5 / $durchslp5 * 100" |bc)
			gelrlp5=${gelrlp5%.*}
			echo $gelrlp5 > ramdisk/gelrlp5
			restzeitlp5=$(echo "scale=6;($lademkwhlp5 - $bishergeladenlp5)/ $ladeleistunglp5 * 1000 * 60" |bc)
			restzeitlp5=${restzeitlp5%.*}
			echo $restzeitlp5 > ramdisk/restzeitlp5m
			if (( restzeitlp5 > 60 )); then
				restzeitlp5h=$((restzeitlp5 / 60))
				restzeitlp5r=$((restzeitlp5 % 60))
				echo "$restzeitlp5h H $restzeitlp5r Min" > ramdisk/restzeitlp5
			else
				echo "$restzeitlp5 Min" > ramdisk/restzeitlp5
			fi
		else
			if ((pushbenachrichtigung == "1")) ; then
				if ((pushbstartl == "1")) ; then
					./runs/pushover.sh "$lp5name Ladung gestartet"
				fi
			fi
			openwbDebugLog "CHARGESTAT" 0 "LP5, Ladung gestartet"

			echo 1 > ramdisk/ladungaktivlp5
			touch ramdisk/ladeustartlp5
			echo $lmodus > ramdisk/loglademodus
			echo -e $(date +%d.%m.%y-%H:%M) > ramdisk/ladeustartlp5
			echo -e $(date +%s) > ramdisk/ladeustartslp5
			echo $llkwhlp5 > ramdisk/ladelstartlp5
		fi
		echo 0 > ramdisk/lloglp5
	else
		lloglp5=$(<ramdisk/lloglp5)
		if (( lloglp5 < 5 )); then
			lloglp5=$((lloglp5 + 1))
			echo $lloglp5 > ramdisk/lloglp5
		else
			if [ -e ramdisk/ladeustartlp5 ]; then
				echo 0 > ramdisk/ladungaktivlp5
				echo "--" > ramdisk/restzeitlp5
				ladelstartlp5=$(<ramdisk/ladelstartlp5)
				ladeustartslp5=$(<ramdisk/ladeustartslp5)
				bishergeladenlp5=$(echo "scale=2;($llkwhlp5 - $ladelstartlp5)/1" |bc | sed 's/^\./0./')
				startlp5=$(<ramdisk/ladeustartlp5)
				jetztlp5=$(date +%d.%m.%y-%H:%M)
				jetztslp5=$(date +%s)
				ladedauerlp5=$(((jetztslp5 - ladeustartslp5) / 60 ))
				ladedauerslp5=$((jetztslp5 - ladeustartslp5))
				ladegeschwlp5=$(echo "scale=2;$bishergeladenlp5 * 60 * 60 / $ladedauerslp5" |bc)
				gelrlp5=$(echo "scale=2;$bishergeladenlp5 / $durchslp5 * 100" |bc)
				gelrlp5=${gelrlp5%.*}

				if (( ladedauerlp5 > 60 )); then
					ladedauerhlp5=$((ladedauerlp5 / 60))
					laderestlp5=$((ladedauerlp5 % 60))
					sed -i '1i'$startlp5,$jetztlp5,$gelrlp5,$bishergeladenlp5,$ladegeschwlp5,$ladedauerhlp5' H '$laderestlp5' Min,5',$lademodus,$rfidlp5 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp5name Ladung gestoppt. $bishergeladenlp5 kWh in $ladedauerhlp5 H $laderestlp5 Min mit durchschnittlich $ladegeschwlp5 kW geladen."
						fi
					fi

				else
					sed -i '1i'$startlp5,$jetztlp5,$gelrlp5,$bishergeladenlp5,$ladegeschwlp5,$ladedauerlp5' Min,5',$lademodus,$rfidlp5 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp5name Ladung gestoppt. $bishergeladenlp5 kWh in $ladedauerlp5 Min mit durchschnittlich $ladegeschwlp5 kW geladen."
						fi
					fi

				fi
				openwbDebugLog "CHARGESTAT" 0 "LP5, Ladung gestoppt"

				rm ramdisk/ladeustartlp5
			fi
		fi

	fi
fi

if (( lastmanagementlp6 == 1 )); then
	ladeleistunglp6=$(<ramdisk/llaktuelllp6)
	llkwhlp6=$(<ramdisk/llkwhlp6)
	plugstatlp6=$(<ramdisk/plugstatlp6)
	if (( plugstatlp6 == 1 )); then
		pluggedladungaktlp6=$(<ramdisk/pluggedladungaktlp6)
		if (( pluggedladungaktlp6 == 0 )); then
			echo $llkwhlp6 > ramdisk/pluggedladunglp6startkwh
			echo 1 > ramdisk/pluggedladungaktlp6
		fi
		pluggedladunglp6startkwh=$(<ramdisk/pluggedladunglp6startkwh)
		pluggedladungbishergeladenlp6=$(echo "scale=2;($llkwhlp6 - $pluggedladunglp6startkwh)/1" |bc | sed 's/^\./0./')
		echo $pluggedladungbishergeladenlp6 > ramdisk/pluggedladungbishergeladenlp6
		echo 0 > ramdisk/pluggedtimerlp6
		if (( stopchargeafterdisclp6 == 1 )); then
			boolstopchargeafterdisclp6=$(<ramdisk/boolstopchargeafterdisclp6)
			if (( boolstopchargeafterdisclp6 == 0 )); then
				echo 1 > ramdisk/boolstopchargeafterdisclp6
			fi
		fi
	else
		pluggedtimerlp6=$(<ramdisk/pluggedtimerlp6)
		if (( pluggedtimerlp6 < 6 )); then
			pluggedtimerlp6=$((pluggedtimerlp6 + 1))
			echo $pluggedtimerlp6 > ramdisk/pluggedtimerlp6
		else
			echo 0 > ramdisk/pluggedladungaktlp6
			if (( stopchargeafterdisclp6 == 1 )); then
				boolstopchargeafterdisclp6=$(<ramdisk/boolstopchargeafterdisclp6)
				if (( boolstopchargeafterdisclp6 == 1 )); then
					echo 0 > ramdisk/boolstopchargeafterdisclp6
					mosquitto_pub -r -t "openWB/set/lp/6/ChargePointEnabled" -m "0"
				fi
			fi
		fi
	fi
	if (( ladeleistunglp6 > 100 )); then
		if [ -e ramdisk/ladeustartlp6 ]; then

			ladelstartlp6=$(<ramdisk/ladelstartlp6)
			bishergeladenlp6=$(echo "scale=2;($llkwhlp6 - $ladelstartlp6)/1" |bc | sed 's/^\./0./')
			echo $bishergeladenlp6 > ramdisk/aktgeladenlp6
			gelrlp6=$(echo "scale=2;$bishergeladenlp6 / $durchslp6 * 100" |bc)
			gelrlp6=${gelrlp6%.*}
			echo $gelrlp6 > ramdisk/gelrlp6
			restzeitlp6=$(echo "scale=6;($lademkwhlp6 - $bishergeladenlp6)/ $ladeleistunglp6 * 1000 * 60" |bc)
			restzeitlp6=${restzeitlp6%.*}
			echo $restzeitlp6 > ramdisk/restzeitlp6m
			if (( restzeitlp6 > 60 )); then
				restzeitlp6h=$((restzeitlp6 / 60))
				restzeitlp6r=$((restzeitlp6 % 60))
				echo "$restzeitlp6h H $restzeitlp6r Min" > ramdisk/restzeitlp6
			else
				echo "$restzeitlp6 Min" > ramdisk/restzeitlp6
			fi
		else
			if ((pushbenachrichtigung == "1")) ; then
				if ((pushbstartl == "1")) ; then
					./runs/pushover.sh "$lp6name Ladung gestartet"
				fi
			fi
			openwbDebugLog "CHARGESTAT" 0 "LP6, Ladung gestartet"

			echo 1 > ramdisk/ladungaktivlp6
			touch ramdisk/ladeustartlp6
			echo $lmodus > ramdisk/loglademodus
			echo -e $(date +%d.%m.%y-%H:%M) > ramdisk/ladeustartlp6
			echo -e $(date +%s) > ramdisk/ladeustartslp6
			echo $llkwhlp6 > ramdisk/ladelstartlp6
		fi
		echo 0 > ramdisk/lloglp6
	else
		lloglp6=$(<ramdisk/lloglp6)
		if (( lloglp6 < 5 )); then
			lloglp6=$((lloglp6 + 1))
			echo $lloglp6 > ramdisk/lloglp6
		else
			if [ -e ramdisk/ladeustartlp6 ]; then
				echo 0 > ramdisk/ladungaktivlp6
				echo "--" > ramdisk/restzeitlp6
				ladelstartlp6=$(<ramdisk/ladelstartlp6)
				ladeustartslp6=$(<ramdisk/ladeustartslp6)
				bishergeladenlp6=$(echo "scale=2;($llkwhlp6 - $ladelstartlp6)/1" |bc | sed 's/^\./0./')
				startlp6=$(<ramdisk/ladeustartlp6)
				jetztlp6=$(date +%d.%m.%y-%H:%M)
				jetztslp6=$(date +%s)
				ladedauerlp6=$(((jetztslp6 - ladeustartslp6) / 60 ))
				ladedauerslp6=$((jetztslp6 - ladeustartslp6))
				ladegeschwlp6=$(echo "scale=2;$bishergeladenlp6 * 60 * 60 / $ladedauerslp6" |bc)
				gelrlp6=$(echo "scale=2;$bishergeladenlp6 / $durchslp6 * 100" |bc)
				gelrlp6=${gelrlp6%.*}

				if (( ladedauerlp6 > 60 )); then
					ladedauerhlp6=$((ladedauerlp6 / 60))
					laderestlp6=$((ladedauerlp6 % 60))
					sed -i '1i'$startlp6,$jetztlp6,$gelrlp6,$bishergeladenlp6,$ladegeschwlp6,$ladedauerhlp6' H '$laderestlp6' Min,6',$lademodus,$rfidlp6 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp6name Ladung gestoppt. $bishergeladenlp6 kWh in $ladedauerhlp6 H $laderestlp6 Min mit durchschnittlich $ladegeschwlp6 kW geladen."
						fi
					fi

				else
					sed -i '1i'$startlp6,$jetztlp6,$gelrlp6,$bishergeladenlp6,$ladegeschwlp6,$ladedauerlp6' Min,6',$lademodus,$rfidlp6 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp6name Ladung gestoppt. $bishergeladenlp6 kWh in $ladedauerlp6 Min mit durchschnittlich $ladegeschwlp6 kW geladen."
						fi
					fi

				fi
				openwbDebugLog "CHARGESTAT" 0 "LP6, Ladung gestoppt"

				rm ramdisk/ladeustartlp6
			fi
		fi

	fi
fi

if (( lastmanagementlp7 == 1 )); then
	ladeleistunglp7=$(<ramdisk/llaktuelllp7)
	llkwhlp7=$(<ramdisk/llkwhlp7)
	plugstatlp7=$(<ramdisk/plugstatlp7)
	if (( plugstatlp7 == 1 )); then
		pluggedladungaktlp7=$(<ramdisk/pluggedladungaktlp7)
		if (( pluggedladungaktlp7 == 0 )); then
			echo $llkwhlp7 > ramdisk/pluggedladunglp7startkwh
			echo 1 > ramdisk/pluggedladungaktlp7
		fi
		pluggedladunglp7startkwh=$(<ramdisk/pluggedladunglp7startkwh)
		pluggedladungbishergeladenlp7=$(echo "scale=2;($llkwhlp7 - $pluggedladunglp7startkwh)/1" |bc | sed 's/^\./0./')
		echo $pluggedladungbishergeladenlp7 > ramdisk/pluggedladungbishergeladenlp7
		echo 0 > ramdisk/pluggedtimerlp7
		if (( stopchargeafterdisclp7 == 1 )); then
			boolstopchargeafterdisclp7=$(<ramdisk/boolstopchargeafterdisclp7)
			if (( boolstopchargeafterdisclp7 == 0 )); then
				echo 1 > ramdisk/boolstopchargeafterdisclp7
			fi
		fi
	else
		pluggedtimerlp7=$(<ramdisk/pluggedtimerlp7)
		if (( pluggedtimerlp7 < 6 )); then
			pluggedtimerlp7=$((pluggedtimerlp7 + 1))
			echo $pluggedtimerlp7 > ramdisk/pluggedtimerlp7
		else
			echo 0 > ramdisk/pluggedladungaktlp7
			if (( stopchargeafterdisclp7 == 1 )); then
				boolstopchargeafterdisclp7=$(<ramdisk/boolstopchargeafterdisclp7)
				if (( boolstopchargeafterdisclp7 == 1 )); then
					echo 0 > ramdisk/boolstopchargeafterdisclp7
					mosquitto_pub -r -t "openWB/set/lp/7/ChargePointEnabled" -m "0"
				fi
			fi
		fi
	fi
	if (( ladeleistunglp7 > 100 )); then
		if [ -e ramdisk/ladeustartlp7 ]; then

			ladelstartlp7=$(<ramdisk/ladelstartlp7)
			bishergeladenlp7=$(echo "scale=2;($llkwhlp7 - $ladelstartlp7)/1" |bc | sed 's/^\./0./')
			echo $bishergeladenlp7 > ramdisk/aktgeladenlp7
			gelrlp7=$(echo "scale=2;$bishergeladenlp7 / $durchslp7 * 100" |bc)
			gelrlp7=${gelrlp7%.*}
			echo $gelrlp7 > ramdisk/gelrlp7
			restzeitlp7=$(echo "scale=6;($lademkwhlp7 - $bishergeladenlp7)/ $ladeleistunglp7 * 1000 * 60" |bc)
			restzeitlp7=${restzeitlp7%.*}
			echo $restzeitlp7 > ramdisk/restzeitlp7m
			if (( restzeitlp7 > 60 )); then
				restzeitlp7h=$((restzeitlp7 / 60))
				restzeitlp7r=$((restzeitlp7 % 60))
				echo "$restzeitlp7h H $restzeitlp7r Min" > ramdisk/restzeitlp7
			else
				echo "$restzeitlp7 Min" > ramdisk/restzeitlp7
			fi
		else
			if ((pushbenachrichtigung == "1")) ; then
				if ((pushbstartl == "1")) ; then
					./runs/pushover.sh "$lp7name Ladung gestartet"
				fi
			fi
			openwbDebugLog "CHARGESTAT" 0 "LP7, Ladung gestartet"

			echo 1 > ramdisk/ladungaktivlp7
			touch ramdisk/ladeustartlp7
			echo $lmodus > ramdisk/loglademodus
			echo -e $(date +%d.%m.%y-%H:%M) > ramdisk/ladeustartlp7
			echo -e $(date +%s) > ramdisk/ladeustartslp7
			echo $llkwhlp7 > ramdisk/ladelstartlp7
		fi
		echo 0 > ramdisk/lloglp7
	else
		lloglp7=$(<ramdisk/lloglp7)
		if (( lloglp7 < 5 )); then
			lloglp7=$((lloglp7 + 1))
			echo $lloglp7 > ramdisk/lloglp7
		else
			if [ -e ramdisk/ladeustartlp7 ]; then
				echo 0 > ramdisk/ladungaktivlp7
				echo "--" > ramdisk/restzeitlp7
				ladelstartlp7=$(<ramdisk/ladelstartlp7)
				ladeustartslp7=$(<ramdisk/ladeustartslp7)
				bishergeladenlp7=$(echo "scale=2;($llkwhlp7 - $ladelstartlp7)/1" |bc | sed 's/^\./0./')
				startlp7=$(<ramdisk/ladeustartlp7)
				jetztlp7=$(date +%d.%m.%y-%H:%M)
				jetztslp7=$(date +%s)
				ladedauerlp7=$(((jetztslp7 - ladeustartslp7) / 60 ))
				ladedauerslp7=$((jetztslp7 - ladeustartslp7))
				ladegeschwlp7=$(echo "scale=2;$bishergeladenlp7 * 60 * 60 / $ladedauerslp7" |bc)
				gelrlp7=$(echo "scale=2;$bishergeladenlp7 / $durchslp7 * 100" |bc)
				gelrlp7=${gelrlp7%.*}

				if (( ladedauerlp7 > 60 )); then
					ladedauerhlp7=$((ladedauerlp7 / 60))
					laderestlp7=$((ladedauerlp7 % 60))
					sed -i '1i'$startlp7,$jetztlp7,$gelrlp7,$bishergeladenlp7,$ladegeschwlp7,$ladedauerhlp7' H '$laderestlp7' Min,7',$lademodus,$rfidlp7 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp7name Ladung gestoppt. $bishergeladenlp7 kWh in $ladedauerhlp7 H $laderestlp7 Min mit durchschnittlich $ladegeschwlp7 kW geladen."
						fi
					fi

				else
					sed -i '1i'$startlp7,$jetztlp7,$gelrlp7,$bishergeladenlp7,$ladegeschwlp7,$ladedauerlp7' Min,7',$lademodus,$rfidlp7 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp7name Ladung gestoppt. $bishergeladenlp7 kWh in $ladedauerlp7 Min mit durchschnittlich $ladegeschwlp7 kW geladen."
						fi
					fi

				fi
				openwbDebugLog "CHARGESTAT" 0 "LP7, Ladung gestoppt"

				rm ramdisk/ladeustartlp7
			fi
		fi

	fi
fi

if (( lastmanagementlp8 == 1 )); then
	ladeleistunglp8=$(<ramdisk/llaktuelllp8)
	llkwhlp8=$(<ramdisk/llkwhlp8)
	plugstatlp8=$(<ramdisk/plugstatlp8)
	if (( plugstatlp8 == 1 )); then
		pluggedladungaktlp8=$(<ramdisk/pluggedladungaktlp8)
		if (( pluggedladungaktlp8 == 0 )); then
			echo $llkwhlp8 > ramdisk/pluggedladunglp8startkwh
			echo 1 > ramdisk/pluggedladungaktlp8
		fi
		pluggedladunglp8startkwh=$(<ramdisk/pluggedladunglp8startkwh)
		pluggedladungbishergeladenlp8=$(echo "scale=2;($llkwhlp8 - $pluggedladunglp8startkwh)/1" |bc | sed 's/^\./0./')
		echo $pluggedladungbishergeladenlp8 > ramdisk/pluggedladungbishergeladenlp8
		echo 0 > ramdisk/pluggedtimerlp8
		if (( stopchargeafterdisclp8 == 1 )); then
			boolstopchargeafterdisclp8=$(<ramdisk/boolstopchargeafterdisclp8)
			if (( boolstopchargeafterdisclp8 == 0 )); then
				echo 1 > ramdisk/boolstopchargeafterdisclp8
			fi
		fi
	else
		pluggedtimerlp8=$(<ramdisk/pluggedtimerlp8)
		if (( pluggedtimerlp8 < 6 )); then
			pluggedtimerlp8=$((pluggedtimerlp8 + 1))
			echo $pluggedtimerlp8 > ramdisk/pluggedtimerlp8
		else
			echo 0 > ramdisk/pluggedladungaktlp8
			if (( stopchargeafterdisclp8 == 1 )); then
				boolstopchargeafterdisclp8=$(<ramdisk/boolstopchargeafterdisclp8)
				if (( boolstopchargeafterdisclp8 == 1 )); then
					echo 0 > ramdisk/boolstopchargeafterdisclp8
					mosquitto_pub -r -t "openWB/set/lp/8/ChargePointEnabled" -m "0"
				fi
			fi
		fi
	fi
	if (( ladeleistunglp8 > 100 )); then
		if [ -e ramdisk/ladeustartlp8 ]; then

			ladelstartlp8=$(<ramdisk/ladelstartlp8)
			bishergeladenlp8=$(echo "scale=2;($llkwhlp8 - $ladelstartlp8)/1" |bc | sed 's/^\./0./')
			echo $bishergeladenlp8 > ramdisk/aktgeladenlp8
			gelrlp8=$(echo "scale=2;$bishergeladenlp8 / $durchslp8 * 100" |bc)
			gelrlp8=${gelrlp8%.*}
			echo $gelrlp8 > ramdisk/gelrlp8
			restzeitlp8=$(echo "scale=6;($lademkwhlp8 - $bishergeladenlp8)/ $ladeleistunglp8 * 1000 * 60" |bc)
			restzeitlp8=${restzeitlp8%.*}
			echo $restzeitlp8 > ramdisk/restzeitlp8m
			if (( restzeitlp8 > 60 )); then
				restzeitlp8h=$((restzeitlp8 / 60))
				restzeitlp8r=$((restzeitlp8 % 60))
				echo "$restzeitlp8h H $restzeitlp8r Min" > ramdisk/restzeitlp8
			else
				echo "$restzeitlp8 Min" > ramdisk/restzeitlp8
			fi
		else
			if ((pushbenachrichtigung == "1")) ; then
				if ((pushbstartl == "1")) ; then
					./runs/pushover.sh "$lp8name Ladung gestartet"
				fi
			fi
			openwbDebugLog "CHARGESTAT" 0 "LP8, Ladung gestartet"

			echo 1 > ramdisk/ladungaktivlp8
			touch ramdisk/ladeustartlp8
			echo $lmodus > ramdisk/loglademodus
			echo -e $(date +%d.%m.%y-%H:%M) > ramdisk/ladeustartlp8
			echo -e $(date +%s) > ramdisk/ladeustartslp8
			echo $llkwhlp8 > ramdisk/ladelstartlp8
		fi
		echo 0 > ramdisk/lloglp8
	else
		lloglp8=$(<ramdisk/lloglp8)
		if (( lloglp8 < 5 )); then
			lloglp8=$((lloglp8 + 1))
			echo $lloglp8 > ramdisk/lloglp8
		else
			if [ -e ramdisk/ladeustartlp8 ]; then
				echo 0 > ramdisk/ladungaktivlp8
				echo "--" > ramdisk/restzeitlp8
				ladelstartlp8=$(<ramdisk/ladelstartlp8)
				ladeustartslp8=$(<ramdisk/ladeustartslp8)
				bishergeladenlp8=$(echo "scale=2;($llkwhlp8 - $ladelstartlp8)/1" |bc | sed 's/^\./0./')
				startlp8=$(<ramdisk/ladeustartlp8)
				jetztlp8=$(date +%d.%m.%y-%H:%M)
				jetztslp8=$(date +%s)
				ladedauerlp8=$(((jetztslp8 - ladeustartslp8) / 60 ))
				ladedauerslp8=$((jetztslp8 - ladeustartslp8))
				ladegeschwlp8=$(echo "scale=2;$bishergeladenlp8 * 60 * 60 / $ladedauerslp8" |bc)
				gelrlp8=$(echo "scale=2;$bishergeladenlp8 / $durchslp8 * 100" |bc)
				gelrlp8=${gelrlp8%.*}

				if (( ladedauerlp8 > 60 )); then
					ladedauerhlp8=$((ladedauerlp8 / 60))
					laderestlp8=$((ladedauerlp8 % 60))
					sed -i '1i'$startlp8,$jetztlp8,$gelrlp8,$bishergeladenlp8,$ladegeschwlp8,$ladedauerhlp8' H '$laderestlp8' Min,8',$lademodus,$rfidlp8 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp8name Ladung gestoppt. $bishergeladenlp8 kWh in $ladedauerhlp8 H $laderestlp8 Min mit durchschnittlich $ladegeschwlp8 kW geladen."
						fi
					fi

				else
					sed -i '1i'$startlp8,$jetztlp8,$gelrlp8,$bishergeladenlp8,$ladegeschwlp8,$ladedauerlp8' Min,8',$lademodus,$rfidlp8 $monthlyfile
					if ((pushbenachrichtigung == "1")) ; then
						if ((pushbstopl == "1")) ; then
							./runs/pushover.sh "$lp8name Ladung gestoppt. $bishergeladenlp8 kWh in $ladedauerlp8 Min mit durchschnittlich $ladegeschwlp8 kW geladen."
						fi
					fi

				fi
				openwbDebugLog "CHARGESTAT" 0 "LP8, Ladung gestoppt"

				rm ramdisk/ladeustartlp8
			fi
		fi

	fi
fi
