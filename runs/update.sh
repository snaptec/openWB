#!/bin/bash
cd /var/www/html/openWB
. /var/www/html/openWB/loadconfig.sh

# set mode to stop and flags in ramdisk and broker to indicate current update state
mosquitto_pub -t openWB/set/ChargeMode -r -m "3"
mosquitto_pub -t openWB/system/updateInProgress -r -m "1"
echo 1 > /var/www/html/openWB/ramdisk/updateinprogress
echo 1 > /var/www/html/openWB/ramdisk/bootinprogress
echo "Update im Gange, bitte warten bis die Meldung nicht mehr sichtbar ist" > /var/www/html/openWB/ramdisk/lastregelungaktiv
mosquitto_pub -t "openWB/global/strLastmanagementActive" -r -m "Update im Gange, bitte warten bis die Meldung nicht mehr sichtbar ist"
echo "Update im Gange, bitte warten bis die Meldung nicht mehr sichtbar ist" > /var/www/html/openWB/ramdisk/mqttlastregelungaktiv
chmod 777 var/www/html/openWB/ramdisk/mqttlastregelungaktiv

if [[ "$releasetrain" == "stable" ]]; then
	train=stable17
else
	train=$releasetrain
fi

# check for ext openWB on configured chargepoints and start update
if [[ "$evsecon" == "extopenwb" ]]; then
	echo "starting update on extOpenWB on LP1"
	mosquitto_pub -t openWB/set/system/releaseTrain -r -h $chargep1ip -m "$releasetrain"
	mosquitto_pub -t openWB/set/system/PerformUpdate -r -h $chargep1ip -m "1"
fi
if [[ $lastmanagement == "1" ]]; then
	if [[ "$evsecons1" == "extopenwb" ]]; then
		echo "starting update on extOpenWB on LP2"
		mosquitto_pub -t openWB/set/system/releaseTrain -r -h $chargep2ip -m "$releasetrain"
		mosquitto_pub -t openWB/set/system/PerformUpdate -r -h $chargep2ip -m "1"
	fi
fi
if [[ $lastmanagements2 == "1" ]]; then
	if [[ "$evsecons2" == "extopenwb" ]]; then
		echo "starting update on extOpenWB on LP3"
		mosquitto_pub -t openWB/set/system/releaseTrain -r -h $chargep3ip -m "$releasetrain"
		mosquitto_pub -t openWB/set/system/PerformUpdate -r -h $chargep3ip -m "1"
	fi
fi
for i in $(seq 4 8); do
	lastmanagementVar="lastmanagementlp$i"
	evseconVar="evseconlp$i"
	if [[ ${!lastmanagementVar} == "1" ]]; then
		if [[ ${!evseconVar} == "extopenwb" ]]; then
			echo "starting update on extOpenWB on LP$i"
			chargepIpVar="chargep${i}ip"
			mosquitto_pub -t openWB/set/system/releaseTrain -r -h ${!chargepIpVar} -m "$releasetrain"
			mosquitto_pub -t openWB/set/system/PerformUpdate -r -h ${!chargepIpVar} -m "1"
		fi
	fi
done

sleep 15

# backup some files before fetching new release
# module soc_eq
cp modules/soc_eq/soc_eq_acc_lp1 /tmp/soc_eq_acc_lp1
cp modules/soc_eq/soc_eq_acc_lp2 /tmp/soc_eq_acc_lp2
cp openwb.conf /tmp/openwb.conf

# fetch new release from GitHub
sudo git fetch origin
sudo git reset --hard origin/$train

# set permissions
cd /var/www/html/
sudo chown -R pi:pi openWB 
sudo chown -R www-data:www-data /var/www/html/openWB/web/backup
sudo chown -R www-data:www-data /var/www/html/openWB/web/tools/upload
sudo cp /tmp/openwb.conf /var/www/html/openWB/openwb.conf

# restore saved files after fetching new release
# module soc_eq
sudo cp /tmp/soc_eq_acc_lp1 /var/www/html/openWB/modules/soc_eq/soc_eq_acc_lp1
sudo cp /tmp/soc_eq_acc_lp2 /var/www/html/openWB/modules/soc_eq/soc_eq_acc_lp2

# set permissions
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod +x /var/www/html/openWB/modules/*
sudo chmod +x /var/www/html/openWB/runs/*
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod 777 /var/www/html/openWB/web/lade.log
sleep 2

# now treat system as in booting state
nohup sudo /var/www/html/openWB/runs/atreboot.sh > /var/log/openWB.log 2>&1 &
