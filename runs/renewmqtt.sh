#!/bin/bash
#force pushing all values in broker
timeout 3 mosquitto_sub -v -h localhost -t "openWB/#" > /var/www/html/openWB/ramdisk/mqttrenew
while read line; do
	if [[ $line == *"openWB"* ]];then
		value=$(echo -e $line | awk '{print $2;}')
		name=$(echo -e $line | awk '{print $1;}')
		mosquitto_pub -r -t $name -m $value
	fi
done < /var/www/html/openWB/ramdisk/mqttrenew
