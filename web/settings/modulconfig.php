<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Einstellungen</title>
		<meta name="description" content="Control your charge" />
		<meta name="author" content="Michael Ortenstein" />
		<!-- Favicons (created with http://realfavicongenerator.net/)-->
		<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
		<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
		<link rel="icon" type="image/png" href="img/favicons/favicon-32x32.png" sizes="32x32">
		<link rel="icon" type="image/png" href="img/favicons/favicon-16x16.png" sizes="16x16">
		<link rel="manifest" href="manifest.json">
		<link rel="shortcut icon" href="img/favicons/favicon.ico">
		<meta name="msapplication-TileColor" content="#00a8ff">
		<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
		<meta name="theme-color" content="#ffffff">

		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
	</head>

	<body>

		<?php

			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach($lines as $line) {
				if(strpos($line, "soclp1_vin=") !== false) {
					list(, $soclp1_vinold) = explode("=", $line);
				}
				if(strpos($line, "pv2wattmodul=") !== false) {
					list(, $pv2wattmodulold) = explode("=", $line);
				}
				if(strpos($line, "pv2id=") !== false) {
					list(, $pv2idold) = explode("=", $line);
				}
				if(strpos($line, "pv1_ipa=") !== false) {
					list(, $pv1_ipaold) = explode("=", $line);
				}
				if(strpos($line, "speicher1_ip=") !== false) {
					list(, $speicher1_ipold) = explode("=", $line);
				}
				if(strpos($line, "bezug1_ip=") !== false) {
					list(, $bezug1_ipold) = explode("=", $line);
				}

				if(strpos($line, "pv2ip=") !== false) {
					list(, $pv2ipold) = explode("=", $line);
				}
				if(strpos($line, "pv2user=") !== false) {
					list(, $pv2userold) = explode("=", $line);
				}
				if(strpos($line, "pv2pass=") !== false) {
					list(, $pv2passold) = explode("=", $line);
				}

				if(strpos($line, "soc_bluelink_interval=") !== false) {
					list(, $soc_bluelink_intervalold) = explode("=", $line);
				}
				if(strpos($line, "soc_bluelink_email=") !== false) {
					list(, $soc_bluelink_emailold) = explode("=", $line);
				}
				if(strpos($line, "soc_bluelink_password=") !== false) {
					list(, $soc_bluelink_passwordold) = explode("=", $line);
				}
				if(strpos($line, "soc_bluelink_pin=") !== false) {
					list(, $soc_bluelink_pinold) = explode("=", $line);
				}
				if(strpos($line, "solarworld_emanagerip=") !== false) {
					list(, $solarworld_emanageripold) = explode("=", $line);
				}
				if(strpos($line, "femsip=") !== false) {
					list(, $femsipold) = explode("=", $line);
				}
				if(strpos($line, "wrsunwaysip=") !== false) {
					list(, $wrsunwaysipold) = explode("=", $line);
				}
				if(strpos($line, "wrsunwayspw=") !== false) {
					list(, $wrsunwayspwold) = explode("=", $line);
				}
				if(strpos($line, "pvkitversion=") !== false) {
					list(, $pvkitversionold) = explode("=", $line);
				}
				if(strpos($line, "evukitversion=") !== false) {
					list(, $evukitversionold) = explode("=", $line);
				}
				if(strpos($line, "myrenault_userlp2=") !== false) {
					list(, $myrenault_userlp2old) = explode("=", $line);
				}
				if(strpos($line, "myrenault_passlp2=") !== false) {
					list(, $myrenault_passlp2old) = explode("=", $line);
				}
				if(strpos($line, "myrenault_locationlp2=") !== false) {
					list(, $myrenault_locationlp2old) = explode("=", $line);
				}
				if(strpos($line, "myrenault_countrylp2=") !== false) {
					list(, $myrenault_countrylp2old) = explode("=", $line);
				}

				if(strpos($line, "myrenault_userlp1=") !== false) {
					list(, $myrenault_userlp1old) = explode("=", $line);
				}
				if(strpos($line, "myrenault_passlp1=") !== false) {
					list(, $myrenault_passlp1old) = explode("=", $line);
				}
				if(strpos($line, "myrenault_locationlp1=") !== false) {
					list(, $myrenault_locationlp1old) = explode("=", $line);
				}
				if(strpos($line, "myrenault_countrylp1=") !== false) {
					list(, $myrenault_countrylp1old) = explode("=", $line);
				}
				if(strpos($line, "wryoulessip=") !== false) {
					list(, $wryoulessipold) = explode("=", $line);
				}
				if(strpos($line, "lastmanagementlp4=") !== false) {
					list(, $lastmanagementlp4old) = explode("=", $line);
				}
				if(strpos($line, "lastmanagementlp5=") !== false) {
					list(, $lastmanagementlp5old) = explode("=", $line);
				}

				if(strpos($line, "lastmanagementlp5=") !== false) {
					list(, $lastmanagementlp5old) = explode("=", $line);
				}

				if(strpos($line, "lastmanagementlp6=") !== false) {
					list(, $lastmanagementlp6old) = explode("=", $line);
				}

				if(strpos($line, "lastmanagementlp7=") !== false) {
					list(, $lastmanagementlp7old) = explode("=", $line);
				}
				if(strpos($line, "lastmanagementlp8=") !== false) {
					list(, $lastmanagementlp8old) = explode("=", $line);
				}

				if(strpos($line, "stopsocnotpluggedlp1=") !== false) {
					list(, $stopsocnotpluggedlp1old) = explode("=", $line);
				}
				if(strpos($line, "evseiplp3=") !== false) {
					list(, $evseiplp3old) = explode("=", $line);
				}
				if(strpos($line, "evseidlp3=") !== false) {
					list(, $evseidlp3old) = explode("=", $line);
				}
				if(strpos($line, "mpmlp3id=") !== false) {
					list(, $mpmlp3idold) = explode("=", $line);
				}
				if(strpos($line, "mpmlp3ip=") !== false) {
					list(, $mpmlp3ipold) = explode("=", $line);
				}
				if(strpos($line, "evseiplp2=") !== false) {
					list(, $evseiplp2old) = explode("=", $line);
				}
				if(strpos($line, "evseidlp2=") !== false) {
					list(, $evseidlp2old) = explode("=", $line);
				}
				if(strpos($line, "mpmlp2id=") !== false) {
					list(, $mpmlp2idold) = explode("=", $line);
				}
				if(strpos($line, "mpmlp2ip=") !== false) {
					list(, $mpmlp2ipold) = explode("=", $line);
				}
				if(strpos($line, "evseiplp1=") !== false) {
					list(, $evseiplp1old) = explode("=", $line);
				}
				if(strpos($line, "evseidlp1=") !== false) {
					list(, $evseidlp1old) = explode("=", $line);
				}
				if(strpos($line, "mpmlp1id=") !== false) {
					list(, $mpmlp1idold) = explode("=", $line);
				}
				if(strpos($line, "mpmlp1ip=") !== false) {
					list(, $mpmlp1ipold) = explode("=", $line);
				}

				if(strpos($line, "evseiplp4=") !== false) {
					list(, $evseiplp4old) = explode("=", $line);
				}
				if(strpos($line, "evseidlp4=") !== false) {
					list(, $evseidlp4old) = explode("=", $line);
				}
				if(strpos($line, "mpmlp4id=") !== false) {
					list(, $mpmlp4idold) = explode("=", $line);
				}
				if(strpos($line, "mpmlp4ip=") !== false) {
					list(, $mpmlp4ipold) = explode("=", $line);
				}
				if(strpos($line, "evseiplp5=") !== false) {
					list(, $evseiplp5old) = explode("=", $line);
				}
				if(strpos($line, "evseidlp5=") !== false) {
					list(, $evseidlp5old) = explode("=", $line);
				}
				if(strpos($line, "mpmlp5id=") !== false) {
					list(, $mpmlp5idold) = explode("=", $line);
				}
				if(strpos($line, "mpmlp5ip=") !== false) {
					list(, $mpmlp5ipold) = explode("=", $line);
				}
				if(strpos($line, "evseiplp6=") !== false) {
					list(, $evseiplp6old) = explode("=", $line);
				}
				if(strpos($line, "evseidlp6=") !== false) {
					list(, $evseidlp6old) = explode("=", $line);
				}
				if(strpos($line, "mpmlp6id=") !== false) {
					list(, $mpmlp6idold) = explode("=", $line);
				}
				if(strpos($line, "mpmlp6ip=") !== false) {
					list(, $mpmlp6ipold) = explode("=", $line);
				}
				if(strpos($line, "evseiplp7=") !== false) {
					list(, $evseiplp7old) = explode("=", $line);
				}
				if(strpos($line, "evseidlp7=") !== false) {
					list(, $evseidlp7old) = explode("=", $line);
				}
				if(strpos($line, "mpmlp7id=") !== false) {
					list(, $mpmlp7idold) = explode("=", $line);
				}
				if(strpos($line, "mpmlp7ip=") !== false) {
					list(, $mpmlp7ipold) = explode("=", $line);
				}
				if(strpos($line, "evseiplp8=") !== false) {
					list(, $evseiplp8old) = explode("=", $line);
				}
				if(strpos($line, "evseidlp8=") !== false) {
					list(, $evseidlp8old) = explode("=", $line);
				}
				if(strpos($line, "mpmlp8id=") !== false) {
					list(, $mpmlp8idold) = explode("=", $line);
				}
				if(strpos($line, "mpmlp8ip=") !== false) {
					list(, $mpmlp8ipold) = explode("=", $line);
				}
				if(strpos($line, "discovergyuser=") !== false) {
					list(, $discovergyuserold) = explode("=", $line);
				}
				if(strpos($line, "discovergypass=") !== false) {
					list(, $discovergypassold) = explode("=", $line);
				}
				if(strpos($line, "discovergyevuid=") !== false) {
					list(, $discovergyevuidold) = explode("=", $line);
				}
				if(strpos($line, "discovergypvid=") !== false) {
					list(, $discovergypvidold) = explode("=", $line);
				}
				if(strpos($line, "ksemip=") !== false) {
                                        list(, $ksemipold) = explode("=", $line);
                                }

				if(strpos($line, "solarview_hostname=") !== false) {
					list(, $solarview_hostnameold) = explode("=", $line);
				}
				if(strpos($line, "solarview_port=") !== false) {
					list(, $solarview_portold) = explode("=", $line);
				}

				if(strpos($line, "soc_audi_username=") !== false) {
					list(, $soc_audi_usernameold) = explode("=", $line);
				}
				if(strpos($line, "soc_audi_passwort=") !== false) {
					list(, $soc_audi_passwortold) = explode("=", $line);
				}

				if(strpos($line, "soc_zerong_username=") !== false) {
					list(, $soc_zerong_usernameold) = explode("=", $line);
				}
				if(strpos($line, "soc_zerong_password=") !== false) {
					list(, $soc_zerong_passwordold) = explode("=", $line);
				}
				if(strpos($line, "soc_zerong_intervall=") !== false) {
					list(, $soc_zerong_intervallold) = explode("=", $line);
				}
				if(strpos($line, "soc_zerong_intervallladen=") !== false) {
					list(, $soc_zerong_intervallladenold) = explode("=", $line);
				}
				if(strpos($line, "soc_zeronglp2_username=") !== false) {
					list(, $soc_zeronglp2_usernameold) = explode("=", $line);
				}
				if(strpos($line, "soc_zeronglp2_password=") !== false) {
					list(, $soc_zeronglp2_passwordold) = explode("=", $line);
				}
				if(strpos($line, "soc_zeronglp2_intervall=") !== false) {
					list(, $soc_zeronglp2_intervallold) = explode("=", $line);
				}
				if(strpos($line, "soc_zeronglp2_intervallladen=") !== false) {
					list(, $soc_zeronglp2_intervallladenold) = explode("=", $line);
				}
				if(strpos($line, "bezug_victronip=") !== false) {
					list(, $bezug_victronipold) = explode("=", $line);
				}
				if(strpos($line, "sonnenecoip=") !== false) {
					list(, $sonnenecoipold) = explode("=", $line);
				}
				if(strpos($line, "sonnenecoalternativ=") !== false) {
					list(, $sonnenecoalternativold) = explode("=", $line);
				}
				if(strpos($line, "wr_sdm120id=") !== false) {
					list(, $wr_sdm120idold) = explode("=", $line);
				}
				if(strpos($line, "wr_sdm120ip=") !== false) {
					list(, $wr_sdm120ipold) = explode("=", $line);
				}
				if(strpos($line, "debug=") !== false) {
					list(, $debugold) = explode("=", $line);
				}

				if(strpos($line, "wakeupmyrenaultlp1=") !== false) {
					list(, $wakeupmyrenaultlp1old) = explode("=", $line);
				}
				if(strpos($line, "wakeupmyrenaultlp2=") !== false) {
					list(, $wakeupmyrenaultlp2old) = explode("=", $line);
				}
				if(strpos($line, "pvbezugeinspeisung=") !== false) {
					list(, $pvbezugeinspeisungold) = explode("=", $line);
				}
				if(strpos($line, "sofortll=") !== false) {
					list(, $sofortllold) = explode("=", $line);
				}
				if(strpos($line, "dspeed=") !== false) {
					list(, $dspeedold) = explode("=", $line);
				}

				if(strpos($line, "sdmids1=") !== false) {
					list(, $sdmids1old) = explode("=", $line);
				}
				if(strpos($line, "minimalampv=") !== false) {
					list(, $minimalampvold) = explode("=", $line);
				}
				if(strpos($line, "minimalapv=") !== false) {
					list(, $minimalapvold) = explode("=", $line);
				}
				if(strpos($line, "minimalstromstaerke=") !== false) {
					list(, $minimalstromstaerkeold) = explode("=", $line);
				}
				if(strpos($line, "maximalstromstaerke=") !== false) {
					list(, $maximalstromstaerkeold) = explode("=", $line);
				}
				if(strpos($line, "httpevseip=") !== false) {
					list(, $httpevseipold) = explode("=", $line);
				}
				if(strpos($line, "evsecon=") !== false) {
					list(, $evseconold) = explode("=", $line);
				}
				if(strpos($line, "twcmanagerlp1ip=") !== false) {
					list(, $twcmanagerlp1ipold) = explode("=", $line);
				}
				if(strpos($line, "twcmanagerlp1phasen=") !== false) {
					list(, $twcmanagerlp1phasenold) = explode("=", $line);
				}

				if(strpos($line, "dacregister=") !== false) {
					list(, $dacregisterold) = explode("=", $line);
				}
				if(strpos($line, "dacregisters2=") !== false) {
					list(, $dacregisters2old) = explode("=", $line);
				}

				if(strpos($line, "dacregisters1=") !== false) {
					list(, $dacregisters1old) = explode("=", $line);
				}
				if(strpos($line, "modbusevsesource=") !== false) {
					list(, $modbusevsesourceold) = explode("=", $line);
				}

				if(strpos($line, "modbusevseid=") !== false) {
					list(, $modbusevseidold) = explode("=", $line);
				}
				if(strpos($line, "modbusevselanip=") !== false) {
					list(, $modbusevselanipold) = explode("=", $line);
				}
				if(strpos($line, "evsesources1=") !== false) {
					list(, $evsesources1old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid1s1=") !== false) {
					list(, $sdm120modbusllid1s1old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid2s1=") !== false) {
					list(, $sdm120modbusllid2s1old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid3s1=") !== false) {
					list(, $sdm120modbusllid3s1old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid1s2=") !== false) {
					list(, $sdm120modbusllid1s2old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid2s2=") !== false) {
					list(, $sdm120modbusllid2s2old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid3s2=") !== false) {
					list(, $sdm120modbusllid3s2old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid1=") !== false) {
					list(, $sdm120modbusllid1old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid2=") !== false) {
					list(, $sdm120modbusllid2old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid3=") !== false) {
					list(, $sdm120modbusllid3old) = explode("=", $line);
				}
				if(strpos($line, "evseids1=") !== false) {
					list(, $evseids1old) = explode("=", $line);
				}
				if(strpos($line, "evseids2=") !== false) {
					list(, $evseids2old) = explode("=", $line);
				}

				if(strpos($line, "evselanips1=") !== false) {
					list(, $evselanips1old) = explode("=", $line);
				}
				if(strpos($line, "lastmanagement=") !== false) {
					list(, $lastmanagementold) = explode("=", $line);
				}
				if(strpos($line, "durchslp1=") !== false) {
					list(, $durchslp1old) = explode("=", $line);
				}
				if(strpos($line, "durchslp2=") !== false) {
					list(, $durchslp2old) = explode("=", $line);
				}
				if(strpos($line, "durchslp3=") !== false) {
					list(, $durchslp3old) = explode("=", $line);
				}
				if(strpos($line, "lastmanagements2=") !== false) {
					list(, $lastmanagements2old) = explode("=", $line);
				}
				if(strpos($line, "lastmmaxw=") !== false) {
					list(, $lastmmaxwold) = explode("=", $line);
				}

				if(strpos($line, "evsecons1=") !== false) {
					list(, $evsecons1old) = explode("=", $line);
				}

				if(strpos($line, "evsecons2=") !== false) {
					list(, $evsecons2old) = explode("=", $line);
				}
				if(strpos($line, "evsesources2=") !== false) {
					list(, $evsesources2old) = explode("=", $line);
				}
				if(strpos($line, "evseids1=") !== false) {
					list(, $evseids1old) = explode("=", $line);
				}
				if(strpos($line, "evselanips2=") !== false) {
					list(, $evselanips2old) = explode("=", $line);
				}
				if(strpos($line, "sdmids2=") !== false) {
					list(, $sdmids2old) = explode("=", $line);
				}
				if(strpos($line, "ladeleistungs2modul=") !== false) {
					list(, $ladeleistungs2modulold) = explode("=", $line);
				}
				if(strpos($line, "wattbezugmodul=") !== false) {
					list(, $wattbezugmodulold) = explode("=", $line);
				}

				if(strpos($line, "vzloggerip=") !== false) {
					list(, $vzloggeripold) = explode("=", $line);
				}
				if(strpos($line, "vzloggerline=") !== false) {
					list(, $vzloggerlineold) = explode("=", $line);
				}
				if(strpos($line, "vzloggerkwhline=") !== false) {
					list(, $vzloggerkwhlineold) = explode("=", $line);
				}
				if(strpos($line, "vzloggerekwhline=") !== false) {
					list(, $vzloggerekwhlineold) = explode("=", $line);
				}
				if(strpos($line, "vzloggerpvip=") !== false) {
					list(, $vzloggerpvipold) = explode("=", $line);
				}
				if(strpos($line, "vzloggerpvline=") !== false) {
					list(, $vzloggerpvlineold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbusbezugid=") !== false) {
					list(, $sdm630modbusbezugidold) = explode("=", $line);
				}

				if(strpos($line, "sdm630modbusbezuglanip=") !== false) {
					list(, $sdm630modbusbezuglanipold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbusbezugsource=") !== false) {
					list(, $sdm630modbusbezugsourceold) = explode("=", $line);
				}


				if(strpos($line, "pvwattmodul=") !== false) {
					list(, $pvwattmodulold) = explode("=", $line);
				}
				if(strpos($line, "wrfroniusip=") !== false) {
					list(, $wrfroniusipold) = explode("=", $line);
				}
				if(strpos($line, "wrfronius2ip=") !== false) {
					list(, $wrfronius2ipold) = explode("=", $line);
				}
				if(strpos($line, "wrkostalpikoip=") !== false) {
					list(, $wrkostalpikoipold) = explode("=", $line);
				}
				if(strpos($line, "ladeleistungmodul=") !== false) {
					list(, $ladeleistungmodulold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbusllid=") !== false) {
					list(, $sdm630modbusllidold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbusllsource=") !== false) {
					list(, $sdm630modbusllsourceold) = explode("=", $line);
				}
				if(strpos($line, "fsm63a3modbusllid=") !== false) {
					list(, $fsm63a3modbusllidold) = explode("=", $line);
				}
				if(strpos($line, "fsm63a3modbusllsource=") !== false) {
					list(, $fsm63a3modbusllsourceold) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllsource=") !== false) {
					list(, $sdm120modbusllsourceold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbuslllanip=") !== false) {
					list(, $sdm630modbuslllanipold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbuswrid=") !== false) {
					list(, $sdm630modbuswridold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbuswrsource=") !== false) {
					list(, $sdm630modbuswrsourceold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbuswrlanip=") !== false) {
					list(, $sdm630modbuswrlanipold) = explode("=", $line);
				}
				if(strpos($line, "socmodul=") !== false) {
					list(, $socmodulold) = explode("=", $line);
				}
				if(strpos($line, "hsocip=") !== false) {
					list(, $hsocipold) = explode("=", $line, 2);
				}
				if(strpos($line, "socmodul1=") !== false) {
					list(, $socmodul1old) = explode("=", $line);
				}
				if(strpos($line, "hsocip1=") !== false) {
					list(, $hsocip1old) = explode("=", $line);
				}
				if(strpos($line, "nachtladen=") !== false) {
					list(, $nachtladenold) = explode("=", $line);
				}
				if(strpos($line, "nachtll=") !== false) {
					list(, $nachtllold) = explode("=", $line);
				}
				if(strpos($line, "nachtladens1=") !== false) {
					list(, $nachtladens1old) = explode("=", $line);
				}
				if(strpos($line, "nachtlls1=") !== false) {
					list(, $nachtlls1old) = explode("=", $line);
				}
				if(strpos($line, "nachtsocs1=") !== false) {
					list(, $nachtsocs1old) = explode("=", $line);
				}
				if(strpos($line, "nachtsoc1s1=") !== false) {
					list(, $nachtsoc1s1old) = explode("=", $line);
				}
				if(strpos($line, "nachtladenabuhrs1=") !== false) {
					list(, $nachtladenabuhrs1old) = explode("=", $line);
				}
				if(strpos($line, "nachtladenbisuhrs1=") !== false) {
					list(, $nachtladenbisuhrs1old) = explode("=", $line);
				}
				if(strpos($line, "httpll_w_url=") !== false) {
					list(, $httpll_w_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "httpll_ip=") !== false) {
					list(, $httpll_ipold) = explode("=", $line, 2);
				}
				if(strpos($line, "httpll_kwh_url=") !== false) {
					list(, $httpll_kwh_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "httpll_a1_url=") !== false) {
					list(, $httpll_a1_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "httpll_a2_url=") !== false) {
					list(, $httpll_a2_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "httpll_a3_url=") !== false) {
					list(, $httpll_a3_urlold) = explode("=", $line, 2);
				}

				if(strpos($line, "wr_http_w_url=") !== false) {
					list(, $wr_http_w_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "wr_http_kwh_url=") !== false) {
					list(, $wr_http_kwh_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_http_w_url=") !== false) {
					list(, $bezug_http_w_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_http_l1_url=") !== false) {
					list(, $bezug_http_l1_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_http_l2_url=") !== false) {
					list(, $bezug_http_l2_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_http_l3_url=") !== false) {
					list(, $bezug_http_l3_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_http_ikwh_url=") !== false) {
					list(, $bezug_http_ikwh_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_http_ekwh_url=") !== false) {
					list(, $bezug_http_ekwh_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "nachtladenabuhr=") !== false) {
					list(, $nachtladenabuhrold) = explode("=", $line);
				}
				if(strpos($line, "nachtladenbisuhr=") !== false) {
					list(, $nachtladenbisuhrold) = explode("=", $line);
				}
				if(strpos($line, "nachtsoc=") !== false) {
					list(, $nachtsocold) = explode("=", $line);
				}
				if(strpos($line, "nachtsoc1=") !== false) {
					list(, $nachtsoc1old) = explode("=", $line);
				}
				if(strpos($line, "mindestuberschuss=") !== false) {
					list(, $mindestuberschussold) = explode("=", $line);
				}
				if(strpos($line, "abschaltuberschuss=") !== false) {
					list(, $abschaltuberschussold) = explode("=", $line);
				}
				if(strpos($line, "ladeleistungs1modul=") !== false) {
					list(, $ladeleistungs1modulold) = explode("=", $line);
				}
				if(strpos($line, "lastmaxap1=") !== false) {
					list(, $lastmaxap1old) = explode("=", $line);
				}
				if(strpos($line, "lastmaxap2=") !== false) {
					list(, $lastmaxap2old) = explode("=", $line);
				}
				if(strpos($line, "lastmaxap3=") !== false) {
					list(, $lastmaxap3old) = explode("=", $line);
				}
				if(strpos($line, "smaemdbezugid=") !== false) {
					list(, $smaemdbezugidold) = explode("=", $line);
				}
				if(strpos($line, "smaemdllid=") !== false) {
					list(, $smaemdllidold) = explode("=", $line);
				}
				if(strpos($line, "smaemdpvid=") !== false) {
					list(, $smaemdpvidold) = explode("=", $line);
				}
				if(strpos($line, "abschaltverzoegerung=") !== false) {
					list(, $abschaltverzoegerungold) = explode("=", $line);
				}

				if(strpos($line, "evsewifiiplp1=") !== false) {
					list(, $evsewifiiplp1old) = explode("=", $line);
				}
				if(strpos($line, "evsewifiiplp2=") !== false) {
					list(, $evsewifiiplp2old) = explode("=", $line);
				}
				if(strpos($line, "evsewifiiplp3=") !== false) {
					list(, $evsewifiiplp3old) = explode("=", $line);
				}

				if(strpos($line, "evsewifitimeoutlp1=") !== false) {
					list(, $evsewifitimeoutlp1old) = explode("=", $line);
				}

				if(strpos($line, "evsewifitimeoutlp2=") !== false) {
					list(, $evsewifitimeoutlp2old) = explode("=", $line);
				}

				if(strpos($line, "evsewifitimeoutlp3=") !== false) {
					list(, $evsewifitimeoutlp3old) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmllsource=") !== false) {
					list(, $mpm3pmllsourceold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmlls1source=") !== false) {
					list(, $mpm3pmlls1sourceold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmlls2source=") !== false) {
					list(, $mpm3pmlls2sourceold) = explode("=", $line);
				}

				if(strpos($line, "mpm3pmpvid=") !== false) {
					list(, $mpm3pmpvidold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmpvsource=") !== false) {
					list(, $mpm3pmpvsourceold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmpvlanip=") !== false) {
					list(, $mpm3pmpvlanipold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmllid=") !== false) {
					list(, $mpm3pmllidold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmlls1id=") !== false) {
					list(, $mpm3pmlls1idold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmlls2id=") !== false) {
					list(, $mpm3pmlls2idold) = explode("=", $line);
				}

				if(strpos($line, "mpm3pmevuid=") !== false) {
					list(, $mpm3pmevuidold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmevusource=") !== false) {
					list(, $mpm3pmevusourceold) = explode("=", $line);
				}
				if(strpos($line, "leafusername=") !== false) {
					list(, $leafusernameold) = explode("=", $line);
				}
				if(strpos($line, "leafpasswort=") !== false) {
					list(, $leafpasswortold) = explode("=", $line);
				}
				if(strpos($line, "leafusernames1=") !== false) {
					list(, $leafusernames1old) = explode("=", $line);
				}
				if(strpos($line, "leafpassworts1=") !== false) {
					list(, $leafpassworts1old) = explode("=", $line);
				}
				if(strpos($line, "i3passworts1=") !== false) {
					list(, $i3passworts1old) = explode("=", $line);
				}
				if(strpos($line, "i3passwort=") !== false) {
					list(, $i3passwortold) = explode("=", $line);
				}
				if(strpos($line, "soci3intervall=") !== false) {
					list(, $soci3intervallold) = explode("=", $line);
				}
				if(strpos($line, "soci3intervall1=") !== false) {
					list(, $soci3intervall1old) = explode("=", $line);
				}
				if(strpos($line, "i3username=") !== false) {
					list(, $i3usernameold) = explode("=", $line);
				}
				if(strpos($line, "i3usernames1=") !== false) {
					list(, $i3usernames1old) = explode("=", $line);
				}
				if(strpos($line, "i3vin=") !== false) {
					list(, $i3vinold) = explode("=", $line);
				}
				if(strpos($line, "i3vins1=") !== false) {
					list(, $i3vins1old) = explode("=", $line);
				}
				if(strpos($line, "zoeusername=") !== false) {
					list(, $zoeusernameold) = explode("=", $line);
				}
				if(strpos($line, "zoepasswort=") !== false) {
					list(, $zoepasswortold) = explode("=", $line);
				}
				if(strpos($line, "zoelp2username=") !== false) {
					list(, $zoelp2usernameold) = explode("=", $line);
				}
				if(strpos($line, "zoelp2passwort=") !== false) {
					list(, $zoelp2passwortold) = explode("=", $line);
				}
				if(strpos($line, "wakeupzoelp1=") !== false) {
					list(, $wakeupzoelp1old) = explode("=", $line);
				}
				if(strpos($line, "wakeupzoelp2=") !== false) {
					list(, $wakeupzoelp2old) = explode("=", $line);
				}

				if(strpos($line, "evnotifytoken=") !== false) {
					list(, $evnotifytokenold) = explode("=", $line);
				}
				if(strpos($line, "evnotifyakey=") !== false) {
					list(, $evnotifyakeyold) = explode("=", $line);
				}
				if(strpos($line, "evnotifytokenlp2=") !== false) {
					list(, $evnotifytokenlp2old) = explode("=", $line);
				}
				if(strpos($line, "evnotifyakeylp2=") !== false) {
					list(, $evnotifyakeylp2old) = explode("=", $line);
				}
				if(strpos($line, "wrjsonurl=") !== false) {
					list(, $wrjsonurlold) = explode("=", $line, 2);
				}
				if(strpos($line, "wrjsonwatt=") !== false) {
					list(, $wrjsonwattold) = explode("=", $line, 2);
				}
				if(strpos($line, "wrjsonkwh=") !== false) {
					list(, $wrjsonkwhold) = explode("=", $line, 2);
				}
				if(strpos($line, "hausbezugnone=") !== false) {
					list(, $hausbezugnoneold) = explode("=", $line);
				}
				if(strpos($line, "bezugjsonurl=") !== false) {
					list(, $bezugjsonurlold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezugjsonwatt=") !== false) {
					list(, $bezugjsonwattold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezugjsonkwh=") !== false) {
					list(, $bezugjsonkwhold) = explode("=", $line, 2);
				}
				if(strpos($line, "einspeisungjsonkwh=") !== false) {
					list(, $einspeisungjsonkwhold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_solarlog_speicherv=") !== false) {
					list(, $bezug_solarlog_speichervold) = explode("=", $line);
				}
				if(strpos($line, "bezug_solarlog_ip=") !== false) {
					list(, $bezug_solarlog_ipold) = explode("=", $line);
				}
				if(strpos($line, "speichermodul=") !== false) {
					list(, $speichermodulold) = explode("=", $line);
				}
				if(strpos($line, "speicherleistung_http=") !== false) {
					list(, $speicherleistung_httpold) = explode("=", $line, 2);
				}
				if(strpos($line, "speichersoc_http=") !== false) {
					list(, $speichersoc_httpold) = explode("=", $line, 2);
				}
				if(strpos($line, "soc_tesla_username=") !== false) {
					list(, $socteslausernameold) = explode("=", $line);
				}
				if(strpos($line, "soc_tesla_carnumber=") !== false) {
					list(, $socteslacarnumberold) = explode("=", $line);
				}
				if(strpos($line, "soc_tesla_password=") !== false) {
					list(, $socteslapwold) = explode("=", $line);
				}
				if(strpos($line, "soc_tesla_intervall=") !== false) {
					list(, $socteslaintervallold) = explode("=", $line);
				}
				if(strpos($line, "soc_tesla_intervallladen=") !== false) {
					list(, $socteslaintervallladenold) = explode("=", $line);
				}
				if(strpos($line, "soc_teslalp2_username=") !== false) {
					list(, $socteslalp2usernameold) = explode("=", $line);
				}
				if(strpos($line, "soc_teslalp2_carnumber=") !== false) {
					list(, $socteslalp2carnumberold) = explode("=", $line);
				}
				if(strpos($line, "soc_teslalp2_password=") !== false) {
					list(, $socteslalp2pwold) = explode("=", $line);
				}
				if(strpos($line, "soc_teslalp2_intervall=") !== false) {
					list(, $socteslalp2intervallold) = explode("=", $line);
				}
				if(strpos($line, "soc_teslalp2_intervallladen=") !== false) {
					list(, $socteslalp2intervallladenold) = explode("=", $line);
				}

				if(strpos($line, "wrkostalpikoip=") !== false) {
					list(, $wrkostalpikoipold) = explode("=", $line);
				}

				if(strpos($line, "solaredgepvip=") !== false) {
					list(, $solaredgepvipold) = explode("=", $line);
				}
				if(strpos($line, "solaredgepvslave1=") !== false) {
					list(, $solaredgeipslave1old) = explode("=", $line);
				}
				if(strpos($line, "solaredgepvslave2=") !== false) {
					list(, $solaredgeipslave2old) = explode("=", $line);
				}
				if(strpos($line, "solaredgepvslave3=") !== false) {
					list(, $solaredgeipslave3old) = explode("=", $line);
				}
				if(strpos($line, "solaredgeip=") !== false) {
					list(, $solaredgeipold) = explode("=", $line);
				}
				if(strpos($line, "solaredgewr2ip=") !== false) {
					list(, $solaredgewr2ipold) = explode("=", $line);
				}

				if(strpos($line, "solaredgespeicherip=") !== false) {
					list(, $solaredgespeicheripold) = explode("=", $line);
				}
				if(strpos($line, "vartaspeicherip=") !== false) {
					list(, $vartaspeicheripold) = explode("=", $line);
				}
				if(strpos($line, "lgessv1ip=") !== false) {
					list(, $lgessv1ipold) = explode("=", $line);
				}
				if(strpos($line, "lgessv1pass=") !== false) {
					list(, $lgessv1passold) = explode("=", $line);
				}
				if(strpos($line, "ess_api_ver=") !== false) {
					list(, $ess_api_ver_old) = explode("=", $line);
				}
				if(strpos($line, "lllaniplp2=") !== false) {
					list(, $lllaniplp2old) = explode("=", $line);
				}
				if(strpos($line, "sdm630lp2source=") !== false) {
					list(, $sdm630lp2sourceold) = explode("=", $line);
				}
				if(strpos($line, "sdm120lp2source=") !== false) {
					list(, $sdm120lp2sourceold) = explode("=", $line);
				}
				if(strpos($line, "sdm630lp3source=") !== false) {
					list(, $sdm630lp3sourceold) = explode("=", $line);
				}
				if(strpos($line, "sdm120lp3source=") !== false) {
					list(, $sdm120lp3sourceold) = explode("=", $line);
				}
				if(strpos($line, "lllaniplp3=") !== false) {
					list(, $lllaniplp3old) = explode("=", $line);
				}
				if(strpos($line, "lp1name=") !== false) {
					list(, $lp1nameold) = explode("=", $line);
				}
				if(strpos($line, "lp2name=") !== false) {
					list(, $lp2nameold) = explode("=", $line);
				}
				if(strpos($line, "lp3name=") !== false) {
					list(, $lp3nameold) = explode("=", $line);
				}
				if(strpos($line, "lp4name=") !== false) {
					list(, $lp4nameold) = explode("=", $line);
				}
				if(strpos($line, "lp5name=") !== false) {
					list(, $lp5nameold) = explode("=", $line);
				}
				if(strpos($line, "lp6name=") !== false) {
					list(, $lp6nameold) = explode("=", $line);
				}
				if(strpos($line, "lp7name=") !== false) {
					list(, $lp7nameold) = explode("=", $line);
				}
				if(strpos($line, "lp8name=") !== false) {
					list(, $lp8nameold) = explode("=", $line);
				}
				if(strpos($line, "goeiplp1=") !== false) {
					list(, $goeiplp1old) = explode("=", $line);
				}
				if(strpos($line, "kebaiplp1=") !== false) {
					list(, $kebaiplp1old) = explode("=", $line);
				}
				if(strpos($line, "kebaiplp2=") !== false) {
					list(, $kebaiplp2old) = explode("=", $line);
				}
				if(strpos($line, "goetimeoutlp1=") !== false) {
					list(, $goetimeoutlp1old) = explode("=", $line);
				}
				if(strpos($line, "goeiplp2=") !== false) {
					list(, $goeiplp2old) = explode("=", $line);
				}
				if(strpos($line, "goetimeoutlp2=") !== false) {
					list(, $goetimeoutlp2old) = explode("=", $line);
				}
				if(strpos($line, "goeiplp3=") !== false) {
					list(, $goeiplp3old) = explode("=", $line);
				}
				if(strpos($line, "goetimeoutlp3=") !== false) {
					list(, $goetimeoutlp3old) = explode("=", $line);
				}
				if(strpos($line, "smashmbezugid=") !== false) {
					list(, $smashmbezugidold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmspeicherpv=") !== false) {
					list(, $mpm3pmspeicherpvold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmspeicherid=") !== false) {
					list(, $mpm3pmspeicheridold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmspeicherlanip=") !== false) {
					list(, $mpm3pmspeicherlanipold) = explode("=", $line);
				}

				if(strpos($line, "mpm3pmspeichersource=") !== false) {
					list(, $mpm3pmspeichersourceold) = explode("=", $line);
				}
				if(strpos($line, "speicherekwh_http=") !== false) {
					list(, $speicherekwh_httpold) = explode("=", $line, 2);
				}
				if(strpos($line, "speicherikwh_http=") !== false) {
					list(, $speicherikwh_httpold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_smartme_user=") !== false) {
					list(, $bezug_smartme_userold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_smartme_pass=") !== false) {
					list(, $bezug_smartme_passold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_smartme_url=") !== false) {
					list(, $bezug_smartme_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "carnetuser=") !== false) {
					list(, $carnetuserold) = explode("=", $line);
				}
				if(strpos($line, "carnetpass=") !== false) {
					list(, $carnetpassold) = explode("=", $line);
				}
				if(strpos($line, "soccarnetintervall=") !== false) {
					list(, $soccarnetintervallold) = explode("=", $line);
				}
				if(strpos($line, "carnetlp2user=") !== false) {
					list(, $carnetlp2userold) = explode("=", $line);
				}
				if(strpos($line, "carnetlp2pass=") !== false) {
					list(, $carnetlp2passold) = explode("=", $line);
				}
				if(strpos($line, "soccarnetlp2intervall=") !== false) {
					list(, $soccarnetlp2intervallold) = explode("=", $line);
				}

				if(strpos($line, "bydhvuser=") !== false) {
					list(, $bydhvuserold) = explode("=", $line);
				}
				if(strpos($line, "bydhvpass=") !== false) {
					list(, $bydhvpassold) = explode("=", $line);
				}
				if(strpos($line, "bydhvip=") !== false) {
					list(, $bydhvipold) = explode("=", $line);
				}
				if(strpos($line, "wr_smartme_user=") !== false) {
					list(, $wr_smartme_userold) = explode("=", $line, 2);
				}
				if(strpos($line, "wr_smartme_pass=") !== false) {
					list(, $wr_smartme_passold) = explode("=", $line, 2);
				}
				if(strpos($line, "wr_smartme_url=") !== false) {
					list(, $wr_smartme_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "wr_piko2_user=") !== false) {
					list(, $wr_piko2_userold) = explode("=", $line, 2);
				}
				if(strpos($line, "wr_piko2_pass=") !== false) {
					list(, $wr_piko2_passold) = explode("=", $line, 2);
				}
				if(strpos($line, "wr_piko2_url=") !== false) {
					list(, $wr_piko2_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "e3dcip=") !== false) {
					list(, $e3dcipold) = explode("=", $line);
				}
				if(strpos($line, "e3dcextprod=") !== false) {
					list(, $e3dcextprodold) = explode("=", $line);
				}
				if(strpos($line, "e3dc2ip=") !== false) {
					list(, $e3dc2ipold) = explode("=", $line);
				}
				if(strpos($line, "speicherpwip=") !== false) {
					list(, $speicherpwipold) = explode("=", $line);
				}
				if(strpos($line, "sbs25ip=") !== false) {
					list(, $sbs25ipold) = explode("=", $line);
				}
				if(strpos($line, "tri9000ip=") !== false) {
					list(, $tri9000ipold) = explode("=", $line);
				}
				if(strpos($line, "bezug_smartfox_ip=") !== false) {
					list(, $bezug_smartfox_ipold) = explode("=", $line);
				}
				if(strpos($line, "wrsmawebbox=") !== false) {
					list(, $wrsmawebboxold) = explode("=", $line);
				}
				if(strpos($line, "wrsma2ip=") !== false) {
					list(, $wrsma2ipold) = explode("=", $line);
				}
				if(strpos($line, "wrsma3ip=") !== false) {
					list(, $wrsma3ipold) = explode("=", $line);
				}
				if(strpos($line, "wrsma4ip=") !== false) {
					list(, $wrsma4ipold) = explode("=", $line);
				}
				if(strpos($line, "kostalplenticoreip=") !== false) {
					list(, $kostalplenticoreipold) = explode("=", $line);
				}
				if(strpos($line, "kostalplenticoreip2=") !== false) {
					list(, $kostalplenticoreip2old) = explode("=", $line);
				}
				if(strpos($line, "name_wechselrichter1=") !== false) {
					list(, $name_wechselrichter1old) = explode("=", $line);
				}
				if(strpos($line, "name_wechselrichter2=") !== false) {
					list(, $name_wechselrichter2old) = explode("=", $line);
				}

				if(strpos($line, "mpm3pmevuhaus=") !== false) {
					list(, $mpm3pmevuhausold) = explode("=", $line);
				}
				if(strpos($line, "evuglaettung=") !== false) {
					list(, $evuglaettungold) = explode("=", $line);
				}
				if(strpos($line, "evuglaettungakt=") !== false) {
					list(, $evuglaettungaktold) = explode("=", $line);
				}
				if(strpos($line, "nrgkickiplp1=") !== false) {
					list(, $nrgkickiplp1old) = explode("=", $line);
				}
				if(strpos($line, "nrgkicktimeoutlp1=") !== false) {
					list(, $nrgkicktimeoutlp1old) = explode("=", $line);
				}
				if(strpos($line, "nrgkickmaclp1=") !== false) {
					list(, $nrgkickmaclp1old) = explode("=", $line);
				}
				if(strpos($line, "nrgkickpwlp1=") !== false) {
					list(, $nrgkickpwlp1old) = explode("=", $line);
				}
				if(strpos($line, "kostalplenticorehaus=") !== false) {
					list(, $kostalplenticorehausold) = explode("=", $line);
				}
				if(strpos($line, "kostalplenticorebatt=") !== false) {
					list(, $kostalplenticorebattold) = explode("=", $line);
				}
				if(strpos($line, "froniuserzeugung=") !== false) {
					list(, $froniuserzeugungold) = explode("=", $line);
				}
				if(strpos($line, "froniusprimo=") !== false) {
					list(, $froniusprimoold) = explode("=", $line);
				}
				if(strpos($line, "nrgkickiplp2=") !== false) {
					list(, $nrgkickiplp2old) = explode("=", $line);
				}
				if(strpos($line, "nrgkicktimeoutlp2=") !== false) {
					list(, $nrgkicktimeoutlp2old) = explode("=", $line);
				}
				if(strpos($line, "nrgkickmaclp2=") !== false) {
					list(, $nrgkickmaclp2old) = explode("=", $line);
				}
				if(strpos($line, "nrgkickpwlp2=") !== false) {
					list(, $nrgkickpwlp2old) = explode("=", $line);
				}
				if(strpos($line, "sunnyislandip=") !== false) {
					list(, $sunnyislandipold) = explode("=", $line);
				}
			}
			$twcmanagerlp1ipold = str_replace( "'", "", $twcmanagerlp1ipold);
			$bezug_http_l1_urlold = str_replace( "'", "", $bezug_http_l1_urlold);
			$bezug_http_l2_urlold = str_replace( "'", "", $bezug_http_l2_urlold);
			$bezug_http_l3_urlold = str_replace( "'", "", $bezug_http_l3_urlold);
			$bezug_http_w_urlold = str_replace( "'", "", $bezug_http_w_urlold);
			$bezug_http_ikwh_urlold = str_replace( "'", "", $bezug_http_ikwh_urlold);
			$bezug_http_ekwh_urlold = str_replace( "'", "", $bezug_http_ekwh_urlold);
			$wr_http_w_urlold = str_replace( "'", "", $wr_http_w_urlold);
			$wr_http_kwh_urlold = str_replace( "'", "", $wr_http_kwh_urlold);
			$httpll_kwh_urlold = str_replace( "'", "", $httpll_kwh_urlold);
			$httpll_w_urlold = str_replace( "'", "", $httpll_w_urlold);
			$httpll_a1_urlold = str_replace( "'", "", $httpll_a1_urlold);
			$httpll_a2_urlold = str_replace( "'", "", $httpll_a2_urlold);
			$httpll_a3_urlold = str_replace( "'", "", $httpll_a3_urlold);
			$hsocipold = str_replace( "'", "", $hsocipold);
			$wrjsonurlold = str_replace( "'", "", $wrjsonurlold);
			$wrjsonwattold = str_replace( "'", "", $wrjsonwattold);
			$wrjsonkwhold = str_replace( "'", "", $wrjsonkwhold);
			$bezugjsonurlold = str_replace( "'", "", $bezugjsonurlold);
			$bezugjsonwattold = str_replace( "'", "", $bezugjsonwattold);
			$bezugjsonkwhold = str_replace( "'", "", $bezugjsonkwhold);
			$einspeisungjsonkwhold = str_replace( "'", "", $einspeisungjsonkwhold);
			$bezug_solarlog_ipold = str_replace( "'", "", $bezug_solarlog_ipold);
			$speichersoc_httpold = str_replace( "'", "", $speichersoc_httpold);
			$speicherleistung_httpold = str_replace( "'", "", $speicherleistung_httpold);
			$speicherikwh_httpold = str_replace( "'", "", $speicherikwh_httpold);
			$speicherekwh_httpold = str_replace( "'", "", $speicherekwh_httpold);
			$bezug_smartme_userold = str_replace( "'", "", $bezug_smartme_userold);
			$bezug_smartme_passold = str_replace( "'", "", $bezug_smartme_passold);
			$bezug_smartme_urlold = str_replace( "'", "", $bezug_smartme_urlold);
			$carnetuserold = str_replace( "'", "", $carnetuserold);
			$carnetpassold = str_replace( "'", "", $carnetpassold);
			$wr_smartme_userold = str_replace( "'", "", $wr_smartme_userold);
			$wr_smartme_passold = str_replace( "'", "", $wr_smartme_passold);
			$wr_smartme_urlold = str_replace( "'", "", $wr_smartme_urlold);
			$socteslapwold = str_replace( "'", "", $socteslapwold);
			$socteslalp2pwold = str_replace( "'", "", $socteslalp2pwold);
			$carnetlp2userold = str_replace( "'", "", $carnetlp2userold);
			$carnetlp2passold = str_replace( "'", "", $carnetlp2passold);
			$wr_piko2_userold = str_replace( "'", "", $wr_piko2_userold);
			$wr_piko2_passold = str_replace( "'", "", $wr_piko2_passold);
			$wr_piko2_urlold = str_replace( "'", "", $wr_piko2_urlold);

			$solaredgepvipold = str_replace( "'", "", $solaredgepvipold);
			$solaredgeipold = str_replace( "'", "", $solaredgeipold);
			$solaredgewr2ipold = str_replace( "'", "", $solaredgewr2ipold);
			$solaredgespeicheripold = str_replace( "'", "", $solaredgespeicheripold);
			$lp1nameold = str_replace( "'", "", $lp1nameold);
			$lp2nameold = str_replace( "'", "", $lp2nameold);
			$lp3nameold = str_replace( "'", "", $lp3nameold);
			$lp4nameold = str_replace( "'", "", $lp4nameold);
			$lp5nameold = str_replace( "'", "", $lp5nameold);
			$lp6nameold = str_replace( "'", "", $lp6nameold);
			$lp7nameold = str_replace( "'", "", $lp7nameold);
			$lp8nameold = str_replace( "'", "", $lp8nameold);
			$zoepasswortold = str_replace( "'", "", $zoepasswortold);
			$zoelp2passwortold = str_replace( "'", "", $zoelp2passwortold);
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<div class="col-sm-12">
				<form action="./tools/savemodul.php" method="POST">
					<div class="row">
						<div class="col">
							<h1> Erster Ladepunkt </h1>
						</div>
					</div>
					<div class="row">
						<div class="col">
							<b><label for="lp1name">Name Ladepunkt 1:</label></b>
							<input type="text" name="lp1name" id="lp1name" value="<?php echo $lp1nameold ?>">
						</div>
					</div>
					<div class="row">
						<div class="col">
							<b><label for="evsecon">Anbindung Ladepunkt 1:</label></b>
							<select name="evsecon" id="evsecon">
								<option <?php if($evseconold == "modbusevse\n" && !($ladeleistungmodulold == "mpm3pmll\n" && $mpm3pmllsourceold == "/dev/ttyUSB0\n" && ($mpm3pmllidold == "5\n" || $mpm3pmllidold == "105\n"))) echo "selected" ?> value="modbusevse">Modbusevse</option>
								<option <?php if($evseconold == "dac\n") echo "selected" ?> value="dac">DAC</option>
								<option <?php if($evseconold == "simpleevsewifi\n") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
								<option <?php if($evseconold == "goe\n") echo "selected" ?> value="goe">Go-e</option>
								<option <?php if($evseconold == "nrgkick\n") echo "selected" ?> value="nrgkick">NRGKick + Connect</option>
								<option <?php if($evseconold == "masterethframer\n") echo "selected" ?> value="masterethframer">openWB Ladepunkt in Verbindung mit Standalone</option>
								<option <?php if($evseconold == "twcmanager\n") echo "selected" ?> value="twcmanager">Tesla TWC mit TWCManager</option>
								<option <?php if($evseconold == "keba\n") echo "selected" ?> value="keba">Keba</option>
								<option <?php if($evseconold == "modbusevse\n" && $ladeleistungmodulold == "mpm3pmll\n" && $mpm3pmllsourceold == "/dev/ttyUSB0\n" && $mpm3pmllidold == "5\n") echo "selected" ?> value="openwb12">openWB series1/2</option>
								<option <?php if($evseconold == "modbusevse\n" && $ladeleistungmodulold == "mpm3pmll\n" && $mpm3pmllsourceold == "/dev/ttyUSB0\n" && $mpm3pmllidold == "105\n") echo "selected" ?> value="openwb12mid">openWB series1/2 mit geeichtem Zähler</option>
								<option <?php if($evseconold == "modbusevse\n" && $ladeleistungmodulold == "mpm3pmll\n" && $mpm3pmllsourceold == "/dev/serial0\n" && $mpm3pmllidold == "105\n") echo "selected" ?> value="openwb12v2mid">openWB series1/2 mit geeichtem Zähler v2</option>
								<option <?php if($evseconold == "ipevse\n") echo "selected" ?> value="ipevse">openWB Satellit </option>
								<option <?php if($evseconold == "httpevse\n") echo "selected" ?> value="httpevse">HTTP</option>
							</select>
						</div>
					</div>
					<div id="evseconmastereth">
						<div class="row bg-success">
							Keine Konfiguration erforderlich.
						</div>
					</div>
					<div id="openwb12">
						<div class="row bg-success">
							Keine Konfiguration erforderlich.<br>
							Dies ist die richtige Option, sowohl für Bausatz als auch für fertige openWB series1 oder series2.
						</div>
					</div>
					<div id="openwb12mid">
						<div class="row bg-success">
							Keine Konfiguration erforderlich.<br>
							Dies ist die richtige Option, sowohl für Bausatz als auch für fertige openWB series1 oder series2 mit geeichtem Zähler.
						</div>
					</div>
					<div id="openwb12v2mid">
						<div class="row bg-success">
							Keine Konfiguration erforderlich.<br>
							Dies ist die richtige Option, für fertige openWB series2 mit geeichtem Zähler und Addon Platine ab Mai 2020 (Standard+).
						</div>
					</div>

					<div id="evsecondac">
						<div class="row bg-success">
							<b><label for="dacregister">Dacregister:</label></b>
							<input type="text" name="dacregister" id="dacregister" value="<?php echo $dacregisterold ?>"><br>
							Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP<br>
							Der benötigte Wert sollte <a href="../ramdisk/i2csearch">HIER</a> zu finden sein.<br>
							Alternativ rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"
						</div>
					</div>
					<div id="evseconswifi">
						<div class="row bg-info">
							<div class="col">
								<b><label for="evsewifiiplp1">Simple EVSE Wifi IP Adressee:</label></b>
								<input type="text" name="evsewifiiplp1" id="evsewifiiplp1" value="<?php echo $evsewifiiplp1old ?>">
							</div>
						</div>
						<div class="row bg-info">
							<div class="col">
								Gültige Werte IP Adresse im Format: 192.168.0.12
							</div>
						</div>
						<div class="row bg-info">
							<div class="col">
								<b><label for="evsewifitimeoutlp1">Simple EVSE Wifi Timeout:</label></b>
								<input type="text" name="evsewifitimeoutlp1" id="evsewifitimeoutlp1" value="<?php echo $evsewifitimeoutlp1old ?>">
							</div>
						</div>
						<div class="row bg-info">
							<div class="col">
								Gültige Werte Zahl. Gibt die Zeit in Sekunden an wie lange auf Antwort der Simple EVSE gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.<br>
								Zulange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die SimpleEVSE z.B. gerade unterwegs genutzt wird.
							</div>
						</div>
					</div>
					<div id="evseconmod">
						<div class="row bg-info">
							<b><label for="modbusevsesource">EVSE Source:</label></b>
							<input type="text" name="modbusevsesource" id="modbusevsesource" value="<?php echo $modbusevsesourceold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.
						</div>
						<div class="row bg-info">
							<b><label for="modbusevseid">EVSE ID:</label></b>
							<input type="text" name="modbusevseid" id="modbusevseid" value="<?php echo $modbusevseidold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID der EVSE.
						</div>
						<div class="row bg-info">
							<b><label for="modbusevselanip">RS485/Lan-Konverter IP:</label></b>
							<input type="text" name="modbusevselanip" id="modbusevselanip" value="<?php echo $modbusevselanipold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP. IP Adresse des Modbus/Lan Konverter. Vermutlich gleich der IP des SDM Zählers in der WB.
						</div>
					</div>
					<div id="evseconipevse">
						<div class="row bg-info">
							<b><label for="evseiplp1">IP Adresse:</label></b>
							<input type="text" name="evseiplp1" id="evseiplp1" value="<?php echo $evseiplp1old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP. Aufgedruckt auf dem Label der openWB.
						</div>
						<div class="row bg-info">
							<b><label for="evseidlp1">EVSE ID:</label></b>
							<input type="text" name="evseidlp1" id="evseidlp1" value="<?php echo $evseidlp1old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Aufgedruckt auf dem Label der openWB.
						</div>
					</div>
					<div id="evseconkeba">
						<div class="row bg-info">
							<b><label for="kebaiplp1">Keba IP Adresse:</label></b>
							<input type="text" name="kebaiplp1" id="kebaiplp1" value="<?php echo $kebaiplp1old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse im Format: 192.168.0.12<br>
							Erforder eine Keba C- oder X- Series. Die Smart Home Funktion (UDP Schnittstelle) muss per DIP Switch in der Keba aktiviert sein!
						</div>
					</div>
					<div id="evseconhttp">
						<div class="row bg-info">
							<b><label for="httpevseip">IP Adresse:</label></b>
							<input type="text" name="httpevseip" id="httpevseip" value="<?php echo $httpevseipold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse im Format: 192.168.0.12<br>
							Der Ampere sollwert wird an http://$IP/setcurrent?current=$WERT gesendet.<br>
							Für eine korrekte Funktion ist als Ladeleistungsmodul HTTP zu wählen.<br>
							WERT kann sein: 0 = keine Ladung erlaubt, 6-32 = x Ampere erlaubt.
						</div>
					</div>

					<div id="evsecontwcmanager">
						<div class="row bg-info">
							<b><label for="twcmanagerlp1ip">TWCManager IP Adresse:</label></b>
							<input type="text" name="twcmanagerlp1ip" id="twcmanagerlp1ip" value="<?php echo $twcmanagerlp1ipold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse im Format: 192.168.0.12
						</div>
						<div class="row bg-info">
							<b><label for="twcmanagerlp1phasen">TWCManager Anzahl Phasen:</label></b>
							<input type="text" name="twcmanagerlp1phasen" id="twcmanagerlp1phasen" value="<?php echo $twcmanagerlp1phasenold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte Zahl. Definiert die genutzte Anzahl der Phasen zur korrekten Errechnung der Ladeleistung (BETA)
						</div>
					</div>
					<div id="evsecongoe">
						<div class="row bg-info">
							<b><label for="goeiplp1">Go-e IP Adresse:</label></b>
							<input type="text" name="goeiplp1" id="goeiplp1" value="<?php echo $goeiplp1old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse im Format: 192.168.0.12
						</div>
						<div class="row bg-info">
							<b><label for="goetimeoutlp1">Go-e Timeout:</label></b>
							<input type="text" name="goetimeoutlp1" id="goetimeoutlp1" value="<?php echo $goetimeoutlp1old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte Zahl. Gibt die Zeit in Sekunden an wie lange auf Antwort des Go-echargers gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.<br>
							Eine zu große Wartezeit zieht einen Verzug der Regellogik von openWB mit sich, wenn der Go-echarger z.B. gerade unterwegs genutzt wird.
						</div>
					</div>
					<div id="evseconnrgkick">
						<div class="row bg-info">
							<b><label for="nrgkickiplp1">NRGKick IP Adresse:</label></b>
							<input type="text" name="nrgkickiplp1" id="nrgkickiplp1" value="<?php echo $nrgkickiplp1old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse im Format: 192.168.0.12 Zu finden in der NRGKick App unter Einstellungen -> Info -> NRGkick Connect Infos.
						</div>
						<div class="row bg-info">
							<b><label for="nrgkicktimeoutlp1">NRGKick Timeout:</label></b>
							<input type="text" name="nrgkicktimeoutlp1" id="nrgkicktimeoutlp1" value="<?php echo $nrgkicktimeoutlp1old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte Zahl. Gibt die Zeit in Sekunden an wie lange auf Antwort des NRGKick Connect gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.<br>
							Zulange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die Go-e z.B. gerade unterwegs genutzt wird.
						</div>
						<div class="row bg-info">
							<b><label for="nrgkickmaclp1">NRGKick MAC Adresse:</label></b>
							<input type="text" name="nrgkickmaclp1" id="nrgkickmaclp1" value="<?php echo $nrgkickmaclp1old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte MAC Adresse im Format: 11:22:33:AA:BB:CC. Zu finden In der NRGKick App unter Einstellungen -> BLE-Mac.
						</div>
						<div class="row bg-info">
							<b><label for="nrgkickpwlp1">NRGKick PW:</label></b>
							<input type="text" name="nrgkickpwlp1" id="nrgkickpwlp1" value="<?php echo $nrgkickpwlp1old ?>">
						</div>
						<div class="row bg-info">
							Password welches in der NRGKick App festgelegt wurde.
						</div>
					</div>

					<script>
						function display_lp1() {
							$('#evsecondac').hide();
							$('#evseconmod').hide();
							$('#evseconswifi').hide();
							$('#llmodullp1').hide();
							$('#evsecongoe').hide();
							$('#evseconnrgkick').hide();
							$('#evseconmastereth').hide();
							$('#evseconkeba').hide();
							$('#openwb12').hide();
							$('#openwb12mid').hide();
							$('#openwb12v2mid').hide();
							$('#evseconhttp').hide();
							$('#evsecontwcmanager').hide();
							$('#evseconipevse').hide();
							if($('#evsecon').val() == 'ipevse') {
								$('#evseconipevse').show();
								$('#llmodullp1').show();
							}
							if($('#evsecon').val() == 'dac') {
								$('#evsecondac').show();
								$('#llmodullp1').show();
							}
							if($('#evsecon').val() == 'modbusevse') {
								$('#evseconmod').show();
								$('#llmodullp1').show();
							}
							if($('#evsecon').val() == 'simpleevsewifi') {
								$('#evseconswifi').show();
							}
							if($('#evsecon').val() == 'httpevse') {
								$('#evseconhttp').show();
								$('#llmodullp1').show();
							}

							if($('#evsecon').val() == 'goe') {
								$('#evsecongoe').show();
							}
							if($('#evsecon').val() == 'masterethframer') {
								$('#evseconmastereth').show();
							}
							if($('#evsecon').val() == 'nrgkick') {
								$('#evseconnrgkick').show();
							}
							if($('#evsecon').val() == 'keba') {
								$('#evseconkeba').show();
							}
							if($('#evsecon').val() == 'twcmanager') {
								$('#evsecontwcmanager').show();
							}
							if($('#evsecon').val() == 'openwb12') {
								$('#openwb12').show();
							}
							if($('#evsecon').val() == 'openwb12mid') {
								$('#openwb12mid').show();
							}
							if($('#evsecon').val() == 'openwb12v2mid') {
								$('#openwb12v2mid').show();
							}

							if($('#evsecon').val() == 'ipevse') {
								$('#evseconipevse').show();
							}
						}

						$(function() {
							display_lp1();
							$('#evsecon').change(function(){
								display_lp1();
							})
						});
					</script>

					<div id="llmodullp1">
						<div class="row">
							<b><label for="ladeleistungmodul">Ladeleistungmodul:</label></b>
							<select name="ladeleistungmodul" id="ladeleistungmodul">
								<option <?php if($ladeleistungmodulold == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
								<option <?php if($ladeleistungmodulold == "sdm630modbusll\n") echo "selected" ?> value="sdm630modbusll">SDM 630 Modbus</option>
								<option <?php if($ladeleistungmodulold == "smaemd_ll\n") echo "selected" ?> value="smaemd_ll">SMA Energy Meter</option>
								<option <?php if($ladeleistungmodulold == "sdm120modbusll\n") echo "selected" ?> value="sdm120modbusll">SDM 120 Modbus</option>
								<option <?php if($ladeleistungmodulold == "simpleevsewifi\n") echo "selected" ?> value="simpleevsewifi">Simple EVSE Wifi</option>
								<option <?php if($ladeleistungmodulold == "mpm3pmll\n") echo "selected" ?> value="mpm3pmll">MPM3PM</option>
								<option <?php if($ladeleistungmodulold == "fsm63a3modbusll\n") echo "selected" ?> value="fsm63a3modbusll">FSM63A3 Modbus</option>
								<option <?php if($ladeleistungmodulold == "httpll\n") echo "selected" ?> value="httpll">HTTP</option>
								<option <?php if($ladeleistungmodulold == "mpm3pmtripple\n") echo "selected" ?> value="mpm3pmtripple">openWB Tripple</option>
								<option <?php if($ladeleistungmodulold == "mpm3pmlllp1\n") echo "selected" ?> value="mpm3pmlllp1">openWB Satellit</option>
							</select>
						</div>
						<div id="mpm3pmlllp1div">
							<div class="row bg-info">
								<b><label for="mpmlp1ip">MPM3PM Modbus Ladeleistung IP:</label></b>
								<input type="text" name="mpmlp1ip" id="mpmlp1ip" value="<?php echo $mpmlp1ipold ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP Adresse des Modbus Ethernet Konverters.
							</div>
							<div class="row bg-info">
								<b><label for="mpmlp1id">MPM3PM Modbus Ladeleistung ID:</label></b>
								<input type="text" name="mpmlp1id" id="mpmlp1id" value="<?php echo $mpmlp1idold ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Modbus ID des MPM3PM.
							</div>
						</div>

						<div id="llmnone">
						</div>
						<div id="httpll">
							<div class="row bg-info" >
								<b><label for="httpll_w_url">Vollständige URL für die Ladeleistungs Watt</label></b>
								<input type="text" name="httpll_w_url" id="httpll_w_url" value="<?php echo htmlspecialchars($httpll_w_urlold) ?>">
							</div>
							<div class="row bg-info" >
								Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als wird der Wert auf null gesetzt. Der Wert muss in Watt sein.
							</div>
							<div class="row bg-info" >
								<b><label for="httpll_kwh_url">Vollständige URL für die Ladeleistungszählerstand in kWh</label></b>
								<input type="text" name="httpll_kwh_url" id="httpll_kwh_url" value="<?php echo htmlspecialchars($httpll_kwh_urlold) ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als wird der Wert auf null gesetzt. Der Wert muss in kWh sein als Trennstelle wird ein Punkt genutzt.
							</div>
							<div class="row bg-info" >
								<b><label for="httpll_a1_url">Vollständige URL für die Ladeleistungs Ampere Phase 1</label></b>
								<input type="text" name="httpll_a1_url" id="httpll_a1_url" value="<?php echo htmlspecialchars($httpll_a1_urlold) ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als wird der Wert auf null gesetzt. Der Wert muss in Ampere sein als Trennstelle wird ein Punkt genutzt.
							</div>
							<div class="row bg-info" >
								<b><label for="httpll_a2_url">Vollständige URL für die Ladeleistungs Ampere Phase 2</label></b>
								<input type="text" name="httpll_a2_url" id="httpll_a2_url" value="<?php echo htmlspecialchars($httpll_a2_urlold) ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als wird der Wert auf null gesetzt. Der Wert muss in Ampere sein als Trennstelle wird ein Punkt genutzt.
							</div>
							<div class="row bg-info" >
								<b><label for="httpll_a3_url">Vollständige URL für die Ladeleistungs Ampere Phase 3</label></b>
								<input type="text" name="httpll_a3_url" id="httpll_a3_url" value="<?php echo htmlspecialchars($httpll_a3_urlold) ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als wird der Wert auf null gesetzt. Der Wert muss in Ampere sein als Trennstelle wird ein Punkt genutzt.
							</div>
							<div class="row bg-info" >
								<b><label for="httpll_ip">IP Adresse für Plug/Charge Status</label></b>
								<input type="text" name="httpll_ip" id="httpll_ip" value="<?php echo htmlspecialchars($httpll_ipold) ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP. Abgerufene wird die Url http://$IP/plugstat und http://$IP/chargestat<br>
								Rückgabe ist jeweils 0 oder 1. Plugstat gibt an ob ein Stecker steckt, Chargestat gibt an ob EVSEseitig die Ladung aktiv ist
							</div>
						</div>
						<div id="llmpm3pm">
								<div class="row bg-info">
								<b><label for="mpm3pmllsource">MPM3PM Modbus Ladeleistung Source:</label></b>
								<input type="text" name="mpm3pmllsource" id="mpm3pmllsource" value="<?php echo $mpm3pmllsourceold ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
								Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
							</div>
							<div class="row bg-info">
								<b><label for="mpm3pmllid">MPM3PM Modbus Ladeleistung ID:</label></b>
								<input type="text" name="mpm3pmllid" id="mpm3pmllid" value="<?php echo $mpm3pmllidold ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Modbus ID des MPM3PM.
							</div>
						</div>
						<div id="llmfsm">
							<div class="row bg-info">
								<b><label for="fsm63a3modbusllsource">Zähler Source:</label></b>
								<input type="text" name="fsm63a3modbusllsource" id="fsm63a3modbusllsource" value="<?php echo $fsm63a3modbusllsourceold ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der fsm63a3 in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
								Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
							</div>
							<div class="row bg-info">
								<b><label for="fsm63a3modbusllid">Zähler ID:</label></b>
								<input type="text" name="fsm63a3modbusllid" id="fsm63a3modbusllid" value="<?php echo $fsm63a3modbusllidold ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Modbus ID des fsm63a3.
							</div>
						</div>
						<div id="llmsdm">
							<div class="row bg-info">
								<b><label for="sdm630modbusllsource">Zähler Source:</label></b>
								<input type="text" name="sdm630modbusllsource" id="sdm630modbusllsource" value="<?php echo $sdm630modbusllsourceold ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der SDM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
								Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
							</div>
							<div class="row bg-info">
								<b><label for="sdm630modbusllid">Zähler ID:</label></b>
								<input type="text" name="sdm630modbusllid" id="sdm630modbusllid" value="<?php echo $sdm630modbusllidold ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Modbus ID des SDM. Für SDM230 & SDM630v2.
							</div>
						</div>
						<div id="sdm120div">
							<div class="row bg-info">
								<b><label for="sdm120modbusllsource">Zähler Source:</label></b>
								<input type="text" name="sdm120modbusllsource" id="sdm120modbusllsource" value="<?php echo $sdm120modbusllsourceold ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der SDM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
								Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
							</div>

							<div class="row bg-info">
								<b><label for="sdm120modbusllid1">SDM 120 Zähler 1 ID:</label></b>
								<input type="text" name="sdm120modbusllid1" id="sdm120modbusllid1" value="<?php echo $sdm120modbusllid1old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Modbus ID des Ladepunkt 1 SDM Zählers in der WB.
							</div>
							<div class="row bg-info">
								<b><label for="sdm120modbusllid2">SDM 120 Zähler 2 ID:</label></b>
								<input type="text" name="sdm120modbusllid2" id="sdm120modbusllid2" value="<?php echo $sdm120modbusllid2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Modbus ID des Ladepunkt 1 SDM Zählers 2 in der WB.  Ist keine zweite Phase / SDM120 vorhanden bitte none eintragen.
							</div>
							<div class="row bg-info">
								<b><label for="sdm120modbusllid3">SDM 120 Zähler 3 ID:</label></b>
								<input type="text" name="sdm120modbusllid3" id="sdm120modbusllid3" value="<?php echo $sdm120modbusllid3old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Modbus ID des Ladepunkt 1 SDM Zählers 3 in der WB. Ist keine dritte Phase / SDM120 vorhanden bitte none eintragen.
							</div>
						</div>
						<div id="rs485lanlp1">
							<div class="row bg-info">
								<b><label for="sdm630modbuslllanip">RS485/Lan-Konverter IP:</label></b>
								<input type="text" name="sdm630modbuslllanip" id="sdm630modbuslllanip" value="<?php echo $sdm630modbuslllanipold ?>">
							</div>
							<div class="row bg-info">
								Ist nur von Belang, wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant.<br>
								Gültige Werte: IPs. Wenn ein LAN Konverter genutzt wird, muss die Source auf /dev/virtualcomx (z.B. /dev/virtualcom0) gesetzt werden.

							</div>
						</div>
						<div id="llswifi">
							<div class="row">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="llsma">
							<div class="row">
								<b><label for="smaemdllid">Seriennummer des SMA Energy Meter</label></b>
								<input type="text" name="smaemdllid" id="smaemdllid" value="<?php echo $smaemdllidold ?>">
							</div>
							<div class="row">
								Gültige Werte: Seriennummer. Hier die Seriennummer des SMA Meter für die Ladeleistung angeben<br>
								Infos zum SMA Energy Meter <a href="https://github.com/snaptec/openWB#extras">HIER</a>

							</div>
						</div>
					</div>

					<script>
						function display_llmp1() {
							$('#llmnone').hide();
							$('#llmsdm').hide();
							$('#llmpm3pm').hide();
							$('#llswifi').hide();
							$('#llsma, #sdm120div').hide();
							$('#rs485lanlp1').hide();
							$('#llmfsm').hide();
							$('#httpll').hide();
							$('#mpm3pmlllp1div').hide();


							if($('#ladeleistungmodul').val() == 'mpm3pmlllp1') {
								$('#mpm3pmlllp1div').show();
								$('#rs485lanlp1').hide();

							}
							if($('#ladeleistungmodul').val() == 'none') {
								$('#llmnone').show();
							}
							if($('#ladeleistungmodul').val() == 'mpm3pmtripple') {
								$('#llmnone').show();
							}

							if($('#ladeleistungmodul').val() == 'httpll') {
								$('#httpll').show();
							}

							if($('#ladeleistungmodul').val() == 'sdm630modbusll') {
								$('#llmsdm').show();
								$('#rs485lanlp1').show();
							}
							if($('#ladeleistungmodul').val() == 'smaemd_ll') {
								$('#llsma').show();
							}
							if($('#ladeleistungmodul').val() == 'sdm120modbusll') {
								$('#sdm120div').show();
								$('#rs485lanlp1').show();
							}
							if($('#ladeleistungmodul').val() == 'simpleevsewifi') {
								$('#llswifi').show();
							}
							if($('#ladeleistungmodul').val() == 'mpm3pmll') {
								$('#llmpm3pm').show();
								$('#rs485lanlp1').show();
							}
							if($('#ladeleistungmodul').val() == 'fsm63a3modbusll') {
								$('#rs485lanlp1').show();
								$('#llmfsm').show();
							}
						}

						$(function() {
							display_llmp1();
							$('#ladeleistungmodul').change(function(){
								display_llmp1();
							});
						});
					</script>

					<div class="row">
						<b><label for="socmodul">SOC Modul:</label></b>
						<select name="socmodul" id="socmodul">
							<option <?php if($socmodulold == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
							<option <?php if($socmodulold == "soc_http\n") echo "selected" ?> value="soc_http">SoC HTTP</option>
							<option <?php if($socmodulold == "soc_leaf\n") echo "selected" ?> value="soc_leaf">SoC Nissan Leaf</option>
							<option <?php if($socmodulold == "soc_i3\n") echo "selected" ?> value="soc_i3">SoC BMW i3</option>
							<option <?php if($socmodulold == "soc_zoe\n") echo "selected" ?> value="soc_zoe">SoC Renault Zoe alt</option>
							<option <?php if($socmodulold == "soc_myrenault\n") echo "selected" ?> value="soc_myrenault">SoC Renault Zoe MyRenault</option>
							<option <?php if($socmodulold == "soc_evnotify\n") echo "selected" ?> value="soc_evnotify">SoC EVNotify</option>
							<option <?php if($socmodulold == "soc_tesla\n") echo "selected" ?> value="soc_tesla">SoC Tesla</option>
							<option <?php if($socmodulold == "soc_carnet\n") echo "selected" ?> value="soc_carnet">SoC VW Carnet</option>
							<option <?php if($socmodulold == "soc_zerong\n") echo "selected" ?> value="soc_zerong">SoC Zero NG</option>
							<option <?php if($socmodulold == "soc_audi\n") echo "selected" ?> value="soc_audi">SoC Audi</option>
							<option <?php if($socmodulold == "soc_mqtt\n") echo "selected" ?> value="soc_mqtt">MQTT</option>
							<option <?php if($socmodulold == "soc_bluelink\n") echo "selected" ?> value="soc_bluelink">Hyundai Bluelink</option>
						</select>
					</div>
					<b><label for="stopsocnotpluggedlp1">SoC nur Abfragen wenn Auto angesteckt:</label></b>
					<select name="stopsocnotpluggedlp1" id="stopsocnotpluggedlp1">
						<option <?php if($stopsocnotpluggedlp1old == "0\n") echo "selected" ?> value="0">Nein</option>
						<option <?php if($stopsocnotpluggedlp1old == "1\n") echo "selected" ?> value="1">Ja</option>
					</select>
					<div class="row bg-info">
						Wenn Ja gewählt wird der SoC nur abgefragt während ein Auto angesteckt ist.<br>
						Bei Nein wird immer entsprechend der SoC Modul Konfiguration abgefragt.<br>
						Funktioniert nur wenn der "steckend" Status korrekt angezeigt wird.
					</div>
					<div id="socmqtt">
							<div class="row">Keine Konfiguration erforderlich</div>
							<div class="row">Per MQTT zu schreiben:</div>
							<div class="row"><b>"openWB/set/lp/1/%Soc"</b></div>
							<div class="row">Ladezustand in %, int, 0-100</div>
					</div>
					<div id="socmnone">
					</div>
					<div id="socmtesla">
						<div class="row bg-info">
						</div>
						<div class="row bg-info">
							<b><label for="teslasocuser">Tesla Benutzername:</label></b>
							<input type="text" name="teslasocuser" id="teslasocuser" value="<?php echo $socteslausernameold ?>">
						</div>
						<div class="row bg-info">
							Email Adresse des Tesla Logins
						</div>
						<div class="row bg-info">
							<b><label for="teslasocpw">Tesla Passwort:</label></b>
							<input type="password" name="teslasocpw" id="teslasocpw" value="<?php echo $socteslapwold ?>">
						</div>
						<div class="row bg-info">
							Password des Tesla Logins
						</div>
						<div class="row bg-info">
							<b><label for="teslasoccarnumber">Auto im Account:</label></b>
							<input type="text" name="teslasoccarnumber" id="teslasoccarnumber" value="<?php echo $socteslacarnumberold ?>">
						</div>
						<div class="row bg-info">
							Im Normalfall hier 0 eintragen. Sind mehrere Teslas im Account für den zweiten Tesla eine 1 eintragen.
						</div>
						<div class="row bg-info">
							<b><label for="teslasocintervall">Abfrageintervall Standby:</label></b>
							<input type="text" name="teslasocintervall" id="teslasocintervall" value="<?php echo $socteslaintervallold ?>">
						</div>
						<div class="row bg-info">
							Wie oft der Tesla abgefragt wird wenn nicht geladen wird. Angabe in Minuten.
						</div>
						<div class="row bg-info">
							<b><label for="teslasocintervallladen">Abfrageintervall Laden:</label></b>
							<input type="text" name="teslasocintervallladen" id="teslasocintervallladen" value="<?php echo $socteslaintervallladenold ?>">
						</div>
						<div class="row bg-info">
							Wie oft der Tesla abgefragt wird während geladen wird. Angabe in Minuten.
						</div>
					</div>
					<div id="socmbluelink">
						<div class="row bg-info">
						</div>
						<div class="row bg-info">
							<b><label for="soc_bluelink_email">Email Adresse:</label></b>
							<input type="text" name="soc_bluelink_email" id="soc_bluelink_email" value="<?php echo $soc_bluelink_emailold ?>">
						</div>
						<div class="row bg-info">
							Email Adresse des Hyundai Bluelink Logins
						</div>
						<div class="row bg-info">
							<b><label for="soc_bluelink_password">Passwort:</label></b>
							<input type="password" name="soc_bluelink_password" id="soc_bluelink_password" value="<?php echo $soc_bluelink_passwordold ?>">
						</div>
						<div class="row bg-info">
							Password des Logins
						</div>
						<div class="row bg-info">
							<b><label for="soc_bluelink_pin">PIN:</label></b>
							<input type="text" name="soc_bluelink_pin" id="soc_bluelink_pin" value="<?php echo $soc_bluelink_pinold ?>">
						</div>
						<div class="row bg-info">
							PIN des Accounts.
						</div>
						<div class="row bg-info">
							<b><label for="soc_bluelink_interval">Abfrageintervall:</label></b>
							<input type="text" name="soc_bluelink_interval" id="soc_bluelink_interval" value="<?php echo $soc_bluelink_intervalold ?>">
						</div>
						<div class="row bg-info">
							Wie oft abgefragt wird. Angabe in Minuten.
						</div>
					</div>

					<div id="socmzerong">
						<div class="row bg-info">
						</div>
						<div class="row bg-info">
							<b><label for="soc_zerong_username">Zero Benutzername:</label></b>
							<input type="text" name="soc_zerong_username" id="soc_zerong_username" value="<?php echo $soc_zerong_usernameold ?>">
						</div>
						<div class="row bg-info">
							Email Adresse des Zero Logins
						</div>
						<div class="row bg-info">
							<b><label for="soc_zerong_password">Zero Passwort:</label></b>
							<input type="password" name="soc_zerong_password" id="soc_zerong_password" value="<?php echo $soc_zerong_passwordold ?>">
						</div>
						<div class="row bg-info">
							Password des Zero Logins
						</div>

						<div class="row bg-info">
							<b><label for="soc_zerong_intervall">Abfrageintervall Standby:</label></b>
							<input type="text" name="soc_zerong_intervall" id="soc_zerong_intervall" value="<?php echo $soc_zerong_intervallold ?>">
						</div>
						<div class="row bg-info">
							Wie oft die Zero abgefragt wird wenn nicht geladen wird. Angabe in Minuten.
						</div>
						<div class="row bg-info">
							<b><label for="soc_zerong_intervallladen">Abfrageintervall Laden:</label></b>
							<input type="text" name="soc_zerong_intervallladen" id="soc_zerong_intervallladen" value="<?php echo $soc_zerong_intervallladenold ?>">
						</div>
						<div class="row bg-info">
							Wie oft die Zero abgefragt wird während geladen wird. Angabe in Minuten.
						</div>
					</div>
					<div id="socmaudi">
						<div class="row bg-info">
						</div>
						<div class="row bg-info">
							<b><label for="soc_audi_username">Audi Benutzername:</label></b>
							<input type="text" name="soc_audi_username" id="soc_audi_username" value="<?php echo $soc_audi_usernameold ?>">
						</div>
						<div class="row bg-info">
							Email Adresse des Audi Logins
						</div>
						<div class="row bg-info">
							<b><label for="soc_audi_passwort">Audi Passwort:</label></b>
							<input type="password" name="soc_audi_passwort" id="soc_audi_passwort" value="<?php echo $soc_audi_passwortold ?>">
						</div>
						<div class="row bg-info">
							Password des Audi Logins
						</div>
					</div>
					<div id="socmhttp">
						<div class="row bg-info">
						</div>
						<div class="row bg-info">
							<b><label for="hsocip">SOC Http Abfrage URL:</label></b>
							<input type="text" name="hsocip" id="hsocip" value="<?php echo htmlspecialchars($hsocipold) ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte none, "url". URL für die Abfrage des Soc, Antwort muss der reine Zahlenwert sein.
						</div>
					</div>
					<div id="soczoe">
						<div class="row bg-info">
							<b><label for="zoeusername">Benutzername:</label></b>
							<input type="text" name="zoeusername" id="zoeusername" value="<?php echo $zoeusernameold ?>">
						</div>
						<div class="row bg-info">
							Renault Zoe Benutzername
						</div>
						<div class="row bg-info">
							<b><label for="zoepasswort">Passwort:</label></b>
							<input type="password" name="zoepasswort" id="zoepasswort" value="<?php echo $zoepasswortold ?>">
						</div>
						<div class="row bg-info">
							Renault Zoe Passwort
						</div>
						<b><label for="wakeupzoelp1">Zoe Remote wecken wenn sie eingeschlafen ist:</label></b>
						<select name="wakeupzoelp1" id="wakeupzoelp1">
							<option <?php if($wakeupzoelp1old == "0\n") echo "selected" ?> value="0">Nein</option>
							<option <?php if($wakeupzoelp1old == "1\n") echo "selected" ?> value="1">Ja</option>
						</select>
						<div class="row bg-info">
							Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
						</div>
					</div>
					<div id="socmyrenault">
						<div class="row bg-info">
							<b><label for="myrenault_userlp1">Benutzername:</label></b>
							<input type="text" name="myrenault_userlp1" id="myrenault_userlp1" value="<?php echo $myrenault_userlp1old ?>">
						</div>
						<div class="row bg-info">
							MyRenault Benutzername
						</div>
						<div class="row bg-info">
							<b><label for="myrenault_passlp1">Passwort:</label></b>
							<input type="password" name="myrenault_passlp1" id="myrenault_passlp1" value="<?php echo $myrenault_passlp1old ?>">
						</div>
						<div class="row bg-info">
							MyRenault Passwort
						</div>
						<div class="row bg-info">
							<b><label for="myrenault_locationlp1">Standort:</label></b>
							<input type="text" name="myrenault_locationlp1" id="myrenault_locationlp1" value="<?php echo $myrenault_locationlp1old ?>">
						</div>
						<div class="row bg-info">
							MyRenault Standort, z.B. de_DE
						</div>
						<div class="row bg-info">
							<b><label for="myrenault_countrylp1">Land:</label></b>
							<input type="text" name="myrenault_countrylp1" id="myrenault_countrylp1" value="<?php echo $myrenault_countrylp1old ?>">
						</div>
						<div class="row bg-info">
							MyRenault Land, z.B. CH, AT, DE
						</div>
						<b><label for="wakeupmyrenaultlp1">Zoe Remote wecken wenn sie eingeschlafen ist:</label></b>
						<select name="wakeupmyrenaultlp1" id="wakeupmyrenaultlp1">
							<option <?php if($wakeupmyrenaultlp1old == "0\n") echo "selected" ?> value="0">Nein</option>
							<option <?php if($wakeupmyrenaultlp1old == "1\n") echo "selected" ?> value="1">Ja</option>
						</select>
						<div class="row bg-info">
							Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
						</div>
						<div class="row bg-info">
							<b><label for="soclp1_vin">VIN:</label></b>
							<input type="text" name="soclp1_vin" id="soclp1_vin" value="<?php echo $soclp1_vinold ?>">
						</div>
						<div class="row bg-info">
							VIN des Autos. Ist nur nötig wenn es sich um ein Importfahrzeug handelt. Kann auf none belassen werden wenn die Auslesung funktioniert.
						</div>
					</div>
					<div id="socevnotify">
						<div class="row bg-info">
							<b><label for="evnotifyakey">Akey:</label></b>
							<input type="text" name="evnotifyakey" id="evnotifyakey" value="<?php echo $evnotifyakeyold ?>">
						</div>
						<div class="row bg-info">
							Akey des EVNotify Kontos
						</div>
						<div class="row bg-info">
							<b><label for="evnotifytoken">Token:</label></b>
							<input type="text" name="evnotifytoken" id="evnotifytoken" value="<?php echo $evnotifytokenold ?>">
						</div>
						<div class="row bg-info">
							Token des Kontos
						</div>
					</div>
					<div id="socleaf">
						<div class="row bg-info">
							<b><label for="leafusername">Benutzername:</label></b>
							<input type="text" name="leafusername" id="leafusername" value="<?php echo $leafusernameold ?>">
						</div>
						<div class="row bg-info">
							Nissan Connect Benutzername
						</div>
						<div class="row bg-info">
							<b><label for="leafpasswort">Passwort:</label></b>
							<input type="password" name="leafpasswort" id="leafpasswort" value="<?php echo $leafpasswortold ?>">
						</div>
						<div class="row bg-info">
							Nissan Connect Passwort
						</div>
					</div>
					<div id="soci3">
						<div class="row bg-info">
							<b><label for="i3username">Benutzername:</label></b>
							<input type="text" name="i3username" id="i3username" value="<?php echo $i3usernameold ?>">
						</div>
						<div class="row bg-info">
							BMW Services Benutzername
						</div>
						<div class="row bg-info">
							<b><label for="i3passwort">Passwort:</label></b>
							<input type="password" name="i3passwort" id="i3passwort" value="<?php echo $i3passwortold ?>">
						</div>
						<div class="row bg-info">
							BMW Services Passwort
						</div>
						<div class="row bg-info">
							<b><label for="i3vin">VIN:</label></b>
							<input type="text" name="i3vin" id="i3vin" value="<?php echo $i3vinold ?>">
						</div>
						<div class="row bg-info">
							BMW i3 VIN. Sie ist in voller Länge anzugeben.
						</div>
						<div class="row bg-info">
							<b><label for="soci3intervall">Verkürztes Intervall beim Laden:</label></b>
							<input type="text" name="soci3intervall" id="soci3intervall" value="<?php echo $soci3intervallold ?>">
						</div>
						<div class="row bg-info">
							Verkürzt das Abfrageintervall beim Laden auf xx Minuten
						</div>
					</div>
					<div id="soccarnet">
						<div class="row bg-info">
							<b><label for="carnetuser">Benutzername:</label></b>
							<input type="text" name="carnetuser" id="carnetuser" value="<?php echo $carnetuserold ?>">
						</div>
						<div class="row bg-info">
							VW Carnet Benutzername. <br>
							Wenn der SoC nicht korrekt angezeigt wird, z.B. weil AGB von VW geändert wurden, ist es nötig sich auf https://www.portal.volkswagen-we.com anzumelden
						</div>
						<div class="row bg-info">
							<b><label for="carnetpass">Passwort:</label></b>
							<input type="password" name="carnetpass" id="carnetpass" value="<?php echo $carnetpassold ?>">
						</div>
						<div class="row bg-info">
							VW Carnet Passwort
						</div>
						<div class="row bg-info">
							<b><label for="soccarnetintervall">Verkürztes Intervall beim Laden:</label></b>
							<input type="text" name="soccarnetintervall" id="soccarnetintervall" value="<?php echo $soccarnetintervallold ?>">
						</div>
						<div class="row bg-info">
							Verkürzt das Abfrageintervall beim Laden auf xx Minuten
						</div>
					</div>

					<script>
						function display_socmodul() {
							$('#socmnone').hide();
							$('#socmhttp').hide();
							$('#socleaf').hide();
							$('#soci3').hide();
							$('#soczoe').hide();
							$('#socevnotify').hide();
							$('#socmtesla').hide();
							$('#soccarnet').hide();
							$('#socmzerong').hide();
							$('#socmaudi').hide();
							$('#socmqtt').hide();
							$('#socmbluelink').hide();

							$('#socmyrenault').hide();
							if($('#socmodul').val() == 'soc_mqtt') {
								$('#socmqtt').show();
							}
							if($('#socmodul').val() == 'soc_bluelink') {
								$('#socmbluelink').show();
							}

							if($('#socmodul').val() == 'soc_audi') {
								$('#socmaudi').show();
							}
							if($('#socmodul').val() == 'soc_myrenault') {
								$('#socmyrenault').show();
							}

							if($('#socmodul').val() == 'none') {
								$('#socmnone').show();
							}
							if($('#socmodul').val() == 'soc_http') {
								$('#socmhttp').show();
							}
							if($('#socmodul').val() == 'soc_zerong') {
								$('#socmzerong').show();
							}

							if($('#socmodul').val() == 'soc_leaf') {
								$('#socleaf').show();
							}
							if($('#socmodul').val() == 'soc_i3') {
								$('#soci3').show();
							}
							if($('#socmodul').val() == 'soc_zoe') {
								$('#soczoe').show();
							}
							if($('#socmodul').val() == 'soc_evnotify') {
								$('#socevnotify').show();
							}
							if($('#socmodul').val() == 'soc_tesla') {
								$('#socmtesla').show();
							}
							if($('#socmodul').val() == 'soc_carnet') {
								$('#soccarnet').show();
							}
						}

						$(function() {
							display_socmodul();
							$('#socmodul').change( function(){
								display_socmodul();
							});
						});
					</script>

					<hr>
					<div class="row">
						<h4>
							<b><label for="lastmanagement">Zweiter Ladepunkt:</label></b>
							<select name="lastmanagement" id="lastmanagement">
								<option <?php if($lastmanagementold == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($lastmanagementold == 1) echo "selected" ?> value="1">An</option>
							</select>
						</h4>
					</div>
					<div id="lastmmaus">
					</div>
					<div id="lastmman" style="margin:5em;">

						<div class="row">
						</div>
						<div class="row">
							<b><label for="lp2name">Name Ladepunkt 2:</label></b>
							<input type="text" name="lp2name" id="lp2name" value="<?php echo $lp2nameold ?>">
						</div>
						<div class="row">
							<b><label for="evsecons1">Anbindung der EVSE an Ladepunkt 2:</label></b>
							<select name="evsecons1" id="evsecons1">
								<option <?php if($evsecons1old == "slaveeth\n") echo "selected" ?> value="slaveeth">openWB Slave</option>
								<option <?php if($evsecons1old == "modbusevse\n" && !($ladeleistungs1modulold == "mpm3pmlls1\n" && $mpm3pmlls1sourceold == "/dev/ttyUSB1\n" && $mpm3pmlls1idold == "6\n")) echo "selected" ?> value="modbusevse">Modbus</option>
								<option <?php if($evsecons1old == "dac\n") echo "selected" ?> value="dac">DAC</option>
								<option <?php if($evsecons1old == "simpleevsewifi\n") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
								<option <?php if($evsecons1old == "goe\n") echo "selected" ?> value="goe">Go-e</option>
								<option <?php if($evsecons1old == "nrgkick\n") echo "selected" ?> value="nrgkick">NRGKick + Connect</option>
								<option <?php if($evsecons1old == "keba\n") echo "selected" ?> value="keba">Keba</option>
								<option <?php if($evsecons1old == "modbusevse\n" && $ladeleistungs1modulold == "mpm3pmlls1\n" && $mpm3pmlls1sourceold == "/dev/ttyUSB1\n" && $mpm3pmlls1idold == "6\n") echo "selected" ?> value="openwb12s1">openWB series1/2 Duo</option>
								<option <?php if($evsecons1old == "ipevse\n") echo "selected" ?> value="ipevse">openWB Satellit</option>
							</select>
						</div>
						<div id="evseconipevselp2">
							<div class="row bg-info">
								<b><label for="evseiplp2">IP Adresse:</label></b>
								<input type="text" name="evseiplp2" id="evseiplp2" value="<?php echo $evseiplp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP. Aufgedruckt auf dem Label der openWB.
							</div>
							<div class="row bg-info">
								<b><label for="evseidlp2">EVSE ID:</label></b>
								<input type="text" name="evseidlp2" id="evseidlp2" value="<?php echo $evseidlp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Aufgedruckt auf dem Label der openWB.
							</div>
						</div>
						<div id="openwb12s1">
							<div class="row bg-success">
								Keine Konfiguration erforderlich.
								Dies ist die richtige option sowohl für Bausatz als auch fertige openWB series1 oder series2.
							</div>
						</div>
						<div id="evseconnrgkicks1">
							<div class="row bg-info">
								<b><label for="nrgkickiplp2">NRGKick IP Adresse:</label></b>
								<input type="text" name="nrgkickiplp2" id="nrgkickiplp2" value="<?php echo $nrgkickiplp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP Adresse im Format: 192.168.0.12 Zu finden in der NRGKick App unter Einstellungen -> Info -> NRGkick Connect Infos.
							</div>
							<div class="row bg-info">
								<b><label for="nrgkicktimeoutlp2">NRGKick Timeout:</label></b>
								<input type="text" name="nrgkicktimeoutlp2" id="nrgkicktimeoutlp2" value="<?php echo $nrgkicktimeoutlp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte Zahl. Gibt die Zeit in Sekunden an wie lange auf Antwort des NRGKick Connect gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.<br>
								Zulange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die Go-e z.B. gerade unterwegs genutzt wird.
							</div>
							<div class="row bg-info">
								<b><label for="nrgkickmaclp2">NRGKick MAC Adresse:</label></b>
								<input type="text" name="nrgkickmaclp2" id="nrgkickmaclp2" value="<?php echo $nrgkickmaclp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte MAC Adresse im Format: 11:22:33:AA:BB:CC. Zu finden In der NRGKick App unter Einstellungen -> BLE-Mac.
							</div>
							<div class="row bg-info">
								<b><label for="nrgkickpwlp2">NRGKick PW:</label></b>
								<input type="text" name="nrgkickpwlp2" id="nrgkickpwlp2" value="<?php echo $nrgkickpwlp2old ?>">
							</div>
							<div class="row bg-info">
								Password welches in der NRGKick App festgelegt wurde.
							</div>
						</div>
						<div id="evseconkebas1">
							<div class="row bg-info">
								<b><label for="kebaiplp2">Keba IP Adresse:</label></b>
								<input type="text" name="kebaiplp2" id="kebaiplp2" value="<?php echo $kebaiplp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP Adresse im Format: 192.168.0.12<br>
								Erforder eine Keba C- oder X- Series. Die Smart Home Funktion (UDP Schnittstelle) muss per DIP Switch in der Keba aktiviert sein!
							</div>
						</div>
						<div id="evseconmbs1">
							<div class="row">
								Modbus für EVSE DIN. Auf der EVSE muss Register 2003 auf 1 gesetzt werden (Deaktivierung analog Eingang), sonst kein beschreiben möglich
							</div>
							<div class="row bg-info">
								<b><label for="evsesources1">EVSE Source:</label></b>
								<input type="text" name="evsesources1" id="evsesources1" value="<?php echo $evsesources1old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.<br>
								Ist nur von belang wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant
							</div>
							<div class="row bg-info">
								<b><label for="evseids1">EVSE ID:</label></b>
								<input type="text" name="evseids1" id="evseids1" value="<?php echo $evseids1old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Modbus ID der Slave 1 EVSE.
							</div>
							<div class="row bg-info">
								<b><label for="evselanips1">RS485/Lan-Konverter IP:</label></b>
								<input type="text" name="evselanips1" id="evselanips1" value="<?php echo $evselanips1old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt, ansonsten ist diese Option irrelevant.
							</div>
						</div>
						<div id="evsecondacs1">
							<div class="row bg-success">
								<b><label for="dacregisters1">Dacregister:</label></b>
								<input type="text" name="dacregisters1" id="dacregisters1" value="<?php echo $dacregisters1old ?>">
							</div>
							<div class="row bg-success">
								Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP<br>
								Rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1". Muss sich bei Nutzung von zweimal DAC zum ersten unterscheiden!
							</div>
						</div>
						<div id="evsecoslaveeth">
							<div class="row bg-success">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="evseconswifis1">
							<div class="row bg-info">
								<b><label for="evsewifiiplp2">Simple EVSE Wifi IP Adressee:</label></b>
								<input type="text" name="evsewifiiplp2" id="evsewifiiplp2" value="<?php echo $evsewifiiplp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP Adresse im Format: 192.168.0.12
							</div>
							<div class="row bg-info">
								<b><label for="evsewifitimeoutlp2">Simple EVSE Wifi Timeout:</label></b>
								<input type="text" name="evsewifitimeoutlp2" id="evsewifitimeoutlp2" value="<?php echo $evsewifitimeoutlp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte Zahl. Gibt die Zeit in Sekunden an wie lange auf Antwort der Simple EVSE gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.<br>
								Zulange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die SimpleEVSE z.B. gerade unterwegs genutzt wird.
							</div>
						</div>
						<div id="evsecongoes1">
							<div class="row bg-info">
								<b><label for="goeiplp2">Go-e IP Adressee:</label></b>
								<input type="text" name="goeiplp2" id="goeiplp2" value="<?php echo $goeiplp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP Adresse im Format: 192.168.0.12
							</div>
							<div class="row bg-info">
								<b><label for="goetimeoutlp2">Go-e Timeout:</label></b>
								<input type="text" name="goetimeoutlp2" id="goetimeoutlp2" value="<?php echo $goetimeoutlp2old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte Zahl. Gibt die Zeit in Sekunden an wie lange auf Antwort der Go-e gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.<br>
								Zulange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die Go-e z.B. gerade unterwegs genutzt wird.
							</div>
						</div>

						<script>
							function display_lp2() {
								$('#evsecondacs1').hide();
								$('#evseconmbs1').hide();
								$('#evseconswifis1').hide();
								$('#llmodullp2').hide();
								$('#evsecongoes1').hide();
								$('#evsecoslaveeth').hide();
								$('#evseconkebas1').hide();
								$('#evseconnrgkicks1').hide();
								$('#openwb12s1').hide();
								$('#evseconipevselp2').hide();
								if($('#evsecons1').val() == 'ipevse') {
									$('#evseconipevselp2').show();
									$('#llmodullp2').show();
								}
								if($('#evsecons1').val() == 'dac') {
									$('#evsecondacs1').show();
									$('#llmodullp2').show();
								}
								if($('#evsecons1').val() == 'modbusevse') {
									$('#evseconmbs1').show();
									$('#llmodullp2').show();
								}
								if($('#evsecons1').val() == 'simpleevsewifi') {
									$('#evseconswifis1').show();
								}
								if($('#evsecons1').val() == 'goe') {
									$('#evsecongoes1').show();
								}
								if($('#evsecons1').val() == 'slaveeth') {
									$('#evsecoslaveeth').show();
								}
								if($('#evsecons1').val() == 'keba') {
									$('#evseconkebas1').show();
								}
								if($('#evsecons1').val() == 'nrgkick') {
									$('#evseconnrgkicks1').show();
								}
								if($('#evsecon').val() == 'openwb12s1') {
									$('#openwb12s1').show();
								}
							}

							$(function() {
								display_lp2();
								$('#evsecons1').change( function(){
									display_lp2();
								});
							});
						</script>

						<div id="llmodullp2">
							<div class="row">
								<b><label for="ladeleistungs1modul">Ladeleistungsmodul für Ladepunkt 2:</label></b>
								<select name="ladeleistungs1modul" id="ladeleistungs1modul">
									<option <?php if($ladeleistungs1modulold == "sdm630modbuslls1\n") echo "selected" ?> value="sdm630modbuslls1">SDM 630 Modbus</option>
									<option <?php if($ladeleistungs1modulold == "sdm120modbuslls1\n") echo "selected" ?> value="sdm120modbuslls1">SDM 120 Modbus</option>
									<option <?php if($ladeleistungs1modulold == "simpleevsewifis1\n") echo "selected" ?> value="simpleevsewifis1">Simple EVSE Wifi</option>
									<option <?php if($ladeleistungs1modulold == "mpm3pmlls1\n") echo "selected" ?> value="mpm3pmlls1">MPM3PM Modbus</option>
									<option <?php if($ladeleistungs1modulold == "goelp2\n") echo "selected" ?> value="goelp2">Go-e</option>
									<option <?php if($ladeleistungs1modulold == "mpm3pmtripplelp2\n") echo "selected" ?> value="mpm3pmtripplelp2">openWB Tripple</option>
									<option <?php if($ladeleistungs1modulold == "mpm3pmlllp2\n") echo "selected" ?> value="mpm3pmlllp2">openWB Satelit</option>
								</select>
							</div>
							<div class="row">
								Modul zur Messung der Ladeleistung des zweiten Ladepunktes.
							</div>
							<div id="mpm3pmlllp2div">
								<div class="row bg-info">
									<b><label for="mpmlp2ip">MPM3PM Modbus Ladeleistung IP:</label></b>
									<input type="text" name="mpmlp2ip" id="mpmlp2ip" value="<?php echo $mpmlp2ipold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte IP Adresse des Modbus Ethernet Konverters.
								</div>
								<div class="row bg-info">
									<b><label for="mpmlp2id">MPM3PM Modbus Ladeleistung ID:</label></b>
									<input type="text" name="mpmlp2id" id="mpmlp2id" value="<?php echo $mpmlp2idold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des MPM3PM.
								</div>
							</div>
							<div id="mpm3pmlls1div">
								<div class="row bg-info">
									<b><label for="mpm3pmlls1source">MPM3PM Modbus Ladeleistung Source:</label></b>
									<input type="text" name="mpm3pmlls1source" id="mpm3pmlls1source" value="<?php echo $mpm3pmlls1sourceold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
									Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich
								</div>
								<div class="row bg-info">
									<b><label for="mpm3pmlls1id">MPM3PM Modbus Ladeleistung ID:</label></b>
									<input type="text" name="mpm3pmlls1id" id="mpm3pmlls1id" value="<?php echo $mpm3pmlls1idold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des MPM3PM.
								</div>
							</div>
							<div id="sdm630s1div">
								<div class="row bg-info">
									<b><label for="sdm630lp2source">Zähler Source:</label></b>
									<input type="text" name="sdm630lp2source" id="sdm630lp2source" value="<?php echo $sdm630lp2sourceold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
									Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich
								</div>
								<div class="row bg-info">
									<b><label for="sdmids1">Zähler ID:</label></b>
									<input type="text" name="sdmids1" id="sdmids1" value="<?php echo $sdmids1old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des Ladepunkt 2 Zählers in der WB.
								</div>
							</div>
							<div id="swifis1div">
								<div class="row">
								Keine Konfiguration erforderlich.
								</div>
							</div>
							<div id="sdm120s1div">
								<div class="row bg-info">
									<b><label for="sdm120lp2source">Zähler Source:</label></b>
									<input type="text" name="sdm120lp2source" id="sdm120lp2source" value="<?php echo $sdm120lp2sourceold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
									Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich
								</div>
								<div class="row bg-info">
									<b><label for="sdm120modbusllid1s1">SDM 120 Zähler 1 ID:</label></b>
									<input type="text" name="sdm120modbusllid1s1" id="sdm120modbusllid1s1" value="<?php echo $sdm120modbusllid1s1old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des Ladepunkt 2 SDM Zählers in der WB.
								</div>
								<div class="row bg-info">
									<b><label for="sdm120modbusllid2s1">SDM Zähler 2 ID:</label></b>
									<input type="text" name="sdm120modbusllid2s1" id="sdm120modbusllid2s1" value="<?php echo $sdm120modbusllid2s1old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des Ladepunkt 2 SDM Zählers 2 in der WB.  Ist keine zweite Phase / SDM120 vorhanden bitte none eintragen.
								</div>
								<div class="row bg-info">
									<b><label for="sdm120modbusllid3s1">SDM Zähler 3 ID:</label></b>
									<input type="text" name="sdm120modbusllid3s1" id="sdm120modbusllid3s1" value="<?php echo $sdm120modbusllid3s1old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des Ladepunkt 2 SDM Zählers 3 in der WB. Ist keine dritte Phase / SDM120 vorhanden bitte none eintragen.
								</div>
							</div>
							<div id="rs485lanlp2">
								<div class="row bg-info">
									<b><label for="lllaniplp2">RS485/Lan-Konverter IP:</label></b>
									<input type="text" name="lllaniplp2" id="lllaniplp2" value="<?php echo $lllaniplp2old ?>">
								</div>
								<div class="row bg-info">
									Ist nur von belang wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant<br>
									Gültige Werte IP. Wenn ein LAN Konverter genutzt wird muss die Source auf /dev/virtualcomx (z.B. /dev/virtualcom0) gesetzt werden.
								</div>
							</div>
						</div>

						<div class="row">
							<b><label for="socmodul1">SOC Modul für Ladepunkt 2:</label></b>
							<select name="socmodul1" id="socmodul1">
								<option <?php if($socmodul1old == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
								<option <?php if($socmodul1old == "soc_http1\n") echo "selected" ?> value="soc_http1">SoC HTTP</option>
								<option <?php if($socmodul1old == "soc_leafs1\n") echo "selected" ?> value="soc_leafs1">SoC Nissan Leaf</option>
								<option <?php if($socmodul1old == "soc_i3s1\n") echo "selected" ?> value="soc_i3s1">SoC BMW i3</option>
								<option <?php if($socmodul1old == "soc_evnotifys1\n") echo "selected" ?> value="soc_evnotifys1">SoC EVNotify</option>
								<option <?php if($socmodul1old == "soc_zoelp2\n") echo "selected" ?> value="soc_zoelp2">SoC Zoe alt</option>
								<option <?php if($socmodul1old == "soc_myrenaultlp2\n") echo "selected" ?> value="soc_myrenaultlp2">SoC MyRenault</option>
								<option <?php if($socmodul1old == "soc_teslalp2\n") echo "selected" ?> value="soc_teslalp2">SoC Tesla</option>
								<option <?php if($socmodul1old == "soc_carnetlp2\n") echo "selected" ?> value="soc_carnetlp2">SoC VW Carnet</option>
								<option <?php if($socmodul1old == "soc_zeronglp2\n") echo "selected" ?> value="soc_zeronglp2">SoC Zero NG</option>
								<option <?php if($socmodul1old == "soc_mqtt\n") echo "selected" ?> value="soc_mqtt">MQTT</option>

							</select>
						</div>
						<div id="socmqtt1">
							<div class="row">Keine Konfiguration erforderlich</div>
							<div class="row">Per MQTT zu schreiben:</div>
							<div class="row"><b>"openWB/set/lp/2/%Soc"</b></div>
							<div class="row">Ladezustand in %, int, 0-100</div>
						</div>
						<div id="socmnone1">
						</div>
						<div id="socmzeronglp2">
							<div class="row bg-info">
							</div>
							<div class="row bg-info">
								<b><label for="soc_zeronglp2_username">Zero Benutzername:</label></b>
								<input type="text" name="soc_zeronglp2_username" id="soc_zeronglp2_username" value="<?php echo $soc_zeronglp2_usernameold ?>">
							</div>
							<div class="row bg-info">
								Email Adresse des Zero Logins
							</div>
							<div class="row bg-info">
								<b><label for="soc_zeronglp2_password">Zero Passwort:</label></b>
								<input type="password" name="soc_zeronglp2_password" id="soc_zeronglp2_password" value="<?php echo $soc_zeronglp2_passwordold ?>">
							</div>
							<div class="row bg-info">
								Password des Zero Logins
							</div>
							<div class="row bg-info">
								<b><label for="soc_zeronglp2_intervall">Abfrageintervall Standby:</label></b>
								<input type="text" name="soc_zeronglp2_intervall" id="soc_zeronglp2_intervall" value="<?php echo $soc_zeronglp2_intervallold ?>">
							</div>
							<div class="row bg-info">
								Wie oft die Zero abgefragt wird wenn nicht geladen wird. Angabe in Minuten.
							</div>
							<div class="row bg-info">
								<b><label for="soc_zeronglp2_intervallladen">Abfrageintervall Laden:</label></b>
								<input type="text" name="soc_zeronglp2_intervallladen" id="soc_zeronglp2_intervallladen" value="<?php echo $soc_zeronglp2_intervallladenold ?>">
							</div>
							<div class="row bg-info">
								Wie oft die Zero abgefragt wird während geladen wird. Angabe in Minuten.
							</div>
						</div>
						<div id="socmteslalp2">
							<div class="row bg-info">
							</div>
							<div class="row bg-info">
								<b><label for="teslasoclp2user">Tesla Benutzername:</label></b>
								<input type="text" name="teslasoclp2user" id="teslasoclp2user" value="<?php echo $socteslalp2usernameold ?>">
							</div>
							<div class="row bg-info">
								Email Adresse des Tesla Logins
							</div>
							<div class="row bg-info">
								<b><label for="teslasoclp2pw">Tesla Passwort:</label></b>
								<input type="password" name="teslasoclp2pw" id="teslasoclp2pw" value="<?php echo $socteslalp2pwold ?>">
							</div>
							<div class="row bg-info">
								Password des Tesla Logins
							</div>
							<div class="row bg-info">
								<b><label for="teslasoclp2carnumber">Auto im Account:</label></b>
								<input type="text" name="teslasoclp2carnumber" id="teslasoclp2carnumber" value="<?php echo $socteslalp2carnumberold ?>">
							</div>
							<div class="row bg-info">
								Im Normalfall hier 0 eintragen. Sind mehrere Teslas im Account für den zweiten Tesla eine 1 eintragen.
							</div>
							<div class="row bg-info">
								<b><label for="teslasoclp2intervall">Abfrageintervall Standby:</label></b>
								<input type="text" name="teslasoclp2intervall" id="teslasoclp2intervall" value="<?php echo $socteslalp2intervallold ?>">
							</div>
							<div class="row bg-info">
								Wie oft der Tesla abgefragt wird wenn nicht geladen wird. Angabe in Minuten.
							</div>
							<div class="row bg-info">
								<b><label for="teslasoclp2intervallladen">Abfrageintervall Laden:</label></b>
								<input type="text" name="teslasoclp2intervallladen" id="teslasoclp2intervallladen" value="<?php echo $socteslalp2intervallladenold ?>">
							</div>
							<div class="row bg-info">
								Wie oft der Tesla abgefragt wird während geladen wird. Angabe in Minuten.
							</div>
						</div>
						<div id="soccarnetlp2">
							<div class="row bg-info">
								<b><label for="carnetlp2user">Benutzername:</label></b>
								<input type="text" name="carnetlp2user" id="carnetlp2user" value="<?php echo $carnetlp2userold ?>">
							</div>
							<div class="row bg-info">
								VW Carnet Benutzername
							</div>
							<div class="row bg-info">
								<b><label for="carnetlp2pass">Passwort:</label></b>
								<input type="password" name="carnetlp2pass" id="carnetlp2pass" value="<?php echo $carnetlp2passold ?>">
							</div>
							<div class="row bg-info">
								VW Carnet Passwort
							</div>
							<div class="row bg-info">
								<b><label for="soccarnetlp2intervall">Verkürztes Intervall beim Laden:</label></b>
								<input type="text" name="soccarnetlp2intervall" id="soccarnetlp2intervall" value="<?php echo $soccarnetlp2intervallold ?>">
							</div>
							<div class="row bg-info">
								Verkürzt das Abfrageintervall beim Laden auf xx Minuten
							</div>
						</div>
						<div id="soczoelp2">
							<div class="row bg-info">
								<b><label for="zoelp2username">Benutzername:</label></b>
								<input type="text" name="zoelp2username" id="zoelp2username" value="<?php echo $zoelp2usernameold ?>">
							</div>
							<div class="row bg-info">
								Renault Zoe Benutzername
							</div>
							<div class="row bg-info">
								<b><label for="zoelp2passwort">Passwort:</label></b>
								<input type="password" name="zoelp2passwort" id="zoelp2passwort" value="<?php echo $zoelp2passwortold ?>">
							</div>
							<div class="row bg-info">
								Renault Zoe Passwort
							</div>
							<b><label for="wakeupzoelp2">Zoe Remote wecken wenn sie eingeschlafen ist:</label></b>
							<select name="wakeupzoelp2" id="wakeupzoelp2">
								<option <?php if($wakeupzoelp2old == "0\n") echo "selected" ?> value="0">Nein</option>
								<option <?php if($wakeupzoelp2old == "1\n") echo "selected" ?> value="1">Ja</option>
							</select>
							<div class="row bg-info">
								Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
							</div>
						</div>
						<div id="socmyrenaultlp2">
							<div class="row bg-info">
								<b><label for="myrenault_userlp2">Benutzername:</label></b>
								<input type="text" name="myrenault_userlp2" id="myrenault_userlp2" value="<?php echo $myrenault_userlp2old ?>">
							</div>
							<div class="row bg-info">
								MyRenault Benutzername
							</div>
							<div class="row bg-info">
								<b><label for="myrenault_passlp2">Passwort:</label></b>
								<input type="password" name="myrenault_passlp2" id="myrenault_passlp2" value="<?php echo $myrenault_passlp2old ?>">
							</div>
							<div class="row bg-info">
								MyRenault Passwort
							</div>
							<div class="row bg-info">
								<b><label for="myrenault_locationlp2">Standort:</label></b>
								<input type="text" name="myrenault_locationlp2" id="myrenault_locationlp2" value="<?php echo $myrenault_locationlp2old ?>">
							</div>
							<div class="row bg-info">
								MyRenault Standort, z.B. de_DE
							</div>
							<div class="row bg-info">
								<b><label for="myrenault_countrylp2">Land:</label></b>
								<input type="text" name="myrenault_countrylp2" id="myrenault_countrylp2" value="<?php echo $myrenault_countrylp2old ?>">
							</div>
							<div class="row bg-info">
								MyRenault Land, z.B. CH, AT, DE
							</div>
							<b><label for="wakeupmyrenaultlp2">Zoe Remote wecken wenn sie eingeschlafen ist:</label></b>
							<select name="wakeupmyrenaultlp2" id="wakeupmyrenaultlp2">
								<option <?php if($wakeupmyrenaultlp2old == "0\n") echo "selected" ?> value="0">Nein</option>
								<option <?php if($wakeupmyrenaultlp2old == "1\n") echo "selected" ?> value="1">Ja</option>
							</select>
							<div class="row bg-info">
								Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
							</div>
						</div>
						<div id="socevnotifylp2">
							<div class="row bg-info">
								<b><label for="evnotifyakeylp2">Akey:</label></b>
								<input type="text" name="evnotifyakeylp2" id="evnotifyakeylp2" value="<?php echo $evnotifyakeylp2old ?>">
							</div>
							<div class="row bg-info">
								Akey des EVNotify Kontos
							</div>
							<div class="row bg-info">
								<b><label for="evnotifytokenlp2">Token:</label></b>
								<input type="text" name="evnotifytokenlp2" id="evnotifytokenlp2" value="<?php echo $evnotifytokenlp2old ?>">
							</div>
							<div class="row bg-info">
								Token des Kontos
							</div>
						</div>
						<div id="socmhttp1">
							<div class="row">
								Gültige Werte none, soc_http. Wenn nicht vorhanden auf none setzen!
							</div>
							<div class="row bg-info">
								<b><label for="hsocip1">SOC zweiter Ladepunkt Http Abfrage URL:</label></b>
								<input type="text" name="hsocip1" id="hsocip1" value="<?php echo $hsocip1old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte none, "url". URL für die Abfrage des Soc der zweiten WB, Antwort muss der reine Zahlenwert sein.
							</div>
						</div>
						<div id="socleaf1">
							<div class="row bg-info">
								<b><label for="leafusernames1">Benutzername:</label></b>
								<input type="text" name="leafusernames1" id="leafusernames1" value="<?php echo $leafusernames1old ?>">
							</div>
							<div class="row bg-info">
								Nissan Connect Benutzername
							</div>
							<div class="row bg-info">
								<b><label for="leafpassworts1">Passwort:</label></b>
								<input type="password" name="leafpassworts1" id="leafpassworts1" value="<?php echo $leafpassworts1old ?>">
							</div>
							<div class="row bg-info">
								Nissan Connect Passwort
							</div>
						</div>
						<div id="soci31">
							<div class="row bg-info">
								<b><label for="i3usernames1">Benutzername:</label></b>
								<input type="text" name="i3usernames1" id="i3usernames1" value="<?php echo $i3usernames1old ?>">
							</div>
							<div class="row bg-info">
								BMW Services Benutzername
							</div>
							<div class="row bg-info">
								<b><label for="i3passworts1">Passwort:</label></b>
								<input type="password" name="i3passworts1" id="i3passworts1" value="<?php echo $i3passworts1old ?>">
							</div>
							<div class="row bg-info">
								BMW Services Passwort
							</div>
							<div class="row bg-info">
								<b><label for="i3vins1">VIN:</label></b>
								<input type="text" name="i3vins1" id="i3vins1" value="<?php echo $i3vins1old ?>">
							</div>
							<div class="row bg-info">
								BMW i3 VIN nötig. Es ist die vollständige aus dem Fzg-Schein anzugeben.
							</div>
							<div class="row bg-info">
								<b><label for="soci3intervall1">Verkürztes Intervall beim Laden:</label></b>
								<input type="text" name="soci3intervall1" id="soci3intervall1" value="<?php echo $soci3intervall1old ?>">
							</div>
							<div class="row bg-info">
								Verkürzt das Abfrageintervall beim Laden auf xx Minuten
							</div>
						</div>

						<script>
							function display_llmp2() {
								$('#sdm630s1div').hide();
								$('#sdm120s1div').hide();
								$('#swifis1div').hide();
								$('#mpm3pmlls1div').hide();
								$('#rs485lanlp2').hide();
								$('#mpm3pmlllp2div').hide();
								if($('#ladeleistungs1modul').val() == 'sdm630modbuslls1') {
									$('#sdm630s1div').show();
									$('#rs485lanlp2').show();
								}
								if($('#ladeleistungs1modul').val() == 'sdm120modbuslls1') {
									$('#sdm120s1div').show();
									$('#rs485lanlp2').show();
								}
								if($('#ladeleistungs1modul').val() == 'simpleevsewifis1') {
									$('#swifis1div').show();
								}
								if($('#ladeleistungs1modul').val() == 'goelp2') {
									$('#swifis1div').show();
								}
								if($('#ladeleistungs1modul').val() == 'mpm3pmlllp2') {
									$('#mpm3pmlllp2div').show();
									$('#rs485lanlp2').hide();
								}

								if($('#ladeleistungs1modul').val() == 'mpm3pmlls1') {
									$('#mpm3pmlls1div').show();
									$('#rs485lanlp2').show();
								}
							}

							$(function() {
								display_llmp2 ();
								$('#ladeleistungs1modul').change( function(){
									display_llmp2();
								});
							});

							function display_socmodul1() {
								$('#socmqtt1').hide();
								$('#socmnone1').hide();
								$('#socmhttp1').hide();
								$('#socleaf1').hide();
								$('#soci31').hide();
								$('#socevnotifylp2').hide();
								$('#soczoelp2').hide();
								$('#socmteslalp2').hide();
								$('#socmyrenaultlp2').hide();
								$('#soccarnetlp2').hide();
								$('#socmzeronglp2').hide();
								if($('#socmodul1').val() == 'soc_mqtt') {
									$('#socmqtt1').show();
								}

								if($('#socmodul1').val() == 'none') {
									$('#socmnone1').hide();
								}
								if($('#socmodul1').val() == 'soc_http1') {
									$('#socmhttp1').show();
								}
								if($('#socmodul1').val() == 'soc_leafs1') {
									$('#socleaf1').show();
								}
								if($('#socmodul1').val() == 'soc_myrenaultlp2') {
									$('#socmyrenaultlp2').show();
								}

								if($('#socmodul1').val() == 'soc_i3s1') {
									$('#soci31').show();
								}
								if($('#socmodul1').val() == 'soc_evnotifys1') {
									$('#socevnotifylp2').show();
								}
								if($('#socmodul1').val() == 'soc_zoelp2') {
							 		$('#soczoelp2').show();
								}
								if($('#socmodul1').val() == 'soc_carnetlp2') {
									$('#soccarnetlp2').show();
								}
								if($('#socmodul1').val() == 'soc_teslalp2') {
									$('#socmteslalp2').show();
								}
								if($('#socmodul1').val() == 'soc_zeronglp2') {
									$('#socmzeronglp2').show();
								}

							}
							$(function() {
								display_socmodul1();
								$('#socmodul1').change( function(){
									display_socmodul1();
								});
							});
						</script>

					</div>

					<script>
						function display_lastmanagement() {
							if($('#lastmanagement').val() == '0') {
								$('#lastmmaus').show();
								$('#lastmman').hide();
								$('#durchslp2').hide();
								$('#nachtls1div').hide();
							}
							else {
								$('#lastmmaus').hide();
								$('#lastmman').show();
								$('#durchslp2').show();
								$('#nachtls1div').show();
							}
						}

						$(function() {
							display_lastmanagement();
							$('#lastmanagement').change( function(){
								display_lastmanagement();
							 } );
						});
					</script>

					<div class="row">
						<h4>
							<b><label for="lastmanagements2">Dritter Ladepunkt:</label></b>
							<select name="lastmanagements2" id="lastmanagements2">
								<option <?php if($lastmanagements2old == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($lastmanagements2old == 1) echo "selected" ?> value="1">An</option>
							</select>
						</h4>
					</div>
					<div class="row">
					</div>
					<div id="lasts2mmaus">
					</div>
					<div id="lasts2mman" style="margin:5em;">
						<div class="row">
						</div>
						<div class="row">
							<b><label for="lp3name">Name Ladepunkt 3:</label></b>
									<input type="text" name="lp3name" id="lp3name" value="<?php echo $lp3nameold ?>">
						</div>

						<div class="row">
							<b><label for="evsecons2">Anbindung der EVSE an Ladepunkt 3:</label></b>
							<select name="evsecons2" id="evsecons2">
								<option <?php if($evsecons2old == "thirdeth\n") echo "selected" ?> value="thirdeth">openWB dritter Ladepunkte</option>
								<option <?php if($evsecons2old == "modbusevse\n") echo "selected" ?> value="modbusevse">Modbus</option>
								<option <?php if($evsecons2old == "dac\n") echo "selected" ?> value="dac">DAC</option>
								<option <?php if($evsecons2old == "simpleevsewifi\n") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
								<option <?php if($evsecons2old == "goe\n") echo "selected" ?> value="goe">Go-e</option>
								<option <?php if($evsecons2old == "ipevse\n") echo "selected" ?> value="ipevse">openWB Satellit</option>
							</select>
						</div>
						<div id="evseconipevselp3">
							<div class="row bg-info">
								<b><label for="evseiplp3">IP Adresse:</label></b>
								<input type="text" name="evseiplp3" id="evseiplp3" value="<?php echo $evseiplp3old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP. Aufgedruckt auf dem Label der openWB.
							</div>
							<div class="row bg-info">
								<b><label for="evseidlp3">EVSE ID:</label></b>
								<input type="text" name="evseidlp3" id="evseidlp3" value="<?php echo $evseidlp3old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte 1-254. Aufgedruckt auf dem Label der openWB.
							</div>
						</div>
							<div id="evseconmbs2">
								<div class="row">
									Modbus nur mit EVSE DIN getestet. Auf der EVSE muss Register 2003 auf 1 gesetzt werden (Deaktivierung analog Eingang), sonst kein beschreiben möglich<br>
									Zudem gibt es einen Bug das die EVSE ID der EVSE DIN sich nicht verstellen und speichern lässt!
								</div>
								<div class="row bg-info">
									<b><label for="evsesources2">EVSE Source:</label></b>
									<input type="text" name="evsesources2" id="evsesources2" value="<?php echo $evsesources2old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.
								</div>
								<div class="row bg-info">
									<b><label for="evseids2">EVSE ID:</label></b>
									<input type="text" name="evseids2" id="evseids2" value="<?php echo $evseids2old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID der Slave 2 EVSE.
								</div>
								<div class="row bg-info">
									<b><label for="evselanips2">RS485/Lan-Konverter IP:</label></b>
									<input type="text" name="evselanips2" id="evselanips2" value="<?php echo $evselanips2old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt, ansonsten ist diese Option irrelevant.
								</div>
							</div>
							<div id="evsecondacs2">
								<div class="row bg-success">
									<b><label for="dacregisters2">Dacregister:</label></b>
									<input type="text" name="dacregisters2" id="dacregisters2" value="<?php echo $dacregisters2old ?>">
								</div>
								<div class="row bg-success">
									Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP<br>
									Rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1". Muss sich von bei Nutzung von zweimal DAC zum ersten unterscheiden!
								</div>
							</div>
							<div id="evseconswifis2">
								<div class="row bg-info">
									<b><label for="evsewifiiplp3">Simple EVSE Wifi IP Adressee:</label></b>
									<input type="text" name="evsewifiiplp3" id="evsewifiiplp3" value="<?php echo $evsewifiiplp3old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte IP Adresse im Format: 192.168.0.12
								</div>
								<div class="row bg-info">
									<b><label for="evsewifitimeoutlp3">Simple EVSE Wifi Timeout:</label></b>
									<input type="text" name="evsewifitimeoutlp3" id="evsewifitimeoutlp3" value="<?php echo $evsewifitimeoutlp3old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte Zahl. Gibt die Zeit in Sekunden an wie lange auf Antwort der Simple EVSE gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.<br>
									Zulange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die SimpleEVSE z.B. gerade unterwegs genutzt wird.
								</div>
							</div>
						<div id="evsecongoes2">
							<div class="row bg-info">
								<b><label for="goeiplp3">Go-e IP Adressee:</label></b>
								<input type="text" name="goeiplp3" id="goeiplp3" value="<?php echo $goeiplp3old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte IP Adresse im Format: 192.168.0.12
							</div>
							<div class="row bg-info">
								<b><label for="goetimeoutlp3">Go-e Timeout:</label></b>
								<input type="text" name="goetimeoutlp3" id="goetimeoutlp3" value="<?php echo $goetimeoutlp3old ?>">
							</div>
							<div class="row bg-info">
								Gültige Werte Zahl. Gibt die Zeit in Sekunden an wie lange auf Antwort der Go-e gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.<br>
								Zulange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die Go-e z.B. gerade unterwegs genutzt wird.
							</div>
						</div>

						<script>
							function display_lp3 () {
								$('#evsecondacs2').hide();
								$('#evseconmbs2').hide();
								$('#evseconswifis2').hide();
								$('#llmodullp3').hide();
								$('#evsecongoes2').hide();
								$('#evseconipevselp3').hide();


								if($('#evsecons2').val() == 'dac') {
									$('#evsecondacs2').show();
									$('#llmodullp3').show();
								}
								if($('#evsecons2').val() == 'modbusevse') {
									$('#evseconmbs2').show();
									$('#llmodullp3').show();
								}
								if($('#evsecons2').val() == 'simpleevsewifi') {
									$('#evseconswifis2').show();
								}
								if($('#evsecons2').val() == 'goe') {
									$('#evsecongoes2').show();
								}
								if($('#evsecons2').val() == 'ipevse') {
									$('#evseconipevselp3').show();
									$('#llmodullp3').show();
								}
							}

							$(function() {
								display_lp3();
								$('#evsecons2').change( function(){
									display_lp3();
								});
							});
						</script>

						<div id="llmodullp3">
							<div class="row">
								<b><label for="ladeleistungss2modul">Ladeleistungsmodul für Ladepunkt 3:</label></b>
								<select name="ladeleistungs2modul" id="ladeleistungss2modul">
									<option <?php if($ladeleistungs2modulold == "sdm630modbuslls2\n") echo "selected" ?> value="sdm630modbuslls2">SDM 630 Modbus</option>
									<option <?php if($ladeleistungs2modulold == "sdm120modbuslls2\n") echo "selected" ?> value="sdm120modbuslls2">SDM 120 Modbus</option>
									<option <?php if($ladeleistungs2modulold == "mpm3pmlls2\n") echo "selected" ?> value="mpm3pmlls2">MPM3PM Modbus</option>
									<option <?php if($ladeleistungs2modulold == "simpleevsewifis2\n") echo "selected" ?> value="simpleevsewifis2">Simple EVSE Wifi</option>
									<option <?php if($ladeleistungs2modulold == "goelp3\n") echo "selected" ?> value="goelp3">Go-E</option>
									<option <?php if($ladeleistungs2modulold == "mpm3pmtripplelp3\n") echo "selected" ?> value="mpm3pmtripplelp3">openWB Tripple</option>
									<option <?php if($ladeleistungs2modulold == "mpm3pmlllp3\n") echo "selected" ?> value="mpm3pmlllp3">openWB Satellit</option>
								</select>
							</div>
							<div class="row">
								Modul zur Messung der Ladeleistung des dritten Ladepunktes.
							</div>
							<div id="mpm3pmlllp3div">
								<div class="row bg-info">
									<b><label for="mpmlp3ip">MPM3PM Modbus Ladeleistung IP:</label></b>
									<input type="text" name="mpmlp3ip" id="mpmlp3ip" value="<?php echo $mpmlp3ipold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte IP Adresse des Modbus Ethernet Konverters.
								</div>
								<div class="row bg-info">
									<b><label for="mpmlp3id">MPM3PM Modbus Ladeleistung ID:</label></b>
									<input type="text" name="mpmlp3id" id="mpmlp3id" value="<?php echo $mpmlp3idold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des MPM3PM.
								</div>
							</div>
							<div id="swifis2div">
								<div class="row">
									Keine Konfiguration erforderlich.
								</div>
							</div>
							<div id="mpm3pmlls2div">
									<div class="row bg-info">
									<b><label for="mpm3pmlls2source">MPM3PM Modbus Ladeleistung Source:</label></b>
									<input type="text" name="mpm3pmlls2source" id="mpm3pmlls2source" value="<?php echo $mpm3pmlls2sourceold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
									Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich
								</div>
								<div class="row bg-info">
									<b><label for="mpm3pmlls2id">MPM3PM Modbus Ladeleistung ID:</label></b>
									<input type="text" name="mpm3pmlls2id" id="mpm3pmlls2id" value="<?php echo $mpm3pmlls2idold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des MPM3PM.
								</div>
							</div>
							<div id="sdm630s2div">
								<div class="row bg-info">
									<b><label for="sdm630lp3source">Zähler Source:</label></b>
									<input type="text" name="sdm630lp3source" id="sdm630lp3source" value="<?php echo $sdm630lp3sourceold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus des Zählers angeschlossen ist.
								</div>
								<div class="row bg-info">
									<b><label for="sdmids2">SDM 630 Zähler ID:</label></b>
									<input type="text" name="sdmids2" id="sdmids2" value="<?php echo $sdmids2old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des Ladepunkt 3 SDM Zählers in der WB.
								</div>
							</div>
							<div id="sdm120s2div">
								<div class="row bg-info">
									<b><label for="sdm120lp3source">Zähler Source:</label></b>
									<input type="text" name="sdm120lp3source" id="sdm120lp3source" value="<?php echo $sdm120lp3sourceold ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus des Zählers angeschlossen ist.
								</div>
								<div class="row bg-info">
									<b><label for="sdm120modbusllid1s2">SDM Zähler 1 ID:</label></b>
									<input type="text" name="sdm120modbusllid1s2" id="sdm120modbusllid1s2" value="<?php echo $sdm120modbusllid1s2old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des Ladepunkt 3 SDM Zählers in der WB.
								</div>
								<div class="row bg-info">
									<b><label for="sdm120modbusllid2s2">SDM Zähler 2 ID:</label></b>
									<input type="text" name="sdm120modbusllid2s2" id="sdm120modbusllid2s2" value="<?php echo $sdm120modbusllid2s2old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des Ladepunkt 3 SDM Zählers 2 in der WB.  Ist keine zweite Phase / SDM120 vorhanden bitte none eintragen.
								</div>
								<div class="row bg-info">
									<b><label for="sdm120modbusllid3s2">SDM Zähler 3 ID:</label></b>
									<input type="text" name="sdm120modbusllid3s2" id="sdm120modbusllid3s2" value="<?php echo $sdm120modbusllid3s2old ?>">
								</div>
								<div class="row bg-info">
									Gültige Werte 1-254. Modbus ID des Ladepunkt 3 SDM Zählers 3 in der WB. Ist keine dritte Phase / SDM120 vorhanden bitte none eintragen.
								</div>
							</div>
							<div id="rs485lanlp3">
								<div class="row bg-info">
									<b><label for="lllaniplp3">RS485/Lan-Konverter IP:</label></b>
									<input type="text" name="lllaniplp3" id="lllaniplp3" value="<?php echo $lllaniplp3old ?>">
								</div>
								<div class="row bg-info">
									Ist nur von belang wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant<br>
									Gültige Werte IP. Wenn ein LAN Konverter genutzt wird muss die Source auf /dev/virtualcomx (z.B. /dev/virtualcom0) gesetzt werden.
								</div>
							</div>
						</div>
					</div>

					<script>
						function display_llmp3 () {
							$('#sdm630s2div').hide();
							$('#sdm120s2div').hide();
							$('#swifis2div').hide();
							$('#rs485lanlp3').hide();
							$('#mpm3pmlls2div').hide();
							$('#mpm3pmlllp3div').hide();


							if($('#ladeleistungss2modul').val() == 'mpm3pmlllp3') {
								$('#mpm3pmlllp3div').show();
								$('#rs485lanlp3').show();
							}

							if($('#ladeleistungss2modul').val() == 'sdm630modbuslls2') {
								$('#sdm630s2div').show();
								$('#rs485lanlp3').show();
							}
							if($('#ladeleistungss2modul').val() == 'sdm120modbuslls2') {
								$('#sdm120s2div').show();
								$('#rs485lanlp3').show();
							}
							if($('#ladeleistungss2modul').val() == 'simpleevsewifis2') {
								$('#swifis2div').show();
							}
							if($('#ladeleistungss2modul').val() == 'goelp3') {
								$('#swifis2div').show();
							}
							if($('#ladeleistungss2modul').val() == 'mpm3pmlls2') {
								$('#mpm3pmlls2div').show();
								$('#rs485lanlp3').show();
							}

						}

						$(function() {
							display_llmp3 ();
							$('#ladeleistungss2modul').change( function(){
								display_llmp3();
							});
						});

						function display_lastmanagement2() {
							if($('#lastmanagements2').val() == '0') {
								$('#lasts2mmaus').show();
								$('#lasts2mman').hide();
								$('#durchslp3').hide();
							}
							else {
								$('#lasts2mmaus').hide();
								$('#lasts2mman').show();
								$('#durchslp3').show();
							}
						}

						$(function() {
							display_lastmanagement2();
							$('#lastmanagements2').change( function() {
								display_lastmanagement2();
							});
						});
					</script>

					<div class="row">
						<h4>
							<b><label for="lastmanagementlp4">Vierter Ladepunkt:</label></b>
							<select name="lastmanagementlp4" id="lastmanagementlp4">
								<option <?php if($lastmanagementlp4old == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($lastmanagementlp4old == 1) echo "selected" ?> value="1">An</option>
							</select>
						</h4>
					</div>

					<div id="lastlp4mmaus">
					</div>
					<div id="lastlp4mman" style="margin:5em;">
						<div class="row">
							<b><label for="lp3name">Name Ladepunkt 4:</label></b>
							<input type="text" name="lp4name" id="lp4name" value="<?php echo $lp4nameold ?>">
						</div>
						<div class="row bg-info">
							<b><label for="evseiplp4">EVSE IP:</label></b>
							<input type="text" name="evseiplp4" id="evseiplp4" value="<?php echo $evseiplp4old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse.
						</div>
						<div class="row bg-info">
							<b><label for="evseidlp4">EVSE ID:</label></b>
							<input type="text" name="evseidlp4" id="evseidlp4" value="<?php echo $evseidlp4old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID der EVSE.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp4ip">MPM3PM Modbus Ladeleistung IP:</label></b>
							<input type="text" name="mpmlp4ip" id="mpmlp4ip" value="<?php echo $mpmlp4ipold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse des Modbus Ethernet Konverters.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp4id">MPM3PM Modbus Ladeleistung ID:</label></b>
							<input type="text" name="mpmlp4id" id="mpmlp4id" value="<?php echo $mpmlp4idold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID des MPM3PM.
						</div>
					</div>

					<script>
						function display_lastmanagementlp4() {
							if($('#lastmanagementlp4').val() == '0') {
								$('#lastlp4mmaus').show();
								$('#lastlp4mman').hide();
							}
							else {
								$('#lastlp4mmaus').hide();
								$('#lastlp4mman').show();
							}
						}

						$(function() {
							display_lastmanagementlp4();
							$('#lastmanagementlp4').change( function() {
								display_lastmanagementlp4();
							});
						});
					</script>
					<div class="row">
						<h4>
							<b><label for="lastmanagementlp5">Fünfter Ladepunkt:</label></b>
							<select name="lastmanagementlp5" id="lastmanagementlp5">
								<option <?php if($lastmanagementlp5old == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($lastmanagementlp5old == 1) echo "selected" ?> value="1">An</option>
							</select>
						</h4>
					</div>

					<div id="lastlp5mmaus">
					</div>
					<div id="lastlp5mman" style="margin:5em;">
						<div class="row">
							<b><label for="lp5name">Name Ladepunkt 5:</label></b>
									<input type="text" name="lp5name" id="lp5name" value="<?php echo $lp5nameold ?>">
						</div>
						<div class="row bg-info">
							<b><label for="evseiplp5">EVSE IP:</label></b>
							<input type="text" name="evseiplp5" id="evseiplp5" value="<?php echo $evseiplp5old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse.
						</div>
						<div class="row bg-info">
							<b><label for="evseidlp5">EVSE ID:</label></b>
							<input type="text" name="evseidlp5" id="evseidlp5" value="<?php echo $evseidlp5old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID der EVSE.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp5ip">MPM3PM Modbus Ladeleistung IP:</label></b>
							<input type="text" name="mpmlp5ip" id="mpmlp5ip" value="<?php echo $mpmlp5ipold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse des Modbus Ethernet Konverters.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp5id">MPM3PM Modbus Ladeleistung ID:</label></b>
							<input type="text" name="mpmlp5id" id="mpmlp5id" value="<?php echo $mpmlp5idold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID des MPM3PM.
						</div>
					</div>

					<script>
						function display_lastmanagementlp5() {
							if($('#lastmanagementlp5').val() == '0') {
								$('#lastlp5mmaus').show();
								$('#lastlp5mman').hide();
							}
							else {
								$('#lastlp5mmaus').hide();
								$('#lastlp5mman').show();
							}
						}

						$(function() {
							display_lastmanagementlp5();
							$('#lastmanagementlp5').change( function() {
								display_lastmanagementlp5();
							});
						});
					</script>
					<div class="row">
						<h4>
							<b><label for="lastmanagementlp6">Sechster Ladepunkt:</label></b>
							<select name="lastmanagementlp6" id="lastmanagementlp6">
								<option <?php if($lastmanagementlp6old == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($lastmanagementlp6old == 1) echo "selected" ?> value="1">An</option>
							</select>
						</h4>
					</div>

					<div id="lastlp6mmaus">
					</div>
					<div id="lastlp6mman" style="margin:5em;">
						<div class="row">
							<b><label for="lp6name">Name Ladepunkt 6:</label></b>
									<input type="text" name="lp6name" id="lp6name" value="<?php echo $lp6nameold ?>">
						</div>
						<div class="row bg-info">
							<b><label for="evseiplp6">EVSE IP:</label></b>
							<input type="text" name="evseiplp6" id="evseiplp6" value="<?php echo $evseiplp6old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse.
						</div>
						<div class="row bg-info">
							<b><label for="evseidlp6">EVSE ID:</label></b>
							<input type="text" name="evseidlp6" id="evseidlp6" value="<?php echo $evseidlp6old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID der EVSE.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp6ip">MPM3PM Modbus Ladeleistung IP:</label></b>
							<input type="text" name="mpmlp6ip" id="mpmlp6ip" value="<?php echo $mpmlp6ipold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse des Modbus Ethernet Konverters.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp6id">MPM3PM Modbus Ladeleistung ID:</label></b>
							<input type="text" name="mpmlp6id" id="mpmlp6id" value="<?php echo $mpmlp6idold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID des MPM3PM.
						</div>
					</div>

					<script>
						function display_lastmanagementlp6() {
							if($('#lastmanagementlp6').val() == '0') {
								$('#lastlp6mmaus').show();
								$('#lastlp6mman').hide();
							}
							else {
								$('#lastlp6mmaus').hide();
								$('#lastlp6mman').show();
							}
						}
						$(function() {
							display_lastmanagementlp6();
							$('#lastmanagementlp6').change( function() {
								display_lastmanagementlp6();
							});
						});
					</script>
					<div class="row">
						<h4>
							<b><label for="lastmanagementlp7">Siebter Ladepunkt:</label></b>
							<select name="lastmanagementlp7" id="lastmanagementlp7">
								<option <?php if($lastmanagementlp7old == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($lastmanagementlp7old == 1) echo "selected" ?> value="1">An</option>
							</select>
						</h4>
					</div>

					<div id="lastlp7mmaus">
					</div>
					<div id="lastlp7mman" style="margin:5em;">
						<div class="row">
							<b><label for="lp7name">Name Ladepunkt 7:</label></b>
									<input type="text" name="lp7name" id="lp7name" value="<?php echo $lp7nameold ?>">
						</div>
						<div class="row bg-info">
							<b><label for="evseiplp7">EVSE IP:</label></b>
							<input type="text" name="evseiplp7" id="evseiplp7" value="<?php echo $evseiplp7old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse.
						</div>
						<div class="row bg-info">
							<b><label for="evseidlp7">EVSE ID:</label></b>
							<input type="text" name="evseidlp7" id="evseidlp7" value="<?php echo $evseidlp7old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID der EVSE.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp7ip">MPM3PM Modbus Ladeleistung IP:</label></b>
							<input type="text" name="mpmlp7ip" id="mpmlp7ip" value="<?php echo $mpmlp7ipold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse des Modbus Ethernet Konverters.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp7id">MPM3PM Modbus Ladeleistung ID:</label></b>
							<input type="text" name="mpmlp7id" id="mpmlp7id" value="<?php echo $mpmlp7idold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID des MPM3PM.
						</div>
					</div>

					<script>
						function display_lastmanagementlp7() {
							if($('#lastmanagementlp7').val() == '0') {
								$('#lastlp7mmaus').show();
								$('#lastlp7mman').hide();
							}
							else {
								$('#lastlp7mmaus').hide();
								$('#lastlp7mman').show();
							}
						}

						$(function() {
							display_lastmanagementlp7();
							$('#lastmanagementlp7').change( function() {
								display_lastmanagementlp7();
							});
						});
					</script>
					<div class="row">
						<h4>
							<b><label for="lastmanagementlp8">Achter Ladepunkt:</label></b>
							<select name="lastmanagementlp8" id="lastmanagementlp8">
								<option <?php if($lastmanagementlp8old == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($lastmanagementlp8old == 1) echo "selected" ?> value="1">An</option>
							</select>
						</h4>
					</div>

					<div id="lastlp8mmaus">
					</div>
					<div id="lastlp8mman" style="margin:5em;">
						<div class="row">
							<b><label for="lp8name">Name Ladepunkt 8:</label></b>
									<input type="text" name="lp8name" id="lp8name" value="<?php echo $lp8nameold ?>">
						</div>
						<div class="row bg-info">
							<b><label for="evseiplp8">EVSE IP:</label></b>
							<input type="text" name="evseiplp8" id="evseiplp8" value="<?php echo $evseiplp8old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse.
						</div>
						<div class="row bg-info">
							<b><label for="evseidlp8">EVSE ID:</label></b>
							<input type="text" name="evseidlp8" id="evseidlp8" value="<?php echo $evseidlp8old ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID der EVSE.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp8ip">MPM3PM Modbus Ladeleistung IP:</label></b>
							<input type="text" name="mpmlp8ip" id="mpmlp8ip" value="<?php echo $mpmlp8ipold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte IP Adresse des Modbus Ethernet Konverters.
						</div>
						<div class="row bg-info">
							<b><label for="mpmlp8id">MPM3PM Modbus Ladeleistung ID:</label></b>
							<input type="text" name="mpmlp8id" id="mpmlp8id" value="<?php echo $mpmlp8idold ?>">
						</div>
						<div class="row bg-info">
							Gültige Werte 1-254. Modbus ID des MPM3PM.
						</div>
					</div>

					<script>
						function display_lastmanagementlp8() {
							if($('#lastmanagementlp8').val() == '0') {
								$('#lastlp8mmaus').show();
								$('#lastlp8mman').hide();
							}
							else {
								$('#lastlp8mmaus').hide();
								$('#lastlp8mman').show();
							}
						}

						$(function() {
							display_lastmanagementlp8();
							$('#lastmanagementlp8').change( function() {
								display_lastmanagementlp8();
							});
						});
					</script>
					<div class="row">
						<h3> Strombezugsmessmodul (EVU-Übergabepunkt)</h3>
					</div>
					<div class="row">
						<b><label for="wattbezugmodul">Strombezugsmodul:</label></b>
						<select name="wattbezugmodul" id="wattbezugmodul">
							<option <?php if($wattbezugmodulold == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
							<option <?php if($wattbezugmodulold == "bezug_ethmpm3pm\n") echo "selected" ?> value="bezug_ethmpm3pm">openWB EVU Kit</option>
							<option <?php if($wattbezugmodulold == "vzlogger\n") echo "selected" ?> value="vzlogger">VZLogger</option>
							<option <?php if($wattbezugmodulold == "sdm630modbusbezug\n") echo "selected" ?> value="sdm630modbusbezug">SDM 630</option>
							<option <?php if($wattbezugmodulold == "bezug_http\n") echo "selected" ?> value="bezug_http">HTTP</option>
							<option <?php if($wattbezugmodulold == "bezug_json\n") echo "selected" ?> value="bezug_json">Json</option>
							<option <?php if($wattbezugmodulold == "bezug_mpm3pm\n") echo "selected" ?> value="bezug_mpm3pm">MPM3PM</option>
							<option <?php if($wattbezugmodulold == "bezug_smashm\n") echo "selected" ?> value="bezug_smashm">SMA HomeManager</option>
							<option <?php if($wattbezugmodulold == "bezug_fronius_sm\n") echo "selected" ?> value="bezug_fronius_sm">Fronius Energy Meter</option>
							<option <?php if($wattbezugmodulold == "bezug_fronius_s0\n") echo "selected" ?> value="bezug_fronius_s0">Fronius WR mit S0 Meter</option>
							<option <?php if($wattbezugmodulold == "bezug_solarlog\n") echo "selected" ?> value="bezug_solarlog">SolarLog</option>
							<option <?php if($wattbezugmodulold == "bezug_solaredge\n") echo "selected" ?> value="bezug_solaredge">Solaredge</option>
							<option <?php if($wattbezugmodulold == "bezug_smartme\n") echo "selected" ?> value="bezug_smartme">Smartme</option>
							<option <?php if($wattbezugmodulold == "bezug_e3dc\n") echo "selected" ?> value="bezug_e3dc">E3DC Speicher</option>
							<option <?php if($wattbezugmodulold == "bezug_sbs25\n") echo "selected" ?> value="bezug_sbs25">SMA Sunny Boy Storage </option>
							<option <?php if($wattbezugmodulold == "bezug_kostalplenticoreem300haus\n") echo "selected" ?> value="bezug_kostalplenticoreem300haus">Kostal Plenticore mit EM300/KSEM</option>
							<option <?php if($wattbezugmodulold == "bezug_kostalpiko\n") echo "selected" ?> value="bezug_kostalpiko">Kostal Piko mit Energy Meter</option>
							<option <?php if($wattbezugmodulold == "bezug_ksem\n") echo selected ?> value="bezug_ksem">Kostal Smart Energy Meter oder TQ EM410</option>
							<option <?php if($wattbezugmodulold == "bezug_smartfox\n") echo "selected" ?> value="bezug_smartfox">Smartfox</option>
							<option <?php if($wattbezugmodulold == "bezug_powerwall\n") echo "selected" ?> value="bezug_powerwall">Tesla Powerwall</option>
							<option <?php if($wattbezugmodulold == "bezug_victrongx\n") echo "selected" ?> value="bezug_victrongx">Victron (z.B. GX)</option>
							<option <?php if($wattbezugmodulold == "bezug_alphaess\n") echo "selected" ?> value="bezug_alphaess">Alpha ESS</option>
							<option <?php if($wattbezugmodulold == "bezug_solarview\n") echo "selected" ?> value="bezug_solarview">Solarview</option>
							<option <?php if($wattbezugmodulold == "bezug_discovergy\n") echo "selected" ?> value="bezug_discovergy">Discovergy</option>
							<option <?php if($wattbezugmodulold == "bezug_lgessv1\n") echo "selected" ?> value="bezug_lgessv1">LG ESS 1.0VI</option>
							<option <?php if($wattbezugmodulold == "bezug_mqtt\n") echo "selected" ?> value="bezug_mqtt">MQTT</option>
							<option <?php if($wattbezugmodulold == "bezug_sonneneco\n") echo "selected" ?> value="bezug_sonneneco">Sonnen eco</option>
							<option <?php if($wattbezugmodulold == "bezug_fems\n") echo "selected" ?> value="bezug_fems">Fenecon FEMS</option>
							<option <?php if($wattbezugmodulold == "bezug_solarworld\n") echo "selected" ?> value="bezug_solarworld">Solarworld</option>
							<option <?php if($wattbezugmodulold == "bezug_siemens\n") echo "selected" ?> value="bezug_siemens">Siemens Speicher</option>
						</select>
					</div>
					<div id="wattbezugsonneneco">
						<div class="row">
							Keine Konfiguration erforderlich. Es muss beim Speicher die alternative Methode ausgewählt werden, da die Daten nur von der JSON-API übergeben werden.
						</div>
					</div>
					<div id="wattbezugmqtt">
						<div class="row">Keine Konfiguration erforderlich</div>
						<div class="row">Per MQTT zu schreiben:</div>
						<div class="row"><b>"openWB/set/evu/W"</b></div>
						<div class="row">Bezugsleistung in Watt, int, positiv Bezug, negativ Einspeisung</div>
						<div class="row"><b>"openWB/set/evu/APhase1"</b></div>
						<div class="row">Strom in Ampere für Phase 1, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung</div>
						<div class="row"><b>"openWB/set/evu/APhase2"</b></div>
						<div class="row">Strom in Ampere für Phase 2, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung</div>
						<div class="row"><b>"openWB/set/evu/APhase3"</b></div>
						<div class="row">Strom in Ampere für Phase 3, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung</div>
						<div class="row"><b>"openWB/set/evu/WhImported"</b></div>
						<div class="row">Bezogene Energie in Wh, float, Punkt als Trenner, nur positiv</div>
						<div class="row"><b>"openWB/set/evu/WhExported"</b></div>
						<div class="row">Eingespeiste Energie in Wh, float, Punkt als Trenner, nur positiv</div>
						<div class="row"><b>"openWB/set/evu/VPhase1"</b></div>
						<div class="row">Spannung in Volt für Phase 1, float, Punkt als Trenner</div>
						<div class="row"><b>"openWB/set/evu/VPhase2"</b></div>
						<div class="row">Spannung in Volt für Phase 2, float, Punkt als Trenner</div>
						<div class="row"><b>"openWB/set/evu/VPhase3"</b></div>
						<div class="row">Spannung in Volt für Phase 3, float, Punkt als Trenner</div>
						<div class="row"><b>"openWB/set/evu/HzFrequenz"</b></div>
						<div class="row">Netzfrequenz in Hz, float, Punkt als Trenner</div>
					</div>
					<div id="wattbezuglgessv1">
						<div class="row">
							Konfiguration im zugehörigen Speichermodul des LG ESS 1.0VI erforderlich. Als PV-Modul auch LG ESS 1.0VI wählen!
						</div>
					</div>
					<div id="wattbezugip">
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug1_ip">IP:</label></b>
							<input type="text" name="bezug1_ip" id="bezug1_ip" value="<?php echo $bezug1_ipold ?>">
						</div>
					</div>

					<div id="wattbezugsiemens">
						<div class="row">
							IP Adresse des Siemens Speichers eingeben. Im Siemens Speicher muss die Schnittstelle openWB gewählt werden.
						</div>
					</div>

					<div id="wattbezugethmpm3pm">
						<div class="row">
							<b><label for="evukitversion">Version des openWB evu Kits:</label></b>
							<select name="evukitversion" id="evukitversion">
								<option <?php if($evukitversionold == 0) echo "selected" ?> value="0">EVU Kit</option>
								<option <?php if($evukitversionold == 1) echo "selected" ?> value="1">EVU Kit v2</option>
							</select>
						</div>
					</div>
					<div id="wattbezugsolarview">
						<div class="row">
							Konfiguration im zugehörigen PV Modul erforderlich.
						</div>
					</div>
					<div id="wattbezugpowerwall">
						<div class="row">
							Keine Konfiguration erforderlich. Mit diesem Modul ist kein Lastmanagement / Hausanschlussüberwachung möglich.
						</div>
					</div>
					<div id="wattbezugvictrongx">
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_victronip">Victron IP:</label></b>
							<input type="text" name="bezug_victronip" id="bezug_victronip" value="<?php echo $bezug_victronipold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP. IP Adresse des Victron, z.B. GX.
						</div>
					</div>
					<div id="wattbezugfems">
						<div class="row" style="background-color:#febebe">
							<b><label for="femsip">Fenecon IP:</label></b>
							<input type="text" name="femsip" id="femsip" value="<?php echo $femsipold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP. IP Adresse des Fenecon FEMS.
						</div>
					</div>
					<div id="wattbezugsolarworld">
						<div class="row" style="background-color:#febebe">
							<b><label for="solarworld_emanagerip">Solarworld IP:</label></b>
							<input type="text" name="solarworld_emanagerip" id="solarworld_emanagerip" value="<?php echo $solarworld_emanageripold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP. IP Adresse des Solarworld eManager.
						</div>
					</div>

					<div id="wattbezugdiscovergy">
						<div class="row" style="background-color:#febebe">
							<b><label for="discovergyuser">Discovergy Username (Email):</label></b>
							<input type="text" name="discovergyuser" id="discovergyuser" value="<?php echo $discovergyuserold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="discovergypass">Discovergy Passwort:</label></b>
							<input type="text" name="discovergypass" id="discovergypass" value="<?php echo $discovergypassold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="discovergyevuid">Meter ID:</label></b>
							<input type="text" name="discovergyevuid" id="discovergyevuid" value="<?php echo $discovergyevuidold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte ID. Um die ID herauszufinden mit dem Browser die Adresse "https://api.discovergy.com/public/v1/meters" aufrufen und dort Benutzername und Passwort eingeben. Hier wird nun u.a. die ID des Zählers angezeigt.
						</div>
					</div>
					<div id="wattbezugkostalsmartenergymeter">
                                                <div class="row" style="background-color:#febebe">
                                                        <b><label for="ksemip">Kostal Smart Energy Meter / TQ EM410 - IP Adresse:</label></b>
                                                        <input type="text" name="ksemip" id="ksemip" value="<?php echo $ksemipold ?>"><br>
                                                </div>
                                        </div>
					<div id="wattbezugkostalpiko">
						<div class="row" style="background-color:#febebe">
							IP Adresse wird im PV Modul konfiguriert. Angeschlossenes Meter erforderlich. Der WR liefert Werte nur solange er auch PV Leistung liefert. Nachts geht er in den Standby.<br>
							Die Hausanschlussüberwachung ist nur aktiv wenn der Wechselrichter auch aktiv ist.<br>
							Ein extra PV-Modul muss nicht mehr ausgewählt werden.
						</div>
					</div>
					<div id="wattbezugplentihaus">
						<div class="row" style="background-color:#febebe">
							Dieses Modul erfordert als 1. PV-Modul das Modul "Kostal Plenticore". Dieses wird automatisch fest eingestellt. Der EM300 bzw. das KSEM muss am 1. Plenticore angeschlossen sein.
							Ein am 1. Plenticore angeschlossener Speicher wird ebenfalls ohne weitere Einstellung ausgelesen, das Speicher-Modul wird dazu entsprechend voreingestellt.
							Am 2. Plenticore darf kein Speicher angeschlossen sein, da dies die weiteren Berechnungen verfälscht.
							Die Einbauposition des EM300/KSEM (Hausverbrauchs-Zweig = Pos. 1 oder Netzanschluss-Zweig = Pos. 2) ist anzugeben.
						</div>
						<input type='hidden' value='0' name='kostalplenticorehaus'>
						<input id="kostalplenticorehaus" name="kostalplenticorehaus" value="1" type="checkbox" <?php if ( $kostalplenticorehausold == 1){ echo "checked"; } ?> >
						<label for="kostalplenticorehaus">EM300/KSEM im Netzanschluss-Zweig (Pos. 2)</label>
					</div>
					<div id="wattbezugmpm3pm">
						<div class="row" style="background-color:#febebe">
							<b><label for="mpm3pmevusource">MPM3PM Zähler EVU Source:</label></b>
							<input type="text" name="mpm3pmevusource" id="mpm3pmevusource" value="<?php echo $mpm3pmevusourceold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
							Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="mpm3pmevuid">MPM3PM Zähler EVU ID:</label></b>
							<input type="text" name="mpm3pmevuid" id="mpm3pmevuid" value="<?php echo $mpm3pmevuidold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte 1-254. Modbus ID des MPM3PM.
						</div>
						<input type='hidden' value='0' name='mpm3pmevuhaus'>
						<input id="mpm3pmevuhaus" name="mpm3pmevuhaus" value="1" type="checkbox" <?php if ( $mpm3pmevuhausold == 1){ echo "checked"; } ?> >
						<label for="mpm3pmevuhaus">MPM3PM im Hausverbrauchszweig</label>
						<div class="row" style="background-color:#febebe">
							Wenn der MPM3PM EVU Zähler im Hausverbrauchszweig NACH den Ladepunkten angeschlossen ist hier ein Hacken setzen.<br>
							z.B. auch zu nutzen wenn der Ladepunkt an einem seperaten Rundsteuerempfänger(=extra Zähler) angeschlossen ist.<br>
							Bei gesetzten Hacken werden die Ladeströme der Ladepunkte zu den Strömen gemessen am EVU Zähler hinzuaddiert.<br>
							Somit ist ein Lastmanagement / Hausanschlussüberwachung möglich.
							Auf korrekte Verkabelung ist zu achten!<br>
							EVU L1, LP1 L1, LP2 L2<br>
							EVU L2, LP1 L2, LP2 L3<br>
							EVU L3, LP1 L3, LP2 L1
						</div>
					</div>
					<div id="wattbezugnone">
						<div class="row" style="background-color:#febebe">
							<b><label for="hausbezugnone">Angenommener Hausverbrauch:</label></b>
							<input type="text" name="hausbezugnone" id="hausbezugnone" value="<?php echo $hausbezugnoneold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte Zahl. Wenn keine EVU Messung vorhanden ist kann hier ein Hausgrundverbrauch festgelegt werden.<br>
							Daraus resultierend agiert die PV Regelung bei vorhandenem PV-Modul
						</div>
					</div>
					<div id="wattbezugsdm">
						<div class="row" style="background-color:#febebe">
							<b><label for="sdm630modbusbezugsource">SDM 630 Zähler Source:</label></b>
							<input type="text" name="sdm630modbusbezugsource" id="sdm630modbusbezugsource" value="<?php echo $sdm630modbusbezugsourceold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte /dev/ttyUSBx, /dev/virtualcomx. Das "x" steht für den Adapter. Dies kann 0,1,2, usw sein. Serieller Port an dem der SDM angeschlossen ist.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="sdm630modbusbezugid">Zähler ID:</label></b>
							<input type="text" name="sdm630modbusbezugid" id="sdm630modbusbezugid" value="<?php echo $sdm630modbusbezugidold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte 1-254. Modbus ID des SDM. Getestet SDM230 & SDM630v2.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="sdm630modbusbezuglanip">RS485/Lan-Konverter IP:</label></b>
							<input type="text" name="sdm630modbusbezuglanip" id="sdm630modbusbezuglanip" value="<?php echo $sdm630modbusbezuglanipold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt.
						</div>
					</div>
					<div id="wattbezugvz">
						<div class="row" style="background-color:#febebe">
							<b><label for="vzloggerip">Vzlogger IP Adresse inkl Port:</label></b>
							<input type="text" name="vzloggerip" id="vzloggerip" value="<?php echo $vzloggeripold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP:Port z.B. 192.168.0.12:8080.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="vzloggerline">Vzlogger Watt Zeile:</label></b>
							<input type="text" name="vzloggerline" id="vzloggerline" value="<?php echo $vzloggerlineold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br>
							Nun zählen in welcher Zeile die aktullen Watt stehen und diesen hier eintragen.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="vzloggerline">Vzlogger Bezug kWh Zeile:</label></b>
							<input type="text" name="vzloggerkwhline" id="vzloggerkwhline" value="<?php echo $vzloggerkwhlineold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br>
							Nun zählen in welcher Zeile die Gesamt kWh stehen und diesen hier eintragen. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="vzloggerline">Vzlogger Einspeisung kWh Zeile:</label></b>
							<input type="text" name="vzloggerekwhline" id="vzloggerekwhline" value="<?php echo $vzloggerekwhlineold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br>
							Nun zählen in welcher Zeile die Gesamt eingespeisten kWh stehen und diesen hier eintragen.
						</div>
					</div>
					<div id="wattbezughttp">
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_http_w_url">Vollständige URL für den Watt Bezug</label></b>
							<input type="text" name="bezug_http_w_url" id="bezug_http_w_url" value="<?php echo htmlspecialchars($bezug_http_w_urlold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Watt sein.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_http_ikwh_url">Vollständige URL für den kWh Bezug</label></b>
							<input type="text" name="bezug_http_ikwh_url" id="bezug_http_ikwh_url" value="<?php echo htmlspecialchars($bezug_http_ikwh_urlold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Der Wert muss in WattStunden sein. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_http_ekwh_url">Vollständige URL für die kWh Einspeisung</label></b>
							<input type="text" name="bezug_http_ekwh_url" id="bezug_http_ekwh_url" value="<?php echo htmlspecialchars($bezug_http_ekwh_urlold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Der Wert muss in WattStunden sein. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_http_l1_url">Vollständige URL für die Ampere Phase 1</label></b>
							<input type="text" name="bezug_http_l1_url" id="bezug_http_l1_url" value="<?php echo htmlspecialchars($bezug_http_l1_urlold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Ampere sein. Bei nicht Nutzung auf none setzen.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_http_l2_url">Vollständige URL für die Ampere Phase 2</label></b>
							<input type="text" name="bezug_http_l2_url" id="bezug_http_l2_url" value="<?php echo htmlspecialchars($bezug_http_l2_urlold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Ampere sein. Bei nicht Nutzung auf none setzen.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_http_l3_url">Vollständige URL für die Ampere Phase 3</label></b>
							<input type="text" name="bezug_http_l3_url" id="bezug_http_l3_url" value="<?php echo htmlspecialchars($bezug_http_l3_urlold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Ampere sein. Bei nicht Nutzung auf none setzen.
						</div>

					</div>
					<div id="wattbezugsmartme">
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_smartme_user">Smartme Benutzername</label></b>
							<input type="text" name="bezug_smartme_user" id="bezug_smartme_user" value="<?php echo htmlspecialchars($bezug_smartme_userold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Smartme Benutzername
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_smartme_pass">Smartme Passwort</label></b>
							<input type="text" name="bezug_smartme_pass" id="bezug_smartme_pass" value="<?php echo htmlspecialchars($bezug_smartme_passold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Smartme Passwort
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_smartme_url">Smartme Url</label></b>
							<input type="text" name="bezug_smartme_url" id="bezug_smartme_url" value="<?php echo htmlspecialchars($bezug_smartme_urlold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Smartme Url
						</div>
					</div>
					<div id="wattbezugshm">
						<div class="row" style="background-color:#febebe">
							<b><label for="smaeshmbezugid">Seriennummer des SMA Home Manager</label></b>
							<input type="text" name="smashmbezugid" id="smaeshmbezugid" value="<?php echo $smashmbezugidold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte: Seriennummer. Hier die Seriennummer des SMA Meter für Bezug/Einspeisung anzugeben. Ist nur erforderlich wenn mehrere SMA HomeManager in Betrieb sind, ansonsten none eintragen. Funktioniert auch mit Energy Meter statt Home Manager.
						</div>
					</div>
					<div id="wattbezugsmartfox">
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_smartfox_ip">Ip Adresse des SmartFox</label></b>
							<input type="text" name="bezug_smartfox_ip" id="bezug_smartfox_ip" value="<?php echo $bezug_smartfox_ipold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP Adresse.
						</div>
					</div>
					<div id="wattbezugsma">
						<div class="row" style="background-color:#febebe">
							<b><label for="smaemdbezugid">Seriennummer des SMA Energy Meter</label></b>
							<input type="text" name="smaemdbezugid" id="smaemdbezugid" value="<?php echo $smaemdbezugidold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte Seriennummer. Hier die Seriennummer des SMA Meter für Bezug/Einspeisung angeben<br>
							Infos zum SMA Energy Meter <a href="https://github.com/snaptec/openWB#extras">HIER</a>
						</div>
					</div>
					<div id="wattbezugfronius">
						<div class="row" style="background-color:#febebe"> Die IP des Wechselrichters wird im dazugehörigen Fronius PV-Modul eingestellt.
						</div>
						<input type='hidden' value='0' name='froniuserzeugung'>
						<input id="froniuserzeugung" name="froniuserzeugung" value="1" type="checkbox" <?php if ( $froniuserzeugungold == 1){ echo "checked"; } ?> >
						<label for="froniuserzeugung"> Meter mit ID 1 statt 0</label><br />
						<input type='hidden' value='0' name='froniusprimo'>
						<input id="froniusprimo" name="froniusprimo" value="1" type="checkbox" <?php if ( $froniusprimoold == 1){ echo "checked"; } ?> >
						<label for="froniusprimo"> Kompatibilitätsmodus für die Primo Reihe</label>
					</div>
					<div id="wattbezugjson">
						<div class="row" style="background-color:#febebe">
							<b><label for="bezugjsonurl">Bezug URL:</label></b>
							<input type="text" name="bezugjsonurl" id="bezugjsonurl" value="<?php echo $bezugjsonurlold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte URL. Vollständige URL die die Json Antwort enthält.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezugjsonwatt">Json Abfrage für Watt:</label></b>
							<input type="text" name="bezugjsonwatt" id="bezugjsonwatt" value="<?php echo $bezugjsonwattold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche.<br>
							Im Hintergrund wird der Befehl jq benutzt.<br>
							Ist die Json Antwort z.B."{"PowerInstalledPeak":4655,"PowerProduced":132,"PowerOut":897.08172362555717,"PowerSelfSupplied":234.9182763744428}" So muss hier - .PowerOut - ohne die - - eingetragen werden.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezugjsonkwh">Json Abfrage für Bezug kWh:</label></b>
							<input type="text" name="bezugjsonkwh" id="bezugjsonkwh" value="<?php echo $bezugjsonkwhold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche.<br>
							Im Hintergrund wird der Befehl jq benutzt.<br>
							Ist die Json Antwort z.B."{"PowerInstalledPeak":4655,"PowerProduced":132,"PowerOut":897.08172362555717,"PowerSelfSupplied":234.9182763744428}" So muss hier - .PowerProduced - ohne die - - eingetragen werden
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="bezugjsonkwh">Json Abfrage für Einspeisung kWh:</label></b>
							<input type="text" name="einspeisungjsonkwh" id="einspeisungjsonkwh" value="<?php echo $einspeisungjsonkwhold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche.<br>
							Im Hintergrund wird der Befehl jq benutzt.<br>
							Ist die Json Antwort z.B."{"PowerInstalledPeak":4655,"PowerProduced":132,"PowerOut":897.08172362555717,"PowerSelfSupplied":234.9182763744428}" So muss hier - .PowerSelfSupplied - ohne die - - eingetragen werden.
						</div>
					</div>
					<div id="wattbezugsolarlog">

						<div class="row" style="background-color:#febebe">
							Die zugehörige IP Adresse ist im PV Modul einzustellen.
						</div>
						<div class="row">
							<b><label for="bezug_solarlog_speicherv">Kompatibilitätsmodus bei vorhandenem Speicher:</label></b>
							<select name="bezug_solarlog_speicherv" id="bezug_solarlog_speicherv">
								<option <?php if($bezug_solarlog_speichervold == 0) echo "selected" ?> value="0">Nein</option>
								<option <?php if($bezug_solarlog_speichervold == 1) echo "selected" ?> value="1">Ja</option>
							</select>
						</div>
					</div>
					<div id="wattbezugsolaredge">
						<div class="row" style="background-color:#febebe">
							<b><label for="solaredgeip">IP Adresse des SolarEdge</label></b>
							<input type="text" name="solaredgeip" id="solaredgeip" value="<?php echo htmlspecialchars($solaredgeipold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP.<br>
							Hierfür muss ein EVU Zähler am SolarEdge Wechselrichter per Modbus angebunden sein.<br>
							Ebenso muss ModbusTCP am Wechselrichter aktiviert werden
						</div>
					</div>
					<div id="wattbezuge3dc">
						<div class="row" style="background-color:#febebe">
							Die IP des Speichers wird im dazugehörigen E3DC Speicher-Modul eingestellt.<br>
							Es kann nötig sein in den Einstellungen des E3DC ModbusTCP zu aktivieren.<br>
							Das Protokoll in den E3DC Einstellungen ist auf E3DC zu stellen.
						</div>
					</div>
					<div id="wattbezugsbs25">
						<div class="row" style="background-color:#febebe">
							Die IP des Speichers wird im dazugehörigen SMA SBS Speicher-Modul eingestellt.
						</div>
					</div>

					<div class="row">
						<h4>
							<b><label for="evuglaettungakt">EVU Glättung:</label></b>
							<select name="evuglaettungakt" id="evuglaettungakt">
								<option <?php if($evuglaettungaktold == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($evuglaettungaktold == 1) echo "selected" ?> value="1">An</option>
							</select>
						</h4>
					</div>

					<div id="evuglaettungdiv">
						<div class="row" style="background-color:#febebe">
							<b><label for="evuglaettung">Glättung der EVU Werte:</label></b>
							<input type="text" name="evuglaettung" id="evuglaettung" value="<?php echo $evuglaettungold ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte: Zeit in Sekunden, z.B. 30,50,200.<br>
							Kombiniert die EVU Werte der letzten x Sekunden und bildet einen Mittelwert darüber.<br>
							Sinnvoll, wenn öfter kurze Lastspitzen auftreten.<br>
							Der Durchschnittswert wird auf der Hauptseite in Klammern angezeigt.
						</div>
					</div>

					<script>
						$(function() {
							if($('#evuglaettungakt').val() == '0') {
								$('#evuglaettungdiv').hide();
							} else {
								$('#evuglaettungdiv').show();
							}

							$('#evuglaettungakt').change(function(){
								if($('#evuglaettungakt').val() == '0') {
									$('#evuglaettungdiv').hide();
								} else {
									$('#evuglaettungdiv').show();
								}
							});
						});

						function enable_pv_selector() {
							// enable das Dropdown-Element zur Auswahl des PV-Moduls
							document.getElementById("pvwattmodul").disabled=false;
						}

						function disable_pv_selector() {
							// disable das Dropdown-Element zur Auswahl des PV-Moduls
							document.getElementById("pvwattmodul").disabled=true;
						}

						function display_wattbezugmodul() {
							$('#wattbezugvz').hide();
							$('#wattbezugsdm').hide();
							$('#wattbezugnone').hide();
							$('#wattbezughttp').hide();
							$('#wattbezugsma').hide();
							$('#wattbezugsolarworld').hide();
							$('#wattbezugfronius').hide();
							$('#wattbezugjson').hide();
							$('#wattbezugmpm3pm').hide();
							$('#wattbezugsolarlog').hide();
							$('#wattbezugsolaredge').hide();
							$('#wattbezugshm').hide();
							$('#wattbezugsmartme').hide();
							$('#wattbezugsbs25').hide();
							$('#wattbezuge3dc').hide();
							$('#wattbezugethmpm3pm').hide();
							$('#wattbezugplentihaus').hide();
							$('#wattbezugkostalpiko').hide();
							$('#wattbezugkostalsmartenergymeter').hide();
							$('#wattbezugsmartfox').hide();
							$('#wattbezugpowerwall').hide();
							$('#wattbezugvictrongx').hide();
							$('#wattbezugsolarview').hide();
							$('#wattbezugdiscovergy').hide();
							$('#wattbezuglgessv1').hide();
							$('#wattbezugmqtt').hide();
							$('#wattbezugsonneneco').hide();
							$('#wattbezugfems').hide();
							$('#wattbezugsiemens').hide();
							$('#wattbezugip').hide();

							// Auswahl PV-Modul generell erlauben
							enable_pv_selector();
							if($('#wattbezugmodul').val() == 'bezug_sonneneco') {
								$('#wattbezugsonneneco').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_siemens') {
								$('#wattbezugsiemens').show();
								$('#wattbezugip').show();

							}

							if($('#wattbezugmodul').val() == 'bezug_fems') {
								$('#wattbezugfems').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_solarworld') {
								$('#wattbezugsolarworld').show();
							}

							if($('#wattbezugmodul').val() == 'bezug_solarview') {
								$('#wattbezugsolarview').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_discovergy') {
								$('#wattbezugdiscovergy').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_mqtt') {
								$('#wattbezugmqtt').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_victrongx') {
								$('#wattbezugvictrongx').show();
							}
							if($('#wattbezugmodul').val() == 'vzlogger') {
								$('#wattbezugvz').show();
							}
							if($('#wattbezugmodul').val() == 'sdm630modbusbezug')   {
								$('#wattbezugsdm').show();
							}
							if($('#wattbezugmodul').val() == 'none')   {
								$('#wattbezugnone').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_http')   {
								$('#wattbezughttp').show();
							}
							if($('#wattbezugmodul').val() == 'smaemd_bezug')   {
						 		$('#wattbezugsma').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_fronius_sm')   {
								$('#wattbezugfronius').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_fronius_s0')   {
								$('#wattbezugfronius').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_json')   {
								$('#wattbezugjson').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_mpm3pm')   {
								$('#wattbezugmpm3pm').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_solarlog')   {
								$('#wattbezugsolarlog').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_solaredge')   {
								$('#wattbezugsolaredge').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_smashm')   {
								$('#wattbezugshm').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_smartme')   {
								$('#wattbezugsmartme').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_e3dc')   {
								$('#wattbezuge3dc').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_ethmpm3pm')   {
								$('#wattbezugethmpm3pm').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_sbs25')   {
								$('#wattbezugsbs25').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_kostalplenticoreem300haus')   {
								$('#wattbezugplentihaus').show();
								// keine Auswahl PV-Modul in dieser Konfiguration
								// Plenticore immer fix auswählen
								document.getElementById('pvwattmodul').value = 'wr_plenticore';
								// und Einstellung sperren
								disable_pv_selector();
								display_pvwattmodul();
								// passendes Speichermodul 'optisch' voreinstellen, da automatisch alle Werte
								// mit aus dem WR gelesen werden
								//document.getElementById('speichermodul').value = 'speicher_kostalplenticore';
								//display_speichermodul();
							}
							if($('#wattbezugmodul').val() == 'bezug_kostalpiko')   {
								$('#wattbezugkostalpiko').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_ksem')   {
                                                                $('#wattbezugkostalsmartenergymeter').show();
                                                        }
							if($('#wattbezugmodul').val() == 'bezug_smartfox')   {
								$('#wattbezugsmartfox').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_powerwall')   {
								$('#wattbezugpowerwall').show();
							}
							if($('#wattbezugmodul').val() == 'bezug_lgessv1')   {
								$('#wattbezuglgessv1').show();
							}
						}

						$(function() {
							display_wattbezugmodul();
							$('#wattbezugmodul').change( function(){
								display_wattbezugmodul();
							});
						});
					</script>

					<div class="row">
						<h3> PV-Modul </h3>
					</div>
					<div class="row">
						<b><label for="pvwattmodul">PV-Modul:</label></b>
						<select name="pvwattmodul" id="pvwattmodul">
							<option <?php if($pvwattmodulold == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
							<option <?php if($pvwattmodulold == "wr_ethmpm3pmaevu\n") echo "selected" ?> value="wr_ethmpm3pmaevu">MPM3PM an openWB EVU Kit</option>
							<option <?php if($pvwattmodulold == "wr_ethsdm120\n") echo "selected" ?> value="wr_ethsdm120">SDM120 an openWB Modbus Lan Konverter</option>
							<option <?php if($pvwattmodulold == "wr_fronius\n") echo "selected" ?> value="wr_fronius">Fronius WR</option>
							<option <?php if($pvwattmodulold == "sdm630modbuswr\n") echo "selected" ?> value="sdm630modbuswr">SDM 630 Modbus</option>
							<option <?php if($pvwattmodulold == "vzloggerpv\n") echo "selected" ?> value="vzloggerpv">VZLogger</option>
							<option <?php if($pvwattmodulold == "wr_http\n") echo "selected" ?> value="wr_http">WR mit URL abfragen</option>
							<option <?php if($pvwattmodulold == "smaemd_pv\n") echo "selected" ?> value="smaemd_pv">SMA Energy Meter</option>
							<option <?php if($pvwattmodulold == "wr_json\n") echo "selected" ?> value="wr_json">WR mit Json abfragen</option>
							<option <?php if($pvwattmodulold == "mpm3pmpv\n") echo "selected" ?> value="mpm3pmpv">MPM3PM </option>
							<option <?php if($pvwattmodulold == "wr_kostalpiko\n") echo "selected" ?> value="wr_kostalpiko">Kostal Piko</option>
							<option <?php if($pvwattmodulold == "wr_solaredge\n") echo "selected" ?> value="wr_solaredge">SolarEdge WR</option>
							<option <?php if($pvwattmodulold == "wr_smartme\n") echo "selected" ?> value="wr_smartme">SmartMe</option>
							<option <?php if($pvwattmodulold == "wr_tripower9000\n") echo "selected" ?> value="wr_tripower9000">SMA ModbusTCP WR</option>
							<option <?php if($pvwattmodulold == "wr_plenticore\n") echo "selected" ?> value="wr_plenticore">Kostal Plenticore</option>
							<option <?php if($pvwattmodulold == "wr_solarlog\n") echo "selected" ?> value="wr_solarlog">SolarLog</option>
							<option <?php if($pvwattmodulold == "wr_kostalpikovar2\n") echo "selected" ?> value="wr_kostalpikovar2">Kostal Piko alt</option>
							<option <?php if($pvwattmodulold == "wr_powerwall\n") echo "selected" ?> value="wr_powerwall">Tesla Powerwall</option>
							<option <?php if($pvwattmodulold == "wr_solarview\n") echo "selected" ?> value="wr_solarview">Solarview</option>
							<option <?php if($pvwattmodulold == "wr_discovergy\n") echo "selected" ?> value="wr_discovergy">Discovergy</option>
							<option <?php if($pvwattmodulold == "wr_youless120\n") echo "selected" ?> value="wr_youless120">Youless 120</option>
							<option <?php if($pvwattmodulold == "wr_lgessv1\n") echo "selected" ?> value="wr_lgessv1">LG ESS 1.0VI</option>
							<option <?php if($pvwattmodulold == "wr_mqtt\n") echo "selected" ?> value="wr_mqtt">MQTT</option>
							<option <?php if($pvwattmodulold == "wr_sunways\n") echo "selected" ?> value="wr_sunways">Sunways</option>
							<option <?php if($pvwattmodulold == "wr_fems\n") echo "selected" ?> value="wr_fems">Fenecon FEMS</option>
							<option <?php if($pvwattmodulold == "wr_solarworld\n") echo "selected" ?> value="wr_solarworld">Solarworld</option>
							<option <?php if($pvwattmodulold == "wr_siemens\n") echo "selected" ?> value="wr_siemens">Siemens Speicher</option>
						</select>
					</div>

					<div id="pvnone">
					</div>
					<div id="pvmqtt">
							<div class="row">Keine Konfiguration erforderlich</div>
							<div class="row">Per MQTT zu schreiben:</div>
							<div class="row"><b>"openWB/set/pv/W"</b></div>
							<div class="row">PVleistung in Watt, int, negativ</div>
							<div class="row"><b>"openWB/set/pv/WhCounter"</b></div>
							<div class="row">Erzeugte Energie in Wh, float, nur positiv</div>
					</div>
					<div id="pvlgessv1">
						<div class="row">
							Konfiguration im zugehörigen Speichermodul des LG ESS 1.0VI erforderlich. Als PV-Modul auch LG ESS 1.0VI wählen!
						</div>
					</div>
					<div id="pvip">
						<div class="row" style="background-color:#febebe">
							<b><label for="pv1_ipa">IP Adresse:</label></b>
							<input type="text" name="pv1_ipa" id="pv1_ipa" value="<?php echo htmlspecialchars($pv1_ipaold) ?>">
						</div>
					</div>

					<div id="pvsiemens">
						<div class="row">
							IP Adresse des Siemens Speichers.
						</div>
					</div>

					<div id="pvfems">
						<div class="row">
							Konfiguration im zugehörigen EVU Modul des FEMS erforderlich.
						</div>
					</div>
					<div id="pvsolarworld">
						<div class="row">
							Konfiguration im zugehörigen EVU Modul des Solarworld erforderlich.
						</div>
					</div>

					<div id="pvyouless">
						<div class="row" style="background-color:#febebe">
							<b><label for="wryoulessip">IP Adresse des Youless</label></b>
							<input type="text" name="wryoulessip" id="wryoulessip" value="<?php echo htmlspecialchars($wryoulessipold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP.
						</div>
					</div>
					<div id="pvsunways">
						<div class="row" style="background-color:#febebe">
							<b><label for="wrsunwaysip">IP Adresse des Sunways</label></b>
							<input type="text" name="wrsunwaysip" id="wrsunwaysip" value="<?php echo htmlspecialchars($wrsunwaysipold) ?>"><br>
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP. <br>
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="wrsunwayspw">Passwort des Sunways</label></b>
							<input type="text" name="wrsunwayspw" id="wrsunwayspw" value="<?php echo htmlspecialchars($wrsunwayspwold) ?>"><br>
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte Passwort. <br>
						</div>

					</div>

					<div id="pvsolarlog">
						<div class="row" style="background-color:#febebe">
							<b><label for="bezug_solarlog_ip">IP Adresse des SolarLog</label></b>
							<input type="text" name="bezug_solarlog_ip" id="bezug_solarlog_ip" value="<?php echo htmlspecialchars($bezug_solarlog_ipold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte IP. Wenn ein Eigenverbrauchszähler installiert ist bitte EVU SolarLog Modul nutzen. Wenn nicht dann dieses Modul.
						</div>
					</div>
					<div id="pvdiscovergy">
						<div class="row" style="background-color:#febebe">
							<b><label for="discovergypvid">Meter ID des Zählers</label></b>
							<input type="text" name="discovergypvid" id="discovergypvid" value="<?php echo htmlspecialchars($discovergypvidold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte ID. Um die ID herauszufinden mit dem Browser die Adresse "https://api.discovergy.com/public/v1/meters" aufrufen und dort Benutzername und Passwort eingeben. Hier wird nun u.a. die ID des Zählers angezeigt.<br>
							Die Benutzerdaten werden im Discovergy EVU Modul konfiguriert.
						</div>
					</div>
					<div id="pvsolarview">
						<div class="row" style="background-color:#febebe">
							<b><label for="solarview_hostname">Hostname des SolarView TCP-Servers</label></b>
							<input type="text" name="solarview_hostname" id="solarview_hostname" value="<?php echo htmlspecialchars($solarview_hostnameold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte Hostname oder IP-Adresse.
						</div>
						<div class="row" style="background-color:#febebe">
							<b><label for="solarview_port">Port des Solarview TCP-Servers</label></b>
							<input type="text" name="solarview_port" id="solarview_port" value="<?php echo htmlspecialchars($solarview_portold) ?>">
						</div>
						<div class="row" style="background-color:#febebe">
							Gültige Werte Port, z.B. 15000.
						</div>
					</div>
					<div id="pvpowerwall">
						<div class="row" style="background-color:#febebe">
							Keine Einstellung nötig. Die IP wird im Speichermodul konfiguriert
						</div>
					</div>
					<div id="pvmpmevu">
						<div class="row" style="background-color:#febebe">
							<b><label for="pvkitversion">Version des openWB PV Kits:</label></b>
							<select name="pvkitversion" id="pvkitversion">
								<option <?php if($pvkitversionold == 0) echo "selected" ?> value="0">PV Kit</option>
								<option <?php if($pvkitversionold == 1) echo "selected" ?> value="1">PV Kit v2</option>
							</select>
						</div>
					</div>
					<div id="pvplenti">
						<div class="row" style="background-color:#befebe">
							<b><label for="kostalplenticoreip">IP Adresse des 1. Kostal Plenticore:</label></b>
							<input type="text" name="kostalplenticoreip" id="kostalplenticoreip" value="<?php echo $kostalplenticoreipold ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Gültige Werte: IP-Adresse des 1. Kostal Plenticore. An diesem muss (wenn vorhanden) der EM300/das KSEM und ggf. Speicher angeschlossen sein. Modbus/Sunspec (TCP) muss im WR aktiviert sein (Port 1502, Unit-ID 71).
						</div>
						<div class="row" style="background-color:#befebe">
							<b><label for="name_wechselrichter1">Bezeichnung des 1. Kostal Plenticore:</label></b>
							<input type="text" name="name_wechselrichter1" id="name_wechselrichter1" value="<?php echo $name_wechselrichter1old ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Gültige Werte: Freie Bezeichnung des Wechselrichters zu Anzeigezwecken, kann leer bleiben.
						</div>
						<div class="row" style="background-color:#befebe">
							<b><label for="kostalplenticoreip2">IP Adresse des 2. Kostal Plenticore:</label></b>
							<input type="text" name="kostalplenticoreip2" id="kostalplenticoreip2" value="<?php echo $kostalplenticoreip2old ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Gültige Werte: IP-Adresse des 2. Kostal Plenticore oder "none". An diesem WR darf kein Speicher angeschlossen sein. Wenn nur ein WR genutzt wird, muss der Wert "none" gesetzt werden, ansonsten muss Modbus/Sunspec (TCP) im WR aktiviert sein (Port 1502, Unit-ID 71).
						</div>
						<div class="row" style="background-color:#befebe">
							<b><label for="name_wechselrichter2">Bezeichnung des 2. Kostal Plenticore:</label></b>
							<input type="text" name="name_wechselrichter2" id="name_wechselrichter2" value="<?php echo $name_wechselrichter2old ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Gültige Werte: Freie Bezeichnung des zweiten Wechselrichters zu Anzeigezwecken, kann leer bleiben.
						</div>
					</div>
					<div id="pvsmartme">
						<div class="row" style="background-color:#befebe">
							<b><label for="wr_smartme_user">Smartme Benutzername</label></b>
							<input type="text" name="wr_smartme_user" id="wr_smartme_user" value="<?php echo htmlspecialchars($wr_smartme_userold) ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Smartme Benutzername
						</div>
						<div class="row" style="background-color:#befebe">
							<b><label for="wr_smartme_pass">Smartme Passwort</label></b>
							<input type="text" name="wr_smartme_pass" id="wr_smartme_pass" value="<?php echo htmlspecialchars($wr_smartme_passold) ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Smartme Passwort
						</div>
						<div class="row" style="background-color:#befebe">
							<b><label for="wr_smartme_url">Smartme Url</label></b>
							<input type="text" name="wr_smartme_url" id="wr_smartme_url" value="<?php echo htmlspecialchars($wr_smartme_urlold) ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Smartme Url
						</div>
					</div>
					<div id="pvpiko2">
						<div class="row" style="background-color:#befebe">
							<b><label for="wr_piko2_user">Benutzername</label></b>
							<input type="text" name="wr_piko2_user" id="wr_piko2_user" value="<?php echo htmlspecialchars($wr_piko2_userold) ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Piko Benutzername
						</div>
						<div class="row" style="background-color:#befebe">
							<b><label for="wr_piko2_pass">Passwort</label></b>
							<input type="text" name="wr_piko2_pass" id="wr_piko2_pass" value="<?php echo htmlspecialchars($wr_piko2_passold) ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Piko Passwort
						</div>
						<div class="row" style="background-color:#befebe">
							<b><label for="wr_piko2_url">Url</label></b>
							<input type="text" name="wr_piko2_url" id="wr_piko2_url" value="<?php echo htmlspecialchars($wr_piko2_urlold) ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Piko Url
						</div>
					</div>
					<div id="pvwrjson">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrjsonurl">WR URL:</label></b>
							<input type="text" name="wrjsonurl" id="wrjsonurl" value="<?php echo $wrjsonurlold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte URL. Vollständige URL die die Json Antwort enthält.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrjsonwatt">Json Abfrage für Watt:</label></b>
							<input type="text" name="wrjsonwatt" id="wrjsonwatt" value="<?php echo $wrjsonwattold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche.<br>
							Im Hintergrund wird der Befehl jq benutzt.<br>
							Ist die Json Antwort z.B."{"PowerInstalledPeak":4655,"PowerProduced":132,"PowerOut":897.08172362555717,"PowerSelfSupplied":234.9182763744428}" So muss hier - .PowerOut - ohne die - - eingetragen werden
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrjsonkwh">Json Abfrage für kWh:</label></b>
							<input type="text" name="wrjsonkwh" id="wrjsonkwh" value="<?php echo $wrjsonkwhold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche.<br>
							Im Hintergrund wird der Befehl jq benutzt.<br>
							Ist die Json Antwort z.B."{"PowerInstalledPeak":4655,"PowerProduced":132,"PowerOut":897.08172362555717,"PowerSelfSupplied":234.9182763744428}" So muss hier - .PowerProduced - ohne die - - eingetragen werden
						</div>
					</div>
					<div id="pvwrkostalpiko">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrfroniusip">WR Kostal Piko IP:</label></b>
							<input type="text" name="wrkostalpikoip" id="wrkostalpikoip" value="<?php echo $wrkostalpikoipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte IP. IP Adresse Kostal Wechselrichter.
						</div>
					</div>
					<div id="pvwrtri9000">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="tri9000ip">SMA WR IP:</label></b>
							<input type="text" name="tri9000ip" id="tri9000ip" value="<?php echo $tri9000ipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte: IPs. IP Adresse des SMA WR, ggf. muss der modbusTCP im WR noch aktiviert werden (normalerweise deaktiviert, entweder direkt am Wechselrichter, per Sunny Portal oder über das Tool "Sunny Explorer").
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrsmawebbox">Handelt es sich um eine SMA Webbox?:</label></b>
							<select name="wrsmawebbox" id="wrsmawebbox">
								<option <?php if($wrsmawebboxold == 0) echo "selected" ?> value="0">Nein</option>
								<option <?php if($wrsmawebboxold == 1) echo "selected" ?> value="1">Ja</option>
							</select>
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrsma2ip">WR 2 IP:</label></b>
							<input type="text" name="wrsma2ip" id="wrsma2ip" value="<?php echo $wrsma2ipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte: IP Adresse oder "none". IP des zweiten SMA Wechselrichters. Wenn nur ein WR genutzt wird, muss der Wert "none" gesetzt werden.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrsma3ip">WR 3 IP:</label></b>
							<input type="text" name="wrsma3ip" id="wrsma3ip" value="<?php echo $wrsma3ipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte: IP Adresse oder "none". IP des dritten SMA Wechselrichters. Wenn nur zwei WR genutzt werden, muss der Wert "none" gesetzt werden.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrsma4ip">WR 4 IP:</label></b>
							<input type="text" name="wrsma4ip" id="wrsma4ip" value="<?php echo $wrsma4ipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte: IP Adresse oder "none". IP des vierten SMA Wechselrichters. Wenn nur drei WR genutzt werden, muss der Wert "none" gesetzt werden.
						</div>
					</div>
					<div id="pvwrsolaredge">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="solaredgepvip">WR Solaredge IP:</label></b>
							<input type="text" name="solaredgepvip" id="solaredgepvip" value="<?php echo $solaredgepvipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte IP. IP Adresse des SolarEdge Wechselrichters.Modbus TCP muss am WR aktiviert werden, der Port ist auf 502 zu stellen.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="solaredgepvslave1">WR 1 Solaredge ID:</label></b>
							<input type="text" name="solaredgepvslave1" id="solaredgepvslave1" value="<?php echo $solaredgeipslave1old ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte Zahl. ID des SolarEdge Wechselrichters. Normalerweise 1.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="solaredgepvslave2">WR 2 Solaredge ID:</label></b>
							<input type="text" name="solaredgepvslave2" id="solaredgepvslave2" value="<?php echo $solaredgeipslave2old ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte Zahl oder none. ID des zweiten SolarEdge Wechselrichters. Wenn nur ein WR genutzt wird auf none setzen.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="solaredgepvslave3">WR 3 Solaredge ID:</label></b>
							<input type="text" name="solaredgepvslave3" id="solaredgepvslave3" value="<?php echo $solaredgeipslave3old ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte Zahl oder none. ID des dritten SolarEdge Wechselrichters. Wenn nur ein oder zwei WRs genutzt werden auf none setzen.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="solaredgewr2ip">WR 2 Solaredge IP:</label></b>
							<input type="text" name="solaredgewr2ip" id="solaredgewr2ip" value="<?php echo $solaredgewr2ipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte IP oder none. IP des zweiten SolarEdge Wechselrichters. Ist nur nötig wenn 2 Wechselrichter genutzt werden die nicht per Modbus miteinander verbunden sind.
						</div>
					</div>
					<div id="pvwrfronius">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrfroniusip">WR Fronius IP:</label></b>
							<input type="text" name="wrfroniusip" id="wrfroniusip" value="<?php echo $wrfroniusipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte IP. IP Adresse des Fronius Wechselrichters. Werden hier und im Feld unten zwei verschiedene Adressen eingetragen, muss hier die Adresse des Wechselrichters stehen, an dem das SmartMeter angeschlossen ist.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wrfronius2ip">WR Fronius 2 IP:</label></b>
							<input type="text" name="wrfronius2ip" id="wrfronius2ip" value="<?php echo $wrfronius2ipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte IP. IP Adresse des zweiten Fronius Wechselrichters. Sind nur Symos in Nutzung, welche über Fronius Solar Net / DATCOM miteinander verbunden sind, reicht die Angabe der Adresse eines Wechselrichters im ersten Feld. Sind aber z.B. Symo und Symo Hybrid im Einsatz, müssen diese beide angegeben werden (hier dann die Adresse des Wechselrichters, an dem das SmartMeter NICHT angeschlossen ist). Ist kein zweiter Wechselrichter vorhanden, dann bitte hier "none" eintragen.
						</div>
					</div>
					<div id="pvmpm3pm">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="mpm3pmpvsource">MPM3PM Wechselrichterleistung Source:</label></b>
							<input type="text" name="mpm3pmpvsource" id="mpm3pmpvsource" value="<?php echo $mpm3pmpvsourceold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM angeschlossen ist. Meist /dev/ttyUSB0<br>
							Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="mpm3pmpvid">MPM3PM Wechselrichterleistung ID:</label></b>
							<input type="text" name="mpm3pmpvid" id="mpm3pmpvid" value="<?php echo $mpm3pmpvidold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte 1-254. Modbus ID des MPM3PM.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="mpm3pmpvlanip">IP des Modbus/Lan Konverter:</label></b>
							<input type="text" name="mpm3pmpvlanip" id="mpm3pmpvlanip" value="<?php echo $mpm3pmpvlanipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt, ansonsten irrelevant.
						</div>
					</div>
					<div id="pvethsdm120">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wr_sdm120ip">SDM Modbus IP Adresse:</label></b>
							<input type="text" name="wr_sdm120ip" id="wr_sdm120ip" value="<?php echo $wr_sdm120ipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte IP. IP Adresse des ModbusLAN Konverters.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wr_sdm120id">SDM Modbus ID:</label></b>
							<input type="text" name="wr_sdm120id" id="wr_sdm120id" value="<?php echo $wr_sdm120idold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte 1-254. Modbus ID des SDM.
						</div>
					</div>
					<div id="pvsdmwr">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="sdm630modbuswrsource">SDM Modbus Wechselrichterleistung Source:</label></b>
							<input type="text" name="sdm630modbuswrsource" id="sdm630modbuswrsource" value="<?php echo $sdm630modbuswrsourceold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der SDM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
							Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="sdm630modbuswrid">SDM Modbus Wechselrichterleistung ID:</label></b>
							<input type="text" name="sdm630modbuswrid" id="sdm630modbuswrid" value="<?php echo $sdm630modbuswridold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte 1-254. Modbus ID des SDM. Getestet SDM230 & SDM630v2.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="sdm630modbuswrlanip">IP des Modbus/Lan Konverter:</label></b>
							<input type="text" name="sdm630modbuswrlanip" id="sdm630modbuswrlanip" value="<?php echo $sdm630modbuswrlanipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt.
						</div>
					</div>
					<div id="pvvzl">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="vzloggerpvip">Vzloggerpv IP Adresse inkl Port:</label></b>
							<input type="text" name="vzloggerpvip" id="vzloggerpvip" value="<?php echo $vzloggerpvipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte IP:Port z.B. 192.168.0.12:8080.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="vzloggerpvline">Vzloggerpv Zeile:</label></b>
							<input type="text" name="vzloggerpvline" id="vzloggerpvline" value="<?php echo $vzloggerpvlineold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br>
							Nun zählen in welcher Zeile der gewünschte Wert steht und diesen hier eintragen.
						</div>
					</div>
					<div id="pvhttp">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wr_http_w_url">Vollständige URL für die Wechselrichter Watt</label></b>
							<input type="text" name="wr_http_w_url" id="wr_http_w_url" value="<?php echo htmlspecialchars($wr_http_w_urlold) ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als wird der Wert auf null gesetzt. Der Wert muss in Watt sein.
						</div>
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="wr_http_kwh_url">Vollständige URL für die Wechselrichter absolut kWh</label></b>
							<input type="text" name="wr_http_kwh_url" id="wr_http_kwh_url" value="<?php echo htmlspecialchars($wr_http_kwh_urlold) ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Der Wert muss in WattStunden sein. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
						</div>
					</div>
					<div id="pvsma">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="smaemdpvid">Seriennummer des SMA Energy Meter</label></b>
							<input type="text" name="smaemdpvid" id="smaemdpvid" value="<?php echo $smaemdpvidold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte Seriennummer. Hier die Seriennummer des SMA Meter für die PV angeben.

						</div>
					</div>

					<script>
						function display_pvwattmodul() {
							$('#pvvzl').hide();
							$('#pvsdmwr').hide();
							$('#pvwrfronius').hide();
							$('#pvnone').hide();
							$('#pvhttp').hide();
							$('#pvsma').hide();
							$('#pvwrjson').hide();
							$('#pvmpm3pm').hide();
							$('#pvwrkostalpiko').hide();
							$('#pvwrsolaredge').hide();
							$('#pvsmartme').hide();
							$('#pvwrtri9000').hide();
							$('#pvplenti').hide();
							$('#pvsolarlog').hide();
							$('#pvpiko2').hide();
							$('#pvpowerwall').hide();
							$('#pvmpmevu').hide();
							$('#pvethsdm120').hide();
							$('#pvsolarview').hide();
							$('#pvdiscovergy').hide();
							$('#pvyouless').hide();
							$('#pvlgessv1').hide();
							$('#pvmqtt').hide();
							$('#pvsunways').hide();
							$('#pvfems').hide();
							$('#pvsolarworld').hide();
							$('#pvip').hide();
							$('#pvsiemens').hide();
							if($('#pvwattmodul').val() == 'wr_siemens') {
								$('#pvip').show();
								$('#pvsiemens').show();
							}
							if($('#pvwattmodul').val() == 'wr_fems') {
								$('#pvfems').show();
							}
							if($('#pvwattmodul').val() == 'wr_solarworld') {
								$('#pvsolarworld').show();
							}

							if($('#pvwattmodul').val() == 'wr_sunways') {
								$('#pvsunways').show();
							}

							if($('#pvwattmodul').val() == 'wr_mqtt') {
								$('#pvmqtt').show();
							}
							if($('#pvwattmodul').val() == 'wr_youless120') {
								$('#pvyouless').show();
							}
							if($('#pvwattmodul').val() == 'wr_solarview') {
								$('#pvsolarview').show();
							}
							if($('#pvwattmodul').val() == 'wr_discovergy') {
								$('#pvdiscovergy').show();
							}
							if($('#pvwattmodul').val() == 'wr_ethsdm120') {
								$('#pvethsdm120').show();
							}
							if($('#pvwattmodul').val() == 'wr_ethmpm3pmaevu') {
								$('#pvmpmevu').show();
							}
							if($('#pvwattmodul').val() == 'vzloggerpv') {
								$('#pvvzl').show();
							}
							if($('#pvwattmodul').val() == 'sdm630modbuswr')   {
								$('#pvsdmwr').show();
							}
							if($('#pvwattmodul').val() == 'wr_fronius')   {
								$('#pvwrfronius').show();
							}
							if($('#pvwattmodul').val() == 'none')   {
								$('#pvnone').show();
							}
							if($('#pvwattmodul').val() == 'wr_http')   {
								$('#pvhttp').show();
							}
							if($('#pvwattmodul').val() == 'smaemd_pv')   {
								$('#pvsma').show();
							}
							if($('#pvwattmodul').val() == 'wr_json')   {
								$('#pvwrjson').show();
							}
							if($('#pvwattmodul').val() == 'mpm3pmpv')   {
								$('#pvmpm3pm').show();
							}
							if($('#pvwattmodul').val() == 'wr_kostalpiko')   {
								$('#pvwrkostalpiko').show();
							}
							if($('#pvwattmodul').val() == 'wr_solaredge')   {
								$('#pvwrsolaredge').show();
							}
							if($('#pvwattmodul').val() == 'wr_smartme')   {
								$('#pvsmartme').show();
							}
							if($('#pvwattmodul').val() == 'wr_tripower9000')   {
								$('#pvwrtri9000').show();
							}
							if($('#pvwattmodul').val() == 'wr_plenticore')   {
								$('#pvplenti').show();
							}
							if($('#pvwattmodul').val() == 'wr_solarlog')   {
								$('#pvsolarlog').show();
							}
							if($('#pvwattmodul').val() == 'wr_kostalpikovar2')   {
								$('#pvpiko2').show();
							}
							if($('#pvwattmodul').val() == 'wr_powerwall')   {
								$('#pvpowerwall').show();
							}
							if($('#pvwattmodul').val() == 'wr_lgessv1')   {
								$('#pvlgessv1').show();
							}
						}

						$(function() {
							display_pvwattmodul();
							$('#pvwattmodul').change( function(){
								display_pvwattmodul();
							} );
						});
					</script>

					<div class="row">
						<h3> Zweites PV-Modul </h3>
					</div>
					<div class="row">
						<b><label for="pv2wattmodul">Zweites PV-Modul:</label></b>
						<select name="pv2wattmodul" id="pv2wattmodul">
							<option <?php if($pv2wattmodulold == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
							<option <?php if($pv2wattmodulold == "wr2_ethlovatoaevu\n") echo "selected" ?> value="wr2_ethlovatoaevu">Lovato an openWB EVU Kit</option>
							<option <?php if($pv2wattmodulold == "wr2_ethlovato\n") echo "selected" ?> value="wr2_ethlovato">openWB PV Kit v2</option>
							<option <?php if($pv2wattmodulold == "wr2_smamodbus\n") echo "selected" ?> value="wr2_smamodbus">SMA Wechselrichter</option>
							<option <?php if($pv2wattmodulold == "wr2_kostalsteca\n") echo "selected" ?> value="wr2_kostalsteca">Kostal Piko MP oder Steca Grid Coolcept</option>
							<option <?php if($pv2wattmodulold == "wr2_victron\n") echo "selected" ?> value="wr2_victron">Victron MPPT</option>

						</select>
					</div>

					<div id="pv2none">
					</div>
					<div id="pv2noconfig">
						Keine Konfiguration erforderlich.
					</div>
					<div id="pv2ipdiv">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="pv2ip">Wechselrichter IP:</label></b>
							<input type="text" name="pv2ip" id="pv2ip" value="<?php echo $pv2ipold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte: IPs. IP Adresse des Wechselrichters, ggf. muss modbusTCP im WR noch aktiviert werden.
						</div>
					</div>
					<div id="pv2iddiv">
						<div class="row" style="background-color:#BEFEBE">
							<b><label for="pv2id">Modbus ID:</label></b>
							<input type="text" name="pv2id" id="pv2id" value="<?php echo $pv2idold ?>">
						</div>
						<div class="row" style="background-color:#BEFEBE">
							Gültige Werte: ID. 
						</div>
					</div>

					<script>
						function display_pv2wattmodul() {
							$('#pv2none').hide();
							$('#pv2noconfig').hide();
							$('#pv2ipdiv').hide();
							$('#pv2iddiv').hide();

							if($('#pv2wattmodul').val() == 'none') {
								$('#pv2none').show();
							}
							if($('#pv2wattmodul').val() == 'wr2_ethlovatoaevu') {
								$('#pv2noconfig').show();
							}
							if($('#pv2wattmodul').val() == 'wr2_ethlovato') {
								$('#pv2noconfig').show();
							}
							if($('#pv2wattmodul').val() == 'wr2_smamodbus') {
								$('#pv2ipdiv').show();
							}
							if($('#pv2wattmodul').val() == 'wr2_kostalsteca') {
								$('#pv2ipdiv').show();
							}
							if($('#pv2wattmodul').val() == 'wr2_victron') {
								$('#pv2ipdiv').show();
								$('#pv2iddiv').show();
							}

						}
						$(function() {
							display_pv2wattmodul();
							$('#pv2wattmodul').change( function(){
								display_pv2wattmodul();
							} );
						});
					</script>
					<div class="row">
						<h3> Speicher-Modul </h3>
					</div>
					<div class="row">
						<b><label for="speichermodul">Speicher-Modul:</label></b>
						<select name="speichermodul" id="speichermodul">
							<option <?php if($speichermodulold == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
							<option <?php if($speichermodulold == "speicher_mpm3pm\n") echo "selected" ?> value="speicher_mpm3pm">openWB Speicher Kit</option>
							<option <?php if($speichermodulold == "speicher_http\n") echo "selected" ?> value="speicher_http">HTTP Abfrage</option>
							<option <?php if($speichermodulold == "mpm3pmspeicher\n") echo "selected" ?> value="mpm3pmspeicher">MPM3PM</option>
							<option <?php if($speichermodulold == "speicher_bydhv\n") echo "selected" ?> value="speicher_bydhv">ByD HV</option>
							<option <?php if($speichermodulold == "speicher_fronius\n") echo "selected" ?> value="speicher_fronius">Fronius Speicher</option>
							<option <?php if($speichermodulold == "speicher_e3dc\n") echo "selected" ?> value="speicher_e3dc">E3DC Speicher</option>
							<option <?php if($speichermodulold == "speicher_sbs25\n") echo "selected" ?> value="speicher_sbs25">SMA Sunny Boy Storage</option>
							<option <?php if($speichermodulold == "speicher_solaredge\n") echo "selected" ?> value="speicher_solaredge">Solaredge Speicher</option>
							<option <?php if($speichermodulold == "speicher_powerwall\n") echo "selected" ?> value="speicher_powerwall">Tesla Powerwall</option>
							<option <?php if($speichermodulold == "speicher_kostalplenticore\n") echo "selected" ?> value="speicher_kostalplenticore">Kostal Plenticore mit Speicher</option>
							<option <?php if($speichermodulold == "speicher_sunnyisland\n") echo "selected" ?> value="speicher_sunnyisland">SMA Sunny Island</option>
							<option <?php if($speichermodulold == "speicher_sonneneco\n") echo "selected" ?> value="speicher_sonneneco">Sonnen eco</option>
							<option <?php if($speichermodulold == "speicher_varta\n") echo "selected" ?> value="speicher_varta">Varta Element u.a.</option>
							<option <?php if($speichermodulold == "speicher_alphaess\n") echo "selected" ?> value="speicher_alphaess">Alpha ESS</option>
							<option <?php if($speichermodulold == "speicher_victron\n") echo "selected" ?> value="speicher_victron">Victron Speicher (GX o.ä.)</option>
							<option <?php if($speichermodulold == "speicher_lgessv1\n") echo "selected" ?> value="speicher_lgessv1">LG ESS 1.0VI</option>
							<option <?php if($speichermodulold == "speicher_mqtt\n") echo "selected" ?> value="speicher_mqtt">MQTT</option>
							<option <?php if($speichermodulold == "speicher_fems\n") echo "selected" ?> value="speicher_fems">Fenecon FEMS</option>
							<option <?php if($speichermodulold == "speicher_siemens\n") echo "selected" ?> value="speicher_siemens">Siemens</option>
						</select>
					</div>

					<div id="divspeicherlgessv1">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="lgessv1ip">LG ESS 1.0VI IP:</label></b>
							<input type="text" name="lgessv1ip" id="lgessv1ip" value="<?php echo $lgessv1ipold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte IP. IP-Adresse des LG ESS 1.0VI
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="lgessv1pass">LG ESS 1.0VI Passwort:</label></b>
							<input type="text" name="lgessv1pass" id="lgessv1pass" value="<?php echo $lgessv1passold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Standardmäßig ist hier die Registrierungsnummer des LG ESS 1.0VI anzugeben
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b>Bitte die API-Version wählen:</b><br />
							<select name="ess_api_ver" id="ess_api_ver">
								<option <?php if($ess_api_ver_old == "10.2019\n") echo "selected" ?> value="10.2019">API-Version Oktober 2019</option>
								<option <?php if($ess_api_ver_old == "01.2020\n") echo "selected" ?> value="01.2020">API-Version Januar 2020</option>
							</select><br />
							Falls Sie nicht wissen, welche API-Version benötigen, benutzten Sie bitte die neueste API-Version<br />
						</div>
					</div>
					<div id="divspeichernone">
					</div>
					<div id="divspeicherkit">
							<div class="row" style="background-color:#fcbe1e">
							Keine Konfiguration erforderlich
						</div>
					</div>
					<div id="divspeichermqtt">
						<div class="row" style="background-color:#fcbe1e">Keine Konfiguration erforderlich</div>
						<div class="row" style="background-color:#fcbe1e">Per MQTT zu schreiben:</div>
						<div class="row" style="background-color:#fcbe1e"><b>"openWB/set/HouseBattery/W"</b></div>
						<div class="row" style="background-color:#fcbe1e">Speicherleistung in Watt, int, positiv Ladung, negativ Entladung</div>
						<div class="row" style="background-color:#fcbe1e"><b>"openWB/set/HouseBattery/WhImported"</b></div>
						<div class="row" style="background-color:#fcbe1e">Geladene Energie in Wh, float, nur positiv</div>
						<div class="row" style="background-color:#fcbe1e"><b>"openWB/set/HouseBattery/WhExported"</b></div>
						<div class="row" style="background-color:#fcbe1e">Entladene Energie in Wh, float, nur positiv</div>
						<div class="row" style="background-color:#fcbe1e"><b>"openWB/set/HouseBattery/%Soc"</b></div>
						<div class="row" style="background-color:#fcbe1e">Ladestand des Speichers, int, 0-100</div>
					</div>
					<div id="divspeichervictron">
							<div class="row" style="background-color:#fcbe1e">
							Konfiguration im Bezug Victron Modul.
						</div>
					</div>
					<div id="divspeicherfems">
							<div class="row" style="background-color:#fcbe1e">
							Konfiguration im Bezug Fenecon Modul.
						</div>
					</div>
					<div id="divspeicherip">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="speicher1_ip">IP:</label></b>
							<input type="text" name="speicher1_ip" id="speicher1_ip" value="<?php echo $speicher1_ipold ?>">
						</div>
					</div>
					<div id="divspeichersiemens">
							<div class="row" style="background-color:#fcbe1e">
							IP Adresse des Siemens Speichers. Im Siemens Speicher muss als Schnittstelle openWB gewählt werden.
						</div>
					</div>

					<div id="divspeichervarta">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="vartaspeicherip">Varta IP:</label></b>
							<input type="text" name="vartaspeicherip" id="vartaspeicherip" value="<?php echo $vartaspeicheripold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte IP. IP Adresse des Varta Speichers.
						</div>
					</div>
					<div id="divspeicheralphaess">

						<div class="row" style="background-color:#fcbe1e">
							Keine Konfiguration erforderlich
						</div>
					</div>
					<div id="divspeicherpw">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="speicherpwip">Powerwall IP:</label></b>
							<input type="text" name="speicherpwip" id="speicherpwip" value="<?php echo $speicherpwipold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte IP. IP Adresse der Tesla Powerwall.
						</div>
					</div>
					<div id="divspeicherseco">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="sonnenecoip">Sonnen eco IP:</label></b>
							<input type="text" name="sonnenecoip" id="sonnenecoip" value="<?php echo $sonnenecoipold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte IP. IP Adresse der Sonnen eco serie 5.
						</div>
						<b><label for="sonnenecoalternativ">Alternativ Auslesung:</label></b>
						<select name="sonnenecoalternativ" id="sonnenecoalternativ">
							<option <?php if($sonnenecoalternativold == "0\n") echo "selected" ?> value="0">Nein</option>
							<option <?php if($sonnenecoalternativold == "1\n") echo "selected" ?> value="1">Ja</option>
							<option <?php if($sonnenecoalternativold == "2\n") echo "selected" ?> value="2">ECO 6</option>
						</select>
						<div class="row bg-info">
							Je nach Sonnen Batterie kann die Alternative Auslesung benötigt werden.
						</div>
					</div>
					<div id="divspeichere3dc">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="e3dcip">E3DCIP:</label></b>
							<input type="text" name="e3dcip" id="e3dcip" value="<?php echo $e3dcipold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte IP. IP Adresse des E3DC Speichers.
						</div>
						<b><label for="e3dcextprod">Externe Produktion des E3DC mit einbeziehen:</label></b>
						<select name="e3dcextprod" id="e3dcextprod">
							<option <?php if($e3dcextprodold == "0\n") echo "selected" ?> value="0">Nein</option>
							<option <?php if($e3dcextprodold == "1\n") echo "selected" ?> value="1">Ja</option>
						</select>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="e3dc2ip">E3DC 2 IP:</label></b>
							<input type="text" name="e3dc2ip" id="e3dc2ip" value="<?php echo $e3dc2ipold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte IP oder none. IP Adresse des zweiten E3DC Speichers. Wenn nicht vorhanden none eintragen.
						</div>
					</div>
					<div id="divspeichersbs25">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="sbs25ip">SBS IP:</label></b>
							<input type="text" name="sbs25ip" id="sbs25ip" value="<?php echo $sbs25ipold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte: IPs. IP Adresse des SMA Sunny Boy Storage Speichers.
						</div>
					</div>
					<div id="divspeichersunnyisland">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="sunnyislandip">Sunny Island IP:</label></b>
							<input type="text" name="sunnyislandip" id="sunnyislandip" value="<?php echo $sunnyislandipold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte IP. IP Adresse des SMA Sunny Island.
						</div>
					</div>
					<div id="divspeichersolaredge">
						<div class="row" style="background-color:#fcbe1e">
								<b><label for="solaredgespeicherip">Solaredge Speicher IP:</label></b>
							<input type="text" name="solaredgespeicherip" id="solaredgespeicherip" value="<?php echo htmlspecialchars($solaredgespeicheripold) ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte IP. IP Adresse des Solaredge Wechselrichters an dem der Speicher angeschlossen ist.
						</div>
					</div>
					<div id="divspeicherplenti">
						<div class="row" style="background-color:#fcbe1e">
							Ein am 1. Kostal Plenticore angeschlossener Speicher setzt einen EM300/KSEM voraus. Nach entsprechender Auswahl im Strombezugsmessmodul und Konfiguration der IP des WR im PV-Modul erfolgt das Auslesen des Speichers über den WR ohne weitere Einstellungen.
						</div>
					</div>
					<div id="divspeicherfronius">
						<div class="row" style="background-color:#fcbe1e">
							Die IP des Wechselrichters wird im dazugehörigen Fronius PV-Modul eingestellt.
						</div>
					</div>
					<div id="divspeicherhttp">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="speicherleistung_http">Speicherleistung URL:</label></b>
							<input type="text" name="speicherleistung_http" id="speicherleistung_http" value="<?php echo $speicherleistung_httpold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte URL. Vollständige URL die den aktuellen Leistungswert in Watt wiedergibt. Erwartet wird eine Ganzzahl. Positiv heißt Speicher wird geladen und eine negative Zahl bedeutet das der Speicher entladen wird. Das Modul dient dazu bei NurPV Ladung eine Entladung des Speichers zu verhindern.
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="speichersoc_http">SpeicherSoC URL:</label></b>
							<input type="text" name="speichersoc_http" id="speichersoc_http" value="<?php echo $speichersoc_httpold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte URL. Vollständige URL die den aktuellen SoC wiedergibt.
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="speicherikwh_http">Speicher Import Wh URL:</label></b>
							<input type="text" name="speicherikwh_http" id="speicherikwh_http" value="<?php echo $speicherikwh_httpold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte URL. Wenn nicht vorhanden, none eintragen. Vollständige URL die den Zählerstand der Batterieladung in WattStunden wiedergibt. Erwartet wird eine Ganzzahl.
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="speicherekwh_http">Speicher Export Wh URL:</label></b>
							<input type="text" name="speicherekwh_http" id="speicherekwh_http" value="<?php echo $speicherekwh_httpold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte URL. Wenn nicht vorhanden, none eintragen.  Vollständige URL die den Zählerstand der Batterieladung in WattStunden wiedergibt. Erwartet wird eine Ganzzahl.
						</div>
					</div>
					<div id="divspeicherbydhv">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="bydhvuser">Byd HV Benutzername:</label></b>
							<input type="text" name="bydhvuser" id="bydhvuser" value="<?php echo $bydhvuserold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Benutzername der ByD Batterie
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="bydhvpass">Byd HV Passwort:</label></b>
							<input type="text" name="bydhvpass" id="bydhvpass" value="<?php echo $bydhvpassold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Passwort der ByD Batterie
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="bydhvip">Byd HV IP Adresse:</label></b>
							<input type="text" name="bydhvip" id="bydhvip" value="<?php echo $bydhvipold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							IP Adresse der ByD Batterie
						</div>
					</div>
					<div id="divspeichermpm3pm">
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="mpm3pmspeichersource">Modbus Source:</label></b>
							<input type="text" name="mpm3pmspeichersource" id="mpm3pmspeichersource" value="<?php echo $mpm3pmspeichersourceold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte /dev/ttyUSBx , /dev/virtualcomX bei Verwendung mit Ethernet Modbus
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="mpm3pmspeicherid">Modbus ID:</label></b>
							<input type="text" name="mpm3pmspeicherid" id="mpm3pmspeicherid" value="<?php echo $mpm3pmspeicheridold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
							Gültige Werte Zahl.
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="mpm3pmspeicherpv">PV mit einberechnen?:</label></b>
							<select name="mpm3pmspeicherpv" id="mpm3pmspeicherpv">
								<option <?php if($mpm3pmspeicherpvold == "0\n") echo "selected" ?> value="0">Keine extra Berechnung</option>
								<option <?php if($mpm3pmspeicherpvold == "1\n") echo "selected" ?> value="1">Subtrahieren der PV Leistung</option>
							</select>
						</div>
						<div class="row" style="background-color:#fcbe1e">
							<b><label for="mpm3pmspeicherlanip">Lan Modbus Konverter IP:</label></b>
							<input type="text" name="mpm3pmspeicherlanip" id="mpm3pmspeicherlanip" value="<?php echo $mpm3pmspeicherlanipold ?>">
						</div>
						<div class="row" style="background-color:#fcbe1e">
						Gültige Werte eine IP Adresse.
						</div>
					</div>

					<script>
						function display_speichermodul() {
							$('#divspeichermqtt').hide();
							$('#divspeichernone').hide();
							$('#divspeicherhttp').hide();
							$('#divspeichermpm3pm').hide();
							$('#divspeicherbydhv').hide();
							$('#divspeicherfronius').hide();
							$('#divspeichere3dc').hide();
							$('#divspeichersbs25').hide();
							$('#divspeichersolaredge').hide();
							$('#divspeicherpw').hide();
							$('#divspeicherplenti').hide();
							$('#divspeichersunnyisland').hide();
							$('#divspeicherseco').hide();
							$('#divspeicherkit').hide();
							$('#divspeichervarta').hide();
							$('#divspeicheralphaess').hide();
							$('#divspeichervictron').hide();
							$('#divspeicherlgessv1').hide();
							$('#divspeicherfems').hide();
							$('#divspeicherip').hide();
							$('#divspeichersiemens').hide();

							if($('#speichermodul').val() == 'speicher_fems') {
								$('#divspeicherfems').show();
							}
							if($('#speichermodul').val() == 'speicher_siemens') {
								$('#divspeicherip').show();
								$('#divspeichersiemens').show();
							}

							if($('#speichermodul').val() == 'speicher_alphaess') {
								$('#divspeicheralphaess').show();
							}
							if($('#speichermodul').val() == 'speicher_mqtt') {
								$('#divspeichermqtt').show();
							}
							if($('#speichermodul').val() == 'speicher_victron') {
								$('#divspeichervictron').show();
							}
							if($('#speichermodul').val() == 'speicher_mpm3pm') {
								$('#divspeicherkit').show();
							}
							if($('#speichermodul').val() == 'speicher_sonneneco') {
								$('#divspeicherseco').show();
							}
							if($('#speichermodul').val() == 'none') {
								$('#divspeichernone').show();
							}
							if($('#speichermodul').val() == 'speicher_http')   {
								$('#divspeicherhttp').show();
							}
							if($('#speichermodul').val() == 'mpm3pmspeicher')   {
								$('#divspeichermpm3pm').show();
							}
							if($('#speichermodul').val() == 'speicher_bydhv')   {
								$('#divspeicherbydhv').show();
							}
							if($('#speichermodul').val() == 'speicher_fronius')   {
								$('#divspeicherfronius').show();
							}
							if($('#speichermodul').val() == 'speicher_e3dc')   {
								$('#divspeichere3dc').show();
							}
							if($('#speichermodul').val() == 'speicher_sbs25')   {
								$('#divspeichersbs25').show();
							}
							if($('#speichermodul').val() == 'speicher_solaredge')   {
								$('#divspeichersolaredge').show();
							}
							if($('#speichermodul').val() == 'speicher_varta')   {
								$('#divspeichervarta').show();
							}

							if($('#speichermodul').val() == 'speicher_powerwall')   {
								$('#divspeicherpw').show();
							}
							if($('#speichermodul').val() == 'speicher_kostalplenticore')   {
								$('#divspeicherplenti').show();
							}
							if($('#speichermodul').val() == 'speicher_sunnyisland')   {
								$('#divspeichersunnyisland').show();
							}
							if($('#speichermodul').val() == 'speicher_lgessv1')   {
								$('#divspeicherlgessv1').show();
							}
						}

						$(function() {
						display_speichermodul();
							$('#speichermodul').change( function(){
								display_speichermodul();
							});
						});
					</script>

					<button type="submit" class="btn btn-green" onclick="enable_pv_selector()">Save</button>
				</form>

				<div class="row justify-content-center">
					<div class="col text-center">
						Open Source made with love!<br>
						Jede Spende hilft die Weiterentwicklung von openWB voranzutreiben<br>
						<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
							<input type="hidden" name="cmd" value="_s-xclick">
							<input type="hidden" name="hosted_button_id" value="2K8C4Y2JTGH7U">
							<input type="image" src="./img/btn_donate_SM.gif" name="submit" alt="Jetzt einfach, schnell und sicher online bezahlen – mit PayPal.">
							<img alt="" src="./img/pixel.gif" width="1" height="1">
						</form>
					</div>
				</div>
			</div>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
			  <small>Sie befinden sich hier: Einstellungen/Modulkonfiguration</small>
			</div>
		</footer>


		<script type="text/javascript">

			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navModulkonfiguration').addClass('disabled');
			});

		</script>


</html>
