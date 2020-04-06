#!/bin/sh

sudo cp /var/www/html/openWB/configfiles/openwb-ssl.conf /etc/apache2/sites-available/
sudo cp /var/www/html/openWB/configfiles/redirect-default.conf /etc/apache2/sites-available/

sudo a2enmod ssl
sudo a2enmod rewrite

sudo a2ensite openwb-ssl
sudo a2ensite redirect-default

sudo a2dissite 000-default

sudo systemctl reload apache2

sudo cp /var/www/html/openWB/configfiles/mosquitto-websocketSSL.conf /etc/mosquitto/conf.d/openwb-websocket.conf
sudo service mosquitto restart
