#!/bin/bash
cd /var/www/html/openWB
. /var/www/html/openWB/loadconfig.sh
mosquitto_pub -t openWB/set/ChargeMode -r -m "3"
mosquitto_pub -t openWB/system/updateInProgress -r -m "1"
if [[ "$releasetrain" == "stable" ]]
then
	train=stable17
elif [[ "$releasetrain" == "stableold" ]]
then
	train=stable
else
	train=$releasetrain
fi
if [[ "$evsecon" == "extopenwb" ]]
then
	mosquitto_pub -t openWB/set/system/releaseTrain -r -h $chargep1ip -m "$releasetrain"
    mosquitto_pub -t openWB/set/system/PerformUpdate -r -h $chargep1ip -m "1"
fi
if [[ $lastmanagement == "1" ]]; then
	if [[ "$evseconlp2" == "extopenwb" ]]
	then
		mosquitto_pub -t openWB/set/system/releaseTrain -r -h $chargiplp2 -m "$releasetrain"
		mosquitto_pub -t openWB/set/system/PerformUpdate -r -h $chargiplp2 -m "1"
	fi
fi
if [[ $lastmanagementlp3 == "1" ]]; then
	if [[ "$evseconlp3" == "extopenwb" ]]
	then
		mosquitto_pub -t openWB/set/system/releaseTrain -r -h $chargeiplp3 -m "$releasetrain"
		mosquitto_pub -t openWB/set/system/PerformUpdate -r -h $chargeiplp3 -m "1"
	fi
fi
sleep 15

echo 1 > /var/www/html/openWB/ramdisk/updateinprogress
echo 1 > /var/www/html/openWB/ramdisk/bootinprogress
echo "Update im Gange, bitte warten bis die Meldung nicht mehr sichtbar ist" > /var/www/html/openWB/ramdisk/lastregelungaktiv
mosquitto_pub -t "openWB/global/strLastmanagementActive" -r -m "Update im Gange, bitte warten bis die Meldung nicht mehr sichtbar ist"
echo "Update im Gange, bitte warten bis die Meldung nicht mehr sichtbar ist" > /var/www/html/openWB/ramdisk/mqttlastregelungaktiv
chmod 777 var/www/html/openWB/ramdisk/mqttlastregelungaktiv
cp modules/soc_i3/auth.json /tmp/auth.json
cp modules/soc_i3s1/auth.json /tmp/auth.json.1
cp openwb.conf /tmp/openwb.conf
#mkdir /tmp/data
#mkdir /tmp/data/daily
#for i in /var/www/html/openWB/web/logging/data/daily/*; do cp "$i" /tmp/data/daily/; done
#mkdir /tmp/data/monthly
#for i in /var/www/html/openWB/web/logging/data/monthly/*; do cp "$i" /tmp/data/monthly/; done
sudo git fetch origin
sudo git reset --hard origin/$train
cd /var/www/html/
sudo chown -R pi:pi openWB
sudo chown -R www-data:www-data /var/www/html/openWB/web/backup
sudo chown -R www-data:www-data /var/www/html/openWB/web/tools/upload
sudo cp /tmp/openwb.conf /var/www/html/openWB/openwb.conf
sudo cp /tmp/auth.json /var/www/html/openWB/modules/soc_i3/auth.json
sudo cp /tmp/auth.json.1 /var/www/html/openWB/modules/soc_i3s1/auth.json
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod +x /var/www/html/openWB/modules/*
sudo chmod +x /var/www/html/openWB/runs/*
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod 777 /var/www/html/openWB/web/lade.log
#for i in /tmp/data/monthly/*; do cp "$i" /var/www/html/openWB/web/logging/data/monthly/; done
#for i in /tmp/data/daily/*; do cp "$i" /var/www/html/openWB/web/logging/data/monthly/; done
sleep 2
if ! grep -Fq "wr_http_w_url=" /var/www/html/openWB/openwb.conf
then
	  echo "wr_http_w_url=http://192.168.0.17/pvwatt.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hsociplp2=" /var/www/html/openWB/openwb.conf
then
	  echo "hsociplp2=http://10.0.0.110/soc.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "socmodullp2=" /var/www/html/openWB/openwb.conf
then
	  echo "socmodullp2=soc_http1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "dacregisterlp2=" /var/www/html/openWB/openwb.conf
then
	  echo "dacregisterlp2=12" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "wr_http_kwh_url=" /var/www/html/openWB/openwb.conf
then
	  echo "wr_http_kwh_url=http://192.168.0.17/pvwh.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "smaemdbezugid=" /var/www/html/openWB/openwb.conf
then
	  echo "smaemdbezugid=1900123456" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "smaemdpvid=" /var/www/html/openWB/openwb.conf
then
	  echo "smaemdpvid=1900123456" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "smaemdllid=" /var/www/html/openWB/openwb.conf
then
	  echo "smaemdllid=1900123456" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "bezug_http_w_url=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_http_w_url=http://192.168.0.17/bezugwatt.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_http_ikwh_url=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_http_ikwh_url=http://192.168.0.17/bezugwh.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_http_ekwh_url=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_http_ekwh_url=http://192.168.0.17/einspeisungwh.txt" >> /var/www/html/openWB/openwb.conf
fi


sudo /var/www/html/openWB/runs/atreboot.sh

