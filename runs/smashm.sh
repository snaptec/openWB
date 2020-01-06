#!/bin/bash
if [  -d /opt/smaemd ]; then
 	sudo rm -r /opt/smaemd
fi
sudo mkdir -p /etc/smaemd/
cd /opt/
sudo git clone -b master --single-branch https://github.com/david-m-m/SMA-EM.git smaemd
sudo cp smaemd/systemd-settings /etc/systemd/system/smaemd.service
sudo cp /var/www/html/openWB/web/files/smashm.conf /etc/smaemd/config
sudo systemctl daemon-reload
sudo systemctl enable smaemd.service
sleep 1
sudo systemctl stop smaemd.service
sleep 1
sudo systemctl start smaemd.service
