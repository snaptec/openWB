#!/bin/bash
. openwb.conf

ladeleistung=$(<ramdisk/llaktuell)
llkwh=$(<ramdisk/llkwh)
soc=$(<ramdisk/soc)
soc1=$(<ramdisk/soc1)
nachtladenstate=$(</var/www/html/openWB/ramdisk/nachtladenstate)
nachtladen2state=$(</var/www/html/openWB/ramdisk/nachtladen2state)
rfidlp1=$(<ramdisk/rfidlp1)
rfidlp2=$(<ramdisk/rfidlp2)
if ((nachtladenstate == 0)) || ((nachtladen2state == 0)); then
	lmodus=$(</var/www/html/openWB/ramdisk/lademodus)
else
	lmodus=7
fi
if [ -e ramdisk/loglademodus ]; then
	lademodus=$(</var/www/html/openWB/ramdisk/loglademodus)
fi
if ((soc > 0)); then
	soctext=$(echo ", bei $soc %SoC")
else
	soctext=$(echo ".")
fi
if ((soc1 > 0)); then
	soctext1=$(echo ", bei $soc1 %SoC")
else
	soctext1=$(echo ".")
fi
plugstat=$(<ramdisk/plugstat)
if ((plugstat == 1)); then
	pluggedladungaktlp1=$(<ramdisk/pluggedladungaktlp1)
	if ((pluggedladungaktlp1 == 0)); then
		echo $llkwh >ramdisk/pluggedladunglp1startkwh
		echo 1 >ramdisk/pluggedladungaktlp1
	fi
	pluggedladunglp1startkwh=$(<ramdisk/pluggedladunglp1startkwh)
	pluggedladungbishergeladen=$(echo "scale=2;($llkwh - $pluggedladunglp1startkwh)/1" | bc | sed 's/^\./0./')
	echo $pluggedladungbishergeladen >ramdisk/pluggedladungbishergeladen
	echo 0 >ramdisk/pluggedtimer1
else
	pluggedtimer1=$(<ramdisk/pluggedtimer1)
	if ((pluggedtimer1 < 3)); then
		pluggedtimer1=$((pluggedtimer1 + 1))
		echo $pluggedtimer1 >ramdisk/pluggedtimer1
	else
		echo 0 >ramdisk/pluggedladungaktlp1
	fi
fi

if ((ladeleistung > 500)); then
	if [ -e ramdisk/ladeustart ]; then

		ladelstart=$(<ramdisk/ladelstart)
		bishergeladen=$(echo "scale=2;($llkwh - $ladelstart)/1" | bc | sed 's/^\./0./')
		echo $bishergeladen >ramdisk/aktgeladen
		gelrlp1=$(echo "scale=2;$bishergeladen / $durchslp1 * 100" | bc)
		gelrlp1=${gelrlp1%.*}
		echo $gelrlp1 >ramdisk/gelrlp1
		restzeitlp1=$(echo "scale=6;($lademkwh - $bishergeladen)/ $ladeleistung * 1000 * 60" | bc)
		restzeitlp1=${restzeitlp1%.*}
		echo $restzeitlp1 >ramdisk/restzeitlp1m
		if ((restzeitlp1 > 60)); then
			restzeitlp1h=$((restzeitlp1 / 60))
			restzeitlp1r=$((restzeitlp1 % 60))
			echo "$restzeitlp1h H $restzeitlp1r Min" >ramdisk/restzeitlp1
		else
			echo "$restzeitlp1 Min" >ramdisk/restzeitlp1
		fi
	else
		echo 1 >ramdisk/ladungaktivlp1
		touch ramdisk/ladeustart
		echo -e $(date +%d.%m.%y-%H:%M) >ramdisk/ladeustart
		echo -e $(date +%s) >ramdisk/ladeustarts
		echo $lmodus >ramdisk/loglademodus
		echo $llkwh >ramdisk/ladelstart
		if ((pushbenachrichtigung == "1")); then
			if ((pushbstartl == "1")); then
				./runs/pushover.sh "$lp1name Ladung gestartet$soctext"
			fi
		fi
		echo "$date LP1, Ladung gestartet." >>ramdisk/ladestatus.log

	fi
	echo 0 >ramdisk/llog1
else
	llog1=$(<ramdisk/llog1)
	if ((llog1 < 5)); then
		llog1=$((llog1 + 1))
		echo $llog1 >ramdisk/llog1
	else
		if [ -e ramdisk/ladeustart ]; then
			echo 0 >ramdisk/ladungaktivlp1
			echo "--" >ramdisk/restzeitlp1
			ladelstart=$(<ramdisk/ladelstart)
			ladeustarts=$(<ramdisk/ladeustarts)
			bishergeladen=$(echo "scale=2;($llkwh - $ladelstart)/1" | bc | sed 's/^\./0./')
			start=$(<ramdisk/ladeustart)
			jetzt=$(date +%d.%m.%y-%H:%M)
			jetzts=$(date +%s)
			ladedauer=$(((jetzts - ladeustarts) / 60))
			ladedauers=$((jetzts - ladeustarts))
			ladegeschw=$(echo "scale=2;$bishergeladen * 60 * 60 / $ladedauers" | bc)
			gelrlp1=$(echo "scale=2;$bishergeladen / $durchslp1 * 100" | bc)
			gelrlp1=${gelrlp1%.*}
			if ((ladedauer > 60)); then
				ladedauerh=$((ladedauer / 60))
				laderest=$((ladedauer % 60))
				sed -i '1i'$start,$jetzt,$gelrlp1,$bishergeladen,$ladegeschw,$ladedauerh' H '$laderest' Min,1',$lademodus,$rfidlp1 web/ladelog
				if ((pushbenachrichtigung == "1")); then
					if ((pushbstopl == "1")); then
						./runs/pushover.sh "$lp1name Ladung gestoppt. $bishergeladen kWh in $ladedauerh H $laderest Min mit durchschnittlich $ladegeschw kW geladen$soctext"
					fi
				fi

			else
				sed -i '1i'$start,$jetzt,$gelrlp1,$bishergeladen,$ladegeschw,$ladedauer' Min,1 ',$lademodus web/ladelog
				if ((pushbenachrichtigung == "1")); then
					if ((pushbstopl == "1")); then
						./runs/pushover.sh "$lp1name Ladung gestoppt. $bishergeladen kWh in $ladedauer Min mit durchschnittlich $ladegeschw kW geladen$soctext"
					fi
				fi

			fi
			echo "$date LP1, Ladung gestoppt" >>ramdisk/ladestatus.log

			rm ramdisk/ladeustart
		fi
	fi
fi

if ((lastmanagement == 1)); then
	ladeleistungs1=$(<ramdisk/llaktuells1)
	llkwhs1=$(<ramdisk/llkwhs1)
	plugstatlp2=$(<ramdisk/plugstats1)
	if ((plugstatlp2 == 1)); then
		pluggedladungaktlp2=$(<ramdisk/pluggedladungaktlp2)
		if ((pluggedladungaktlp2 == 0)); then
			echo $llkwhs1 >ramdisk/pluggedladunglp2startkwh
			echo 1 >ramdisk/pluggedladungaktlp2
		fi
		pluggedladunglp2startkwh=$(<ramdisk/pluggedladunglp2startkwh)
		pluggedladungbishergeladenlp2=$(echo "scale=2;($llkwhs1 - $pluggedladunglp2startkwh)/1" | bc | sed 's/^\./0./')
		echo $pluggedladungbishergeladenlp2 >ramdisk/pluggedladungbishergeladenlp2
		echo 0 >ramdisk/pluggedtimer2
	else
		pluggedtimer2=$(<ramdisk/pluggedtimer2)
		if ((pluggedtimer2 < 3)); then
			pluggedtimer2=$((pluggedtimer2 + 1))
			echo $pluggedtimer2 >ramdisk/pluggedtimer2
		else
			echo 0 >ramdisk/pluggedladungaktlp2
		fi
	fi

	if ((ladeleistungs1 > 500)); then
		if [ -e ramdisk/ladeustarts1 ]; then

			ladelstarts1=$(<ramdisk/ladelstarts1)
			bishergeladens1=$(echo "scale=2;($llkwhs1 - $ladelstarts1)/1" | bc | sed 's/^\./0./')
			echo $bishergeladens1 >ramdisk/aktgeladens1
			gelrlp2=$(echo "scale=2;$bishergeladens1 / $durchslp2 * 100" | bc)
			gelrlp2=${gelrlp2%.*}
			echo $gelrlp2 >ramdisk/gelrlp2
			restzeitlp2=$(echo "scale=6;($lademkwhs1 - $bishergeladens1)/ $ladeleistungs1 * 1000 * 60" | bc)
			restzeitlp2=${restzeitlp2%.*}
			echo $restzeitlp2 >ramdisk/restzeitlp2m

			if ((restzeitlp2 > 60)); then
				restzeitlp2h=$((restzeitlp2 / 60))
				restzeitlp2r=$((restzeitlp2 % 60))
				echo "$restzeitlp2h H $restzeitlp2r Min" >ramdisk/restzeitlp2
			else
				echo "$restzeitlp2 Min" >ramdisk/restzeitlp2
			fi

		else
			if ((pushbenachrichtigung == "1")); then
				if ((pushbstartl == "1")); then
					./runs/pushover.sh "$lp2name Ladung gestartet$soctext1"
				fi
			fi
			echo "$date LP2, Ladung gestartet" >>ramdisk/ladestatus.log

			echo 1 >ramdisk/ladungaktivlp2
			touch ramdisk/ladeustarts1
			echo $lmodus >ramdisk/loglademodus
			echo -e $(date +%d.%m.%y-%H:%M) >ramdisk/ladeustarts1
			echo -e $(date +%s) >ramdisk/ladeustartss1
			echo $llkwhs1 >ramdisk/ladelstarts1
		fi
		echo 0 >ramdisk/llogs1
	else

		llogs1=$(<ramdisk/llogs1)
		if ((llogs1 < 5)); then
			llogs1=$((llogs1 + 1))
			echo $llogs1 >ramdisk/llogs1
		else
			if [ -e ramdisk/ladeustarts1 ]; then
				echo 0 >ramdisk/ladungaktivlp2
				echo "--" >ramdisk/restzeitlp2
				ladelstarts1=$(<ramdisk/ladelstarts1)
				ladeustartss1=$(<ramdisk/ladeustartss1)
				bishergeladens1=$(echo "scale=2;($llkwhs1 - $ladelstarts1)/1" | bc | sed 's/^\./0./')
				starts1=$(<ramdisk/ladeustarts1)
				jetzts1=$(date +%d.%m.%y-%H:%M)
				jetztss1=$(date +%s)
				ladedauers1=$(((jetztss1 - ladeustartss1) / 60))
				ladedauerss1=$((jetztss1 - ladeustartss1))
				ladegeschws1=$(echo "scale=2;$bishergeladens1 * 60 * 60 / $ladedauerss1" | bc)
				gelrlp2=$(echo "scale=2;$bishergeladens1 / $durchslp2 * 100" | bc)
				gelrlp2=${gelrlp2%.*}
				if ((ladedauers1 > 60)); then
					ladedauerhs1=$((ladedauers1 / 60))
					laderests1=$((ladedauers1 % 60))
					sed -i '1i'$starts1,$jetzts1,$gelrlp2,$bishergeladens1,$ladegeschws1,$ladedauerhs1' H '$laderests1' Min,2',$lademodus,$rfidlp2 web/ladelog
					if ((pushbenachrichtigung == "1")); then
						if ((pushbstopl == "1")); then
							./runs/pushover.sh "$lp2name Ladung gestoppt. $bishergeladens1 kWh in $ladedauerhs1 H $laderests1 Min mit durchschnittlich $ladegeschws1 kW geladen$soctext1"
						fi
					fi
				else
					sed -i '1i'$starts1,$jetzts1,$gelrlp2,$bishergeladens1,$ladegeschws1,$ladedauers1' Min,2',$lademodus web/ladelog
					if ((pushbenachrichtigung == "1")); then
						if ((pushbstopl == "1")); then
							./runs/pushover.sh "$lp2name Ladung gestoppt. $bishergeladens1 kWh in $ladedauers1 Min mit durchschnittlich $ladegeschws1 kW geladen$soctext1"
						fi
					fi

				fi
				echo "$date LP2, Ladung gestoppt" >>ramdisk/ladestatus.log

				rm ramdisk/ladeustarts1
			fi
		fi

	fi
fi

if ((lastmanagements2 == 1)); then
	ladeleistungs2=$(<ramdisk/llaktuells2)
	llkwhs2=$(<ramdisk/llkwhs2)
	if ((ladeleistungs2 > 500)); then
		if [ -e ramdisk/ladeustarts2 ]; then

			ladelstarts2=$(<ramdisk/ladelstarts2)
			bishergeladens2=$(echo "scale=2;($llkwhs2 - $ladelstarts2)/1" | bc | sed 's/^\./0./')
			echo $bishergeladens2 >ramdisk/aktgeladens2
			gelrlp3=$(echo "scale=2;$bishergeladens2 / $durchslp3 * 100" | bc)
			gelrlp3=${gelrlp3%.*}
			echo $gelrlp3 >ramdisk/gelrlp3
			restzeitlp3=$(echo "scale=6;($lademkwhs2 - $bishergeladens2)/ $ladeleistungs2 * 1000 * 60" | bc)
			restzeitlp3=${restzeitlp3%.*}
			echo $restzeitlp3 >ramdisk/restzeitlp3m
			if ((restzeitlp3 > 60)); then
				restzeitlp3h=$((restzeitlp3 / 60))
				restzeitlp3r=$((restzeitlp3 % 60))
				echo "$restzeitlp3h H $restzeitlp3r Min" >ramdisk/restzeitlp3
			else
				echo "$restzeitlp3 Min" >ramdisk/restzeitlp3
			fi
		else
			if ((pushbenachrichtigung == "1")); then
				if ((pushbstartl == "1")); then
					./runs/pushover.sh "$lp3name Ladung gestartet"
				fi
			fi
			echo "$date LP3, Ladung gestartet" >>ramdisk/ladestatus.log

			echo 1 >ramdisk/ladungaktivlp3
			touch ramdisk/ladeustarts2
			echo $lmodus >ramdisk/loglademodus
			echo -e $(date +%d.%m.%y-%H:%M) >ramdisk/ladeustarts2
			echo -e $(date +%s) >ramdisk/ladeustartss2
			echo $llkwhs2 >ramdisk/ladelstarts2
		fi
		echo 0 >ramdisk/llogs2
	else
		llogs2=$(<ramdisk/llogs2)
		if ((llogs2 < 5)); then
			llogs2=$((llogs2 + 1))
			echo $llogs2 >ramdisk/llogs2
		else
			if [ -e ramdisk/ladeustarts2 ]; then
				echo 0 >ramdisk/ladungaktivlp3
				echo "--" >ramdisk/restzeitlp3
				ladelstarts2=$(<ramdisk/ladelstarts2)
				ladeustartss2=$(<ramdisk/ladeustartss2)
				bishergeladens2=$(echo "scale=2;($llkwhs2 - $ladelstarts2)/1" | bc | sed 's/^\./0./')
				starts2=$(<ramdisk/ladeustarts2)
				jetzts2=$(date +%d.%m.%y-%H:%M)
				jetztss2=$(date +%s)
				ladedauers2=$(((jetztss2 - ladeustartss2) / 60))
				ladedauerss2=$((jetztss2 - ladeustartss2))
				ladegeschws2=$(echo "scale=2;$bishergeladens2 * 60 * 60 / $ladedauerss2" | bc)
				gelrlp3=$(echo "scale=2;$bishergeladens2 / $durchslp3 * 100" | bc)
				gelrlp3=${gelrlp3%.*}

				if ((ladedauers2 > 60)); then
					ladedauerhs2=$((ladedauers2 / 60))
					laderests2=$((ladedauers2 % 60))
					sed -i '1i'$starts2,$jetzts2,$gelrlp3,$bishergeladens2,$ladegeschws2,$ladedauerhs2' H '$laderests2' Min,3',$lademodus web/ladelog
					if ((pushbenachrichtigung == "1")); then
						if ((pushbstopl == "1")); then
							./runs/pushover.sh "$lp3name Ladung gestoppt. $bishergeladens2 kWh in $ladedauerhs2 H $laderests2 Min mit durchschnittlich $ladegeschws2 kW geladen."
						fi
					fi

				else
					sed -i '1i'$starts2,$jetzts2,$gelrlp3,$bishergeladens2,$ladegeschws2,$ladedauers2' Min,3',$lademodus web/ladelog
					if ((pushbenachrichtigung == "1")); then
						if ((pushbstopl == "1")); then
							./runs/pushover.sh "$lp3name Ladung gestoppt. $bishergeladens2 kWh in $ladedauers2 Min mit durchschnittlich $ladegeschws2 kW geladen."
						fi
					fi

				fi
				echo "$date LP3, Ladung gestoppt" >>ramdisk/ladestatus.log

				rm ramdisk/ladeustarts2
			fi
		fi

	fi
fi
