#!/bin/bash

cd /var/www/html/openWB
cp openwb.conf /tmp/openwb.conf
sudo git fetch origin
sudo git reset --hard origin/master
cd /var/www/html/
sudo chown -R pi:pi openWB 
sudo cp /tmp/openwb.conf /var/www/html/openWB/openwb.conf
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod +x /var/www/html/openWB/modules/*                     
sudo chmod +x /var/www/html/openWB/runs/*
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod 777 /var/www/html/openWB/web/lade.log
sleep 2
if ! grep -Fq "wr_http_w_url=" /var/www/html/openwb.conf
then
	  echo "wr_http_w_url=http://192.168.0.17/pvwatt.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wr_http_kwh_url=" /var/www/html/openwb.conf
then
	  echo "wr_http_kwh_url=http://192.168.0.17/pvwh.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_http_w_url=" /var/www/html/openwb.conf
then
	  echo "bezug_http_w_url=http://192.168.0.17/bezugwatt.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_http_ikwh_url=" /var/www/html/openwb.conf
then
	  echo "bezug_http_ikwh_url=http://192.168.0.17/bezugwh.txt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_http_ekwh_url=" /var/www/html/openwb.conf
then
	  echo "bezug_http_ekwh_url=http://192.168.0.17/einspeisungwh.txt" >> /var/www/html/openWB/openwb.conf
fi


sudo /var/www/html/openWB/runs/atreboot.sh

