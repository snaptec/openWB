#!/bin/bash

mosquitto_pub -t openWB/system/1alllivevalues -r -m "$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"0" | head -n "$((50 - 0))")" &
all2livevalues=$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"100" | head -n "$((100 - 50))")
all3livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"150" | head -n "$((150 - 100))")"
all4livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"200" | head -n "$((200 - 150))")"
all5livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"250" | head -n "$((250 - 200))")"
all6livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"300" | head -n "$((300 - 250))")"
all7livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"350" | head -n "$((350 - 300))")"
all8livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"400" | head -n "$((400 - 350))")"
all9livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"450" | head -n "$((450 - 400))")"
all10livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"500" | head -n "$((500 - 450))")"
all11livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"550" | head -n "$((550 - 500))")"
all12livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"600" | head -n "$((600 - 550))")"
all13livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"650" | head -n "$((650 - 600))")"
all14livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"700" | head -n "$((700 - 650))")"
all15livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"750" | head -n "$((750 - 700))")"
all16livevalues="$(< /var/www/html/openWB/ramdisk/all-live.graph tail -n +"800" | head -n "$((800 - 750))")"
mosquitto_pub -t openWB/system/2alllivevalues -r -m "$([ ${#all2livevalues} -ge 10 ] && echo "$all2livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/3alllivevalues -r -m "$([ ${#all3livevalues} -ge 10 ] && echo "$all3livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/4alllivevalues -r -m "$([ ${#all4livevalues} -ge 10 ] && echo "$all4livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/5alllivevalues -r -m "$([ ${#all5livevalues} -ge 10 ] && echo "$all5livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/6alllivevalues -r -m "$([ ${#all6livevalues} -ge 10 ] && echo "$all6livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/7alllivevalues -r -m "$([ ${#all7livevalues} -ge 10 ] && echo "$all7livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/8alllivevalues -r -m "$([ ${#all8livevalues} -ge 10 ] && echo "$all8livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/9alllivevalues -r -m "$([ ${#all9livevalues} -ge 10 ] && echo "$all9livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/10alllivevalues -r -m "$([ ${#all10livevalues} -ge 10 ] && echo "$all10livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/11alllivevalues -r -m "$([ ${#all11livevalues} -ge 10 ] && echo "$all11livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/12alllivevalues -r -m "$([ ${#all12livevalues} -ge 10 ] && echo "$all12livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/13alllivevalues -r -m "$([ ${#all13livevalues} -ge 10 ] && echo "$all13livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/14alllivevalues -r -m "$([ ${#all14livevalues} -ge 10 ] && echo "$all14livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/15alllivevalues -r -m "$([ ${#all15livevalues} -ge 10 ] && echo "$all15livevalues" || echo "-")" &
mosquitto_pub -t openWB/system/16alllivevalues -r -m "$([ ${#all16livevalues} -ge 10 ] && echo "$all16livevalues" || echo "-")" &
(sleep 5 && mosquitto_pub -t openWB/set/graph/RequestLLiveGraph -r -m "0")& 
