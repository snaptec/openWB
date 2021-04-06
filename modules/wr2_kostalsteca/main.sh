#!/bin/bash
#
# RainerW 8th of April 2020
# Unfortunately Kostal has introduced the third version of interface: XML
# This script is for Kostal_Piko_MP_plus and StecaGrid coolcept (single phase inverter)
# In fact Kostal is not developing own single phase inverter anymore but is sourcing them from Steca
# If you have the chance to test this module for the latest three phase inverter from Kostal (Plenticore) or Steca (coolcept3 or coolcept XL) let us know if it works
# DetMoerk 20210323: Anpassung fuer ein- und dreiphasige WR der Serie. Anstatt eine feste Zeile aus dem Ergebnis zu schneiden wird nach der Zeile mit AC_Power gesucht.
DMOD="MAIN" 


# call for XML file and parse it for current PV power
power_kostal_piko_MP=$(curl --connect-timeout 5 -s $pv2ip/measurements.xml |grep -e "Type=\"AC_Power\""| grep -Po "Value=\"\K[^\"]*" )

# cut the comma and the digit behind the comma
power_kostal_piko_MP=$(echo $power_kostal_piko_MP | sed 's/\..*$//')

# allow only numbers
re='^-?[0-9]+$'
if ! [[ $power_kostal_piko_MP =~ $re ]] ; then
	power_kostal_piko_MP="0"
fi
openwbDebugLog ${DMOD} 2 "PVWatt: $power_kostal_piko_MP"

# call for XML file and parse it for total produced kwh
#pvkwh_kostal_piko_MP=$(curl --connect-timeout 5 -s $pv2ip/yields.xml | grep -Po "Value=\"\K[^\"]*" | sed -n 1p)
pvkwh_kostal_piko_MP=$(curl --connect-timeout 5 -s $pv2ip/yields.xml |grep "YieldValue" | grep -Po "Value=\"\K[^\"]*" )
if ! [[ $pvkwh_kostal_piko_MP =~ $re ]] ; then
	openwbDebugLog ${DMOD} 2 "PVkWh: NaN get prev. Value"
	pvkwh_kostal_piko_MP=$(</var/www/html/openWB/ramdisk/pv2kwh)
fi

openwbDebugLog ${DMOD} 2 "PVkWh: $pvkwh_kostal_piko_MP"

## Daten in Ramdisk schreiben

echo $pvkwh_kostal_piko_MP > /var/www/html/openWB/ramdisk/pv2kwh
echo '-'$power_kostal_piko_MP > /var/www/html/openWB/ramdisk/pv2watt
echo '-'$power_kostal_piko_MP
