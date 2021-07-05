#!/bin/sh

newHostname=$1
newVirtual_ip_eth0_evu=$2
newVirtual_ip_wlan0_evu=$3
echo "Changing hostname to $newHostname..."
touch /tmp/tmphostname
echo $newHostname > /tmp/tmphostname
mv /tmp/tmphostname /etc/hostname
sed -i "s/127.0.1.1.*/127.0.1.1    $newHostname/" /etc/hosts
sed -i "s/virtual_ip_eth0_evu=.*/virtual_ip_eth0_evu=$newVirtual_ip_eth0_evu/" /var/www/html/openWB/openwb.conf
sed -i "s/virtual_ip_wlan0_evu=.*/virtual_ip_wlan0_evu=$newVirtual_ip_wlan0_evu/" /var/www/html/openWB/openwb.conf
echo "done"
