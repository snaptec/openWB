#!/bin/bash
sudo iwlist wlan0 scan |grep ESSID: > /var/www/html/openWB/ramdisk/wifilist.txt
sudo iwconfig wlan0|grep ESSID: > /var/www/html/openWB/ramdisk/wifilist2.txt
input=$(</var/www/html/openWB/ramdisk/wifilist2.txt)
temp="${input#*ESSID:}"
awk 'BEGIN{print " "} {for(i=1;i<=NF;i++)print "<br> " $i " "} END{print " "}' /var/www/html/openWB/ramdisk/wifilist.txt > /var/www/html/openWB/ramdisk/wifilist1.txt
cat  /var/www/html/openWB/ramdisk/wifilist1.txt
echo "<br>"
echo "<br>"
echo "aktuell verbunden mit ESSID: <b> " $temp  "</b>"