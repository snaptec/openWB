#!/bin/bash

mosquitto_pub -t openWB/system/LiveGraphData1 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"0" | head -n "$((49 - 0))")" &
mosquitto_pub -t openWB/system/LiveGraphData2 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"50" | head -n "$((100 - 50))")" &
mosquitto_pub -t openWB/system/LiveGraphData3 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"100" | head -n "$((150 - 100))")" &
mosquitto_pub -t openWB/system/LiveGraphData4 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"150" | head -n "$((200 - 150))")" &
mosquitto_pub -t openWB/system/LiveGraphData5 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"200" | head -n "$((250 - 200))")" &
mosquitto_pub -t openWB/system/LiveGraphData6 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"250" | head -n "$((300 - 250))")" &
mosquitto_pub -t openWB/system/LiveGraphData7 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"300" | head -n "$((350 - 300))")" &
mosquitto_pub -t openWB/system/LiveGraphData8 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"350" | head -n "$((400 - 350))")" &
mosquitto_pub -t openWB/system/LiveGraphData9 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"400" | head -n "$((450 - 400))")" &

(sleep 5 && mosquitto_pub -t openWB/set/graph/RequestLLiveGraph -r -m "0")& 
