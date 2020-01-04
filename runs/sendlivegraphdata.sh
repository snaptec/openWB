#!/bin/bash

mosquitto_pub -t openWB/system/LiveGraphData -r -m "$(cat /var/www/html/openWB/ramdisk/all-live.graph | tail -n 80)" &
(sleep 3 && mosquitto_pub -t openWB/set/graph/RequestLiveGraph -r -m "0")& 
