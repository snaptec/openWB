#!/bin/bash

mosquitto_pub -t openWB/system/DayGraphData1 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"0" | head -n "$((24 - 0))")" &
mosquitto_pub -t openWB/system/DayGraphData2 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"25" | head -n "$((50 - 25))")" &
mosquitto_pub -t openWB/system/DayGraphData3 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"50" | head -n "$((75 - 50))")" &
mosquitto_pub -t openWB/system/DayGraphData4 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"75" | head -n "$((100 - 75))")" &
mosquitto_pub -t openWB/system/DayGraphData5 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"100" | head -n "$((125 - 100))")" &
mosquitto_pub -t openWB/system/DayGraphData6 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"125" | head -n "$((150 - 125))")" &
mosquitto_pub -t openWB/system/DayGraphData7 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"150" | head -n "$((175 - 150))")" &
mosquitto_pub -t openWB/system/DayGraphData8 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"175" | head -n "$((200 - 175))")" &
mosquitto_pub -t openWB/system/DayGraphData9 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"200" | head -n "$((225 - 200))")" &
mosquitto_pub -t openWB/system/DayGraphData10 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"225" | head -n "$((250 - 225))")" &
mosquitto_pub -t openWB/system/DayGraphData11 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"250" | head -n "$((275 - 250))")" &
mosquitto_pub -t openWB/system/DayGraphData12 -r -m "$(</var/www/html/openWB/web/logging/data/daily/$1.csv tail -n +"275" | head -n "$((300 - 275))")" &

(sleep 3 && mosquitto_pub -t openWB/set/graph/RequestDayGraph -r -m "0")& 
