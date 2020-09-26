#!/bin/bash
. /var/www/html/openWB/loadconfig.sh
echo "Start cron nightly @ $(date)"
#logfile aufräumen
echo "$(tail -1000 /var/log/openWB.log)" > /var/log/openWB.log
echo 1 > /var/www/html/openWB/ramdisk/reloaddisplay
echo "reset" > /var/www/html/openWB/ramdisk/mqtt.log





monthlyfile="/var/www/html/openWB/web/logging/data/monthly/$(date +%Y%m)"

bezug=$(</var/www/html/openWB/ramdisk/bezugkwh)
einspeisung=$(</var/www/html/openWB/ramdisk/einspeisungkwh)
if [[ $pv2wattmodul != "none" ]]; then
	pv=$(</var/www/html/openWB/ramdisk/pvallwh)
else
	pv=$(</var/www/html/openWB/ramdisk/pvkwh)
fi
ll1=$(</var/www/html/openWB/ramdisk/llkwh)
ll2=$(</var/www/html/openWB/ramdisk/llkwhs1)
ll3=$(</var/www/html/openWB/ramdisk/llkwhs2)
llg=$(</var/www/html/openWB/ramdisk/llkwhges)
speicherikwh=$(</var/www/html/openWB/ramdisk/speicherikwh)
speicherekwh=$(</var/www/html/openWB/ramdisk/speicherekwh)
verbraucher1iwh=$(</var/www/html/openWB/ramdisk/verbraucher1_wh)
verbraucher1ewh=$(</var/www/html/openWB/ramdisk/verbraucher1_whe)
verbraucher2iwh=$(</var/www/html/openWB/ramdisk/verbraucher2_wh)
verbraucher2ewh=$(</var/www/html/openWB/ramdisk/verbraucher2_whe)
ll4=$(</var/www/html/openWB/ramdisk/llkwhlp4)
ll5=$(</var/www/html/openWB/ramdisk/llkwhlp5)
ll6=$(</var/www/html/openWB/ramdisk/llkwhlp6)
ll7=$(</var/www/html/openWB/ramdisk/llkwhlp7)
ll8=$(</var/www/html/openWB/ramdisk/llkwhlp8)
d1=$(</var/www/html/openWB/ramdisk/device1_wh)
d2=$(</var/www/html/openWB/ramdisk/device2_wh)
d3=$(</var/www/html/openWB/ramdisk/device3_wh)
d4=$(</var/www/html/openWB/ramdisk/device4_wh)
d5=$(</var/www/html/openWB/ramdisk/device5_wh)
d6=$(</var/www/html/openWB/ramdisk/device6_wh)
d7=$(</var/www/html/openWB/ramdisk/device7_wh)
d8=$(</var/www/html/openWB/ramdisk/device8_wh)
d9=$(</var/www/html/openWB/ramdisk/device9_wh)
d10=$(</var/www/html/openWB/ramdisk/device10_wh)

ll1=$(echo "$ll1 * 1000" | bc)
ll2=$(echo "$ll2 * 1000" | bc)
ll3=$(echo "$ll3 * 1000" | bc)
llg=$(echo "$llg * 1000" | bc)
ll4=$(echo "$ll4 * 1000" | bc)
ll5=$(echo "$ll5 * 1000" | bc)
ll6=$(echo "$ll6 * 1000" | bc)
ll7=$(echo "$ll7 * 1000" | bc)
ll8=$(echo "$ll8 * 1000" | bc)

echo $(date +%Y%m%d),$bezug,$einspeisung,$pv,$ll1,$ll2,$ll3,$llg,$verbraucher1iwh,$verbraucher1ewh,$verbraucher2iwh,$verbraucher2ewh,$ll4,$ll5,$ll6,$ll7,$ll8,$speicherikwh,$speicherekwh,$d1,$d2,$d3,$d4,$d5,$d6,$d7,$d8,$d9,$d10 >> $monthlyfile.csv


if [[ $verbraucher1_typ == "tasmota" ]]; then
	verbraucher1_oldwh=$(curl -s http://$verbraucher1_ip/cm?cmnd=Status%208 | jq '.StatusSNS.ENERGY.Total')
	if [[ $? == "0" ]]; then
		if [ -z "$verbraucher1_tempwh" ]; then
			verbraucher1_writewh=$(echo "scale=0;($verbraucher1_oldwh * 1000) / 1" | bc)
		else
			verbraucher1_writewh=$(echo "scale=0;(($verbraucher1_oldwh * 1000) + $verbraucher1_tempwh) / 1" | bc)
		fi
		sed -i "s/verbraucher1_tempwh=.*/verbraucher1_tempwh=$verbraucher1_writewh/" /var/www/html/openWB/openwb.conf
		curl -s http://$verbraucher1_ip/cm?cmnd=EnergyReset1%200
		curl -s http://$verbraucher1_ip/cm?cmnd=EnergyReset2%200
		curl -s http://$verbraucher1_ip/cm?cmnd=EnergyReset3%200
	fi
fi
if [[ $verbraucher2_typ == "tasmota" ]]; then
	verbraucher2_oldwh=$(curl -s http://$verbraucher2_ip/cm?cmnd=Status%208 | jq '.StatusSNS.ENERGY.Total')
	if [[ $? == "0" ]]; then
		if [ -z "$verbraucher2_tempwh" ]; then
			verbraucher2_writewh=$(echo "scale=0;($verbraucher2_oldwh * 1000) / 1" | bc)
		else
			verbraucher2_writewh=$(echo "scale=0;(($verbraucher2_oldwh * 1000) + $verbraucher2_tempwh) / 1" | bc)
		fi
		sed -i "s/verbraucher2_tempwh=.*/verbraucher2_tempwh=$verbraucher2_writewh/" /var/www/html/openWB/openwb.conf
		curl -s http://$verbraucher2_ip/cm?cmnd=EnergyReset1%200
		curl -s http://$verbraucher2_ip/cm?cmnd=EnergyReset2%200
		curl -s http://$verbraucher2_ip/cm?cmnd=EnergyReset3%200
	fi
fi

curl -s https://raw.githubusercontent.com/snaptec/openWB/master/web/version > /var/www/html/openWB/ramdisk/vnightly
curl -s https://raw.githubusercontent.com/snaptec/openWB/beta/web/version > /var/www/html/openWB/ramdisk/vbeta
curl -s https://raw.githubusercontent.com/snaptec/openWB/stable/web/version > /var/www/html/openWB/ramdisk/vstable

