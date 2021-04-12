#!/bin/bash
echo "atreboot.sh started"
(sleep 600; sudo kill $(ps aux |grep '[a]treboot.sh' | awk '{print $2}'); echo 0 > /var/www/html/openWB/ramdisk/bootinprogress; echo 0 > /var/www/html/openWB/ramdisk/updateinprogress) &

# read openwb.conf
echo "loading config"
. /var/www/html/openWB/loadconfig.sh

# load functions to init ramdisk and update config
# no code will run here, functions need to be called
. /var/www/html/openWB/runs/initRamdisk.sh
. /var/www/html/openWB/runs/updateConfig.sh

sleep 5
mkdir -p /var/www/html/openWB/web/backup
touch /var/www/html/openWB/web/backup/.donotdelete
sudo chown -R www-data:www-data /var/www/html/openWB/web/backup
sudo chown -R www-data:www-data /var/www/html/openWB/web/tools/upload
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod 777 /var/www/html/openWB/smarthome.ini
sudo chmod 777 /var/www/html/openWB/ramdisk
sudo chmod 777 /var/www/html/openWB/ramdisk/
sudo chmod 777 /var/www/html/openWB/web/files/*
sudo chmod -R +x /var/www/html/openWB/modules/*

sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3
sudo chmod -R 777 /var/www/html/openWB/modules/soc_eq
sudo chmod -R 777 /var/www/html/openWB/modules/soc_tesla

sudo chmod 777 /var/www/html/openWB/web/files/*
sudo chmod -R +x /var/www/html/openWB/modules/*

mkdir -p /var/www/html/openWB/web/logging/data/daily
mkdir -p /var/www/html/openWB/web/logging/data/monthly
mkdir -p /var/www/html/openWB/web/logging/data/ladelog
mkdir -p /var/www/html/openWB/web/logging/data/v001
sudo chmod -R 777 /var/www/html/openWB/web/logging/data/

# update openwb.conf
updateConfig
# reload our changed openwb.conf
. /var/www/html/openWB/loadconfig.sh
# now setup all files in ramdisk
initRamdisk

# standard socket - activated after reboot due to RASPI init defaults so we need to disable it as soon as we can
if [[ $standardSocketInstalled == "1" ]]; then
	echo "turning off standard socket ..."
	sudo python /var/www/html/openWB/runs/standardSocket.py off
fi

# initialize automatic phase switching
if (( u1p3paktiv == 1 )); then
	echo "triginit..."
	sudo python /var/www/html/openWB/runs/triginit.py -d $u1p3ppause
fi

# check if buttons are configured and start daemon
if (( ladetaster == 1 )); then
	echo "pushbuttons..."
	if ! [ -x "$(command -v nmcli)" ]; then
		if ps ax |grep -v grep |grep "python /var/www/html/openWB/runs/ladetaster.py" > /dev/null
		then
			echo "test" > /dev/null
		else
			sudo python /var/www/html/openWB/runs/ladetaster.py &
		fi
	fi
fi

# check for rse and start daemon
if (( rseenabled == 1 )); then
	echo "rse..."
	if ! [ -x "$(command -v nmcli)" ]; then
		if ps ax |grep -v grep |grep "python /var/www/html/openWB/runs/rse.py" > /dev/null
		then
			echo "test" > /dev/null
		else
			sudo python /var/www/html/openWB/runs/rse.py &
		fi
	fi
fi

# check if rfid is configured and start daemons to listen on input devices
if (( rfidakt == 1 )); then
	echo "rfid 1..."
	sudo kill $(ps aux |grep '[r]eadrfid.py' | awk '{print $2}')
	(sleep 10; sudo python /var/www/html/openWB/runs/readrfid.py $displayaktiv) &
	(sleep 10; sudo python /var/www/html/openWB/runs/readrfid2.py $displayaktiv) &
fi
if (( rfidakt == 2 )); then
	echo "rfid 2..."
	sudo kill $(ps aux |grep '[r]eadrfid.py' | awk '{print $2}')
	(sleep 10; sudo python /var/www/html/openWB/runs/readrfid.py $displayaktiv) &
	(sleep 10; sudo python /var/www/html/openWB/runs/readrfid2.py $displayaktiv) &
fi

# check if tesla wall connector is configured and start daemon
if [[ $evsecon == twcmanager ]]; then
	echo "twcmanager..."
	if [[ $twcmanagerlp1ip == "localhost/TWC" ]]; then
		screen -dm -S TWCManager /var/www/html/TWC/TWCManager.py &
	fi
fi

# check if display is configured and setup timeout
if (( displayaktiv == 1 )); then
	echo "display..."
	if ! grep -Fq "pinch" /home/pi/.config/lxsession/LXDE-pi/autostart
	then
		echo "not found"
		echo "@xscreensaver -no-splash" > /home/pi/.config/lxsession/LXDE-pi/autostart
		echo "@point-rpi" >> /home/pi/.config/lxsession/LXDE-pi/autostart
		echo "@xset s 600" >> /home/pi/.config/lxsession/LXDE-pi/autostart
		echo "@chromium-browser --incognito --disable-pinch --kiosk http://localhost/openWB/web/display.php" >> /home/pi/.config/lxsession/LXDE-pi/autostart
	fi
fi

# restart smarthomehandler
echo "smarthome handler..."
if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/smarthomehandler.py" > /dev/null
then
	sudo kill $(ps aux |grep '[s]marthomehandler.py' | awk '{print $2}')
fi
python3 /var/www/html/openWB/runs/smarthomehandler.py >> /var/www/html/openWB/ramdisk/smarthome.log 2>&1 &

# restart mqttsub handler
echo "mqtt handler..."
if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/mqttsub.py" > /dev/null
then
	sudo kill $(ps aux |grep '[m]qttsub.py' | awk '{print $2}')
fi
python3 /var/www/html/openWB/runs/mqttsub.py &

# check crontab for user pi
echo "crontab 1..."
crontab -l -u pi > /var/www/html/openWB/ramdisk/tmpcrontab
if grep -Fq "lade.log" /var/www/html/openWB/ramdisk/tmpcrontab
then
	echo "crontab modified"
	sed -i '/lade.log/d' /var/www/html/openWB/ramdisk/tmpcrontab
	echo "* * * * * /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1" >> /var/www/html/openWB/ramdisk/tmpcrontab
	cat /var/www/html/openWB/ramdisk/tmpcrontab | crontab -u pi -
fi

# check crontab for user root and remove old @reboot entry
sudo crontab -l > /var/www/html/openWB/ramdisk/tmprootcrontab
if grep -Fq "atreboot.sh" /var/www/html/openWB/ramdisk/tmprootcrontab
then
	echo "executed"
	sed -i '/atreboot.sh/d' /var/www/html/openWB/ramdisk/tmprootcrontab
	cat /var/www/html/openWB/ramdisk/tmprootcrontab | sudo crontab -
fi

# check for LAN/WLAN connection
echo "LAN/WLAN..."
ethstate=$(</sys/class/net/eth0/carrier)
if (( ethstate == 1 )); then
	sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 up
else
	sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 up
fi

# check for apache configuration
echo "apache..."
if grep -Fxq "AllowOverride" /etc/apache2/sites-available/000-default.conf
then
	echo "...ok"
else
	sudo cp /var/www/html/openWB/web/tools/000-default.conf /etc/apache2/sites-available/
	echo "...changed"
fi

# add some crontab entries for user pi
echo "crontab 2..."
if ! sudo grep -Fq "cronnightly.sh" /var/spool/cron/crontabs/pi
then
	(crontab -l -u pi ; echo "1 0 * * * /var/www/html/openWB/runs/cronnightly.sh >> /var/log/openWB.log 2>&1")| crontab -u pi -
fi
if ! sudo grep -Fq "cron5min.sh" /var/spool/cron/crontabs/pi
then
	(crontab -l -u pi ; echo "*/5 * * * * /var/www/html/openWB/runs/cron5min.sh >> /var/log/openWB.log 2>&1")| crontab -u pi -
fi
if ! sudo grep -Fq "atreboot.sh" /var/spool/cron/crontabs/pi
then
	(crontab -l -u pi ; echo "@reboot /var/www/html/openWB/runs/atreboot.sh >> /var/log/openWB.log 2>&1")| crontab -u pi -
fi

# check for needed packages
echo "packages 1..."
if python -c "import evdev" &> /dev/null; then
	echo 'evdev installed...'
else
	sudo pip install evdev
fi
if ! [ -x "$(command -v sshpass)" ];then
	apt-get -qq update
	sleep 1
	apt-get -qq install sshpass
fi
if [ $(dpkg-query -W -f='${Status}' php-gd 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	sudo apt-get -qq update
	sleep 1
	sudo apt-get -qq install -y php-gd
	sleep 1
	sudo apt-get -qq install -y php7.0-xml
fi

# no need to reload config
# . /var/www/html/openWB/loadconfig.sh

# update old ladelog
/var/www/html/openWB/runs/transferladelog.sh

# check for led handler
if (( ledsakt == 1 )); then
	echo "led..."
	sudo python /var/www/html/openWB/runs/leds.py startup
fi

# setup timezone
echo "timezone..."
sudo cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# check for mosquitto packages
echo "mosquitto..."
if [ ! -f /etc/mosquitto/mosquitto.conf ]; then
	sudo apt-get update
	sudo apt-get -qq install -y mosquitto mosquitto-clients
	sudo service mosquitto restart
fi

# check for mosquitto configuration
if [ ! -f /etc/mosquitto/conf.d/openwb.conf ]; then
	sudo cp /var/www/html/openWB/web/files/mosquitto.conf /etc/mosquitto/conf.d/openwb.conf
	sudo service mosquitto restart
fi

# check for other dependencies
echo "packages 2..."
if python3 -c "import paho.mqtt.publish as publish" &> /dev/null; then
	echo 'mqtt installed...'
else
	sudo apt-get -qq install -y python3-pip
	sudo pip3 install paho-mqtt
fi
if python3 -c "import docopt" &> /dev/null; then
	echo 'docopt installed...'
else
	sudo pip3 install docopt
fi
if python3 -c "import certifi" &> /dev/null; then
	echo 'certifi installed...'
else
	sudo pip3 install certifi
fi
if python3 -c "import aiohttp" &> /dev/null; then
	echo 'aiohttp installed...'
else
	sudo pip3 install aiohttp
fi
if python3 -c "import pymodbus" &> /dev/null; then
	echo 'pymodbus installed...'
else
	sudo pip3 install pymodbus
fi
#Prepare for jq in Python
if python3 -c "import jq" &> /dev/null; then
	echo 'jq installed...'
else
	sudo pip3 install jq
fi

# update version
echo "version..."
uuid=$(</sys/class/net/eth0/address)
owbv=$(</var/www/html/openWB/web/version)
curl -d "update="$releasetrain$uuid"vers"$owbv"" -H "Content-Type: application/x-www-form-urlencoded" -X POST https://openwb.de/tools/update.php

# all done, remove warning in display
echo "clear warning..."
echo "" > /var/www/html/openWB/ramdisk/lastregelungaktiv
echo "" > /var/www/html/openWB/ramdisk/mqttlastregelungaktiv
chmod 777 /var/www/html/openWB/ramdisk/mqttlastregelungaktiv

#if [ $(dpkg-query -W -f='${Status}' php-curl 2>/dev/null | grep -c "ok installed") -eq 0 ];
#then
#  sudo apt-get update
#  sudo apt-get -qq install -y php-curl
#fi

# check for slave config and start handler
if (( isss == 1 )); then
	echo "isss..."
	echo $lastmanagement > /var/www/html/openWB/ramdisk/issslp2act
	if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/isss.py" > /dev/null
	then
		sudo kill $(ps aux |grep '[i]sss.py' | awk '{print $2}')
	fi
	python3 /var/www/html/openWB/runs/isss.py &
	# second IP already set up !
	ethstate=$(</sys/class/net/eth0/carrier)
	if (( ethstate == 1 )); then
		sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 down
	else
		sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 down
	fi
fi

# check for socket system and start handler
if [[ "$evsecon" == "buchse" ]]  && [[ "$isss" == "0" ]]; then
	echo "socket..."
	# ppbuchse is used in issss.py to detect "openWB Buchse"
	if [ ! -f /home/pi/ppbuchse ]; then
		echo "32" > /home/pi/ppbuchse
	fi
	if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/buchse.py" > /dev/null
	then
		sudo kill $(ps aux |grep '[b]uchse.py' | awk '{print $2}')
	fi
	python3 /var/www/html/openWB/runs/buchse.py &
fi

# check for rfid mode 2 and start handler
if [[ "$rfidakt" == "2" ]]; then
	echo "rfid 2 handler..."
	if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/rfid.py" > /dev/null
	then
		sudo kill $(ps aux |grep '[r]fid.py' | awk '{print $2}')
	fi
	python3 /var/www/html/openWB/runs/rfid.py &
fi

# update display configuration
echo "display update..."
if grep -Fq "@chromium-browser --incognito --disable-pinch --kiosk http://localhost/openWB/web/display.php" /home/pi/.config/lxsession/LXDE-pi/autostart
then
	sed -i "s,@chromium-browser --incognito --disable-pinch --kiosk http://localhost/openWB/web/display.php,@chromium-browser --incognito --disable-pinch --overscroll-history-navigation=0 --kiosk http://localhost/openWB/web/display.php,g" /home/pi/.config/lxsession/LXDE-pi/autostart
fi

# get local ip
ip route get 1 | awk '{print $7;exit}' > /var/www/html/openWB/ramdisk/ipaddress

# update current published versions
echo "load versions..."
curl -s https://raw.githubusercontent.com/snaptec/openWB/master/web/version > /var/www/html/openWB/ramdisk/vnightly
curl -s https://raw.githubusercontent.com/snaptec/openWB/beta/web/version > /var/www/html/openWB/ramdisk/vbeta
curl -s https://raw.githubusercontent.com/snaptec/openWB/stable/web/version > /var/www/html/openWB/ramdisk/vstable

# update our local version
sudo git -C /var/www/html/openWB show --pretty='format:%ci [%h]' | head -n1 > /var/www/html/openWB/web/lastcommit

# update broker
echo "update broker..."
for i in $(seq 1 9);
do
	configured=$(timeout 1 mosquitto_sub -C 1 -t openWB/config/get/SmartHome/Devices/$i/device_configured)
	if ! [[ "$configured" == 0 || "$configured" == 1 ]]; then
		mosquitto_pub -r -t openWB/config/get/SmartHome/Devices/$i/device_configured -m "0"
	fi
done
mosquitto_pub -r -t openWB/graph/boolDisplayLiveGraph -m "1"
mosquitto_pub -t openWB/global/strLastmanagementActive -r -m ""
mosquitto_pub -t openWB/lp/1/W -r -m "0"
mosquitto_pub -t openWB/lp/2/W -r -m "0"
mosquitto_pub -t openWB/lp/3/W -r -m "0"
mosquitto_pub -t openWB/lp/1/boolChargePointConfigured -r -m "1"
mosquitto_pub -r -t openWB/SmartHome/Devices/1/TemperatureSensor0 -m ""
mosquitto_pub -r -t openWB/SmartHome/Devices/1/TemperatureSensor1 -m ""
mosquitto_pub -r -t openWB/SmartHome/Devices/1/TemperatureSensor2 -m ""
mosquitto_pub -r -t openWB/SmartHome/Devices/2/TemperatureSensor0 -m ""
mosquitto_pub -r -t openWB/SmartHome/Devices/2/TemperatureSensor1 -m ""
mosquitto_pub -r -t openWB/SmartHome/Devices/2/TemperatureSensor2 -m ""
rm -rf /var/www/html/openWB/web/themes/dark19_01
(sleep 10; mosquitto_pub -t openWB/set/ChargeMode -r -m "$bootmodus") &
(sleep 10; mosquitto_pub -t openWB/global/ChargeMode -r -m "$bootmodus") &
echo " " > /var/www/html/openWB/ramdisk/lastregelungaktiv
chmod 777 /var/www/html/openWB/ramdisk/lastregelungaktiv
chmod 777 /var/www/html/openWB/ramdisk/smarthome.log
chmod 777 /var/www/html/openWB/ramdisk/smarthomehandlerloglevel

# update etprovider pricelist
echo "etprovider..."
if [[ "$etprovideraktiv" == "1" ]]; then
	echo "update electricity pricelist..."
	echo "" > /var/www/html/openWB/ramdisk/etprovidergraphlist
	mosquitto_pub -r -t openWB/global/ETProvider/modulePath -m "$etprovider"
	/var/www/html/openWB/modules/$etprovider/main.sh > /var/log/openWB.log 2>&1 &
else
	echo "not activated, skipping"
	mosquitto_pub -r -t openWB/global/awattar/pricelist -m ""
fi

# set upload limit in php
#prepare for Buster
echo -n "fix upload limit..."
if [ -d "/etc/php/7.0/" ]; then
	echo "OS Stretch"
	sudo /bin/su -c "echo 'upload_max_filesize = 300M' > /etc/php/7.0/apache2/conf.d/20-uploadlimit.ini"
	sudo /bin/su -c "echo 'post_max_size = 300M' >> /etc/php/7.0/apache2/conf.d/20-uploadlimit.ini"
elif [ -d "/etc/php/7.3/" ]; then
	echo "OS Buster"
	sudo /bin/su -c "echo 'upload_max_filesize = 300M' > /etc/php/7.3/apache2/conf.d/20-uploadlimit.ini"
	sudo /bin/su -c "echo 'post_max_size = 300M' >> /etc/php/7.3/apache2/conf.d/20-uploadlimit.ini"
fi
sudo /usr/sbin/apachectl -k graceful

# all done, remove boot and update status
echo $(date +"%Y-%m-%d %H:%M:%S:") "boot done :-)"
echo 0 > /var/www/html/openWB/ramdisk/bootinprogress
echo 0 > /var/www/html/openWB/ramdisk/updateinprogress
mosquitto_pub -t openWB/system/updateInProgress -r -m "0"
mosquitto_pub -t openWB/system/reloadDisplay -m "1"
