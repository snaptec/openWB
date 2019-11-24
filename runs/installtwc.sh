#!/bin/bash
sudo apt-get -qq install -y screen
sudo apt-get -qq install -y python3-pip
sudo python3 -m pip install pyserial
sudo python3 -m pip install sysv_ipc
cd /var/www/html/
git clone -b master --single-branch https://github.com/cdragon/TWCManager.git TWC
