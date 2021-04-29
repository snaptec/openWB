#!/bin/bash
input=$1
if [[ "$input" == "202012" ]]; then
	oldmonth="202101"
elif [[ "$input" == "201912" ]]; then
	oldmonth="202001"
elif [[ "$input" == "201812" ]]; then
	oldmonth="201901"

else
	month=${input: -2}
	month=$(( ${month#0} +1))
	if (( month < 10 )); then
		month=$(printf "0$month")
	fi
	year=$(echo $input |cut -c1-4)
	oldmonth=$(printf $year$month)
fi
firstload=$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$oldmonth.csv)

mosquitto_pub -t openWB/system/MonthGraphDatan1 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"0" | head -n "$((24 - 0))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan2 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"25" | head -n "$((50 - 25))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan3 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"50" | head -n "$((75 - 50))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan4 -r -m "$firstload" &
#mosquitto_pub -t openWB/system/MonthGraphData4 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"75" | head -n "$((100 - 75))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan5 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"100" | head -n "$((125 - 100))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan6 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"125" | head -n "$((150 - 125))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan7 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"150" | head -n "$((175 - 150))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan8 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"175" | head -n "$((200 - 175))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan9 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"200" | head -n "$((225 - 200))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan10 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"225" | head -n "$((250 - 225))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan11 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"250" | head -n "$((275 - 250))")" &
mosquitto_pub -t openWB/system/MonthGraphDatan12 -r -m "$(</var/www/html/openWB/web/logging/data/monthly/$1.csv tail -n +"275" | head -n "$((300 - 275))")" &

(sleep 3 && mosquitto_pub -t openWB/set/graph/RequestMonthGraphv1 -r -m "0")&
