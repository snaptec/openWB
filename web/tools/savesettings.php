<?php
if(isset($_POST['minimalstromstaerke'])) {

	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		$writeit = '0';
		if(strpos($line, "schieflastmaxa=") !== false) {
			$result .= 'schieflastmaxa='.$_POST['schieflastmaxa']."\n";
			$writeit = '1';
		}
		if(strpos($line, "isss=") !== false) {
			$result .= 'isss='.$_POST['isss']."\n";
			$writeit = '1';
		}
		if(strpos($line, "schieflastaktiv=") !== false) {
			$result .= 'schieflastaktiv='.$_POST['schieflastaktiv']."\n";
			$writeit = '1';
		}
		if(strpos($line, "awattaraktiv=") !== false) {
			$result .= 'awattaraktiv='.$_POST['awattaraktiv']."\n";
			$writeit = '1';
		}
		if(strpos($line, "pvbezugeinspeisung=") !== false) {
			$result .= 'pvbezugeinspeisung='.$_POST['pvbezugeinspeisung']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1moab=") !== false) {
			$result .= 'mollp1moab='.$_POST['mollp1moab']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1mobis=") !== false) {
			$result .= 'mollp1mobis='.$_POST['mollp1mobis']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1moll=") !== false) {
			$result .= 'mollp1moll='.$_POST['mollp1moll']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1diab=") !== false) {
			$result .= 'mollp1diab='.$_POST['mollp1diab']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1dibis=") !== false) {
			$result .= 'mollp1dibis='.$_POST['mollp1dibis']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1dill=") !== false) {
			$result .= 'mollp1dill='.$_POST['mollp1dill']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1miab=") !== false) {
			$result .= 'mollp1miab='.$_POST['mollp1miab']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1mibis=") !== false) {
			$result .= 'mollp1mibis='.$_POST['mollp1mibis']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1mill=") !== false) {
			$result .= 'mollp1mill='.$_POST['mollp1mill']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1doab=") !== false) {
			$result .= 'mollp1doab='.$_POST['mollp1doab']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1dobis=") !== false) {
			$result .= 'mollp1dobis='.$_POST['mollp1dobis']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1doll=") !== false) {
			$result .= 'mollp1doll='.$_POST['mollp1doll']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1frab=") !== false) {
			$result .= 'mollp1frab='.$_POST['mollp1frab']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1frll=") !== false) {
			$result .= 'mollp1frll='.$_POST['mollp1frll']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1saab=") !== false) {
			$result .= 'mollp1saab='.$_POST['mollp1saab']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1sabis=") !== false) {
			$result .= 'mollp1sabis='.$_POST['mollp1sabis']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1sall=") !== false) {
			$result .= 'mollp1sall='.$_POST['mollp1sall']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1soab=") !== false) {
			$result .= 'mollp1soab='.$_POST['mollp1soab']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1sobis=") !== false) {
			$result .= 'mollp1sobis='.$_POST['mollp1sobis']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1soll=") !== false) {
			$result .= 'mollp1soll='.$_POST['mollp1soll']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mollp1frbis=") !== false) {
			$result .= 'mollp1frbis='.$_POST['mollp1frbis']."\n";
			$writeit = '1';
		}
		if(strpos($line, "minimalampv=") !== false) {
			$result .= 'minimalampv='.$_POST['minimalampv']."\n";
			$writeit = '1';
		}
		if(strpos($line, "minimalapv=") !== false) {
			$result .= 'minimalapv='.$_POST['minimalapv']."\n";
			$writeit = '1';
		}
		if(strpos($line, "minimalstromstaerke=") !== false) {
			$result .= 'minimalstromstaerke='.$_POST['minimalstromstaerke']."\n";
			$writeit = '1';
		}
		if(strpos($line, "maximalstromstaerke=") !== false) {
			$result .= 'maximalstromstaerke='.$_POST['maximalstromstaerke']."\n";
			$writeit = '1';
		}
		if(strpos($line, "debug=") !== false) {
			$result .= 'debug='.$_POST['debug']."\n";
			$writeit = '1';
		}
		if(strpos($line, "evsecon=") !== false) {
			$result .= 'evsecon='.$_POST['evsecon']."\n";
			$writeit = '1';
		}
		if(strpos($line, "dacregisters1=") !== false) {
			$result .= 'dacregisters1='.$_POST['dacregisters1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "dacregister=") !== false) {
			$result .= 'dacregister='.$_POST['dacregister']."\n";
			$writeit = '1';
		}
		if(strpos($line, "modbusevsesource=") !== false) {
			$result .= 'modbusevsesource='.$_POST['modbusevsesource']."\n";
			$writeit = '1';
		}
		if(strpos($line, "modbusevseid=") !== false) {
			$result .= 'modbusevseid='.$_POST['modbusevseid']."\n";
			$writeit = '1';
		}
		if(strpos($line, "wattbezugmodul=") !== false) {
			$result .= 'wattbezugmodul='.$_POST['wattbezugmodul']."\n";
			$writeit = '1';
		}
		if(strpos($line, "vzloggerip=") !== false) {
			$result .= 'vzloggerip='.$_POST['vzloggerip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "vzloggerpvip=") !== false) {
			$result .= 'vzloggerpvip='.$_POST['vzloggerpvip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "vzloggerline=") !== false) {
			$result .= 'vzloggerline='.$_POST['vzloggerline']."\n";
			$writeit = '1';
		}
		if(strpos($line, "vzloggerkwhline=") !== false) {
			$result .= 'vzloggerkwhline='.$_POST['vzloggerkwhline']."\n";
			$writeit = '1';
		}
		if(strpos($line, "vzloggerekwhline=") !== false) {
			$result .= 'vzloggerekwhline='.$_POST['vzloggerekwhline']."\n";
			$writeit = '1';
		}
		if(strpos($line, "vzloggerpvline=") !== false) {
			$result .= 'vzloggerpvline='.$_POST['vzloggerpvline']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm630modbusbezugid=") !== false) {
			$result .= 'sdm630modbusbezugid='.$_POST['sdm630modbusbezugid']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm630modbusbezugsource=") !== false) {
			$result .= 'sdm630modbusbezugsource='.$_POST['sdm630modbusbezugsource']."\n";
			$writeit = '1';
		}
		if(strpos($line, "pvwattmodul=") !== false) {
			$result .= 'pvwattmodul='.$_POST['pvwattmodul']."\n";
			$writeit = '1';
		}
		if(strpos($line, "wrfroniusip=") !== false) {
			$result .= 'wrfroniusip='.$_POST['wrfroniusip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "ladeleistungmodul=") !== false) {
			$result .= 'ladeleistungmodul='.$_POST['ladeleistungmodul']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm630modbusllid=") !== false) {
			$result .= 'sdm630modbusllid='.$_POST['sdm630modbusllid']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm630modbusllsource=") !== false) {
			$result .= 'sdm630modbusllsource='.$_POST['sdm630modbusllsource']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm630modbusbezuglanip=") !== false) {
			$result .= 'sdm630modbusbezuglanip='.$_POST['sdm630modbusbezuglanip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm630modbuswrid=") !== false) {
			$result .= 'sdm630modbuswrid='.$_POST['sdm630modbuswrid']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm630modbuswrsource=") !== false) {
			$result .= 'sdm630modbuswrsource='.$_POST['sdm630modbuswrsource']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm630modbuswrlanip=") !== false) {
			$result .= 'sdm630modbuswrlanip='.$_POST['sdm630modbuswrlanip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm630modbuslllanip=") !== false) {
			$result .= 'sdm630modbuslllanip='.$_POST['sdm630modbuslllanip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "socmodul=") !== false) {
			$result .= 'socmodul='.$_POST['socmodul']."\n";
			$writeit = '1';
		}
		if(strpos($line, "socmodul1=") !== false) {
			$result .= 'socmodul1='.$_POST['socmodul1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "hsocip=") !== false) {
			$result .= 'hsocip=\''.$_POST['hsocip']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "hsocip1=") !== false) {
			$result .= 'hsocip1='.$_POST['hsocip1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladen=") !== false) {
			$result .= 'nachtladen='.$_POST['nachtladen']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtll=") !== false) {
			$result .= 'nachtll='.$_POST['nachtll']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladenabuhr=") !== false) {
			$result .= 'nachtladenabuhr='.$_POST['nachtladenabuhr']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladenbisuhr=") !== false) {
			$result .= 'nachtladenbisuhr='.$_POST['nachtladenbisuhr']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nacht2ll=") !== false) {
			$result .= 'nacht2ll='.$_POST['nacht2ll']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladen2abuhr=") !== false) {
			$result .= 'nachtladen2abuhr='.$_POST['nachtladen2abuhr']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladen2bisuhr=") !== false) {
			$result .= 'nachtladen2bisuhr='.$_POST['nachtladen2bisuhr']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nacht2lls1=") !== false) {
			$result .= 'nacht2lls1='.$_POST['nacht2lls1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladen2abuhrs1=") !== false) {
			$result .= 'nachtladen2abuhrs1='.$_POST['nachtladen2abuhrs1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladen2bisuhrs1=") !== false) {
			$result .= 'nachtladen2bisuhrs1='.$_POST['nachtladen2bisuhrs1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtsoc=") !== false) {
			$result .= 'nachtsoc='.$_POST['nachtsoc']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtsoc1=") !== false) {
			$result .= 'nachtsoc1='.$_POST['nachtsoc1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mindestuberschuss=") !== false) {
			$result .= 'mindestuberschuss='.$_POST['mindestuberschuss']."\n";
			$writeit = '1';
		}
		if(strpos($line, "abschaltuberschuss=") !== false) {
			$result .= 'abschaltuberschuss='.$_POST['abschaltuberschuss']."\n";
			$writeit = '1';
		}
		if(strpos($line, "abschaltverzoegerung=") !== false) {
			$result .= 'abschaltverzoegerung='.$_POST['abschaltverzoegerung']."\n";
			$writeit = '1';
		}
		if(strpos($line, "modbusevselanip=") !== false) {
			$result .= 'modbusevselanip='.$_POST['modbusevselanip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "evsecons1=") !== false) {
			$result .= 'evsecons1='.$_POST['evsecons1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "evsecons2=") !== false) {
			$result .= 'evsecons2='.$_POST['evsecons2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "evsesources1=") !== false) {
			$result .= 'evsesources1='.$_POST['evsesources1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "evsesources2=") !== false) {
			$result .= 'evsesources2='.$_POST['evsesources2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "evseids1=") !== false) {
			$result .= 'evseids1='.$_POST['evseids1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "evseids2=") !== false) {
			$result .= 'evseids2='.$_POST['evseids2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "evselanips1=") !== false) {
			$result .= 'evselanips1='.$_POST['evselanips1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "evselanips2=") !== false) {
			$result .= 'evselanips2='.$_POST['evselanips2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "lastmanagement=") !== false) {
			$result .= 'lastmanagement='.$_POST['lastmanagement']."\n";
			$writeit = '1';
		}
		if(strpos($line, "lastmanagements2=") !== false) {
			$result .= 'lastmanagements2='.$_POST['lastmanagements2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "lastmmaxw=") !== false) {
			$result .= 'lastmmaxw='.$_POST['lastmmaxw']."\n";
			$writeit = '1';
		}
		if(strpos($line, "lastmaxap1=") !== false) {
			$result .= 'lastmaxap1='.$_POST['lastmaxap1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "lastmaxap2=") !== false) {
			$result .= 'lastmaxap2='.$_POST['lastmaxap2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "lastmaxap3=") !== false) {
			$result .= 'lastmaxap3='.$_POST['lastmaxap3']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdmids1=") !== false) {
			$result .= 'sdmids1='.$_POST['sdmids1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdmids2=") !== false) {
			$result .= 'sdmids2='.$_POST['sdmids2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "smaemdbezugid=") !== false) {
			$result .= 'smaemdbezugid='.$_POST['smaemdbezugid']."\n";
			$writeit = '1';
		}
		if(strpos($line, "smaemdllid=") !== false) {
			$result .= 'smaemdllid='.$_POST['smaemdllid']."\n";
			$writeit = '1';
		}
		if(strpos($line, "smaemdpvid=") !== false) {
			$result .= 'smaemdpvid='.$_POST['smaemdpvid']."\n";
			$writeit = '1';
		}
		if(strpos($line, "ladeleistungs1modul=") !== false) {
			$result .= 'ladeleistungs1modul='.$_POST['ladeleistungs1modul']."\n";
			$writeit = '1';
		}
		if(strpos($line, "ladeleistungs2modul=") !== false) {
			$result .= 'ladeleistungs2modul='.$_POST['ladeleistungs2modul']."\n";
			$writeit = '1';
		}
		if(strpos($line, "wr_http_w_url=") !== false) {
			$result .= 'wr_http_w_url=\''.$_POST['wr_http_w_url']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "wr_http_kwh_url=") !== false) {
			$result .= 'wr_http_kwh_url=\''.$_POST['wr_http_kwh_url']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "bezug_http_w_url=") !== false) {
			$result .= 'bezug_http_w_url=\''.$_POST['bezug_http_w_url']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "bezug_http_ekwh_url=") !== false) {
			$result .= 'bezug_http_ekwh_url=\''.$_POST['bezug_http_ekwh_url']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "dspeed=") !== false) {
			$result .= 'dspeed='.$_POST['dspeed']."\n";
			$writeit = '1';
		}
		if(strpos($line, "durchslp1=") !== false) {
			$result .= 'durchslp1='.$_POST['durchslp1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "durchslp2=") !== false) {
			$result .= 'durchslp2='.$_POST['durchslp2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "durchslp3=") !== false) {
			$result .= 'durchslp3='.$_POST['durchslp3']."\n";
			$writeit = '1';
		}
		if(strpos($line, "bezug_http_ikwh_url=") !== false) {
			$result .= 'bezug_http_ikwh_url=\''.$_POST['bezug_http_ikwh_url']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtlls1=") !== false) {
			$result .= 'nachtlls1='.$_POST['nachtlls1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladens1=") !== false) {
			$result .= 'nachtladens1='.$_POST['nachtladens1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtsocs1=") !== false) {
			$result .= 'nachtsocs1='.$_POST['nachtsocs1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtsoc1s1=") !== false) {
			$result .= 'nachtsoc1s1='.$_POST['nachtsoc1s1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladenabuhrs1=") !== false) {
			$result .= 'nachtladenabs1='.$_POST['nachtladenabuhrs1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "nachtladenbisuhrs1=") !== false) {
			$result .= 'nachtladenbisuhrs1='.$_POST['nachtladenbisuhrs1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm120modbusllid1s1=") !== false) {
			$result .= 'sdm120modbusllid1s1='.$_POST['sdm120modbusllid1s1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm120modbusllid2s1=") !== false) {
			$result .= 'sdm120modbusllid2s1='.$_POST['sdm120modbusllid2s1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm120modbusllid3s1=") !== false) {
			$result .= 'sdm120modbusllid3s1='.$_POST['sdm120modbusllid3s1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sdm120modbusllid1s1=") !== false) {
			$result .= 'sdm120modbusllid1s1='.$_POST['sdm120modbusllid1s1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "pushovertoken=") !== false) {
			$result .= 'pushovertoken=\''.$_POST['pushovertoken']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "pushoveruser=") !== false) {
			$result .= 'pushoveruser=\''.$_POST['pushoveruser']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "pushbenachrichtigung=") !== false) {
			$result .= 'pushbenachrichtigung='.$_POST['pushbenachrichtigung']."\n";
			$writeit = '1';
		}
		if(strpos($line, "pushbstartl=") !== false) {
			$result .= 'pushbstartl='.$_POST['pushbstartl']."\n";
			$writeit = '1';
		}
		if(strpos($line, "pushbstopl=") !== false) {
			$result .= 'pushbstopl='.$_POST['pushbstopl']."\n";
			$writeit = '1';
		}
		if(strpos($line, "speicherpveinbeziehen=") !== false) {
			$result .= 'speicherpveinbeziehen='.$_POST['speicherpveinbeziehen']."\n";
			$writeit = '1';
		}
		if(strpos($line, "akkuglp1=") !== false) {
			$result .= 'akkuglp1='.$_POST['akkuglp1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "akkuglp2=") !== false) {
			$result .= 'akkuglp2='.$_POST['akkuglp2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "zielladensoclp1=") !== false) {
			$result .= 'zielladensoclp1='.$_POST['zielladensoclp1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "zielladenalp1=") !== false) {
			$result .= 'zielladenalp1='.$_POST['zielladenalp1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "zielladenmaxalp1=") !== false) {
			$result .= 'zielladenmaxalp1='.$_POST['zielladenmaxalp1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "zielladenphasenlp1=") !== false) {
			$result .= 'zielladenphasenlp1='.$_POST['zielladenphasenlp1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "zielladenaktivlp1=") !== false) {
			$result .= 'zielladenaktivlp1='.$_POST['zielladenaktivlp1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "offsetpv=") !== false) {
			$result .= 'offsetpv='.$_POST['offsetpv']."\n";
			$writeit = '1';
		}
		if(strpos($line, "hook1ein_url=") !== false) {
			$result .= 'hook1ein_url=\''.$_POST['hook1ein_url']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "hook1aus_url=") !== false) {
			$result .= 'hook1aus_url=\''.$_POST[hook1aus_url]."'\n";
			$writeit = '1';
		}
		if(strpos($line, "hook1_aktiv=") !== false) {
			$result .= 'hook1_aktiv='.$_POST['hook1_aktiv']."\n";
			$writeit = '1';
		}
		if(strpos($line, "hook1ein_watt=") !== false) {
			$result .= 'hook1ein_watt='.$_POST['hook1ein_watt']."\n";
			$writeit = '1';
		}
		if(strpos($line, "hook1aus_watt=") !== false) {
			$result .= 'hook1aus_watt='.$_POST['hook1aus_watt']."\n";
			$writeit = '1';
		}
		if(strpos($line, "zielladenuhrzeitlp1=") !== false) {
			$result .= 'zielladenuhrzeitlp1=\''.$_POST['zielladenuhrzeitlp1']."\'\n";
			$writeit = '1';
		}

		if ( $writeit == '0') {
			$result .= $line;
		}
	}
	file_put_contents('/var/www/html/openWB/openwb.conf', $result);
}
header("Location: ../index.php");
?>
