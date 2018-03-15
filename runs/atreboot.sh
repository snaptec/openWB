#!/bin/bash
#Ramdisk mit initialen Werten befüllen nach neustart
sleep 10
echo 6 > /var/www/html/openWB/ramdisk/llsoll
touch /var/www/html/openWB/ramdisk/wattbezug
touch /var/www/html/openWB/ramdisk/ladestatus
touch /var/www/html/openWB/ramdisk/lademodus
touch /var/www/html/openWB/ramdisk/llaktuell
touch /var/www/html/openWB/ramdisk/pvwatt
touch /var/www/html/openWB/ramdisk/soc
touch /var/www/html/openWB/ramdisk/lla1
touch /var/www/html/openWB/ramdisk/lla2
touch /var/www/html/openWB/ramdisk/lla3
echo 0 > /var/www/html/openWB/ramdisk/wattbezug
echo 0 > /var/www/html/openWB/ramdisk/ladestatus
echo 0 > /var/www/html/openWB/ramdisk/lademodus
echo 0 > /var/www/html/openWB/ramdisk/llaktuell
echo 0 > /var/www/html/openWB/ramdisk/pvwatt
echo 0 > /var/www/html/openWB/ramdisk/soc
chmod 777 /var/www/html/openWB/ramdisk/*
chmod 777 /var/www/html/openWB/web/lade.log
