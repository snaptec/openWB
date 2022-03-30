#!/bin/sh

newIpEth0=$1
newIpWlan0=$2
echo "Changing virtual ip for eth0 to ${newIpEth0}..."
sed -i "s/^virtual_ip_eth0=.*/virtual_ip_eth0='${newIpEth0}'/" /var/www/html/openWB/openwb.conf
echo "Changing virtual ip for wlan0 to ${newIpWlan0}..."
sed -i "s/^virtual_ip_wlan0=.*/virtual_ip_wlan0='${newIpWlan0}'/" /var/www/html/openWB/openwb.conf
echo "done"
