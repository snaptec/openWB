#!/bin/bash
sudo python /var/www/html/openWB/modules/phoenixlllp1/phoenix.py $phoenixlp1ip
#EVStatus
EVStatus=$(</var/www/html/openWB/ramdisk/phoenixlp1rEVStatus)
#A=nicht angeschlossen, B=angeschlossen EVSE nicht bereit,C|D= angeschlossen ladebereit, E=angeschlossen laden nicht möglich, F=angeschlossen laden nicht möglich
if [ $EVStatus == 'A' ] ; then
EVStatus=0
else EVStatus=1
fi
echo $EVStatus > /var/www/html/openWB/ramdisk/plugstat
EVSEnable=$(</var/www/html/openWB/ramdisk/phoenixlp1rEnableSet)
echo $EVSEnable > /var/www/html/openWB/ramdisk/chargestat
#pwm
pwm=$(</var/www/html/openWB/ramdisk/phoenixlp1rPWM)
ladeleistung=$(</var/www/html/openWB/ramdisk/phoenixlp1ractPower)
#watt=$(echo "($watt / 1000)/1" |bc)
#ladeleistung=$(echo "scale=2;$ladeleistung * 1000" |bc)
if [ $ladeleistung == -1 ]
then
if [ $EVStatusfull == 0 ] || [ $EVSEnable == 0 ] ; then
ladeleistung=0
lla1=0
lla2=0
lla3=0
llu1=0
llu2=0
llu3=0
else
ladeleistung=$(echo "($pwm * 230)" |bc)
lla1=pwm
lla2=pwm
lla3=pwm
llu1=230
llu2=230
llu3=230
fi
else
lla1=$(</var/www/html/openWB/ramdisk/phoenixlp1rA1)
lla2=$(</var/www/html/openWB/ramdisk/phoenixlp1rA2)
lla3=$(</var/www/html/openWB/ramdisk/phoenixlp1rA3)
lla1=$(</var/www/html/openWB/ramdisk/phoenixlp1rV1)
lla2=$(</var/www/html/openWB/ramdisk/phoenixlp1rV2)
lla3=$(</var/www/html/openWB/ramdisk/phoenixlp1rV3)
fi
echo $ladeleistung > /var/www/html/openWB/ramdisk/llaktuell
echo $llv1 > /var/www/html/openWB/ramdisk/lla1
echo $llv2 > /var/www/html/openWB/ramdisk/lla2
echo $llv3 > /var/www/html/openWB/ramdisk/lla3
echo $llv1 > /var/www/html/openWB/ramdisk/llv1
echo $llv2 > /var/www/html/openWB/ramdisk/llv2
echo $llv3 > /var/www/html/openWB/ramdisk/llv3
