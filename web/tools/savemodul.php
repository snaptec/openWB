
<?php
if(isset($_POST['evsecon'])) {
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsecon=") !== false) {
	    $result .= 'evsecon='.$_POST[evsecon]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "dacregisters1=") !== false) {
	    $result .= 'dacregisters1='.$_POST[dacregisters1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "dacregister=") !== false) {
	    $result .= 'dacregister='.$_POST[dacregister]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "modbusevsesource=") !== false) {
	    $result .= 'modbusevsesource='.$_POST[modbusevsesource]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "modbusevseid=") !== false) {
	    $result .= 'modbusevseid='.$_POST[modbusevseid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "wattbezugmodul=") !== false) {
	    $result .= 'wattbezugmodul='.$_POST[wattbezugmodul]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "vzloggerip=") !== false) {
	    $result .= 'vzloggerip='.$_POST[vzloggerip]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "vzloggerpvip=") !== false) {
	    $result .= 'vzloggerpvip='.$_POST[vzloggerpvip]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "vzloggerline=") !== false) {
	    $result .= 'vzloggerline='.$_POST[vzloggerline]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "vzloggerkwhline=") !== false) {
	    $result .= 'vzloggerkwhline='.$_POST[vzloggerkwhline]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "vzloggerekwhline=") !== false) {
	    $result .= 'vzloggerekwhline='.$_POST[vzloggerekwhline]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "vzloggerpvline=") !== false) {
	    $result .= 'vzloggerpvline='.$_POST[vzloggerpvline]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630modbusbezugid=") !== false) {
	    $result .= 'sdm630modbusbezugid='.$_POST[sdm630modbusbezugid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630modbusbezugsource=") !== false) {
	    $result .= 'sdm630modbusbezugsource='.$_POST[sdm630modbusbezugsource]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "pvwattmodul=") !== false) {
	    $result .= 'pvwattmodul='.$_POST[pvwattmodul]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "wrfroniusip=") !== false) {
	    $result .= 'wrfroniusip='.$_POST[wrfroniusip]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	if(strpos($line, "ladeleistungmodul=") !== false) {
		if($_POST[evsecon] == "simpleevsewifi") {
			$result .= 'ladeleistungmodul=simpleevsewifi'."\n";
		} else {
			$result .= 'ladeleistungmodul='.$_POST[ladeleistungmodul]."\n";
	    } 
	} else {
	    $result .= $line;
	    }
}



file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630modbusllid=") !== false) {
	    $result .= 'sdm630modbusllid='.$_POST[sdm630modbusllid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630modbusllsource=") !== false) {
	    $result .= 'sdm630modbusllsource='.$_POST[sdm630modbusllsource]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630modbusbezuglanip=") !== false) {
	    $result .= 'sdm630modbusbezuglanip='.$_POST[sdm630modbusbezuglanip]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630modbuswrid=") !== false) {
	    $result .= 'sdm630modbuswrid='.$_POST[sdm630modbuswrid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630modbuswrsource=") !== false) {
	    $result .= 'sdm630modbuswrsource='.$_POST[sdm630modbuswrsource]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630modbuswrlanip=") !== false) {
	    $result .= 'sdm630modbuswrlanip='.$_POST[sdm630modbuswrlanip]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630modbuslllanip=") !== false) {
	    $result .= 'sdm630modbuslllanip='.$_POST[sdm630modbuslllanip]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "socmodul=") !== false) {
	    $result .= 'socmodul='.$_POST[socmodul]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "socmodul1=") !== false) {
	    $result .= 'socmodul1='.$_POST[socmodul1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "hsocip=") !== false) {
	    $result .= 'hsocip=\''.$_POST[hsocip]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "hsocip1=") !== false) {
	    $result .= 'hsocip1='.$_POST[hsocip1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';

$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "modbusevselanip=") !== false) {
	    $result .= 'modbusevselanip='.$_POST[modbusevselanip]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsecons1=") !== false) {
	    $result .= 'evsecons1='.$_POST[evsecons1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsecons2=") !== false) {
	    $result .= 'evsecons2='.$_POST[evsecons2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsesources1=") !== false) {
	    $result .= 'evsesources1='.$_POST[evsesources1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsesources2=") !== false) {
	    $result .= 'evsesources2='.$_POST[evsesources2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evseids1=") !== false) {
	    $result .= 'evseids1='.$_POST[evseids1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evseids2=") !== false) {
	    $result .= 'evseids2='.$_POST[evseids2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evselanips1=") !== false) {
	    $result .= 'evselanips1='.$_POST[evselanips1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evselanips2=") !== false) {
	    $result .= 'evselanips2='.$_POST[evselanips2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';

$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "lastmanagement=") !== false) {
	    $result .= 'lastmanagement='.$_POST[lastmanagement]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "lastmanagements2=") !== false) {
		    if($_POST[lastmanagement] == 0) {
			$result .= 'lastmanagements2=0'."\n";
		    } else {						
			$result .= 'lastmanagements2='.$_POST[lastmanagements2]."\n";
	    	    } 
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdmids1=") !== false) {
	    $result .= 'sdmids1='.$_POST[sdmids1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdmids2=") !== false) {
	    $result .= 'sdmids2='.$_POST[sdmids2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "smaemdbezugid=") !== false) {
	    $result .= 'smaemdbezugid='.$_POST[smaemdbezugid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "smaemdllid=") !== false) {
	    $result .= 'smaemdllid='.$_POST[smaemdllid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "smaemdpvid=") !== false) {
	    $result .= 'smaemdpvid='.$_POST[smaemdpvid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "ladeleistungs1modul=") !== false) {
	    	if($_POST[evsecons1] == "simpleevsewifi") {
			$result .= 'ladeleistungs1modul=simpleevsewifis1'."\n";
		} else {
			$result .= 'ladeleistungs1modul='.$_POST[ladeleistungs1modul]."\n";
	    } 

	    }  else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "ladeleistungs2modul=") !== false) {
	    	if($_POST[evsecons2] == "simpleevsewifi") {
			$result .= 'ladeleistungs2modul=simpleevsewifis2'."\n";
		} else {
			$result .= 'ladeleistungs2modul='.$_POST[ladeleistungs2modul]."\n";
	    } 

	    }  else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "wr_http_w_url=") !== false) {
	    $result .= 'wr_http_w_url=\''.$_POST[wr_http_w_url]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "wr_http_kwh_url=") !== false) {
	    $result .= 'wr_http_kwh_url=\''.$_POST[wr_http_kwh_url]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "bezug_http_w_url=") !== false) {
	    $result .= 'bezug_http_w_url=\''.$_POST[bezug_http_w_url]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "bezug_http_ekwh_url=") !== false) {
	    $result .= 'bezug_http_ekwh_url=\''.$_POST[bezug_http_ekwh_url]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "bezug_http_ikwh_url=") !== false) {
	    $result .= 'bezug_http_ikwh_url=\''.$_POST[bezug_http_ikwh_url]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120modbusllid1s1=") !== false) {
	    $result .= 'sdm120modbusllid1s1='.$_POST[sdm120modbusllid1s1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120modbusllid2s1=") !== false) {
	    $result .= 'sdm120modbusllid2s1='.$_POST[sdm120modbusllid2s1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120modbusllid3s1=") !== false) {
	    $result .= 'sdm120modbusllid3s1='.$_POST[sdm120modbusllid3s1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120modbusllid1s2=") !== false) {
	    $result .= 'sdm120modbusllid1s2='.$_POST[sdm120modbusllid1s2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120modbusllid2s2=") !== false) {
	    $result .= 'sdm120modbusllid2s2='.$_POST[sdm120modbusllid2s2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120modbusllid3s2=") !== false) {
	    $result .= 'sdm120modbusllid3s2='.$_POST[sdm120modbusllid3s2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120modbusllid1=") !== false) {
	    $result .= 'sdm120modbusllid1='.$_POST[sdm120modbusllid1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120modbusllid2=") !== false) {
	    $result .= 'sdm120modbusllid2='.$_POST[sdm120modbusllid2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120modbusllid3=") !== false) {
	    $result .= 'sdm120modbusllid3='.$_POST[sdm120modbusllid3]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';

$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mpm3pmevuid=") !== false) {
	    $result .= 'mpm3pmevuid='.$_POST[mpm3pmevuid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mpm3pmevusource=") !== false) {
	    $result .= 'mpm3pmevusource='.$_POST[mpm3pmevusource]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';


$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mpm3pmlls1id=") !== false) {
	    $result .= 'mpm3pmlls1id='.$_POST[mpm3pmlls1id]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);




$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mpm3pmlls1source=") !== false) {
	    $result .= 'mpm3pmlls1source='.$_POST[mpm3pmlls1source]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';


$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mpm3pmllid=") !== false) {
	    $result .= 'mpm3pmllid='.$_POST[mpm3pmllid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);




$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mpm3pmllsource=") !== false) {
	    $result .= 'mpm3pmllsource='.$_POST[mpm3pmllsource]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsewifitimeoutlp3=") !== false) {
	    $result .= 'evsewifitimeoutlp3='.$_POST[evsewifitimeoutlp3]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsewifiiplp3=") !== false) {
	    $result .= 'evsewifiiplp3='.$_POST[evsewifiiplp3]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsewifitimeoutlp2=") !== false) {
	    $result .= 'evsewifitimeoutlp2='.$_POST[evsewifitimeoutlp2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsewifiiplp2=") !== false) {
	    $result .= 'evsewifiiplp2='.$_POST[evsewifiiplp2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsewifitimeoutlp1=") !== false) {
	    $result .= 'evsewifitimeoutlp1='.$_POST[evsewifitimeoutlp1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evsewifiiplp1=") !== false) {
	    $result .= 'evsewifiiplp1='.$_POST[evsewifiiplp1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "leafusername=") !== false) {
	    $result .= 'leafusername='.$_POST[leafusername]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "leafpasswort=") !== false) {
	    $result .= 'leafpasswort='.$_POST[leafpasswort]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "leafusernames1=") !== false) {
	    $result .= 'leafusernames1='.$_POST[leafusernames1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "leafpassworts1=") !== false) {
	    $result .= 'leafpassworts1='.$_POST[leafpassworts1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "i3username=") !== false) {
	    $result .= 'i3username='.$_POST[i3username]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "i3passwort=") !== false) {
	    $result .= 'i3passwort='.$_POST[i3passwort]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "i3vin=") !== false) {
	    $result .= 'i3vin='.$_POST[i3vin]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "i3usernames1=") !== false) {
	    $result .= 'i3usernames1='.$_POST[i3usernames1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "i3passworts1=") !== false) {
	    $result .= 'i3passworts1='.$_POST[i3passworts1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "i3vins1=") !== false) {
	    $result .= 'i3vins1='.$_POST[i3vins1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$i3soc = "/var/www/html/openWB/modules/soc_i3/auth.json";
$i3soc = fopen($i3soc, 'w');
fwrite($i3soc,"{".PHP_EOL.'"username": "'.$_POST[i3username].'",'.PHP_EOL.'"password": "'.$_POST[i3passwort].'",'.PHP_EOL.'"vehicle": "'.$_POST[i3vin].'"'.PHP_EOL."}".PHP_EOL);
$i3soc1 = "/var/www/html/openWB/modules/soc_i3s1/auth.json";
$i3soc1 = fopen($i3soc1, 'w');
fwrite($i3soc1,"{".PHP_EOL.'"username": "'.$_POST[i3usernames1].'",'.PHP_EOL.'"password": "'.$_POST[i3passworts1].'",'.PHP_EOL.'"vehicle": "'.$_POST[i3vins1].'"'.PHP_EOL."}".PHP_EOL);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "zoeusername=") !== false) {
	    $result .= 'zoeusername='.$_POST[zoeusername]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "zoepasswort=") !== false) {
	    $result .= 'zoepasswort='.$_POST[zoepasswort]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evnotifypasswort=") !== false) {
	    $result .= 'evnotifypasswort='.$_POST[evnotifypasswort]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "evnotifyakey=") !== false) {
	    $result .= 'evnotifyakey='.$_POST[evnotifyakey]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "wrjsonurl=") !== false) {
	    $result .= 'wrjsonurl=\''.$_POST[wrjsonurl]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "wrjsonwatt=") !== false) {
	    $result .= 'wrjsonwatt=\''.$_POST[wrjsonwatt]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "wrjsonkwh=") !== false) {
	    $result .= 'wrjsonkwh=\''.$_POST[wrjsonkwh]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);


$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "hausbezugnone=") !== false) {
	    $result .= 'hausbezugnone='.$_POST[hausbezugnone]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mpm3pmpvsource=") !== false) {
	    $result .= 'mpm3pmpvsource='.$_POST[mpm3pmpvsource]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mpm3pmpvid=") !== false) {
	    $result .= 'mpm3pmpvid='.$_POST[mpm3pmpvid]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mpm3pmpvlanip=") !== false) {
	    $result .= 'mpm3pmpvlanip='.$_POST[mpm3pmpvlanip]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "bezugjsonurl=") !== false) {
	    $result .= 'bezugjsonurl=\''.$_POST[bezugjsonurl]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "bezugjsonwatt=") !== false) {
	    $result .= 'bezugjsonwatt=\''.$_POST[bezugjsonwatt]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "bezugjsonkwh=") !== false) {
	    $result .= 'bezugjsonkwh=\''.$_POST[bezugjsonkwh]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "einspeisungjsonkwh=") !== false) {
	    $result .= 'einspeisungjsonkwh=\''.$_POST[einspeisungjsonkwh]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "bezug_solarlog_ip=") !== false) {
	    $result .= 'bezug_solarlog_ip=\''.$_POST[bezug_solarlog_ip]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "speicherleistung_http=") !== false) {
	    $result .= 'speicherleistung_http=\''.$_POST[speicherleistung_http]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "speichersoc_http=") !== false) {
	    $result .= 'speichersoc_http=\''.$_POST[speichersoc_http]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "speichermodul=") !== false) {
	    $result .= 'speichermodul='.$_POST[speichermodul]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "soc_tesla_username=") !== false) {
	    $result .= 'soc_tesla_username='.$_POST[teslasocuser]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "soc_tesla_password=") !== false) {
	    $result .= 'soc_tesla_password='.$_POST[teslasocpw]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "soc_tesla_intervall=") !== false) {
	    $result .= 'soc_tesla_intervall='.$_POST[teslasocintervall]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "wrkostalpikoip=") !== false) {
    	    $result .= 'wrkostalpikoip='.$_POST[wrkostalpikoip]."\n";
    	    } 
   	    else {
    	    $result .= $line;
    	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "solaredgeip=") !== false) {
	    $result .= 'solaredgeip=\''.$_POST[solaredgeip]."'\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "lllaniplp2=") !== false) {
    	    $result .= 'lllaniplp2='.$_POST[lllaniplp2]."\n";
    	    } 
   	    else {
    	    $result .= $line;
    	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630lp2source=") !== false) {
    	    $result .= 'sdm630lp2source='.$_POST[sdm630lp2source]."\n";
    	    } 
   	    else {
    	    $result .= $line;
    	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120lp2source=") !== false) {
    	    $result .= 'sdm120lp2source='.$_POST[sdm120lp2source]."\n";
    	    } 
   	    else {
    	    $result .= $line;
    	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm630lp3source=") !== false) {
    	    $result .= 'sdm630lp3source='.$_POST[sdm630lp3source]."\n";
    	    } 
   	    else {
    	    $result .= $line;
    	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sdm120lp3source=") !== false) {
    	    $result .= 'sdm120lp3source='.$_POST[sdm120lp3source]."\n";
    	    } 
   	    else {
    	    $result .= $line;
    	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);


$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "lllaniplp3=") !== false) {
    	    $result .= 'lllaniplp3='.$_POST[lllaniplp3]."\n";
    	    } 
   	    else {
    	    $result .= $line;
    	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);







}
header("Location: ../index.php");

?>



