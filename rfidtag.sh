#!/bin/bash

rfid() {
lasttag=$(<ramdisk/readtag)
if [[ $lasttag != "0" ]]; then
	if [ $lasttag == $rfidlp1c1 ] || [ $lasttag == $rfidlp1c2 ]  || [ $lasttag == $rfidlp1c3 ] ; then
	       echo $lasttag > ramdisk/rfidlp1
	fi	       
	if [ $lasttag == $rfidlp2c1 ] || [ $lasttag == $rfidlp2c2 ]  || [ $lasttag == $rfidlp2c3 ] ; then
	       echo $lasttag > ramdisk/rfidlp2
	fi
	if [ $lasttag == $rfidstop ] || [ $lasttag == $rfidstop2 ] || [ $lasttag == $rfidstop3 ] ; then
		echo 3 > ramdisk/lademodus
	fi	

	if [ $lasttag == $rfidsofort ] || [ $lasttag == $rfidsofort2 ] || [ $lasttag == $rfidsofort3 ]  ; then
		echo 0 > ramdisk/lademodus
	fi	

	if [ $lasttag == $rfidminpv ] || [ $lasttag == $rfidminpv2 ] || [ $lasttag == $rfidminpv3 ]  ; then
		echo 1 > ramdisk/lademodus
	fi	

	if [ $lasttag == $rfidnurpv ] || [ $lasttag == $rfidnurpv2 ] || [ $lasttag == $rfidnurpv3 ]   ; then
		echo 2 > ramdisk/lademodus
	fi	

	if [ $lasttag == $rfidstandby ] || [ $lasttag == $rfidstandby2 ] || [ $lasttag == $rfidstandby3 ] ; then
		echo 4 > ramdisk/lademodus
	fi
	if [ $lasttag == $rfidlp1start1 ] || [ $lasttag == $rfidlp1start2 ] || [ $lasttag == $rfidlp1start3 ] ; then
		mosquitto_pub -r -t openWB/set/lp1/ChargePointEnabled -m "1"
	fi
	if [ $lasttag == $rfidlp2start1 ] || [ $lasttag == $rfidlp2start2 ] || [ $lasttag == $rfidlp2start3 ] ; then
		mosquitto_pub -r -t openWB/set/lp2/ChargePointEnabled -m "1"
	fi
	rfidlist=$(<ramdisk/AllowedRfidsForLp1)
	for i in $(echo $rfidlist | sed "s/,/ /g")
	do
		if [ $lasttag == $i ] ; then
			mosquitto_pub -r -t openWB/set/lp1/ChargePointEnabled -m "1"
		fi
	done
	echo $lasttag > ramdisk/rfidlasttag
	echo 0 > ramdisk/readtag
fi
}
