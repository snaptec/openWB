#!/bin/bash

cd /var/www/html/
git pull origin master:master
sudo chown -R pi:pi openWB 
chmod +x /var/www/html/openWB/modules/*                     
chmod +x /var/www/html/openWB/runs/*

