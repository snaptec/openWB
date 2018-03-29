#!/bin/bash

cd /var/www/html/openWB
sudo git reset --hard
sudo git pull origin master:master
cd /var/www/html/
sudo chown -R pi:pi openWB 
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod +x /var/www/html/openWB/modules/*                     
sudo chmod +x /var/www/html/openWB/runs/*
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod 777 /var/www/html/openWB/web/lade.log
sleep 2
sudo /var/www/html/openWB/runs/atreboot.sh

