#!/bin/bash
#Ramdisk mit initialen Werten befüllen nach neustart
sleep 10
sudo chown -R www-data:www-data /var/www/html/openWB/web/backup
sudo chown -R www-data:www-data /var/www/html/openWB/web/tools/upload
sudo chmod 777 /var/www/html/openWB/openwb.conf
sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod 777 /var/www/html/openWB/web/files/*
sudo chmod -R +x /var/www/html/openWB/modules/*
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3s1

echo 0 > /var/www/html/openWB/ramdisk/blockall
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
touch /var/www/html/openWB/ramdisk/nachtladenstate
touch /var/www/html/openWB/ramdisk/nachtladenstates1
touch /var/www/html/openWB/ramdisk/zielladenkorrektura
touch /var/www/html/openWB/ramdisk/hausverbrauch
echo 0 > /var/www/html/openWB/ramdisk/zielladenkorrektura
echo 0 > /var/www/html/openWB/ramdisk/nachtladenstate
echo 0 > /var/www/html/openWB/ramdisk/nachtladen2state
echo 0 > /var/www/html/openWB/ramdisk/nachtladen2states1
echo 0 > /var/www/html/openWB/ramdisk/nachtladenstates1
echo 4 > /var/www/html/openWB/ramdisk/graphtimer
echo "" > /var/www/html/openWB/ramdisk/lastregelungaktiv
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
echo 3 > /var/www/html/openWB/ramdisk/lademodus
echo 0 > /var/www/html/openWB/ramdisk/llaktuell
echo 0 > /var/www/html/openWB/ramdisk/pvwatt
echo 0 > /var/www/html/openWB/ramdisk/soc
echo 0 > /var/www/html/openWB/ramdisk/soc1
echo 0 > /var/www/html/openWB/ramdisk/lla1
echo 0 > /var/www/html/openWB/ramdisk/lla2
echo 0 > /var/www/html/openWB/ramdisk/lla3
echo 0 > /var/www/html/openWB/ramdisk/llaktuells1
echo 0 > /var/www/html/openWB/ramdisk/llaktuells2
echo 0 > /var/www/html/openWB/ramdisk/hausverbrauch
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
echo 0 > /var/www/html/openWB/ramdisk/speicherleistung
echo 0 > /var/www/html/openWB/ramdisk/speichersoc
echo 0 > /var/www/html/openWB/ramdisk/speicherikwh
echo 0 > /var/www/html/openWB/ramdisk/speicherekwh
echo 28 > /var/www/html/openWB/ramdisk/evsemodbustimer
echo "nicht angefragt" > /var/www/html/openWB/ramdisk/evsedintestlp1
echo "nicht angefragt" > /var/www/html/openWB/ramdisk/evsedintestlp2
echo "nicht angefragt" > /var/www/html/openWB/ramdisk/evsedintestlp3
echo 0 > /var/www/html/openWB/ramdisk/u1p3pstat

sudo chmod 777 /var/www/html/openWB/ramdisk/*
sudo chmod 777 /var/www/html/openWB/web/files/*
sudo chmod -R +x /var/www/html/openWB/modules/*
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3
sudo chmod -R 777 /var/www/html/openWB/modules/soc_i3s1




ln -s /var/log/openWB.log /var/www/html/openWB/ramdisk/openWB.log
mkdir -p /var/www/html/openWB/web/logging/data/daily
mkdir -p /var/www/html/openWB/web/logging/data/monthly
sudo chmod -R 777 /var/www/html/openWB/web/logging/data/


if ! grep -Fq "abschaltverzoegerung=" /var/www/html/openWB/openwb.conf
then
  echo "abschaltverzoegerung=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "einschaltverzoegerung=" /var/www/html/openWB/openwb.conf
then
  echo "einschaltverzoegerung=10" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "ladetaster=" /var/www/html/openWB/openwb.conf
then
	  echo "ladetaster=0" >> /var/www/html/openWB/openwb.conf
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
if ! grep -Fq "sdm120modbusllsource=" /var/www/html/openWB/openwb.conf
then
	  echo "sdm120modbusllsource=/dev/ttyUSB1" >> /var/www/html/openWB/openwb.conf
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
if ! grep -Fq "speichermodul=" /var/www/html/openWB/openwb.conf
then
	  echo "speichermodul=none" >> /var/www/html/openWB/openwb.conf
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
if ! grep -Fq "hook1ein_url=" /var/www/html/openWB/openwb.conf
then
	  echo "hook1ein_url='https://webhook.com/ein.php'" >> /var/www/html/openWB/openwb.conf
fi
if ! grep -Fq "hook1aus_url=" /var/www/html/openWB/openwb.conf
then
	  echo "hook1aus_url='https://webhook.com/aus.php'" >> /var/www/html/openWB/openwb.conf
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



ethstate=$(</sys/class/net/eth0/carrier)
if (( ethstate == 1 )); then
	sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 up
fi
sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 up


if  grep -Fxq "AllowOverride" /etc/apache2/sites-available/000-default.conf
then
	echo "...ok"
else
	sudo cp /var/www/html/openWB/web/tools/000-default.conf /etc/apache2/sites-available/
	sudo service apache2 restart
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
if [ $(dpkg-query -W -f='${Status}' php-gd 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	sudo apt-get -qq update
	sleep 1
	sudo apt-get -qq install -y php-gd
	sleep 1
	sudo apt-get -qq install -y php7.0-xml

fi

. /var/www/html/openWB/openwb.conf
sudo cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime
uuid=$(</sys/class/net/eth0/address)

curl -d "update="$releasetrain$uuid"" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://openwb.de/tools/update.php

sudo i2cdetect -y 1 | grep -o ' .. --' |grep -o '[0-9]*' > /var/www/html/openWB/ramdisk/i2csearch
