#/bin/bash

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
	apt-get -qq install -y libapache2-mod-php5
	sleep 2
	apt-get -qq install -y jq
	sleep 2
	apt-get -qq install -y php5-gd
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

echo "check for initial git clone"
if [ ! -d /var/www/html/openWB/web ]; then
	cd /var/www/html/
	git clone https://github.com/snaptec/openWB.git
	chown -R pi:pi openWB 
	echo "... git cloned"
else
	echo "...ok"
fi

echo "check for ramdisk" 
if [ ! -d /var/www/html/openWB/ramdisk ]; then
	mkdir -p /var/www/html/openWB/ramdisk
	echo "tmpfs /var/www/html/openWB/ramdisk tmpfs nodev,nosuid,size=32M 0 0" >> /etc/fstab
	mount -a
	echo "...created"
else
	echo "...ok"
fi


echo "check for crontab"
if grep -Fxq "@reboot /var/www/html/openWB/runs/atreboot.sh &" /var/spool/cron/crontabs/root
then
	echo "...ok"
else
	echo "@reboot /var/www/html/openWB/runs/atreboot.sh &" >> /tmp/tocrontab
	chmod +x /var/www/html/openWB/runs/*
	crontab -l -u root | cat - /tmp/tocrontab | crontab -u root -
	rm /tmp/tocrontab
	echo "...added"
	fi

echo "check for MCP4725"
if [ ! -d /home/pi/Adafruit_Python_MCP4725 ]; then
	apt-get install build-essential python-dev
	cd /home/pi
	git clone https://github.com/adafruit/Adafruit_Python_MCP4725.git
	cd Adafruit_Python_MCP4725
	python setup.py install
	echo "... installed"
else
	echo "...ok"
fi


chmod +x /var/www/html/openWB/modules/*                     
chmod +x /var/www/html/openWB/runs/*


