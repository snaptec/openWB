#!/bin/bash
echo "***** debuglog level 1 start..." >> /var/www/html/openWB/ramdisk/openWB.log
sed -i 's/^debug=.*/debug=1/' /var/www/html/openWB/openwb.conf
sleep 60
echo "***** debuglog level 2 start..." >> /var/www/html/openWB/ramdisk/openWB.log
sed -i 's/^debug=.*/debug=2/' /var/www/html/openWB/openwb.conf
sleep 60

debugFile=/var/www/html/openWB/ramdisk/debug.log
cat /var/www/html/openWB/ramdisk/debuguser > $debugFile
debugemail=$(</var/www/html/openWB/ramdisk/debugemail)
echo "############################ system ###############" >> $debugFile
uptime >> $debugFile
free >> $debugFile
echo "############################ storage ###############" >> $debugFile
df -h >> $debugFile
echo "############################ network ##############" >> $debugFile
ifconfig >> $debugFile
echo "############################ version ##############" >> $debugFile
cat /var/www/html/openWB/web/version >> $debugFile
cat /var/www/html/openWB/web/lastcommit >> $debugFile
echo "############################ openWB.log ##############" >> $debugFile
echo "$(tail -500 /var/www/html/openWB/ramdisk/openWB.log)" >> $debugFile
echo "############################ isss ##############" >> $debugFile
echo "$(tail -300 /var/www/html/openWB/ramdisk/isss.log)" >> $debugFile
echo "############################ mqtt ##############" >> $debugFile
echo "$(tail -200 /var/www/html/openWB/ramdisk/mqtt.log)" >> $debugFile
echo "############################ ladestatus.log ##############" >> $debugFile
echo "$(tail -300 /var/www/html/openWB/ramdisk/ladestatus.log)" >> $debugFile
echo "############################ soc.log ##############" >> $debugFile
echo "$(tail -100 /var/www/html/openWB/ramdisk/soc.log)" >> $debugFile
echo "############################ nurpv.log ##############" >> $debugFile
echo "$(tail -200 /var/www/html/openWB/ramdisk/nurpv.log)" >> $debugFile
echo "############################ rfid.log ##############" >> $debugFile
echo "$(cat /var/www/html/openWB/ramdisk/rfid.log)" >> $debugFile

for currentConfig in /etc/mosquitto/conf.d/99-bridge-*; do
	if [ -f "$currentConfig" ]; then
		echo "############################ mqtt bridge '$currentConfig' ######" >> $debugFile
		sudo grep -F -v -e password "$currentConfig" | sed '/^#/ d'>> $debugFile
	fi
done

echo "############################ config ##############" >> $debugFile
grep -F -v -e soc_id_passwort -e leaf -e myopel_clientidlp2 -e soc_eq_client_secret_lp1 -e psa_clientsecretlp1 -e psa_clientsecretlp2 -e tibbertoken -e soc_eq_client_secret_lp2 -e myopel_clientsecretlp2 -e myopel_clientidlp1 -e myopel_clientsecretlp1 -e i3user -e i3pass -e zoeuser -e zoepass -e zoelp2 -e tesla -e socpass -e soc2pass -e passlp1 -e passlp2 -e carnet -e settingspw -e wrsunwayspw -e cloudpw -e wr_piko2_pass -e zerong -e discovergyuser -e discovergypass -e audi -e smartme -e bydhvpass -e lgessv1pass -e myrenault -e bluelink -e soc_vag_passwort -e soc_id_vin -e soc_tronity_client_id_lp1 -e soc_tronity_client_id_lp2 -e soc_tronity_client_secret_lp1 -e soc_tronity_client_secret_lp2 -e soc_tronity_vehicle_id_lp1 -e soc_tronity_vehicle_id_lp2 /var/www/html/openWB/openwb.conf >> $debugFile

echo "############################ mqtt topics ##############" >> $debugFile
timeout 1 mosquitto_sub -v -t 'openWB/#' >> $debugFile

echo "############################ smarthome.log ##############" >> $debugFile
echo "$(tail -200 /var/www/html/openWB/ramdisk/smarthome.log)" >> $debugFile

# echo "############################ file and directory listing ##############" >> $debugFile
# ls -lRa /var/www/html/openWB/modules/soc_* >> $debugFile

echo "***** uploading debuglog..." >> /var/www/html/openWB/ramdisk/openWB.log
curl --upload $debugFile "https://openwb.de/tools/debug2.php?debugemail=$debugemail"

echo "***** cleanup..." >> /var/www/html/openWB/ramdisk/openWB.log
sed -i 's/^debug=.*/debug=0/' /var/www/html/openWB/openwb.conf
rm $debugFile
rm /var/www/html/openWB/ramdisk/debuguser
rm /var/www/html/openWB/ramdisk/debugemail

echo "***** debuglog end" >> /var/www/html/openWB/ramdisk/openWB.log
