#!/bin/bash
#Ramdisk mit initialen Werten befüllen nach neustart
sleep 10
echo 0 > /var/www/html/openWB/ramdisk/llsoll
touch /var/www/html/openWB/ramdisk/wattbezug
touch /var/www/html/openWB/ramdisk/ladestatus
touch /var/www/html/openWB/ramdisk/lademodus
touch /var/www/html/openWB/ramdisk/llaktuell
touch /var/www/html/openWB/ramdisk/llaktuells1
touch /var/www/html/openWB/ramdisk/pvwatt
touch /var/www/html/openWB/ramdisk/soc
touch /var/www/html/openWB/ramdisk/soc1
touch /var/www/html/openWB/ramdisk/lla1
touch /var/www/html/openWB/ramdisk/lla2
touch /var/www/html/openWB/ramdisk/lla3
touch /var/www/html/openWB/ramdisk/llkombiniert
touch /var/www/html/openWB/ramdisk/llas11
touch /var/www/html/openWB/ramdisk/llas12
touch /var/www/html/openWB/ramdisk/llas13
touch /var/www/html/openWB/ramdisk/llas21
touch /var/www/html/openWB/ramdisk/llas22
touch /var/www/html/openWB/ramdisk/llas23
touch /var/www/html/openWB/ramdisk/llkwh
touch /var/www/html/openWB/ramdisk/pvkwh
touch /var/www/html/openWB/ramdisk/llkwhs1
touch /var/www/html/openWB/ramdisk/einspeisungkwh
touch /var/www/html/openWB/ramdisk/bezugkwh
touch /var/www/html/openWB/ramdisk/llkwhs2
echo 0 > /var/www/html/openWB/ramdisk/pvcounter
echo 0 > /var/www/html/openWB/ramdisk/llas11
echo 0 > /var/www/html/openWB/ramdisk/bezuga1
echo 0 > /var/www/html/openWB/ramdisk/bezuga2
echo 0 > /var/www/html/openWB/ramdisk/bezuga3
echo 0 > /var/www/html/openWB/ramdisk/llv1
echo 0 > /var/www/html/openWB/ramdisk/llv2
echo 0 > /var/www/html/openWB/ramdisk/llv3
echo 0 > /var/www/html/openWB/ramdisk/llaltnv
echo 0 > /var/www/html/openWB/ramdisk/llhz
echo 0 > /var/www/html/openWB/ramdisk/llpf1
echo 0 > /var/www/html/openWB/ramdisk/llpf2
echo 0 > /var/www/html/openWB/ramdisk/llpf3
echo 0 > /var/www/html/openWB/ramdisk/evuv1
echo 0 > /var/www/html/openWB/ramdisk/evuv2
echo 0 > /var/www/html/openWB/ramdisk/evuv3
echo 0 > /var/www/html/openWB/ramdisk/evuhz
echo 0 > /var/www/html/openWB/ramdisk/evupf1
echo 0 > /var/www/html/openWB/ramdisk/evupf2
echo 0 > /var/www/html/openWB/ramdisk/evupf3
echo 0 > /var/www/html/openWB/ramdisk/evuhz
echo 0 > /var/www/html/openWB/ramdisk/gelrlp1
echo 0 > /var/www/html/openWB/ramdisk/gelrlp2
echo 0 > /var/www/html/openWB/ramdisk/llsolls1
echo 0 > /var/www/html/openWB/ramdisk/llsolls2
echo 0 > /var/www/html/openWB/ramdisk/gelrlp3
echo 0 > /var/www/html/openWB/ramdisk/aktgeladen
echo 0 > /var/www/html/openWB/ramdisk/aktgeladens1
echo 0 > /var/www/html/openWB/ramdisk/aktgeladens2
echo 0 > /var/www/html/openWB/ramdisk/llas12
echo 0 > /var/www/html/openWB/ramdisk/llas13
echo 0 > /var/www/html/openWB/ramdisk/wattbezug
echo 0 > /var/www/html/openWB/ramdisk/ladestatus
echo 0 > /var/www/html/openWB/ramdisk/lademodus
echo 0 > /var/www/html/openWB/ramdisk/llaktuell
echo 0 > /var/www/html/openWB/ramdisk/pvwatt
echo 0 > /var/www/html/openWB/ramdisk/soc
echo 0 > /var/www/html/openWB/ramdisk/lla1
echo 0 > /var/www/html/openWB/ramdisk/lla2
echo 0 > /var/www/html/openWB/ramdisk/lla3	
echo 0 > /var/www/html/openWB/ramdisk/llaktuells1
echo 0 > /var/www/html/openWB/ramdisk/llaktuells2
touch /var/www/html/openWB/ramdisk/llog1
touch /var/www/html/openWB/ramdisk/llogs1
touch /var/www/html/openWB/ramdisk/llogs2
echo 0 > /var/www/html/openWB/ramdisk/llkombiniert
echo 0 > /var/www/html/openWB/ramdisk/llkwh
echo 0 > /var/www/html/openWB/ramdisk/pvkwh
echo 0 > /var/www/html/openWB/ramdisk/bezugkwh
echo 0 > /var/www/html/openWB/ramdisk/einspeisungkwh
echo 0 > /var/www/html/openWB/ramdisk/llkwhs1
sudo chown -R www-data:www-data /var/www/html/openWB/web/backup
sudo chown -R www-data:www-data /var/www/html/openWB/web/tools/upload
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod -R +x /var/www/html/openWB/modules/*
ln -s /var/log/openWB.log /var/www/html/openWB/ramdisk/openWB.log

if ! grep -Fq "abschaltverzoegerung=" /var/www/html/openWB/openwb.conf
then
  echo "abschaltverzoegerung=10" >> /var/www/html/openWB/openwb.conf
fi
if ps ax |grep -v grep |grep "python /var/www/html/openWB/runs/ladetaster.py" > /dev/null
then
	echo "test" > /dev/null
else
	sudo python /var/www/html/openWB/runs/ladetaster.py &
fi

if ! grep -Fq "minimalapv=" /var/www/html/openWB/openwb.conf
then
	  echo "minimalapv=6" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "minimalampv=" /var/www/html/openWB/openwb.conf
then
	  echo "minimalampv=10" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "pvbezugeinspeisung=" /var/www/html/openWB/openwb.conf
then
	  echo "pvbezugeinspeisung=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsecons2=" /var/www/html/openWB/openwb.conf
then
	  echo "evsecons2=dac" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsesources2=" /var/www/html/openWB/openwb.conf
then
	  echo "evsesources2=dac" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evseids2=" /var/www/html/openWB/openwb.conf
then
	  echo "evseids2=3" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evselanips2=" /var/www/html/openWB/openwb.conf
then
	  echo "evselanips2=192.168.14.2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ladeleistungs2modul=" /var/www/html/openWB/openwb.conf
then
	  echo "ladeleistungs2modul=sdm630modbuslls2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdmids2=" /var/www/html/openWB/openwb.conf
then
	  echo "sdmids2=4" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lastmanagements2=" /var/www/html/openWB/openwb.conf
then
	  echo "lastmanagements2=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortlls1=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortlls1=18" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortlls2=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortlls2=17" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "dspeed=" /var/www/html/openWB/openwb.conf
then
	  echo "dspeed=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "durchslp1=" /var/www/html/openWB/openwb.conf
then
	  echo "durchslp1=15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "durchslp3=" /var/www/html/openWB/openwb.conf
then
	  echo "durchslp3=15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "durchslp2=" /var/www/html/openWB/openwb.conf
then
	  echo "durchslp2=15" >> /var/www/html/openWB/openwb.conf
fi
if [ ! -e /var/www/html/openWB/web/ladelog ]; then
	sudo touch /var/www/html/openWB/web/ladelog
	sudo echo Start > /var/www/html/openWB/web/ladelog

	sudo chmod 777 /var/www/html/openWB/web/ladelog
fi


