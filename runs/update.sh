#!/bin/bash

cd /var/www/html/openWB
. /var/www/html/openWB/openwb.conf
cp modules/soc_i3/auth.json /tmp/auth.json
cp modules/soc_i3s1/auth.json /tmp/auth.json.1
cp openwb.conf /tmp/openwb.conf
mkdir /tmp/data
mkdir /tmp/data/daily
cp web/logging/data/daily/* /tmp/data/daily
mkdir /tmp/data/monthly
cp web/logging/data/monthly/* /tmp/data/monthly
sudo git fetch origin
sudo git reset --hard origin/$releasetrain
cd /var/www/html/
sudo chown -R pi:pi openWB 
sudo chown -R www-data:www-data /var/www/html/openWB/web/backup
sudo chown -R www-data:www-data /var/www/html/openWB/web/tools/upload
sudo cp /tmp/openwb.conf /var/www/html/openWB/openwb.conf
sudo cp /tmp/auth.json /var/www/html/openWB/modules/soc_i3/auth.json
sudo cp /tmp/auth.json.1 /var/www/html/openWB/modules/soc_i3s1/auth.json
sudo cp /tmp/data/daily/* /var/www/html/openWB/web/logging/data/daily/
sudo cp /tmp/data/monthly/* /var/www/html/openWB/web/logging/data/monthly/
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod +x /var/www/html/openWB/modules/*                     
sudo chmod +x /var/www/html/openWB/runs/*
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod 777 /var/www/html/openWB/web/lade.log
sleep 2
if ! grep -Fq "wr_http_w_url=" /var/www/html/openWB/openwb.conf
then
	  echo "wr_http_w_url=http://192.168.0.17/pvwatt.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hsocip1=" /var/www/html/openWB/openwb.conf
then
	  echo "hsocip1=http://10.0.0.110/soc.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "socmodul1=" /var/www/html/openWB/openwb.conf
then
	  echo "socmodul1=soc_http1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "dacregisters1=" /var/www/html/openWB/openwb.conf
then
	  echo "dacregisters1=12" >> /var/www/html/openWB/openwb.conf
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

