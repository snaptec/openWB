#!/bin/bash
. openwb.conf

ladeleistung=$(<ramdisk/llaktuell)
llkwh=$(<ramdisk/llkwh)
soc=$(<ramdisk/soc)
soc1=$(<ramdisk/soc1)
lmodus=$(</var/www/html/openWB/ramdisk/lademodus)
lademodus=$(</var/www/html/openWB/ramdisk/loglademodus)

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

if (( ladeleistung > 500 )); then
	if [ -e ramdisk/ladeustart ]; then

		ladelstart=$(<ramdisk/ladelstart)
		bishergeladen=$(echo "scale=3;($llkwh - $ladelstart)/1" |bc | sed 's/^\./0./')
		echo $bishergeladen > ramdisk/aktgeladen
		gelrlp1=$(echo "scale=3;$bishergeladen / $durchslp1 * 100" |bc)
		gelrlp1=${gelrlp1%.*}
		echo $gelrlp1 > ramdisk/gelrlp1
		restzeitlp1=$(echo "scale=6;($lademkwh - $bishergeladen)/ $ladeleistung * 1000 * 60" |bc)
		restzeitlp1=${restzeitlp1%.*}
		if (( restzeitlp1 > 60 )); then
			restzeitlp1h=$((restzeitlp1 / 60))
			restzeitlp1r=$((restzeitlp1 % 60))
			echo "$restzeitlp1h H $restzeitlp1r Min" > ramdisk/restzeitlp1
		else
			echo "$restzeitlp1 Min" > ramdisk/restzeitlp1
		fi
	else
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
	fi
	echo 0 > ramdisk/llog1
else
	llog1=$(<ramdisk/llog1)
	if (( llog1 < 5 )); then
		llog1=$((llog1 + 1))
		echo $llog1 > ramdisk/llog1
	else
		if [ -e ramdisk/ladeustart ]; then
			echo "--" > ramdisk/restzeitlp1
			ladelstart=$(<ramdisk/ladelstart)
			ladeustarts=$(<ramdisk/ladeustarts)
			bishergeladen=$(echo "scale=3;($llkwh - $ladelstart)/1" |bc | sed 's/^\./0./')
			start=$(<ramdisk/ladeustart)
			jetzt=$(date +%d.%m.%y-%H:%M)
			jetzts=$(date +%s)
			ladedauer=$(((jetzts - ladeustarts) / 60 ))
			ladedauers=$((jetzts - ladeustarts))
			ladegeschw=$(echo "scale=3;$bishergeladen * 60 * 60 / $ladedauers" |bc)
			gelrlp1=$(echo "scale=3;$bishergeladen / $durchslp1 * 100" |bc)
			gelrlp1=${gelrlp1%.*}
			if (( ladedauer > 60 )); then
				ladedauerh=$((ladedauer / 60))
				laderest=$((ladedauer % 60))
				sed -i '1i'$start,$jetzt,$gelrlp1,$bishergeladen,$ladegeschw,$ladedauerh' H '$laderest' Min,1',$lademodus web/ladelog
				if ((pushbenachrichtigung == "1")) ; then
					if ((pushbstopl == "1")) ; then
						./runs/pushover.sh "$lp1name Ladung gestoppt. $bishergeladen kWh in $ladedauerh H $laderest Min mit durchschnittlich $ladegeschw kW geladen$soctext"
					fi
				fi

			else
				sed -i '1i'$start,$jetzt,$gelrlp1,$bishergeladen,$ladegeschw,$ladedauer' Min,1 ',$lademodus web/ladelog
				if ((pushbenachrichtigung == "1")) ; then
					if ((pushbstopl == "1")) ; then
						./runs/pushover.sh "$lp1name Ladung gestoppt. $bishergeladen kWh in $ladedauer Min mit durchschnittlich $ladegeschw kW geladen$soctext"
					fi
				fi

			fi

			rm ramdisk/ladeustart
		fi
	fi
fi

if (( lastmanagement == 1 )); then

ladeleistungs1=$(<ramdisk/llaktuells1)
llkwhs1=$(<ramdisk/llkwhs1)
if (( ladeleistungs1 > 500 )); then
	if [ -e ramdisk/ladeustarts1 ]; then

		ladelstarts1=$(<ramdisk/ladelstarts1)
		bishergeladens1=$(echo "scale=3;($llkwhs1 - $ladelstarts1)/1" |bc | sed 's/^\./0./')
		echo $bishergeladens1 > ramdisk/aktgeladens1
		gelrlp2=$(echo "scale=3;$bishergeladens1 / $durchslp2 * 100" |bc)
		gelrlp2=${gelrlp2%.*}
		echo $gelrlp2 > ramdisk/gelrlp2
		restzeitlp2=$(echo "scale=6;($lademkwhs1 - $bishergeladens1)/ $ladeleistungs1 * 1000 * 60" |bc)
		restzeitlp2=${restzeitlp2%.*}
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
			echo "--" > ramdisk/restzeitlp2
			ladelstarts1=$(<ramdisk/ladelstarts1)
			ladeustartss1=$(<ramdisk/ladeustartss1)
			bishergeladens1=$(echo "scale=3;($llkwhs1 - $ladelstarts1)/1" |bc | sed 's/^\./0./')
			starts1=$(<ramdisk/ladeustarts1)
			jetzts1=$(date +%d.%m.%y-%H:%M)
			jetztss1=$(date +%s)
			ladedauers1=$(((jetztss1 - ladeustartss1) / 60 ))
			ladedauerss1=$((jetztss1 - ladeustartss1))
			ladegeschws1=$(echo "scale=3;$bishergeladens1 * 60 * 60 / $ladedauerss1" |bc)
			gelrlp2=$(echo "scale=3;$bishergeladens1 / $durchslp2 * 100" |bc)
			gelrlp2=${gelrlp2%.*}
			if (( ladedauers1 > 60 )); then
				ladedauerhs1=$((ladedauers1 / 60))
				laderests1=$((ladedauers1 % 60))
				sed -i '1i'$starts1,$jetzts1,$gelrlp2,$bishergeladens1,$ladegeschws1,$ladedauerhs1' H '$laderests1' Min,2',$lademodus web/ladelog
				if ((pushbenachrichtigung == "1")) ; then
					if ((pushbstopl == "1")) ; then
						./runs/pushover.sh "$lp2name Ladung gestoppt. $bishergeladens1 kWh in $ladedauerhs1 H $laderests1 Min mit durchschnittlich $ladegeschws1 kW geladen$soctext1"
					fi
				fi
			else
				sed -i '1i'$starts1,$jetzts1,$gelrlp2,$bishergeladens1,$ladegeschws1,$ladedauers1' Min,2',$lademodus web/ladelog
				if ((pushbenachrichtigung == "1")) ; then
					if ((pushbstopl == "1")) ; then
						./runs/pushover.sh "$lp2name Ladung gestoppt. $bishergeladens1 kWh in $ladedauers1 Min mit durchschnittlich $ladegeschws1 kW geladen$soctext1"
					fi
				fi

			fi
			rm ramdisk/ladeustarts1
		fi
	fi

fi
fi

if (( lastmanagements2 == 1 )); then
ladeleistungs2=$(<ramdisk/llaktuells2)
llkwhs2=$(<ramdisk/llkwhs2)
if (( ladeleistungs2 > 500 )); then
	if [ -e ramdisk/ladeustarts2 ]; then

		ladelstarts2=$(<ramdisk/ladelstarts2)
		bishergeladens2=$(echo "scale=3;($llkwhs2 - $ladelstarts2)/1" |bc | sed 's/^\./0./')
		echo $bishergeladens2 > ramdisk/aktgeladens2
		gelrlp3=$(echo "scale=3;$bishergeladens2 / $durchslp3 * 100" |bc)
		gelrlp3=${gelrlp3%.*}
		echo $gelrlp3 > ramdisk/gelrlp3
		restzeitlp3=$(echo "scale=6;($lademkwhs2 - $bishergeladens2)/ $ladeleistungs2 * 1000 * 60" |bc)
		restzeitlp3=${restzeitlp3%.*}
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
			echo "--" > ramdisk/restzeitlp3
			ladelstarts2=$(<ramdisk/ladelstarts2)
			ladeustartss2=$(<ramdisk/ladeustartss2)
			bishergeladens2=$(echo "scale=3;($llkwhs2 - $ladelstarts2)/1" |bc | sed 's/^\./0./')
			starts2=$(<ramdisk/ladeustarts2)
			jetzts2=$(date +%d.%m.%y-%H:%M)
			jetztss2=$(date +%s)
			ladedauers2=$(((jetztss2 - ladeustartss2) / 60 ))
			ladedauerss2=$((jetztss2 - ladeustartss2))
			ladegeschws2=$(echo "scale=3;$bishergeladens2 * 60 * 60 / $ladedauerss2" |bc)
			gelrlp3=$(echo "scale=3;$bishergeladens2 / $durchslp3 * 100" |bc)
			gelrlp3=${gelrlp3%.*}
	
			if (( ladedauers2 > 60 )); then
				ladedauerhs2=$((ladedauers2 / 60))
				laderests2=$((ladedauers2 % 60))
				sed -i '1i'$starts2,$jetzts2,$gelrlp3,$bishergeladens2,$ladegeschws2,$ladedauerhs2' H '$laderests2' Min,3',$lademodus web/ladelog
				if ((pushbenachrichtigung == "1")) ; then
					if ((pushbstopl == "1")) ; then
						./runs/pushover.sh "$lp3name Ladung gestoppt. $bishergeladens2 kWh in $ladedauerhs2 H $laderests2 Min mit durchschnittlich $ladegeschws2 kW geladen."
					fi
				fi

			else
				sed -i '1i'$starts2,$jetzts2,$gelrlp3,$bishergeladens2,$ladegeschws2,$ladedauers2' Min,3',$lademodus web/ladelog
				if ((pushbenachrichtigung == "1")) ; then
					if ((pushbstopl == "1")) ; then
						./runs/pushover.sh "$lp3name Ladung gestoppt. $bishergeladens2 kWh in $ladedauers2 Min mit durchschnittlich $ladegeschws2 kW geladen."
					fi
				fi

			fi
			rm ramdisk/ladeustarts2
		fi
	fi

fi
fi


