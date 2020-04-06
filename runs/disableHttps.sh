#!/bin/sh

sudo a2dissite openwb-ssl
sudo a2dissite redirect-default

sudo a2ensite 000-default

sudo systemctl reload apache2

sudo cp /var/www/html/openWB/configfiles/mosquitto-websocket.conf /etc/mosquitto/conf.d/openwb-websocket.conf
sudo service mosquitto restart
