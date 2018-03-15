#!/bin/bash

cd /var/www/html/
git clone https://github.com/snaptec/openWB.git
sudo chown -R pi:pi openWB 
chmod +x /var/www/html/openWB/modules/*                     
chmod +x /var/www/html/openWB/runs/*

