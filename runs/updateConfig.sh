#!/bin/bash
# Nach Update Inhalt der openwb.conf prüfen und ergänzen

updateConfig(){
	ConfigFile="/var/www/html/openWB/openwb.conf"
	echo "Updating $ConfigFile..."

	if ! grep -Fq "wr_http_w_url=" $ConfigFile; then
		echo "wr_http_w_url='http://192.168.0.17/pvwatt.txt'" >> $ConfigFile
	else
		sed -i "/wr_http_w_url='/b; s/^wr_http_w_url=\(.*\)/wr_http_w_url=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "hsocip1=" $ConfigFile; then
		echo "hsocip1='http://10.0.0.110/soc.txt'" >> $ConfigFile
	else
		sed -i "/hsocip1='/b; s/^hsocip1=\(.*\)/hsocip1=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "socmodul1=" $ConfigFile; then
		echo "socmodul1=none" >> $ConfigFile
	else
		sed -i "s/^socmodul1=soc_http1/socmodul1=soc_httplp2/g" $ConfigFile
	fi
	if ! grep -Fq "dacregisters1=" $ConfigFile; then
		echo "dacregisters1=12" >> $ConfigFile
	fi
	if ! grep -Fq "wr_http_kwh_url=" $ConfigFile; then
		echo "wr_http_kwh_url='http://192.168.0.17/pvwh.txt'" >> $ConfigFile
	else
		sed -i "/wr_http_kwh_url='/b; s/^wr_http_kwh_url=\(.*\)/wr_http_kwh_url=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "smaemdbezugid=" $ConfigFile; then
		echo "smaemdbezugid=1900123456" >> $ConfigFile
	fi
	# upgrade after renaming "smaemd_pv" -> "wr_smashm"
	if grep -Fq "pvwattmodul=smaemd_pv" $ConfigFile; then
		sed -i "s/^pvwattmodul=smaemd_pv/pvwattmodul=wr_smashm/g" $ConfigFile
	fi
	if ! grep -Fq "smaemdpvid=" $ConfigFile; then
		echo "smaemdpvid=1900123456" >> $ConfigFile
	fi
	if ! grep -Fq "smaemdllid=" $ConfigFile; then
		echo "smaemdllid=1900123456" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_http_w_url=" $ConfigFile; then
		echo "bezug_http_w_url='http://192.168.0.17/bezugwatt.txt'" >> $ConfigFile
	else
		sed -i "/bezug_http_w_url='/b; s/^bezug_http_w_url=\(.*\)/bezug_http_w_url=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "bezug_http_ikwh_url=" $ConfigFile; then
		echo "bezug_http_ikwh_url='http://192.168.0.17/bezugwh.txt'" >> $ConfigFile
	else
		sed -i "/bezug_http_ikwh_url='/b; s/^bezug_http_ikwh_url=\(.*\)/bezug_http_ikwh_url=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "bezug_http_ekwh_url=" $ConfigFile; then
		echo "bezug_http_ekwh_url='http://192.168.0.17/einspeisungwh.txt'" >> $ConfigFile
	else
		sed -i "/bezug_http_ekwh_url='/b; s/^bezug_http_ekwh_url=\(.*\)/bezug_http_ekwh_url=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "minimalapv=" $ConfigFile; then
		echo "minimalapv=6" >> $ConfigFile
	fi
	if ! grep -Fq "minimalalp2pv=" $ConfigFile; then
		echo "minimalalp2pv=6" >> $ConfigFile
	fi
	if ! grep -Fq "minimalampv=" $ConfigFile; then
		echo "minimalampv=10" >> $ConfigFile
	fi
	if ! grep -Fq "pvbezugeinspeisung=" $ConfigFile; then
		echo "pvbezugeinspeisung=0" >> $ConfigFile
	fi
	if ! grep -Fq "evsecons2=" $ConfigFile; then
		echo "evsecons2=none" >> $ConfigFile
	fi
	if ! grep -Fq "evsesources2=" $ConfigFile; then
		echo "evsesources2=dac" >> $ConfigFile
	fi
	if ! grep -Fq "evseids2=" $ConfigFile; then
		echo "evseids2=3" >> $ConfigFile
	fi
	if ! grep -Fq "evselanips2=" $ConfigFile; then
		echo "evselanips2=192.168.14.2" >> $ConfigFile
	fi
	if ! grep -Fq "ladeleistungs2modul=" $ConfigFile; then
		echo "ladeleistungs2modul=sdm630modbuslls2" >> $ConfigFile
	fi
	if ! grep -Fq "sdmids2=" $ConfigFile; then
		echo "sdmids2=4" >> $ConfigFile
	fi
	if ! grep -Fq "lastmanagements2=" $ConfigFile; then
		echo "lastmanagements2=0" >> $ConfigFile
	fi
	if ! grep -Fq "sofortlls1=" $ConfigFile; then
		echo "sofortlls1=18" >> $ConfigFile
	fi
	if ! grep -Fq "sofortlls2=" $ConfigFile; then
		echo "sofortlls2=17" >> $ConfigFile
	fi
	if ! grep -Fq "dspeed=" $ConfigFile; then
		echo "dspeed=0" >> $ConfigFile
	fi
	if ! grep -Fq "durchslp1=" $ConfigFile; then
		echo "durchslp1=15" >> $ConfigFile
	fi
	if ! grep -Fq "durchslp3=" $ConfigFile; then
		echo "durchslp3=15" >> $ConfigFile
	fi
	if ! grep -Fq "durchslp2=" $ConfigFile; then
		echo "durchslp2=15" >> $ConfigFile
	fi
	if ! grep -Fq "nachtladens1=" $ConfigFile; then
		echo "nachtladens1=0" >> $ConfigFile
	fi
	if ! grep -Fq "nachtsocs1=" $ConfigFile; then
		echo "nachtsocs1=50" >> $ConfigFile
	fi
	if ! grep -Fq "nachtsoc1s1=" $ConfigFile; then
		echo "nachtsoc1s1=35" >> $ConfigFile
	fi
	if ! grep -Fq "nachtsoc1=" $ConfigFile; then
		echo "nachtsoc1=35" >> $ConfigFile
	fi
	if ! grep -Fq "nachtlls1=" $ConfigFile; then
		echo "nachtlls1=12" >> $ConfigFile
	fi
	if ! grep -Fq "nachtladenabuhrs1=" $ConfigFile; then
		echo "nachtladenabuhrs1=20" >> $ConfigFile
	fi
	if ! grep -Fq "lademkwh=" $ConfigFile; then
		echo "lademkwh=15" >> $ConfigFile
	fi
	if ! grep -Fq "lademkwhs1=" $ConfigFile; then
		echo "lademkwhs1=15" >> $ConfigFile
	fi
	if ! grep -Fq "lademkwhs2=" $ConfigFile; then
		echo "lademkwhs2=15" >> $ConfigFile
	fi
	if ! grep -Fq "lademstat=" $ConfigFile; then
		echo "lademstat=" >> $ConfigFile
	fi
	if ! grep -Fq "lademstats1=" $ConfigFile; then
		echo "lademstats1=" >> $ConfigFile
	fi
	if ! grep -Fq "lademstats2=" $ConfigFile; then
		echo "lademstats2=" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllsource=" $ConfigFile; then
		echo "sdm120modbusllsource=/dev/ttyUSB1" >> $ConfigFile
	fi
	if ! grep -Fq "speichersocnurpv=" $ConfigFile; then
		echo "speichersocnurpv=100" >> $ConfigFile
	fi
	if ! grep -Fq "speichersocminpv=" $ConfigFile; then
		echo "speichersocminpv=0" >> $ConfigFile
	fi
	if ! grep -Fq "speichersochystminpv=" $ConfigFile; then
		echo "speichersochystminpv=0" >> $ConfigFile
	fi
	if ! grep -Fq "speicherwattnurpv=" $ConfigFile; then
		echo "speicherwattnurpv=1500" >> $ConfigFile
	fi
	if ! grep -Fq "nurpvslowup=" $ConfigFile; then
		echo "nurpvslowup=0" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllid1=" $ConfigFile; then
		echo "sdm120modbusllid1=10" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllid2=" $ConfigFile; then
		echo "sdm120modbusllid2=10" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllid3=" $ConfigFile; then
		echo "sdm120modbusllid3=10" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllid1s1=" $ConfigFile; then
		echo "sdm120modbusllid1s1=10" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllid2s1=" $ConfigFile; then
		echo "sdm120modbusllid2s1=10" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllid3s1=" $ConfigFile; then
		echo "sdm120modbusllid3s1=10" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllid1s2=" $ConfigFile; then
		echo "sdm120modbusllid1s2=10" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllid2s2=" $ConfigFile; then
		echo "sdm120modbusllid2s2=10" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbusllid3s2=" $ConfigFile; then
		echo "sdm120modbusllid3s2=10" >> $ConfigFile
	fi
	# upgrade from old "none" to 254
	if grep -Fq "sdm120modbusllid2=none" $ConfigFile; then
		echo "sdm120modbusllid2=254" >> $ConfigFile
	fi
	if grep -Fq "sdm120modbusllid3=none" $ConfigFile; then
		echo "sdm120modbusllid3=254" >> $ConfigFile
	fi
	if grep -Fq "sdm120modbusllid2s1=none" $ConfigFile; then
		echo "sdm120modbusllid2s1=254" >> $ConfigFile
	fi
	if grep -Fq "sdm120modbusllid3s1=none" $ConfigFile; then
		echo "sdm120modbusllid3s1=254" >> $ConfigFile
	fi
	if grep -Fq "sdm120modbusllid2s2=none" $ConfigFile; then
		echo "sdm120modbusllid2s2=254" >> $ConfigFile
	fi
	if grep -Fq "sdm120modbusllid3s2=none" $ConfigFile; then
		echo "sdm120modbusllid3s2=254" >> $ConfigFile
	fi
	if ! grep -Fq "evsewifiiplp1=" $ConfigFile; then
		echo "evsewifiiplp1=192.168.0.25" >> $ConfigFile
	fi
	if ! grep -Fq "evsewifiiplp2=" $ConfigFile; then
		echo "evsewifiiplp2=192.168.0.25" >> $ConfigFile
	fi
	if ! grep -Fq "evsewifiiplp3=" $ConfigFile; then
		echo "evsewifiiplp3=192.168.0.25" >> $ConfigFile
	fi
	if ! grep -Fq "evsewifitimeoutlp1=" $ConfigFile; then
		echo "evsewifitimeoutlp1=2" >> $ConfigFile
	fi
	if ! grep -Fq "evsewifitimeoutlp2=" $ConfigFile; then
		echo "evsewifitimeoutlp2=2" >> $ConfigFile
	fi
	if ! grep -Fq "evsewifitimeoutlp3=" $ConfigFile; then
		echo "evsewifitimeoutlp3=2" >> $ConfigFile
	fi
	if ! grep -Fq "sofortsoclp1=" $ConfigFile; then
		echo "sofortsoclp1=90" >> $ConfigFile
	fi
	if ! grep -Fq "sofortsoclp2=" $ConfigFile; then
		echo "sofortsoclp2=90" >> $ConfigFile
	fi
	if ! grep -Fq "sofortsoclp3=" $ConfigFile; then
		echo "sofortsoclp3=90" >> $ConfigFile
	fi
	if ! grep -Fq "sofortsocstatlp1=" $ConfigFile; then
		echo "sofortsocstatlp1=" >> $ConfigFile
	fi
	if ! grep -Fq "sofortsocstatlp2=" $ConfigFile; then
		echo "sofortsocstatlp2=" >> $ConfigFile
	fi
	if ! grep -Fq "sofortsocstatlp3=" $ConfigFile; then
		echo "sofortsocstatlp3=" >> $ConfigFile
	fi
	if ! grep -Fq "pvsoclp1=" $ConfigFile; then
		echo "pvsoclp1=100" >> $ConfigFile
	fi
	if ! grep -Fq "pvsoclp2=" $ConfigFile; then
		echo "pvsoclp2=100" >> $ConfigFile
	fi
	if ! grep -Fq "pvsoclp3=" $ConfigFile; then
		echo "pvsoclp3=100" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmllsource=" $ConfigFile; then
		echo "mpm3pmllsource=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmllid=" $ConfigFile; then
		echo "mpm3pmllid=1" >> $ConfigFile
	fi
	if ! grep -Fq "msmoduslp1=" $ConfigFile; then
		echo "msmoduslp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "msmoduslp2=" $ConfigFile; then
		echo "msmoduslp2=0" >> $ConfigFile
	fi
	if ! grep -Fq "stopchargepvatpercentlp1=" $ConfigFile; then
		{
			echo "stopchargepvatpercentlp1=0"
			echo "stopchargepvatpercentlp2=0"
			echo "stopchargepvpercentagelp1=90"
			echo "stopchargepvpercentagelp2=90"
		} >> $ConfigFile
	fi
	if ! grep -Fq "msmoduslp3=" $ConfigFile; then
		{
			echo "msmoduslp3=0"
			echo "msmoduslp4=0"
			echo "msmoduslp5=0"
			echo "msmoduslp6=0"
			echo "msmoduslp7=0"
			echo "msmoduslp8=0"
		} >> $ConfigFile
	fi
	if ! grep -Fq "nachtladenbisuhrs1=" $ConfigFile; then
		echo "nachtladenbisuhrs1=6" >> $ConfigFile
	fi
	if ! grep -Fq "leafusername=" $ConfigFile; then
		echo "leafusername=username" >> $ConfigFile
	fi
	if ! grep -Fq "leafpasswort=" $ConfigFile; then
		echo "leafpasswort=''" >> $ConfigFile
	else
		sed -i "/leafpasswort='/b; s/^leafpasswort=\(.*\)/leafpasswort=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "leafusernames1=" $ConfigFile; then
		echo "leafusernames1=username" >> $ConfigFile
	fi
	if ! grep -Fq "leafpassworts1=" $ConfigFile; then
		echo "leafpassworts1=''" >> $ConfigFile
	else
		sed -i "/leafpassworts1='/b; s/^leafpassworts1=\(.*\)/leafpassworts1=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "i3username=" $ConfigFile; then
		echo "i3username=username" >> $ConfigFile
	fi
	if ! grep -Fq "soci3intervall=" $ConfigFile; then
		echo "soci3intervall=10" >> $ConfigFile
	fi
	if ! grep -Fq "soci3intervall1=" $ConfigFile; then
		echo "soci3intervall1=10" >> $ConfigFile
	fi
	if ! grep -Fq "i3passwort=" $ConfigFile; then
		echo "i3passwort=''" >> $ConfigFile
	else
		sed -i "/i3passwort='/b; s/^i3passwort=\(.*\)/i3passwort=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "i3usernames1=" $ConfigFile; then
		echo "i3usernames1=username" >> $ConfigFile
	fi
	if ! grep -Fq "i3passworts1=" $ConfigFile; then
		echo "i3passworts1=''" >> $ConfigFile
	else
		sed -i "/i3passworts1='/b; s/^i3passworts1=\(.*\)/i3passworts1=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "i3vins1=" $ConfigFile; then
		echo "i3vins1=VIN" >> $ConfigFile
	fi
	if ! grep -Fq "i3vin=" $ConfigFile; then
		echo "i3vin=VIN" >> $ConfigFile
	fi
	if ! grep -Fq "i3captcha_token=" $ConfigFile; then
		echo "i3captcha_token=''" >> $ConfigFile
	fi
	if ! grep -Fq "i3captcha_tokens1=" $ConfigFile; then
		echo "i3captcha_tokens1=''" >> $ConfigFile
	fi
	if ! grep -Fq "i3_soccalclp1=" $ConfigFile; then
		echo "i3_soccalclp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "i3_soccalclp2=" $ConfigFile; then
		echo "i3_soccalclp2=0" >> $ConfigFile
	fi
	if ! grep -Fq "zoeusername=" $ConfigFile; then
		echo "zoeusername=username" >> $ConfigFile
	fi
	if ! grep -Fq "zoepasswort=" $ConfigFile; then
		echo "zoepasswort=''" >> $ConfigFile
	else
		sed -i "/zoepasswort='/b; s/^zoepasswort=\(.*\)/zoepasswort=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "socpass=" $ConfigFile; then
		echo "socpass=''" >> $ConfigFile
	else
		sed -i "/socpass='/b; s/^socpass=\(.*\)/socpass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "socuser=" $ConfigFile; then
		echo "socuser=username" >> $ConfigFile
	fi
	if ! grep -Fq "zoelp2username=" $ConfigFile; then
		echo "zoelp2username=username" >> $ConfigFile
	fi
	if ! grep -Fq "zoelp2passwort=" $ConfigFile; then
		echo "zoelp2passwort=''" >> $ConfigFile
	else
		sed -i "/zoelp2passwort='/b; s/^zoelp2passwort=\(.*\)/zoelp2passwort=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "minnurpvsocll=" $ConfigFile; then
		echo "minnurpvsocll=12" >> $ConfigFile
	fi
	if ! grep -Fq "minnurpvsoclp1=" $ConfigFile; then
		echo "minnurpvsoclp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "maxnurpvsoclp1=" $ConfigFile; then
		echo "maxnurpvsoclp1=100" >> $ConfigFile
	fi
	if ! grep -Fq "evnotifyakey=" $ConfigFile; then
		echo "evnotifyakey=abcdef" >> $ConfigFile
	fi
	if ! grep -Fq "evnotifytoken=" $ConfigFile; then
		echo "evnotifytoken=token" >> $ConfigFile
	fi
	if ! grep -Fq "evnotifyakeylp2=" $ConfigFile; then
		echo "evnotifyakeylp2=abcdef" >> $ConfigFile
	fi
	if ! grep -Fq "evnotifytokenlp2=" $ConfigFile; then
		echo "evnotifytokenlp2=token" >> $ConfigFile
	fi
	if ! grep -Fq "wrjsonwatt=" $ConfigFile; then
		echo "wrjsonwatt='.watt'" >> $ConfigFile
	else
		sed -i "/wrjsonwatt='/b; s/^wrjsonwatt=\(.*\)/wrjsonwatt=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "wrjsonkwh=" $ConfigFile; then
		echo "wrjsonkwh='.kwh'" >> $ConfigFile
	else
		sed -i "/wrjsonkwh='/b; s/^wrjsonkwh=\(.*\)/wrjsonkwh=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "wrjsonurl=" $ConfigFile; then
		echo "wrjsonurl='http://192.168.0.12/solar_api'" >> $ConfigFile
	else
		sed -i "/wrjsonurl='/b; s/^wrjsonurl=\(.*\)/wrjsonurl=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "wr2jsonwatt=" $ConfigFile; then
		echo "wr2jsonwatt='.watt'" >> $ConfigFile
	else
		sed -i "/wr2jsonwatt='/b; s/^wr2jsonwatt=\(.*\)/wr2jsonwatt=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "wr2jsonkwh=" $ConfigFile; then
		echo "wr2jsonkwh='.kwh'" >> $ConfigFile
	else
		sed -i "/wr2jsonkwh='/b; s/^wr2jsonkwh=\(.*\)/wr2jsonkwh=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "wr2jsonurl=" $ConfigFile; then
		echo "wr2jsonurl='http://192.168.0.12/solar_api'" >> $ConfigFile
	else
		sed -i "/wr2jsonurl='/b; s/^wr2jsonurl=\(.*\)/wr2jsonurl=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "hausbezugnone=" $ConfigFile; then
		echo "hausbezugnone=200" >> $ConfigFile
	fi
	if ! grep -Fq "twcmanagerlp1ip=" $ConfigFile; then
		echo "twcmanagerlp1ip='192.168.0.15'" >> $ConfigFile
	fi
	if ! grep -Fq "httpevseip=" $ConfigFile; then
		echo "httpevseip='192.168.0.15'" >> $ConfigFile
	fi
	if ! grep -Fq "twcmanagerlp1phasen=" $ConfigFile; then
		echo "twcmanagerlp1phasen=3" >> $ConfigFile
	fi
	if ! grep -Fq "twcmanagerlp1httpcontrol=" $ConfigFile; then
		echo "twcmanagerlp1httpcontrol=0" >> $ConfigFile
	fi
	if ! grep -Fq "twcmanagerlp1port=" $ConfigFile; then
		echo "twcmanagerlp1port=8080" >> $ConfigFile
	fi
	if ! grep -Fq "twcmanagerlp2ip=" $ConfigFile; then
		echo "twcmanagerlp2ip='127.0.0.1'" >> $ConfigFile
	fi
	if ! grep -Fq "twcmanagerlp2port=" $ConfigFile; then
		echo "twcmanagerlp2port=8080" >> $ConfigFile
	fi
	if ! grep -Fq "twcmanagerlp2phasen=" $ConfigFile; then
		echo "twcmanagerlp2phasen=3" >> $ConfigFile
	fi
	if ! grep -Fq "twcmanagerlp2httpcontrol=" $ConfigFile; then
		echo "twcmanagerlp2httpcontrol=0" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmpvsource=" $ConfigFile; then
		echo "mpm3pmpvsource=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmpvid=" $ConfigFile; then
		echo "mpm3pmpvid=1" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmpvlanip=" $ConfigFile; then
		echo "mpm3pmpvlanip=192.168.1.12" >> $ConfigFile
	fi
	if ! grep -Fq "bezugjsonwatt=" $ConfigFile; then
		echo "bezugjsonwatt='.watt'" >> $ConfigFile
	else
		sed -i "/bezugjsonwatt='/b; s/^bezugjsonwatt=\(.*\)/bezugjsonwatt=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "bezugjsonkwh=" $ConfigFile; then
		echo "bezugjsonkwh='.kwh'" >> $ConfigFile
	else
		sed -i "/bezugjsonkwh='/b; s/^bezugjsonkwh=\(.*\)/bezugjsonkwh=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "einspeisungjsonkwh=" $ConfigFile; then
		echo "einspeisungjsonkwh='.kwh'" >> $ConfigFile
	else
		sed -i "/einspeisungjsonkwh='/b; s/^einspeisungjsonkwh=\(.*\)/einspeisungjsonkwh=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "bezugjsonurl=" $ConfigFile; then
		echo "bezugjsonurl='http://192.168.0.12/solar_api'" >> $ConfigFile
	else
		sed -i "/bezugjsonurl='/b; s/^bezugjsonurl=\(.*\)/bezugjsonurl=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "mpm3pmlls1source=" $ConfigFile; then
		echo "mpm3pmlls1source=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmlls1id=" $ConfigFile; then
		echo "mpm3pmlls1id=1" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmlls2source=" $ConfigFile; then
		echo "mpm3pmlls2source=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmlls2id=" $ConfigFile; then
		echo "mpm3pmlls2id=5" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmevusource=" $ConfigFile; then
		echo "mpm3pmevusource=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmevuid=" $ConfigFile; then
		echo "mpm3pmevuid=1" >> $ConfigFile
	fi
	if ! grep -Fq "livegraph=" $ConfigFile; then
		echo "livegraph=20" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_solarlog_ip=" $ConfigFile; then
		echo "bezug_solarlog_ip=192.168.0.10" >> $ConfigFile
	fi
	if ! grep -Fq "bezug2_solarlog_ip=" $ConfigFile; then
		echo "bezug2_solarlog_ip=192.168.0.12" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_id=" $ConfigFile; then
		echo "bezug_id=30" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_solarlog_speicherv=" $ConfigFile; then
		echo "bezug_solarlog_speicherv=0" >> $ConfigFile
	fi
	if ! grep -Fq "bezug2_solarlog_speicherv=" $ConfigFile; then
		echo "bezug2_solarlog_speicherv=0" >> $ConfigFile
	fi
	if ! grep -Fq "wrenphasehostname=" $ConfigFile; then
		echo "wrenphasehostname=envoy.local" >> $ConfigFile
	fi
	if ! grep -Fq "wrenphaseeid=" $ConfigFile; then
		echo "wrenphaseeid=0" >> $ConfigFile
	fi
	if ! grep -Fq "bezugenphaseeid=" $ConfigFile; then
		echo "bezugenphaseeid=0" >> $ConfigFile
	fi
	if ! grep -Fq "wrfronius2ip=" $ConfigFile; then
		echo "wrfronius2ip=none" >> $ConfigFile
	fi
	if ! grep -Fq "speichermodul=" $ConfigFile; then
		echo "speichermodul=none" >> $ConfigFile
	fi
	if ! grep -Fq "displaytheme=" $ConfigFile; then
		echo "displaytheme=0" >> $ConfigFile
	fi
	if ! grep -Fq "displayEinBeimAnstecken=" $ConfigFile; then
		echo "displayEinBeimAnstecken=1" >> $ConfigFile
	fi
	if ! grep -Fq "speicherleistung_http=" $ConfigFile; then
		echo "speicherleistung_http='192.168.0.10/watt'" >> $ConfigFile
	else
		sed -i "/speicherleistung_http='/b; s/^speicherleistung_http=\(.*\)/speicherleistung_http=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "speichersoc_http=" $ConfigFile; then
		echo "speichersoc_http='192.168.0.10/soc'" >> $ConfigFile
	else
		sed -i "/speichersoc_http='/b; s/^speichersoc_http=\(.*\)/speichersoc_http=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "speicherekwh_http=" $ConfigFile; then
		echo "speicherekwh_http='192.168.0.10/eWh'" >> $ConfigFile
		echo "speicherikwh_http='192.168.0.10/iWh'" >> $ConfigFile
	else
		sed -i "/speicherekwh_http='/b; s/^speicherekwh_http=\(.*\)/speicherekwh_http=\'\1\'/g" $ConfigFile
		sed -i "/speicherikwh_http='/b; s/^speicherikwh_http=\(.*\)/speicherikwh_http=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "battjsonurl=" $ConfigFile; then
		echo "battjsonurl='192.168.0.10/speicher'" >> $ConfigFile
	else
		sed -i "/battjsonurl='/b; s/^battjsonurl=\(.*\)/battjsonurl=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "battjsonsoc=" $ConfigFile; then
		echo "battjsonsoc='.RSOC'" >> $ConfigFile
	else
		sed -i "/battjsonsoc='/b; s/^battjsonsoc=\(.*\)/battjsonsoc=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "battjsonwatt=" $ConfigFile; then
		echo "battjsonwatt='.Consumption_W'" >> $ConfigFile
	else
		sed -i "/battjsonwatt='/b; s/^battjsonwatt=\(.*\)/battjsonwatt=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_tesla_username=" $ConfigFile; then
		echo "soc_tesla_username=deine@email.com" >> $ConfigFile
	fi
	if ! grep -Fq "soc_tesla_carnumber=" $ConfigFile; then
		echo "soc_tesla_carnumber=0" >> $ConfigFile
	fi
	if ! grep -Fq "soc_tesla_password=" $ConfigFile; then
		echo "soc_tesla_password=''" >> $ConfigFile
	else
		sed -i "/soc_tesla_password='/b; s/^soc_tesla_password=\(.*\)/soc_tesla_password=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_tesla_intervallladen=" $ConfigFile; then
		echo "soc_tesla_intervallladen=20" >> $ConfigFile
	fi
	if ! grep -Fq "soc_tesla_intervall=" $ConfigFile; then
		echo "soc_tesla_intervall=20" >> $ConfigFile
	fi
	if ! grep -Fq "soc_id_intervallladen=" $ConfigFile; then
		echo "soc_id_intervallladen=20" >> $ConfigFile
	fi
	if ! grep -Fq "soc_id_intervall=" $ConfigFile; then
		echo "soc_id_intervall=120" >> $ConfigFile
	fi
	if ! grep -Fq "soc_ovms_intervallladen=" $ConfigFile; then
		echo "soc_ovms_intervallladen=20" >> $ConfigFile
	fi
	if ! grep -Fq "soc_ovms_intervall=" $ConfigFile; then
		echo "soc_ovms_intervall=120" >> $ConfigFile
	fi
	if ! grep -Fq "releasetrain=" $ConfigFile; then
		echo "releasetrain=stable" >> $ConfigFile
	fi
	if ! grep -Fq "wrkostalpikoip=" $ConfigFile; then
		echo "wrkostalpikoip=192.168.0.10" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgeip=" $ConfigFile; then
		echo "solaredgeip=192.168.0.10" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgemodbusport=" $ConfigFile; then
		echo "solaredgemodbusport=502" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgepvip=" $ConfigFile; then
		echo "solaredgepvip=192.168.0.10" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgepvslave1=" $ConfigFile; then
		echo "solaredgepvslave1=1" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgepvslave2=" $ConfigFile; then
		echo "solaredgepvslave2=none" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgepvslave3=" $ConfigFile; then
		echo "solaredgepvslave3=none" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgepvslave4=" $ConfigFile; then
		echo "solaredgepvslave4=none" >> $ConfigFile
	fi
	if ! grep -Fq "lllaniplp2=" $ConfigFile; then
		echo "lllaniplp2=192.168.0.10" >> $ConfigFile
	fi
	if ! grep -Fq "sdm630lp2source=" $ConfigFile; then
		echo "sdm630lp2source=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120lp2source=" $ConfigFile; then
		echo "sdm120lp2source=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120lp3source=" $ConfigFile; then
		echo "sdm120lp3source=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "sdm630lp3source=" $ConfigFile; then
		echo "sdm630lp3source=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "lllaniplp3=" $ConfigFile; then
		echo "lllaniplp3=192.168.0.10" >> $ConfigFile
	fi
	if ! grep -Fq "lp1name=" $ConfigFile; then
		echo "lp1name='LP1'" >> $ConfigFile
	fi
	if ! grep -Fq "lp2name=" $ConfigFile; then
		echo "lp2name='LP2'" >> $ConfigFile
	fi
	if ! grep -Fq "lp3name=" $ConfigFile; then
		echo "lp3name='LP3'" >> $ConfigFile
	fi
	if ! grep -Fq "loadsharinglp12=" $ConfigFile; then
		echo "loadsharinglp12=0" >> $ConfigFile
	fi
	if ! grep -Fq "loadsharingalp12=" $ConfigFile; then
		echo "loadsharingalp12=32" >> $ConfigFile
	fi
	if ! grep -Fq "goeiplp1=" $ConfigFile; then
		echo "goeiplp1=192.168.0.15" >> $ConfigFile
	fi
	if ! grep -Fq "goetimeoutlp1=" $ConfigFile; then
		echo "goetimeoutlp1=5" >> $ConfigFile
	fi
	if ! grep -Fq "goeiplp2=" $ConfigFile; then
		echo "goeiplp2=192.168.0.15" >> $ConfigFile
	fi
	if ! grep -Fq "goetimeoutlp2=" $ConfigFile; then
		echo "goetimeoutlp2=5" >> $ConfigFile
	fi
	if ! grep -Fq "goeiplp3=" $ConfigFile; then
		echo "goeiplp3=192.168.0.15" >> $ConfigFile
	fi
	if ! grep -Fq "goetimeoutlp3=" $ConfigFile; then
		echo "goetimeoutlp3=5" >> $ConfigFile
	fi
	if ! grep -Fq "pushbenachrichtigung=" $ConfigFile; then
		echo "pushbenachrichtigung=0" >> $ConfigFile
	fi
	if ! grep -Fq "pushovertoken=" $ConfigFile; then
		echo "pushovertoken='demotoken'" >> $ConfigFile
	fi
	if ! grep -Fq "pushoveruser=" $ConfigFile; then
		echo "pushoveruser='demouser'" >> $ConfigFile
	fi
	if ! grep -Fq "pushbstartl=" $ConfigFile; then
		echo "pushbstartl=1" >> $ConfigFile
	fi
	if ! grep -Fq "pushbstopl=" $ConfigFile; then
		echo "pushbstopl=1" >> $ConfigFile
	fi
	if ! grep -Fq "smashmbezugid=" $ConfigFile; then
		echo "smashmbezugid=1234567789" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmspeichersource=" $ConfigFile; then
		echo "mpm3pmspeichersource=/dev/tty2" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmspeicherid=" $ConfigFile; then
		echo "mpm3pmspeicherid=8" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmspeicherpv=" $ConfigFile; then
		echo "mpm3pmspeicherpv=0" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmspeicherlanip=" $ConfigFile; then
		echo "mpm3pmspeicherlanip=192.168.5.10" >> $ConfigFile
	fi
	if ! grep -Fq "logdailywh=" $ConfigFile; then
		echo "logdailywh=1" >> $ConfigFile
	fi
	if ! grep -Fq "logeinspeisungneg=" $ConfigFile; then
		echo "logeinspeisungneg=1" >> $ConfigFile
	fi
	if ! grep -Fq "speicherpveinbeziehen=" $ConfigFile; then
		echo "speicherpveinbeziehen=0" >> $ConfigFile
	fi
	if ! grep -Fq "speicherpvui=" $ConfigFile; then
		echo "speicherpvui=0" >> $ConfigFile
	fi
	if ! grep -Fq "speichermaxwatt=" $ConfigFile; then
		echo "speichermaxwatt=0" >> $ConfigFile
	fi
	if ! grep -Fq "nacht2lls1=" $ConfigFile; then
		echo "nacht2lls1=12" >> $ConfigFile
	fi
	if ! grep -Fq "nachtladen2abuhrs1=" $ConfigFile; then
		echo "nachtladen2abuhrs1=7" >> $ConfigFile
	fi
	if ! grep -Fq "nachtladen2bisuhrs1=" $ConfigFile; then
		echo "nachtladen2bisuhrs1=7" >> $ConfigFile
	fi
	if ! grep -Fq "nacht2ll=" $ConfigFile; then
		echo "nacht2ll=12" >> $ConfigFile
	fi
	if ! grep -Fq "nachtladen2abuhr=" $ConfigFile; then
		echo "nachtladen2abuhr=7" >> $ConfigFile
	fi
	if ! grep -Fq "nachtladen2bisuhr=" $ConfigFile; then
		echo "nachtladen2bisuhr=7" >> $ConfigFile
	fi
	if ! grep -Fq "akkuglp1=" $ConfigFile; then
		echo "akkuglp1=35" >> $ConfigFile
	fi
	if ! grep -Fq "akkuglp2=" $ConfigFile; then
		echo "akkuglp2=35" >> $ConfigFile
	fi
	if ! grep -Fq "zielladenuhrzeitlp1=" $ConfigFile; then
		echo "zielladenuhrzeitlp1='2018-12-19 06:15'" >> $ConfigFile
	fi
	if ! grep -Fq "zielladensoclp1=" $ConfigFile; then
		echo "zielladensoclp1=60" >> $ConfigFile
	fi
	if ! grep -Fq "zielladenalp1=" $ConfigFile; then
		echo "zielladenalp1=10" >> $ConfigFile
	fi
	if ! grep -Fq "zielladenphasenlp1=" $ConfigFile; then
		echo "zielladenphasenlp1=1" >> $ConfigFile
	fi
	if ! grep -Fq "zielladenmaxalp1=" $ConfigFile; then
		echo "zielladenmaxalp1=32" >> $ConfigFile
	fi
	if ! grep -Fq "zielladenaktivlp1=" $ConfigFile; then
		echo "zielladenaktivlp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_smartme_user=" $ConfigFile; then
		echo "bezug_smartme_user='user'" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_smartme_pass=" $ConfigFile; then
		echo "bezug_smartme_pass=''" >> $ConfigFile
	else
		sed -i "/bezug_smartme_pass='/b; s/^bezug_smartme_pass=\(.*\)/bezug_smartme_pass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "bezug_smartme_url=" $ConfigFile; then
		echo "bezug_smartme_url='https://smart-me.com:443/api/Devices/[ID]'" >> $ConfigFile
	fi
	if ! grep -Fq "wr_smartme_user=" $ConfigFile; then
		echo "wr_smartme_user='user'" >> $ConfigFile
	fi
	if ! grep -Fq "wr_smartme_pass=" $ConfigFile; then
		echo "wr_smartme_pass=''" >> $ConfigFile
	else
		sed -i "/wr_smartme_pass='/b; s/^wr_smartme_pass=\(.*\)/wr_smartme_pass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "wr_smartme_url=" $ConfigFile; then
		echo "wr_smartme_url='https://smart-me.com:443/api/Devices/[ID]'" >> $ConfigFile
	fi
	if ! grep -Fq "wr_piko2_user=" $ConfigFile; then
		echo "wr_piko2_user='user'" >> $ConfigFile
	fi
	if ! grep -Fq "wr_piko2_pass=" $ConfigFile; then
		echo "wr_piko2_pass=''" >> $ConfigFile
	else
		sed -i "/wr_piko2_pass='/b; s/^wr_piko2_pass=\(.*\)/wr_piko2_pass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "wr_piko2_url=" $ConfigFile; then
		echo "wr_piko2_url='https://url'" >> $ConfigFile
	fi
	if ! grep -Fq "wr2_piko2_user=" $ConfigFile; then
		echo "wr2_piko2_user='user'" >> $ConfigFile
	fi
	if ! grep -Fq "wr2_piko2_pass=" $ConfigFile; then
		echo "wr2_piko2_pass=''" >> $ConfigFile
	else
		sed -i "/wr2_piko2_pass='/b; s/^wr2_piko2_pass=\(.*\)/wr2_piko2_pass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "wr2_piko2_url=" $ConfigFile; then
		echo "wr2_piko2_url='https://url'" >> $ConfigFile
	fi
	if ! grep -Fq "wr2_kostal_steca_variant=" $ConfigFile; then
		echo "wr2_kostal_steca_variant=0" >> $ConfigFile
	fi
	if ! grep -Fq "carnetuser=" $ConfigFile; then
		echo "carnetuser='user'" >> $ConfigFile
	fi
	if ! grep -Fq "carnetpass=" $ConfigFile; then
		echo "carnetpass=''" >> $ConfigFile
	else
		sed -i "/carnetpass='/b; s/^carnetpass=\(.*\)/carnetpass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soccarnetintervall=" $ConfigFile; then
		echo "soccarnetintervall=10" >> $ConfigFile
	fi
	if ! grep -Fq "soc_vag_type=" $ConfigFile; then
		echo "soc_vag_type=vw" >> $ConfigFile
	fi
	if ! grep -Fq "soc_vag_username=" $ConfigFile; then
		echo "soc_vag_username=user" >> $ConfigFile
	fi
	if ! grep -Fq "soc_vag_password=" $ConfigFile; then
		echo "soc_vag_password=''" >> $ConfigFile
	else
		sed -i "/soc_vag_password='/b; s/^soc_vag_password=\(.*\)/soc_vag_password=\'\1\'/g" $ConfigFile
	fi
	# remove line with syntax error from config
	if grep -Fq "soc_vag_vin=vin (WVWZZZ...)" $ConfigFile; then
		sed -i '/^soc_vag_vin=/d' $ConfigFile
	fi
	if ! grep -Fq "soc_vag_vin=" $ConfigFile; then
		echo "soc_vag_vin='WVWZZZ...'" >> $ConfigFile
	fi
	if ! grep -Fq "soc_vag_intervall=" $ConfigFile; then
		echo "soc_vag_intervall=60" >> $ConfigFile
		echo "soc_vag_intervallladen=10" >> $ConfigFile
	fi
	if ! grep -Fq "soc2type=" $ConfigFile; then
		echo "soc2type=vw" >> $ConfigFile
	fi
	if ! grep -Fq "soc2intervallladen=" $ConfigFile; then
		echo "soc2intervallladen=10" >> $ConfigFile
	fi
	if ! grep -Fq "soc_http_intervall=" $ConfigFile; then
		echo "soc_http_intervall=60" >> $ConfigFile
		echo "soc_http_intervallladen=10" >> $ConfigFile
	fi
	if ! grep -Fq "bydhvuser=" $ConfigFile; then
		echo "bydhvuser=benutzer" >> $ConfigFile
	fi
	if ! grep -Fq "bydhvpass=" $ConfigFile; then
		echo "bydhvpass=''" >> $ConfigFile
	else
		sed -i "/bydhvpass='/b; s/^bydhvpass=\(.*\)/bydhvpass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "bydhvip=" $ConfigFile; then
		echo "bydhvip=192.168.10.12" >> $ConfigFile
	fi
	if ! grep -Fq "e3dcip=" $ConfigFile; then
		echo "e3dcip=192.168.10.12" >> $ConfigFile
	fi
	if ! grep -Fq "e3dc2ip=" $ConfigFile; then
		echo "e3dc2ip=none" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_http_l1_url=" $ConfigFile; then
		echo "bezug_http_l1_url='http://192.168.0.17/bezuga1'" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_http_l2_url=" $ConfigFile; then
		echo "bezug_http_l2_url='http://192.168.0.17/bezuga2'" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_http_l3_url=" $ConfigFile; then
		echo "bezug_http_l3_url='http://192.168.0.17/bezuga3'" >> $ConfigFile
	fi
	if ! grep -Fq "sbs25ip=" $ConfigFile; then
		echo "sbs25ip=192.168.10.12" >> $ConfigFile
	fi
	if ! grep -Fq "sbs25se=" $ConfigFile; then
		echo "sbs25se=0" >> $ConfigFile
	fi
	if ! grep -Fq "tri9000ip=" $ConfigFile; then
		echo "tri9000ip=192.168.10.12" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgespeicherip=" $ConfigFile; then
		echo "solaredgespeicherip='192.168.0.31'" >> $ConfigFile
	fi
	if ! grep -Fq "offsetpv=" $ConfigFile; then
		echo "offsetpv=0" >> $ConfigFile
	fi
	if ! grep -Fq "kostalplenticoreip=" $ConfigFile; then
		echo "kostalplenticoreip=192.168.0.30" >> $ConfigFile
	fi
	if ! grep -Fq "kostalplenticoreip2=" $ConfigFile; then
		echo "kostalplenticoreip2=none" >> $ConfigFile
	fi
	if ! grep -Fq "kostalplenticoreip3=" $ConfigFile; then
		echo "kostalplenticoreip3=none" >> $ConfigFile
	fi
	if ! grep -Fq "name_wechselrichter1=" $ConfigFile; then
		echo "name_wechselrichter1=WR1" >> $ConfigFile
	fi
	if ! grep -Fq "name_wechselrichter2=" $ConfigFile; then
		echo "name_wechselrichter2=WR2" >> $ConfigFile
	fi
	if ! grep -Fq "name_wechselrichter3=" $ConfigFile; then
		echo "name_wechselrichter3=WR3" >> $ConfigFile
	fi
	if ! grep -Fq "hook1ein_url=" $ConfigFile; then
		echo "hook1ein_url='https://webhook.com/ein.php'" >> $ConfigFile
	fi
	if ! grep -Fq "angesteckthooklp1_url=" $ConfigFile; then
		echo "angesteckthooklp1_url='https://webhook.com/ein.php'" >> $ConfigFile
	fi
	if ! grep -Fq "abgesteckthooklp1_url=" $ConfigFile; then
		echo "abgesteckthooklp1_url='https://webhook.com/aus.php'" >> $ConfigFile
	fi
	if ! grep -Fq "ladestarthooklp1_url=" $ConfigFile; then
		echo "ladestarthooklp1_url='https://webhook.com/ein.php'" >> $ConfigFile
	fi
	if ! grep -Fq "ladestophooklp1_url=" $ConfigFile; then
		echo "ladestophooklp1_url='https://webhook.com/aus.php'" >> $ConfigFile
	fi
	if ! grep -Fq "hook1aus_url=" $ConfigFile; then
		echo "hook1aus_url='https://webhook.com/aus.php'" >> $ConfigFile
	fi
	if ! grep -Fq "hook1_ausverz=" $ConfigFile; then
		echo "hook1_ausverz=0" >> $ConfigFile
	fi
	if ! grep -Fq "hook1ein_watt=" $ConfigFile; then
		echo "hook1ein_watt=1200" >> $ConfigFile
	fi
	if ! grep -Fq "hook1aus_watt=" $ConfigFile; then
		echo "hook1aus_watt=400" >> $ConfigFile
	fi
	if ! grep -Fq "hook1_aktiv=" $ConfigFile; then
		echo "hook1_aktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "angesteckthooklp1=" $ConfigFile; then
		echo "angesteckthooklp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "abgesteckthooklp1=" $ConfigFile; then
		echo "abgesteckthooklp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "ladestarthooklp1=" $ConfigFile; then
		echo "ladestarthooklp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "ladestophooklp1=" $ConfigFile; then
		echo "ladestophooklp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "hook1_dauer=" $ConfigFile; then
		echo "hook1_dauer=5" >> $ConfigFile
	fi
	if ! grep -Fq "hook2ein_url=" $ConfigFile; then
		echo "hook2ein_url='https://webhook.com/ein.php'" >> $ConfigFile
	fi
	if ! grep -Fq "hook2aus_url=" $ConfigFile; then
		echo "hook2aus_url='https://webhook.com/aus.php'" >> $ConfigFile
	fi
	if ! grep -Fq "hook2ein_watt=" $ConfigFile; then
		echo "hook2ein_watt=1200" >> $ConfigFile
	fi
	if ! grep -Fq "hook2aus_watt=" $ConfigFile; then
		echo "hook2aus_watt=400" >> $ConfigFile
	fi
	if ! grep -Fq "hook2_aktiv=" $ConfigFile; then
		echo "hook2_aktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "hook2_dauer=" $ConfigFile; then
		echo "hook2_dauer=5" >> $ConfigFile
	fi
	if ! grep -Fq "hook2_ausverz=" $ConfigFile; then
		echo "hook2_ausverz=0" >> $ConfigFile
	fi
	if ! grep -Fq "hook3ein_url=" $ConfigFile; then
		echo "hook3ein_url='https://webhook.com/ein.php'" >> $ConfigFile
	fi
	if ! grep -Fq "hook3aus_url=" $ConfigFile; then
		echo "hook3aus_url='https://webhook.com/aus.php'" >> $ConfigFile
	fi
	if ! grep -Fq "hook3ein_watt=" $ConfigFile; then
		echo "hook3ein_watt=1200" >> $ConfigFile
	fi
	if ! grep -Fq "hook3aus_watt=" $ConfigFile; then
		echo "hook3aus_watt=400" >> $ConfigFile
	fi
	if ! grep -Fq "hook3_aktiv=" $ConfigFile; then
		echo "hook3_aktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "hook3_dauer=" $ConfigFile; then
		echo "hook3_dauer=5" >> $ConfigFile
	fi
	if ! grep -Fq "hook3_ausverz=" $ConfigFile; then
		echo "hook3_ausverz=0" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher1_aktiv=" $ConfigFile; then
		echo "verbraucher1_aktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher1_typ=" $ConfigFile; then
		echo "verbraucher1_typ=http" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher1_name=" $ConfigFile; then
		echo "verbraucher1_name=Name" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher1_id=" $ConfigFile; then
		echo "verbraucher1_id=10" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher1_ip=" $ConfigFile; then
		echo "verbraucher1_ip=192.168.4.123" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher1_source=" $ConfigFile; then
		echo "verbraucher1_source=/dev/ttyUSB5" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher1_urlw=" $ConfigFile; then
		echo "verbraucher1_urlw='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher1_urlh=" $ConfigFile; then
		echo "verbraucher1_urlh='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher1_tempwh=" $ConfigFile; then
		echo "verbraucher1_tempwh=0" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher2_tempwh=" $ConfigFile; then
		echo "verbraucher2_tempwh=0" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher2_name=" $ConfigFile; then
		echo "verbraucher2_name=Name" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher2_aktiv=" $ConfigFile; then
		echo "verbraucher2_aktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher2_typ=" $ConfigFile; then
		echo "verbraucher2_typ=http" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher2_urlw=" $ConfigFile; then
		echo "verbraucher2_urlw='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher2_urlh=" $ConfigFile; then
		echo "verbraucher2_urlh='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher2_id=" $ConfigFile; then
		echo "verbraucher2_id=10" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher2_ip=" $ConfigFile; then
		echo "verbraucher2_ip=192.168.4.123" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher2_source=" $ConfigFile; then
		echo "verbraucher2_source=/dev/ttyUSB5" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher3_name=" $ConfigFile; then
		echo "verbraucher3_name=Name" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher3_aktiv=" $ConfigFile; then
		echo "verbraucher3_aktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher3_typ=" $ConfigFile; then
		echo "verbraucher3_typ=http" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher3_urlw=" $ConfigFile; then
		echo "verbraucher3_urlw='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "verbraucher3_urlh=" $ConfigFile; then
		echo "verbraucher3_urlh='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "nurpv70dynact=" $ConfigFile; then
		echo "nurpv70dynact=0" >> $ConfigFile
		echo "nurpv70dynw=6000" >> $ConfigFile
	fi
	if ! grep -Fq "nlakt_sofort=" $ConfigFile; then
		echo "nlakt_sofort=0" >> $ConfigFile
	fi
	if ! grep -Fq "nlakt_minpv=" $ConfigFile; then
		echo "nlakt_minpv=0" >> $ConfigFile
	fi
	if ! grep -Fq "nlakt_nurpv=" $ConfigFile; then
		echo "nlakt_nurpv=0" >> $ConfigFile
	fi
	if ! grep -Fq "nlakt_standby=" $ConfigFile; then
		echo "nlakt_standby=0" >> $ConfigFile
	fi
	if ! grep -Fq "mpm3pmevuhaus=" $ConfigFile; then
		echo "mpm3pmevuhaus=0" >> $ConfigFile
	fi
	if ! grep -Fq "carnetlp2user=" $ConfigFile; then
		echo "carnetlp2user='user'" >> $ConfigFile
	fi
	if ! grep -Fq "carnetlp2pass=" $ConfigFile; then
		echo "carnetlp2pass=''" >> $ConfigFile
	else
		sed -i "/carnetlp2pass='/b; s/^carnetlp2pass=\(.*\)/carnetlp2pass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soccarnetlp2intervall=" $ConfigFile; then
		echo "soccarnetlp2intervall=10" >> $ConfigFile
	fi
	if ! grep -Fq "soc_teslalp2_username=" $ConfigFile; then
		echo "soc_teslalp2_username=deine@email.com" >> $ConfigFile
	fi
	if ! grep -Fq "soc_teslalp2_carnumber=" $ConfigFile; then
		echo "soc_teslalp2_carnumber=0" >> $ConfigFile
	fi
	if ! grep -Fq "soc_teslalp2_password=" $ConfigFile; then
		echo "soc_teslalp2_password=''" >> $ConfigFile
	else
		sed -i "/soc_teslalp2_password='/b; s/^soc_teslalp2_password=\(.*\)/soc_teslalp2_password=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_teslalp2_intervallladen=" $ConfigFile; then
		echo "soc_teslalp2_intervallladen=20" >> $ConfigFile
	fi
	if ! grep -Fq "soc_teslalp2_intervall=" $ConfigFile; then
		echo "soc_teslalp2_intervall=20" >> $ConfigFile
	fi
	if ! grep -Fq "wrsma2ip=" $ConfigFile; then
		echo "wrsma2ip=none" >> $ConfigFile
	fi
	if ! grep -Fq "wrsma3ip=" $ConfigFile; then
		echo "wrsma3ip=none" >> $ConfigFile
	fi
	if ! grep -Fq "wrsma4ip=" $ConfigFile; then
		echo "wrsma4ip=none" >> $ConfigFile
	fi
	if ! grep -Fq "evuglaettung=" $ConfigFile; then
		echo "evuglaettung=10" >> $ConfigFile
	fi
	if ! grep -Fq "evuglaettungakt=" $ConfigFile; then
		echo "evuglaettungakt=0" >> $ConfigFile
	fi
	if ! grep -Fq "u1p3paktiv=" $ConfigFile; then
		echo "u1p3paktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "u1p3ppause=" $ConfigFile; then
		echo "u1p3ppause=2" >> $ConfigFile
	fi
	if ! grep -Fq "u1p3psofort=" $ConfigFile; then
		echo "u1p3psofort=3" >> $ConfigFile
	fi
	if ! grep -Fq "u1p3pstandby=" $ConfigFile; then
		echo "u1p3pstandby=3" >> $ConfigFile
	fi
	if ! grep -Fq "u1p3pnurpv=" $ConfigFile; then
		echo "u1p3pnurpv=1" >> $ConfigFile
	fi
	if ! grep -Fq "u1p3pminundpv=" $ConfigFile; then
		echo "u1p3pminundpv=1" >> $ConfigFile
	fi
	if ! grep -Fq "u1p3pnl=" $ConfigFile; then
		echo "u1p3pnl=3" >> $ConfigFile
	fi
	if ! grep -Fq "speicherpwip=" $ConfigFile; then
		echo "speicherpwip=192.168.0.10" >> $ConfigFile
	fi
	if ! grep -Fq "vartaspeicherip=" $ConfigFile; then
		echo "vartaspeicherip=192.168.0.10" >> $ConfigFile
	fi
	if ! grep -Fq "vartaspeicher2ip=" $ConfigFile; then
		echo "vartaspeicher2ip=none" >> $ConfigFile
	fi
	if ! grep -Fq "usevartamodbus=" $ConfigFile; then
		echo "usevartamodbus=0" >> $ConfigFile
	fi
	if ! grep -Fq "adaptpv=" $ConfigFile; then
		echo "adaptpv=0" >> $ConfigFile
	fi
	if ! grep -Fq "adaptfaktor=" $ConfigFile; then
		echo "adaptfaktor=5" >> $ConfigFile
	fi
	if ! grep -Fq "grapham=" $ConfigFile; then
		echo "grapham=0" >> $ConfigFile
	fi
	if ! grep -Fq "graphliveam=" $ConfigFile; then
		echo "graphliveam=0" >> $ConfigFile
	fi
	if ! grep -Fq "nrgkickiplp1=" $ConfigFile; then
		echo "nrgkickiplp1=192.168.0.17" >> $ConfigFile
	fi
	if ! grep -Fq "nrgkicktimeoutlp1=" $ConfigFile; then
		echo "nrgkicktimeoutlp1=3" >> $ConfigFile
	fi
	if ! grep -Fq "nrgkickmaclp1=" $ConfigFile; then
		echo "nrgkickmaclp1=11:22:33:aa:bb:cc" >> $ConfigFile
	fi
	if ! grep -Fq "nrgkickpwlp1=" $ConfigFile; then
		echo "nrgkickpwlp1=1234" >> $ConfigFile
	fi
	if ! grep -Fq "kostalplenticorehaus=" $ConfigFile; then
		echo "kostalplenticorehaus=0" >> $ConfigFile
	fi
	if ! grep -Fq "kostalplenticorebatt=" $ConfigFile; then
		echo "kostalplenticorebatt=0" >> $ConfigFile
	fi
	if ! grep -Fq "froniuserzeugung=" $ConfigFile; then
		echo "froniuserzeugung=0" >> $ConfigFile
	fi
	if ! grep -Fq "froniusvar2=" $ConfigFile; then
		echo "froniusvar2=0" >> $ConfigFile
	fi
	if ! grep -Fq "kebaiplp1=" $ConfigFile; then
		echo "kebaiplp1=192.168.25.25" >> $ConfigFile
	fi
	if ! grep -Fq "kebaiplp2=" $ConfigFile; then
		echo "kebaiplp2=192.168.25.25" >> $ConfigFile
	fi
	if ! grep -Fq "graphinteractiveam=" $ConfigFile; then
		echo "graphinteractiveam=1" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_smartfox_ip=" $ConfigFile; then
		echo "bezug_smartfox_ip=192.168.0.50" >> $ConfigFile
	fi
	if ! grep -Fq "chartlegendmain=" $ConfigFile; then
		echo "chartlegendmain=1" >> $ConfigFile
	fi
	if ! grep -Fq "nrgkickiplp2=" $ConfigFile; then
		echo "nrgkickiplp2=192.168.0.17" >> $ConfigFile
	fi
	if ! grep -Fq "nrgkicktimeoutlp2=" $ConfigFile; then
		echo "nrgkicktimeoutlp2=3" >> $ConfigFile
	fi
	if ! grep -Fq "nrgkickmaclp2=" $ConfigFile; then
		echo "nrgkickmaclp2=11:22:33:aa:bb:cc" >> $ConfigFile
	fi
	if ! grep -Fq "nrgkickpwlp2=" $ConfigFile; then
		echo "nrgkickpwlp2=1234" >> $ConfigFile
	fi
	if ! grep -Fq "hausverbrauchstat=" $ConfigFile; then
		echo "hausverbrauchstat=1" >> $ConfigFile
	fi
	if ! grep -Fq "theme=" $ConfigFile; then
		echo "theme=standard" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgewr2ip=" $ConfigFile; then
		echo "solaredgewr2ip=none" >> $ConfigFile
	fi
	if ! grep -Fq "heutegeladen=" $ConfigFile; then
		echo "heutegeladen=1" >> $ConfigFile
	fi
	if ! grep -Fq "sunnyislandip=" $ConfigFile; then
		echo "sunnyislandip=192.168.0.17" >> $ConfigFile
	fi
	if ! grep -Fq "bezug1_ip=" $ConfigFile; then
		{
			echo "bezug1_ip=192.168.0.17"
			echo "pv1_ipa=192.168.0.17"
			echo "pv1_ipb=192.168.0.17"
			echo "pv1_ipc=192.168.0.17"
			echo "pv1_ipd=192.168.0.17"
			echo "pv1_ida=1"
			echo "pv1_idb=1"
			echo "pv1_idc=1"
			echo "pv1_idd=1"
			echo "speicher1_ip=192.168.0.17"
		} >> $ConfigFile
	fi
	if ! grep -Fq "pv1_ida=" $ConfigFile; then
		echo "pv1_ida=1" >> $ConfigFile
	fi

	if ! grep -Fq "speicher1_ip2=" $ConfigFile; then
		echo "speicher1_ip2=192.168.0.17" >> $ConfigFile
	fi
	if ! grep -Fq "fsm63a3modbusllsource=" $ConfigFile; then
		echo "fsm63a3modbusllsource=/dev/ttyUSB2" >> $ConfigFile
	fi
	if ! grep -Fq "fsm63a3modbusllid=" $ConfigFile; then
		echo "fsm63a3modbusllid=8" >> $ConfigFile
	fi
	if ! grep -Fq "wakeupzoelp1=" $ConfigFile; then
		echo "wakeupzoelp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "wakeupzoelp2=" $ConfigFile; then
		echo "wakeupzoelp2=0" >> $ConfigFile
	fi
	if ! grep -Fq "wakeupmyrenaultlp1=" $ConfigFile; then
		echo "wakeupmyrenaultlp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "wakeupmyrenaultlp2=" $ConfigFile; then
		echo "wakeupmyrenaultlp2=0" >> $ConfigFile
	fi
	if ! grep -Fq "awattarlocation=" $ConfigFile; then
		echo "awattarlocation=de" >> $ConfigFile
	fi
	# upgrade from awattar to electricity tariff provider
	if ! grep -Fq "etprovideraktiv=" $ConfigFile; then
		if grep -Fq "awattaraktiv=1" $ConfigFile; then
			echo "etprovideraktiv=1" >> $ConfigFile
			echo "etprovider=et_awattar" >> $ConfigFile
		else
			echo "etprovideraktiv=0" >> $ConfigFile
		fi
	fi
	# tibber demo settings
	if ! grep -Fq "tibbertoken=" $ConfigFile; then
		echo "tibbertoken=5K4MVS-OjfWhK_4yrjOlFe1F6kJXPVf7eQYggo8ebAE" >> $ConfigFile
		echo "tibberhomeid=96a14971-525a-4420-aae9-e5aedaa129ff" >> $ConfigFile
	else
		# replace outdated demo account (2022-10-19)
		sed -i "s/^tibbertoken=d1007ead2dc84a2b82f0de19451c5fb22112f7ae11d19bf2bedb224a003ff74a/tibbertoken=5K4MVS-OjfWhK_4yrjOlFe1F6kJXPVf7eQYggo8ebAE/g" $ConfigFile
		sed -i "s/^tibberhomeid=c70dcbe5-4485-4821-933d-a8a86452737b/tibberhomeid=96a14971-525a-4420-aae9-e5aedaa129ff/g" $ConfigFile
	fi
	if ! grep -Fq "etprovider=" $ConfigFile; then
		echo "etprovider=et_awattar" >> $ConfigFile
	fi
	# remove obsolete line from config
	if grep -Fq "awattaraktiv=" $ConfigFile; then
		sed -i '/^awattaraktiv=/d' $ConfigFile
	fi
	for i in $(seq 1 8); do
		if ! grep -Fq "lp${i}etbasedcharging=" $ConfigFile; then
			echo "lp${i}etbasedcharging=1" >> $ConfigFile
		fi
	done
	if ! grep -Fq "plz=" $ConfigFile; then
		echo "plz=36124" >> $ConfigFile
	fi
	if ! grep -Fq "pushbplug=" $ConfigFile; then
		echo "pushbplug=0" >> $ConfigFile
	fi
	if ! grep -Fq "wrsmawebbox=" $ConfigFile; then
		echo "wrsmawebbox=0" >> $ConfigFile
	fi
	if ! grep -Fq "wrsmahybrid=" $ConfigFile; then
		echo "wrsmahybrid=0" >> $ConfigFile
	fi
	if ! grep -Fq "bootmodus=" $ConfigFile; then
		echo "bootmodus=3" >> $ConfigFile
	fi
	if ! grep -Fq "httpll_w_url=" $ConfigFile; then
		echo "httpll_w_url='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "httpll_ip=" $ConfigFile; then
		echo "httpll_ip=192.168.0.22" >> $ConfigFile
	fi
	if ! grep -Fq "httpll_kwh_url=" $ConfigFile; then
		echo "httpll_kwh_url='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "httpll_a1_url=" $ConfigFile; then
		echo "httpll_a1_url='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "httpll_a2_url=" $ConfigFile; then
		echo "httpll_a2_url='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "httpll_a3_url=" $ConfigFile; then
		echo "httpll_a3_url='http://url'" >> $ConfigFile
	fi
	if ! grep -Fq "clouduser=" $ConfigFile; then
		echo "clouduser=leer" >> $ConfigFile
	fi
	if ! grep -Fq "cloudpw=" $ConfigFile; then
		echo "cloudpw=leer" >> $ConfigFile
	fi
	if ! grep -Fq "rfidakt=" $ConfigFile; then
		echo "rfidakt=0" >> $ConfigFile
	fi
	if ! grep -Fq "rfidsofort=" $ConfigFile; then
		echo "rfidsofort=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidlp1start1=" $ConfigFile; then
		{
			echo "rfidlp1start1=000"
			echo "rfidlp1start2=000"
			echo "rfidlp1start3=000"
			echo "rfidlp2start1=000"
			echo "rfidlp2start2=000"
			echo "rfidlp2start3=000"
		} >> $ConfigFile
	fi
	if ! grep -Fq "rfidlp1start4=" $ConfigFile; then
		{
			echo "rfidlp1start4=000"
			echo "rfidlp1start5=000"
			echo "rfidlp2start4=000"
			echo "rfidlp2start5=000"
		} >> $ConfigFile
	fi
	if ! grep -Fq "rfidstandby=" $ConfigFile; then
		echo "rfidstandby=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidstop=" $ConfigFile; then
		echo "rfidstop=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidnurpv=" $ConfigFile; then
		echo "rfidnurpv=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidminpv=" $ConfigFile; then
		echo "rfidminpv=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidsofort2=" $ConfigFile; then
		echo "rfidsofort2=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidstandby2=" $ConfigFile; then
		echo "rfidstandby2=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidstop2=" $ConfigFile; then
		echo "rfidstop2=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidnurpv2=" $ConfigFile; then
		echo "rfidnurpv2=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidminpv2=" $ConfigFile; then
		echo "rfidminpv2=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidsofort3=" $ConfigFile; then
		echo "rfidsofort3=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidstandby3=" $ConfigFile; then
		echo "rfidstandby3=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidstop3=" $ConfigFile; then
		echo "rfidstop3=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidnurpv3=" $ConfigFile; then
		echo "rfidnurpv3=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidminpv3=" $ConfigFile; then
		echo "rfidminpv3=000" >> $ConfigFile
	fi
	if ! grep -Fq "rfidlp1c1=" $ConfigFile; then
		echo "rfidlp1c1=0" >> $ConfigFile
	fi
	if ! grep -Fq "rfidlp1c2=" $ConfigFile; then
		echo "rfidlp1c2=0" >> $ConfigFile
	fi
	if ! grep -Fq "rfidlp1c3=" $ConfigFile; then
		echo "rfidlp1c3=0" >> $ConfigFile
	fi
	if ! grep -Fq "rfidlp2c1=" $ConfigFile; then
		echo "rfidlp2c1=0" >> $ConfigFile
	fi
	if ! grep -Fq "rfidlp2c2=" $ConfigFile; then
		echo "rfidlp2c2=0" >> $ConfigFile
	fi
	if ! grep -Fq "rfidlp2c3=" $ConfigFile; then
		echo "rfidlp2c3=0" >> $ConfigFile
	fi
	if ! grep -Fq "wr_sdm120ip=" $ConfigFile; then
		echo "wr_sdm120ip=192.168.3.5" >> $ConfigFile
	fi
	if ! grep -Fq "wr_sdm120id=" $ConfigFile; then
		echo "wr_sdm120id=2" >> $ConfigFile
	fi
	if ! grep -Fq "bezug_victronip=" $ConfigFile; then
		echo "bezug_victronip=192.168.15.3" >> $ConfigFile
	fi
	if ! grep -Fq "victron_energy_meter=" $ConfigFile; then
		echo "victron_energy_meter=1" >> $ConfigFile
	fi
	if ! grep -Fq "pushbsmarthome=" $ConfigFile; then
		echo "pushbsmarthome=1" >> $ConfigFile
	fi
	if ! grep -Fq "graphsocdyn=" $ConfigFile; then
		echo "graphsocdyn=1" >> $ConfigFile
	fi
	if ! grep -Fq "ledsakt=" $ConfigFile; then
		echo "ledsakt=0" >> $ConfigFile
	fi
	if ! grep -Fq "led0sofort=" $ConfigFile; then
		echo "led0sofort=aus" >> $ConfigFile
	fi
	if ! grep -Fq "led0minpv=" $ConfigFile; then
		echo "led0minpv=aus" >> $ConfigFile
	fi
	if ! grep -Fq "led0nurpv=" $ConfigFile; then
		echo "led0nurpv=aus" >> $ConfigFile
	fi
	if ! grep -Fq "led0stop=" $ConfigFile; then
		echo "led0stop=aus" >> $ConfigFile
	fi
	if ! grep -Fq "led0standby=" $ConfigFile; then
		echo "led0standby=aus" >> $ConfigFile
	fi
	if ! grep -Fq "ledsofort=" $ConfigFile; then
		echo "ledsofort=aus" >> $ConfigFile
	fi
	if ! grep -Fq "ledminpv=" $ConfigFile; then
		echo "ledminpv=aus" >> $ConfigFile
	fi
	if ! grep -Fq "lednurpv=" $ConfigFile; then
		echo "lednurpv=aus" >> $ConfigFile
	fi
	if ! grep -Fq "ledstop=" $ConfigFile; then
		echo "ledstop=aus" >> $ConfigFile
	fi
	if ! grep -Fq "ledstandby=" $ConfigFile; then
		echo "ledstandby=aus" >> $ConfigFile
	fi
	if ! grep -Fq "displayconfigured=" $ConfigFile; then
		echo "displayconfigured=0" >> $ConfigFile
	fi
	if ! grep -Fq "displayaktiv=" $ConfigFile; then
		echo "displayaktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "displaysleep=" $ConfigFile; then
		echo "displaysleep=60" >> $ConfigFile
	fi
	if ! grep -Fq "displayevumax=" $ConfigFile; then
		echo "displayevumax=5000" >> $ConfigFile
	fi
	if ! grep -Fq "displaypvmax=" $ConfigFile; then
		echo "displaypvmax=10000" >> $ConfigFile
	fi
	if ! grep -Fq "displayspeichermax=" $ConfigFile; then
		echo "displayspeichermax=3000" >> $ConfigFile
	fi
	if ! grep -Fq "displayhausanzeigen=" $ConfigFile; then
		echo "displayhausanzeigen=1" >> $ConfigFile
	fi
	if ! grep -Fq "displayhausmax=" $ConfigFile; then
		echo "displayhausmax=5000" >> $ConfigFile
	fi
	if ! grep -Fq "displaylp1max=" $ConfigFile; then
		echo "displaylp1max=22000" >> $ConfigFile
	fi
	if ! grep -Fq "displaylp2max=" $ConfigFile; then
		echo "displaylp2max=22000" >> $ConfigFile
	fi
	if ! grep -Fq "displaypinaktiv=" $ConfigFile; then
		echo "displaypinaktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "displaypincode=" $ConfigFile; then
		echo "displaypincode=1234" >> $ConfigFile
	fi
	if ! grep -Fq "settingspw=" $ConfigFile; then
		echo "settingspw='openwb'" >> $ConfigFile
	fi
	if ! grep -Fq "settingspwakt=" $ConfigFile; then
		echo "settingspwakt=0" >> $ConfigFile
	fi
	if ! grep -Fq "netzabschaltunghz=" $ConfigFile; then
		echo "netzabschaltunghz=1" >> $ConfigFile
	fi
	if ! grep -Fq "cpunterbrechunglp1=" $ConfigFile; then
		echo "cpunterbrechunglp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "cpunterbrechungdauerlp1=" $ConfigFile; then
		echo "cpunterbrechungdauerlp1=4" >> $ConfigFile
	fi
	if ! grep -Fq "cpunterbrechunglp2=" $ConfigFile; then
		echo "cpunterbrechunglp2=0" >> $ConfigFile
	fi
	if ! grep -Fq "cpunterbrechungdauerlp2=" $ConfigFile; then
		echo "cpunterbrechungdauerlp2=4" >> $ConfigFile
	fi
	if ! grep -Fq "soc_zerong_username=" $ConfigFile; then
		echo "soc_zerong_username=deine@email.com" >> $ConfigFile
	fi
	if ! grep -Fq "soc_zerong_password=" $ConfigFile; then
		echo "soc_zerong_password=''" >> $ConfigFile
	else
		sed -i "/soc_zerong_password='/b; s/^soc_zerong_password=\(.*\)/soc_zerong_password=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_zerong_intervallladen=" $ConfigFile; then
		echo "soc_zerong_intervallladen=10" >> $ConfigFile
	fi
	if ! grep -Fq "soc_zerong_intervall=" $ConfigFile; then
		echo "soc_zerong_intervall=20" >> $ConfigFile
	fi
	if ! grep -Fq "soc_zeronglp2_username=" $ConfigFile; then
		echo "soc_zeronglp2_username=" >> $ConfigFile
	fi
	if ! grep -Fq "soc_zeronglp2_password=" $ConfigFile; then
		echo "soc_zeronglp2_password=''" >> $ConfigFile
	else
		sed -i "/soc_zeronglp2_password='/b; s/^soc_zeronglp2_password=\(.*\)/soc_zeronglp2_password=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_zeronglp2_intervallladen=" $ConfigFile; then
		echo "soc_zeronglp2_intervallladen=10" >> $ConfigFile
	fi
	if ! grep -Fq "soc_zeronglp2_intervall=" $ConfigFile; then
		echo "soc_zeronglp2_intervall=20" >> $ConfigFile
	fi
	if ! grep -Fq "solarview_hostname=" $ConfigFile; then
		echo "solarview_hostname=192.168.0.31" >> $ConfigFile
	fi
	if ! grep -Fq "solarview_port=" $ConfigFile; then
		echo "solarview_port=15000" >> $ConfigFile
	fi
	if ! grep -Fq "solarview_timeout=" $ConfigFile; then
		echo "solarview_timeout=1" >> $ConfigFile
	fi
	if ! grep -Fq "solarview_command_wr=" $ConfigFile; then
		echo "solarview_command_wr=00*" >> $ConfigFile
	fi
	if ! grep -Fq "discovergyuser=" $ConfigFile; then
		echo "discovergyuser=name@mail.de" >> $ConfigFile
	fi
	if ! grep -Fq "discovergypass=" $ConfigFile; then
		echo "discovergypass=''" >> $ConfigFile
	else
		sed -i "/discovergypass='/b; s/^discovergypass=\(.*\)/discovergypass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "discovergyevuid=" $ConfigFile; then
		echo "discovergyevuid=idesmeters" >> $ConfigFile
	fi
	if ! grep -Fq "discovergypvid=" $ConfigFile; then
		echo "discovergypvid=idesmeters" >> $ConfigFile
	fi
	if ! grep -Fq "powerfoxuser=" $ConfigFile; then
		echo "powerfoxuser=name@mail.de" >> $ConfigFile
	fi
	if ! grep -Fq "powerfoxpass=" $ConfigFile; then
		echo "powerfoxpass=''" >> $ConfigFile
	else
		sed -i "/powerfoxpass='/b; s/^powerfoxpass=\(.*\)/powerfoxpass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "powerfoxid=" $ConfigFile; then
		echo "powerfoxid=idesmeters" >> $ConfigFile
	fi
	if ! grep -Fq "powerfoxpvid=" $ConfigFile; then
		echo "powerfoxpvid=idesmeters" >> $ConfigFile
	fi
	if ! grep -Fq "ksemip=" $ConfigFile; then
		echo "ksemip=ipdesmeters" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1moab=" $ConfigFile; then
		echo "mollp1moab=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1mobis=" $ConfigFile; then
		echo "mollp1mobis=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1diab=" $ConfigFile; then
		echo "mollp1diab=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1dibis=" $ConfigFile; then
		echo "mollp1dibis=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1miab=" $ConfigFile; then
		echo "mollp1miab=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1mibis=" $ConfigFile; then
		echo "mollp1mibis=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1doab=" $ConfigFile; then
		echo "mollp1doab=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1dobis=" $ConfigFile; then
		echo "mollp1dobis=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1frab=" $ConfigFile; then
		echo "mollp1frab=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1frbis=" $ConfigFile; then
		echo "mollp1frbis=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1sabis=" $ConfigFile; then
		echo "mollp1sabis=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1soab=" $ConfigFile; then
		echo "mollp1soab=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1sobis=" $ConfigFile; then
		echo "mollp1sobis=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1saab=" $ConfigFile; then
		echo "mollp1saab=06:00" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1moll=" $ConfigFile; then
		echo "mollp1moll=13" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1dill=" $ConfigFile; then
		echo "mollp1dill=13" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1mill=" $ConfigFile; then
		echo "mollp1mill=13" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1doll=" $ConfigFile; then
		echo "mollp1doll=13" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1frll=" $ConfigFile; then
		echo "mollp1frll=13" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1sall=" $ConfigFile; then
		echo "mollp1sall=13" >> $ConfigFile
	fi
	if ! grep -Fq "mollp1soll=" $ConfigFile; then
		echo "mollp1soll=13" >> $ConfigFile
	fi
	if ! grep -Fq "wryoulessip=" $ConfigFile; then
		echo "wryoulessip=192.168.0.3" >> $ConfigFile
	fi
	if ! grep -Fq "wryoulessalt=" $ConfigFile; then
		echo "wryoulessalt=0" >> $ConfigFile
	fi
	if ! grep -Fq "soc_audi_username=" $ConfigFile; then
		echo "soc_audi_username=demo@demo.de" >> $ConfigFile
	fi
	if ! grep -Fq "soc_audi_passwort=" $ConfigFile; then
		echo "soc_audi_passwort=''" >> $ConfigFile
	else
		sed -i "/soc_audi_passwort='/b; s/^soc_audi_passwort=\(.*\)/soc_audi_passwort=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_audi_vin=" $ConfigFile; then
		echo "soc_audi_vin=VIN" >> $ConfigFile
	fi
	if ! grep -Fq "soc2user=" $ConfigFile; then
		echo "soc2user=demo@demo.de" >> $ConfigFile
	fi
	if ! grep -Fq "soc2pass=" $ConfigFile; then
		echo "soc2pass=''" >> $ConfigFile
	else
		sed -i "/soc2pass='/b; s/^soc2pass=\(.*\)/soc2pass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc2pin=" $ConfigFile; then
		echo "soc2pin=pin" >> $ConfigFile
	fi
	if ! grep -Fq "lgessv1ip=" $ConfigFile; then
		echo "lgessv1ip=youripaddress" >> $ConfigFile
	fi
	if ! grep -Fq "lgessv1pass=" $ConfigFile; then
		echo "lgessv1pass='regnum_as_default_password'" >> $ConfigFile
	else
		sed -i "/lgessv1pass='/b; s/^lgessv1pass=\(.*\)/lgessv1pass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "ess_api_ver=" $ConfigFile; then
		echo "ess_api_ver=01.2020" >> $ConfigFile
	fi
	if ! grep -Fq "mpmlp4ip=" $ConfigFile; then
		{
			echo "mpmlp4ip=192.168.193.54"
			echo "mpmlp5ip=192.168.193.55"
			echo "mpmlp6ip=192.168.193.56"
			echo "mpmlp7ip=192.168.193.57"
			echo "mpmlp8ip=192.168.193.58"
			echo "mpmlp4id=14"
			echo "mpmlp5id=15"
			echo "mpmlp6id=16"
			echo "mpmlp7id=17"
			echo "mpmlp8id=18"
			echo "lastmanagementlp4=0"
			echo "lastmanagementlp5=0"
			echo "lastmanagementlp6=0"
			echo "lastmanagementlp7=0"
			echo "lastmanagementlp8=0"
			echo "evseconlp4=none"
			echo "evseconlp5=none"
			echo "evseconlp6=none"
			echo "evseconlp7=none"
			echo "evseconlp8=none"
			echo "evseidlp4=24"
			echo "evseidlp5=25"
			echo "evseidlp6=26"
			echo "evseidlp7=27"
			echo "evseidlp8=28"
			echo "evseiplp4=192.168.193.44"
			echo "evseiplp5=192.168.193.45"
			echo "evseiplp6=192.168.193.46"
			echo "evseiplp7=192.168.193.47"
			echo "evseiplp8=192.168.193.48"
			echo "sofortlllp4=13"
			echo "sofortlllp5=13"
			echo "sofortlllp6=13"
			echo "sofortlllp7=13"
			echo "sofortlllp8=13"
			echo "lademkwhlp4=10"
			echo "lademkwhlp5=10"
			echo "lademkwhlp6=10"
			echo "lademkwhlp7=10"
			echo "lademkwhlp8=10"
			echo "durchslp4=20"
			echo "durchslp5=20"
			echo "durchslp6=20"
			echo "durchslp7=20"
			echo "durchslp8=20"
			echo "evseidlp1=21"
			echo "evseidlp2=22"
			echo "evseidlp3=23"
			echo "evseiplp1=192.168.193.41"
			echo "evseiplp2=192.168.193.42"
			echo "evseiplp3=192.168.193.43"
			echo "mpmlp1ip=192.168.193.51"
			echo "mpmlp2ip=192.168.193.52"
			echo "mpmlp3ip=192.168.193.53"
			echo "mpmlp1id=11"
			echo "mpmlp2id=12"
			echo "mpmlp3id=13"
			echo "lp4name=LP4"
			echo "lp5name=LP5"
			echo "lp6name=LP6"
			echo "lp7name=LP7"
			echo "lp8name=LP8"
			echo "simplemode=0"
			echo "lademstatlp4=01"
			echo "lademstatlp5=0"
			echo "lademstatlp6=0"
			echo "lademstatlp7=0"
			echo "lademstatlp8=0"
		} >> $ConfigFile
	fi
	if ! grep -Fq "stopchargeafterdisclp1=" $ConfigFile; then
		{
			echo "stopchargeafterdisclp1=0"
			echo "stopchargeafterdisclp2=0"
			echo "stopchargeafterdisclp3=0"
			echo "stopchargeafterdisclp4=0"
			echo "stopchargeafterdisclp5=0"
			echo "stopchargeafterdisclp6=0"
			echo "stopchargeafterdisclp7=0"
			echo "stopchargeafterdisclp8=0"
		} >> $ConfigFile
	fi
	if ! grep -Fq "myrenault_userlp1=" $ConfigFile; then
		{
			echo "myrenault_userlp1=Benutzername"
			echo "myrenault_passlp1=''"
			echo "myrenault_locationlp1=de_DE"
			echo "myrenault_countrylp1=DE"
			echo "myrenault_userlp2=Benutzername"
			echo "myrenault_passlp2=''"
			echo "myrenault_locationlp2=de_DE"
			echo "myrenault_countrylp2=DE"
		} >> $ConfigFile
	else
		sed -i "/myrenault_passlp1='/b; s/^myrenault_passlp1=\(.*\)/myrenault_passlp1=\'\1\'/g" $ConfigFile
		sed -i "/myrenault_passlp2='/b; s/^myrenault_passlp2=\(.*\)/myrenault_passlp2=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "evukitversion=" $ConfigFile; then
		echo "evukitversion=0" >> $ConfigFile
	fi
	if ! grep -Fq "speicherkitversion=" $ConfigFile; then
		echo "speicherkitversion=0" >> $ConfigFile
	fi
	if ! grep -Fq "pvkitversion=" $ConfigFile; then
		echo "pvkitversion=0" >> $ConfigFile
	fi
	if ! grep -Fq "pv2kitversion=" $ConfigFile; then
		echo "pv2kitversion=0" >> $ConfigFile
	fi
	if ! grep -Fq "wrsunwayspw=" $ConfigFile; then
		echo "wrsunwayspw=''" >> $ConfigFile
	fi
	if ! grep -Fq "e3dcextprod=" $ConfigFile; then
		echo "e3dcextprod=0" >> $ConfigFile
	fi
	if ! grep -Fq "schieflastmaxa=" $ConfigFile; then
		echo "schieflastmaxa=20" >> $ConfigFile
	fi
	if ! grep -Fq "schieflastaktiv=" $ConfigFile; then
		echo "schieflastaktiv=0" >> $ConfigFile
	fi
	if ! grep -Fq "wrsunwaysip=" $ConfigFile; then
		echo "wrsunwaysip=192.168.0.10" >> $ConfigFile
	fi
	if ! grep -Fq "lastmmaxw=" $ConfigFile; then
		echo "lastmmaxw=44000" >> $ConfigFile
	fi
	if ! grep -Fq "slavemode=" $ConfigFile; then
		echo "slavemode=0" >> $ConfigFile
	fi
	if ! grep -Fq "slaveModeUseLastChargingPhase=" $ConfigFile; then
		echo "slaveModeUseLastChargingPhase=1" >> $ConfigFile
	fi
	if ! grep -Fq "slaveModeSlowRamping=" $ConfigFile; then
		echo "slaveModeSlowRamping=1" >> $ConfigFile
	fi
	if ! grep -Fq "slaveModeMinimumAdjustmentInterval=" $ConfigFile; then
		echo "slaveModeMinimumAdjustmentInterval=15" >> $ConfigFile
	fi
	if ! grep -Fq "standardSocketInstalled=" /var/www/html/openWB/openwb.conf
	then
		echo "standardSocketInstalled=0" >> /var/www/html/openWB/openwb.conf
	fi
	if ! grep -Fq "sdm120modbussocketsource=" $ConfigFile; then
		echo "sdm120modbussocketsource=/dev/ttyUSB0" >> $ConfigFile
	fi
	if ! grep -Fq "sdm120modbussocketid=" $ConfigFile; then
		echo "sdm120modbussocketid=9" >> $ConfigFile
	fi
	if ! grep -Fq "solarworld_emanagerip=" $ConfigFile; then
		echo "solarworld_emanagerip=192.192.192.192" >> $ConfigFile
	fi
	if ! grep -Fq "femsip=" $ConfigFile; then
		echo "femsip=192.168.1.23" >> $ConfigFile
	fi
	if ! grep -Fq "femskacopw=" $ConfigFile; then
		echo "femskacopw=user" >> $ConfigFile
	fi
	if ! grep -Fq "pv2wattmodul=" $ConfigFile; then
		echo "pv2wattmodul=none" >> $ConfigFile
	fi
	if ! grep -Fq "pv2ip2=" $ConfigFile; then
		{
			echo "pv2ip2=192.168.192.192"
			echo "pv2id2=0"
		} >> $ConfigFile
	fi
	if ! grep -Fq "pv2port=" $ConfigFile; then
		echo "pv2port=502" >> $ConfigFile
	fi
	if ! grep -Fq "pv2ip=" $ConfigFile; then
		{
			echo "pv2ip=none"
			echo "pv2id=1"
			echo "pv2user=none"
			echo "pv2pass=''"
		} >> $ConfigFile
	else
		sed -i "/pv2pass='/b; s/^pv2pass=\(.*\)/pv2pass=\'\1\'/g" $ConfigFile
	fi
	if grep -Fq "pv2id=none" $ConfigFile; then
		sed -i "s/^pv2id=none/pv2id=1/g" $ConfigFile
	fi
	if ! grep -Fq "soc_bluelink_email=" $ConfigFile; then
		{
			echo "soc_bluelink_email=mail@mail.de"
			echo "soc_bluelink_password=''"
			echo "soc_bluelink_pin=1111"
			echo "soc_bluelink_interval=30"
		} >> $ConfigFile
	else
		sed -i "/soc_bluelink_password='/b; s/^soc_bluelink_password=\(.*\)/soc_bluelink_password=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_vin=" $ConfigFile; then
		echo "soc_vin=VIN" >> $ConfigFile
	fi
	if ! grep -Fq "kia_soccalclp1=" $ConfigFile; then
		echo "kia_soccalclp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "kia_soccalclp2=" $ConfigFile; then
		echo "kia_soccalclp2=0" >> $ConfigFile
	fi
	if ! grep -Fq "kia_abrp_enable=" $ConfigFile; then
		echo "kia_abrp_enable=0" >> $ConfigFile
	fi
	if ! grep -Fq "kia_abrp_token=" $ConfigFile; then
		echo "kia_abrp_token=''" >> $ConfigFile
	fi
	if ! grep -Fq "kia_abrp_enable_2=" $ConfigFile; then
		echo "kia_abrp_enable_2=0" >> $ConfigFile
	fi
	if ! grep -Fq "kia_abrp_token_2=" $ConfigFile; then
		echo "kia_abrp_token_2=''" >> $ConfigFile
	fi
	if ! grep -Fq "kia_advanced=" $ConfigFile; then
		echo "kia_advanced=0" >> $ConfigFile
	fi
	if ! grep -Fq "kia_advanced2=" $ConfigFile; then
		echo "kia_advanced2=0" >> $ConfigFile
	fi
	if ! grep -Fq "kia_adv_cachevalid=" $ConfigFile; then
		echo "kia_adv_cachevalid=10" >> $ConfigFile
	fi
	if ! grep -Fq "kia_adv_cachevalid2=" $ConfigFile; then
		echo "kia_adv_cachevalid2=10" >> $ConfigFile
	fi
	if ! grep -Fq "kia_adv_12v=" $ConfigFile; then
		echo "kia_adv_12v=20" >> $ConfigFile
	fi
	if ! grep -Fq "kia_adv_12v2=" $ConfigFile; then
		echo "kia_adv_12v2=20" >> $ConfigFile
	fi
	if ! grep -Fq "kia_adv_interval_unplug=" $ConfigFile; then
		echo "kia_adv_interval_unplug=360" >> $ConfigFile
	fi
	if ! grep -Fq "kia_adv_interval_unplug2=" $ConfigFile; then
		echo "kia_adv_interval_unplug2=360" >> $ConfigFile
	fi
	if ! grep -Fq "kia_adv_ratelimit=" $ConfigFile; then
		echo "kia_adv_ratelimit=15" >> $ConfigFile
	fi
	if ! grep -Fq "kia_adv_ratelimit2=" $ConfigFile; then
		echo "kia_adv_ratelimit2=15" >> $ConfigFile
	fi
	if ! grep -Fq "isss=" $ConfigFile; then
		echo "isss=0" >> $ConfigFile
	fi
	if ! grep -Fq "ssdisplay=" $ConfigFile; then
		echo "ssdisplay=0" >> $ConfigFile
	fi
	if ! grep -Fq "owbpro1ip=" $ConfigFile; then
		{
			echo "owbpro1ip=192.168.1.100"
			echo "owbpro2ip=192.168.1.100"
			echo "owbpro3ip=192.168.1.100"
			echo "owbpro4ip=192.168.1.100"
			echo "owbpro5ip=192.168.1.100"
			echo "owbpro6ip=192.168.1.100"
			echo "owbpro7ip=192.168.1.100"
			echo "owbpro8ip=192.168.1.100"
		} >> $ConfigFile
	fi
	if ! grep -Fq "chargep1ip=" $ConfigFile; then
		echo "chargep1ip=192.168.1.100" >> $ConfigFile
	fi
	if ! grep -Fq "chargep1cp=" $ConfigFile; then
		{
			echo "chargep1cp=1"
			echo "chargep2cp=1"
			echo "chargep3cp=1"
			echo "chargep4cp=1"
			echo "chargep5cp=1"
			echo "chargep6cp=1"
			echo "chargep7cp=1"
			echo "chargep8cp=1"
		} >> $ConfigFile
	fi
	if ! grep -Fq "chargep2ip=" $ConfigFile; then
		echo "chargep2ip=192.168.1.100" >> $ConfigFile
	fi
	if ! grep -Fq "chargep3ip=" $ConfigFile; then
		echo "chargep3ip=192.168.1.100" >> $ConfigFile
	fi
	if ! grep -Fq "chargep4ip=" $ConfigFile; then
		echo "chargep4ip=192.168.1.100" >> $ConfigFile
	fi
	if ! grep -Fq "chargep5ip=" $ConfigFile; then
		echo "chargep5ip=192.168.1.100" >> $ConfigFile
	fi
	if ! grep -Fq "chargep6ip=" $ConfigFile; then
		echo "chargep6ip=192.168.1.100" >> $ConfigFile
	fi
	if ! grep -Fq "chargep7ip=" $ConfigFile; then
		echo "chargep7ip=192.168.1.100" >> $ConfigFile
	fi
	if ! grep -Fq "chargep8ip=" $ConfigFile; then
		echo "chargep8ip=192.168.1.100" >> $ConfigFile
	fi
	if ! grep -Fq "datenschutzack=" $ConfigFile; then
		echo "datenschutzack=0" >> $ConfigFile
	fi
	if ! grep -Fq "soclp1_vin=" $ConfigFile; then
		echo "soclp1_vin=none" >> $ConfigFile
	fi
	if ! grep -Fq "soclp2_vin=" $ConfigFile; then
		echo "soclp2_vin=none" >> $ConfigFile
	fi
	if ! grep -Fq "rfidlist=" $ConfigFile; then
		echo "rfidlist=0" >> $ConfigFile
	fi
	if ! grep -Fq "wizzarddone=" $ConfigFile; then
		echo "wizzarddone=100" >> $ConfigFile
	else
		# fix wizzarddone value
		if grep -Fq "wizzarddone=1[0-9][0-9]" $ConfigFile; then
			sed -i 's/^wizzarddone=1[0-9][0-9]/wizzarddone=100/g' $ConfigFile
		fi
	fi
	if ! grep -Fq "preisjekwh=" $ConfigFile; then
		echo "preisjekwh=0.30" >> $ConfigFile
	fi
	if ! grep -Fq "displaylp3max=" $ConfigFile; then
		echo "displaylp3max=22000" >> $ConfigFile
	fi
	if ! grep -Fq "displaylp4max=" $ConfigFile; then
		echo "displaylp4max=22000" >> $ConfigFile
	fi
	if ! grep -Fq "displaylp5max=" $ConfigFile; then
		echo "displaylp5max=22000" >> $ConfigFile
	fi
	if ! grep -Fq "displaylp6max=" $ConfigFile; then
		echo "displaylp6max=22000" >> $ConfigFile
	fi
	if ! grep -Fq "displaylp7max=" $ConfigFile; then
		echo "displaylp7max=22000" >> $ConfigFile
	fi
	if ! grep -Fq "displaylp8max=" $ConfigFile; then
		echo "displaylp8max=22000" >> $ConfigFile
	fi
	if ! grep -Fq "psa_userlp1=" $ConfigFile; then
		{
			echo "psa_userlp1=User"
			echo "psa_passlp1=''"
			echo "psa_clientidlp1=ID"
			echo "psa_clientsecretlp1=Secret"
			echo "psa_userlp2=User"
			echo "psa_passlp2=''"
			echo "psa_clientidlp2=ID"
			echo "psa_clientsecretlp2=Secret"
		} >> $ConfigFile
	else
		sed -i "/psa_passlp1='/b; s/^psa_passlp1=\(.*\)/psa_passlp1=\'\1\'/g" $ConfigFile
		sed -i "/psa_passlp2='/b; s/^psa_passlp2=\(.*\)/psa_passlp2=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "psa_intervallp1=" $ConfigFile; then
		echo "psa_intervallp1=10" >> $ConfigFile
	fi
	if ! grep -Fq "psa_intervallp2=" $ConfigFile; then
		echo "psa_intervallp2=10" >> $ConfigFile
	fi
	if ! grep -Fq "psa_manufacturerlp1=" $ConfigFile; then
		echo "psa_manufacturerlp1=Peugeot" >> $ConfigFile
	fi
	if ! grep -Fq "psa_manufacturerlp2=" $ConfigFile; then
		echo "psa_manufacturerlp2=Peugeot" >> $ConfigFile
	fi
	if ! grep -Fq "psa_vinlp1=" $ConfigFile; then
		echo "psa_vinlp1=''" >> $ConfigFile
	fi
	if ! grep -Fq "psa_vinlp2=" $ConfigFile; then
		echo "psa_vinlp2=''" >> $ConfigFile
	fi  
	if ! grep -Fq "soc_eq_client_id_lp1=" $ConfigFile; then
		{
			echo "soc_eq_client_id_lp1=ID"
			echo "soc_eq_client_secret_lp1=Secret"
			echo "soc_eq_vin_lp1=VIN"
			echo "soc_eq_cb_lp1='http://openWB/openWB/modules/soc_eq/callback_lp1.php'"
			echo "soc_eq_client_id_lp2=ID"
			echo "soc_eq_client_secret_lp2=Secret"
			echo "soc_eq_vin_lp2=VIN"
			echo "soc_eq_cb_lp2='http://openWB/openWB/modules/soc_eq/callback_lp2.php'"
		} >> $ConfigFile
	else
		sed -i "/soc_eq_cb_lp1='/b; s/^soc_eq_cb_lp1=\(.*\)/soc_eq_cb_lp1=\'\1\'/g" $ConfigFile
		sed -i "/soc_eq_cb_lp2='/b; s/^soc_eq_cb_lp2=\(.*\)/soc_eq_cb_lp2=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_id_username=" $ConfigFile; then
		echo "soc_id_username=User" >> $ConfigFile
	fi
	if ! grep -Fq "soc_id_passwort=" $ConfigFile; then
		echo "soc_id_passwort=''" >> $ConfigFile
	else
		sed -i "/soc_id_passwort='/b; s/^soc_id_passwort=\(.*\)/soc_id_passwort=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_id_vin=" $ConfigFile; then
		echo "soc_id_vin=VIN" >> $ConfigFile
	fi
	if ! grep -Fq "soc_ovms_server=" $ConfigFile; then
		echo "soc_ovms_server=https://ovms.dexters-web.de:6869" >> $ConfigFile
	fi
	if ! grep -Fq "soc2server=" $ConfigFile; then
		echo "soc2server=https://ovms.dexters-web.de:6869" >> $ConfigFile
	fi
	if ! grep -Fq "soc_ovms_username=" $ConfigFile; then
		echo "soc_ovms_username=User" >> $ConfigFile
	fi
	if ! grep -Fq "soc_ovms_passwort=" $ConfigFile; then
		echo "soc_ovms_passwort=''" >> $ConfigFile
	else
		sed -i "/soc_ovms_passwort='/b; s/^soc_ovms_passwort=\(.*\)/soc_ovms_passwort=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "soc_ovms_vehicleid=" $ConfigFile; then
		echo "soc_ovms_vehicleid=vehicleid" >> $ConfigFile
	fi
	if ! grep -Fq "soc2vin=" $ConfigFile; then
		echo "soc2vin=" >> $ConfigFile
		echo "soc2intervall=60" >> $ConfigFile
	fi
	if ! grep -Fq "soc2vehicleid=" $ConfigFile; then
		echo "soc2vehicleid=" >> $ConfigFile
	fi
	if ! grep -Fq "soc2intervall=" $ConfigFile; then
		echo "soc2intervall=60" >> $ConfigFile
	fi
	if ! grep -Fq "soc2intervallladen=" $ConfigFile; then
		echo "soc2intervallladen=10" >> $ConfigFile
	fi
	if ! grep -Fq "wirkungsgradlp1=" $ConfigFile; then
		echo "wirkungsgradlp1=90" >> $ConfigFile
	fi
	if ! grep -Fq "akkuglp2=" $ConfigFile; then
		echo "akkuglp2=35" >> $ConfigFile
	fi
	if ! grep -Fq "wirkungsgradlp2=" $ConfigFile; then
		echo "wirkungsgradlp2=90" >> $ConfigFile
	fi
	if ! grep -Fq "solaxip=" $ConfigFile; then
		echo "solaxip=192.168.1.1" >> $ConfigFile
	fi
	if ! grep -Fq "psa_soccalclp1=" $ConfigFile; then
		echo "psa_soccalclp1=0" >> $ConfigFile;
	fi
	if ! grep -Fq "psa_soccalclp2=" $ConfigFile; then
		echo "psa_soccalclp2=0" >> $ConfigFile;
	fi
	if ! grep -Fq "wr1extprod=" $ConfigFile; then
		echo "wr1extprod=0" >> $ConfigFile
	fi
	if ! grep -Fq "hook1einschaltverz=" $ConfigFile; then
		echo "hook1einschaltverz=20" >> $ConfigFile
	fi
	if ! grep -Fq "hook2einschaltverz=" $ConfigFile; then
		echo "hook2einschaltverz=20" >> $ConfigFile
	fi
	if ! grep -Fq "hook3einschaltverz=" $ConfigFile; then
		echo "hook3einschaltverz=20" >> $ConfigFile
	fi
	if ! grep -Fq "stopsocnotpluggedlp1=" $ConfigFile; then
		echo "stopsocnotpluggedlp1=0" >> $ConfigFile
	fi
	if ! grep -Fq "sonnenecoip=" $ConfigFile; then
		echo "sonnenecoip=192.168.15.3" >> $ConfigFile
	fi
	if ! grep -Fq "sonnenecoalternativ=" $ConfigFile; then
		echo "sonnenecoalternativ=0" >> $ConfigFile
	fi
	if ! grep -Fq "abschaltverzoegerung=" $ConfigFile; then
		echo "abschaltverzoegerung=600" >> $ConfigFile
	fi
	if ! grep -Fq "einschaltverzoegerung=" $ConfigFile; then
		echo "einschaltverzoegerung=30" >> $ConfigFile
	fi
	if ! grep -Fq "ladetaster=" $ConfigFile; then
		echo "ladetaster=0" >> $ConfigFile
	fi
	if ! grep -Fq "rseenabled=" $ConfigFile; then
		echo "rseenabled=0" >> $ConfigFile
	fi
	if ! grep -Fq "u1p3schaltparam=" $ConfigFile; then
		echo "u1p3schaltparam=8" >> $ConfigFile
	fi
	if ! grep -Fq "soc_tesla_mfapasscode=" $ConfigFile; then
		echo "soc_tesla_mfapasscode=''" >> $ConfigFile
		echo "soc_teslalp2_mfapasscode=''" >> $ConfigFile
	fi
	if ! grep -Fq "speicherpwloginneeded=" $ConfigFile; then
		{
			echo "speicherpwloginneeded=0"
			echo "speicherpwuser=Username"
			echo "speicherpwpass=''"
		} >> $ConfigFile
	else
		sed -i "/speicherpwpass='/b; s/^speicherpwpass=\(.*\)/speicherpwpass=\'\1\'/g" $ConfigFile
	fi
	if ! grep -Fq "multifems=" $ConfigFile; then
		echo "multifems=0" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgezweiterspeicher=" $ConfigFile; then
		echo "solaredgezweiterspeicher=0" >> $ConfigFile
	fi
	if ! grep -Fq "solaredgesubbat=" $ConfigFile; then
		echo "solaredgesubbat=0" >> $ConfigFile
	fi
	if ! grep -Fq "studer_ip=" $ConfigFile; then
		{
			echo "studer_ip=192.168.1.1"
			echo "studer_xt=1"
			echo "studer_vc=1"
			echo "studer_vc_type=VS"
		} >> $ConfigFile
	fi
	if ! grep -Fq "pingcheckactive=" $ConfigFile; then
		echo "pingcheckactive=0" >> $ConfigFile
	fi
	if ! grep -Fq "soc_tronity_client_id_lp1=" $ConfigFile; then
		{
			echo "soc_tronity_client_id_lp1=''"
			echo "soc_tronity_client_secret_lp1=''"
			echo "soc_tronity_vehicle_id_lp1=''"
			echo "soc_tronity_intervall=720"
			echo "soc_tronity_intervallladen=15"
			echo "soc_tronity_client_id_lp2=''"
			echo "soc_tronity_client_secret_lp2=''"
			echo "soc_tronity_vehicle_id_lp2=''"
		} >> $ConfigFile
	fi
	if ! grep -Fq "soc_evcc_type_lp1=" $ConfigFile; then
		{
			echo "soc_evcc_type_lp1=vw"
			echo "soc_evcc_username_lp1=''"
			echo "soc_evcc_password_lp1=''"
			echo "soc_evcc_vin_lp1=''"
			echo "soc_evcc_pin_lp1=''"
			echo "soc_evcc_token_lp1=''"
			echo "soc_evcc_intervall=720"
			echo "soc_evcc_intervallladen=15"
			echo "soc_evcc_type_lp2=vw"
			echo "soc_evcc_username_lp2=''"
			echo "soc_evcc_password_lp2=''"
			echo "soc_evcc_vin_lp2=''"
			echo "soc_evcc_pin_lp2=''"
			echo "soc_evcc_token_lp2=''"
		} >> $ConfigFile
	fi
	if ! grep -Fq "soc_evcc_pin_lp1=" $ConfigFile; then
			echo "soc_evcc_pin_lp1=''" >> $ConfigFile
	fi
	if ! grep -Fq "soc_evcc_pin_lp2=" $ConfigFile; then
			echo "soc_evcc_pin_lp2=''" >> $ConfigFile
	fi
	if ! grep -Fq "cpunterbrechungmindestlaufzeitaktiv=" $ConfigFile; then
		{
			echo "cpunterbrechungmindestlaufzeitaktiv=0"
			echo "cpunterbrechungmindestlaufzeit=30"
		} >> $ConfigFile
	fi
	if ! grep -Fq "solarwattmethod=" $ConfigFile; then
		echo "solarwattmethod=0" >> $ConfigFile
	fi
	if ! grep -Fq "sungrowsr=" $ConfigFile; then
		echo "sungrowsr=0" >> $ConfigFile
	fi
	if ! grep -Fq "sungrow2sr=" $ConfigFile; then
		echo "sungrow2sr=0" >> $ConfigFile
	fi
	if ! grep -Fq "sungrowspeicherport=" $ConfigFile; then
		echo "sungrowspeicherport=502" >> $ConfigFile
		echo "sungrowspeicherid=1" >> $ConfigFile
	fi
	if ! grep -Fq "alphasource=" $ConfigFile; then
		echo "alphasource=0" >> $ConfigFile
	fi
	if ! grep -Fq "alphav123=" $ConfigFile; then
		echo "alphav123=0" >> $ConfigFile
	fi
	if ! grep -Fq "alphaip=" $ConfigFile; then
		echo "alphaip=192.168.193.15" >> $ConfigFile
	fi
	if ! grep -Fq "good_we_ip=" $ConfigFile; then
		echo "good_we_ip=192.168.1.1" >> $ConfigFile
	fi
	if ! grep -Fq "good_we_id=" $ConfigFile; then
		echo "good_we_id=247" >> $ConfigFile
	fi
	if ! grep -Fq "batterx_ip=" $ConfigFile; then
		echo "batterx_ip=192.168.0.17" >> $ConfigFile
	fi
	if ! grep -Fq "pvbatterxextinverter=" $ConfigFile; then
		echo "pvbatterxextinverter=0" >> $ConfigFile
	fi
	if grep -Fq "socmodul=soc_bluelink" $ConfigFile; then
		sed -i "s/^socmodul=soc_bluelink/socmodul=soc_kia/g" $ConfigFile
	fi
	if grep -Fq "socmodul1=soc_bluelinklp2" $ConfigFile; then
		sed -i "s/^socmodul1=soc_bluelinklp2/socmodul1=soc_kialp2/g" $ConfigFile
	fi
	if ! grep -Fq "virtual_ip_eth0=" $ConfigFile; then
		echo "virtual_ip_eth0='192.168.193.5'" >> $ConfigFile
	fi
	if ! grep -Fq "virtual_ip_wlan0=" $ConfigFile; then
		echo "virtual_ip_wlan0='192.168.193.6'" >> $ConfigFile
	fi
	if ! grep -Fq "evuflexip=" $ConfigFile; then
		{
			echo "evuflexversion=2"
			echo "evuflexip='192.168.193.5'"
			echo "evuflexport=8899"
			echo "evuflexid=1"
		} >> $ConfigFile
	fi
	if ! grep -Fq "pvflexip=" $ConfigFile; then
		{
			echo "pvflexip='192.168.193.5'"
			echo "pvflexport=8899"
			echo "pvflexid=1"
			echo "pvflexversion=1"
		} >> $ConfigFile
	fi
	if ! grep -Fq "pv2flexip=" $ConfigFile; then
		{
			echo "pv2flexip='192.168.193.5'"
			echo "pv2flexport=8899"
			echo "pv2flexid=1"
			echo "pv2flexversion=1"
		} >> $ConfigFile
	fi
	if ! grep -Fq "soc_aiways_user=" $ConfigFile; then
		{
			echo "soc_aiways_user=''"
			echo "soc_aiways_pass=''"
			echo "soc_aiways_vin=''"
			echo "soc_aiways_intervall=''"
			echo "soc_aiwayslp2_user=''"
			echo "soc_aiwayslp2_pass=''"
			echo "soc_aiwayslp2_vin=''"
			echo "soc_aiwayslp2_intervall=''"
		} >> $ConfigFile
	fi
	if ! grep -Fq "wrsmaversion=" $ConfigFile; then
		{
			echo "wrsmaversion=0"
			echo "wr2smaversion=0"
		} >> $ConfigFile
	fi

	# replace obsolete soc_id configuration by soc_vwid
	if grep -Fq "socmodul=soc_id" $ConfigFile; then
		sed -i "s/^socmodul=soc_id/socmodul=soc_vwid/g" $ConfigFile
	fi
	if grep -Fq "socmodul1=soc_idlp2" $ConfigFile; then
		sed -i "s/^socmodul1=soc_idlp2/socmodul=soc_vwidlp2/g" $ConfigFile
	fi
	if [[ -f /home/pi/ppbuchse ]]; then
		ppbuchse=$(</home/pi/ppbuchse)
		if ! grep -Fq "ppbuchse=" $ConfigFile; then
			echo "ppbuchse=$ppbuchse" >> $ConfigFile
		else
			ppbuchseOld=$(grep -F "ppbuchse=" $ConfigFile)
			ppbuchseOld=${ppbuchseOld#ppbuchse=}
			if ((ppbuchseOld != ppbuchse)); then
				sed -i "s/^ppbuchse=.*$/ppbuchse=$ppbuchse/g" $ConfigFile
			fi
		fi
	fi
	echo "remove soc_smarteq entries from Config file"
	cp $ConfigFile $ConfigFile.tmp
	# check for socmodul1=soc_smarteqlp2
	ism2=`grep "socmodul1=soc_smarteqlp2" $ConfigFile.tmp | wc -l | awk '{print $1}'`
	if [ $ism2 -ne 0 ]
	then
		echo "soc_smarteq found configured as socmodul1 - cleanup soc2 entries"
		sed -e "
			s/soc2user=.*$/soc2user=demo@demo.de/
			s/soc2pass=.*$/soc2pass=\'\'/
			s/soc2pin=.*$/soc2pin=pin/
			s/soc2vin=.*$/soc2vin=/
			s/soc2intervall=.*$/soc2intervall=60/
			s/soc2intervallladen=.*$/soc2intervallladen=10/
		" $ConfigFile.tmp > $ConfigFile.tmp.out
		cp $ConfigFile.tmp.out $ConfigFile.tmp
	fi
	# modify configured smarteq modules to none
	sed -e '
		s/socmodul=soc_smarteq/socmodul=none/
		s/socmodul1=soc_smarteqlp2/socmodul1=none/
		/soc2pint=/d
		/soc_smarteq/d
	' $ConfigFile.tmp > $ConfigFile.tmp.out
	cp $ConfigFile.tmp.out $ConfigFile
	rm $ConfigFile.tmp $ConfigFile.tmp.out

	echo "Config file Update done."
}
