#!/bin/bash
#if [ ! -d /opt/smaemd ]; then
sudo mkdir /opt/smaemd/
sudo mkdir /etc/smaemd/
cd /opt/smaemd/
sudo git clone https://github.com/datenschuft/SMA-EM.git .
sudo git reset --hard 3586f3ca94ab8de17c709337615e896cb158f973
sudo cp systemd-settings /etc/systemd/system/smaemd.service
#fi
sudo cp /var/www/html/openWB/web/files/smashm.conf /etc/smaemd/config
sudo systemctl daemon-reload
sudo systemctl enable smaemd.service
sleep 1
sudo systemctl stop smaemd.service
sleep 1
sudo systemctl start smaemd.service
