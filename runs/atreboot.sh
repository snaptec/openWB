#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"

echo "atreboot.sh started"
(sleep 600; sudo kill $(ps aux |grep '[a]treboot.sh' | awk '{print $2}'); echo 0 > $RAMDISKDIR/bootinprogress; echo 0 > $RAMDISKDIR/updateinprogress) &

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "atreboot.sh: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

openwbDebugLog "MAIN" 0 "##### atreboot.sh started #####"

# load functions to init ramdisk and update config
# no code will run here, functions need to be called
. $OPENWBBASEDIR/runs/initRamdisk.sh
. $OPENWBBASEDIR/runs/updateConfig.sh

sleep 5
openwbDebugLog "MAIN" 1 "fixing file and folder permissions"
mkdir -p $OPENWBBASEDIR/web/backup
touch $OPENWBBASEDIR/web/backup/.donotdelete
sudo chown -R www-data:www-data $OPENWBBASEDIR/web/backup
sudo chown -R www-data:www-data $OPENWBBASEDIR/web/tools/upload
sudo chmod 777 $OPENWBBASEDIR/openwb.conf
sudo chmod 777 $OPENWBBASEDIR/smarthome.ini
sudo chmod 777 $RAMDISKDIR
sudo chmod 777 $RAMDISKDIR/
sudo chmod 777 $OPENWBBASEDIR/web/files/*
sudo chmod -R +x $OPENWBBASEDIR/modules/*

sudo chmod -R 777 $OPENWBBASEDIR/modules/soc_i3
sudo chmod -R 777 $OPENWBBASEDIR/modules/soc_eq
sudo chmod -R 777 $OPENWBBASEDIR/modules/soc_tesla

sudo chmod 777 $OPENWBBASEDIR/web/files/*
sudo chmod -R +x $OPENWBBASEDIR/modules/*

mkdir -p $OPENWBBASEDIR/web/logging/data/daily
mkdir -p $OPENWBBASEDIR/web/logging/data/monthly
mkdir -p $OPENWBBASEDIR/web/logging/data/ladelog
mkdir -p $OPENWBBASEDIR/web/logging/data/v001
sudo chmod -R 777 $OPENWBBASEDIR/web/logging/data/

# update openwb.conf
updateConfig
# reload our changed openwb.conf
. $OPENWBBASEDIR/loadconfig.sh
# now setup all files in ramdisk
initRamdisk

# standard socket - activated after reboot due to RASPI init defaults so we need to disable it as soon as we can
if [[ $standardSocketInstalled == "1" ]]; then
	openwbDebugLog "MAIN" 0 "turning off standard socket ..."
	sudo python $OPENWBBASEDIR/runs/standardSocket.py off
fi

# initialize automatic phase switching
if (( u1p3paktiv == 1 )); then
	openwbDebugLog "MAIN" 0 "triginit..."
	sudo python $OPENWBBASEDIR/runs/triginit.py -d $u1p3ppause
fi

# check if buttons are configured and start daemon
if (( ladetaster == 1 )); then
	openwbDebugLog "MAIN" 0 "pushbuttons..."
	if ! [ -x "$(command -v nmcli)" ]; then
		if ps ax |grep -v grep |grep "python $OPENWBBASEDIR/runs/ladetaster.py" > /dev/null
		then
			openwbDebugLog "MAIN" 1 "pushbutton handler already running"
		else
			openwbDebugLog "MAIN" 0 "pushbutton handler not detected; restarting"
			sudo python $OPENWBBASEDIR/runs/ladetaster.py &
		fi
	fi
fi

# check for rse and start daemon
if (( rseenabled == 1 )); then
	openwbDebugLog "MAIN" 0 "rse..."
	if ! [ -x "$(command -v nmcli)" ]; then
		if ps ax |grep -v grep |grep "python $OPENWBBASEDIR/runs/rse.py" > /dev/null
		then
			openwbDebugLog "MAIN" 0 "rse handler already running"
		else
			openwbDebugLog "MAIN" 0 "rse handler not detected; restarting"
			sudo python $OPENWBBASEDIR/runs/rse.py &
		fi
	fi
fi

# check if rfid is configured and start daemons to listen on input devices
if (( rfidakt == 1 )); then
	openwbDebugLog "MAIN" 0 "rfid mode 1..."
	sudo kill $(ps aux |grep '[r]eadrfid.py' | awk '{print $2}')
	(sleep 10; sudo python $OPENWBBASEDIR/runs/readrfid.py $displayaktiv) &
	(sleep 10; sudo python $OPENWBBASEDIR/runs/readrfid2.py $displayaktiv) &
fi
if (( rfidakt == 2 )); then
	openwbDebugLog "MAIN" 0 "rfid mode 2..."
	sudo kill $(ps aux |grep '[r]eadrfid.py' | awk '{print $2}')
	(sleep 10; sudo python $OPENWBBASEDIR/runs/readrfid.py $displayaktiv) &
	(sleep 10; sudo python $OPENWBBASEDIR/runs/readrfid2.py $displayaktiv) &
fi

# check if tesla wall connector is configured and start daemon
if [[ $evsecon == twcmanager ]]; then
	openwbDebugLog "MAIN" 0 "twcmanager..."
	if [[ $twcmanagerlp1ip == "localhost/TWC" ]]; then
		screen -dm -S TWCManager /var/www/html/TWC/TWCManager.py &
	fi
fi

# check if display is configured and setup timeout
if (( displayaktiv == 1 )); then
	openwbDebugLog "MAIN" 0 "display..."
	if ! grep -Fq "pinch" /home/pi/.config/lxsession/LXDE-pi/autostart
	then
		openwbDebugLog "MAIN" 1 "autostart file not found; creating new file"
		echo "@xscreensaver -no-splash" > /home/pi/.config/lxsession/LXDE-pi/autostart
		echo "@point-rpi" >> /home/pi/.config/lxsession/LXDE-pi/autostart
		echo "@xset s 600" >> /home/pi/.config/lxsession/LXDE-pi/autostart
		echo "@chromium-browser --incognito --disable-pinch --kiosk http://localhost/openWB/web/display.php" >> /home/pi/.config/lxsession/LXDE-pi/autostart
	fi
fi

# restart smarthomehandler
openwbDebugLog "MAIN" 0 "smarthome handler..."
if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/smarthomehandler.py" > /dev/null
then
	sudo kill $(ps aux |grep '[s]marthomehandler.py' | awk '{print $2}')
fi
python3 $OPENWBBASEDIR/runs/smarthomehandler.py >> $RAMDISKDIR/smarthome.log 2>&1 &

# restart mqttsub handler
openwbDebugLog "MAIN" 0 "mqtt handler..."
if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/mqttsub.py" > /dev/null
then
	sudo kill $(ps aux |grep '[m]qttsub.py' | awk '{print $2}')
fi
python3 $OPENWBBASEDIR/runs/mqttsub.py &

# check crontab for user pi
openwbDebugLog "MAIN" 0 "crontab 1..."
crontab -l -u pi > $RAMDISKDIR/tmpcrontab
if grep -Fq "lade.log" $RAMDISKDIR/tmpcrontab
then
	openwbDebugLog "MAIN" 1 "crontab for user pi modified"
	sed -i '/lade.log/d' $RAMDISKDIR/tmpcrontab
	echo "* * * * * $OPENWBBASEDIR/regel.sh >> /var/log/openWB.log 2>&1" >> $RAMDISKDIR/tmpcrontab
	cat $RAMDISKDIR/tmpcrontab | crontab -u pi -
fi

# check crontab for user root and remove old @reboot entry
sudo crontab -l > $RAMDISKDIR/tmprootcrontab
if grep -Fq "atreboot.sh" $RAMDISKDIR/tmprootcrontab
then
	openwbDebugLog "MAIN" 1 "crontab for user root modified"
	sed -i '/atreboot.sh/d' $RAMDISKDIR/tmprootcrontab
	cat $RAMDISKDIR/tmprootcrontab | sudo crontab -
fi

# check for LAN/WLAN connection
openwbDebugLog "MAIN" 0 "LAN/WLAN..."
	sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 up
else
	sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 up
fi

# check for apache configuration
openwbDebugLog "MAIN" 0 "apache..."
if grep -Fxq "AllowOverride" /etc/apache2/sites-available/000-default.conf
then
	openwbDebugLog "MAIN" 0 "...ok"
else
	sudo cp $OPENWBBASEDIR/web/tools/000-default.conf /etc/apache2/sites-available/
	openwbDebugLog "MAIN" 0 "...changed"
fi

# add some crontab entries for user pi
openwbDebugLog "MAIN" 0 "crontab 2..."
if ! sudo grep -Fq "cronnightly.sh" /var/spool/cron/crontabs/pi
then
	openwbDebugLog "MAIN" 1 "adding cronjob for cronnightly.sh"
	(crontab -l -u pi ; echo "1 0 * * * $OPENWBBASEDIR/runs/cronnightly.sh >> /var/log/openWB.log 2>&1")| crontab -u pi -
fi
if ! sudo grep -Fq "cron5min.sh" /var/spool/cron/crontabs/pi
then
	openwbDebugLog "MAIN" 1 "adding cronjob for cron5min.sh"
	(crontab -l -u pi ; echo "*/5 * * * * $OPENWBBASEDIR/runs/cron5min.sh >> /var/log/openWB.log 2>&1")| crontab -u pi -
fi
if ! sudo grep -Fq "atreboot.sh" /var/spool/cron/crontabs/pi
then
	openwbDebugLog "MAIN" 1 "adding cronjob for atreboot.sh"
	(crontab -l -u pi ; echo "@reboot $OPENWBBASEDIR/runs/atreboot.sh >> /var/log/openWB.log 2>&1")| crontab -u pi -
fi

# check for needed packages
openwbDebugLog "MAIN" 0 "packages 1..."
if python -c "import evdev" &> /dev/null; then
	openwbDebugLog "MAIN" 1 "evdev installed..."
else
	openwbDebugLog "MAIN" 0 "installing evdev"
	sudo pip install evdev
fi
if ! [ -x "$(command -v sshpass)" ];then
	openwbDebugLog "MAIN" 0 "installing sshpass"
	apt-get -qq update
	sleep 1
	apt-get -qq install sshpass
fi
if [ $(dpkg-query -W -f='${Status}' php-gd 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	openwbDebugLog "MAIN" 0 "installing php modules"
	sudo apt-get -qq update
	sleep 1
	sudo apt-get -qq install -y php-gd
	sleep 1
	sudo apt-get -qq install -y php7.0-xml
fi

# update old ladelog
$OPENWBBASEDIR/runs/transferladelog.sh

# check for led handler
if (( ledsakt == 1 )); then
	openwbDebugLog "MAIN" 0 "initializing leds..."
	sudo python $OPENWBBASEDIR/runs/leds.py startup
fi

# setup timezone
openwbDebugLog "MAIN" 0 "timezone..."
sudo cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# check for mosquitto packages
openwbDebugLog "MAIN" 0 "mosquitto..."
if [ ! -f /etc/mosquitto/mosquitto.conf ]; then
	openwbDebugLog "MAIN" 0 "installing server and client packages"
	sudo apt-get update
	sudo apt-get -qq install -y mosquitto mosquitto-clients
	sudo service mosquitto restart
fi

# check for mosquitto configuration
if [ ! -f /etc/mosquitto/conf.d/openwb.conf ]; then
	openwbDebugLog "MAIN" 0 "adding openwb.conf for mosquitto"
	sudo cp $OPENWBBASEDIR/web/files/mosquitto.conf /etc/mosquitto/conf.d/openwb.conf
	sudo service mosquitto restart
fi

# check for other dependencies
openwbDebugLog "MAIN" 0 "packages 2..."
if python3 -c "import paho.mqtt.publish as publish" &> /dev/null; then
	openwbDebugLog "MAIN" 1 "paho mqtt already installed"
else
	openwbDebugLog "MAIN" 0 "installing paho-mqtt for python3"
	sudo apt-get -qq install -y python3-pip
	sudo pip3 install paho-mqtt
fi
if python3 -c "import docopt" &> /dev/null; then
	openwbDebugLog "MAIN" 1 "docopt already installed"
else
	openwbDebugLog "MAIN" 0 "installing docopt for python3"
	sudo pip3 install docopt
fi
if python3 -c "import certifi" &> /dev/null; then
	openwbDebugLog "MAIN" 1 "certifi already installed"
else
	openwbDebugLog "MAIN" 0 "installing certifi for python3"
	sudo pip3 install certifi
fi
if python3 -c "import aiohttp" &> /dev/null; then
	openwbDebugLog "MAIN" 1 "aiohttp already installed"
else
	openwbDebugLog "MAIN" 0 "installing aiohttp for python3"
	sudo pip3 install aiohttp
fi
if python3 -c "import pymodbus" &> /dev/null; then
	openwbDebugLog "MAIN" 1 "pymodbus already installed"
else
	openwbDebugLog "MAIN" 0 "installing pymodbus for python3"
	sudo pip3 install pymodbus
fi
if python3 -c "import jq" &> /dev/null; then
	openwbDebugLog "MAIN" 1 "jq already installed"
else
	openwbDebugLog "MAIN" 0 "installing jq for python3"
	sudo pip3 install jq
fi

# update version
openwbDebugLog "MAIN" 0 "version..."
uuid=$(</sys/class/net/eth0/address)
owbv=$(<$OPENWBBASEDIR/web/version)
curl -d "update="$releasetrain$uuid"vers"$owbv"" -H "Content-Type: application/x-www-form-urlencoded" -X POST https://openwb.de/tools/update.php

# all done, remove warning in display
openwbDebugLog "MAIN" 0 "clear warning..."
echo "" > $RAMDISKDIR/lastregelungaktiv
echo "" > $RAMDISKDIR/mqttlastregelungaktiv
chmod 777 $RAMDISKDIR/mqttlastregelungaktiv

#if [ $(dpkg-query -W -f='${Status}' php-curl 2>/dev/null | grep -c "ok installed") -eq 0 ];
#then
#  sudo apt-get update
#  sudo apt-get -qq install -y php-curl
#fi

# check for slave config and start handler
if (( isss == 1 )); then
	openwbDebugLog "MAIN" 0 "isss..."
	echo $lastmanagement > $RAMDISKDIR/issslp2act
	if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/isss.py" > /dev/null
	then
		sudo kill $(ps aux |grep '[i]sss.py' | awk '{print $2}')
	fi
	python3 $OPENWBBASEDIR/runs/isss.py &
	# second IP already set up !
	# ethstate=$(</sys/class/net/eth0/carrier)
	# if (( ethstate == 1 )); then
	# 	sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 down
	# else
	# 	sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 down
	# fi
fi

# check for socket system and start handler
if [[ "$evsecon" == "buchse" ]]  && [[ "$isss" == "0" ]]; then
	openwbDebugLog "MAIN" 0 "socket..."
	# ppbuchse is used in issss.py to detect "openWB Buchse"
	if [ ! -f /home/pi/ppbuchse ]; then
		echo "32" > /home/pi/ppbuchse
	fi
	if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/buchse.py" > /dev/null
	then
		sudo kill $(ps aux |grep '[b]uchse.py' | awk '{print $2}')
	fi
	python3 $OPENWBBASEDIR/runs/buchse.py &
fi

# check for rfid mode 2 and start handler
if [[ "$rfidakt" == "2" ]]; then
	openwbDebugLog "MAIN" 0 "rfid 2 handler..."
	if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/rfid.py" > /dev/null
	then
		sudo kill $(ps aux |grep '[r]fid.py' | awk '{print $2}')
	fi
	python3 $OPENWBBASEDIR/runs/rfid.py &
fi

# update display configuration
openwbDebugLog "MAIN" 0 "display update..."
if grep -Fq "@chromium-browser --incognito --disable-pinch --kiosk http://localhost/openWB/web/display.php" /home/pi/.config/lxsession/LXDE-pi/autostart
then
	sed -i "s,@chromium-browser --incognito --disable-pinch --kiosk http://localhost/openWB/web/display.php,@chromium-browser --incognito --disable-pinch --overscroll-history-navigation=0 --kiosk http://localhost/openWB/web/display.php,g" /home/pi/.config/lxsession/LXDE-pi/autostart
fi

# get local ip
openwbDebugLog "MAIN" 0 "update local ip..."
ip route get 1 | awk '{print $7;exit}' > $RAMDISKDIR/ipaddress

# update current published versions
openwbDebugLog "MAIN" 0 "load versions..."
curl -s https://raw.githubusercontent.com/snaptec/openWB/master/web/version > $RAMDISKDIR/vnightly
curl -s https://raw.githubusercontent.com/snaptec/openWB/beta/web/version > $RAMDISKDIR/vbeta
curl -s https://raw.githubusercontent.com/snaptec/openWB/stable/web/version > $RAMDISKDIR/vstable

# update our local version
sudo git -C $OPENWBBASEDIR show --pretty='format:%ci [%h]' | head -n1 > $OPENWBBASEDIR/web/lastcommit

# update broker
openwbDebugLog "MAIN" 0 "update broker..."
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
rm -rf $OPENWBBASEDIR/web/themes/dark19_01
(sleep 10; mosquitto_pub -t openWB/set/ChargeMode -r -m "$bootmodus") &
(sleep 10; mosquitto_pub -t openWB/global/ChargeMode -r -m "$bootmodus") &
echo " " > $RAMDISKDIR/lastregelungaktiv
chmod 777 $RAMDISKDIR/lastregelungaktiv
chmod 777 $RAMDISKDIR/smarthome.log
chmod 777 $RAMDISKDIR/smarthomehandlerloglevel

# update etprovider pricelist
openwbDebugLog "MAIN" 0 "etprovider..."
if [[ "$etprovideraktiv" == "1" ]]; then
	openwbDebugLog "MAIN" 0 "update electricity pricelist..."
	echo "" > $RAMDISKDIR/etprovidergraphlist
	mosquitto_pub -r -t openWB/global/ETProvider/modulePath -m "$etprovider"
	$OPENWBBASEDIR/modules/$etprovider/main.sh > /var/log/openWB.log 2>&1 &
else
	openwbDebugLog "MAIN" 1 "not activated, skipping"
	mosquitto_pub -r -t openWB/global/awattar/pricelist -m ""
fi

# set upload limit in php
openwbDebugLog "MAIN" 0 "fix upload limit..."
if [ -d "/etc/php/7.0/" ]; then
	openwbDebugLog "MAIN" 0 "OS Stretch"
	sudo /bin/su -c "echo 'upload_max_filesize = 300M' > /etc/php/7.0/apache2/conf.d/20-uploadlimit.ini"
	sudo /bin/su -c "echo 'post_max_size = 300M' >> /etc/php/7.0/apache2/conf.d/20-uploadlimit.ini"
elif [ -d "/etc/php/7.3/" ]; then
	openwbDebugLog "MAIN" 0 "OS Buster"
	sudo /bin/su -c "echo 'upload_max_filesize = 300M' > /etc/php/7.3/apache2/conf.d/20-uploadlimit.ini"
	sudo /bin/su -c "echo 'post_max_size = 300M' >> /etc/php/7.3/apache2/conf.d/20-uploadlimit.ini"
fi
sudo /usr/sbin/apachectl -k graceful

# all done, remove boot and update status
openwbDebugLog "MAIN" 0 "boot done :-)"
echo 0 > $RAMDISKDIR/bootinprogress
echo 0 > $RAMDISKDIR/updateinprogress
mosquitto_pub -t openWB/system/updateInProgress -r -m "0"
mosquitto_pub -t openWB/system/reloadDisplay -m "1"

openwbDebugLog "MAIN" 0 "##### atreboot.sh finished #####"
