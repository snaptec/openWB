#!/bin/bash

sudo rm /var/log/openWB.log
sudo touch /var/log/openWB.log
sudo chmod ugo=rwX /var/log/openWB.log
$(sleep 5 && sudo reboot now)&
