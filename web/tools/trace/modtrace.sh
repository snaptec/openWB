#!/bin/bash
input=$(echo $1) 
temp="${input#*ip=}"
ip="${temp%%&*}"
temp="${input#*start=}"
start="${temp%%&*}"
temp="${input#*len=}"
len="${temp%%&*}"
temp="${input#*fun=}"
fun="${temp%%&*}"
temp="${input#*id=}"
id="${temp%%&*}"
echo "<br/> parmeters parsed ip $ip ";
echo " start $start ";
echo " len $len ";
echo " id $id ";
echo " fun $fun <br/>";
sudo python /var/www/html/openWB/web/tools/trace/trace.py $ip $start $len $id $fun
