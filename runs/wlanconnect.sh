#!/bin/bash
wssid=$(</var/www/html/openWB/ramdisk/wssid)
wpassword=$(</var/www/html/openWB/ramdisk/wpassword)
echo "country=DE" > /etc/wpa_supplicant/wpa_supplicant.conf
echo "ctrl_interface=/var/run/wpa_supplicant GROUP=netdev" >> /etc/wpa_supplicant/wpa_supplicant.conf
echo "network={" >> /etc/wpa_supplicant/wpa_supplicant.conf
echo "ssid=\""$wssid"\"" >> /etc/wpa_supplicant/wpa_supplicant.conf
echo "psk=\""$wpassword"\"" >> /etc/wpa_supplicant/wpa_supplicant.conf
echo "}" >> /etc/wpa_supplicant/wpa_supplicant.conf
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
sleep 5
sudo cp /etc/dhcpcd.conf.dhcp /etc/dhcpcd.conf
sudo cp /etc/dnsmasq.conf.dhcp /etc/dnsmasq.conf
systemctl restart dhcpcd 
ifconfig wlan0 up
wpa_cli -i wlan0 reconfigure	
sleep 15
wlan0state=$(</sys/class/net/wlan0/carrier)
wlan0ip=$(ifconfig wlan0 |grep 'inet ' |awk '{print $2}')
if [[ $wlan0state -eq 0 || $wlan0ip -eq "192.168.4.1"  ]]; then
	sudo reboot now
else
	sed -i 's/displayconfigured.*/displayconfigured=1/' /var/www/html/openWB/openwb.conf
fi
