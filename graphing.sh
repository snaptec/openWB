#!/bin/bash
graphing(){
#Live Graphing
if (( speichervorhanden == 1 )); then
	echo $speicherleistung >> /var/www/html/openWB/ramdisk/speicher-live.graph
fi
echo $((pvwatt * -1)) >> /var/www/html/openWB/ramdisk/pv-live.graph
echo $wattbezugint >> /var/www/html/openWB/ramdisk/evu-live.graph
echo $ladeleistung >> /var/www/html/openWB/ramdisk/ev-live.graph
echo $soc >> /var/www/html/openWB/ramdisk/soc-live.graph
date +%H:%M >> /var/www/html/openWB/ramdisk/time-live.graph
if ! [[ $livegraph == $re ]] ; then      
	livegraph=$((livegraph * 6 ))
	if ! [[ $livegraph =~ $re ]] ; then
	livegraph="30"
	fi
	echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/pv-live.graph)" > /var/www/html/openWB/ramdisk/pv-live.graph
	echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/soc-live.graph)" > /var/www/html/openWB/ramdisk/soc-live.graph
	echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/evu-live.graph)" > /var/www/html/openWB/ramdisk/evu-live.graph
	echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/ev-live.graph)" > /var/www/html/openWB/ramdisk/ev-live.graph 
	echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/time-live.graph)" > /var/www/html/openWB/ramdisk/time-live.graph
	if ((speichervorhanden == 1 )); then
		echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/speicher-live.graph)" > /var/www/html/openWB/ramdisk/speicher-live.graph
	fi
fi
#Long Time Graphing
if (( graphtimer == 1 )) || (( graphtimer == 4 )); then
echo $((pvwatt * -1)) >> /var/www/html/openWB/ramdisk/pv.graph
echo $wattbezugint >> /var/www/html/openWB/ramdisk/evu.graph
echo $soc >> /var/www/html/openWB/ramdisk/soc.graph
echo $ladeleistung >> /var/www/html/openWB/ramdisk/ev.graph
if (( speichervorhanden == 1 )); then
	echo $speicherleistung >> /var/www/html/openWB/ramdisk/speicher.graph
fi
date +%H:%M >> /var/www/html/openWB/ramdisk/time.graph
echo "$(tail -720 /var/www/html/openWB/ramdisk/pv.graph)" > /var/www/html/openWB/ramdisk/pv.graph
echo "$(tail -720 /var/www/html/openWB/ramdisk/evu.graph)" > /var/www/html/openWB/ramdisk/evu.graph
echo "$(tail -720 /var/www/html/openWB/ramdisk/soc.graph)" > /var/www/html/openWB/ramdisk/soc.graph
echo "$(tail -720 /var/www/html/openWB/ramdisk/ev.graph)" > /var/www/html/openWB/ramdisk/ev.graph 
echo "$(tail -720 /var/www/html/openWB/ramdisk/time.graph)" > /var/www/html/openWB/ramdisk/time.graph
if ((speichervorhanden == 1 )); then
	echo "$(tail -720 /var/www/html/openWB/ramdisk/speicher.graph)" > /var/www/html/openWB/ramdisk/speicher.graph
fi

fi
}
