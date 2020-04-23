#!/bin/bash
sed -i 's/debug.*/debug=1/' /var/www/html/openWB/openwb.conf
sleep 60

debugFile=/var/www/html/openWB/ramdisk/debug.log
cat /var/www/html/openWB/ramdisk/debuguser > $debugFile
echo "############################ network ##############" >> $debugFile
ifconfig >> $debugFile

echo "############################ version ##############" >> $debugFile
echo "Version" >> $debugFile
cat /var/www/html/openWB/web/version >> $debugFile
echo "$(tail -1000 /var/www/html/openWB/ramdisk/openWB.log)" >> $debugFile

echo "############################ mqtt ##############" >> $debugFile
echo "$(tail -200 /var/www/html/openWB/ramdisk/mqtt.log)" >> $debugFile
echo "############################ ladestatus.log ##############" >> $debugFile
echo "$(tail -800 /var/www/html/openWB/ramdisk/ladestatus.log)" >> $debugFile

for currentConfig in /etc/mosquitto/conf.d/99-bridge-*; do
    if [ -f "$currentConfig" ]; then
        echo "############################ mqtt bridge '$currentConfig' ######" >> $debugFile
        sudo grep -F -v -e password "$currentConfig" | sed '/^#/ d'>> $debugFile
    fi
done

echo "############################ config ##############" >> $debugFile
grep -F -v -e leaf -e i3 -e zoe -e tesla -e carnet -e bezug_smartme -e bydhv -e cloud -e discovergy -e evnotify -e lgessv1 -e myrenault -e nrgkick -e pushover -e pv2 -e settingspw -e soc_audi -e soc_bluelink -e soc_zerong -e wr_piko2 -e wr_smartme -e wrsunwayspw /var/www/html/openWB/openwb.conf >> $debugFile


curl --upload $debugFile https://openwb.de/tools/debug.php

sed -i 's/debug.*/debug=0/' /var/www/html/openWB/openwb.conf
rm /var/www/html/openWB/ramdisk/debuguser
