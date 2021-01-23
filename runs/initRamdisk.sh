#!/bin/bash
# Ramdisk mit initialen Werten befüllen nach Neustart

initRamdisk(){
	RamdiskPath="/var/www/html/openWB/ramdisk"
	echo "Initializing Ramdisk $RamdiskPath"

	# Logfiles erstellen
	ln -s /var/log/openWB.log $RamdiskPath/openWB.log
	echo "**** REBOOT ****" > $RamdiskPath/mqtt.log
	echo "**** REBOOT ****" > $RamdiskPath/ladestatus.log
	echo "**** REBOOT ****" > $RamdiskPath/soc.log
	echo "**** REBOOT ****" > $RamdiskPath/rfid.log
	echo "**** REBOOT ****" > $RamdiskPath/nurpv.log
	echo "**** REBOOT ****" > $RamdiskPath/cleanup.log
	echo "**** REBOOT ****" > $RamdiskPath/smarthome.log

	echo 0 > $RamdiskPath/randomSleepValue
	echo 0 > $RamdiskPath/rfidlp1
	echo 0 > $RamdiskPath/rfidlp2
	echo 0 > $RamdiskPath/rfidlp3
	echo 0 > $RamdiskPath/rfidlp4
	echo 0 > $RamdiskPath/rfidlp5
	echo 0 > $RamdiskPath/rfidlp6
	echo 0 > $RamdiskPath/rfidlp7
	echo 0 > $RamdiskPath/rfidlp8
	echo 1 > $RamdiskPath/bootinprogress
	echo 0 > $RamdiskPath/nurpv70dynstatus
	echo 0 > $RamdiskPath/cpulp1counter
	echo 0 > $RamdiskPath/tmpsoc
	echo 0 > $RamdiskPath/tmpsoc1
	echo 0 > $RamdiskPath/lp1phasen
	echo 0 > $RamdiskPath/lp2phasen
	echo 0 > $RamdiskPath/lp3phasen
	echo 0 > $RamdiskPath/lp4phasen
	echo 0 > $RamdiskPath/lp5phasen
	echo 0 > $RamdiskPath/lp6phasen
	echo 0 > $RamdiskPath/lp7phasen
	echo 0 > $RamdiskPath/lp8phasen
	echo 0 > $RamdiskPath/AllowedTotalCurrentPerPhase
	echo 0 > $RamdiskPath/ChargingVehiclesOnL1
	echo 0 > $RamdiskPath/ChargingVehiclesOnL2
	echo 0 > $RamdiskPath/ChargingVehiclesOnL3
	echo 0 > $RamdiskPath/TotalCurrentConsumptionOnL1
	echo 0 > $RamdiskPath/TotalCurrentConsumptionOnL2
	echo 0 > $RamdiskPath/TotalCurrentConsumptionOnL3
	echo 0 > $RamdiskPath/autolocktimer
	echo 0 > $RamdiskPath/ipaddress
	echo 0 > $RamdiskPath/etproviderprice
	echo 1 > $RamdiskPath/mqttetproviderprice
	echo 0 > $RamdiskPath/etprovidermaxprice
	echo 1 > $RamdiskPath/mqttetprovidermaxprice
	echo 0 > $RamdiskPath/mqttdurchslp2
	echo 0 > $RamdiskPath/mqttdurchslp3
	echo 1 > $RamdiskPath/mqttsoc1
	echo 1 > $RamdiskPath/lp1enabled
	echo 0 > $RamdiskPath/device1_wh
	echo 0 > $RamdiskPath/device2_wh
	echo 0 > $RamdiskPath/device3_wh
	echo 0 > $RamdiskPath/device4_wh
	echo 0 > $RamdiskPath/device5_wh
	echo 0 > $RamdiskPath/device6_wh
	echo 0 > $RamdiskPath/device7_wh
	echo 0 > $RamdiskPath/device8_wh
	echo 0 > $RamdiskPath/device9_wh
	echo 0 > $RamdiskPath/device1_temp0
	echo 0 > $RamdiskPath/device1_temp1
	echo 0 > $RamdiskPath/device1_temp2
	echo 0 > $RamdiskPath/device2_temp0
	echo 0 > $RamdiskPath/device2_temp1
	echo 0 > $RamdiskPath/device2_temp2
	echo 1 > $RamdiskPath/lp2enabled
	echo 1 > $RamdiskPath/lp3enabled
	echo 1 > $RamdiskPath/lp4enabled
	echo 1 > $RamdiskPath/lp5enabled
	echo 1 > $RamdiskPath/lp6enabled
	echo 1 > $RamdiskPath/lp7enabled
	echo 1 > $RamdiskPath/lp8enabled
	echo 0 > $RamdiskPath/schieflast
	echo 0 > $RamdiskPath/renewmqtt
	echo 0 > $RamdiskPath/netzschutz
	echo 0 > $RamdiskPath/hausverbrauch
	echo 0 > $RamdiskPath/blockall
	echo 0 > $RamdiskPath/llsoll
	echo 0 > $RamdiskPath/llsolllp4
	echo 0 > $RamdiskPath/llsolllp5
	echo 0 > $RamdiskPath/llsolllp6
	echo 0 > $RamdiskPath/llsolllp7
	echo 0 > $RamdiskPath/llsolllp8
	echo 0 > $RamdiskPath/ladungaktivlp1
	echo 0 > $RamdiskPath/ladungaktivlp2
	echo 0 > $RamdiskPath/ladungaktivlp3
	echo 0 > $RamdiskPath/plugstat
	echo 0 > $RamdiskPath/plugstats1
	echo 0 > $RamdiskPath/chargestat
	echo 0 > $RamdiskPath/chargestats1
	echo 0 > $RamdiskPath/chargestatlp3
	echo 0 > $RamdiskPath/plugstatlp3
	echo 0 > $RamdiskPath/plugstatlp4
	echo 0 > $RamdiskPath/plugstatlp5
	echo 0 > $RamdiskPath/plugstatlp6
	echo 0 > $RamdiskPath/plugstatlp7
	echo 0 > $RamdiskPath/plugstatlp8
	echo 0 > $RamdiskPath/chargestatlp4
	echo 0 > $RamdiskPath/chargestatlp5
	echo 0 > $RamdiskPath/chargestatlp6
	echo 0 > $RamdiskPath/chargestatlp7
	echo 0 > $RamdiskPath/chargestatlp8
	echo 0 > $RamdiskPath/verbraucher1vorhanden
	echo 0 > $RamdiskPath/verbraucher1_watt
	echo 0 > $RamdiskPath/verbraucher1_wh
	echo 0 > $RamdiskPath/verbraucher1_whe
	echo 0 > $RamdiskPath/verbraucher2vorhanden
	echo 0 > $RamdiskPath/verbraucher2_watt
	echo 0 > $RamdiskPath/verbraucher2_wh
	echo 0 > $RamdiskPath/verbraucher2_whe
	echo 0 > $RamdiskPath/verbraucher3vorhanden
	echo 0 > $RamdiskPath/verbraucher3_watt
	echo 0 > $RamdiskPath/verbraucher3_wh
	echo 0 > $RamdiskPath/evseausgelesen
	echo 0 > $RamdiskPath/progevsedinlp1
	echo 0 > $RamdiskPath/progevsedinlp2
	echo 0 > $RamdiskPath/progevsedinlp12000
	echo 0 > $RamdiskPath/progevsedinlp12007
	echo 0 > $RamdiskPath/progevsedinlp22000
	echo 0 > $RamdiskPath/progevsedinlp22007
	echo 0 > $RamdiskPath/readtag
	echo 0 > $RamdiskPath/rfidlp1
	echo 0 > $RamdiskPath/mqttrfidlp1
	echo 0 > $RamdiskPath/rfidlp2
	echo 0 > $RamdiskPath/mqttrfidlp2
	echo 0 > $RamdiskPath/rfidlasttag
	echo 0 > $RamdiskPath/mqttrfidlasttag
	echo 0 > $RamdiskPath/ledstatus
	echo 1 > $RamdiskPath/execdisplay
	echo 0 > $RamdiskPath/pluggedladungbishergeladen
	echo 0 > $RamdiskPath/pluggedtimer1
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp2
	echo 0 > $RamdiskPath/pluggedtimer2
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp3
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp4
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp5
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp6
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp7
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp8
	echo 1 > $RamdiskPath/mqttlademkwhs1
	echo 1 > $RamdiskPath/mqttlademkwhs2
	echo 0 > $RamdiskPath/mqttlastladestatus
	echo 0 > $RamdiskPath/mqttlastplugstat
	echo 0 > $RamdiskPath/mqttlastchargestat
	echo 0 > $RamdiskPath/mqttlastchargestats1
	echo 0 > $RamdiskPath/mqttlastplugstats1
	echo 2 > $RamdiskPath/mqttspeichervorhanden
	echo 0 > $RamdiskPath/mqttpvvorhanden
	echo 3 > $RamdiskPath/mqttspeichersoc
	echo 2 > $RamdiskPath/mqttspeicherleistung
	echo 0 > $RamdiskPath/mqttladeleistungs1
	echo 0 > $RamdiskPath/mqttladeleistungs2
	echo 0 > $RamdiskPath/mqttladeleistunglp1
	echo 3 > $RamdiskPath/mqttlastmanagement
	echo 3 > $RamdiskPath/mqttlastmanagements2
	echo 3 > $RamdiskPath/mqttlastmanagementlp4
	echo 3 > $RamdiskPath/mqttlastmanagementlp5
	echo 3 > $RamdiskPath/mqttlastmanagementlp6
	echo 3 > $RamdiskPath/mqttlastmanagementlp7
	echo 3 > $RamdiskPath/mqttlastmanagementlp8
	echo 0 > $RamdiskPath/autolockstatuslp1
	echo 0 > $RamdiskPath/autolockstatuslp2
	echo 0 > $RamdiskPath/autolockstatuslp3
	echo 0 > $RamdiskPath/autolockstatuslp4
	echo 0 > $RamdiskPath/autolockstatuslp5
	echo 0 > $RamdiskPath/autolockstatuslp6
	echo 0 > $RamdiskPath/autolockstatuslp7
	echo 0 > $RamdiskPath/autolockstatuslp8
	echo 0 > $RamdiskPath/autolockconfiguredlp1
	echo 0 > $RamdiskPath/autolockconfiguredlp2
	echo 0 > $RamdiskPath/autolockconfiguredlp3
	echo 0 > $RamdiskPath/autolockconfiguredlp4
	echo 0 > $RamdiskPath/autolockconfiguredlp5
	echo 0 > $RamdiskPath/autolockconfiguredlp6
	echo 0 > $RamdiskPath/autolockconfiguredlp7
	echo 0 > $RamdiskPath/autolockconfiguredlp8
	echo 1 > $RamdiskPath/mqttautolockstatuslp1
	echo 1 > $RamdiskPath/mqttautolockstatuslp2
	echo 1 > $RamdiskPath/mqttautolockstatuslp3
	echo 1 > $RamdiskPath/mqttautolockstatuslp4
	echo 1 > $RamdiskPath/mqttautolockstatuslp5
	echo 1 > $RamdiskPath/mqttautolockstatuslp6
	echo 1 > $RamdiskPath/mqttautolockstatuslp7
	echo 1 > $RamdiskPath/mqttautolockstatuslp8
	echo 1 > $RamdiskPath/mqttautolockconfiguredlp1
	echo 1 > $RamdiskPath/mqttautolockconfiguredlp2
	echo 1 > $RamdiskPath/mqttautolockconfiguredlp3
	echo 1 > $RamdiskPath/mqttautolockconfiguredlp4
	echo 1 > $RamdiskPath/mqttautolockconfiguredlp5
	echo 1 > $RamdiskPath/mqttautolockconfiguredlp6
	echo 1 > $RamdiskPath/mqttautolockconfiguredlp7
	echo 1 > $RamdiskPath/mqttautolockconfiguredlp8
	echo 0 > $RamdiskPath/smarthome_device_manual_1
	echo 0 > $RamdiskPath/smarthome_device_manual_2
	echo 0 > $RamdiskPath/smarthome_device_manual_3
	echo 0 > $RamdiskPath/smarthome_device_manual_4
	echo 0 > $RamdiskPath/smarthome_device_manual_5
	echo 0 > $RamdiskPath/smarthome_device_manual_6
	echo 0 > $RamdiskPath/smarthome_device_manual_7
	echo 0 > $RamdiskPath/smarthome_device_manual_8
	echo 0 > $RamdiskPath/smarthome_device_manual_9
	echo 0 > $RamdiskPath/devicetotal_watt
	touch $RamdiskPath/wattbezug
	echo 10 > $RamdiskPath/lp1sofortll
	echo 10 > $RamdiskPath/lp2sofortll
	echo 10 > $RamdiskPath/lp3sofortll
	echo 10 > $RamdiskPath/lp4sofortll
	echo 10 > $RamdiskPath/lp5sofortll
	echo 10 > $RamdiskPath/lp6sofortll
	echo 10 > $RamdiskPath/lp7sofortll
	echo 10 > $RamdiskPath/lp8sofortll
	echo 0 > $RamdiskPath/wattbezug
	echo 0 > $RamdiskPath/hook1akt
	echo 0 > $RamdiskPath/hook2akt
	echo 0 > $RamdiskPath/hook3akt
	echo 0 > $RamdiskPath/urcounter
	echo 0 > $RamdiskPath/uhcounter
	echo 1 > $RamdiskPath/mqttllsolls1
	echo 1 > $RamdiskPath/mqttllsolls2
	echo 0 > $RamdiskPath/lla1lp4
	echo 0 > $RamdiskPath/lla2lp4
	echo 0 > $RamdiskPath/lla3lp4
	echo 0 > $RamdiskPath/llv1lp4
	echo 0 > $RamdiskPath/llv2lp4
	echo 0 > $RamdiskPath/llv3lp4
	echo 0 > $RamdiskPath/ladeleistunglp4
	echo 0 > $RamdiskPath/llkwhlp4
	echo 0 > $RamdiskPath/lla1lp5
	echo 0 > $RamdiskPath/lla2lp5
	echo 0 > $RamdiskPath/lla3lp5
	echo 0 > $RamdiskPath/llv1lp5
	echo 0 > $RamdiskPath/llv2lp5
	echo 0 > $RamdiskPath/llv3lp5
	echo 0 > $RamdiskPath/ladeleistunglp5
	echo 0 > $RamdiskPath/llkwhlp5
	echo 0 > $RamdiskPath/lla1lp6
	echo 0 > $RamdiskPath/lla2lp6
	echo 0 > $RamdiskPath/lla3lp6
	echo 0 > $RamdiskPath/llv1lp6
	echo 0 > $RamdiskPath/llv2lp6
	echo 0 > $RamdiskPath/llv3lp6
	echo 0 > $RamdiskPath/ladeleistunglp6
	echo 0 > $RamdiskPath/llkwhlp6
	echo 0 > $RamdiskPath/lla1lp7
	echo 0 > $RamdiskPath/lla2lp7
	echo 0 > $RamdiskPath/lla3lp7
	echo 0 > $RamdiskPath/llv1lp7
	echo 0 > $RamdiskPath/llv2lp7
	echo 0 > $RamdiskPath/llv3lp7
	echo 0 > $RamdiskPath/ladeleistunglp7
	echo 0 > $RamdiskPath/llkwhlp7
	echo 0 > $RamdiskPath/lla1lp8
	echo 0 > $RamdiskPath/lla2lp8
	echo 0 > $RamdiskPath/lla3lp8
	echo 0 > $RamdiskPath/llv1lp8
	echo 0 > $RamdiskPath/llv2lp8
	echo 0 > $RamdiskPath/llv3lp8
	echo 0 > $RamdiskPath/ladeleistunglp8
	echo 0 > $RamdiskPath/llkwhlp8
	echo 0 > $RamdiskPath/ladestatuslp4
	echo 0 > $RamdiskPath/ladestatuslp5
	echo 0 > $RamdiskPath/ladestatuslp6
	echo 0 > $RamdiskPath/ladestatuslp7
	echo 0 > $RamdiskPath/ladestatuslp8
	touch $RamdiskPath/ladestatus
	touch $RamdiskPath/lademodus
	touch $RamdiskPath/llaktuell
	touch $RamdiskPath/llaktuells1
	echo 0 > $RamdiskPath/boolstopchargeafterdisclp1
	echo 0 > $RamdiskPath/boolstopchargeafterdisclp2
	echo 0 > $RamdiskPath/boolstopchargeafterdisclp3
	echo 0 > $RamdiskPath/boolstopchargeafterdisclp4
	echo 0 > $RamdiskPath/boolstopchargeafterdisclp5
	echo 0 > $RamdiskPath/boolstopchargeafterdisclp6
	echo 0 > $RamdiskPath/boolstopchargeafterdisclp7
	echo 0 > $RamdiskPath/boolstopchargeafterdisclp8
	echo 0 > $RamdiskPath/pv2watt
	echo 0 > $RamdiskPath/pv2kwh
	echo 0 > $RamdiskPath/pv2a1
	echo 0 > $RamdiskPath/pv2a2
	echo 0 > $RamdiskPath/pv2a3
	echo 0 > $RamdiskPath/pvvorhanden
	echo 0 > $RamdiskPath/pv1watt
	echo 0 > $RamdiskPath/pv2watt
	# Gesamtleistung AC PV-Module WR 1 + 2
	touch $RamdiskPath/pvwatt
	echo 0 > $RamdiskPath/pvwatt
	# Leistung AC PV-Module WR 1
	touch $RamdiskPath/pvwatt1
	echo 0 > $RamdiskPath/pvwatt1
	# Leistung AC PV-Module WR 2
	touch $RamdiskPath/pvwatt2
	echo 0 > $RamdiskPath/pvwatt2
	# Gesamtertrag in Wattstunden WR 1 + 2
	touch $RamdiskPath/pvkwh
	echo 0 > $RamdiskPath/pvkwh
	# Gesamtertrag in Kilowattstunden WR 1 + 2
	touch $RamdiskPath/pvkwhk
	echo 0 > $RamdiskPath/pvkwhk
	# Tagesertrag in Kilowattstunden WR 1 + 2
	touch $RamdiskPath/daily_pvkwhk
	echo 0 > $RamdiskPath/daily_pvkwhk
	# Monatsertrag in Kilowattstunden WR 1 + 2
	touch $RamdiskPath/monthly_pvkwhk
	echo 0 > $RamdiskPath/monthly_pvkwhk
	# Jahresertrag in Kilowattstunden WR 1 + 2
	touch $RamdiskPath/yearly_pvkwhk
	echo 0 > $RamdiskPath/yearly_pvkwhk
	# Gesamtertrag in Kilowattstunden WR 1
	touch $RamdiskPath/pvkwhk1
	echo 0 > $RamdiskPath/pvkwhk1
	# Tagesertrag in Kilowattstunden WR 1
	touch $RamdiskPath/daily_pvkwhk1
	echo 0 > $RamdiskPath/daily_pvkwhk1
	# Monatsertrag in Kilowattstunden WR 1
	touch $RamdiskPath/monthly_pvkwhk1
	echo 0 > $RamdiskPath/monthly_pvkwhk1
	# Jahresertrag in Kilowattstunden WR 1
	touch $RamdiskPath/yearly_pvkwhk1
	echo 0 > $RamdiskPath/yearly_pvkwhk1
	# Gesamtertrag in Kilowattstunden WR 2
	touch $RamdiskPath/pvkwhk2
	echo 0 > $RamdiskPath/pvkwhk2
	# Tagesertrag in Kilowattstunden WR 2
	touch $RamdiskPath/daily_pvkwhk2
	echo 0 > $RamdiskPath/daily_pvkwhk2
	# Monatsertrag in Kilowattstunden WR 2
	touch $RamdiskPath/monthly_pvkwhk2
	echo 0 > $RamdiskPath/monthly_pvkwhk2
	# Jahresertrag in Kilowattstunden WR 2
	touch $RamdiskPath/yearly_pvkwhk2
	echo 0 > $RamdiskPath/yearly_pvkwhk2
	# SoC Speicher am WR 1
	touch $RamdiskPath/speichersoc
	echo 0 > $RamdiskPath/speichersoc
	# SoC Speicher am WR 2
	touch $RamdiskPath/speichersoc2
	echo 0 > $RamdiskPath/speichersoc2
	# Gesamtleistung AC Speicher WR 1 + 2
	touch $RamdiskPath/speicherleistung
	echo 0 > $RamdiskPath/speicherleistung
	# Leistung AC Speicher WR 1
	touch $RamdiskPath/speicherleistung1
	echo 0 > $RamdiskPath/speicherleistung1
	# Leistung AC Speicher WR 2
	touch $RamdiskPath/speicherleistung2
	echo 0 > $RamdiskPath/speicherleistung2

	touch $RamdiskPath/soc
	touch $RamdiskPath/soc1
	touch $RamdiskPath/lla1
	touch $RamdiskPath/lla2
	touch $RamdiskPath/lla3
	touch $RamdiskPath/llkombiniert
	touch $RamdiskPath/llas11
	touch $RamdiskPath/llas12
	touch $RamdiskPath/llas13
	touch $RamdiskPath/llas21
	touch $RamdiskPath/llas22
	touch $RamdiskPath/llas23
	echo 0 > $RamdiskPath/llas21
	echo 0 > $RamdiskPath/llas22
	echo 0 > $RamdiskPath/llas23
	touch $RamdiskPath/llkwh
	touch $RamdiskPath/llkwhs1
	touch $RamdiskPath/einspeisungkwh
	touch $RamdiskPath/bezugkwh
	touch $RamdiskPath/llkwhs2
	touch $RamdiskPath/speicher
	touch $RamdiskPath/nachtladenstate
	touch $RamdiskPath/nachtladenstates1
	touch $RamdiskPath/zielladenkorrektura

	# temporäre Zwischenspeicher für z. B. Kostal Plenticore, da
	# bei Anschluss von Speicher und Energiemanager direkt am WR
	# alle Werte im Modul des Wechselrichters aus den Registern
	# gelesen werden, um einen zeitlich zusammenhängenden Datensatz
	# zu bekommen. Im jeweiligen Modul Speicher/Bezug werden
	# die Werte dann in die ramdisk für die weitere globale
	# Verarbeitung geschrieben.
	# Bezug/Einspeisung
	touch $RamdiskPath/temp_wattbezug
	echo 0 > $RamdiskPath/temp_wattbezug
	# Gesamte AC-Leistung des Speichers am WR 1 + 2
	touch $RamdiskPath/temp_speicherleistung
	echo 0 > $RamdiskPath/temp_peicherleistung
	# AC-Leistung des Speichers am WR 1
	touch $RamdiskPath/temp_speicherleistung1
	echo 0 > $RamdiskPath/temp_peicherleistung1
	# AC-Leistung des Speichers am WR 2
	touch $RamdiskPath/temp_speicherleistung2
	echo 0 > $RamdiskPath/temp_peicherleistung2
	# SoC des Speichers am WR 1
	touch $RamdiskPath/temp_speichersoc
	echo 0 > $RamdiskPath/temp_speichersoc
	# Strom auf den jeweiligen Phasen
	touch $RamdiskPath/temp_bezuga1
	echo 0 > $RamdiskPath/temp_bezuga1
	touch $RamdiskPath/temp_bezuga2
	echo 0 > $RamdiskPath/temp_bezuga2
	touch $RamdiskPath/temp_bezuga3
	echo 0 > $RamdiskPath/temp_bezuga3
	# Netzfrequenz
	touch $RamdiskPath/temp_evuhz
	echo 0 > $RamdiskPath/temp_evuhz
	# Leistung auf den jeweiligen Phasen
	touch $RamdiskPath/temp_bezugw1
	echo 0 > $RamdiskPath/temp_bezugw1
	touch $RamdiskPath/temp_bezugw2
	echo 0 > $RamdiskPath/temp_bezugw2
	touch $RamdiskPath/temp_bezugw3
	echo 0 > $RamdiskPath/temp_bezugw3
	# Spannung auf den jeweiligen Phasen
	touch $RamdiskPath/temp_evuv1
	echo 0 > $RamdiskPath/temp_evuv1
	touch $RamdiskPath/temp_evuv2
	echo 0 > $RamdiskPath/temp_evuv2
	touch $RamdiskPath/temp_evuv3
	echo 0 > $RamdiskPath/temp_evuv3
	# Wirkfaktor, wird aus historischen Gründen je Phase geschrieben
	touch $RamdiskPath/temp_evupf1
	echo 0 > $RamdiskPath/temp_evupf1
	touch $RamdiskPath/temp_evupf2
	echo 0 > $RamdiskPath/temp_evupf2
	touch $RamdiskPath/temp_evupf3
	echo 0 > $RamdiskPath/temp_evupf3

	echo 0 > $RamdiskPath/zielladenkorrektura
	echo 0 > $RamdiskPath/nachtladenstate
	echo 0 > $RamdiskPath/nachtladen2state
	echo 0 > $RamdiskPath/nachtladen2states1
	echo 0 > $RamdiskPath/nachtladenstates1
	echo 4 > $RamdiskPath/graphtimer
	echo 0 > $RamdiskPath/speicher
	echo 0 > $RamdiskPath/ladestatus
	echo 0 > $RamdiskPath/ladestatuss1
	echo 0 > $RamdiskPath/ladestatuss2
	echo 0 > $RamdiskPath/pvcounter
	echo 0 > $RamdiskPath/pvecounter
	echo 0 > $RamdiskPath/glattwattbezug
	echo 0 > $RamdiskPath/llas11
	echo 0 > $RamdiskPath/bezuga1
	echo 0 > $RamdiskPath/bezuga2
	echo 0 > $RamdiskPath/bezuga3
	echo 0 > $RamdiskPath/bezugw1
	echo 0 > $RamdiskPath/bezugw2
	echo 0 > $RamdiskPath/bezugw3
	echo 0 > $RamdiskPath/llv1
	echo 0 > $RamdiskPath/llv2
	echo 0 > $RamdiskPath/llv3
	echo 0 > $RamdiskPath/llvs11
	echo 0 > $RamdiskPath/llvs12
	echo 0 > $RamdiskPath/llvs13
	echo 0 > $RamdiskPath/llvs21
	echo 0 > $RamdiskPath/llvs22
	echo 0 > $RamdiskPath/llvs23
	echo 0 > $RamdiskPath/llaltnv
	echo 0 > $RamdiskPath/llhz
	echo 0 > $RamdiskPath/llpf1
	echo 0 > $RamdiskPath/llpf2
	echo 0 > $RamdiskPath/llpf3
	echo 0 > $RamdiskPath/evuv1
	echo 0 > $RamdiskPath/evuv2
	echo 0 > $RamdiskPath/evuv3
	echo 0 > $RamdiskPath/evuhz
	echo 0 > $RamdiskPath/evupf1
	echo 0 > $RamdiskPath/evupf2
	echo 0 > $RamdiskPath/evupf3
	echo 0 > $RamdiskPath/evuhz
	echo 0 > $RamdiskPath/gelrlp1
	echo 0 > $RamdiskPath/gelrlp2
	echo 0 > $RamdiskPath/gelrlp3
	echo 0 > $RamdiskPath/mqttgelrlp1
	echo 0 > $RamdiskPath/mqttgelrlp2
	echo 0 > $RamdiskPath/mqttgelrlp3
	echo 0 > $RamdiskPath/llsolls1
	echo 0 > $RamdiskPath/llsolls2
	echo 0 > $RamdiskPath/gelrlp3
	echo 0 > $RamdiskPath/aktgeladen
	echo 0 > $RamdiskPath/aktgeladens1
	echo 0 > $RamdiskPath/aktgeladens2
	echo 0 > $RamdiskPath/aktgeladenlp4
	echo 0 > $RamdiskPath/aktgeladenlp5
	echo 0 > $RamdiskPath/aktgeladenlp6
	echo 0 > $RamdiskPath/aktgeladenlp7
	echo 0 > $RamdiskPath/aktgeladenlp8
	echo 0 > $RamdiskPath/llas12
	echo 0 > $RamdiskPath/llas13
	echo 0 > $RamdiskPath/ladestatus
	echo $bootmodus > $RamdiskPath/lademodus
	echo 1 > $RamdiskPath/llaktuell
	echo 1 > $RamdiskPath/llaktuells1
	echo 1 > $RamdiskPath/llaktuells2
	echo 1 > $RamdiskPath/llaktuelllp4
	echo 1 > $RamdiskPath/llaktuelllp5
	echo 1 > $RamdiskPath/llaktuelllp6
	echo 1 > $RamdiskPath/llaktuelllp7
	echo 1 > $RamdiskPath/llaktuelllp8
	echo 0 > $RamdiskPath/soc
	echo 0 > $RamdiskPath/soc1
	echo 0 > $RamdiskPath/soc1vorhanden
	echo 0 > $RamdiskPath/lla1
	echo 0 > $RamdiskPath/lla2
	echo 0 > $RamdiskPath/lla3
	touch $RamdiskPath/llog1
	touch $RamdiskPath/llogs1
	touch $RamdiskPath/llogs2
	echo 1 > $RamdiskPath/anzahlphasen
	echo 0 > $RamdiskPath/llkombiniert
	echo 0 > $RamdiskPath/llkwh
	echo "--" > $RamdiskPath/restzeitlp1
	echo "--" > $RamdiskPath/restzeitlp2
	echo "--" > $RamdiskPath/restzeitlp3
	echo "--" > $RamdiskPath/restzeitlp4
	echo "--" > $RamdiskPath/restzeitlp5
	echo "--" > $RamdiskPath/restzeitlp6
	echo "--" > $RamdiskPath/restzeitlp7
	echo "--" > $RamdiskPath/restzeitlp8
	echo "0" > $RamdiskPath/restzeitlp1m
	echo "0" > $RamdiskPath/restzeitlp2m
	echo "0" > $RamdiskPath/restzeitlp3m
	echo 0 > $RamdiskPath/bezugkwh
	echo 0 > $RamdiskPath/einspeisungkwh
	echo 0 > $RamdiskPath/llkwhs1
	echo 0 > $RamdiskPath/llkwhs2
	echo 0 > $RamdiskPath/llkwhges
	echo 20000 > $RamdiskPath/soctimer
	echo 20000 > $RamdiskPath/soctimer1
	echo 0 > $RamdiskPath/ev.graph
	echo 0 > $RamdiskPath/ev-live.graph
	echo 0 > $RamdiskPath/evu.graph
	echo 0 > $RamdiskPath/evu-live.graph
	echo 0 > $RamdiskPath/pv.graph
	echo 0 > $RamdiskPath/pv-live.graph
	echo 0 > $RamdiskPath/date.graph
	echo 0 > $RamdiskPath/date-live.graph
	echo 0 > $RamdiskPath/soc.graph
	echo 0 > $RamdiskPath/soc-live.graph
	echo 0 > $RamdiskPath/speicherikwh
	echo 0 > $RamdiskPath/speicherekwh
	echo 28 > $RamdiskPath/evsemodbustimer
	echo 0 > $RamdiskPath/rsestatus
	echo 0 > $RamdiskPath/rseaktiv
	echo "nicht angefragt" > $RamdiskPath/evsedintestlp1
	echo "nicht angefragt" > $RamdiskPath/evsedintestlp2
	echo "nicht angefragt" > $RamdiskPath/evsedintestlp3
	echo 0 > $RamdiskPath/u1p3pstat
	echo 0 > $RamdiskPath/hook1einschaltverzcounter
	echo 0 > $RamdiskPath/hook2einschaltverzcounter
	echo 0 > $RamdiskPath/daily_verbraucher1ikwh
	echo 0 > $RamdiskPath/daily_verbraucher1ekwh
	echo 0 > $RamdiskPath/daily_verbraucher2ikwh
	echo 0 > $RamdiskPath/daily_verbraucher2ekwh
	echo 0 > $RamdiskPath/daily_verbraucher3ikwh
	echo $verbraucher1_name > $RamdiskPath/verbraucher1_name
	echo $verbraucher2_name > $RamdiskPath/verbraucher2_name
	echo $rfidlist > $RamdiskPath/rfidlist

	# init common files for lp1 to lp8
	for i in $(seq 1 8);
	do
		for f in \
			"pluggedladunglp${i}startkwh:openWB/lp/${i}/plugStartkWh" \
			"pluggedladungaktlp${i}:openWB/lp/${i}/pluggedladungakt" \
			"mqttmsmoduslp${i}:openWB/config/get/sofort/lp/${i}/chargeLimitation" \
			"mqttlp${i}name:openWB/lp/${i}/strChargePointName" \
			"mqttdisplaylp${i}max:openWB/config/get/display/chartLp/${i}/max"
		do
			IFS=':' read -r -a tuple <<< "$f"
			currentRamdiskFileVar="\"$RamdiskPath/${tuple[0]}\""
			eval currentRamdiskFile=\$$currentRamdiskFileVar
			if ! [ -f $currentRamdiskFile ]; then
				mqttValue=$(timeout 1 mosquitto_sub -C 1 -t ${tuple[1]})
				if [[ ! -z "$mqttValue" ]]; then
					echo "'$currentRamdiskFile' missing: Setting from MQTT topic '${tuple[0]}' to value '$mqttValue'"
					echo "$mqttValue" > $currentRamdiskFile
				else
					echo "'$currentRamdiskFile' missing: MQTT topic '${tuple[0]}' can also not provide any value: Setting to 0"
					echo 0 > $currentRamdiskFile
				fi
			fi
		done
	done

	# init other files
	for f in \
		"mqttCp1Configured:openWB/lp/1/boolChargePointConfigured" \
		"mqttRandomSleepValue:openWB/system/randomSleep" \
		"mqttabschaltuberschuss:openWB/config/get/pv/maxPowerConsumptionBeforeStop" \
		"mqttabschaltverzoegerung:openWB/config/get/pv/stopDelay" \
		"mqttadaptfaktor:openWB/config/get/pv/adaptiveChargingFactor" \
		"mqttadaptpv:openWB/config/get/pv/boolAdaptiveCharging" \
		"mqttaktgeladen:openWB/openWB/lp/1/kWhActualCharged" \
		"mqttaktgeladens1:openWB/openWB/lp/2/kWhActualCharged" \
		"mqttaktgeladens2:openWB/openWB/lp/3/kWhActualCharged" \
		"mqttdailychargelp1:openWB/lp/1/kWhDailyCharged" \
		"mqttdailychargelp2:openWB/lp/2/kWhDailyCharged" \
		"mqttdailychargelp3:openWB/lp/3/kWhDailyCharged" \
		"mqttdatenschutzack:openWB/config/get/global/dataProtectionAcknoledged" \
		"mqttdisplayevumax:openWB/config/get/display/chartEvuMinMax" \
		"mqttdisplayhausanzeigen:openWB/config/get/display/showHouseConsumption" \
		"mqttdisplayhausmax:openWB/config/get/display/chartHouseConsumptionMax" \
		"mqttdisplaypvmax:openWB/config/get/display/chartPvMax" \
		"mqttdisplayspeichermax:openWB/config/get/display/chartBatteryMinMax" \
		"mqttdurchslp1:openWB/lp/1/energyConsumptionPer100km" \
		"mqtteinschaltverzoegerung:openWB/config/get/pv/startDelay" \
		"mqttetprovideraktiv:openWB/global/awattar/boolAwattarEnabled" \
		"mqttevuglaettungakt:openWB/boolEvuSmoothedActive" \
		"mqtthausverbrauch:openWB/global/WHouseConsumption" \
		"mqtthausverbrauchstat:openWB/boolDisplayHouseConsumption" \
		"mqttheutegeladen:openWB/boolDisplayDailyCharged" \
		"mqtthook1_aktiv:openWB/hook/1/boolHookConfigured" \
		"mqtthook2_aktiv:openWB/hook/2/boolHookConfigured" \
		"mqtthook3_aktiv:openWB/hook/3/boolHookConfigured" \
		"mqttlademkwh:openWB/config/get/sofort/lp/1/energyToCharge" \
		"mqttlademkwhlp4:openWB/config/get/sofort/lp/4/energyToCharge" \
		"mqttlademkwhlp5:openWB/config/get/sofort/lp/5/energyToCharge" \
		"mqttlademkwhlp6:openWB/config/get/sofort/lp/6/energyToCharge" \
		"mqttlademkwhlp7:openWB/config/get/sofort/lp/7/energyToCharge" \
		"mqttlademkwhlp8:openWB/config/get/sofort/lp/8/energyToCharge" \
		"mqttlademstat:openWB/lp/1/boolDirectModeChargekWh" \
		"mqttlademstatlp4:openWB/lp/4/boolDirectModeChargekWh" \
		"mqttlademstatlp5:openWB/lp/5/boolDirectModeChargekWh" \
		"mqttlademstatlp6:openWB/lp/6/boolDirectModeChargekWh" \
		"mqttlademstatlp7:openWB/lp/7/boolDirectModeChargekWh" \
		"mqttlademstatlp8:openWB/lp/8/boolDirectModeChargekWh" \
		"mqttlademstats1:openWB/lp/2/boolDirectModeChargekWh" \
		"mqttlademstats2:openWB/lp/3/boolDirectModeChargekWh" \
		"mqttlastlademodus:openWB/global/ChargeMode" \
		"mqttmaximalstromstaerke:openWB/config/get/global/maxEVSECurrentAllowed" \
		"mqttmaxnurpvsoclp1:openWB/config/get/pv/lp/1/maxSocToChargeTo" \
		"mqttmindestuberschuss:openWB/config/get/pv/minFeedinPowerBeforeStart" \
		"mqttminimalalp2pv:openWB/config/get/pv/lp/2/minCurrent" \
		"mqttminimalampv:openWB/config/get/pv/minCurrentMinPv" \
		"mqttminimalapv:openWB/config/get/pv/lp/1/minCurrent" \
		"mqttminimalstromstaerke:openWB/config/get/global/minEVSECurrentAllowed" \
		"mqttminnurpvsocll:openWB/config/get/pv/lp/1/minSocAlwaysToChargeToCurrent" \
		"mqttminnurpvsoclp1:openWB/config/get/pv/lp/1/minSocAlwaysToChargeTo" \
		"mqttnachtladen:openWB/lp/1/boolChargeAtNight" \
		"mqttnachtladens1:openWB/lp/2/boolChargeAtNight" \
		"mqttnlakt_minpv:openWB/boolChargeAtNight_minpv" \
		"mqttnlakt_nurpv:openWB/boolChargeAtNight_nurpv" \
		"mqttnlakt_sofort:openWB/boolChargeAtNight_direct" \
		"mqttnlakt_standby:openWB/boolChargeAtNight_standby" \
		"mqttnurpv70dynact:openWB/config/get/pv/nurpv70dynact" \
		"mqttnurpv70dynw:openWB/config/get/pv/nurpv70dynw" \
		"mqttoffsetpv:openWB/config/get/pv/regulationPoint" \
		"mqttpreisjekwh:openWB/system/priceForKWh" \
		"mqttpvbezugeinspeisung:openWB/config/get/pv/chargeSubmode" \
		"mqttpvwatt:openWB/pv/W" \
		"mqttrestzeitlp1:openWB/lp/1/TimeRemaining" \
		"mqttrestzeitlp2:openWB/lp/2/TimeRemaining" \
		"mqttrestzeitlp3:openWB/lp/3/TimeRemaining" \
		"mqttrfidakt:openWB/global/rfidConfigured" \
		"mqttsoc1vorhanden:openWB/lp/2/boolSocConfigured" \
		"mqttsoc:openWB/lp/1/%Soc" \
		"mqttsocvorhanden:openWB/lp/1/boolSocConfigured" \
		"mqttsofortsoclp1:openWB/config/get/sofort/lp/1/socToChargeTo" \
		"mqttsofortsoclp2:openWB/config/get/sofort/lp/2/socToChargeTo" \
		"mqttsofortsocstatlp1:openWB/lp/1/boolDirectChargeModeSoc" \
		"mqttsofortsocstatlp2:openWB/lp/2/boolDirectChargeModeSoc" \
		"mqttspeichermaxwatt:openWB/config/get/pv/minBatteryChargePowerAtEvPriority" \
		"mqttspeicherpveinbeziehen:openWB/config/get/pv/priorityModeEVBattery" \
		"mqttspeicherpvui:openWB/config/get/pv/boolShowPriorityIconInTheme" \
		"mqttspeichersochystminpv:openWB/config/get/pv/socStopChargeAtMinPv" \
		"mqttspeichersocminpv:openWB/config/get/pv/socStartChargeAtMinPv" \
		"mqttspeichersocnurpv:openWB/config/get/pv/minBatteryDischargeSocAtBattPriority" \
		"mqttspeicherwattnurpv:openWB/config/get/pv/batteryDischargePowerAtBattPriority" \
		"mqttstopchargepvatpercentlp1:openWB/config/get/pv/lp/1/socLimitation" \
		"mqttstopchargepvatpercentlp2:openWB/config/get/pv/lp/2/socLimitation" \
		"mqttstopchargepvpercentagelp1:openWB/config/get/pv/lp/1/maxSoc" \
		"mqttstopchargepvpercentagelp2:openWB/config/get/pv/lp/2/maxSoc" \
		"mqttu1p3paktiv:openWB/config/get/u1p3p/isConfigured" \
		"mqttu1p3pminundpv:openWB/config/get/u1p3p/minundpvPhases" \
		"mqttu1p3pnl:openWB/config/get/u1p3p/nachtPhases" \
		"mqttu1p3pnurpv:openWB/config/get/u1p3p/nurpvPhases" \
		"mqttu1p3psofort:openWB/config/get/u1p3p/sofortPhases" \
		"mqttu1p3pstandby:openWB/config/get/u1p3p/standbyPhases" \
		"mqttupdateinprogress:openWB/system/updateInProgress" \
		"mqttverbraucher1_aktiv:openWB/Verbraucher/1/Configured" \
		"mqttverbraucher1_name:openWB/Verbraucher/1/Name" \
		"mqttverbraucher2_aktiv:openWB/Verbraucher/2/Configured" \
		"mqttverbraucher2_name:openWB/Verbraucher/2/Name" \
		"mqttversion:openWB/system/Version" \
		"mqttwattbezug:openWB/evu/W" \
		"mqttwizzarddone:openWB/system/wizzardDone" \
		"mqttzielladenaktivlp1:openWB/lp/1/boolFinishAtTimeChargeActive"
	do
		IFS=':' read -r -a tuple <<< "$f"
		currentRamdiskFileVar="\"$RamdiskPath/${tuple[0]}\""
		eval currentRamdiskFile=\$$currentRamdiskFileVar
		if ! [ -f $currentRamdiskFile ]; then
			mqttValue=$(timeout 1 mosquitto_sub -C 1 -t ${tuple[1]})
			if [[ ! -z "$mqttValue" ]]; then
				echo "'$currentRamdiskFile' missing: Setting from MQTT topic '${tuple[0]}' to value '$mqttValue'"
				echo "$mqttValue" > $currentRamdiskFile
			else
				echo "'$currentRamdiskFile' missing: MQTT topic '${tuple[0]}' can also not provide any value: Setting to 0"
				echo 0 > $currentRamdiskFile
			fi
		fi
	done

	sudo chmod 777 $RamdiskPath/*

	echo "Ramdisk init done."
}
