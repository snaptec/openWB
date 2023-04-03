#!/bin/bash
input=$(echo $1) 
temp="${input#*ip=}"
ip="${temp%%&*}"
temp="${input#*port=}"
port="${temp%%&*}"
temp="${input#*id=}"
id="${temp%%&*}"
temp="${input#*start=}"
start="${temp%%&*}"
temp="${input#*len=}"
len="${temp%%&*}"
temp="${input#*data_type=}"
data_type="${temp%%&*}"
temp="${input#*func=}"
func="${temp%%&*}"
echo "<br/> parmeters parsed IP $ip ";
echo " Port $port ";
echo " ID $id ";
echo " Address $start ";
echo " Len $len ";
echo " DataType $data_type ";
echo " Function $func <br/>";
sudo python3 /var/www/html/openWB/packages/modbus_test.py $ip $port $id $start $len $data_type $func
