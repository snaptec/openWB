#!/bin/bash

echo "update system"
apt-get update

echo "check for vim"
if ! [ -x "$(command -v vim)" ]; then
	apt-get -qq install -y vim
	echo "... installed"
else
	echo "...ok"
fi
echo "check for timezone"
if  grep -Fxq "Europe/Berlin" /etc/timezone
then
	echo "...ok"
else
	echo 'Europe/Berlin' > /etc/timezone
	dpkg-reconfigure -f noninteractive tzdata
	cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime
	echo "...changed"
fi

echo "check for bc"
if ! [ -x "$(command -v bc)" ];then
	apt-get -qq install bc
	echo "...installed"
else
	echo "...ok"
fi

echo "check for apache"
if ! [ -x "$(command -v apachectl)" ]; then
	apt-get -qq install -y apache2
	sleep 2
	apt-get -qq install -y php
	sleep 1
	apt-get -qq install -y php-gd
	sleep 1
	#prepare for Buster
	if [ -d "/etc/php/7.0/" ]; then 
		apt-get -qq install -y php7.0-xml
	elif [ -d "/etc/php/7.3/" ]; then
		apt-get -qq install -y php7.3-xml
	fi	
	sleep 2
	apt-get -qq install -y php-curl
	sleep 1	
	#prepare for Buster
	if [ -d "/etc/php/7.0/" ]; then 
		apt-get -qq install -y libapache2-mod-php7.0
	elif [ -d "/etc/php/7.3/" ]; then
		apt-get -qq install -y libapache2-mod-php7.3
	fi	
	sleep 2
	apt-get -qq install -y jq
	sleep 2
	apt-get -qq install -y raspberrypi-kernel-headers
	echo "... installed"
else
	echo "...ok"
fi

echo "check for i2c bus"
if grep -Fxq "i2c-bcm2835" /etc/modules
then
	echo "...ok"
else
	echo "i2c-dev" >> /etc/modules
	echo "i2c-bcm2708" >> /etc/modules
	echo "snd-bcm2835" >> /etc/modules
	echo "dtparam=i2c1=on" >> /etc/modules
	echo "dtparam=i2c_arm=on" >> /etc/modules
fi

echo "check for i2c package"
if ! [ -x "$(command -v i2cdetect)" ]; then
	apt-get -qq install -y i2c-tools
	echo "... installed"
else
	echo "...ok"
fi

echo "check for git"
if ! [ -x "$(command -v git)" ]; then
	apt-get -qq install -y git
	echo "... installed"
else
	echo "...ok"
fi

echo "check for initial git clone"
if [ ! -d /var/www/html/openWB/web ]; then
	cd /var/www/html/
	git clone https://github.com/snaptec/openWB.git --branch master
	chown -R pi:pi openWB 
	echo "... git cloned"
else
	echo "...ok"
fi
if ! grep -Fq "bootmodus=" /var/www/html/openWB/openwb.conf
then
	echo "bootmodus=3" >> /var/www/html/openWB/openwb.conf
fi
echo "check for ramdisk" 
if grep -Fxq "tmpfs /var/www/html/openWB/ramdisk tmpfs nodev,nosuid,size=32M 0 0" /etc/fstab 
then
	echo "...ok"
else
	mkdir -p /var/www/html/openWB/ramdisk
	echo "tmpfs /var/www/html/openWB/ramdisk tmpfs nodev,nosuid,size=32M 0 0" >> /etc/fstab
	mount -a
	echo "0" > /var/www/html/openWB/ramdisk/ladestatus
	echo "0" > /var/www/html/openWB/ramdisk/llsoll
	echo "0" > /var/www/html/openWB/ramdisk/soc
	echo "...created"
fi

echo "check for crontab"
if grep -Fxq "@reboot /var/www/html/openWB/runs/atreboot.sh &" /var/spool/cron/crontabs/root
then
	echo "...ok"
else
	echo "@reboot /var/www/html/openWB/runs/atreboot.sh &" >> /tmp/tocrontab
	crontab -l -u root | cat - /tmp/tocrontab | crontab -u root -
	rm /tmp/tocrontab
	echo "...added"
fi

#echo "check for MCP4725"
####### Library is deprecated. the manual install doesn't work anymore pip3 install for compatibility reasons
#if [ ! -d /home/pi/Adafruit_Python_MCP4725 ]; then
	#apt-get install build-essential python-dev
	#cd /home/pi
	#git clone https://github.com/adafruit/Adafruit_Python_MCP4725.git
	#cd Adafruit_Python_MCP4725
	#python setup.py install
	#echo "... installed"
#else
	#echo "...ok"
#fi

echo "check for socat"
if ! [ -x "$(command -v socat)" ]; then
	apt-get -qq install -y socat
	echo "... installed"
else
	echo "...ok"
fi

echo "disable cronjob logging"
if grep -Fxq "EXTRA_OPTS=\"-L 0\"" /etc/default/cron
then
	echo "...ok"
else
	echo "EXTRA_OPTS=\"-L 0\"" >> /etc/default/cron
fi

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

echo "checking for pip..."
if ! [ -x "$(command -v pip)" ]; then
        sudo apt-get -qq install -y python-pip
        echo "...OK"
else
        echo "pip is installed"
fi

echo "checking for pip3..."
if ! [ -x "$(command -v pip3)" ]; then
        sudo apt-get -qq install -y python3-pip
        echo "...OK"
else
        echo "pip3 is installed"
fi

echo "installing pymodbus"
sudo pip install  -U pymodbus

echo "check for paho-mqtt"
if python3 -c "import paho.mqtt.publish as publish" &> /dev/null; then
        echo 'mqtt installed...'
else
        sudo pip3 install paho-mqtt
fi

#Adafruit install
echo "check for MCP4725"
#if python3 -c "import Adafruit_MCP4725" &> /dev/null; then
        #echo 'Adafruit_MCP4725 installed...'
#else
        #sudo pip3 install Adafruit_MCP4725
#fi
if python -c "import Adafruit_MCP4725" &> /dev/null; then
        echo 'Adafruit_MCP4725 installed...'
else
        sudo pip install Adafruit_MCP4725
fi

echo "www-data ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/010_pi-nopasswd

chmod 777 /var/www/html/openWB/openwb.conf
chmod +x /var/www/html/openWB/modules/*
chmod +x /var/www/html/openWB/runs/*
touch /var/log/openWB.log
chmod 777 /var/log/openWB.log
/var/www/html/openWB/runs/atreboot.sh
