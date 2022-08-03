#!/bin/bash
# input ist Jahr JJJJ 2020
input=$1
nextyear=$(( input + 1 ))

echo ""  > /var/www/html/openWB/ramdisk/yearlydata
echo "" > /var/www/html/openWB/ramdisk/yearlydata00

if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}01.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"01.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}02.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"02.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}03.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"03.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}04.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"04.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}05.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"05.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}06.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"06.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}07.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"07.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}08.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"08.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}09.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"09.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}10.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"10.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}11.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"11.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi
if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}12.csv ]; then
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"12.csv")" >> /var/www/html/openWB/ramdisk/yearlydata
fi

grep . /var/www/html/openWB/ramdisk/yearlydata > /var/www/html/openWB/ramdisk/yearlydatas

if [ -s /var/www/html/openWB/web/logging/data/monthly/${nextyear}01.csv ]; then
    #new year found
    echo "$(head -n 1 /var/www/html/openWB/web/logging/data/monthly/$nextyear"01.csv")" > /var/www/html/openWB/ramdisk/yearlydata1
else
    if [ -s /var/www/html/openWB/web/logging/data/monthly/${input}12.csv ]; then
        #get the latest record 12
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"12.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}11.csv ]; then
        #get the latest record 11
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"11.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}10.csv ]; then
        #get the latest record 10
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"10.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}09.csv ]; then
        #get the latest record 09
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"09.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}08.csv ]; then
        #get the latest record 08
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"08.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}07.csv ]; then
        #get the latest record 07
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"07.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}06.csv ]; then
        #get the latest record 06
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"06.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}05.csv ]; then
        #get the latest record 05
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"05.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}04.csv ]; then
        #get the latest record 04
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"04.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}03.csv ]; then
        #get the latest record 03
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"03.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}02.csv ]; then
        #get the latest record 02
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"02.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    elif [ -s /var/www/html/openWB/web/logging/data/monthly/${input}01.csv ]; then
        #get the latest record 01
        echo "$(tail -n 1 /var/www/html/openWB/web/logging/data/monthly/$input"01.csv")" > /var/www/html/openWB/ramdisk/yearlydata00
    fi

    # copy this found record to the new year
    cut --complement -f 1 -d, /var/www/html/openWB/ramdisk/yearlydata00 > /var/www/html/openWB/ramdisk/yearlydata02 
    echo "${nextyear}0101" > /var/www/html/openWB/ramdisk/yearlydata01
    paste -d , /var/www/html/openWB/ramdisk/yearlydata01 /var/www/html/openWB/ramdisk/yearlydata02 > /var/www/html/openWB/ramdisk/yearlydata1
fi
grep . /var/www/html/openWB/ramdisk/yearlydata1 > /var/www/html/openWB/ramdisk/yearlydatas1

mosquitto_pub -t openWB/system/YearGraphData1 -r -f  /var/www/html/openWB/ramdisk/yearlydatas &
mosquitto_pub -t openWB/system/YearGraphData2 -r -f  /var/www/html/openWB/ramdisk/yearlydatas1 &
mosquitto_pub -t openWB/system/YearGraphData3 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphData4 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphData5 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphData6 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphData7 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphData8 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphData9 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphData10 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphData11 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphData12 -r -m  "0" &

(sleep 3 && mosquitto_pub -t openWB/set/graph/RequestYearGraph -r -m "0") &
