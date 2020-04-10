#!/bin/bash

mosquitto_pub -t openWB/system/LiveGraphData1 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"0" | head -n "$((99 - 0))")" &
mosquitto_pub -t openWB/system/LiveGraphData2 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"100" | head -n "$((200 - 100))")" &
mosquitto_pub -t openWB/system/LiveGraphData3 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"200" | head -n "$((300 - 200))")" &
mosquitto_pub -t openWB/system/LiveGraphData4 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"300" | head -n "$((400 - 300))")" &
mosquitto_pub -t openWB/system/LiveGraphData5 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"400" | head -n "$((500 - 400))")" &
mosquitto_pub -t openWB/system/LiveGraphData6 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"500" | head -n "$((600 - 500))")" &
mosquitto_pub -t openWB/system/LiveGraphData7 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"600" | head -n "$((700 - 600))")" &
mosquitto_pub -t openWB/system/LiveGraphData8 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"700" | head -n "$((800 - 700))")" &
mosquitto_pub -t openWB/system/LiveGraphData9 -r -m "$(</var/www/html/openWB/ramdisk/all-live.graph tail -n +"800" | head -n "$((900 - 800))")" &

(sleep 5 && mosquitto_pub -t openWB/set/graph/RequestLLiveGraph -r -m "0")& 
