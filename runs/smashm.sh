#!/bin/bash
if [  -d /opt/smaemd ]; then
	sudo rm -r /opt/smaemd
fi
	sudo mkdir /opt/smaemd/
	sudo mkdir /etc/smaemd/
	cd /opt/smaemd/
	sudo git clone https://github.com/david-m-m/SMA-EM/tree/master .
	sudo cp systemd-settings /etc/systemd/system/smaemd.service
#fi
sudo cp /var/www/html/openWB/web/files/smashm.conf /etc/smaemd/config
sudo systemctl daemon-reload
sudo systemctl enable smaemd.service
sleep 1
sudo systemctl stop smaemd.service
sleep 1
sudo systemctl start smaemd.service
