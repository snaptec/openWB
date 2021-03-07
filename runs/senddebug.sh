#!/bin/bash
sed -i 's/debug.*/debug=1/' /var/www/html/openWB/openwb.conf
sleep 60

debugFile=/var/www/html/openWB/ramdisk/debug.log
cat /var/www/html/openWB/ramdisk/debuguser > $debugFile
echo "############################ network ##############" >> $debugFile
ifconfig >> $debugFile
uptime >> $debugFile
echo "############################ version ##############" >> $debugFile
echo "Version" >> $debugFile
cat /var/www/html/openWB/web/version >> $debugFile
echo "############################ openWB.log ##############" >> $debugFile
echo "$(tail -1000 /var/www/html/openWB/ramdisk/openWB.log)" >> $debugFile
echo "############################ mqtt ##############" >> $debugFile
echo "$(tail -200 /var/www/html/openWB/ramdisk/mqtt.log)" >> $debugFile
echo "############################ ladestatus.log ##############" >> $debugFile
echo "$(tail -800 /var/www/html/openWB/ramdisk/ladestatus.log)" >> $debugFile
echo "############################ soc.log ##############" >> $debugFile
echo "$(cat /var/www/html/openWB/ramdisk/soc.log)" >> $debugFile
echo "############################ rfid.log ##############" >> $debugFile
echo "$(cat /var/www/html/openWB/ramdisk/rfid.log)" >> $debugFile

for currentConfig in /etc/mosquitto/conf.d/99-bridge-*; do
    if [ -f "$currentConfig" ]; then
        echo "############################ mqtt bridge '$currentConfig' ######" >> $debugFile
        sudo grep -F -v -e password "$currentConfig" | sed '/^#/ d'>> $debugFile
    fi
done

echo "############################ config ##############" >> $debugFile
grep -F -v -e soc_id_passwort -e leaf -e myopel_clientidlp2 -e soc_eq_client_secret_lp1 -e psa_clientsecretlp1 -e psa_clientsecretlp2 -e tibbertoken -e soc_eq_client_secret_lp2 -e myopel_clientsecretlp2 -e myopel_clientidlp1 -e myopel_clientsecretlp1 -e i3 -e zoeuser -e zoepass -e zoelp2 -e tesla -e socpass -e soc2pass -e passlp1 -e passlp2 -e carnet -e settingspw -e wrsunwayspw -e cloudpw -e wr_piko2_pass -e zerong -e discovergy -e audi -e smartme -e bydhvpass -e lgessv1pass -e myrenault -e bluelink  /var/www/html/openWB/openwb.conf >> $debugFile


curl --upload $debugFile https://openwb.de/tools/debug.php

sed -i 's/debug.*/debug=0/' /var/www/html/openWB/openwb.conf
rm /var/www/html/openWB/ramdisk/debuguser
