#!/bin/bash
if [ ! -d /opt/smaemd ]; then
	sudo mkdir /opt/smaemd/
	sudo mkdir /etc/smaemd/
	cd /opt/smaemd/
	sudo git clone https://github.com/datenschuft/SMA-EM.git .
	sudo cp systemd-settings /etc/systemd/system/smaemd.service
fi
sudo cp /var/www/html/openWB/web/files/smashm.conf /etc/smaemd/config
sudo systemctl daemon-reload
sudo systemctl enable smaemd.service
sudo systemctl start smaemd.service
