#!/bin/bash
firstload=$(tail -n 100 /var/www/html/openWB/ramdisk/openWB.log)

mosquitto_pub -t openWB/system/debug/DebugInfo -m "$firstload" &

(sleep 1 && mosquitto_pub -t openWB/set/system/debug/RequestDebugInfo -r -m "0")& 
