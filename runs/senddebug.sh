#!/bin/bash
sed -i 's/debug.*/debug=1/' /var/www/html/openWB/openwb.conf
sleep 60
echo "$(tail -1000 /var/www/html/openWB/ramdisk/openWB.log)" > /var/www/html/openWB/ramdisk/debug.log
echo "############################ mqtt ##############" >> /var/www/html/openWB/ramdisk/debug.log
echo "$(tail -200 /var/www/html/openWB/ramdisk/mqtt.log)" >> /var/www/html/openWB/ramdisk/debug.log
echo "############################ config ##############" >> /var/www/html/openWB/ramdisk/debug.log

grep -F -v -e leaf -e i3 -e zoe -e tesla -e carnet /var/www/html/openWB/openwb.conf >> /var/www/html/openWB/ramdisk/debug.log
cat /var/www/html/openWB/ramdisk/debuguser >> /var/www/html/openWB/ramdisk/debug.log
echo "############################ version ##############" >> /var/www/html/openWB/ramdisk/debug.log

echo "Version" >> /var/www/html/openWB/ramdisk/debug.log
cat /var/www/html/openWB/web/version >> /var/www/html/openWB/ramdisk/debug.log
curl --upload /var/www/html/openWB/ramdisk/debug.log https://openwb.de/tools/debug.php

sed -i 's/debug.*/debug=0/' /var/www/html/openWB/openwb.conf
rm /var/www/html/openWB/ramdisk/debuguser

