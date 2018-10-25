#!/bin/bash
#Ramdisk mit initialen Werten befüllen nach neustart
sleep 10
echo 0 > /var/www/html/openWB/ramdisk/llsoll
touch /var/www/html/openWB/ramdisk/wattbezug
touch /var/www/html/openWB/ramdisk/ladestatus
touch /var/www/html/openWB/ramdisk/lademodus
touch /var/www/html/openWB/ramdisk/llaktuell
touch /var/www/html/openWB/ramdisk/llaktuells1
touch /var/www/html/openWB/ramdisk/pvwatt
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
touch /var/www/html/openWB/ramdisk/llkwh
touch /var/www/html/openWB/ramdisk/pvkwh
touch /var/www/html/openWB/ramdisk/llkwhs1
touch /var/www/html/openWB/ramdisk/einspeisungkwh
touch /var/www/html/openWB/ramdisk/bezugkwh
touch /var/www/html/openWB/ramdisk/llkwhs2
touch /var/www/html/openWB/ramdisk/speicher
echo 4 > /var/www/html/openWB/ramdisk/graphtimer
echo 0 > /var/www/html/openWB/ramdisk/speicher
echo 0 > /var/www/html/openWB/ramdisk/ladestatus
echo 0 > /var/www/html/openWB/ramdisk/ladestatuss1
echo 0 > /var/www/html/openWB/ramdisk/ladestatuss2
echo 0 > /var/www/html/openWB/ramdisk/pvcounter
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
echo 0 > /var/www/html/openWB/ramdisk/llsolls1
echo 0 > /var/www/html/openWB/ramdisk/llsolls2
echo 0 > /var/www/html/openWB/ramdisk/gelrlp3
echo 0 > /var/www/html/openWB/ramdisk/aktgeladen
echo 0 > /var/www/html/openWB/ramdisk/aktgeladens1
echo 0 > /var/www/html/openWB/ramdisk/aktgeladens2
echo 0 > /var/www/html/openWB/ramdisk/llas12
echo 0 > /var/www/html/openWB/ramdisk/llas13
echo 0 > /var/www/html/openWB/ramdisk/wattbezug
echo 0 > /var/www/html/openWB/ramdisk/ladestatus
echo 0 > /var/www/html/openWB/ramdisk/lademodus
echo 0 > /var/www/html/openWB/ramdisk/llaktuell
echo 0 > /var/www/html/openWB/ramdisk/pvwatt
echo 0 > /var/www/html/openWB/ramdisk/soc
echo 0 > /var/www/html/openWB/ramdisk/lla1
echo 0 > /var/www/html/openWB/ramdisk/lla2
echo 0 > /var/www/html/openWB/ramdisk/lla3	
echo 0 > /var/www/html/openWB/ramdisk/llaktuells1
echo 0 > /var/www/html/openWB/ramdisk/llaktuells2
touch /var/www/html/openWB/ramdisk/llog1
touch /var/www/html/openWB/ramdisk/llogs1
touch /var/www/html/openWB/ramdisk/llogs2
echo 0 > /var/www/html/openWB/ramdisk/llkombiniert
echo 0 > /var/www/html/openWB/ramdisk/llkwh
echo "--" > /var/www/html/openWB/ramdisk/restzeitlp1
echo "--" > /var/www/html/openWB/ramdisk/restzeitlp2
echo "--" > /var/www/html/openWB/ramdisk/restzeitlp3
echo 0 > /var/www/html/openWB/ramdisk/pvkwh
echo 0 > /var/www/html/openWB/ramdisk/pvkwhk
echo 0 > /var/www/html/openWB/ramdisk/bezugkwh
echo 0 > /var/www/html/openWB/ramdisk/einspeisungkwh
echo 0 > /var/www/html/openWB/ramdisk/llkwhs1
echo 0 > /var/www/html/openWB/ramdisk/llkwhs2
echo 57 > /var/www/html/openWB/ramdisk/soctimer
echo 57 > /var/www/html/openWB/ramdisk/soctimer1
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


sudo chown -R www-data:www-data /var/www/html/openWB/web/backup
sudo chown -R www-data:www-data /var/www/html/openWB/web/tools/upload
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod -R +x /var/www/html/openWB/modules/*
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3s1

ln -s /var/log/openWB.log /var/www/html/openWB/ramdisk/openWB.log

if ! grep -Fq "abschaltverzoegerung=" /var/www/html/openWB/openwb.conf
then
  echo "abschaltverzoegerung=10" >> /var/www/html/openWB/openwb.conf
fi
if ps ax |grep -v grep |grep "python /var/www/html/openWB/runs/ladetaster.py" > /dev/null
then
	echo "test" > /dev/null
else
	sudo python /var/www/html/openWB/runs/ladetaster.py &
fi

if ! grep -Fq "minimalapv=" /var/www/html/openWB/openwb.conf
then
	  echo "minimalapv=6" >> /var/www/html/openWB/openwb.conf
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

if ! grep -Fq "nachtladenbisuhrs1=" /var/www/html/openWB/openwb.conf
then
	  echo "nachtladenbisuhrs1=6" >> /var/www/html/openWB/openwb.conf
fi
if [ ! -e /var/www/html/openWB/web/ladelog ]; then
	sudo touch /var/www/html/openWB/web/ladelog
	sudo echo Start > /var/www/html/openWB/web/ladelog

	sudo chmod 777 /var/www/html/openWB/web/ladelog
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
	  echo "zoepasswort=passwort" >> /var/www/html/openWB/openwb.conf
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
if ! grep -Fq "evnotifypasswort=" /var/www/html/openWB/openwb.conf
then
	  echo "evnotifypasswort=abcdef" >> /var/www/html/openWB/openwb.conf
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
if ! sudo grep -Fq "cronnightly.sh" /var/spool/cron/crontabs/pi
then
	(crontab -l ; echo "1 0 * * * /var/www/html/openWB/runs/cronnightly.sh >> /var/log/openWB.log 2>&1")| crontab -
fi

if ! sudo grep -Fq "cron5min.sh" /var/spool/cron/crontabs/pi
then
	(crontab -l ; echo "*/5 * * * * /var/www/html/openWB/runs/cron5min.sh >> /var/log/openWB.log 2>&1")| crontab -
fi

if [ $(dpkg-query -W -f='${Status}' php-gd 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	sudo apt-get update
	sleep 1
	sudo apt-get -qq install -y php-gd
	sleep 1
	sudo apt-get -qq install -y php7.0-xml
	
fi



sudo i2cdetect -y 1 | grep -o ' .. --' |grep -o '[0-9]*' > /var/www/html/openWB/ramdisk/i2csearch
