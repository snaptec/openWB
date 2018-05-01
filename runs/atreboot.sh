#!/bin/bash
#Ramdisk mit initialen Werten befüllen nach neustart
sleep 10
echo 0 > /var/www/html/openWB/ramdisk/llsoll
touch /var/www/html/openWB/ramdisk/wattbezug
touch /var/www/html/openWB/ramdisk/ladestatus
touch /var/www/html/openWB/ramdisk/lademodus
touch /var/www/html/openWB/ramdisk/llaktuell
touch /var/www/html/openWB/ramdisk/llaktuells1
touch /var/www/html/openWB/ramdisk/pvwatt
touch /var/www/html/openWB/ramdisk/soc
touch /var/www/html/openWB/ramdisk/soc1
touch /var/www/html/openWB/ramdisk/lla1
touch /var/www/html/openWB/ramdisk/lla2
touch /var/www/html/openWB/ramdisk/lla3
touch /var/www/html/openWB/ramdisk/llkombiniert
touch /var/www/html/openWB/ramdisk/llas11
touch /var/www/html/openWB/ramdisk/llas12
touch /var/www/html/openWB/ramdisk/llas13
touch /var/www/html/openWB/ramdisk/llkwh
touch /var/www/html/openWB/ramdisk/pvkwh
touch /var/www/html/openWB/ramdisk/llkwhs1
touch /var/www/html/openWB/ramdisk/einspeisungkwh
touch /var/www/html/openWB/ramdisk/bezugkwh
echo 0 > /var/www/html/openWB/ramdisk/llas11
echo 0 > /var/www/html/openWB/ramdisk/llas12
echo 0 > /var/www/html/openWB/ramdisk/llas13
echo 0 > /var/www/html/openWB/ramdisk/wattbezug
echo 0 > /var/www/html/openWB/ramdisk/ladestatus
echo 0 > /var/www/html/openWB/ramdisk/lademodus
echo 0 > /var/www/html/openWB/ramdisk/llaktuell
echo 0 > /var/www/html/openWB/ramdisk/pvwatt
echo 0 > /var/www/html/openWB/ramdisk/soc
echo 0 > /var/www/html/openWB/ramdisk/lla1
echo 0 > /var/www/html/openWB/ramdisk/lla2
echo 0 > /var/www/html/openWB/ramdisk/lla3	
echo 0 > /var/www/html/openWB/ramdisk/llaktuells1
echo 0 > /var/www/html/openWB/ramdisk/llkombiniert
echo 0 > /var/www/html/openWB/ramdisk/llkwh
echo 0 > /var/www/html/openWB/ramdisk/pvkwh
echo 0 > /var/www/html/openWB/ramdisk/bezugkwh
echo 0 > /var/www/html/openWB/ramdisk/einspeisungkwh
echo 0 > /var/www/html/openWB/ramdisk/llkwhs1
sudo chown -R www-data:www-data /var/www/html/openWB/web/backup
sudo chown -R www-data:www-data /var/www/html/openWB/web/tools/upload
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod -R +x /var/www/html/openWB/modules/*
ln -s /var/log/openWB.log /var/www/html/openWB/ramdisk/openWB.log
