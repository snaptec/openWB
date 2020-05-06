#!/bin/bash
(sleep 600; sudo kill $(ps aux |grep '[a]treboot.sh' | awk '{print $2}'); echo 0 > /var/www/html/openWB/ramdisk/bootinprogress) &
#Ramdisk mit initialen Werten befüllen nach neustart
. /var/www/html/openWB/openwb.conf
sleep 5
sudo chown -R www-data:www-data /var/www/html/openWB/web/backup
sudo chown -R www-data:www-data /var/www/html/openWB/web/tools/upload
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod 777 /var/www/html/openWB/smarthome.ini
sudo chmod 777 /var/www/html/openWB/ramdisk
sudo chmod 777 /var/www/html/openWB/ramdisk/
sudo chmod 777 /var/www/html/openWB/web/files/*
sudo chmod -R +x /var/www/html/openWB/modules/*
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3s1
echo 1 > /var/www/html/openWB/ramdisk/bootinprogress
echo 0 > /var/www/html/openWB/ramdisk/nurpv70dynstatus
echo 0 > /var/www/html/openWB/ramdisk/lp1phasen
echo 0 > /var/www/html/openWB/ramdisk/lp2phasen
echo 0 > /var/www/html/openWB/ramdisk/lp3phasen
echo 0 > /var/www/html/openWB/ramdisk/lp4phasen
echo 0 > /var/www/html/openWB/ramdisk/lp5phasen
echo 0 > /var/www/html/openWB/ramdisk/lp6phasen
echo 0 > /var/www/html/openWB/ramdisk/lp7phasen
echo 0 > /var/www/html/openWB/ramdisk/lp8phasen
echo 0 > /var/www/html/openWB/ramdisk/rfidlist
echo 0 > /var/www/html/openWB/ramdisk/AllowedTotalCurrentPerPhase
echo 0 > /var/www/html/openWB/ramdisk/ChargingVehiclesOnL1
echo 0 > /var/www/html/openWB/ramdisk/ChargingVehiclesOnL2
echo 0 > /var/www/html/openWB/ramdisk/ChargingVehiclesOnL3
echo 0 > /var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL1
echo 0 > /var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL2
echo 0 > /var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL3
echo 0 > /var/www/html/openWB/ramdisk/autolocktimer
echo 0 > /var/www/html/openWB/ramdisk/ipaddress
echo 0 > /var/www/html/openWB/ramdisk/awattarprice
echo 1 > /var/www/html/openWB/ramdisk/mqttawattarprice
echo 0 > /var/www/html/openWB/ramdisk/awattarmaxprice
echo 1 > /var/www/html/openWB/ramdisk/mqttawattarmaxprice
echo 1 > /var/www/html/openWB/ramdisk/mqtt.log
echo 1 > /var/www/html/openWB/ramdisk/mqttsoc1
echo 1 > /var/www/html/openWB/ramdisk/lp1enabled
echo 0 > /var/www/html/openWB/ramdisk/device1_wh
echo 0 > /var/www/html/openWB/ramdisk/device2_wh
echo 0 > /var/www/html/openWB/ramdisk/device3_wh
echo 0 > /var/www/html/openWB/ramdisk/device4_wh
echo 0 > /var/www/html/openWB/ramdisk/device5_wh
echo 0 > /var/www/html/openWB/ramdisk/device6_wh
echo 0 > /var/www/html/openWB/ramdisk/device7_wh
echo 0 > /var/www/html/openWB/ramdisk/device8_wh
echo 0 > /var/www/html/openWB/ramdisk/device9_wh
echo 0 > /var/www/html/openWB/ramdisk/device10_wh
echo 0 > /var/www/html/openWB/ramdisk/device1_temp0
echo 0 > /var/www/html/openWB/ramdisk/device1_temp1
echo 0 > /var/www/html/openWB/ramdisk/device1_temp2
echo 0 > /var/www/html/openWB/ramdisk/device2_temp0
echo 0 > /var/www/html/openWB/ramdisk/device2_temp1
echo 0 > /var/www/html/openWB/ramdisk/device2_temp2
echo 1 > /var/www/html/openWB/ramdisk/lp2enabled
echo 1 > /var/www/html/openWB/ramdisk/lp3enabled
echo 1 > /var/www/html/openWB/ramdisk/lp4enabled
echo 1 > /var/www/html/openWB/ramdisk/lp5enabled
echo 1 > /var/www/html/openWB/ramdisk/lp6enabled
echo 1 > /var/www/html/openWB/ramdisk/lp7enabled
echo 1 > /var/www/html/openWB/ramdisk/lp8enabled
echo 0 > /var/www/html/openWB/ramdisk/schieflast
echo 0 > /var/www/html/openWB/ramdisk/renewmqtt
echo 0 > /var/www/html/openWB/ramdisk/netzschutz
echo 0 > /var/www/html/openWB/ramdisk/hausverbrauch
echo 0 > /var/www/html/openWB/ramdisk/blockall
echo 0 > /var/www/html/openWB/ramdisk/llsoll
echo 0 > /var/www/html/openWB/ramdisk/llsolllp4
echo 0 > /var/www/html/openWB/ramdisk/llsolllp5
echo 0 > /var/www/html/openWB/ramdisk/llsolllp6
echo 0 > /var/www/html/openWB/ramdisk/llsolllp7
echo 0 > /var/www/html/openWB/ramdisk/llsolllp8
echo 0 > /var/www/html/openWB/ramdisk/ladungaktivlp1
echo 0 > /var/www/html/openWB/ramdisk/ladungaktivlp2
echo 0 > /var/www/html/openWB/ramdisk/ladungaktivlp3
echo 0 > /var/www/html/openWB/ramdisk/plugstat
echo 0 > /var/www/html/openWB/ramdisk/plugstats1
echo 0 > /var/www/html/openWB/ramdisk/plugstats2
echo 0 > /var/www/html/openWB/ramdisk/chargestat
echo 0 > /var/www/html/openWB/ramdisk/chargestats1
echo 0 > /var/www/html/openWB/ramdisk/chargestats2
echo 0 > /var/www/html/openWB/ramdisk/plugstats2
echo 0 > /var/www/html/openWB/ramdisk/chargestatlp3
echo 0 > /var/www/html/openWB/ramdisk/plugstatlp3
echo 0 > /var/www/html/openWB/ramdisk/plugstatlp4
echo 0 > /var/www/html/openWB/ramdisk/plugstatlp5
echo 0 > /var/www/html/openWB/ramdisk/plugstatlp6
echo 0 > /var/www/html/openWB/ramdisk/plugstatlp7
echo 0 > /var/www/html/openWB/ramdisk/plugstatlp8
echo 0 > /var/www/html/openWB/ramdisk/chargestatlp4
echo 0 > /var/www/html/openWB/ramdisk/chargestatlp5
echo 0 > /var/www/html/openWB/ramdisk/chargestatlp6
echo 0 > /var/www/html/openWB/ramdisk/chargestatlp7
echo 0 > /var/www/html/openWB/ramdisk/chargestatlp8
echo 0 > /var/www/html/openWB/ramdisk/verbraucher1_watt
echo 0 > /var/www/html/openWB/ramdisk/verbraucher1_wh
echo 0 > /var/www/html/openWB/ramdisk/verbraucher2_watt
echo 0 > /var/www/html/openWB/ramdisk/verbraucher2_wh
echo 0 > /var/www/html/openWB/ramdisk/verbraucher2_whe
echo 0 > /var/www/html/openWB/ramdisk/verbraucher3_watt
echo 0 > /var/www/html/openWB/ramdisk/verbraucher3_wh
echo 0 > /var/www/html/openWB/ramdisk/verbraucher1_whe
echo 0 > /var/www/html/openWB/ramdisk/verbraucher1vorhanden
echo 0 > /var/www/html/openWB/ramdisk/verbraucher2vorhanden
echo 0 > /var/www/html/openWB/ramdisk/verbraucher3vorhanden
echo 0 > /var/www/html/openWB/ramdisk/evseausgelesen
echo 0 > /var/www/html/openWB/ramdisk/progevsedinlp1
echo 0 > /var/www/html/openWB/ramdisk/progevsedinlp2
echo 0 > /var/www/html/openWB/ramdisk/progevsedinlp12000
echo 0 > /var/www/html/openWB/ramdisk/progevsedinlp12007
echo 0 > /var/www/html/openWB/ramdisk/progevsedinlp22000
echo 0 > /var/www/html/openWB/ramdisk/progevsedinlp22007
echo 0 > /var/www/html/openWB/ramdisk/readtag
echo 0 > /var/www/html/openWB/ramdisk/rfidlp1
echo 0 > /var/www/html/openWB/ramdisk/mqttrfidlp1
echo 0 > /var/www/html/openWB/ramdisk/rfidlp2
echo 0 > /var/www/html/openWB/ramdisk/mqttrfidlp2
echo 0 > /var/www/html/openWB/ramdisk/rfidlasttag
echo 0 > /var/www/html/openWB/ramdisk/mqttrfidlasttag
echo 1 > /var/www/html/openWB/ramdisk/reloaddisplay
echo 0 > /var/www/html/openWB/ramdisk/ledstatus
echo 1 > /var/www/html/openWB/ramdisk/execdisplay
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungaktlp1
echo 0 > /var/www/html/openWB/ramdisk/pluggedladunglp1startkwh
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungbishergeladen
echo 0 > /var/www/html/openWB/ramdisk/pluggedtimer1
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungaktlp2
echo 0 > /var/www/html/openWB/ramdisk/pluggedladunglp2startkwh
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungbishergeladenlp2
echo 0 > /var/www/html/openWB/ramdisk/pluggedtimer2
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungbishergeladenlp3
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungbishergeladenlp4
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungbishergeladenlp5
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungbishergeladenlp6
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungbishergeladenlp7
echo 0 > /var/www/html/openWB/ramdisk/pluggedladungbishergeladenlp8
echo 1 > /var/www/html/openWB/ramdisk/mqttlademkwhs1
echo 1 > /var/www/html/openWB/ramdisk/mqttlademkwhs2
echo 0 > /var/www/html/openWB/ramdisk/mqttlastladestatus
echo 0 > /var/www/html/openWB/ramdisk/mqttlastplugstat
echo 0 > /var/www/html/openWB/ramdisk/mqttlastchargestat
echo 0 > /var/www/html/openWB/ramdisk/mqttlastchargestats1
echo 0 > /var/www/html/openWB/ramdisk/mqttlastplugstats1
echo 0 > /var/www/html/openWB/ramdisk/mqttspeichervorhanden
echo 3 > /var/www/html/openWB/ramdisk/mqttspeichersoc
echo 2 > /var/www/html/openWB/ramdisk/mqttspeicherleistung
echo 0 > /var/www/html/openWB/ramdisk/mqttladeleistungs1
echo 0 > /var/www/html/openWB/ramdisk/mqttladeleistungs2
echo 0 > /var/www/html/openWB/ramdisk/mqttladeleistunglp1
echo 0 > /var/www/html/openWB/ramdisk/autolockstatuslp1
echo 0 > /var/www/html/openWB/ramdisk/autolockstatuslp2
echo 0 > /var/www/html/openWB/ramdisk/autolockstatuslp3
echo 0 > /var/www/html/openWB/ramdisk/autolockstatuslp4
echo 0 > /var/www/html/openWB/ramdisk/autolockstatuslp5
echo 0 > /var/www/html/openWB/ramdisk/autolockstatuslp6
echo 0 > /var/www/html/openWB/ramdisk/autolockstatuslp7
echo 0 > /var/www/html/openWB/ramdisk/autolockstatuslp8
echo 0 > /var/www/html/openWB/ramdisk/autolockconfiguredlp1
echo 0 > /var/www/html/openWB/ramdisk/autolockconfiguredlp2
echo 0 > /var/www/html/openWB/ramdisk/autolockconfiguredlp3
echo 0 > /var/www/html/openWB/ramdisk/autolockconfiguredlp4
echo 0 > /var/www/html/openWB/ramdisk/autolockconfiguredlp5
echo 0 > /var/www/html/openWB/ramdisk/autolockconfiguredlp6
echo 0 > /var/www/html/openWB/ramdisk/autolockconfiguredlp7
echo 0 > /var/www/html/openWB/ramdisk/autolockconfiguredlp8
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockstatuslp1
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockstatuslp2
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockstatuslp3
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockstatuslp4
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockstatuslp5
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockstatuslp6
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockstatuslp7
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockstatuslp8
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockconfiguredlp1
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockconfiguredlp2
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockconfiguredlp3
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockconfiguredlp4
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockconfiguredlp5
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockconfiguredlp6
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockconfiguredlp7
echo 1 > /var/www/html/openWB/ramdisk/mqttautolockconfiguredlp8
echo 0 > /var/www/html/openWB/ramdisk/smarthome_device_manual_1
echo 0 > /var/www/html/openWB/ramdisk/smarthome_device_manual_2
echo 0 > /var/www/html/openWB/ramdisk/smarthome_device_manual_3
echo 0 > /var/www/html/openWB/ramdisk/smarthome_device_manual_4
echo 0 > /var/www/html/openWB/ramdisk/smarthome_device_manual_5
echo 0 > /var/www/html/openWB/ramdisk/smarthome_device_manual_6
echo 0 > /var/www/html/openWB/ramdisk/smarthome_device_manual_7
echo 0 > /var/www/html/openWB/ramdisk/smarthome_device_manual_8
echo 0 > /var/www/html/openWB/ramdisk/smarthome_device_manual_9
touch /var/www/html/openWB/ramdisk/wattbezug
echo 10 > /var/www/html/openWB/ramdisk/lp1sofortll
echo 10 > /var/www/html/openWB/ramdisk/lp2sofortll
echo 10 > /var/www/html/openWB/ramdisk/lp3sofortll
echo 10 > /var/www/html/openWB/ramdisk/lp4sofortll
echo 10 > /var/www/html/openWB/ramdisk/lp5sofortll
echo 10 > /var/www/html/openWB/ramdisk/lp6sofortll
echo 10 > /var/www/html/openWB/ramdisk/lp7sofortll
echo 10 > /var/www/html/openWB/ramdisk/lp8sofortll
echo 0 > /var/www/html/openWB/ramdisk/wattbezug
echo 0 > /var/www/html/openWB/ramdisk/hook1akt
echo 0 > /var/www/html/openWB/ramdisk/hook2akt
echo 0 > /var/www/html/openWB/ramdisk/hook3akt
echo 0 > /var/www/html/openWB/ramdisk/urcounter
echo 0 > /var/www/html/openWB/ramdisk/uhcounter
echo 1 > /var/www/html/openWB/ramdisk/mqttllsolls1
echo 1 > /var/www/html/openWB/ramdisk/mqttllsolls2
echo 0 > /var/www/html/openWB/ramdisk/lla1lp4
echo 0 > /var/www/html/openWB/ramdisk/lla2lp4
echo 0 > /var/www/html/openWB/ramdisk/lla3lp4
echo 0 > /var/www/html/openWB/ramdisk/llv1lp4
echo 0 > /var/www/html/openWB/ramdisk/llv2lp4
echo 0 > /var/www/html/openWB/ramdisk/llv3lp4
echo 0 > /var/www/html/openWB/ramdisk/ladeleistunglp4
echo 0 > /var/www/html/openWB/ramdisk/llkwhlp4
echo 0 > /var/www/html/openWB/ramdisk/lla1lp5
echo 0 > /var/www/html/openWB/ramdisk/lla2lp5
echo 0 > /var/www/html/openWB/ramdisk/lla3lp5
echo 0 > /var/www/html/openWB/ramdisk/llv1lp5
echo 0 > /var/www/html/openWB/ramdisk/llv2lp5
echo 0 > /var/www/html/openWB/ramdisk/llv3lp5
echo 0 > /var/www/html/openWB/ramdisk/ladeleistunglp5
echo 0 > /var/www/html/openWB/ramdisk/llkwhlp5
echo 0 > /var/www/html/openWB/ramdisk/lla1lp6
echo 0 > /var/www/html/openWB/ramdisk/lla2lp6
echo 0 > /var/www/html/openWB/ramdisk/lla3lp6
echo 0 > /var/www/html/openWB/ramdisk/llv1lp6
echo 0 > /var/www/html/openWB/ramdisk/llv2lp6
echo 0 > /var/www/html/openWB/ramdisk/llv3lp6
echo 0 > /var/www/html/openWB/ramdisk/ladeleistunglp6
echo 0 > /var/www/html/openWB/ramdisk/llkwhlp6
echo 0 > /var/www/html/openWB/ramdisk/lla1lp7
echo 0 > /var/www/html/openWB/ramdisk/lla2lp7
echo 0 > /var/www/html/openWB/ramdisk/lla3lp7
echo 0 > /var/www/html/openWB/ramdisk/llv1lp7
echo 0 > /var/www/html/openWB/ramdisk/llv2lp7
echo 0 > /var/www/html/openWB/ramdisk/llv3lp7
echo 0 > /var/www/html/openWB/ramdisk/ladeleistunglp7
echo 0 > /var/www/html/openWB/ramdisk/llkwhlp7
echo 0 > /var/www/html/openWB/ramdisk/lla1lp8
echo 0 > /var/www/html/openWB/ramdisk/lla2lp8
echo 0 > /var/www/html/openWB/ramdisk/lla3lp8
echo 0 > /var/www/html/openWB/ramdisk/llv1lp8
echo 0 > /var/www/html/openWB/ramdisk/llv2lp8
echo 0 > /var/www/html/openWB/ramdisk/llv3lp8
echo 0 > /var/www/html/openWB/ramdisk/ladeleistunglp8
echo 0 > /var/www/html/openWB/ramdisk/llkwhlp8
echo 0 > /var/www/html/openWB/ramdisk/ladestatuslp4
echo 0 > /var/www/html/openWB/ramdisk/ladestatuslp5
echo 0 > /var/www/html/openWB/ramdisk/ladestatuslp6
echo 0 > /var/www/html/openWB/ramdisk/ladestatuslp7
echo 0 > /var/www/html/openWB/ramdisk/ladestatuslp8
touch /var/www/html/openWB/ramdisk/ladestatus
touch /var/www/html/openWB/ramdisk/lademodus
touch /var/www/html/openWB/ramdisk/llaktuell
touch /var/www/html/openWB/ramdisk/llaktuells1
echo 0 > /var/www/html/openWB/ramdisk/boolstopchargeafterdisclp1
echo 0 > /var/www/html/openWB/ramdisk/boolstopchargeafterdisclp2
echo 0 > /var/www/html/openWB/ramdisk/boolstopchargeafterdisclp3
echo 0 > /var/www/html/openWB/ramdisk/boolstopchargeafterdisclp4
echo 0 > /var/www/html/openWB/ramdisk/boolstopchargeafterdisclp5
echo 0 > /var/www/html/openWB/ramdisk/boolstopchargeafterdisclp6
echo 0 > /var/www/html/openWB/ramdisk/boolstopchargeafterdisclp7
echo 0 > /var/www/html/openWB/ramdisk/boolstopchargeafterdisclp8

echo 0 > /var/www/html/openWB/ramdisk/pv2watt

echo 0 > /var/www/html/openWB/ramdisk/pv2kwh
echo 0 > /var/www/html/openWB/ramdisk/pv2a1
echo 0 > /var/www/html/openWB/ramdisk/pv2a2
echo 0 > /var/www/html/openWB/ramdisk/pv2a3



# Gesamtleistung AC PV-Module WR 1 + 2
touch /var/www/html/openWB/ramdisk/pvwatt
echo 0 > /var/www/html/openWB/ramdisk/pvwatt
# Leistung AC PV-Module WR 1
touch /var/www/html/openWB/ramdisk/pvwatt1
echo 0 > /var/www/html/openWB/ramdisk/pvwatt1
# Leistung AC PV-Module WR 2
touch /var/www/html/openWB/ramdisk/pvwatt2
echo 0 > /var/www/html/openWB/ramdisk/pvwatt2
# Gesamtertrag in Wattstunden WR 1 + 2
touch /var/www/html/openWB/ramdisk/pvkwh
echo 0 > /var/www/html/openWB/ramdisk/pvkwh
# Gesamtertrag in Kilowattstunden WR 1 + 2
touch /var/www/html/openWB/ramdisk/pvkwhk
echo 0 > /var/www/html/openWB/ramdisk/pvkwhk
# Tagesertrag in Kilowattstunden WR 1 + 2
touch /var/www/html/openWB/ramdisk/daily_pvkwhk
echo 0 > /var/www/html/openWB/ramdisk/daily_pvkwhk
# Monatsertrag in Kilowattstunden WR 1 + 2
touch /var/www/html/openWB/ramdisk/monthly_pvkwhk
echo 0 > /var/www/html/openWB/ramdisk/monthly_pvkwhk
# Jahresertrag in Kilowattstunden WR 1 + 2
touch /var/www/html/openWB/ramdisk/yearly_pvkwhk
echo 0 > /var/www/html/openWB/ramdisk/yearly_pvkwhk
# Gesamtertrag in Kilowattstunden WR 1
touch /var/www/html/openWB/ramdisk/pvkwhk1
echo 0 > /var/www/html/openWB/ramdisk/pvkwhk1
# Tagesertrag in Kilowattstunden WR 1
touch /var/www/html/openWB/ramdisk/daily_pvkwhk1
echo 0 > /var/www/html/openWB/ramdisk/daily_pvkwhk1
# Monatsertrag in Kilowattstunden WR 1
touch /var/www/html/openWB/ramdisk/monthly_pvkwhk1
echo 0 > /var/www/html/openWB/ramdisk/monthly_pvkwhk1
# Jahresertrag in Kilowattstunden WR 1
touch /var/www/html/openWB/ramdisk/yearly_pvkwhk1
echo 0 > /var/www/html/openWB/ramdisk/yearly_pvkwhk1
# Gesamtertrag in Kilowattstunden WR 2
touch /var/www/html/openWB/ramdisk/pvkwhk2
echo 0 > /var/www/html/openWB/ramdisk/pvkwhk2
# Tagesertrag in Kilowattstunden WR 2
touch /var/www/html/openWB/ramdisk/daily_pvkwhk2
echo 0 > /var/www/html/openWB/ramdisk/daily_pvkwhk2
# Monatsertrag in Kilowattstunden WR 2
touch /var/www/html/openWB/ramdisk/monthly_pvkwhk2
echo 0 > /var/www/html/openWB/ramdisk/monthly_pvkwhk2
# Jahresertrag in Kilowattstunden WR 2
touch /var/www/html/openWB/ramdisk/yearly_pvkwhk2
echo 0 > /var/www/html/openWB/ramdisk/yearly_pvkwhk2
# SoC Speicher am WR 1
touch /var/www/html/openWB/ramdisk/speichersoc
echo 4 > /var/www/html/openWB/ramdisk/speichersoc
# SoC Speicher am WR 2
touch /var/www/html/openWB/ramdisk/speichersoc2
echo 0 > /var/www/html/openWB/ramdisk/speichersoc2
# Gesamtleistung AC Speicher WR 1 + 2
touch /var/www/html/openWB/ramdisk/speicherleistung
echo 0 > /var/www/html/openWB/ramdisk/speicherleistung
# Leistung AC Speicher WR 1
touch /var/www/html/openWB/ramdisk/speicherleistung1
echo 0 > /var/www/html/openWB/ramdisk/speicherleistung1
# Leistung AC Speicher WR 2
touch /var/www/html/openWB/ramdisk/speicherleistung2
echo 0 > /var/www/html/openWB/ramdisk/speicherleistung2

touch /var/www/html/openWB/ramdisk/soc
touch /var/www/html/openWB/ramdisk/soc1
touch /var/www/html/openWB/ramdisk/lla1
touch /var/www/html/openWB/ramdisk/lla2
touch /var/www/html/openWB/ramdisk/lla3
touch /var/www/html/openWB/ramdisk/llkombiniert
touch /var/www/html/openWB/ramdisk/llas11
touch /var/www/html/openWB/ramdisk/llas12
touch /var/www/html/openWB/ramdisk/llas13
touch /var/www/html/openWB/ramdisk/llas21
touch /var/www/html/openWB/ramdisk/llas22
touch /var/www/html/openWB/ramdisk/llas23
echo 0 > /var/www/html/openWB/ramdisk/llas21
echo 0 > /var/www/html/openWB/ramdisk/llas22
echo 0 > /var/www/html/openWB/ramdisk/llas23
touch /var/www/html/openWB/ramdisk/llkwh
touch /var/www/html/openWB/ramdisk/llkwhs1
touch /var/www/html/openWB/ramdisk/einspeisungkwh
touch /var/www/html/openWB/ramdisk/bezugkwh
touch /var/www/html/openWB/ramdisk/llkwhs2
touch /var/www/html/openWB/ramdisk/speicher
touch /var/www/html/openWB/ramdisk/nachtladenstate
touch /var/www/html/openWB/ramdisk/nachtladenstates1
touch /var/www/html/openWB/ramdisk/zielladenkorrektura
touch /var/www/html/openWB/ramdisk/ladestatus.log

# temporäre Zwischenspeicher für z. B. Kostal Plenticore, da
# bei Anschluss von Speicher und Energiemanager direkt am WR
# alle Werte im Modul des Wechselrichters aus den Registern
# gelesen werden, um einen zeitlich zusammenhängenden Datensatz
# zu bekommen. Im jeweiligen Modul Speicher/Bezug werden
# die Werte dann in die ramdisk für die weitere globale
# Verarbeitung geschrieben.
# Bezug/Einspeisung
touch /var/www/html/openWB/ramdisk/temp_wattbezug
echo 0 > /var/www/html/openWB/ramdisk/temp_wattbezug
# Gesamte AC-Leistung des Speichers am WR 1 + 2
touch /var/www/html/openWB/ramdisk/temp_speicherleistung
echo 0 > /var/www/html/openWB/ramdisk/temp_peicherleistung
# AC-Leistung des Speichers am WR 1
touch /var/www/html/openWB/ramdisk/temp_speicherleistung1
echo 0 > /var/www/html/openWB/ramdisk/temp_peicherleistung1
# AC-Leistung des Speichers am WR 2
touch /var/www/html/openWB/ramdisk/temp_speicherleistung2
echo 0 > /var/www/html/openWB/ramdisk/temp_peicherleistung2
# SoC des Speichers am WR 1
touch /var/www/html/openWB/ramdisk/temp_speichersoc
echo 0 > /var/www/html/openWB/ramdisk/temp_speichersoc
# Strom auf den jeweiligen Phasen
touch /var/www/html/openWB/ramdisk/temp_bezuga1
echo 0 > /var/www/html/openWB/ramdisk/temp_bezuga1
touch /var/www/html/openWB/ramdisk/temp_bezuga2
echo 0 > /var/www/html/openWB/ramdisk/temp_bezuga2
touch /var/www/html/openWB/ramdisk/temp_bezuga3
echo 0 > /var/www/html/openWB/ramdisk/temp_bezuga3
# Netzfrequenz
touch /var/www/html/openWB/ramdisk/temp_evuhz
echo 0 > /var/www/html/openWB/ramdisk/temp_evuhz
# Leistung auf den jeweiligen Phasen
touch /var/www/html/openWB/ramdisk/temp_bezugw1
echo 0 > /var/www/html/openWB/ramdisk/temp_bezugw1
touch /var/www/html/openWB/ramdisk/temp_bezugw2
echo 0 > /var/www/html/openWB/ramdisk/temp_bezugw2
touch /var/www/html/openWB/ramdisk/temp_bezugw3
echo 0 > /var/www/html/openWB/ramdisk/temp_bezugw3
# Spannung auf den jeweiligen Phasen
touch /var/www/html/openWB/ramdisk/temp_evuv1
echo 0 > /var/www/html/openWB/ramdisk/temp_evuv1
touch /var/www/html/openWB/ramdisk/temp_evuv2
echo 0 > /var/www/html/openWB/ramdisk/temp_evuv2
touch /var/www/html/openWB/ramdisk/temp_evuv3
echo 0 > /var/www/html/openWB/ramdisk/temp_evuv3
# Wirkfaktor, wird aus historischen Gründen je Phase geschrieben
touch /var/www/html/openWB/ramdisk/temp_evupf1
echo 0 > /var/www/html/openWB/ramdisk/temp_evupf1
touch /var/www/html/openWB/ramdisk/temp_evupf2
echo 0 > /var/www/html/openWB/ramdisk/temp_evupf2
touch /var/www/html/openWB/ramdisk/temp_evupf3
echo 0 > /var/www/html/openWB/ramdisk/temp_evupf3

echo 0 > /var/www/html/openWB/ramdisk/zielladenkorrektura
echo 0 > /var/www/html/openWB/ramdisk/nachtladenstate
echo 0 > /var/www/html/openWB/ramdisk/nachtladen2state
echo 0 > /var/www/html/openWB/ramdisk/nachtladen2states1
echo 0 > /var/www/html/openWB/ramdisk/nachtladenstates1
echo 4 > /var/www/html/openWB/ramdisk/graphtimer

echo 0 > /var/www/html/openWB/ramdisk/speicher
echo 0 > /var/www/html/openWB/ramdisk/ladestatus
echo 0 > /var/www/html/openWB/ramdisk/ladestatuss1
echo 0 > /var/www/html/openWB/ramdisk/ladestatuss2
echo 0 > /var/www/html/openWB/ramdisk/pvcounter
echo 0 > /var/www/html/openWB/ramdisk/pvecounter
echo 0 > /var/www/html/openWB/ramdisk/glattwattbezug
echo 0 > /var/www/html/openWB/ramdisk/llas11
echo 0 > /var/www/html/openWB/ramdisk/bezuga1
echo 0 > /var/www/html/openWB/ramdisk/bezuga2
echo 0 > /var/www/html/openWB/ramdisk/bezuga3
echo 0 > /var/www/html/openWB/ramdisk/bezugw1
echo 0 > /var/www/html/openWB/ramdisk/bezugw2
echo 0 > /var/www/html/openWB/ramdisk/bezugw3
echo 0 > /var/www/html/openWB/ramdisk/llv1
echo 0 > /var/www/html/openWB/ramdisk/llv2
echo 0 > /var/www/html/openWB/ramdisk/llv3
echo 0 > /var/www/html/openWB/ramdisk/llvs11
echo 0 > /var/www/html/openWB/ramdisk/llvs12
echo 0 > /var/www/html/openWB/ramdisk/llvs13
echo 0 > /var/www/html/openWB/ramdisk/llvs21
echo 0 > /var/www/html/openWB/ramdisk/llvs22
echo 0 > /var/www/html/openWB/ramdisk/llvs23
echo 0 > /var/www/html/openWB/ramdisk/llaltnv
echo 0 > /var/www/html/openWB/ramdisk/llhz
echo 0 > /var/www/html/openWB/ramdisk/llpf1
echo 0 > /var/www/html/openWB/ramdisk/llpf2
echo 0 > /var/www/html/openWB/ramdisk/llpf3
echo 0 > /var/www/html/openWB/ramdisk/evuv1
echo 0 > /var/www/html/openWB/ramdisk/evuv2
echo 0 > /var/www/html/openWB/ramdisk/evuv3
echo 0 > /var/www/html/openWB/ramdisk/evuhz
echo 0 > /var/www/html/openWB/ramdisk/evupf1
echo 0 > /var/www/html/openWB/ramdisk/evupf2
echo 0 > /var/www/html/openWB/ramdisk/evupf3
echo 0 > /var/www/html/openWB/ramdisk/evuhz
echo 0 > /var/www/html/openWB/ramdisk/gelrlp1
echo 0 > /var/www/html/openWB/ramdisk/gelrlp2
echo 0 > /var/www/html/openWB/ramdisk/gelrlp3
echo 0 > /var/www/html/openWB/ramdisk/mqttgelrlp1
echo 0 > /var/www/html/openWB/ramdisk/mqttgelrlp2
echo 0 > /var/www/html/openWB/ramdisk/mqttgelrlp3

echo 0 > /var/www/html/openWB/ramdisk/llsolls1
echo 0 > /var/www/html/openWB/ramdisk/llsolls2
echo 0 > /var/www/html/openWB/ramdisk/gelrlp3
echo 0 > /var/www/html/openWB/ramdisk/aktgeladen
echo 0 > /var/www/html/openWB/ramdisk/aktgeladens1
echo 0 > /var/www/html/openWB/ramdisk/aktgeladens2
echo 0 > /var/www/html/openWB/ramdisk/aktgeladenlp4
echo 0 > /var/www/html/openWB/ramdisk/aktgeladenlp5
echo 0 > /var/www/html/openWB/ramdisk/aktgeladenlp6
echo 0 > /var/www/html/openWB/ramdisk/aktgeladenlp7
echo 0 > /var/www/html/openWB/ramdisk/aktgeladenlp8
echo 0 > /var/www/html/openWB/ramdisk/llas12
echo 0 > /var/www/html/openWB/ramdisk/llas13

echo 0 > /var/www/html/openWB/ramdisk/ladestatus
echo $bootmodus > /var/www/html/openWB/ramdisk/lademodus
echo 1 > /var/www/html/openWB/ramdisk/llaktuell
echo 1 > /var/www/html/openWB/ramdisk/llaktuells1
echo 1 > /var/www/html/openWB/ramdisk/llaktuells2
echo 1 > /var/www/html/openWB/ramdisk/llaktuelllp4
echo 1 > /var/www/html/openWB/ramdisk/llaktuelllp5
echo 1 > /var/www/html/openWB/ramdisk/llaktuelllp6
echo 1 > /var/www/html/openWB/ramdisk/llaktuelllp7
echo 1 > /var/www/html/openWB/ramdisk/llaktuelllp8
echo 0 > /var/www/html/openWB/ramdisk/soc
echo 2 > /var/www/html/openWB/ramdisk/soc1
echo 0 > /var/www/html/openWB/ramdisk/soc1vorhanden
echo 0 > /var/www/html/openWB/ramdisk/lla1
echo 0 > /var/www/html/openWB/ramdisk/lla2
echo 0 > /var/www/html/openWB/ramdisk/lla3
touch /var/www/html/openWB/ramdisk/llog1
touch /var/www/html/openWB/ramdisk/llogs1
touch /var/www/html/openWB/ramdisk/llogs2
echo 1 > /var/www/html/openWB/ramdisk/anzahlphasen
echo 0 > /var/www/html/openWB/ramdisk/llkombiniert
echo 0 > /var/www/html/openWB/ramdisk/llkwh
echo "--" > /var/www/html/openWB/ramdisk/restzeitlp1
echo "--" > /var/www/html/openWB/ramdisk/restzeitlp2
echo "--" > /var/www/html/openWB/ramdisk/restzeitlp3
echo "0" > /var/www/html/openWB/ramdisk/restzeitlp1m
echo "0" > /var/www/html/openWB/ramdisk/restzeitlp2m
echo "0" > /var/www/html/openWB/ramdisk/restzeitlp3m
echo 0 > /var/www/html/openWB/ramdisk/bezugkwh
echo 0 > /var/www/html/openWB/ramdisk/einspeisungkwh
echo 0 > /var/www/html/openWB/ramdisk/llkwhs1
echo 0 > /var/www/html/openWB/ramdisk/llkwhs2
echo 0 > /var/www/html/openWB/ramdisk/llkwhges
echo 20000 > /var/www/html/openWB/ramdisk/soctimer
echo 20000 > /var/www/html/openWB/ramdisk/soctimer1
echo 0 > /var/www/html/openWB/ramdisk/ev.graph
echo 0 > /var/www/html/openWB/ramdisk/ev-live.graph
echo 0 > /var/www/html/openWB/ramdisk/evu.graph
echo 0 > /var/www/html/openWB/ramdisk/evu-live.graph
echo 0 > /var/www/html/openWB/ramdisk/pv.graph
echo 0 > /var/www/html/openWB/ramdisk/pv-live.graph
echo 0 > /var/www/html/openWB/ramdisk/date.graph
echo 0 > /var/www/html/openWB/ramdisk/date-live.graph
echo 0 > /var/www/html/openWB/ramdisk/soc.graph
echo 0 > /var/www/html/openWB/ramdisk/soc-live.graph
echo 0 > /var/www/html/openWB/ramdisk/speicherikwh
echo 0 > /var/www/html/openWB/ramdisk/speicherekwh
echo 28 > /var/www/html/openWB/ramdisk/evsemodbustimer
echo 0 > /var/www/html/openWB/ramdisk/rsestatus
echo 0 > /var/www/html/openWB/ramdisk/rseaktiv
echo "nicht angefragt" > /var/www/html/openWB/ramdisk/evsedintestlp1
echo "nicht angefragt" > /var/www/html/openWB/ramdisk/evsedintestlp2
echo "nicht angefragt" > /var/www/html/openWB/ramdisk/evsedintestlp3
echo 0 > /var/www/html/openWB/ramdisk/u1p3pstat
echo 0 > /var/www/html/openWB/ramdisk/hook1einschaltverzcounter
echo 0 > /var/www/html/openWB/ramdisk/hook2einschaltverzcounter
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod 777 /var/www/html/openWB/web/files/*
sudo chmod -R +x /var/www/html/openWB/modules/*
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3s1




ln -s /var/log/openWB.log /var/www/html/openWB/ramdisk/openWB.log
mkdir -p /var/www/html/openWB/web/logging/data/daily
mkdir -p /var/www/html/openWB/web/logging/data/monthly
sudo chmod -R 777 /var/www/html/openWB/web/logging/data/
if ! grep -Fq "hook1einschaltverz=" /var/www/html/openWB/openwb.conf
then
  echo "hook1einschaltverz=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook2einschaltverz=" /var/www/html/openWB/openwb.conf
then
  echo "hook2einschaltverz=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "stopsocnotpluggedlp1=" /var/www/html/openWB/openwb.conf
then
  echo "stopsocnotpluggedlp1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sonnenecoip=" /var/www/html/openWB/openwb.conf
then
  echo "sonnenecoip=192.168.15.3" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sonnenecoalternativ=" /var/www/html/openWB/openwb.conf
then
  echo "sonnenecoalternativ=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "abschaltverzoegerung=" /var/www/html/openWB/openwb.conf
then
  echo "abschaltverzoegerung=600" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "einschaltverzoegerung=" /var/www/html/openWB/openwb.conf
then
  echo "einschaltverzoegerung=30" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ladetaster=" /var/www/html/openWB/openwb.conf
then
	  echo "ladetaster=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rseenabled=" /var/www/html/openWB/openwb.conf
then
	  echo "rseenabled=0" >> /var/www/html/openWB/openwb.conf
fi
. /var/www/html/openWB/openwb.conf
if (( ladetaster == 1 )); then
	if ! [ -x "$(command -v nmcli)" ]; then
		if ps ax |grep -v grep |grep "python /var/www/html/openWB/runs/ladetaster.py" > /dev/null
		then
			echo "test" > /dev/null
		else
			sudo python /var/www/html/openWB/runs/ladetaster.py &
		fi
	fi
fi
if (( rseenabled == 1 )); then
	if ! [ -x "$(command -v nmcli)" ]; then
		if ps ax |grep -v grep |grep "python /var/www/html/openWB/runs/rse.py" > /dev/null
		then
			echo "test" > /dev/null
		else
			sudo python /var/www/html/openWB/runs/rse.py &
		fi
	fi
fi
if (( rfidakt == 1 )); then
	(sleep 10; sudo python /var/www/html/openWB/runs/readrfid.py $displayaktiv) &
	(sleep 10; sudo python /var/www/html/openWB/runs/readrfid2.py $displayaktiv) &
fi
if [[ $evsecon == twcmanager ]]; then
	if [[ $twcmanagerlp1ip == "localhost/TWC" ]]; then
		su - pi -c "screen -dm -S TWCManager /var/www/html/TWC/TWCManager.py" &
	fi
fi
if (( displayaktiv == 1 )); then
	if ! grep -Fq "pinch" /home/pi/.config/lxsession/LXDE-pi/autostart
	then
		echo "not found"
		echo "@xscreensaver -no-splash" > /home/pi/.config/lxsession/LXDE-pi/autostart
		echo "@point-rpi" >> /home/pi/.config/lxsession/LXDE-pi/autostart
		echo "@xset s 600" >> /home/pi/.config/lxsession/LXDE-pi/autostart
		echo "@chromium-browser --incognito --disable-pinch --kiosk http://localhost/openWB/web/display.php" >> /home/pi/.config/lxsession/LXDE-pi/autostart
	fi
fi

if ! grep -Fq "minimalapv=" /var/www/html/openWB/openwb.conf
then
	  echo "minimalapv=6" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "minimalalp2pv=" /var/www/html/openWB/openwb.conf
then
	  echo "minimalalp2pv=6" >> /var/www/html/openWB/openwb.conf
fi


if ! grep -Fq "minimalampv=" /var/www/html/openWB/openwb.conf
then
	  echo "minimalampv=10" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "pvbezugeinspeisung=" /var/www/html/openWB/openwb.conf
then
	  echo "pvbezugeinspeisung=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsecons2=" /var/www/html/openWB/openwb.conf
then
	  echo "evsecons2=dac" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsesources2=" /var/www/html/openWB/openwb.conf
then
	  echo "evsesources2=dac" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evseids2=" /var/www/html/openWB/openwb.conf
then
	  echo "evseids2=3" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evselanips2=" /var/www/html/openWB/openwb.conf
then
	  echo "evselanips2=192.168.14.2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ladeleistungs2modul=" /var/www/html/openWB/openwb.conf
then
	  echo "ladeleistungs2modul=sdm630modbuslls2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdmids2=" /var/www/html/openWB/openwb.conf
then
	  echo "sdmids2=4" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lastmanagements2=" /var/www/html/openWB/openwb.conf
then
	  echo "lastmanagements2=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortlls1=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortlls1=18" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortlls2=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortlls2=17" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "dspeed=" /var/www/html/openWB/openwb.conf
then
	  echo "dspeed=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "durchslp1=" /var/www/html/openWB/openwb.conf
then
	  echo "durchslp1=15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "durchslp3=" /var/www/html/openWB/openwb.conf
then
	  echo "durchslp3=15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "durchslp2=" /var/www/html/openWB/openwb.conf
then
	  echo "durchslp2=15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nachtladens1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtladens1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nachtsocs1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtsocs1=50" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nachtsoc1s1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtsoc1s1=35" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nachtsoc1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtsoc1=35" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "nachtlls1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtlls1=12" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nachtladenabuhrs1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtladenabuhrs1=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lademkwh=" /var/www/html/openWB/openwb.conf
then
	  echo "lademkwh=15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lademkwhs1=" /var/www/html/openWB/openwb.conf
then
	  echo "lademkwhs1=15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lademkwhs2=" /var/www/html/openWB/openwb.conf
then
	  echo "lademkwhs2=15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lademstat=" /var/www/html/openWB/openwb.conf
then
	  echo "lademstat=" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lademstats1=" /var/www/html/openWB/openwb.conf
then
	  echo "lademstats1=" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lademstats2=" /var/www/html/openWB/openwb.conf
then
	  echo "lademstats2=" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllsource=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllsource=/dev/ttyUSB1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "speichersocnurpv=" /var/www/html/openWB/openwb.conf
then
	  echo "speichersocnurpv=100" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "speichersocminpv=" /var/www/html/openWB/openwb.conf
then
	  echo "speichersocminpv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "speichersochystminpv=" /var/www/html/openWB/openwb.conf
then
	  echo "speichersochystminpv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "speicherwattnurpv=" /var/www/html/openWB/openwb.conf
then
	  echo "speicherwattnurpv=1500" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nurpvslowup=" /var/www/html/openWB/openwb.conf
then
	  echo "nurpvslowup=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllid1=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllid1=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllid2=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllid2=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllid3=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllid3=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllid1s1=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllid1s1=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllid2s1=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllid2s1=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllid3s1=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllid3s1=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllid1s2=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllid1s2=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllid2s2=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllid2s2=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120modbusllid3s2=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllid3s2=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsewifiiplp1=" /var/www/html/openWB/openwb.conf
then
	  echo "evsewifiiplp1=192.168.0.25" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsewifiiplp2=" /var/www/html/openWB/openwb.conf
then
	  echo "evsewifiiplp2=192.168.0.25" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsewifiiplp3=" /var/www/html/openWB/openwb.conf
then
	  echo "evsewifiiplp3=192.168.0.25" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsewifitimeoutlp1=" /var/www/html/openWB/openwb.conf
then
	  echo "evsewifitimeoutlp1=2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsewifitimeoutlp2=" /var/www/html/openWB/openwb.conf
then
	  echo "evsewifitimeoutlp2=2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evsewifitimeoutlp3=" /var/www/html/openWB/openwb.conf
then
	  echo "evsewifitimeoutlp3=2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortsoclp1=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortsoclp1=90" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortsoclp2=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortsoclp2=90" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortsoclp3=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortsoclp3=90" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortsocstatlp1=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortsocstatlp1=" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortsocstatlp2=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortsocstatlp2=" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sofortsocstatlp3=" /var/www/html/openWB/openwb.conf
then
	  echo "sofortsocstatlp3=" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pvsoclp1=" /var/www/html/openWB/openwb.conf
then
	  echo "pvsoclp1=100" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pvsoclp2=" /var/www/html/openWB/openwb.conf
then
	  echo "pvsoclp2=100" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pvsoclp3=" /var/www/html/openWB/openwb.conf
then
	  echo "pvsoclp3=100" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmllsource=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmllsource=/dev/ttyUSB0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmllid=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmllid=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "msmoduslp1=" /var/www/html/openWB/openwb.conf
then
	  echo "msmoduslp1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "msmoduslp2=" /var/www/html/openWB/openwb.conf
then
	  echo "msmoduslp2=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "stopchargepvatpercentlp1=" /var/www/html/openWB/openwb.conf
then
	echo "stopchargepvatpercentlp1=0" >> /var/www/html/openWB/openwb.conf
	echo "stopchargepvatpercentlp2=0" >> /var/www/html/openWB/openwb.conf
	echo "stopchargepvpercentagelp1=90" >> /var/www/html/openWB/openwb.conf
	echo "stopchargepvpercentagelp2=90" >> /var/www/html/openWB/openwb.conf

fi
if ! grep -Fq "msmoduslp3=" /var/www/html/openWB/openwb.conf
then
	echo "msmoduslp3=0" >> /var/www/html/openWB/openwb.conf
	echo "msmoduslp4=0" >> /var/www/html/openWB/openwb.conf
	echo "msmoduslp5=0" >> /var/www/html/openWB/openwb.conf
	echo "msmoduslp6=0" >> /var/www/html/openWB/openwb.conf
	echo "msmoduslp7=0" >> /var/www/html/openWB/openwb.conf
	echo "msmoduslp8=0" >> /var/www/html/openWB/openwb.conf

fi
if ! grep -Fq "nachtladenbisuhrs1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtladenbisuhrs1=6" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "leafusername=" /var/www/html/openWB/openwb.conf
then
	  echo "leafusername=username" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "leafpasswort=" /var/www/html/openWB/openwb.conf
then
	  echo "leafpasswort=passwort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "leafusernames1=" /var/www/html/openWB/openwb.conf
then
	  echo "leafusernames1=username" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "leafpassworts1=" /var/www/html/openWB/openwb.conf
then
	  echo "leafpassworts1=passwort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "i3username=" /var/www/html/openWB/openwb.conf
then
	  echo "i3username=username" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soci3intervall=" /var/www/html/openWB/openwb.conf
then
	  echo "soci3intervall=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soci3intervall1=" /var/www/html/openWB/openwb.conf
then
	  echo "soci3intervall1=10" >> /var/www/html/openWB/openwb.conf
fi


if ! grep -Fq "i3passwort=" /var/www/html/openWB/openwb.conf
then
	  echo "i3passwort=passwort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "i3usernames1=" /var/www/html/openWB/openwb.conf
then
	  echo "i3usernames1=username" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "i3passworts1=" /var/www/html/openWB/openwb.conf
then
	  echo "i3passworts1=passwort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "i3vins1=" /var/www/html/openWB/openwb.conf
then
	  echo "i3vins1=VIN" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "i3vin=" /var/www/html/openWB/openwb.conf
then
	  echo "i3vin=VIN" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zoeusername=" /var/www/html/openWB/openwb.conf
then
	  echo "zoeusername=username" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zoepasswort=" /var/www/html/openWB/openwb.conf
then
	  echo "zoepasswort='passwort'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zoelp2username=" /var/www/html/openWB/openwb.conf
then
	  echo "zoelp2username=username" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zoelp2passwort=" /var/www/html/openWB/openwb.conf
then
	  echo "zoelp2passwort='passwort'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "minnurpvsocll=" /var/www/html/openWB/openwb.conf
then
	  echo "minnurpvsocll=12" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "minnurpvsoclp1=" /var/www/html/openWB/openwb.conf
then
	  echo "minnurpvsoclp1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "maxnurpvsoclp1=" /var/www/html/openWB/openwb.conf
then
	  echo "maxnurpvsoclp1=100" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evnotifyakey=" /var/www/html/openWB/openwb.conf
then
	  echo "evnotifyakey=abcdef" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evnotifytoken=" /var/www/html/openWB/openwb.conf
then
	  echo "evnotifytoken=token" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evnotifyakeylp2=" /var/www/html/openWB/openwb.conf
then
	  echo "evnotifyakeylp2=abcdef" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evnotifytokenlp2=" /var/www/html/openWB/openwb.conf
then
	  echo "evnotifytokenlp2=token" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrjsonwatt=" /var/www/html/openWB/openwb.conf
then
	  echo "wrjsonwatt=.watt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrjsonkwh=" /var/www/html/openWB/openwb.conf
then
	  echo "wrjsonkwh=.kwh" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrjsonurl=" /var/www/html/openWB/openwb.conf
then
	  echo "wrjsonurl=http://192.168.0.12/solar_api" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hausbezugnone=" /var/www/html/openWB/openwb.conf
then
	  echo "hausbezugnone=200" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "twcmanagerlp1ip=" /var/www/html/openWB/openwb.conf
then
	  echo "twcmanagerlp1ip='192.168.0.15'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "twcmanagerlp1phasen=" /var/www/html/openWB/openwb.conf
then
	  echo "twcmanagerlp1phasen=3" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "mpm3pmpvsource=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmpvsource=/dev/ttyUSB0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmpvid=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmpvid=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmpvlanip=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmpvlanip=192.168.1.12" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezugjsonwatt=" /var/www/html/openWB/openwb.conf
then
	  echo "bezugjsonwatt=.watt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezugjsonkwh=" /var/www/html/openWB/openwb.conf
then
	  echo "bezugjsonkwh=.kwh" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "einspeisungjsonkwh=" /var/www/html/openWB/openwb.conf
then
	  echo "einspeisungjsonkwh=.kwh" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezugjsonurl=" /var/www/html/openWB/openwb.conf
then
	  echo "bezugjsonurl=http://192.168.0.12/solar_api" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmlls1source=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmlls1source=/dev/ttyUSB0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmlls1id=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmlls1id=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmlls2source=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmlls2source=/dev/ttyUSB0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmlls2id=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmlls2id=5" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmevusource=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmevusource=/dev/ttyUSB0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmevuid=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmevuid=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "livegraph=" /var/www/html/openWB/openwb.conf
then
	  echo "livegraph=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_solarlog_ip=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_solarlog_ip=192.168.0.10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_solarlog_speicherv=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_solarlog_speicherv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrfronius2ip=" /var/www/html/openWB/openwb.conf
then
	  echo "wrfronius2ip=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "speichermodul=" /var/www/html/openWB/openwb.conf
then
	  echo "speichermodul=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displaytheme=" /var/www/html/openWB/openwb.conf
then
	  echo "displaytheme=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displaytagesgraph=" /var/www/html/openWB/openwb.conf
then
	  echo "displaytagesgraph=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displayEinBeimAnstecken=" /var/www/html/openWB/openwb.conf
then
	  echo "displayEinBeimAnstecken=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "speicherleistung_http=" /var/www/html/openWB/openwb.conf
then
	  echo "speicherleistung_http=192.168.0.10/watt" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "speichersoc_http=" /var/www/html/openWB/openwb.conf
then
	  echo "speichersoc_http=192.168.0.10/soc" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_tesla_username=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_tesla_username=deine@email.com" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_tesla_carnumber=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_tesla_carnumber=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_tesla_password=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_tesla_password=daspasswort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_tesla_intervallladen=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_tesla_intervallladen=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_tesla_intervall=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_tesla_intervall=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "releasetrain=" /var/www/html/openWB/openwb.conf
then
	  echo "releasetrain=stable" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrkostalpikoip=" /var/www/html/openWB/openwb.conf
then
		  echo "wrkostalpikoip=192.168.0.10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "solaredgeip=" /var/www/html/openWB/openwb.conf
then
		  echo "solaredgeip=192.168.0.10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "solaredgepvip=" /var/www/html/openWB/openwb.conf
then
		  echo "solaredgepvip=192.168.0.10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "solaredgepvslave1=" /var/www/html/openWB/openwb.conf
then
		  echo "solaredgepvslave1=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "solaredgepvslave2=" /var/www/html/openWB/openwb.conf
then
		  echo "solaredgepvslave2=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "solaredgepvslave3=" /var/www/html/openWB/openwb.conf
then
		  echo "solaredgepvslave3=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lllaniplp2=" /var/www/html/openWB/openwb.conf
then
		  echo "lllaniplp2=192.168.0.10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm630lp2source=" /var/www/html/openWB/openwb.conf
then
		  echo "sdm630lp2source=/dev/ttyUSB0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120lp2source=" /var/www/html/openWB/openwb.conf
then
		  echo "sdm120lp2source=/dev/ttyUSB0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm120lp3source=" /var/www/html/openWB/openwb.conf
then
		  echo "sdm120lp3source=/dev/ttyUSB0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sdm630lp3source=" /var/www/html/openWB/openwb.conf
then
		  echo "sdm630lp3source=/dev/ttyUSB0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lllaniplp3=" /var/www/html/openWB/openwb.conf
then
		  echo "lllaniplp3=192.168.0.10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lp1name=" /var/www/html/openWB/openwb.conf
then
		  echo "lp1name='LP1'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lp2name=" /var/www/html/openWB/openwb.conf
then
		  echo "lp2name='LP2'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lp3name=" /var/www/html/openWB/openwb.conf
then
		  echo "lp3name='LP3'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "loadsharinglp12=" /var/www/html/openWB/openwb.conf
then
		  echo "loadsharinglp12=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "loadsharingalp12=" /var/www/html/openWB/openwb.conf
then
		  echo "loadsharingalp12=32" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "goeiplp1=" /var/www/html/openWB/openwb.conf
then
		  echo "goeiplp1=192.168.0.15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "goetimeoutlp1=" /var/www/html/openWB/openwb.conf
then
		  echo "goetimeoutlp1=5" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "goeiplp2=" /var/www/html/openWB/openwb.conf
then
		  echo "goeiplp2=192.168.0.15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "goetimeoutlp2=" /var/www/html/openWB/openwb.conf
then
		  echo "goetimeoutlp2=5" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "goeiplp3=" /var/www/html/openWB/openwb.conf
then
		  echo "goeiplp3=192.168.0.15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "goetimeoutlp3=" /var/www/html/openWB/openwb.conf
then
		  echo "goetimeoutlp3=5" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pushbenachrichtigung=" /var/www/html/openWB/openwb.conf
then
		  echo "pushbenachrichtigung=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pushovertoken=" /var/www/html/openWB/openwb.conf
then
		  echo "pushovertoken='demotoken'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pushoveruser=" /var/www/html/openWB/openwb.conf
then
		  echo "pushoveruser='demouser'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pushbstartl=" /var/www/html/openWB/openwb.conf
then
		  echo "pushbstartl=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pushbstopl=" /var/www/html/openWB/openwb.conf
then
		  echo "pushbstopl=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "smashmbezugid=" /var/www/html/openWB/openwb.conf
then
		  echo "smashmbezugid=1234567789" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmspeichersource=" /var/www/html/openWB/openwb.conf
then
		  echo "mpm3pmspeichersource=/dev/tty2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmspeicherid=" /var/www/html/openWB/openwb.conf
then
		  echo "mpm3pmspeicherid=8" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmspeicherpv=" /var/www/html/openWB/openwb.conf
then
		  echo "mpm3pmspeicherpv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmspeicherlanip=" /var/www/html/openWB/openwb.conf
then
		  echo "mpm3pmspeicherlanip=192.168.5.10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "logdailywh=" /var/www/html/openWB/openwb.conf
then
		  echo "logdailywh=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "logeinspeisungneg=" /var/www/html/openWB/openwb.conf
then
		  echo "logeinspeisungneg=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "speicherpveinbeziehen=" /var/www/html/openWB/openwb.conf
then
		  echo "speicherpveinbeziehen=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "speicherpvui=" /var/www/html/openWB/openwb.conf
then
		  echo "speicherpvui=0" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "speichermaxwatt=" /var/www/html/openWB/openwb.conf
then
		  echo "speichermaxwatt=0" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "nacht2lls1=" /var/www/html/openWB/openwb.conf
then
	  echo "nacht2lls1=12" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nachtladen2abuhrs1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtladen2abuhrs1=7" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nachtladen2bisuhrs1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtladen2bisuhrs1=7" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nacht2ll=" /var/www/html/openWB/openwb.conf
then
	  echo "nacht2ll=12" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nachtladen2abuhr=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtladen2abuhr=7" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nachtladen2bisuhr=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtladen2bisuhr=7" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "akkuglp1=" /var/www/html/openWB/openwb.conf
then
	  echo "akkuglp1=35" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "akkuglp2=" /var/www/html/openWB/openwb.conf
then
	  echo "akkuglp2=35" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zielladenuhrzeitlp1=" /var/www/html/openWB/openwb.conf
then
	  echo "zielladenuhrzeitlp1='2018-12-19 06:15'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zielladensoclp1=" /var/www/html/openWB/openwb.conf
then
	  echo "zielladensoclp1=60" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zielladenalp1=" /var/www/html/openWB/openwb.conf
then
	  echo "zielladenalp1=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zielladenphasenlp1=" /var/www/html/openWB/openwb.conf
then
	  echo "zielladenphasenlp1=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zielladenmaxalp1=" /var/www/html/openWB/openwb.conf
then
	  echo "zielladenmaxalp1=32" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "zielladenaktivlp1=" /var/www/html/openWB/openwb.conf
then
	  echo "zielladenaktivlp1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_smartme_user=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_smartme_user='user'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_smartme_pass=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_smartme_pass='pass'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_smartme_url=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_smartme_url='https://smart-me.com:443/api/Devices/[ID]'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wr_smartme_user=" /var/www/html/openWB/openwb.conf
then
	  echo "wr_smartme_user='user'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wr_smartme_pass=" /var/www/html/openWB/openwb.conf
then
	  echo "wr_smartme_pass='pass'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wr_smartme_url=" /var/www/html/openWB/openwb.conf
then
	  echo "wr_smartme_url='https://smart-me.com:443/api/Devices/[ID]'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wr_piko2_user=" /var/www/html/openWB/openwb.conf
then
	  echo "wr_piko2_user='user'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wr_piko2_pass=" /var/www/html/openWB/openwb.conf
then
	  echo "wr_piko2_pass='pass'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wr_piko2_url=" /var/www/html/openWB/openwb.conf
then
	  echo "wr_piko2_url='https://url'" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "carnetuser=" /var/www/html/openWB/openwb.conf
then
	  echo "carnetuser='user'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "carnetpass=" /var/www/html/openWB/openwb.conf
then
	  echo "carnetpass='pass'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soccarnetintervall=" /var/www/html/openWB/openwb.conf
then
	  echo "soccarnetintervall=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bydhvuser=" /var/www/html/openWB/openwb.conf
then
	  echo "bydhvuser=benutzer" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "bydhvpass=" /var/www/html/openWB/openwb.conf
then
	  echo "bydhvpass=pass" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "bydhvip=" /var/www/html/openWB/openwb.conf
then
	  echo "bydhvip=192.168.10.12" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "e3dcip=" /var/www/html/openWB/openwb.conf
then
	  echo "e3dcip=192.168.10.12" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "e3dc2ip=" /var/www/html/openWB/openwb.conf
then
	  echo "e3dc2ip=none" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "bezug_http_l1_url=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_http_l1_url='http://192.168.0.17/bezuga1'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_http_l2_url=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_http_l2_url='http://192.168.0.17/bezuga2'" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "bezug_http_l3_url=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_http_l3_url='http://192.168.0.17/bezuga3'" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "sbs25ip=" /var/www/html/openWB/openwb.conf
then
	  echo "sbs25ip=192.168.10.12" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "tri9000ip=" /var/www/html/openWB/openwb.conf
then
	  echo "tri9000ip=192.168.10.12" >> /var/www/html/openWB/openwb.conf
  fi

 if ! grep -Fq "solaredgespeicherip=" /var/www/html/openWB/openwb.conf
then
	  echo "solaredgespeicherip='192.168.0.31'" >> /var/www/html/openWB/openwb.conf
  fi
 if ! grep -Fq "offsetpv=" /var/www/html/openWB/openwb.conf
then
	  echo "offsetpv=0" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "kostalplenticoreip=" /var/www/html/openWB/openwb.conf
then
    echo "kostalplenticoreip=192.168.0.30" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "kostalplenticoreip2=" /var/www/html/openWB/openwb.conf
then
    echo "kostalplenticoreip2=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "name_wechselrichter1=" /var/www/html/openWB/openwb.conf
then
    echo "name_wechselrichter1=WR1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "name_wechselrichter2=" /var/www/html/openWB/openwb.conf
then
    echo "name_wechselrichter2=WR2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook1ein_url=" /var/www/html/openWB/openwb.conf
then
	  echo "hook1ein_url='https://webhook.com/ein.php'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "angesteckthooklp1_url=" /var/www/html/openWB/openwb.conf
then
	  echo "angesteckthooklp1_url='https://webhook.com/ein.php'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook1aus_url=" /var/www/html/openWB/openwb.conf
then
	  echo "hook1aus_url='https://webhook.com/aus.php'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook1_ausverz=" /var/www/html/openWB/openwb.conf
then
	  echo "hook1_ausverz=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook1ein_watt=" /var/www/html/openWB/openwb.conf
then
	  echo "hook1ein_watt=1200" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook1aus_watt=" /var/www/html/openWB/openwb.conf
then
	  echo "hook1aus_watt=400" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook1_aktiv=" /var/www/html/openWB/openwb.conf
then
	  echo "hook1_aktiv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "angesteckthooklp1=" /var/www/html/openWB/openwb.conf
then
	  echo "angesteckthooklp1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook1_dauer=" /var/www/html/openWB/openwb.conf
then
	  echo "hook1_dauer=5" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook2ein_url=" /var/www/html/openWB/openwb.conf
then
	  echo "hook2ein_url='https://webhook.com/ein.php'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook2aus_url=" /var/www/html/openWB/openwb.conf
then
	  echo "hook2aus_url='https://webhook.com/aus.php'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook2ein_watt=" /var/www/html/openWB/openwb.conf
then
	  echo "hook2ein_watt=1200" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook2aus_watt=" /var/www/html/openWB/openwb.conf
then
	  echo "hook2aus_watt=400" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook2_aktiv=" /var/www/html/openWB/openwb.conf
then
	  echo "hook2_aktiv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook2_dauer=" /var/www/html/openWB/openwb.conf
then
	  echo "hook2_dauer=5" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook2_ausverz=" /var/www/html/openWB/openwb.conf
then
	  echo "hook2_ausverz=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook3ein_url=" /var/www/html/openWB/openwb.conf
then
	  echo "hook3ein_url='https://webhook.com/ein.php'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook3aus_url=" /var/www/html/openWB/openwb.conf
then
	  echo "hook3aus_url='https://webhook.com/aus.php'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook3ein_watt=" /var/www/html/openWB/openwb.conf
then
	  echo "hook3ein_watt=1200" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook3aus_watt=" /var/www/html/openWB/openwb.conf
then
	  echo "hook3aus_watt=400" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook3_aktiv=" /var/www/html/openWB/openwb.conf
then
	  echo "hook3_aktiv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook3_dauer=" /var/www/html/openWB/openwb.conf
then
	  echo "hook3_dauer=5" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook3_ausverz=" /var/www/html/openWB/openwb.conf
then
	  echo "hook3_ausverz=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher1_aktiv=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher1_aktiv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher1_typ=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher1_typ=http" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher1_name=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher1_name=Name" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher1_id=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher1_id=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher1_ip=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher1_ip=192.168.4.123" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher1_source=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher1_source=/dev/ttyUSB5" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "verbraucher1_urlw=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher1_urlw='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher1_urlh=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher1_urlh='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher1_tempwh=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher1_tempwh=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher2_tempwh=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher2_tempwh=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher2_name=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher2_name=Name" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher2_aktiv=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher2_aktiv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher2_typ=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher2_typ=http" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher2_urlw=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher2_urlw='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher2_urlh=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher2_urlh='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher2_id=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher2_id=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher2_ip=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher2_ip=192.168.4.123" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher2_source=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher2_source=/dev/ttyUSB5" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "verbraucher3_name=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher3_name=Name" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher3_aktiv=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher3_aktiv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher3_typ=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher3_typ=http" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher3_urlw=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher3_urlw='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "verbraucher3_urlh=" /var/www/html/openWB/openwb.conf
then
	  echo "verbraucher3_urlh='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nurpv70dynact=" /var/www/html/openWB/openwb.conf
then
	echo "nurpv70dynact=0" >> /var/www/html/openWB/openwb.conf
	echo "nurpv70dynw=6000" >> /var/www/html/openWB/openwb.conf

fi

if ! grep -Fq "nlakt_sofort=" /var/www/html/openWB/openwb.conf
then
	  echo "nlakt_sofort=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nlakt_minpv=" /var/www/html/openWB/openwb.conf
then
	  echo "nlakt_minpv=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nlakt_nurpv=" /var/www/html/openWB/openwb.conf
then
	  echo "nlakt_nurpv=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nlakt_standby=" /var/www/html/openWB/openwb.conf
then
	  echo "nlakt_standby=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpm3pmevuhaus=" /var/www/html/openWB/openwb.conf
then
	  echo "mpm3pmevuhaus=0" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "carnetlp2user=" /var/www/html/openWB/openwb.conf
then
	  echo "carnetlp2user='user'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "carnetlp2pass=" /var/www/html/openWB/openwb.conf
then
	  echo "carnetlp2pass='pass'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soccarnetlp2intervall=" /var/www/html/openWB/openwb.conf
then
	  echo "soccarnetlp2intervall=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_teslalp2_username=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_teslalp2_username=deine@email.com" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_teslalp2_carnumber=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_teslalp2_carnumber=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_teslalp2_password=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_teslalp2_password=daspasswort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_teslalp2_intervallladen=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_teslalp2_intervallladen=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_teslalp2_intervall=" /var/www/html/openWB/openwb.conf
then
	  echo "soc_teslalp2_intervall=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrsma2ip=" /var/www/html/openWB/openwb.conf
then
	  echo "wrsma2ip=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrsma3ip=" /var/www/html/openWB/openwb.conf
then
	  echo "wrsma3ip=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrsma4ip=" /var/www/html/openWB/openwb.conf
then
	  echo "wrsma4ip=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evuglaettung=" /var/www/html/openWB/openwb.conf
then
	  echo "evuglaettung=10" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "evuglaettungakt=" /var/www/html/openWB/openwb.conf
then
	  echo "evuglaettungakt=0" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "u1p3paktiv=" /var/www/html/openWB/openwb.conf
then
	  echo "u1p3paktiv=0" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "u1p3psofort=" /var/www/html/openWB/openwb.conf
then
	  echo "u1p3psofort=3" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "u1p3pstandby=" /var/www/html/openWB/openwb.conf
then
	  echo "u1p3pstandby=3" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "u1p3pnurpv=" /var/www/html/openWB/openwb.conf
then
	  echo "u1p3pnurpv=1" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "u1p3pminundpv=" /var/www/html/openWB/openwb.conf
then
	  echo "u1p3pminundpv=1" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "u1p3pnl=" /var/www/html/openWB/openwb.conf
then
	  echo "u1p3pnl=3" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "speicherpwip=" /var/www/html/openWB/openwb.conf
then
	  echo "speicherpwip=192.168.0.10" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "vartaspeicherip=" /var/www/html/openWB/openwb.conf
then
	  echo "vartaspeicherip=192.168.0.10" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "adaptpv=" /var/www/html/openWB/openwb.conf
then
	  echo "adaptpv=0" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "adaptfaktor=" /var/www/html/openWB/openwb.conf
then
	  echo "adaptfaktor=5" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "grapham=" /var/www/html/openWB/openwb.conf
then
	  echo "grapham=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "graphliveam=" /var/www/html/openWB/openwb.conf
then
	  echo "graphliveam=0" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "nrgkickiplp1=" /var/www/html/openWB/openwb.conf
then
	  echo "nrgkickiplp1=192.168.0.17" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nrgkicktimeoutlp1=" /var/www/html/openWB/openwb.conf
then
	  echo "nrgkicktimeoutlp1=3" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nrgkickmaclp1=" /var/www/html/openWB/openwb.conf
then
	  echo "nrgkickmaclp1=11:22:33:aa:bb:cc" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nrgkickpwlp1=" /var/www/html/openWB/openwb.conf
then
	  echo "nrgkickpwlp1=1234" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "kostalplenticorehaus=" /var/www/html/openWB/openwb.conf
then
	  echo "kostalplenticorehaus=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "kostalplenticorebatt=" /var/www/html/openWB/openwb.conf
then
	  echo "kostalplenticorebatt=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "froniusprimo=" /var/www/html/openWB/openwb.conf
then
	  echo "froniusprimo=0" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "kebaiplp1=" /var/www/html/openWB/openwb.conf
then
	  echo "kebaiplp1=192.168.25.25" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "kebaiplp2=" /var/www/html/openWB/openwb.conf
then
	  echo "kebaiplp2=192.168.25.25" >> /var/www/html/openWB/openwb.conf
  fi

  if ! grep -Fq "graphinteractiveam=" /var/www/html/openWB/openwb.conf
then
	  echo "graphinteractiveam=1" >> /var/www/html/openWB/openwb.conf
  fi
  if ! grep -Fq "bezug_smartfox_ip=" /var/www/html/openWB/openwb.conf
then
	  echo "bezug_smartfox_ip=192.168.0.50" >> /var/www/html/openWB/openwb.conf
  fi
  if ! grep -Fq "chartlegendmain=" /var/www/html/openWB/openwb.conf
then
	  echo "chartlegendmain=1" >> /var/www/html/openWB/openwb.conf
  fi
if ! grep -Fq "nrgkickiplp2=" /var/www/html/openWB/openwb.conf
then
	  echo "nrgkickiplp2=192.168.0.17" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nrgkicktimeoutlp2=" /var/www/html/openWB/openwb.conf
then
	  echo "nrgkicktimeoutlp2=3" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nrgkickmaclp2=" /var/www/html/openWB/openwb.conf
then
	  echo "nrgkickmaclp2=11:22:33:aa:bb:cc" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "nrgkickpwlp2=" /var/www/html/openWB/openwb.conf
then
	  echo "nrgkickpwlp2=1234" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hausverbrauchstat=" /var/www/html/openWB/openwb.conf
then
	  echo "hausverbrauchstat=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "theme=" /var/www/html/openWB/openwb.conf
then
	  echo "theme=standard" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "solaredgewr2ip=" /var/www/html/openWB/openwb.conf
then
	  echo "solaredgewr2ip=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "heutegeladen=" /var/www/html/openWB/openwb.conf
then
	  echo "heutegeladen=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "sunnyislandip=" /var/www/html/openWB/openwb.conf
then
	  echo "sunnyislandip=192.168.0.17" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug1_ip=" /var/www/html/openWB/openwb.conf
then
	echo "bezug1_ip=192.168.0.17" >> /var/www/html/openWB/openwb.conf
	echo "pv1_ipa=192.168.0.17" >> /var/www/html/openWB/openwb.conf
	echo "pv1_ipb=192.168.0.17" >> /var/www/html/openWB/openwb.conf
	echo "pv1_ipc=192.168.0.17" >> /var/www/html/openWB/openwb.conf
	echo "pv1_ipd=192.168.0.17" >> /var/www/html/openWB/openwb.conf
	echo "pv1_ida=1" >> /var/www/html/openWB/openwb.conf
	echo "pv1_idb=1" >> /var/www/html/openWB/openwb.conf
	echo "pv1_idc=1" >> /var/www/html/openWB/openwb.conf
	echo "pv1_idd=1" >> /var/www/html/openWB/openwb.conf
	echo "speicher1_ip=192.168.0.17" >> /var/www/html/openWB/openwb.conf

fi
if ! grep -Fq "fsm63a3modbusllsource=" /var/www/html/openWB/openwb.conf
then
	  echo "fsm63a3modbusllsource=/dev/ttyUSB2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "fsm63a3modbusllid=" /var/www/html/openWB/openwb.conf
then
	  echo "fsm63a3modbusllid=8" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wakeupzoelp1=" /var/www/html/openWB/openwb.conf
then
	echo "wakeupzoelp1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wakeupzoelp2=" /var/www/html/openWB/openwb.conf
then
	echo "wakeupzoelp2=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wakeupmyrenaultlp1=" /var/www/html/openWB/openwb.conf
then
	echo "wakeupmyrenaultlp1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wakeupmyrenaultlp2=" /var/www/html/openWB/openwb.conf
then
	echo "wakeupmyrenaultlp2=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "awattarlocation=" /var/www/html/openWB/openwb.conf
then
	echo "awattarlocation=de" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "awattaraktiv=" /var/www/html/openWB/openwb.conf
then
	echo "awattaraktiv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "plz=" /var/www/html/openWB/openwb.conf
then
	echo "plz=36124" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pushbplug=" /var/www/html/openWB/openwb.conf
then
	echo "pushbplug=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrsmawebbox=" /var/www/html/openWB/openwb.conf
then
	echo "wrsmawebbox=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bootmodus=" /var/www/html/openWB/openwb.conf
then
	echo "bootmodus=3" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "httpll_w_url=" /var/www/html/openWB/openwb.conf
then
	  echo "httpll_w_url='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "httpll_kwh_url=" /var/www/html/openWB/openwb.conf
then
	  echo "httpll_kwh_url='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "httpll_a1_url=" /var/www/html/openWB/openwb.conf
then
	  echo "httpll_a1_url='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "httpll_a2_url=" /var/www/html/openWB/openwb.conf
then
	  echo "httpll_a2_url='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "httpll_a3_url=" /var/www/html/openWB/openwb.conf
then
	  echo "httpll_a3_url='http://url'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "clouduser=" /var/www/html/openWB/openwb.conf
then
	echo "clouduser=leer" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "cloudpw=" /var/www/html/openWB/openwb.conf
then
	echo "cloudpw=leer" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidakt=" /var/www/html/openWB/openwb.conf
then
	echo "rfidakt=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidsofort=" /var/www/html/openWB/openwb.conf
then
	echo "rfidsofort=000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidlp1start1=" /var/www/html/openWB/openwb.conf
then
	echo "rfidlp1start1=000" >> /var/www/html/openWB/openwb.conf
	echo "rfidlp1start2=000" >> /var/www/html/openWB/openwb.conf
	echo "rfidlp1start3=000" >> /var/www/html/openWB/openwb.conf
	echo "rfidlp2start1=000" >> /var/www/html/openWB/openwb.conf
	echo "rfidlp2start2=000" >> /var/www/html/openWB/openwb.conf
	echo "rfidlp2start3=000" >> /var/www/html/openWB/openwb.conf

fi
if ! grep -Fq "rfidstandby=" /var/www/html/openWB/openwb.conf
then
	echo "rfidstandby=000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidstop=" /var/www/html/openWB/openwb.conf
then
	echo "rfidstop=000" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidnurpv=" /var/www/html/openWB/openwb.conf
then
	echo "rfidnurpv=000" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidminpv=" /var/www/html/openWB/openwb.conf
then
	echo "rfidminpv=000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidsofort2=" /var/www/html/openWB/openwb.conf
then
	echo "rfidsofort2=000" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidstandby2=" /var/www/html/openWB/openwb.conf
then
	echo "rfidstandby2=000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidstop2=" /var/www/html/openWB/openwb.conf
then
	echo "rfidstop2=000" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidnurpv2=" /var/www/html/openWB/openwb.conf
then
	echo "rfidnurpv2=000" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidminpv2=" /var/www/html/openWB/openwb.conf
then
	echo "rfidminpv2=000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidsofort3=" /var/www/html/openWB/openwb.conf
then
	echo "rfidsofort3=000" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidstandby3=" /var/www/html/openWB/openwb.conf
then
	echo "rfidstandby3=000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidstop3=" /var/www/html/openWB/openwb.conf
then
	echo "rfidstop3=000" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidnurpv3=" /var/www/html/openWB/openwb.conf
then
	echo "rfidnurpv3=000" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidminpv3=" /var/www/html/openWB/openwb.conf
then
	echo "rfidminpv3=000" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "rfidlp1c1=" /var/www/html/openWB/openwb.conf
then
	echo "rfidlp1c1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidlp1c2=" /var/www/html/openWB/openwb.conf
then
	echo "rfidlp1c2=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidlp1c3=" /var/www/html/openWB/openwb.conf
then
	echo "rfidlp1c3=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidlp2c1=" /var/www/html/openWB/openwb.conf
then
	echo "rfidlp2c1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidlp2c2=" /var/www/html/openWB/openwb.conf
then
	echo "rfidlp2c2=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "rfidlp2c3=" /var/www/html/openWB/openwb.conf
then
	echo "rfidlp2c3=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wr_sdm120ip=" /var/www/html/openWB/openwb.conf
then
	echo "wr_sdm120ip=192.168.3.5" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wr_sdm120id=" /var/www/html/openWB/openwb.conf
then
	echo "wr_sdm120id=2" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "bezug_victronip=" /var/www/html/openWB/openwb.conf
then
	echo "bezug_victronip=192.168.15.3" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pushbsmarthome=" /var/www/html/openWB/openwb.conf
then
	echo "pushbsmarthome=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "graphsocdyn=" /var/www/html/openWB/openwb.conf
then
	echo "graphsocdyn=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ledsakt=" /var/www/html/openWB/openwb.conf
then
	echo "ledsakt=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "led0sofort=" /var/www/html/openWB/openwb.conf
then
	echo "led0sofort=aus" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "led0minpv=" /var/www/html/openWB/openwb.conf
then
	echo "led0minpv=aus" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "led0nurpv=" /var/www/html/openWB/openwb.conf
then
	echo "led0nurpv=aus" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "led0stop=" /var/www/html/openWB/openwb.conf
then
	echo "led0stop=aus" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "led0standby=" /var/www/html/openWB/openwb.conf
then
	echo "led0standby=aus" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "ledsofort=" /var/www/html/openWB/openwb.conf
then
	echo "ledsofort=aus" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ledminpv=" /var/www/html/openWB/openwb.conf
then
	echo "ledminpv=aus" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lednurpv=" /var/www/html/openWB/openwb.conf
then
	echo "lednurpv=aus" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ledstop=" /var/www/html/openWB/openwb.conf
then
	echo "ledstop=aus" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ledstandby=" /var/www/html/openWB/openwb.conf
then
	echo "ledstandby=aus" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displayconfigured=" /var/www/html/openWB/openwb.conf
then
	echo "displayconfigured=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displayaktiv=" /var/www/html/openWB/openwb.conf
then
	echo "displayaktiv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displaysleep=" /var/www/html/openWB/openwb.conf
then
	echo "displaysleep=60" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displayevumax=" /var/www/html/openWB/openwb.conf
then
	echo "displayevumax=5000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displaypvmax=" /var/www/html/openWB/openwb.conf
then
	echo "displaypvmax=10000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displayspeichermax=" /var/www/html/openWB/openwb.conf
then
	echo "displayspeichermax=3000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displayhausanzeigen=" /var/www/html/openWB/openwb.conf
then
	echo "displayhausanzeigen=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displayhausmax=" /var/www/html/openWB/openwb.conf
then
	echo "displayhausmax=5000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displaylp1max=" /var/www/html/openWB/openwb.conf
then
	echo "displaylp1max=22000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displaylp2max=" /var/www/html/openWB/openwb.conf
then
	echo "displaylp2max=22000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displaypinaktiv=" /var/www/html/openWB/openwb.conf
then
	echo "displaypinaktiv=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "displaypincode=" /var/www/html/openWB/openwb.conf
then
	echo "displaypincode=1234" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "settingspw=" /var/www/html/openWB/openwb.conf
then
	echo "settingspw='openwb'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "settingspwakt=" /var/www/html/openWB/openwb.conf
then
	echo "settingspwakt=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "netzabschaltunghz=" /var/www/html/openWB/openwb.conf
then
	echo "netzabschaltunghz=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "cpunterbrechunglp1=" /var/www/html/openWB/openwb.conf
then
	echo "cpunterbrechunglp1=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "cpunterbrechunglp2=" /var/www/html/openWB/openwb.conf
then
	echo "cpunterbrechunglp2=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_zerong_username=" /var/www/html/openWB/openwb.conf
then
	echo "soc_zerong_username=deine@email.com" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_zerong_password=" /var/www/html/openWB/openwb.conf
then
	echo "soc_zerong_password=daspasswort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_zerong_intervallladen=" /var/www/html/openWB/openwb.conf
then
	echo "soc_zerong_intervallladen=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_zerong_intervall=" /var/www/html/openWB/openwb.conf
then
	echo "soc_zerong_intervall=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_zeronglp2_username=" /var/www/html/openWB/openwb.conf
then
	echo "soc_zeronglp2_username=" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_zeronglp2_password=" /var/www/html/openWB/openwb.conf
then
	echo "soc_zeronglp2_password=daspasswort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_zeronglp2_intervallladen=" /var/www/html/openWB/openwb.conf
then
	echo "soc_zeronglp2_intervallladen=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_zeronglp2_intervall=" /var/www/html/openWB/openwb.conf
then
	echo "soc_zeronglp2_intervall=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "alphaessip=" /var/www/html/openWB/openwb.conf
then
	echo "alphaessip=192.168.193.31" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "solarview_hostname=" /var/www/html/openWB/openwb.conf
then
	echo "solarview_hostname=192.168.0.31" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "solarview_port=" /var/www/html/openWB/openwb.conf
then
	echo "solarview_port=80" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "discovergyuser=" /var/www/html/openWB/openwb.conf
then
	echo "discovergyuser=name@mail.de" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "discovergypass=" /var/www/html/openWB/openwb.conf
then
	echo "discovergypass=passwort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "discovergyevuid=" /var/www/html/openWB/openwb.conf
then
	echo "discovergyevuid=idesmeters" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "discovergypvid=" /var/www/html/openWB/openwb.conf
then
	echo "discovergypvid=idesmeters" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ksemip=" /var/www/html/openWB/openwb.conf
then
        echo "ksemip=ipdesmeters" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1moab=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1moab=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1mobis=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1mobis=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1diab=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1diab=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1dibis=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1dibis=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1miab=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1miab=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1mibis=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1mibis=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1doab=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1doab=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1dobis=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1dobis=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1frab=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1frab=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1frbis=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1frbis=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1sabis=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1sabis=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1soab=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1soab=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1sobis=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1sobis=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1saab=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1saab=06:00" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1moll=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1moll=13" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1dill=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1dill=13" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1mill=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1mill=13" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1doll=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1doll=13" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1frll=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1frll=13" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1sall=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1sall=13" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mollp1soll=" /var/www/html/openWB/openwb.conf
then
	echo "mollp1soll=13" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wryoulessip=" /var/www/html/openWB/openwb.conf
then
	echo "wryoulessip=192.168.0.3" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_audi_username=" /var/www/html/openWB/openwb.conf
then
	echo "soc_audi_username=demo@demo.de" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "soc_audi_passwort=" /var/www/html/openWB/openwb.conf
then
	echo "soc_audi_passwort=passwort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lgessv1ip=" /var/www/html/openWB/openwb.conf
then
	echo "lgessv1ip=youripaddress" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lgessv1pass=" /var/www/html/openWB/openwb.conf
then
	echo "lgessv1pass=regnum_as_default_password" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ess_api_ver=" /var/www/html/openWB/openwb.conf
then
	echo "ess_api_ver=01.2020" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "mpmlp4ip=" /var/www/html/openWB/openwb.conf
then
	echo "mpmlp4ip=192.168.193.54" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp5ip=192.168.193.55" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp6ip=192.168.193.56" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp7ip=192.168.193.57" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp8ip=192.168.193.58" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp4id=14" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp5id=15" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp6id=16" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp7id=17" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp8id=18" >> /var/www/html/openWB/openwb.conf
	echo "lastmanagementlp4=0" >> /var/www/html/openWB/openwb.conf
	echo "lastmanagementlp5=0" >> /var/www/html/openWB/openwb.conf
	echo "lastmanagementlp6=0" >> /var/www/html/openWB/openwb.conf
	echo "lastmanagementlp7=0" >> /var/www/html/openWB/openwb.conf
	echo "lastmanagementlp8=0" >> /var/www/html/openWB/openwb.conf
	echo "evseconlp4=ipevse" >> /var/www/html/openWB/openwb.conf
	echo "evseconlp5=ipevse" >> /var/www/html/openWB/openwb.conf
	echo "evseconlp6=ipevse" >> /var/www/html/openWB/openwb.conf
	echo "evseconlp7=ipevse" >> /var/www/html/openWB/openwb.conf
	echo "evseconlp8=ipevse" >> /var/www/html/openWB/openwb.conf
	echo "evseidlp4=24" >> /var/www/html/openWB/openwb.conf
	echo "evseidlp5=25" >> /var/www/html/openWB/openwb.conf
	echo "evseidlp6=26" >> /var/www/html/openWB/openwb.conf
	echo "evseidlp7=27" >> /var/www/html/openWB/openwb.conf
	echo "evseidlp8=28" >> /var/www/html/openWB/openwb.conf
	echo "evseiplp4=192.168.193.44" >> /var/www/html/openWB/openwb.conf
	echo "evseiplp5=192.168.193.45" >> /var/www/html/openWB/openwb.conf
	echo "evseiplp6=192.168.193.46" >> /var/www/html/openWB/openwb.conf
	echo "evseiplp7=192.168.193.47" >> /var/www/html/openWB/openwb.conf
	echo "evseiplp8=192.168.193.48" >> /var/www/html/openWB/openwb.conf
	echo "sofortlllp4=13" >> /var/www/html/openWB/openwb.conf
	echo "sofortlllp5=13" >> /var/www/html/openWB/openwb.conf
	echo "sofortlllp6=13" >> /var/www/html/openWB/openwb.conf
	echo "sofortlllp7=13" >> /var/www/html/openWB/openwb.conf
	echo "sofortlllp8=13" >> /var/www/html/openWB/openwb.conf
	echo "lademkwhlp4=10" >> /var/www/html/openWB/openwb.conf
	echo "lademkwhlp5=10" >> /var/www/html/openWB/openwb.conf
	echo "lademkwhlp6=10" >> /var/www/html/openWB/openwb.conf
	echo "lademkwhlp7=10" >> /var/www/html/openWB/openwb.conf
	echo "lademkwhlp8=10" >> /var/www/html/openWB/openwb.conf
	echo "durchslp4=20" >> /var/www/html/openWB/openwb.conf
	echo "durchslp5=20" >> /var/www/html/openWB/openwb.conf
	echo "durchslp6=20" >> /var/www/html/openWB/openwb.conf
	echo "durchslp7=20" >> /var/www/html/openWB/openwb.conf
	echo "durchslp8=20" >> /var/www/html/openWB/openwb.conf
	echo "evseidlp1=21" >> /var/www/html/openWB/openwb.conf
	echo "evseidlp2=22" >> /var/www/html/openWB/openwb.conf
	echo "evseidlp3=23" >> /var/www/html/openWB/openwb.conf
	echo "evseiplp1=192.168.193.41" >> /var/www/html/openWB/openwb.conf
	echo "evseiplp2=192.168.193.42" >> /var/www/html/openWB/openwb.conf
	echo "evseiplp3=192.168.193.43" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp1ip=192.168.193.51" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp2ip=192.168.193.52" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp3ip=192.168.193.53" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp1id=11" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp2id=12" >> /var/www/html/openWB/openwb.conf
	echo "mpmlp3id=13" >> /var/www/html/openWB/openwb.conf
	echo "lp4name=LP4" >> /var/www/html/openWB/openwb.conf
	echo "lp5name=LP5" >> /var/www/html/openWB/openwb.conf
	echo "lp6name=LP6" >> /var/www/html/openWB/openwb.conf
	echo "lp7name=LP7" >> /var/www/html/openWB/openwb.conf
	echo "lp8name=LP8" >> /var/www/html/openWB/openwb.conf
	echo "simplemode=0" >> /var/www/html/openWB/openwb.conf
	echo "lademstatlp4=01" >> /var/www/html/openWB/openwb.conf
	echo "lademstatlp5=0" >> /var/www/html/openWB/openwb.conf
	echo "lademstatlp6=0" >> /var/www/html/openWB/openwb.conf
	echo "lademstatlp7=0" >> /var/www/html/openWB/openwb.conf
	echo "lademstatlp8=0" >> /var/www/html/openWB/openwb.conf

fi
if ! grep -Fq "stopchargeafterdisclp1=" /var/www/html/openWB/openwb.conf
then
	echo "stopchargeafterdisclp1=0" >> /var/www/html/openWB/openwb.conf
	echo "stopchargeafterdisclp2=0" >> /var/www/html/openWB/openwb.conf
	echo "stopchargeafterdisclp3=0" >> /var/www/html/openWB/openwb.conf
	echo "stopchargeafterdisclp4=0" >> /var/www/html/openWB/openwb.conf
	echo "stopchargeafterdisclp5=0" >> /var/www/html/openWB/openwb.conf
	echo "stopchargeafterdisclp6=0" >> /var/www/html/openWB/openwb.conf
	echo "stopchargeafterdisclp7=0" >> /var/www/html/openWB/openwb.conf
	echo "stopchargeafterdisclp8=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "myrenault_userlp1=" /var/www/html/openWB/openwb.conf
then
	echo "myrenault_userlp1=Benutzername" >> /var/www/html/openWB/openwb.conf
	echo "myrenault_passlp1=Passwort" >> /var/www/html/openWB/openwb.conf
	echo "myrenault_locationlp1=de_DE" >> /var/www/html/openWB/openwb.conf
	echo "myrenault_countrylp1=DE" >> /var/www/html/openWB/openwb.conf
	echo "myrenault_userlp2=Benutzername" >> /var/www/html/openWB/openwb.conf
	echo "myrenault_passlp2=Passwort" >> /var/www/html/openWB/openwb.conf
	echo "myrenault_locationlp2=de_DE" >> /var/www/html/openWB/openwb.conf
	echo "myrenault_countrylp2=DE" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "evukitversion=" /var/www/html/openWB/openwb.conf
then
	echo "evukitversion=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pvkitversion=" /var/www/html/openWB/openwb.conf
then
	echo "pvkitversion=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "wrsunwayspw=" /var/www/html/openWB/openwb.conf
then
	echo "wrsunwayspw=passwort" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "e3dcextprod=" /var/www/html/openWB/openwb.conf
then
	echo "e3dcextprod=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "schieflastmaxa=" /var/www/html/openWB/openwb.conf
then
	echo "schieflastmaxa=20" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "schieflastaktiv=" /var/www/html/openWB/openwb.conf
then
	echo "schieflastaktiv=0" >> /var/www/html/openWB/openwb.conf
fi

if ! grep -Fq "wrsunwaysip=" /var/www/html/openWB/openwb.conf
then
	echo "wrsunwaysip=192.168.0.10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "lastmmaxw=" /var/www/html/openWB/openwb.conf
then
	echo "lastmmaxw=44000" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "slavemode=" /var/www/html/openWB/openwb.conf
then
	echo "slavemode=0" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "slaveModeUseLastChargingPhase=" /var/www/html/openWB/openwb.conf
then
	echo "slaveModeUseLastChargingPhase=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "slaveModeSlowRamping=" /var/www/html/openWB/openwb.conf
then
	echo "slaveModeSlowRamping=1" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "slaveModeMinimumAdjustmentInterval=" /var/www/html/openWB/openwb.conf
then
	echo "slaveModeMinimumAdjustmentInterval=15" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "solarworld_emanagerip=" /var/www/html/openWB/openwb.conf
then
	echo "solarworld_emanagerip=192.192.192.192" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "femsip=" /var/www/html/openWB/openwb.conf
then
	echo "femsip=192.168.1.23" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pv2wattmodul=" /var/www/html/openWB/openwb.conf
then
	echo "pv2wattmodul=none" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "pv2ip=" /var/www/html/openWB/openwb.conf
then
	echo "pv2ip=none" >> /var/www/html/openWB/openwb.conf
	echo "pv2id=none" >> /var/www/html/openWB/openwb.conf
	echo "pv2user=none" >> /var/www/html/openWB/openwb.conf
	echo "pv2pass=none" >> /var/www/html/openWB/openwb.conf


fi
if ! grep -Fq "soc_bluelink_email=" /var/www/html/openWB/openwb.conf
then
	echo "soc_bluelink_email=mail@mail.de" >> /var/www/html/openWB/openwb.conf
	echo "soc_bluelink_password=passwort" >> /var/www/html/openWB/openwb.conf
	echo "soc_bluelink_pin=1111" >> /var/www/html/openWB/openwb.conf
	echo "soc_bluelink_interval=30" >> /var/www/html/openWB/openwb.conf

fi
sudo kill $(ps aux |grep '[s]marthomehandler.py' | awk '{print $2}')
if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/smarthomehandler.py" > /dev/null
then
	echo "test" > /dev/null
else
	python3 /var/www/html/openWB/runs/smarthomehandler.py &
fi
sudo kill $(ps aux |grep '[m]qttsub.py' | awk '{print $2}')
if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/mqttsub.py" > /dev/null
then
	echo "test" > /dev/null
else
	python3 /var/www/html/openWB/runs/mqttsub.py &
fi

crontab -l -u pi > /var/www/html/openWB/ramdisk/tmpcrontab
if grep -Fq "lade.log" /var/www/html/openWB/ramdisk/tmpcrontab
then
	echo "crontab modified"
	sed -i '/lade.log/d' /var/www/html/openWB/ramdisk/tmpcrontab
	echo "* * * * * /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1" >> /var/www/html/openWB/ramdisk/tmpcrontab
	cat /var/www/html/openWB/ramdisk/tmpcrontab | crontab -u pi -
fi
sudo crontab -l > /var/www/html/openWB/ramdisk/tmprootcrontab
if grep -Fq "atreboot.sh" /var/www/html/openWB/ramdisk/tmprootcrontab
then
echo "executed"
sed -i '/atreboot.sh/d' /var/www/html/openWB/ramdisk/tmprootcrontab
cat /var/www/html/openWB/ramdisk/tmprootcrontab | sudo crontab -
fi
ethstate=$(</sys/class/net/eth0/carrier)
if (( ethstate == 1 )); then
	sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 up
else
	sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 up
fi

if  grep -Fxq "AllowOverride" /etc/apache2/sites-available/000-default.conf
then
	echo "...ok"
else
	sudo cp /var/www/html/openWB/web/tools/000-default.conf /etc/apache2/sites-available/
	echo "...changed"
fi
if ! sudo grep -Fq "cronnightly.sh" /var/spool/cron/crontabs/pi
then
	(crontab -l -u pi ; echo "1 0 * * * /var/www/html/openWB/runs/cronnightly.sh >> /var/log/openWB.log 2>&1")| crontab -u pi -
fi

if ! sudo grep -Fq "cron5min.sh" /var/spool/cron/crontabs/pi
then
	(crontab -l -u pi ; echo "*/5 * * * * /var/www/html/openWB/runs/cron5min.sh >> /var/log/openWB.log 2>&1")| crontab -u pi -
fi

if ! sudo grep -Fq "atreboot.sh" /var/spool/cron/crontabs/pi
then
	(crontab -l -u pi ; echo "@reboot /var/www/html/openWB/runs/atreboot.sh >> /var/log/openWB.log 2>&1")| crontab -u pi -
fi
if python -c "import evdev" &> /dev/null; then
	echo 'evdev installed...'
else
	sudo pip install evdev
fi
if ! [ -x "$(command -v sshpass)" ];then
	apt-get -qq update
	sleep 1
	apt-get -qq install sshpass
fi
if [ $(dpkg-query -W -f='${Status}' php-gd 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	sudo apt-get -qq update
	sleep 1
	sudo apt-get -qq install -y php-gd
	sleep 1
	sudo apt-get -qq install -y php7.0-xml

fi

. /var/www/html/openWB/openwb.conf
/var/www/html/openWB/runs/transferladelog.sh
if (( ledsakt == 1 )); then
	sudo python /var/www/html/openWB/runs/leds.py startup
fi
sudo cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime
if [ ! -f /etc/mosquitto/mosquitto.conf ]; then
	sudo apt-get update
	sudo apt-get -qq install -y mosquitto mosquitto-clients
	sudo service mosquitto restart
fi
if [ ! -f /etc/mosquitto/conf.d/openwb.conf ]; then
	sudo cp /var/www/html/openWB/web/files/mosquitto.conf /etc/mosquitto/conf.d/openwb.conf
	sudo service mosquitto restart
fi
if python3 -c "import paho.mqtt.publish as publish" &> /dev/null; then
	echo 'mqtt installed...'
else
	sudo apt-get -qq install -y python3-pip
	sudo pip3 install paho-mqtt
fi
uuid=$(</sys/class/net/eth0/address)
owbv=$(</var/www/html/openWB/web/version)
curl -d "update="$releasetrain$uuid"vers"$owbv"" -H "Content-Type: application/x-www-form-urlencoded" -X POST https://openwb.de/tools/update.php
echo $verbraucher1_name > /var/www/html/openWB/ramdisk/verbraucher1_name
echo $verbraucher2_name > /var/www/html/openWB/ramdisk/verbraucher2_name


echo "" > /var/www/html/openWB/ramdisk/lastregelungaktiv
echo "" > /var/www/html/openWB/ramdisk/mqttlastregelungaktiv
chmod 777 /var/www/html/openWB/ramdisk/mqttlastregelungaktiv

#if [ $(dpkg-query -W -f='${Status}' php-curl 2>/dev/null | grep -c "ok installed") -eq 0 ];
#then
#	  sudo apt-get update
#	  sudo apt-get -qq install -y php-curl
#  fi
(sleep 10; echo 1 > /var/www/html/openWB/ramdisk/reloaddisplay) &
ip route get 1 | awk '{print $NF;exit}' > /var/www/html/openWB/ramdisk/ipaddress
curl -s https://raw.githubusercontent.com/snaptec/openWB/master/web/version > /var/www/html/openWB/ramdisk/vnightly
curl -s https://raw.githubusercontent.com/snaptec/openWB/beta/web/version > /var/www/html/openWB/ramdisk/vbeta
curl -s https://raw.githubusercontent.com/snaptec/openWB/stable/web/version > /var/www/html/openWB/ramdisk/vstable
sudo git -C /var/www/html/openWB show --pretty='format:%ci [%h]' | head -n1 > /var/www/html/openWB/web/lastcommit
for i in $(seq 1 9);
do
	configured=$(timeout 2 mosquitto_sub -C 1 -t openWB/config/get/SmartHome/Devices/$i/device_configured)
	if ! [[ "$configured" == 0 || "$configured" == 1 ]]; then
		mosquitto_pub -r -t openWB/config/get/SmartHome/Devices/$i/device_configured -m "0"
	fi
done
mosquitto_pub -r -t openWB/global/awattar/pricelist -m " "
mosquitto_pub -r -t openWB/graph/boolDisplayLiveGraph -m "1"
mosquitto_pub -t openWB/strLastmanagementActive -r -m " "
mosquitto_pub -t openWB/lp/1/W -r -m "0"
mosquitto_pub -t openWB/lp/2/W -r -m "0"
mosquitto_pub -t openWB/lp/3/W -r -m "0"
mosquitto_pub -t openWB/lp/1/boolChargePointConfigured -r -m "1"
rm -rf /var/www/html/openWB/web/themes/dark19_01
(sleep 10; mosquitto_pub -t openWB/set/ChargeMode -r -m $bootmodus) &
(sleep 10; mosquitto_pub -t openWB/global/ChargeMode -r -m $bootmodus) &
echo " " > /var/www/html/openWB/ramdisk/lastregelungaktiv
chmod 777 /var/www/html/openWB/ramdisk/lastregelungaktiv
chmod 777 /var/www/html/openWB/ramdisk/smarthome.log
chmod 777 /var/www/html/openWB/ramdisk/smarthomehandlerloglevel
echo 0 > /var/www/html/openWB/ramdisk/bootinprogress
echo 0 > /var/www/html/openWB/ramdisk/updateinprogress
