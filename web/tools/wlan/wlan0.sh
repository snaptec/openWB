#!/bin/bash

ramdiskdir=/var/www/html/openWB/ramdisk

sudo iwlist wlan0 scan |grep "ESSID:"|sort|uniq > ${ramdiskdir}/wifilist.txt
sudo iwconfig wlan0|grep ESSID: > ${ramdiskdir}/wifilist2.txt
input=$(<${ramdiskdir}/wifilist2.txt)
temp="${input#*ESSID:}"
while read  line
do
  echo "${line}<br>" 
done <${ramdiskdir}/wifilist.txt
echo "<br>"
echo "<br>"
echo "aktuell verbunden mit ESSID: <b> " $temp  "</b>"
