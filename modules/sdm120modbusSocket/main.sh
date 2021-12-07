#!/bin/bash

if [[ $sdm120modbussocketid != "none" ]]; then
	sudo python /var/www/html/openWB/modules/sdm120modbusSocket/readsdm.py $sdm120modbussocketsource $sdm120modbussocketid
fi
