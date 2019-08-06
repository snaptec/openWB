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
	echo $lasttag > ramdisk/rfidlasttag
	echo 0 > ramdisk/readtag
fi
}
