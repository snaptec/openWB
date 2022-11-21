#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
DEBUGFILE="$RAMDISKDIR/debug.log"
DEBUGEMAIL=$(<"$RAMDISKDIR/debugemail")

# change debug level
echo "***** debuglog level 1 start..." >> "$RAMDISKDIR/openWB.log"
sed -i 's/^debug=.*/debug=1/' "$OPENWBBASEDIR/openwb.conf"
sleep 60
echo "***** debuglog level 2 start..." >> "$RAMDISKDIR/openWB.log"
sed -i 's/^debug=.*/debug=2/' "$OPENWBBASEDIR/openwb.conf"
sleep 60

touch "$DEBUGFILE"
{
	cat "$RAMDISKDIR/debuguser"
	echo "############################ system ###############"
	uptime
	free
	echo "############################ storage ###############"
	df -h
	echo "############################ network ##############"
	ifconfig
	echo "############################ version ##############"
	cat "$OPENWBBASEDIR/web/version"
	cat "$OPENWBBASEDIR/web/lastcommit"
	echo "############################ openWB.log ##############"
	tail -2500 "$RAMDISKDIR/openWB.log"
	echo "############################ isss ##############"
	tail -2500 "$RAMDISKDIR/isss.log"
	echo "############################ mqtt ##############"
	tail -200 "$RAMDISKDIR/mqtt.log"
	echo "############################ ladestatus.log ##############"
	tail -300 "$RAMDISKDIR/ladestatus.log"
	echo "############################ soc.log ##############"
	tail -100 "$RAMDISKDIR/soc.log"
	echo "############################ nurpv.log ##############"
	tail -200 "$RAMDISKDIR/nurpv.log"
	echo "############################ rfid.log ##############"
	cat "$RAMDISKDIR/rfid.log"

	for currentConfig in /etc/mosquitto/conf.d/99-bridge-*; do
		if [ -f "$currentConfig" ]; then
			echo "############################ mqtt bridge '$currentConfig' ######"
			sudo grep -F -v -e password "$currentConfig" | sed '/^#/ d'
		fi
	done

	echo "############################ config ##############"
	grep -F -v -e soc_id_passwort -e leaf -e myopel_clientidlp2 -e soc_eq_client_secret_lp1 -e psa_clientsecretlp1 -e psa_clientsecretlp2 -e tibbertoken -e soc_eq_client_secret_lp2 -e myopel_clientsecretlp2 -e myopel_clientidlp1 -e myopel_clientsecretlp1 -e i3user -e i3pass -e zoeuser -e zoepass -e zoelp2 -e tesla -e socpass -e soc2pass -e passlp1 -e passlp2 -e carnet -e settingspw -e wrsunwayspw -e cloudpw -e wr_piko2_pass -e zerong -e discovergyuser -e discovergypass -e audi -e smartme -e bydhvpass -e lgessv1pass -e myrenault -e bluelink -e soc_vag_password -e soc_id_vin -e soc_tronity_client_id_lp1 -e soc_tronity_client_id_lp2 -e soc_tronity_client_secret_lp1 -e soc_tronity_client_secret_lp2 -e soc_tronity_vehicle_id_lp1 -e soc_tronity_vehicle_id_lp2 "$OPENWBBASEDIR/openwb.conf"

	echo "############################ mqtt topics ##############"
	timeout 1 mosquitto_sub -v -t 'openWB/#'

	echo "############################ smarthome.log ##############"
	tail -200 "$RAMDISKDIR/smarthome.log"
} >> "$DEBUGFILE"

echo "***** uploading debuglog..." >> "$RAMDISKDIR/openWB.log"
curl --upload "$DEBUGFILE" "https://openwb.de/tools/debug2.php?debugemail=$DEBUGEMAIL"

echo "***** cleanup..." >> "$RAMDISKDIR/openWB.log"
sed -i 's/^debug=.*/debug=0/' "$OPENWBBASEDIR/openwb.conf"
rm "$DEBUGFILE"
rm "$RAMDISKDIR/debuguser"
rm "$RAMDISKDIR/debugemail"

echo "***** debuglog end" >> "$RAMDISKDIR/openWB.log"
