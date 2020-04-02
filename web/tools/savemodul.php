<?php
if(isset($_POST['evsecon'])) {
	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		$writeit = '0';
		if(strpos($line, "evsecon=") !== false) {
			if($_POST['evsecon'] == "openwb12" or $_POST['evsecon'] == "openwb12mid") {
				$result .= 'evsecon=modbusevse'."\n";
			} else {
				$result .= 'evsecon='.$_POST['evsecon']."\n";
			}
			$writeit = '1';
		}
			if(strpos($line, "dacregisters1=") !== false) {
			$result .= 'dacregisters1='.$_POST['dacregisters1']."\n";
			$writeit = '1';
			}
			if(strpos($line, "soc_bluelink_interval=") !== false) {
			$result .= 'soc_bluelink_interval='.$_POST['soc_bluelink_interval']."\n";
			$writeit = '1';
			}
			if(strpos($line, "soc_bluelink_email=") !== false) {
			$result .= 'soc_bluelink_email='.$_POST['soc_bluelink_email']."\n";
			$writeit = '1';
			}
			if(strpos($line, "soc_bluelink_password=") !== false) {
			$result .= 'soc_bluelink_password='.$_POST['soc_bluelink_password']."\n";
			$writeit = '1';
			}
			if(strpos($line, "soc_bluelink_pin=") !== false) {
			$result .= 'soc_bluelink_pin='.$_POST['soc_bluelink_pin']."\n";
			$writeit = '1';
			}
			if(strpos($line, "solarworld_emanagerip=") !== false) {
			$result .= 'solarworld_emanagerip='.$_POST['solarworld_emanagerip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "dacregister=") !== false) {
			$result .= 'dacregister='.$_POST['dacregister']."\n";
			$writeit = '1';
			}
			if(strpos($line, "femsip=") !== false) {
			$result .= 'femsip='.$_POST['femsip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "modbusevsesource=") !== false) {
			if($_POST['evsecon'] == "openwb12" or $_POST['evsecon'] == "openwb12mid") {
				$result .= 'modbusevsesource=/dev/ttyUSB0'."\n";
			} else {

				$result .= 'modbusevsesource='.$_POST['modbusevsesource']."\n";
			}
			$writeit = '1';
			}
			if(strpos($line, "modbusevseid=") !== false) {
			if($_POST['evsecon'] == "openwb12" or $_POST['evsecon'] == "openwb12mid") {
				$result .= 'modbusevseid=1'."\n";
			} else {
					$result .= 'modbusevseid='.$_POST['modbusevseid']."\n";
			}
			$writeit = '1';
			}
			if(strpos($line, "wattbezugmodul=") !== false) {
			$result .= 'wattbezugmodul='.$_POST['wattbezugmodul']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evukitversion=") !== false) {
			$result .= 'evukitversion='.$_POST['evukitversion']."\n";
			$writeit = '1';
			}
			if(strpos($line, "pvkitversion=") !== false) {
			$result .= 'pvkitversion='.$_POST['pvkitversion']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseidlp3=") !== false) {
			$result .= 'evseidlp3='.$_POST['evseidlp3']."\n";
			$writeit = '1';
			}
			if(strpos($line, "wrsunwaysip=") !== false) {
			$result .= 'wrsunwaysip='.$_POST['wrsunwaysip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "wrsunwayspw=") !== false) {
			$result .= 'wrsunwayspw='.$_POST['wrsunwayspw']."\n";
			$writeit = '1';
			}
			if(strpos($line, "myrenault_userlp2=") !== false) {
			$result .= 'myrenault_userlp2='.$_POST['myrenault_userlp2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "myrenault_passlp2=") !== false) {
			$result .= 'myrenault_passlp2='.$_POST['myrenault_passlp2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "myrenault_countrylp2=") !== false) {
			$result .= 'myrenault_countrylp2='.$_POST['myrenault_countrylp2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "myrenault_locationlp2=") !== false) {
			$result .= 'myrenault_locationlp2='.$_POST['myrenault_locationlp2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "myrenault_userlp1=") !== false) {
			$result .= 'myrenault_userlp1='.$_POST['myrenault_userlp1']."\n";
			$writeit = '1';
			}
			if(strpos($line, "myrenault_passlp1=") !== false) {
			$result .= 'myrenault_passlp1='.$_POST['myrenault_passlp1']."\n";
			$writeit = '1';
			}
			if(strpos($line, "myrenault_countrylp1=") !== false) {
			$result .= 'myrenault_countrylp1='.$_POST['myrenault_countrylp1']."\n";
			$writeit = '1';
			}
			if(strpos($line, "myrenault_locationlp1=") !== false) {
			$result .= 'myrenault_locationlp1='.$_POST['myrenault_locationlp1']."\n";
			$writeit = '1';
			}

			if(strpos($line, "evseiplp3=") !== false) {
			$result .= 'evseiplp3='.$_POST['evseiplp3']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseidlp1=") !== false) {
			$result .= 'evseidlp1='.$_POST['evseidlp1']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseiplp1=") !== false) {
			$result .= 'evseiplp1='.$_POST['evseiplp1']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseidlp2=") !== false) {
			$result .= 'evseidlp2='.$_POST['evseidlp2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseiplp2=") !== false) {
			$result .= 'evseiplp2='.$_POST['evseiplp2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseidlp4=") !== false) {
			$result .= 'evseidlp4='.$_POST['evseidlp4']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseiplp4=") !== false) {
			$result .= 'evseiplp4='.$_POST['evseiplp4']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp4id=") !== false) {
			$result .= 'mpmlp4id='.$_POST['mpmlp4id']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp4ip=") !== false) {
			$result .= 'mpmlp4ip='.$_POST['mpmlp4ip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp1id=") !== false) {
			$result .= 'mpmlp1id='.$_POST['mpmlp1id']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp1ip=") !== false) {
			$result .= 'mpmlp1ip='.$_POST['mpmlp1ip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp2id=") !== false) {
			$result .= 'mpmlp2id='.$_POST['mpmlp2id']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp2ip=") !== false) {
			$result .= 'mpmlp2ip='.$_POST['mpmlp2ip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp3id=") !== false) {
			$result .= 'mpmlp3id='.$_POST['mpmlp3id']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp3ip=") !== false) {
			$result .= 'mpmlp3ip='.$_POST['mpmlp3ip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "lastmanagementlp4=") !== false) {
			$result .= 'lastmanagementlp4='.$_POST['lastmanagementlp4']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseidlp5=") !== false) {
			$result .= 'evseidlp5='.$_POST['evseidlp5']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseiplp5=") !== false) {
			$result .= 'evseiplp5='.$_POST['evseiplp5']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp5id=") !== false) {
			$result .= 'mpmlp5id='.$_POST['mpmlp5id']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp5ip=") !== false) {
			$result .= 'mpmlp5ip='.$_POST['mpmlp5ip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "lastmanagementlp5=") !== false) {
			$result .= 'lastmanagementlp5='.$_POST['lastmanagementlp5']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseidlp6=") !== false) {
			$result .= 'evseidlp6='.$_POST['evseidlp6']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseiplp6=") !== false) {
			$result .= 'evseiplp6='.$_POST['evseiplp6']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp6id=") !== false) {
			$result .= 'mpmlp6id='.$_POST['mpmlp6id']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp6ip=") !== false) {
			$result .= 'mpmlp6ip='.$_POST['mpmlp6ip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "lastmanagementlp6=") !== false) {
			$result .= 'lastmanagementlp6='.$_POST['lastmanagementlp6']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseidlp7=") !== false) {
			$result .= 'evseidlp7='.$_POST['evseidlp7']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseiplp7=") !== false) {
			$result .= 'evseiplp7='.$_POST['evseiplp7']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp7id=") !== false) {
			$result .= 'mpmlp7id='.$_POST['mpmlp7id']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp7ip=") !== false) {
			$result .= 'mpmlp7ip='.$_POST['mpmlp7ip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "lastmanagementlp7=") !== false) {
			$result .= 'lastmanagementlp7='.$_POST['lastmanagementlp7']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseidlp8=") !== false) {
			$result .= 'evseidlp8='.$_POST['evseidlp8']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseiplp8=") !== false) {
			$result .= 'evseiplp8='.$_POST['evseiplp8']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp8id=") !== false) {
			$result .= 'mpmlp8id='.$_POST['mpmlp8id']."\n";
			$writeit = '1';
			}
			if(strpos($line, "mpmlp8ip=") !== false) {
			$result .= 'mpmlp8ip='.$_POST['mpmlp8ip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "lastmanagementlp8=") !== false) {
			$result .= 'lastmanagementlp8='.$_POST['lastmanagementlp8']."\n";
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
		if(strpos($line, "ladeleistungmodul=") !== false) {
			if($_POST['evsecon'] == "simpleevsewifi" or $_POST['evsecon'] == "goe" or $_POST['evsecon'] == "twcmanager" or $_POST['evsecon'] == "masterethframer" or $_POST['evsecon'] == "nrgkick" or $_POST['evsecon'] == "keba" or $_POST['evsecon'] == "openwb12" or $_POST['evsecon'] == "openwb12mid") {
				if($_POST['evsecon'] == "goe") {
					$result .= 'ladeleistungmodul=goelp1'."\n";
				}
				if($_POST['evsecon'] == "twcmanager") {
					$result .= 'ladeleistungmodul=twcmanagerlp1'."\n";
				}
				if($_POST['evsecon'] == "openwb12" or $_POST['evsecon'] == "openwb12mid") {
					$result .= 'ladeleistungmodul=mpm3pmll'."\n";
				}
				if($_POST['evsecon'] == "keba") {
					$result .= 'ladeleistungmodul=keballlp1'."\n";
				}
				if($_POST['evsecon'] == "nrgkick") {
					$result .= 'ladeleistungmodul=nrgkicklp1'."\n";
				}
				if($_POST['evsecon'] == "masterethframer") {
					$result .= 'ladeleistungmodul=mpm3pmethllframer'."\n";
				}
				if($_POST['evsecon'] == "simpleevsewifi") {
					$result .= 'ladeleistungmodul=simpleevsewifi'."\n";
				}
			} else {
				$result .= 'ladeleistungmodul='.$_POST['ladeleistungmodul']."\n";
			}
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
			if(strpos($line, "fsm63a3modbusllid=") !== false) {
			$result .= 'fsm63a3modbusllid='.$_POST['fsm63a3modbusllid']."\n";
			$writeit = '1';
			}
			if(strpos($line, "fsm63a3modbusllsource=") !== false) {
			$result .= 'fsm63a3modbusllsource='.$_POST['fsm63a3modbusllsource']."\n";
			$writeit = '1';
			}
			if(strpos($line, "sdm120modbusllsource=") !== false) {
			$result .= 'sdm120modbusllsource='.$_POST['sdm120modbusllsource']."\n";
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
			if(strpos($line, "modbusevselanip=") !== false) {
			$result .= 'modbusevselanip='.$_POST['modbusevselanip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evsecons1=") !== false) {
			if($_POST['evsecons1'] == "openwb12s1" or $_POST['evsecons1'] == "openwb12s1mid") {
				$result .= 'evsecons1=modbusevse'."\n";
			} else {
				$result .= 'evsecons1='.$_POST['evsecons1']."\n";
			}


			$writeit = '1';
			}
			if(strpos($line, "evsecons2=") !== false) {
			$result .= 'evsecons2='.$_POST['evsecons2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evsesources1=") !== false) {
			if($_POST['evsecons1'] == "openwb12s1" or $_POST['evsecons1'] == "openwb12s1mid") {
				$result .= 'evsesources1=/dev/ttyUSB1'."\n";
			} else {

				$result .= 'evsesources1='.$_POST['evsesources1']."\n";
			}
			$writeit = '1';
			}
			if(strpos($line, "evsesources2=") !== false) {
			$result .= 'evsesources2='.$_POST['evsesources2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "evseids1=") !== false) {
			if($_POST['evsecons1'] == "openwb12s1" or $_POST['evsecons1'] == "openwb12s1mid") {
				$result .= 'evseids1=1'."\n";
			} else {
				$result .= 'evseids1='.$_POST['evseids1']."\n";
			}
			$writeit = '1';
			}
			if(strpos($line, "wakeupzoelp1=") !== false) {
			$result .= 'wakeupzoelp1='.$_POST['wakeupzoelp1']."\n";
			$writeit = '1';
			}
			if(strpos($line, "wakeupzoelp2=") !== false) {
			$result .= 'wakeupzoelp2='.$_POST['wakeupzoelp2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "wakeupmyrenaultlp1=") !== false) {
			$result .= 'wakeupmyrenaultlp1='.$_POST['wakeupmyrenaultlp1']."\n";
			$writeit = '1';
			}
			if(strpos($line, "wakeupmyrenaultlp2=") !== false) {
			$result .= 'wakeupmyrenaultlp2='.$_POST['wakeupmyrenaultlp2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "wrsmawebbox=") !== false) {
			$result .= 'wrsmawebbox='.$_POST['wrsmawebbox']."\n";
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
				if($_POST['lastmanagement'] == 0) {
				$result .= 'lastmanagements2=0'."\n";
				} else {
				$result .= 'lastmanagements2='.$_POST['lastmanagements2']."\n";
					}
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
				if($_POST['evsecons1'] == "simpleevsewifi" or  $_POST['evsecons1'] == "nrgkick" or $_POST['evsecons1'] == "keba" or $_POST['evsecons1'] == "goe" or $_POST['evsecons1'] == "slaveeth" or $_POST['evsecons1'] == "openwb12s1" or $_POST['evsecons1'] == "openwb12s1mid") {
				if($_POST['evsecons1'] == "nrgkick") {
					$result .= 'ladeleistungs1modul=nrgkicklp2'."\n";
				}
				if($_POST['evsecons1'] == "goe") {
					$result .= 'ladeleistungs1modul=goelp2'."\n";
				}
				if($_POST['evsecons1'] == "keba") {
					$result .= 'ladeleistungs1modul=keballlp2'."\n";
				}
				if($_POST['evsecons1'] == "slaveeth") {
					$result .= 'ladeleistungs1modul=mpm3pmethll'."\n";
				}
				if($_POST['evsecons1'] == "simpleevsewifi") {
					$result .= 'ladeleistungs1modul=simpleevsewifis1'."\n";
				}
				if($_POST['evsecons1'] == "openwb12s1" or $_POST['evsecons1'] == "openwb12s1mid") {
					$result .= 'ladeleistungs1modul=mpm3pmlls1'."\n";
				}
			} else {
				$result .= 'ladeleistungs1modul='.$_POST['ladeleistungs1modul']."\n";
			}
			$writeit = '1';
			}
			if(strpos($line, "ladeleistungs2modul=") !== false) {
				if($_POST['evsecons2'] == "simpleevsewifi" or $_POST['evsecons2'] == "goe" or $_POST['evsecons2'] == "thirdeth") {
				if($_POST['evsecons2'] == "goe") {
					$result .= 'ladeleistungs2modul=goelp3'."\n";
				}
				if($_POST['evsecons2'] == "simpleevsewifi") {
					$result .= 'ladeleistungs2modul=simpleevsewifis2'."\n";
				}
				if($_POST['evsecons2'] == "thirdeth") {
						$result .= 'ladeleistungs2modul=mpm3pmethlls2'."\n";
				}
			} else {
				$result .= 'ladeleistungs2modul='.$_POST['ladeleistungs2modul']."\n";
			}
			$writeit = '1';
			}
			if(strpos($line, "httpll_w_url=") !== false) {
			$result .= 'httpll_w_url=\''.$_POST['httpll_w_url']."'\n";
			$writeit = '1';
			}
			if(strpos($line, "httpll_kwh_url=") !== false) {
			$result .= 'httpll_kwh_url=\''.$_POST['httpll_kwh_url']."'\n";
			$writeit = '1';
			}
			if(strpos($line, "httpll_a1_url=") !== false) {
			$result .= 'httpll_a1_url=\''.$_POST['httpll_a1_url']."'\n";
			$writeit = '1';
			}
			if(strpos($line, "httpll_a2_url=") !== false) {
			$result .= 'httpll_a2_url=\''.$_POST['httpll_a2_url']."'\n";
			$writeit = '1';
			}
			if(strpos($line, "httpll_a3_url=") !== false) {
			$result .= 'httpll_a3_url=\''.$_POST['httpll_a3_url']."'\n";
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
			if(strpos($line, "bezug_http_l1_url=") !== false) {
			$result .= 'bezug_http_l1_url=\''.$_POST['bezug_http_l1_url']."'\n";
			$writeit = '1';
			}
			if(strpos($line, "bezug_http_l2_url=") !== false) {
			$result .= 'bezug_http_l2_url=\''.$_POST['bezug_http_l2_url']."'\n";
			$writeit = '1';
			}
			if(strpos($line, "bezug_http_l3_url=") !== false) {
			$result .= 'bezug_http_l3_url=\''.$_POST['bezug_http_l3_url']."'\n";
			$writeit = '1';
			}
			if(strpos($line, "bezug_http_ekwh_url=") !== false) {
			$result .= 'bezug_http_ekwh_url=\''.$_POST['bezug_http_ekwh_url']."'\n";
			$writeit = '1';
			}
			if(strpos($line, "bezug_http_ikwh_url=") !== false) {
			$result .= 'bezug_http_ikwh_url=\''.$_POST['bezug_http_ikwh_url']."'\n";
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
			if(strpos($line, "sdm120modbusllid1s2=") !== false) {
			$result .= 'sdm120modbusllid1s2='.$_POST['sdm120modbusllid1s2']."\n";
		$writeit = '1';
	}
			if(strpos($line, "sdm120modbusllid2s2=") !== false) {
			$result .= 'sdm120modbusllid2s2='.$_POST['sdm120modbusllid2s2']."\n";
			$writeit = '1';
	}
			if(strpos($line, "sdm120modbusllid3s2=") !== false) {
			$result .= 'sdm120modbusllid3s2='.$_POST['sdm120modbusllid3s2']."\n";
		$writeit = '1';
		}
			if(strpos($line, "sdm120modbusllid1=") !== false) {
			$result .= 'sdm120modbusllid1='.$_POST['sdm120modbusllid1']."\n";
		$writeit = '1';
		}
			if(strpos($line, "sdm120modbusllid2=") !== false) {
			$result .= 'sdm120modbusllid2='.$_POST['sdm120modbusllid2']."\n";
		$writeit = '1';
		}
			if(strpos($line, "sdm120modbusllid3=") !== false) {
			$result .= 'sdm120modbusllid3='.$_POST['sdm120modbusllid3']."\n";
		$writeit = '1';
		}
			if(strpos($line, "mpm3pmevuid=") !== false) {
			$result .= 'mpm3pmevuid='.$_POST['mpm3pmevuid']."\n";
		$writeit = '1';
		}
			if(strpos($line, "mpm3pmevusource=") !== false) {
			$result .= 'mpm3pmevusource='.$_POST['mpm3pmevusource']."\n";
		$writeit = '1';
		}
			if(strpos($line, "mpm3pmlls1id=") !== false) {
				if($_POST['evsecons1'] == "openwb12s1" or $_POST['evsecons1'] == "openwb12s1mid") {
					if($_POST['evsecons1'] == "openwb12s1") {
						$result .= 'mpm3pmlls1id=6'."\n";
					}
					if($_POST['evsecons1'] == "openwb12s1mid") {
						$result .= 'mpm3pmlls1id=106'."\n";
					}

			} else {
					$result .= 'mpm3pmlls1id='.$_POST['mpm3pmlls1id']."\n";
			}
			$writeit = '1';
		}
			if(strpos($line, "mpm3pmlls1source=") !== false) {
			if($_POST['evsecons1'] == "openwb12s1" or $_POST['evsecons1'] == "openwb12s1mid") {
				$result .= 'mpm3pmlls1source=/dev/ttyUSB1'."\n";
			} else {
				$result .= 'mpm3pmlls1source='.$_POST['mpm3pmlls1source']."\n";
			}
		$writeit = '1';
			}
			if(strpos($line, "mpm3pmlls2id=") !== false) {
			$result .= 'mpm3pmlls2id='.$_POST['mpm3pmlls2id']."\n";
		$writeit = '1';
		}
			if(strpos($line, "mpm3pmlls2source=") !== false) {
			$result .= 'mpm3pmlls2source='.$_POST['mpm3pmlls2source']."\n";
		$writeit = '1';
		}
			if(strpos($line, "mpm3pmllid=") !== false) {
				if($_POST['evsecon'] == "openwb12" or $_POST['evsecon'] == "openwb12mid") {
				if($_POST['evsecon'] == "openwb12") {
					$result .= 'mpm3pmllid=5'."\n";
				}
				if($_POST['evsecon'] == "openwb12mid") {
					$result .= 'mpm3pmllid=105'."\n";
				}

			} else {
				$result .= 'mpm3pmllid='.$_POST['mpm3pmllid']."\n";
			}
		$writeit = '1';
		}
			if(strpos($line, "mpm3pmllsource=") !== false) {
			if($_POST['evsecon'] == "openwb12" or $_POST['evsecon'] == "openwb12mid") {
				$result .= 'mpm3pmllsource=/dev/ttyUSB0'."\n";
			} else {
			$result .= 'mpm3pmllsource='.$_POST['mpm3pmllsource']."\n";
			}
			$writeit = '1';
		}
			if(strpos($line, "evsewifitimeoutlp3=") !== false) {
			$result .= 'evsewifitimeoutlp3='.$_POST['evsewifitimeoutlp3']."\n";
		$writeit = '1';
		}
			if(strpos($line, "evsewifiiplp3=") !== false) {
			$result .= 'evsewifiiplp3='.$_POST['evsewifiiplp3']."\n";
		$writeit = '1';
		}
			if(strpos($line, "evsewifitimeoutlp2=") !== false) {
			$result .= 'evsewifitimeoutlp2='.$_POST['evsewifitimeoutlp2']."\n";
		$writeit = '1';
		}
			if(strpos($line, "evsewifiiplp2=") !== false) {
			$result .= 'evsewifiiplp2='.$_POST['evsewifiiplp2']."\n";
		$writeit = '1';
		}
			if(strpos($line, "evsewifitimeoutlp1=") !== false) {
			$result .= 'evsewifitimeoutlp1='.$_POST['evsewifitimeoutlp1']."\n";
		$writeit = '1';
		}
			if(strpos($line, "evsewifiiplp1=") !== false) {
			$result .= 'evsewifiiplp1='.$_POST['evsewifiiplp1']."\n";
		$writeit = '1';
		}
			if(strpos($line, "leafusername=") !== false) {
			$result .= 'leafusername='.$_POST['leafusername']."\n";
		$writeit = '1';
		}
			if(strpos($line, "leafpasswort=") !== false) {
			$result .= 'leafpasswort='.$_POST['leafpasswort']."\n";
		$writeit = '1';
		}
			if(strpos($line, "leafusernames1=") !== false) {
			$result .= 'leafusernames1='.$_POST['leafusernames1']."\n";
		$writeit = '1';
		}
			if(strpos($line, "leafpassworts1=") !== false) {
			$result .= 'leafpassworts1='.$_POST['leafpassworts1']."\n";
		$writeit = '1';
		}
			if(strpos($line, "i3username=") !== false) {
			$result .= 'i3username='.$_POST['i3username']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soci3intervall=") !== false) {
			$result .= 'soci3intervall='.$_POST['soci3intervall']."\n";
		$writeit = '1';
		}
	if(strpos($line, "soci3intervall1=") !== false) {
			$result .= 'soci3intervall1='.$_POST['soci3intervall']."\n";
		$writeit = '1';
		}

			if(strpos($line, "i3passwort=") !== false) {
			$result .= 'i3passwort='.$_POST['i3passwort']."\n";
		$writeit = '1';
		}
			if(strpos($line, "i3vin=") !== false) {
			$result .= 'i3vin='.$_POST['i3vin']."\n";
		$writeit = '1';
		}
			if(strpos($line, "i3usernames1=") !== false) {
			$result .= 'i3usernames1='.$_POST['i3usernames1']."\n";
		$writeit = '1';
		}
			if(strpos($line, "i3passworts1=") !== false) {
			$result .= 'i3passworts1='.$_POST['i3passworts1']."\n";
		$writeit = '1';
		}
			if(strpos($line, "i3vins1=") !== false) {
			$result .= 'i3vins1='.$_POST['i3vins1']."\n";
		$writeit = '1';
		}
			if(strpos($line, "zoeusername=") !== false) {
			$result .= 'zoeusername='.$_POST['zoeusername']."\n";
		$writeit = '1';
		}
			if(strpos($line, "zoepasswort=") !== false) {
			$result .= 'zoepasswort=\''.$_POST['zoepasswort']."'\n";
		$writeit = '1';
			}
			if(strpos($line, "zoelp2username=") !== false) {
			$result .= 'zoelp2username='.$_POST['zoelp2username']."\n";
		$writeit = '1';
		}
			if(strpos($line, "zoelp2passwort=") !== false) {
			$result .= 'zoelp2passwort=\''.$_POST['zoelp2passwort']."'\n";
		$writeit = '1';
		}
			if(strpos($line, "evnotifytoken=") !== false) {
			$result .= 'evnotifytoken='.$_POST['evnotifytoken']."\n";
		$writeit = '1';
		}
			if(strpos($line, "evnotifyakey=") !== false) {
			$result .= 'evnotifyakey='.$_POST['evnotifyakey']."\n";
		$writeit = '1';
			}

			if(strpos($line, "evnotifytokenlp2=") !== false) {
			$result .= 'evnotifytokenlp2='.$_POST['evnotifytokenlp2']."\n";
		$writeit = '1';
		}
			if(strpos($line, "evnotifyakeylp2=") !== false) {
			$result .= 'evnotifyakeylp2='.$_POST['evnotifyakeylp2']."\n";
		$writeit = '1';
		}

			if(strpos($line, "wrjsonurl=") !== false) {
			$result .= 'wrjsonurl=\''.$_POST['wrjsonurl']."'\n";
		$writeit = '1';
		}
			if(strpos($line, "wrjsonwatt=") !== false) {
			$result .= 'wrjsonwatt=\''.$_POST['wrjsonwatt']."'\n";
		$writeit = '1';
		}
			if(strpos($line, "wrjsonkwh=") !== false) {
			$result .= 'wrjsonkwh=\''.$_POST['wrjsonkwh']."'\n";
		$writeit = '1';
	}
			if(strpos($line, "hausbezugnone=") !== false) {
			$result .= 'hausbezugnone='.$_POST['hausbezugnone']."\n";
		$writeit = '1';
	}
			if(strpos($line, "mpm3pmpvsource=") !== false) {
			$result .= 'mpm3pmpvsource='.$_POST['mpm3pmpvsource']."\n";
		$writeit = '1';
	}
			if(strpos($line, "mpm3pmpvid=") !== false) {
			$result .= 'mpm3pmpvid='.$_POST['mpm3pmpvid']."\n";
		$writeit = '1';
	}
			if(strpos($line, "mpm3pmpvlanip=") !== false) {
			$result .= 'mpm3pmpvlanip='.$_POST['mpm3pmpvlanip']."\n";
		$writeit = '1';
		}
			if(strpos($line, "bezugjsonurl=") !== false) {
			$result .= 'bezugjsonurl=\''.$_POST['bezugjsonurl']."'\n";
		$writeit = '1';
		}
			if(strpos($line, "bezugjsonwatt=") !== false) {
			$result .= 'bezugjsonwatt=\''.$_POST['bezugjsonwatt']."'\n";
		$writeit = '1';
		}
			if(strpos($line, "bezugjsonkwh=") !== false) {
			$result .= 'bezugjsonkwh=\''.$_POST['bezugjsonkwh']."'\n";
		$writeit = '1';
		}
			if(strpos($line, "einspeisungjsonkwh=") !== false) {
			$result .= 'einspeisungjsonkwh=\''.$_POST['einspeisungjsonkwh']."'\n";
		$writeit = '1';
		}
			if(strpos($line, "bezug_solarlog_ip=") !== false) {
			$result .= 'bezug_solarlog_ip=\''.$_POST['bezug_solarlog_ip']."'\n";
		$writeit = '1';
			}
			if(strpos($line, "bezug_solarlog_speicherv=") !== false) {
			$result .= 'bezug_solarlog_speicherv='.$_POST['bezug_solarlog_speicherv']."\n";
		$writeit = '1';
		}
			if(strpos($line, "speicherleistung_http=") !== false) {
			$result .= 'speicherleistung_http=\''.$_POST['speicherleistung_http']."'\n";
		$writeit = '1';
		}
			if(strpos($line, "speicherikwh_http=") !== false) {
			$result .= 'speicherikwh_http=\''.$_POST['speicherikwh_http']."'\n";
			$writeit = '1';
		}
			if(strpos($line, "speicherekwh_http=") !== false) {
			$result .= 'speicherekwh_http=\''.$_POST['speicherekwh_http']."'\n";
		$writeit = '1';
	}
			if(strpos($line, "speichersoc_http=") !== false) {
			$result .= 'speichersoc_http=\''.$_POST['speichersoc_http']."'\n";
		$writeit = '1';
	}
			if(strpos($line, "speichermodul=") !== false) {
			$result .= 'speichermodul='.$_POST['speichermodul']."\n";
		$writeit = '1';
	}
			if(strpos($line, "ess_api_ver=") !== false) {
			$result .= 'ess_api_ver='.$_POST['ess_api_ver']."\n";
		$writeit = '1';
	}
			if(strpos($line, "soc_tesla_username=") !== false) {
			$result .= 'soc_tesla_username='.$_POST['teslasocuser']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_tesla_carnumber=") !== false) {
			$result .= 'soc_tesla_carnumber='.$_POST['teslasoccarnumber']."\n";
		$writeit = '1';
	}
			if(strpos($line, "soc_tesla_password=") !== false) {
			$result .= 'soc_tesla_password=\''.$_POST['teslasocpw']."'\n";
		$writeit = '1';
	}
			if(strpos($line, "soc_tesla_intervall=") !== false) {
			$result .= 'soc_tesla_intervall='.$_POST['teslasocintervall']."\n";
		$writeit = '1';
	}
			if(strpos($line, "soc_tesla_intervallladen=") !== false) {
			$result .= 'soc_tesla_intervallladen='.$_POST['teslasocintervallladen']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_teslalp2_username=") !== false) {
			$result .= 'soc_teslalp2_username='.$_POST['teslasoclp2user']."\n";
		$writeit = '1';
	}
			if(strpos($line, "soc_teslalp2_password=") !== false) {
			$result .= 'soc_teslalp2_password=\''.$_POST['teslasoclp2pw']."'\n";
		$writeit = '1';
	}
			if(strpos($line, "soc_teslalp2_intervall=") !== false) {
			$result .= 'soc_teslalp2_intervall='.$_POST['teslasoclp2intervall']."\n";
		$writeit = '1';
	}
			if(strpos($line, "soc_teslalp2_intervallladen=") !== false) {
			$result .= 'soc_teslalp2_intervallladen='.$_POST['teslasoclp2intervallladen']."\n";
		$writeit = '1';
	}

			if(strpos($line, "wrkostalpikoip=") !== false) {
				$result .= 'wrkostalpikoip='.$_POST['wrkostalpikoip']."\n";
			$writeit = '1';
	}
			if(strpos($line, "solaredgeip=") !== false) {
			$result .= 'solaredgeip=\''.$_POST['solaredgeip']."'\n";
		$writeit = '1';
			}
			if(strpos($line, "solaredgewr2ip=") !== false) {
			$result .= 'solaredgewr2ip=\''.$_POST['solaredgewr2ip']."'\n";
		$writeit = '1';
			}

			if(strpos($line, "solaredgespeicherip=") !== false) {
			$result .= 'solaredgespeicherip=\''.$_POST['solaredgespeicherip']."'\n";
		$writeit = '1';
			}
			if(strpos($line, "solaredgepvip=") !== false) {
			$result .= 'solaredgepvip=\''.$_POST['solaredgepvip']."'\n";
		$writeit = '1';
	}
			if(strpos($line, "solaredgepvslave1=") !== false) {
			$result .= 'solaredgepvslave1='.$_POST['solaredgepvslave1']."\n";
		$writeit = '1';
			}
			if(strpos($line, "solaredgepvslave2=") !== false) {
			$result .= 'solaredgepvslave2='.$_POST['solaredgepvslave2']."\n";
		$writeit = '1';
	}
			if(strpos($line, "solaredgepvslave3=") !== false) {
			$result .= 'solaredgepvslave3='.$_POST['solaredgepvslave3']."\n";
		$writeit = '1';
	}
			if(strpos($line, "lllaniplp2=") !== false) {
				$result .= 'lllaniplp2='.$_POST['lllaniplp2']."\n";
			$writeit = '1';
	}
			if(strpos($line, "sdm630lp2source=") !== false) {
				$result .= 'sdm630lp2source='.$_POST['sdm630lp2source']."\n";
			$writeit = '1';
	}
			if(strpos($line, "sdm120lp2source=") !== false) {
				$result .= 'sdm120lp2source='.$_POST['sdm120lp2source']."\n";
			$writeit = '1';
	}
			if(strpos($line, "sdm630lp3source=") !== false) {
				$result .= 'sdm630lp3source='.$_POST['sdm630lp3source']."\n";
			$writeit = '1';
	}
			if(strpos($line, "sdm120lp3source=") !== false) {
				$result .= 'sdm120lp3source='.$_POST['sdm120lp3source']."\n";
			$writeit = '1';
	}
			if(strpos($line, "lllaniplp3=") !== false) {
				$result .= 'lllaniplp3='.$_POST['lllaniplp3']."\n";
			$writeit = '1';
	}
			if(strpos($line, "wryoulessip=") !== false) {
				$result .= 'wryoulessip='.$_POST['wryoulessip']."\n";
			$writeit = '1';
	}
			if(strpos($line, "lp1name=") !== false) {
				$result .= 'lp1name=\''.$_POST['lp1name']."'\n";
			$writeit = '1';
	}
			if(strpos($line, "lp2name=") !== false) {
			$result .= 'lp2name=\''.$_POST['lp2name']."'\n";
			$writeit = '1';
	}
			if(strpos($line, "lp3name=") !== false) {
			$result .= 'lp3name=\''.$_POST['lp3name']."'\n";
			$writeit = '1';
			}
			if(strpos($line, "lp4name=") !== false) {
			$result .= 'lp4name=\''.$_POST['lp4name']."'\n";
			$writeit = '1';
	}
			if(strpos($line, "lp8name=") !== false) {
			$result .= 'lp8name=\''.$_POST['lp8name']."'\n";
			$writeit = '1';
	}
			if(strpos($line, "lp7name=") !== false) {
			$result .= 'lp7name=\''.$_POST['lp7name']."'\n";
			$writeit = '1';
	}
			if(strpos($line, "lp6name=") !== false) {
			$result .= 'lp6name=\''.$_POST['lp6name']."'\n";
			$writeit = '1';
	}
			if(strpos($line, "lp5name=") !== false) {
			$result .= 'lp5name=\''.$_POST['lp5name']."'\n";
			$writeit = '1';
	}
			if(strpos($line, "nrgkickiplp1=") !== false) {
				$result .= 'nrgkickiplp1='.$_POST['nrgkickiplp1']."\n";
			$writeit = '1';
			}
			if(strpos($line, "nrgkicktimeoutlp1=") !== false) {
				$result .= 'nrgkicktimeoutlp1='.$_POST['nrgkicktimeoutlp1']."\n";
			$writeit = '1';
	}
			if(strpos($line, "nrgkickmaclp1=") !== false) {
				$result .= 'nrgkickmaclp1='.$_POST['nrgkickmaclp1']."\n";
			$writeit = '1';
	}
			if(strpos($line, "nrgkickpwlp1=") !== false) {
				$result .= 'nrgkickpwlp1='.$_POST['nrgkickpwlp1']."\n";
			$writeit = '1';
	}
			if(strpos($line, "nrgkickiplp2=") !== false) {
				$result .= 'nrgkickiplp2='.$_POST['nrgkickiplp2']."\n";
			$writeit = '1';
			}
			if(strpos($line, "nrgkicktimeoutlp2=") !== false) {
				$result .= 'nrgkicktimeoutlp2='.$_POST['nrgkicktimeoutlp2']."\n";
			$writeit = '1';
	}
			if(strpos($line, "nrgkickmaclp2=") !== false) {
				$result .= 'nrgkickmaclp2='.$_POST['nrgkickmaclp2']."\n";
			$writeit = '1';
	}
			if(strpos($line, "nrgkickpwlp2=") !== false) {
				$result .= 'nrgkickpwlp2='.$_POST['nrgkickpwlp2']."\n";
			$writeit = '1';
	}
			if(strpos($line, "goeiplp1=") !== false) {
				$result .= 'goeiplp1='.$_POST['goeiplp1']."\n";
			$writeit = '1';
	}
			if(strpos($line, "goeiplp2=") !== false) {
				$result .= 'goeiplp2='.$_POST['goeiplp2']."\n";
			$writeit = '1';
	}
			if(strpos($line, "goeiplp3=") !== false) {
				$result .= 'goeiplp3='.$_POST['goeiplp3']."\n";
			$writeit = '1';
	}
			if(strpos($line, "goetimeoutlp1=") !== false) {
				$result .= 'goetimeoutlp1='.$_POST['goetimeoutlp1']."\n";
			$writeit = '1';
	}
			if(strpos($line, "goetimeoutlp2=") !== false) {
				$result .= 'goetimeoutlp2='.$_POST['goetimeoutlp2']."\n";
			$writeit = '1';
	}
			if(strpos($line, "goetimeoutlp3=") !== false) {
				$result .= 'goetimeoutlp3='.$_POST['goetimeoutlp3']."\n";
			$writeit = '1';
	}
			if(strpos($line, "smashmbezugid=") !== false) {
			$result .= 'smashmbezugid='.$_POST['smashmbezugid']."\n";
		$writeit = '1';
	}
			if(strpos($line, "wrfroniusip=") !== false) {
				$result .= 'wrfroniusip='.$_POST['wrfroniusip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "wrfronius2ip=") !== false) {
				$result .= 'wrfronius2ip='.$_POST['wrfronius2ip']."\n";
			$writeit = '1';
	}
			if(strpos($line, "mpm3pmspeicherpv=") !== false) {
				$result .= 'mpm3pmspeicherpv='.$_POST['mpm3pmspeicherpv']."\n";
			$writeit = '1';
	}
			if(strpos($line, "mpm3pmspeicherid=") !== false) {
				$result .= 'mpm3pmspeicherid='.$_POST['mpm3pmspeicherid']."\n";
			$writeit = '1';
	}
			if(strpos($line, "mpm3pmspeichersource=") !== false) {
				$result .= 'mpm3pmspeichersource='.$_POST['mpm3pmspeichersource']."\n";
			$writeit = '1';
	}
			if(strpos($line, "mpm3pmspeicherlanip=") !== false) {
				$result .= 'mpm3pmspeicherlanip='.$_POST['mpm3pmspeicherlanip']."\n";
			$writeit = '1';
	}
		if(strpos($line, "bezug_smartme_user=") !== false) {
			$result .= 'bezug_smartme_user=\''.$_POST['bezug_smartme_user']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "bezug_smartme_pass=") !== false) {
			$result .= 'bezug_smartme_pass=\''.$_POST['bezug_smartme_pass']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "bezug_smartme_url=") !== false) {
			$result .= 'bezug_smartme_url=\''.$_POST['bezug_smartme_url']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "carnetuser=") !== false) {
			$result .= 'carnetuser=\''.$_POST['carnetuser']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "carnetpass=") !== false) {
			$result .= 'carnetpass=\''.$_POST['carnetpass']."'\n";
			$writeit = '1';
			}
				if(strpos($line, "soccarnetintervall=") !== false) {
			$result .= 'soccarnetintervall='.$_POST['soccarnetintervall']."\n";
			$writeit = '1';
			}
		if(strpos($line, "carnetlp2user=") !== false) {
			$result .= 'carnetlp2user=\''.$_POST['carnetlp2user']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "carnetlp2pass=") !== false) {
			$result .= 'carnetlp2pass=\''.$_POST['carnetlp2pass']."'\n";
			$writeit = '1';
			}
				if(strpos($line, "soccarnetlp2intervall=") !== false) {
			$result .= 'soccarnetlp2intervall='.$_POST['soccarnetlp2intervall']."\n";
			$writeit = '1';
			}

		if(strpos($line, "bydhvuser=") !== false) {
			$result .= 'bydhvuser='.$_POST['bydhvuser']."\n";
			$writeit = '1';
			}
		if(strpos($line, "bydhvpass=") !== false) {
			$result .= 'bydhvpass='.$_POST['bydhvpass']."\n";
			$writeit = '1';
			}
		if(strpos($line, "bydhvip=") !== false) {
			$result .= 'bydhvip='.$_POST['bydhvip']."\n";
			$writeit = '1';
			}
		if(strpos($line, "wr_smartme_user=") !== false) {
			$result .= 'wr_smartme_user=\''.$_POST['wr_smartme_user']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "wr_smartme_pass=") !== false) {
			$result .= 'wr_smartme_pass=\''.$_POST['wr_smartme_pass']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "wr_smartme_url=") !== false) {
			$result .= 'wr_smartme_url=\''.$_POST['wr_smartme_url']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "wr_piko2_user=") !== false) {
			$result .= 'wr_piko2_user=\''.$_POST['wr_piko2_user']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "wr_piko2_pass=") !== false) {
			$result .= 'wr_piko2_pass=\''.$_POST['wr_piko2_pass']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "wr_piko2_url=") !== false) {
			$result .= 'wr_piko2_url=\''.$_POST['wr_piko2_url']."'\n";
			$writeit = '1';
			}
		if(strpos($line, "e3dcip=") !== false) {
			$result .= 'e3dcip='.$_POST['e3dcip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "e3dcextprod=") !== false) {
			$result .= 'e3dcextprod='.$_POST['e3dcextprod']."\n";
			$writeit = '1';
		}
		if(strpos($line, "e3dc2ip=") !== false) {
			$result .= 'e3dc2ip='.$_POST['e3dc2ip']."\n";
			$writeit = '1';
			}
		if(strpos($line, "speicherpwip=") !== false) {
			$result .= 'speicherpwip='.$_POST['speicherpwip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "vartaspeicherip=") !== false) {
			$result .= 'vartaspeicherip='.$_POST['vartaspeicherip']."\n";
			$writeit = '1';
			}
		if(strpos($line, "lgessv1ip=") !== false) {
			$result .= 'lgessv1ip='.$_POST['lgessv1ip']."\n";
			$writeit = '1';
			}
		if(strpos($line, "lgessv1pass=") !== false) {
			$result .= 'lgessv1pass='.$_POST['lgessv1pass']."\n";
			$writeit = '1';
			}
			if(strpos($line, "sunnyislandip=") !== false) {
			$result .= 'sunnyislandip='.$_POST['sunnyislandip']."\n";
			$writeit = '1';
			}
			if(strpos($line, "sbs25ip=") !== false) {
			$result .= 'sbs25ip='.$_POST['sbs25ip']."\n";
			$writeit = '1';
			}
		if(strpos($line, "tri9000ip=") !== false) {
			$result .= 'tri9000ip='.$_POST['tri9000ip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "wrsma2ip=") !== false) {
			$result .= 'wrsma2ip='.$_POST['wrsma2ip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "wrsma3ip=") !== false) {
			$result .= 'wrsma3ip='.$_POST['wrsma3ip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "wrsma4ip=") !== false) {
			$result .= 'wrsma4ip='.$_POST['wrsma4ip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "kostalplenticoreip=") !== false) {
			$result .= 'kostalplenticoreip='.$_POST['kostalplenticoreip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "kostalplenticoreip2=") !== false) {
			$result .= 'kostalplenticoreip2='.$_POST['kostalplenticoreip2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "name_wechselrichter1=") !== false) {
			$result .= 'name_wechselrichter1='.$_POST['name_wechselrichter1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "name_wechselrichter2=") !== false) {
			$result .= 'name_wechselrichter2='.$_POST['name_wechselrichter2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "kostalplenticorehaus=") !== false) {
			$result .= 'kostalplenticorehaus='.$_POST['kostalplenticorehaus']."\n";
			$writeit = '1';
		}
		if(strpos($line, "kostalplenticorebatt=") !== false) {
			$result .= 'kostalplenticorebatt='.$_POST['kostalplenticorebatt']."\n";
			$writeit = '1';
		}
		if(strpos($line, "mpm3pmevuhaus=") !== false) {
			$result .= 'mpm3pmevuhaus='.$_POST['mpm3pmevuhaus']."\n";
		$writeit = '1';
		}
			if(strpos($line, "evuglaettung=") !== false) {
			$result .= 'evuglaettung='.$_POST['evuglaettung']."\n";
		$writeit = '1';
		}
			if(strpos($line, "evuglaettungakt=") !== false) {
			$result .= 'evuglaettungakt='.$_POST['evuglaettungakt']."\n";
		$writeit = '1';
		}
			if(strpos($line, "froniusprimo=") !== false) {
			$result .= 'froniusprimo='.$_POST['froniusprimo']."\n";
		$writeit = '1';
		}
			if(strpos($line, "kebaiplp1=") !== false) {
			$result .= 'kebaiplp1='.$_POST['kebaiplp1']."\n";
		$writeit = '1';
		}
			if(strpos($line, "kebaiplp2=") !== false) {
			$result .= 'kebaiplp2='.$_POST['kebaiplp2']."\n";
		$writeit = '1';
		}
			if(strpos($line, "bezug_smartfox_ip=") !== false) {
			$result .= 'bezug_smartfox_ip='.$_POST['bezug_smartfox_ip']."\n";
		$writeit = '1';
		}
			if(strpos($line, "wr_sdm120id=") !== false) {
			$result .= 'wr_sdm120id='.$_POST['wr_sdm120id']."\n";
		$writeit = '1';
		}
			if(strpos($line, "wr_sdm120ip=") !== false) {
			$result .= 'wr_sdm120ip='.$_POST['wr_sdm120ip']."\n";
		$writeit = '1';
		}
			if(strpos($line, "sonnenecoip=") !== false) {
			$result .= 'sonnenecoip='.$_POST['sonnenecoip']."\n";
		$writeit = '1';
			}
			if(strpos($line, "sonnenecoalternativ=") !== false) {
			$result .= 'sonnenecoalternativ='.$_POST['sonnenecoalternativ']."\n";
		$writeit = '1';
		}
			if(strpos($line, "bezug_victronip=") !== false) {
			$result .= 'bezug_victronip='.$_POST['bezug_victronip']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_audi_username=") !== false) {
			$result .= 'soc_audi_username='.$_POST['soc_audi_username']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_audi_passwort=") !== false) {
			$result .= 'soc_audi_passwort='.$_POST['soc_audi_passwort']."\n";
		$writeit = '1';
			}
			if(strpos($line, "stopsocnotpluggedlp1=") !== false) {
			$result .= 'stopsocnotpluggedlp1='.$_POST['stopsocnotpluggedlp1']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_zerong_username=") !== false) {
			$result .= 'soc_zerong_username='.$_POST['soc_zerong_username']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_zerong_password=") !== false) {
			$result .= 'soc_zerong_password='.$_POST['soc_zerong_password']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_zerong_intervall=") !== false) {
			$result .= 'soc_zerong_intervall='.$_POST['soc_zerong_intervall']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_zerong_intervallladen=") !== false) {
			$result .= 'soc_zerong_intervallladen='.$_POST['soc_zerong_intervallladen']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_zeronglp2_username=") !== false) {
			$result .= 'soc_zeronglp2_username='.$_POST['soc_zeronglp2_username']."\n";
		$writeit = '1';
			}
			if(strpos($line, "soc_zeronglp2_password=") !== false) {
			$result .= 'soc_zeronglp2_password='.$_POST['soc_zeronglp2_password']."\n";
		$writeit = '1';
			}

			if(strpos($line, "soc_zeronglp2_intervall=") !== false) {
			$result .= 'soc_zeronglp2_intervall='.$_POST['soc_zeronglp2_intervall']."\n";
		$writeit = '1';
			}

		if(strpos($line, "soc_zeronglp2_intervallladen=") !== false) {
			$result .= 'soc_zeronglp2_intervallladen='.$_POST['soc_zeronglp2_intervallladen']."\n";
			$writeit = '1';
			}
		if(strpos($line, "twcmanagerlp1ip=") !== false) {
			$result .= 'twcmanagerlp1ip=\''.$_POST['twcmanagerlp1ip']."'\n";
			$writeit = '1';
		}
		if(strpos($line, "twcmanagerlp1phasen=") !== false) {
			$result .= 'twcmanagerlp1phasen='.$_POST['twcmanagerlp1phasen']."\n";
			$writeit = '1';
		}
		if(strpos($line, "alphaessip=") !== false) {
			$result .= 'alphaessip='.$_POST['alphaessip']."\n";
			$writeit = '1';
		}
		if(strpos($line, "solarview_hostname=") !== false) {
			$result .= 'solarview_hostname='.$_POST['solarview_hostname']."\n";
			$writeit = '1';
		}
		if(strpos($line, "solarview_port=") !== false) {
			$result .= 'solarview_port='.$_POST['solarview_port']."\n";
			$writeit = '1';
		}
		if(strpos($line, "discovergyuser=") !== false) {
			$result .= 'discovergyuser='.$_POST['discovergyuser']."\n";
			$writeit = '1';
		}
		if(strpos($line, "discovergypass=") !== false) {
			$result .= 'discovergypass='.$_POST['discovergypass']."\n";
			$writeit = '1';
		}
		if(strpos($line, "discovergyevuid=") !== false) {
			$result .= 'discovergyevuid='.$_POST['discovergyevuid']."\n";
			$writeit = '1';
		}
		if(strpos($line, "discovergypvid=") !== false) {
			$result .= 'discovergypvid='.$_POST['discovergypvid']."\n";
			$writeit = '1';
		}
		if(strpos($line, "ksemip=") !== false) {
                	$result .= 'ksemip='.$_POST[ksemip]."\n";
                	$writeit = '1';
        	}

		if ( $writeit == '0') {
			$result .= $line;
		}
	}
	file_put_contents('/var/www/html/openWB/openwb.conf', $result);

	$result = '';
	$lines = file('/var/www/html/openWB/web/files/smashm.conf');
	foreach($lines as $line) {
		if( (strpos($line, "serials=") !== false) and (strpos($line, "serials=") == 0) ) {
				$result .= 'serials='.$_POST['smashmbezugid']."\n";
		} else {
			$result .= $line;
		}
	}
	file_put_contents('/var/www/html/openWB/web/files/smashm.conf', $result);

	$i3soc = "/var/www/html/openWB/modules/soc_i3/auth.json";
	$i3soc = fopen($i3soc, 'w');
	fwrite($i3soc,"{".PHP_EOL.'"username": "'.$_POST['i3username'].'",'.PHP_EOL.'"password": "'.$_POST['i3passwort'].'",'.PHP_EOL.'"vehicle": "'.$_POST['i3vin'].'"'.PHP_EOL."}".PHP_EOL);
	$i3soc1 = "/var/www/html/openWB/modules/soc_i3s1/auth.json";
	$i3soc1 = fopen($i3soc1, 'w');
	fwrite($i3soc1,"{".PHP_EOL.'"username": "'.$_POST['i3usernames1'].'",'.PHP_EOL.'"password": "'.$_POST['i3passworts1'].'",'.PHP_EOL.'"vehicle": "'.$_POST['i3vins1'].'"'.PHP_EOL."}".PHP_EOL);

}
header("Location: ../index.php");
?>
