#!/bin/bash


sudo cp /var/www/html/openWB/web/tools/upload/backup.tar.gz /home/pi/backup.tar.gz
cd /home/pi/
sudo tar -xf backup.tar.gz
sudo cp -R /home/pi/var/www/html/openWB/ /var/www/html/openWB/
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo rm /var/www/html/openWB/web/tools/upload/backup.tar.gz
sudo rm /home/pi/backup.tar.gz


