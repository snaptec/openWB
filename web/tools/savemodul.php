
<?php
if(isset($_POST['evsecon'])) {
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	$writeit = '0';
	if(strpos($line, "evsecon=") !== false) {
	    $result .= 'evsecon='.$_POST[evsecon]."\n";
	    $writeit = '1';
	}
	    if(strpos($line, "dacregisters1=") !== false) {
	    $result .= 'dacregisters1='.$_POST[dacregisters1]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "dacregister=") !== false) {
	    $result .= 'dacregister='.$_POST[dacregister]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "modbusevsesource=") !== false) {
	    $result .= 'modbusevsesource='.$_POST[modbusevsesource]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "modbusevseid=") !== false) {
	    $result .= 'modbusevseid='.$_POST[modbusevseid]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "wattbezugmodul=") !== false) {
	    $result .= 'wattbezugmodul='.$_POST[wattbezugmodul]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "vzloggerip=") !== false) {
	    $result .= 'vzloggerip='.$_POST[vzloggerip]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "vzloggerpvip=") !== false) {
	    $result .= 'vzloggerpvip='.$_POST[vzloggerpvip]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "vzloggerline=") !== false) {
	    $result .= 'vzloggerline='.$_POST[vzloggerline]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "vzloggerkwhline=") !== false) {
	    $result .= 'vzloggerkwhline='.$_POST[vzloggerkwhline]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "vzloggerekwhline=") !== false) {
	    $result .= 'vzloggerekwhline='.$_POST[vzloggerekwhline]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "vzloggerpvline=") !== false) {
	    $result .= 'vzloggerpvline='.$_POST[vzloggerpvline]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm630modbusbezugid=") !== false) {
	    $result .= 'sdm630modbusbezugid='.$_POST[sdm630modbusbezugid]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm630modbusbezugsource=") !== false) {
	    $result .= 'sdm630modbusbezugsource='.$_POST[sdm630modbusbezugsource]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "pvwattmodul=") !== false) {
	    $result .= 'pvwattmodul='.$_POST[pvwattmodul]."\n";
	    $writeit = '1';
	    } 
	if(strpos($line, "ladeleistungmodul=") !== false) {
		if($_POST[evsecon] == "simpleevsewifi" or $_POST[evsecon] == "goe") {
			if($_POST[evsecon] == "goe") {
				$result .= 'ladeleistungmodul=goelp1'."\n";
			}
			if($_POST[evsecon] == "simpleevsewifi") { 
				$result .= 'ladeleistungmodul=simpleevsewifi'."\n";
			}
		} else {
			$result .= 'ladeleistungmodul='.$_POST[ladeleistungmodul]."\n";
		} 
		$writeit = '1';
	}
	    if(strpos($line, "sdm630modbusllid=") !== false) {
	    $result .= 'sdm630modbusllid='.$_POST[sdm630modbusllid]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm630modbusllsource=") !== false) {
	    $result .= 'sdm630modbusllsource='.$_POST[sdm630modbusllsource]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm120modbusllsource=") !== false) {
	    $result .= 'sdm120modbusllsource='.$_POST[sdm120modbusllsource]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm630modbusbezuglanip=") !== false) {
	    $result .= 'sdm630modbusbezuglanip='.$_POST[sdm630modbusbezuglanip]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm630modbuswrid=") !== false) {
	    $result .= 'sdm630modbuswrid='.$_POST[sdm630modbuswrid]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm630modbuswrsource=") !== false) {
	    $result .= 'sdm630modbuswrsource='.$_POST[sdm630modbuswrsource]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm630modbuswrlanip=") !== false) {
	    $result .= 'sdm630modbuswrlanip='.$_POST[sdm630modbuswrlanip]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm630modbuslllanip=") !== false) {
	    $result .= 'sdm630modbuslllanip='.$_POST[sdm630modbuslllanip]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "socmodul=") !== false) {
	    $result .= 'socmodul='.$_POST[socmodul]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "socmodul1=") !== false) {
	    $result .= 'socmodul1='.$_POST[socmodul1]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "hsocip=") !== false) {
	    $result .= 'hsocip=\''.$_POST[hsocip]."'\n";
	    $writeit = '1';
	    }
	    if(strpos($line, "hsocip1=") !== false) {
	    $result .= 'hsocip1='.$_POST[hsocip1]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "modbusevselanip=") !== false) {
	    $result .= 'modbusevselanip='.$_POST[modbusevselanip]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "evsecons1=") !== false) {
	    $result .= 'evsecons1='.$_POST[evsecons1]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "evsecons2=") !== false) {
	    $result .= 'evsecons2='.$_POST[evsecons2]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "evsesources1=") !== false) {
	    $result .= 'evsesources1='.$_POST[evsesources1]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "evsesources2=") !== false) {
	    $result .= 'evsesources2='.$_POST[evsesources2]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "evseids1=") !== false) {
	    $result .= 'evseids1='.$_POST[evseids1]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "evseids2=") !== false) {
	    $result .= 'evseids2='.$_POST[evseids2]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "evselanips1=") !== false) {
	    $result .= 'evselanips1='.$_POST[evselanips1]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "evselanips2=") !== false) {
	    $result .= 'evselanips2='.$_POST[evselanips2]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "lastmanagement=") !== false) {
	    $result .= 'lastmanagement='.$_POST[lastmanagement]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "lastmanagements2=") !== false) {
		    if($_POST[lastmanagement] == 0) {
			$result .= 'lastmanagements2=0'."\n";
		    } else {						
			$result .= 'lastmanagements2='.$_POST[lastmanagements2]."\n";
	    	    } 
		    $writeit = '1';
	    } 
	    if(strpos($line, "sdmids1=") !== false) {
	    $result .= 'sdmids1='.$_POST[sdmids1]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdmids2=") !== false) {
	    $result .= 'sdmids2='.$_POST[sdmids2]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "smaemdbezugid=") !== false) {
	    $result .= 'smaemdbezugid='.$_POST[smaemdbezugid]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "smaemdllid=") !== false) {
	    $result .= 'smaemdllid='.$_POST[smaemdllid]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "smaemdpvid=") !== false) {
	    $result .= 'smaemdpvid='.$_POST[smaemdpvid]."\n";
	    $writeit = '1';
	    } 
            if(strpos($line, "ladeleistungs1modul=") !== false) {
	    	if($_POST[evsecons1] == "simpleevsewifi" or $_POST[evsecons1] == "goe" or $_POST[evsecons1] == "slaveeth") {
			if($_POST[evsecons1] == "goe") {
				$result .= 'ladeleistungs1modul=goelp2'."\n";
			}
			if($_POST[evsecons1] == "slaveeth") {
				$result .= 'ladeleistungs1modul=mpm3pmethll'."\n";
			}
			if($_POST[evsecons1] == "simpleevsewifi") { 
				$result .= 'ladeleistungs1modul=simpleevsewifis1'."\n";
			}
		} else {
			$result .= 'ladeleistungs1modul='.$_POST[ladeleistungs1modul]."\n";
	    } 
		$writeit = '1';
	    } 
	    if(strpos($line, "ladeleistungs2modul=") !== false) {
	    	if($_POST[evsecons2] == "simpleevsewifi" or $_POST[evsecons2] == "goe") {
			if($_POST[evsecons2] == "goe") {
				$result .= 'ladeleistungs2modul=goelp3'."\n";
			}
			if($_POST[evsecons2] == "simpleevsewifi") { 
				$result .= 'ladeleistungs2modul=simpleevsewifis2'."\n";
			}
		} else {
			$result .= 'ladeleistungs2modul='.$_POST[ladeleistungs2modul]."\n";
	    } 
		$writeit = '1';
	    } 
	    if(strpos($line, "wr_http_w_url=") !== false) {
	    $result .= 'wr_http_w_url=\''.$_POST[wr_http_w_url]."'\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "wr_http_kwh_url=") !== false) {
	    $result .= 'wr_http_kwh_url=\''.$_POST[wr_http_kwh_url]."'\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "bezug_http_w_url=") !== false) {
	    $result .= 'bezug_http_w_url=\''.$_POST[bezug_http_w_url]."'\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "bezug_http_l1_url=") !== false) {
	    $result .= 'bezug_http_l1_url=\''.$_POST[bezug_http_l1_url]."'\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "bezug_http_l2_url=") !== false) {
	    $result .= 'bezug_http_l2_url=\''.$_POST[bezug_http_l2_url]."'\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "bezug_http_l3_url=") !== false) {
	    $result .= 'bezug_http_l3_url=\''.$_POST[bezug_http_l3_url]."'\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "bezug_http_ekwh_url=") !== false) {
	    $result .= 'bezug_http_ekwh_url=\''.$_POST[bezug_http_ekwh_url]."'\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "bezug_http_ikwh_url=") !== false) {
	    $result .= 'bezug_http_ikwh_url=\''.$_POST[bezug_http_ikwh_url]."'\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "sdm120modbusllid1s1=") !== false) {
	    $result .= 'sdm120modbusllid1s1='.$_POST[sdm120modbusllid1s1]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "sdm120modbusllid2s1=") !== false) {
	    $result .= 'sdm120modbusllid2s1='.$_POST[sdm120modbusllid2s1]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "sdm120modbusllid3s1=") !== false) {
	    $result .= 'sdm120modbusllid3s1='.$_POST[sdm120modbusllid3s1]."\n";
	  $writeit = '1';
  } 
	    if(strpos($line, "sdm120modbusllid1s2=") !== false) {
	    $result .= 'sdm120modbusllid1s2='.$_POST[sdm120modbusllid1s2]."\n";
	   $writeit = '1';
 } 
	    if(strpos($line, "sdm120modbusllid2s2=") !== false) {
	    $result .= 'sdm120modbusllid2s2='.$_POST[sdm120modbusllid2s2]."\n";
	    $writeit = '1';
} 
	    if(strpos($line, "sdm120modbusllid3s2=") !== false) {
	    $result .= 'sdm120modbusllid3s2='.$_POST[sdm120modbusllid3s2]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "sdm120modbusllid1=") !== false) {
	    $result .= 'sdm120modbusllid1='.$_POST[sdm120modbusllid1]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "sdm120modbusllid2=") !== false) {
	    $result .= 'sdm120modbusllid2='.$_POST[sdm120modbusllid2]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "sdm120modbusllid3=") !== false) {
	    $result .= 'sdm120modbusllid3='.$_POST[sdm120modbusllid3]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "mpm3pmevuid=") !== false) {
	    $result .= 'mpm3pmevuid='.$_POST[mpm3pmevuid]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "mpm3pmevusource=") !== false) {
	    $result .= 'mpm3pmevusource='.$_POST[mpm3pmevusource]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "mpm3pmlls1id=") !== false) {
	    $result .= 'mpm3pmlls1id='.$_POST[mpm3pmlls1id]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "mpm3pmlls1source=") !== false) {
	    $result .= 'mpm3pmlls1source='.$_POST[mpm3pmlls1source]."\n";
	$writeit = '1';
	    }
	    if(strpos($line, "mpm3pmlls2id=") !== false) {
	    $result .= 'mpm3pmlls2id='.$_POST[mpm3pmlls2id]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "mpm3pmlls2source=") !== false) {
	    $result .= 'mpm3pmlls2source='.$_POST[mpm3pmlls2source]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "mpm3pmllid=") !== false) {
	    $result .= 'mpm3pmllid='.$_POST[mpm3pmllid]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "mpm3pmllsource=") !== false) {
	    $result .= 'mpm3pmllsource='.$_POST[mpm3pmllsource]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "evsewifitimeoutlp3=") !== false) {
	    $result .= 'evsewifitimeoutlp3='.$_POST[evsewifitimeoutlp3]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "evsewifiiplp3=") !== false) {
	    $result .= 'evsewifiiplp3='.$_POST[evsewifiiplp3]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "evsewifitimeoutlp2=") !== false) {
	    $result .= 'evsewifitimeoutlp2='.$_POST[evsewifitimeoutlp2]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "evsewifiiplp2=") !== false) {
	    $result .= 'evsewifiiplp2='.$_POST[evsewifiiplp2]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "evsewifitimeoutlp1=") !== false) {
	    $result .= 'evsewifitimeoutlp1='.$_POST[evsewifitimeoutlp1]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "evsewifiiplp1=") !== false) {
	    $result .= 'evsewifiiplp1='.$_POST[evsewifiiplp1]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "leafusername=") !== false) {
	    $result .= 'leafusername='.$_POST[leafusername]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "leafpasswort=") !== false) {
	    $result .= 'leafpasswort='.$_POST[leafpasswort]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "leafusernames1=") !== false) {
	    $result .= 'leafusernames1='.$_POST[leafusernames1]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "leafpassworts1=") !== false) {
	    $result .= 'leafpassworts1='.$_POST[leafpassworts1]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "i3username=") !== false) {
	    $result .= 'i3username='.$_POST[i3username]."\n";
	$writeit = '1';
	    } 
	    if(strpos($line, "soci3intervall=") !== false) {
	    $result .= 'soci3intervall='.$_POST[soci3intervall]."\n";
	$writeit = '1';
    } 
  if(strpos($line, "soci3intervall1=") !== false) {
	    $result .= 'soci3intervall1='.$_POST[soci3intervall]."\n";
	$writeit = '1';
    } 

	    if(strpos($line, "i3passwort=") !== false) {
	    $result .= 'i3passwort='.$_POST[i3passwort]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "i3vin=") !== false) {
	    $result .= 'i3vin='.$_POST[i3vin]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "i3usernames1=") !== false) {
	    $result .= 'i3usernames1='.$_POST[i3usernames1]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "i3passworts1=") !== false) {
	    $result .= 'i3passworts1='.$_POST[i3passworts1]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "i3vins1=") !== false) {
	    $result .= 'i3vins1='.$_POST[i3vins1]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "zoeusername=") !== false) {
	    $result .= 'zoeusername='.$_POST[zoeusername]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "zoepasswort=") !== false) {
	    $result .= 'zoepasswort='.$_POST[zoepasswort]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "evnotifytoken=") !== false) {
	    $result .= 'evnotifytoken='.$_POST[evnotifytoken]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "evnotifyakey=") !== false) {
	    $result .= 'evnotifyakey='.$_POST[evnotifyakey]."\n";
	$writeit = '1';
	    }

	    if(strpos($line, "evnotifytokenlp2=") !== false) {
	    $result .= 'evnotifytokenlp2='.$_POST[evnotifytokenlp2]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "evnotifyakeylp2=") !== false) {
	    $result .= 'evnotifyakeylp2='.$_POST[evnotifyakeylp2]."\n";
	$writeit = '1';
    } 

	    if(strpos($line, "wrjsonurl=") !== false) {
	    $result .= 'wrjsonurl=\''.$_POST[wrjsonurl]."'\n";
	$writeit = '1';
    } 
	    if(strpos($line, "wrjsonwatt=") !== false) {
	    $result .= 'wrjsonwatt=\''.$_POST[wrjsonwatt]."'\n";
	$writeit = '1';
    } 
	    if(strpos($line, "wrjsonkwh=") !== false) {
	    $result .= 'wrjsonkwh=\''.$_POST[wrjsonkwh]."'\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "hausbezugnone=") !== false) {
	    $result .= 'hausbezugnone='.$_POST[hausbezugnone]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "mpm3pmpvsource=") !== false) {
	    $result .= 'mpm3pmpvsource='.$_POST[mpm3pmpvsource]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "mpm3pmpvid=") !== false) {
	    $result .= 'mpm3pmpvid='.$_POST[mpm3pmpvid]."\n";
	  $writeit = '1';
  } 
	    if(strpos($line, "mpm3pmpvlanip=") !== false) {
	    $result .= 'mpm3pmpvlanip='.$_POST[mpm3pmpvlanip]."\n";
	$writeit = '1';
    } 
	    if(strpos($line, "bezugjsonurl=") !== false) {
	    $result .= 'bezugjsonurl=\''.$_POST[bezugjsonurl]."'\n";
	$writeit = '1';
    } 
	    if(strpos($line, "bezugjsonwatt=") !== false) {
	    $result .= 'bezugjsonwatt=\''.$_POST[bezugjsonwatt]."'\n";
	$writeit = '1';
    } 
	    if(strpos($line, "bezugjsonkwh=") !== false) {
	    $result .= 'bezugjsonkwh=\''.$_POST[bezugjsonkwh]."'\n";
	$writeit = '1';
    } 
	    if(strpos($line, "einspeisungjsonkwh=") !== false) {
	    $result .= 'einspeisungjsonkwh=\''.$_POST[einspeisungjsonkwh]."'\n";
	$writeit = '1';
    } 
	    if(strpos($line, "bezug_solarlog_ip=") !== false) {
	    $result .= 'bezug_solarlog_ip=\''.$_POST[bezug_solarlog_ip]."'\n";
	$writeit = '1';
    } 
	    if(strpos($line, "speicherleistung_http=") !== false) {
	    $result .= 'speicherleistung_http=\''.$_POST[speicherleistung_http]."'\n";
	$writeit = '1';
    } 
	    if(strpos($line, "speicherikwh_http=") !== false) {
	    $result .= 'speicherikwh_http=\''.$_POST[speicherikwh_http]."'\n";
		$writeit = '1';
    } 
	    if(strpos($line, "speicherekwh_http=") !== false) {
	    $result .= 'speicherekwh_http=\''.$_POST[speicherekwh_http]."'\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "speichersoc_http=") !== false) {
	    $result .= 'speichersoc_http=\''.$_POST[speichersoc_http]."'\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "speichermodul=") !== false) {
	    $result .= 'speichermodul='.$_POST[speichermodul]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "soc_tesla_username=") !== false) {
	    $result .= 'soc_tesla_username='.$_POST[teslasocuser]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "soc_tesla_password=") !== false) {
	    $result .= 'soc_tesla_password='.$_POST[teslasocpw]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "soc_tesla_intervall=") !== false) {
	    $result .= 'soc_tesla_intervall='.$_POST[teslasocintervall]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "soc_tesla_intervallladen=") !== false) {
	    $result .= 'soc_tesla_intervallladen='.$_POST[teslasocintervallladen]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "wrkostalpikoip=") !== false) {
    	    $result .= 'wrkostalpikoip='.$_POST[wrkostalpikoip]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "solaredgeip=") !== false) {
	    $result .= 'solaredgeip=\''.$_POST[solaredgeip]."'\n";
	 $writeit = '1';
	    }
	    if(strpos($line, "solaredgepvip=") !== false) {
	    $result .= 'solaredgepvip=\''.$_POST[solaredgepvip]."'\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "solaredgepvslave1=") !== false) {
	    $result .= 'solaredgepvslave1='.$_POST[solaredgepvslave1]."\n";
	 $writeit = '1';
	    } 
	    if(strpos($line, "solaredgepvslave2=") !== false) {
	    $result .= 'solaredgepvslave2='.$_POST[solaredgepvslave2]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "solaredgepvslave3=") !== false) {
	    $result .= 'solaredgepvslave3='.$_POST[solaredgepvslave3]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "lllaniplp2=") !== false) {
    	    $result .= 'lllaniplp2='.$_POST[lllaniplp2]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "sdm630lp2source=") !== false) {
    	    $result .= 'sdm630lp2source='.$_POST[sdm630lp2source]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "sdm120lp2source=") !== false) {
    	    $result .= 'sdm120lp2source='.$_POST[sdm120lp2source]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "sdm630lp3source=") !== false) {
    	    $result .= 'sdm630lp3source='.$_POST[sdm630lp3source]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "sdm120lp3source=") !== false) {
    	    $result .= 'sdm120lp3source='.$_POST[sdm120lp3source]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "lllaniplp3=") !== false) {
    	    $result .= 'lllaniplp3='.$_POST[lllaniplp3]."\n";
    	 $writeit = '1';
   } 

	    if(strpos($line, "lp1name=") !== false) {
		    $result .= 'lp1name=\''.$_POST[lp1name]."'\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "lp2name=") !== false) {
		$result .= 'lp2name=\''.$_POST[lp2name]."'\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "lp3name=") !== false) {
		$result .= 'lp3name=\''.$_POST[lp3name]."'\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "goeiplp1=") !== false) {
    	    $result .= 'goeiplp1='.$_POST[goeiplp1]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "goeiplp2=") !== false) {
    	    $result .= 'goeiplp2='.$_POST[goeiplp2]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "goeiplp3=") !== false) {
    	    $result .= 'goeiplp3='.$_POST[goeiplp3]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "goetimeoutlp1=") !== false) {
    	    $result .= 'goetimeoutlp1='.$_POST[goetimeoutlp1]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "goetimeoutlp2=") !== false) {
    	    $result .= 'goetimeoutlp2='.$_POST[goetimeoutlp2]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "goetimeoutlp3=") !== false) {
    	    $result .= 'goetimeoutlp3='.$_POST[goetimeoutlp3]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "smashmbezugid=") !== false) {
	    $result .= 'smashmbezugid='.$_POST[smashmbezugid]."\n";
	 $writeit = '1';
   } 
	    if(strpos($line, "wrfroniusip=") !== false) {
    	    $result .= 'wrfroniusip='.$_POST[wrfroniusip]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "mpm3pmspeicherpv=") !== false) {
    	    $result .= 'mpm3pmspeicherpv='.$_POST[mpm3pmspeicherpv]."\n";
    	 $writeit = '1';
   } 
	    if(strpos($line, "mpm3pmspeicherid=") !== false) {
    	    $result .= 'mpm3pmspeicherid='.$_POST[mpm3pmspeicherid]."\n";
    	 $writeit = '1';
   } 
   	    if(strpos($line, "mpm3pmspeichersource=") !== false) {
    	    $result .= 'mpm3pmspeichersource='.$_POST[mpm3pmspeichersource]."\n";
    	 $writeit = '1';
   } 
  	    if(strpos($line, "mpm3pmspeicherlanip=") !== false) {
    	    $result .= 'mpm3pmspeicherlanip='.$_POST[mpm3pmspeicherlanip]."\n";
    	  $writeit = '1';
  } 
	if(strpos($line, "bezug_smartme_user=") !== false) {
	    $result .= 'bezug_smartme_user=\''.$_POST[bezug_smartme_user]."'\n";
	    $writeit = '1';
	    } 
	if(strpos($line, "bezug_smartme_pass=") !== false) {
	    $result .= 'bezug_smartme_pass=\''.$_POST[bezug_smartme_pass]."'\n";
	    $writeit = '1';
	    } 
	if(strpos($line, "bezug_smartme_url=") !== false) {
	    $result .= 'bezug_smartme_url=\''.$_POST[bezug_smartme_url]."'\n";
	    $writeit = '1';
	    } 
	   if(strpos($line, "carnetuser=") !== false) {
	    $result .= 'carnetuser=\''.$_POST[carnetuser]."'\n";
	    $writeit = '1';
	    }
	   if(strpos($line, "carnetpass=") !== false) {
	    $result .= 'carnetpass=\''.$_POST[carnetpass]."'\n";
	    $writeit = '1';
	    }
            if(strpos($line, "soccarnetintervall=") !== false) {
		$result .= 'soccarnetintervall='.$_POST[soccarnetintervall]."\n";
		$writeit = '1';
	    }
	   if(strpos($line, "bydhvuser=") !== false) {
	    $result .= 'bydhvuser='.$_POST[bydhvuser]."\n";
	    $writeit = '1';
	    }
	   if(strpos($line, "bydhvpass=") !== false) {
	    $result .= 'bydhvpass='.$_POST[bydhvpass]."\n";
	    $writeit = '1';
	    }
	   if(strpos($line, "bydhvip=") !== false) {
	    $result .= 'bydhvip='.$_POST[bydhvip]."\n";
	    $writeit = '1';
	    }
	   if(strpos($line, "wr_smartme_user=") !== false) {
	    $result .= 'wr_smartme_user=\''.$_POST[wr_smartme_user]."'\n";
	    $writeit = '1';
	    }
	   if(strpos($line, "wr_smartme_pass=") !== false) {
	    $result .= 'wr_smartme_pass=\''.$_POST[wr_smartme_pass]."'\n";
	    $writeit = '1';
	    }
	   if(strpos($line, "wr_smartme_url=") !== false) {
	    $result .= 'wr_smartme_url=\''.$_POST[wr_smartme_url]."'\n";
	    $writeit = '1';
	    }
	   if(strpos($line, "e3dcip=") !== false) {
	    $result .= 'e3dcip='.$_POST[e3dcip]."\n";
	    $writeit = '1';
	    }
	   if(strpos($line, "sbs25ip=") !== false) {
	    $result .= 'sbs25ip='.$_POST[sbs25ip]."\n";
	    $writeit = '1';
	    }
	   if(strpos($line, "tri9000ip=") !== false) {
	    $result .= 'tri9000ip='.$_POST[tri9000ip]."\n";
	    $writeit = '1';
	    





	    if ( $writeit == '0') {
		$result .= $line;
	}
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

 



$result = '';
$lines = file('/var/www/html/openWB/web/files/smashm.conf');
foreach($lines as $line) {
	    if(strpos($line, "serials=") !== false) {
		    	    $result .= 'serials='.$_POST[smashmbezugid]."\n";
			    	    } 
	    else {
		    	    $result .= $line;
			    	    }
}
file_put_contents('/var/www/html/openWB/web/files/smashm.conf', $result);




$i3soc = "/var/www/html/openWB/modules/soc_i3/auth.json";
$i3soc = fopen($i3soc, 'w');
fwrite($i3soc,"{".PHP_EOL.'"username": "'.$_POST[i3username].'",'.PHP_EOL.'"password": "'.$_POST[i3passwort].'",'.PHP_EOL.'"vehicle": "'.$_POST[i3vin].'"'.PHP_EOL."}".PHP_EOL);
$i3soc1 = "/var/www/html/openWB/modules/soc_i3s1/auth.json";
$i3soc1 = fopen($i3soc1, 'w');
fwrite($i3soc1,"{".PHP_EOL.'"username": "'.$_POST[i3usernames1].'",'.PHP_EOL.'"password": "'.$_POST[i3passworts1].'",'.PHP_EOL.'"vehicle": "'.$_POST[i3vins1].'"'.PHP_EOL."}".PHP_EOL);



}
header("Location: ../index.php");

?>





