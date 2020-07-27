#!/bin/bash
token=$(</var/www/html/openWB/ramdisk/remotetoken)
IFS=';' read -r token port <<< "$token"
/var/www/html/openWB/runs/startremotesupport.sh $token $port &>/dev/null & disown;

