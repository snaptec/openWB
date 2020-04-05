#!/bin/bash
input=$1

if [[ "$input" > "201501" ]]; then
	if [[ "$input" == "201912" ]]; then
		oldmonth="202001"
	elif [[ "$input" == "201812" ]]; then
		oldmonth="201901"

	else
		month=${input: -2}
		month=$(( month + 1 ))
		if (( month < 10 )); then
			month=$(printf "0$month")
		fi
		year=$(echo $input |cut -c1-4)
		oldmonth=$(printf $year$month)
	fi

	mosquitto_pub -t openWB/system/MonthLadelogData1 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"0" | head -n "$((24 - 0))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData2 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"25" | head -n "$((50 - 25))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData3 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"50" | head -n "$((75 - 50))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData4 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"75" | head -n "$((100 - 75))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData5 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"100" | head -n "$((125 - 100))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData6 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"125" | head -n "$((150 - 125))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData7 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"150" | head -n "$((175 - 150))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData8 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"175" | head -n "$((200 - 175))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData9 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"200" | head -n "$((225 - 200))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData10 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"225" | head -n "$((250 - 225))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData11 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"250" | head -n "$((275 - 250))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData12 -r -m "$(</var/www/html/openWB/web/logging/data/ladelog/$1.csv tail -n +"275" | head -n "$((300 - 275))")" &
else
	mosquitto_pub -t openWB/system/MonthLadelogData1 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"0" | head -n "$((24 - 0))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData2 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"25" | head -n "$((50 - 25))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData3 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"50" | head -n "$((75 - 50))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData4 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"75" | head -n "$((100 - 75))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData5 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"100" | head -n "$((125 - 100))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData6 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"125" | head -n "$((150 - 125))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData7 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"150" | head -n "$((175 - 150))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData8 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"175" | head -n "$((200 - 175))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData9 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"200" | head -n "$((225 - 200))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData10 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"225" | head -n "$((250 - 225))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData11 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"250" | head -n "$((275 - 250))")" &
	mosquitto_pub -t openWB/system/MonthLadelogData12 -r -m "$(</var/www/html/openWB/web/ladelog tail -n +"275" | head -n "$((300 - 275))")" &
fi
(sleep 3 && mosquitto_pub -t openWB/set/graph/RequestMonthLadelog -r -m "0")& 
