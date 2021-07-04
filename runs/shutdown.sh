#!/bin/bash

sudo rm /var/log/openWB.log
sudo touch /var/log/openWB.log
sudo chmod 777 /var/log/openWB.log
$(sleep 5 && sudo shutdown now)&
