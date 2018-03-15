#!/bin/bash

cd /var/www/html/openWB
git pull origin master:master
cd /var/www/html/
sudo chown -R pi:pi openWB 
chmod +x /var/www/html/openWB/modules/*                     
chmod +x /var/www/html/openWB/runs/*

