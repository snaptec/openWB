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

		<link rel="stylesheet" type="text/css" href="fonts/font-awesome-5.8.2/css/all.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<script>
			/**
			 * hideSection
			 * add class 'hide' to element with id 'section'
			 * disables all contained input and select elements if 'disableChildren' is not set to false
			**/
			function hideSection(section, disableChildren=true) {
				$('#'+section).addClass('hide');
				if (disableChildren) {
					$('#'+section).find('input').prop("disabled", true);
					$('#'+section).find('select').prop("disabled", true);
				}
			}

			/**
			 * showSection
			 * remove class 'hide' from element with id 'section'
			 * enables all contained input and select elements if 'enableChildren' is not set to false
			**/
			function showSection(section, enableChildren=true) {
				$('#'+section).removeClass('hide');
				if (enableChildren) {
					$('#'+section).find('input').prop("disabled", false);
					$('#'+section).find('select').prop("disabled", false);
				}
			}

			function getCookie(cname) {
				var name = cname + '=';
				var decodedCookie = decodeURIComponent(document.cookie);
				var ca = decodedCookie.split(';');
				for(var i = 0; i <ca.length; i++) {
					var c = ca[i];
					while (c.charAt(0) == ' ') {
						c = c.substring(1);
					}
					if (c.indexOf(name) == 0) {
						return c.substring(name.length, c.length);
					}
				}
				return '';
			}
			var themeCookie = getCookie('openWBTheme');
			// include special Theme style
			if( '' != themeCookie ){
				$('head').append('<link rel="stylesheet" href="themes/' + themeCookie + '/settings.css?v=20200801">');
			}
		</script>
	</head>

	<body>

		<?php

			$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
			foreach($lines as $line) {
				if(strpos($line, "socuser=") !== false) {
					list(, $socuserold) = explode("=", $line);
				}
				if(strpos($line, "socpass=") !== false) {
					list(, $socpassold) = explode("=", $line);
				}
				if(strpos($line, "soc2user=") !== false) {
					list(, $soc2userold) = explode("=", $line);
				}
				if(strpos($line, "soc2pass=") !== false) {
					list(, $soc2passold) = explode("=", $line);
				}
				if(strpos($line, "soc2pin=") !== false) {
					list(, $soc2pinold) = explode("=", $line);
				}
				if(strpos($line, "soclp1_vin=") !== false) {
					list(, $soclp1_vinold) = explode("=", $line);
				}
				if(strpos($line, "soclp2_vin=") !== false) {
					list(, $soclp2_vinold) = explode("=", $line);
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
				if(strpos($line, "soc_vin=") !== false) {
					list(, $soc_vinold) = explode("=", $line);
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
				if(strpos($line, "lastmanagementlp4=") !== false) {
					list(, $lastmanagementlp4old) = explode("=", $line);
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
				if(strpos($line, "chargep1cp=") !== false) {
				list(, $chargep1cpold) = explode("=", $line);
				}
				if(strpos($line, "chargep2cp=") !== false) {
					list(, $chargep2cpold) = explode("=", $line);
				}
				if(strpos($line, "chargep3cp=") !== false) {
					list(, $chargep3cpold) = explode("=", $line);
				}
				if(strpos($line, "chargep4cp=") !== false) {
					list(, $chargep4cpold) = explode("=", $line);
				}
				if(strpos($line, "chargep5cp=") !== false) {
					list(, $chargep5cpold) = explode("=", $line);
				}
				if(strpos($line, "chargep6cp=") !== false) {
					list(, $chargep6cpold) = explode("=", $line);
				}
				if(strpos($line, "chargep7cp=") !== false) {
					list(, $chargep7cpold) = explode("=", $line);
				}
				if(strpos($line, "chargep8cp=") !== false) {
					list(, $chargep8cpold) = explode("=", $line);
				}
				if(strpos($line, "chargep1ip=") !== false) {
				list(, $chargep1ipold) = explode("=", $line);
				}
				if(strpos($line, "chargep2ip=") !== false) {
					list(, $chargep2ipold) = explode("=", $line);
				}
				if(strpos($line, "chargep3ip=") !== false) {
					list(, $chargep3ipold) = explode("=", $line);
				}
				if(strpos($line, "chargep4ip=") !== false) {
					list(, $chargep4ipold) = explode("=", $line);
				}
				if(strpos($line, "chargep5ip=") !== false) {
					list(, $chargep5ipold) = explode("=", $line);
				}
				if(strpos($line, "chargep6ip=") !== false) {
					list(, $chargep6ipold) = explode("=", $line);
				}
				if(strpos($line, "chargep7ip=") !== false) {
					list(, $chargep7ipold) = explode("=", $line);
				}
				if(strpos($line, "chargep8ip=") !== false) {
					list(, $chargep8ipold) = explode("=", $line);
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
				if(strpos($line, "debug=") !== false) {
					list(, $debugold) = explode("=", $line);
				}
				if(strpos($line, "wakeupmyrenaultlp1=") !== false) {
					list(, $wakeupmyrenaultlp1old) = explode("=", $line);
				}
				if(strpos($line, "wakeupmyrenaultlp2=") !== false) {
					list(, $wakeupmyrenaultlp2old) = explode("=", $line);
				}
				if(strpos($line, "sdmids1=") !== false) {
					list(, $sdmids1old) = explode("=", $line);
				}
				if(strpos($line, "httpevseip=") !== false) {
					list(, $httpevseipold) = explode("=", $line);
				}
				if(strpos($line, "evsecon=") !== false) {
					list(, $evseconold) = explode("=", $line);
				}
				if(strpos($line, "evseconlp4=") !== false) {
					list(, $evseconlp4old) = explode("=", $line);
				}
				if(strpos($line, "evseconlp5=") !== false) {
					list(, $evseconlp5old) = explode("=", $line);
				}
				if(strpos($line, "evseconlp6=") !== false) {
					list(, $evseconlp6old) = explode("=", $line);
				}
				if(strpos($line, "evseconlp7=") !== false) {
					list(, $evseconlp7old) = explode("=", $line);
				}
				if(strpos($line, "evseconlp8=") !== false) {
					list(, $evseconlp8old) = explode("=", $line);
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
				if(strpos($line, "lastmanagements2=") !== false) {
					list(, $lastmanagements2old) = explode("=", $line);
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
				if(strpos($line, "ladeleistungs1modul=") !== false) {
					list(, $ladeleistungs1modulold) = explode("=", $line);
				}
				if(strpos($line, "smaemdllid=") !== false) {
					list(, $smaemdllidold) = explode("=", $line);
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
				if(strpos($line, "mpm3pmllid=") !== false) {
					list(, $mpm3pmllidold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmlls1id=") !== false) {
					list(, $mpm3pmlls1idold) = explode("=", $line);
				}
				if(strpos($line, "mpm3pmlls2id=") !== false) {
					list(, $mpm3pmlls2idold) = explode("=", $line);
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
				if(strpos($line, "lllaniplp2=") !== false) {
					list(, $lllaniplp2old) = explode("=", $line);
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
			}
			$twcmanagerlp1ipold = str_replace( "'", "", $twcmanagerlp1ipold);
			$httpevseipold = str_replace( "'", "", $httpevseipold);
			$httpll_kwh_urlold = str_replace( "'", "", $httpll_kwh_urlold);
			$httpll_w_urlold = str_replace( "'", "", $httpll_w_urlold);
			$httpll_a1_urlold = str_replace( "'", "", $httpll_a1_urlold);
			$httpll_a2_urlold = str_replace( "'", "", $httpll_a2_urlold);
			$httpll_a3_urlold = str_replace( "'", "", $httpll_a3_urlold);
			$hsocipold = str_replace( "'", "", $hsocipold);
			$carnetuserold = str_replace( "'", "", $carnetuserold);
			$carnetpassold = str_replace( "'", "", $carnetpassold);
			$socteslapwold = str_replace( "'", "", $socteslapwold);
			$socteslalp2pwold = str_replace( "'", "", $socteslalp2pwold);
			$carnetlp2userold = str_replace( "'", "", $carnetlp2userold);
			$carnetlp2passold = str_replace( "'", "", $carnetlp2passold);
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
			$socpassold = str_replace( "'", "", $socpassold);
			$soc2passold = str_replace( "'", "", $soc2passold);
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Modulkonfiguration</h1>
			<form action="./tools/debugrequest.php" method="POST">

				<!-- Ladepunkt 1 -->
				<div class="card border-primary">
					<div class="card-header bg-primary">
						Ladepunkt 1
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="lp1name" class="col-md-4 col-form-label">Name</label>
								<div class="col">
									<input class="form-control" type="text" name="lp1name" id="lp1name" value="<?php echo trim($lp1nameold) ?>">
								</div>
							</div>
						</div>
						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="evsecon" class="col-md-4 col-form-label">Anbindung</label>
							<div class="col">
								<select name="evsecon" id="evsecon" class="form-control">
									<option <?php if($evseconold == "modbusevse\n" && $ladeleistungmodulold == "mpm3pmll\n" && $mpm3pmllsourceold == "/dev/ttyUSB0\n" && $mpm3pmllidold == "5\n") echo "selected" ?> value="openwb12">openWB series1/2</option>
									<option <?php if($evseconold == "modbusevse\n" && $ladeleistungmodulold == "mpm3pmll\n" && $mpm3pmllsourceold == "/dev/ttyUSB0\n" && $mpm3pmllidold == "105\n") echo "selected" ?> value="openwb12mid">openWB series1/2 mit geeichtem Zähler</option>
									<option <?php if($evseconold == "modbusevse\n" && $ladeleistungmodulold == "mpm3pmll\n" && $mpm3pmllsourceold == "/dev/serial0\n" && $mpm3pmllidold == "105\n") echo "selected" ?> value="openwb12v2mid">openWB series1/2 mit geeichtem Zähler v2</option>
									<option <?php if($evseconold == "buchse\n") echo "selected" ?> value="buchse">openWB mit Buchse</option>
									<option <?php if($evseconold == "masterethframer\n") echo "selected" ?> value="masterethframer">openWB Ladepunkt in Verbindung mit Standalone</option>
									<option <?php if($evseconold == "ipevse\n") echo "selected" ?> value="ipevse">openWB Satellit </option>
									<option <?php if($evseconold == "extopenwb\n") echo "selected" ?> value="extopenwb">externe openWB</option>
									<option <?php if($evseconold == "dac\n") echo "selected" ?> value="dac">DAC</option>
									<option <?php if($evseconold == "httpevse\n") echo "selected" ?> value="httpevse">HTTP</option>
									<option <?php if($evseconold == "modbusevse\n" && !($ladeleistungmodulold == "mpm3pmll\n" && $mpm3pmllsourceold == "/dev/ttyUSB0\n" && ($mpm3pmllidold == "5\n" || $mpm3pmllidold == "105\n"))) echo "selected" ?> value="modbusevse">Modbusevse</option>
									<option <?php if($evseconold == "simpleevsewifi\n") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
									<option <?php if($evseconold == "goe\n") echo "selected" ?> value="goe">Go-e</option>
									<option <?php if($evseconold == "nrgkick\n") echo "selected" ?> value="nrgkick">NRGKick + Connect</option>
									<option <?php if($evseconold == "twcmanager\n") echo "selected" ?> value="twcmanager">Tesla TWC mit TWCManager</option>
									<option <?php if($evseconold == "keba\n") echo "selected" ?> value="keba">Keba</option>
								</select>
							</div>
						</div>
						<div id="evseconmastereth" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="openwb12" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option, sowohl für Bausatz als auch für fertige openWB series1 oder series2.
							</div>
						</div>
						<div id="openwbbuchse" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option für die openWB mit Buchse.
							</div>
						</div>
						<div id="openwb12mid" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="openwb12v2mid" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="evsecondac" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="dacregister" class="col-md-4 col-form-label">Dacregister</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="99" step="1" name="dacregister" id="dacregister" value="<?php echo trim($dacregisterold) ?>">
										<span class="form-text small">
											Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP.
											Der benötigte Wert sollte <a href="/openWB/ramdisk/i2csearch">HIER</a> zu finden sein.
											Alternativ rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconswifi" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsewifiiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evsewifiiplp1" id="evsewifiiplp1" value="<?php echo trim($evsewifiiplp1old) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evsewifitimeoutlp1" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="evsewifitimeoutlp1" id="evsewifitimeoutlp1" value="<?php echo trim($evsewifitimeoutlp1old) ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort der Simple EVSE gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die SimpleEVSE z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconextopenwb" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="chargep1ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="chargep1ip" id="chargep1ip" value="<?php echo trim($chargep1ipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Die externe openWB muss die Option "openWB ist nur ein Ladepunkt" aktiv haben!
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="chargep1cp" class="col-md-4 col-form-label">Ladepunkt an der externen openWB</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="2" step="1" name="chargep1cp" id="chargep1cp" value="<?php echo trim($chargep1cpold) ?>">
										<span class="form-text small">Ist die externe openWB eine Duo gibt diese Option an ob Ladepunkt 1 oder 2 angesprochen werden soll.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconmod" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="modbusevsesource" class="col-md-4 col-form-label">Source</label>
									<div class="col">
										<input class="form-control" type="text" name="modbusevsesource" id="modbusevsesource" value="<?php echo trim($modbusevsesourceold) ?>">
										<span class="form-text small">Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="modbusevseid" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="modbusevseid" id="modbusevseid" value="<?php echo trim($modbusevseidold) ?>">
										<span class="form-text small">Gültige Werte 1-254. Modbus ID der EVSE.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="modbusevselanip" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="modbusevselanip" id="modbusevselanip" value="<?php echo trim($modbusevselanipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Vermutlich gleich der IP des SDM Zählers in der WB.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconipevse" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evseiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evseiplp1" id="evseiplp1" value="<?php echo trim($evseiplp1old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Aufgedruckt auf dem Label der openWB.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseidlp1" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseidlp1" id="evseidlp1" value="<?php echo trim($evseidlp1old) ?>">
										<span class="form-text small">Gültige Werte 1-254. Aufgedruckt auf dem Label der openWB.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconkeba" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="kebaiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="kebaiplp1" id="kebaiplp1" value="<?php echo trim($kebaiplp1old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Erforder eine Keba C- oder X- Series. Die Smart Home Funktion (UDP Schnittstelle) muss per DIP Switch in der Keba aktiviert sein!
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconhttp" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="httpevseip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="httpevseip" id="httpevseip" value="<?php echo trim($httpevseipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Der Ampere sollwert wird an http://$IP/setcurrent?current=$WERT gesendet.
											Für eine korrekte Funktion ist als Ladeleistungsmodul HTTP zu wählen.
											WERT kann sein: 0 = keine Ladung erlaubt, 6-32 = x Ampere erlaubt.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecontwcmanager" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="twcmanagerlp1ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="twcmanagerlp1ip" id="twcmanagerlp1ip" value="<?php echo trim($twcmanagerlp1ipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="twcmanagerlp1phasen" class="col-md-4 col-form-label">Anzahl Phasen</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="3" step="1" name="twcmanagerlp1phasen" id="twcmanagerlp1phasen" value="<?php echo trim($twcmanagerlp1phasenold) ?>">
										<span class="form-text small">Definiert die genutzte Anzahl der Phasen zur korrekten Errechnung der Ladeleistung (BETA).</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecongoe" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="goeiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="goeiplp1" id="goeiplp1" value="<?php echo trim($goeiplp1old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="goetimeoutlp1" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="goetimeoutlp1" id="goetimeoutlp1" value="<?php echo trim($goetimeoutlp1old) ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des Go-echargers gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der Go-echarger z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconnrgkick" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="nrgkickiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="nrgkickiplp1" id="nrgkickiplp1" value="<?php echo trim($nrgkickiplp1old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Zu finden in der NRGKick App unter Einstellungen -> Info -> NRGkick Connect Infos.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkicktimeoutlp1" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="nrgkicktimeoutlp1" id="nrgkicktimeoutlp1" value="<?php echo trim($nrgkicktimeoutlp1old) ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des NRGKick Connect gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der NRGKick z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkickmaclp1" class="col-md-4 col-form-label">MAC Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$" name="nrgkickmaclp1" id="nrgkickmaclp1" value="<?php echo trim($nrgkickmaclp1old) ?>">
										<span class="form-text small">
											Gültige Werte MAC Adresse im Format: 11:22:33:AA:BB:CC<br>
											Zu finden In der NRGKick App unter Einstellungen -> BLE-Mac.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkickpwlp1" class="col-md-4 col-form-label">Password</label>
									<div class="col">
										<input class="form-control" type="password" name="nrgkickpwlp1" id="nrgkickpwlp1" value="<?php echo trim($nrgkickpwlp1old) ?>">
										<span class="form-text small">
											Password, welches in der NRGKick App festgelegt wurde.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="llmodullp1" class="hide">
							<hr class="border-primary">
							<div class="form-row mb-1">
								<label for="ladeleistungmodul" class="col-md-4 col-form-label">Ladeleistungmodul</label>
								<div class="col">
									<select name="ladeleistungmodul" id="ladeleistungmodul" class="form-control">
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
										<option <?php if($ladeleistungmodulold == "mqttll\n") echo "selected" ?> value="mqttll">MQTT</option>
									</select>
								</div>
							</div>
							<div id="llmnone" class="hide">
							</div>
							<div id="mpm3pmlllp1div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpmlp1ip" class="col-md-4 col-form-label">IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpmlp1ip" id="mpmlp1ip" value="<?php echo trim($mpmlp1ipold) ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse des Modbus Ethernet Konverters im Format: 192.168.0.12
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp1id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpmlp1id" id="mpmlp1id" value="<?php echo trim($mpmlp1idold) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="httpll" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="httpll_w_url" class="col-md-4 col-form-label">URL Ladeleistung in Watt</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_w_url" id="httpll_w_url" value="<?php echo htmlspecialchars(trim($httpll_w_urlold)) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in Watt sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_kwh_url" class="col-md-4 col-form-label">URL Zählerstand in kWh</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_kwh_url" id="httpll_kwh_url" value="<?php echo htmlspecialchars(trim($httpll_kwh_urlold)) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in kWh mit einem Punkt als Trennzeichen für Nachkommastellen sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_a1_url" class="col-md-4 col-form-label">URL Stromstärke Phase 1</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_a1_url" id="httpll_a1_url" value="<?php echo htmlspecialchars(trim($httpll_a1_urlold)) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in Ampere mit einem Punkt als Trennzeichen für Nachkommastellen sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_a2_url" class="col-md-4 col-form-label">URL Stromstärke Phase 2</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_a2_url" id="httpll_a2_url" value="<?php echo htmlspecialchars(trim($httpll_a2_urlold)) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in Ampere mit einem Punkt als Trennzeichen für Nachkommastellen sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_a3_url" class="col-md-4 col-form-label">URL Stromstärke Phase 3</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_a3_url" id="httpll_a3_url" value="<?php echo htmlspecialchars(trim($httpll_a3_urlold)) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in Ampere mit einem Punkt als Trennzeichen für Nachkommastellen sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_ip" class="col-md-4 col-form-label">IP Adresse Plug/Charge Status</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="httpll_ip" id="httpll_ip" value="<?php echo trim($httpll_ipold) ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse im Format: 192.168.0.12<br>
												Abgerufene werden die Urls <span class="text-info">http://IP/plugstat</span> und <span class="text-info">http://IP/chargestat</span>.
												Rückgabe ist jeweils 0 oder 1. Plugstat gibt an ob ein Stecker steckt, Chargestat gibt an, ob EVSEseitig die Ladung aktiv ist
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="llmpm3pm" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpm3pmllsource" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="mpm3pmllsource" id="mpm3pmllsource" value="<?php echo trim($mpm3pmllsourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das MPM3PM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpm3pmllid" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmllid" id="mpm3pmllid" value="<?php echo trim($mpm3pmllidold) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="llmfsm" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="fsm63a3modbusllsource" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="fsm63a3modbusllsource" id="fsm63a3modbusllsource" value="<?php echo trim($fsm63a3modbusllsourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das fsm63a3 angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="fsm63a3modbusllid" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="fsm63a3modbusllid" id="fsm63a3modbusllid" value="<?php echo trim($fsm63a3modbusllidold) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des fsm63a3.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="llmsdm" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm630modbusllsource" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm630modbusllsource" id="sdm630modbusllsource" value="<?php echo trim($sdm630modbusllsourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm630modbusllid" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm630modbusllid" id="sdm630modbusllid" value="<?php echo trim($sdm630modbusllidold) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM. Für SDM230 & SDM630v2.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="sdm120div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm120modbusllsource" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm120modbusllsource" id="sdm120modbusllsource" value="<?php echo trim($sdm120modbusllsourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid1" class="col-md-4 col-form-label">ID Phase 1</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid1" id="sdm120modbusllid1" value="<?php echo trim($sdm120modbusllid1old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der ersten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid2" class="col-md-4 col-form-label">ID Phase 2</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid2" id="sdm120modbusllid2" value="<?php echo trim($sdm120modbusllid2old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der zweiten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid3" class="col-md-4 col-form-label">ID Phase 3</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid3" id="sdm120modbusllid3" value="<?php echo trim($sdm120modbusllid3old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der dritten Phase.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="rs485lanlp1" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm630modbuslllanip" class="col-md-4 col-form-label">IP Adresse RS485/Lan-Konverter</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sdm630modbuslllanip" id="sdm630modbuslllanip" value="<?php echo trim($sdm630modbuslllanipold) ?>">
											<span class="form-text small">
												Ist nur von Belang, wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant.<br>
												Gültige Werte IPs. Wenn ein LAN Konverter genutzt wird, muss die Source auf /dev/virtualcomx (z.B. /dev/virtualcom0) gesetzt werden.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="llswifi" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.
								</div>
							</div>
							<div id="llsma" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="smaemdllid" class="col-md-4 col-form-label">Seriennummer</label>
										<div class="col">
											<input class="form-control" type="text" name="smaemdllid" id="smaemdllid" value="<?php echo trim($smaemdllidold) ?>">
											<span class="form-text small">
												Gültige Werte: Seriennummer. Hier die Seriennummer des SMA Meter für die Ladeleistung angeben.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="mqttll" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.<br>
									Per MQTT zu schreiben:<br>
									<span class="text-info">openWB/set/lp/1/W</span> Ladeleistung in Watt, int, positiv<br>
									<span class="text-info">openWB/set/lp/1/kWhCounter</span> Zählerstand in kWh, float, Punkt als Trenner, nur positiv
								</div>
							</div>
						</div>

						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="socmodul" class="col-md-4 col-form-label">SOC Modul</label>
							<div class="col">
								<select name="socmodul" id="socmodul" class="form-control">
									<option <?php if($socmodulold == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
									<option <?php if($socmodulold == "soc_http\n") echo "selected" ?> value="soc_http">SoC HTTP</option>
									<option <?php if($socmodulold == "soc_leaf\n") echo "selected" ?> value="soc_leaf">SoC Nissan Leaf</option>
									<option <?php if($socmodulold == "soc_i3\n") echo "selected" ?> value="soc_i3">SoC BMW & Mini</option>
									<option <?php if($socmodulold == "soc_zoe\n") echo "selected" ?> value="soc_zoe">SoC Renault Zoe alt</option>
									<option <?php if($socmodulold == "soc_myrenault\n") echo "selected" ?> value="soc_myrenault">SoC Renault Zoe MyRenault</option>
									<option <?php if($socmodulold == "soc_evnotify\n") echo "selected" ?> value="soc_evnotify">SoC EVNotify</option>
									<option <?php if($socmodulold == "soc_tesla\n") echo "selected" ?> value="soc_tesla">SoC Tesla</option>
									<option <?php if($socmodulold == "soc_carnet\n") echo "selected" ?> value="soc_carnet">SoC VW Carnet</option>
									<option <?php if($socmodulold == "soc_zerong\n") echo "selected" ?> value="soc_zerong">SoC Zero NG</option>
									<option <?php if($socmodulold == "soc_audi\n") echo "selected" ?> value="soc_audi">SoC Audi</option>
									<option <?php if($socmodulold == "soc_mqtt\n") echo "selected" ?> value="soc_mqtt">MQTT</option>
									<option <?php if($socmodulold == "soc_bluelink\n") echo "selected" ?> value="soc_bluelink">Hyundai Bluelink</option>
									<option <?php if($socmodulold == "soc_kia\n") echo "selected" ?> value="soc_kia">Kia</option>
									<option <?php if($socmodulold == "soc_volvo\n") echo "selected" ?> value="soc_volvo">Volvo</option>
								</select>
							</div>
						</div>
						<div id="socmodullp1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">SoC nur Abfragen wenn Auto angesteckt</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($stopsocnotpluggedlp1old == 0) echo " active" ?>">
												<input type="radio" name="stopsocnotpluggedlp1" id="stopsocnotpluggedlp1Off" value="0"<?php if($stopsocnotpluggedlp1old == 0) echo " checked=\"checked\"" ?>>Nein
											</label>
											<label class="btn btn-outline-info<?php if($stopsocnotpluggedlp1old == 1) echo " active" ?>">
												<input type="radio" name="stopsocnotpluggedlp1" id="stopsocnotpluggedlp1On" value="1"<?php if($stopsocnotpluggedlp1old == 1) echo " checked=\"checked\"" ?>>Ja
											</label>
										</div>
										<span class="form-text small">
											Wenn Ja gewählt wird der SoC nur abgefragt während ein Auto angesteckt ist.
											Bei Nein wird immer entsprechend der SoC Modul Konfiguration abgefragt.
											Funktioniert nur wenn der "steckend" Status korrekt angezeigt wird.
										</span>
									</div>
								</div>
							</div>
							<div id="socmnone" class="hide">
								<!-- nothing here -->
							</div>
							<div id="socmqtt" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.<br>
									Per MQTT zu schreiben:<br>
									<span class="text-info">openWB/set/lp/1/%Soc</span> Ladezustand in %, int, 0-100
								</div>
							</div>
							<div id="socmtesla" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="teslasocuser" class="col-md-4 col-form-label">E-Mail</label>
										<div class="col">
											<input class="form-control" type="email" name="teslasocuser" id="teslasocuser" value="<?php echo trim($socteslausernameold) ?>">
											<span class="form-text small">
												Email Adresse des Tesla Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="teslasocpw" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="teslasocpw" id="teslasocpw" value="<?php echo trim($socteslapwold) ?>">
											<span class="form-text small">
												Password des Tesla Logins. Das Passwort wird nur bei der ersten Einrichtung verwendet. Sobald die Anmeldung erfolgreich war, wird die Anmeldung über Token geregelt und das Passwort durch "#TokenInUse#" ersetzt.<br>
												Wird bei Tesla direkt das Passwort geändert, kann die WB sich nicht mehr anmelden und es muss hier wieder einmalig das aktuelle Passwort eingetragen werden.<br>
												Wenn das Eingabefeld geleert wird, dann werden auch die Anmeldetoken komplett entfernt.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="teslasoccarnumber" class="col-md-4 col-form-label">Auto im Account</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="teslasoccarnumber" id="teslasoccarnumber" value="<?php echo trim($socteslacarnumberold) ?>">
											<span class="form-text small">
												Im Normalfall hier 0 eintragen. Sind mehrere Teslas im Account für den zweiten Tesla eine 1 eintragen.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="teslasocintervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="teslasocintervall" id="teslasocintervall" value="<?php echo trim($socteslaintervallold) ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall (in Minuten bei normaler Regelgeschwindigkeit) der Ladestand des Autos abgefragt werden soll, wenn nicht geladen wird.<br>
												Damit das Auto in den Standby gehen kann und die Energieverluste gering bleiben, sollte das Intervall mindestens eine Stunde ("60") betragen, besser 12 Stunden ("720") oder mehr.<br>
												Zu Beginn einer Ladung wird das Auto immer geweckt, um den aktuellen SoC zu erhalten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="teslasocintervallladen" class="col-md-4 col-form-label">Abfrageintervall Laden</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="teslasocintervallladen" id="teslasocintervallladen" value="<?php echo trim($socteslaintervallladenold) ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall (in Minuten bei normaler Regelgeschwindigkeit) der Ladestand des Autos während des Ladens abgefragt werden soll.<br>
												Je nach Ladeleistung werden 5 - 10 Minuten empfohlen, damit eventuell eingestellte SoC-Grenzen rechtzeitig erkannt werden können.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmbluelink" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_bluelink_email" class="col-md-4 col-form-label">E-Mail</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_bluelink_email" id="soc_bluelink_email" value="<?php echo trim($soc_bluelink_emailold) ?>">
											<span class="form-text small">
												Email Adresse des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_bluelink_password" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_bluelink_password" id="soc_bluelink_password" value="<?php echo trim($soc_bluelink_passwordold) ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_bluelink_pin" class="col-md-4 col-form-label">PIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_bluelink_pin" id="soc_bluelink_pin" value="<?php echo trim($soc_bluelink_pinold) ?>">
											<span class="form-text small">
												PIN des Accounts.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_bluelink_interval" class="col-md-4 col-form-label">Abfrageintervall</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_bluelink_interval" id="soc_bluelink_interval" value="<?php echo trim($soc_bluelink_intervalold) ?>">
											<span class="form-text small">
												Wie oft abgefragt wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmkia" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_vin" id="soc_vin" value="<?php echo trim($soc_vinold) ?>">
											<span class="form-text small">
												VIN des Autos.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmzerong" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_zerong_username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_zerong_username" id="soc_zerong_username" value="<?php echo trim($soc_zerong_usernameold) ?>">
											<span class="form-text small">
												Email Adresse des Zero Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zerong_password" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_zerong_password" id="soc_zerong_password" value="<?php echo trim($soc_zerong_passwordold) ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zerong_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_zerong_intervall" id="soc_zerong_intervall" value="<?php echo trim($soc_zerong_intervallold) ?>">
											<span class="form-text small">
												Wie oft die Zero abgefragt wird wenn nicht geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zerong_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Laden</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_zerong_intervallladen" id="soc_zerong_intervallladen" value="<?php echo trim($soc_zerong_intervallladenold) ?>">
											<span class="form-text small">
												Wie oft die Zero abgefragt wird während geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmaudi" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_audi_username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_audi_username" id="soc_audi_username" value="<?php echo trim($soc_audi_usernameold) ?>">
											<span class="form-text small">
												Email Adresse des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_audi_passwort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_audi_passwort" id="soc_audi_passwort" value="<?php echo trim($soc_audi_passwortold) ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmhttp" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="hsocip" class="col-md-4 col-form-label">Abfrage URL</label>
										<div class="col">
											<input class="form-control" type="text" name="hsocip" id="hsocip" value="<?php echo htmlspecialchars(trim($hsocipold)) ?>">
											<span class="form-text small">
												Gültige Werte none, "url". URL für die Abfrage des Soc, Antwort muss der reine Zahlenwert sein.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmuser" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="socuser" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="socuser" id="socuser" value="<?php echo trim($socuserold) ?>">
										</div>
									</div>
								</div>
							</div>
							<div id="socmpass" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="socpass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="socpass" id="socpass" value="<?php echo trim($socpassold) ?>">
										</div>
									</div>
								</div>
							</div>
							<div id="soczoe" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="zoeusername" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="zoeusername" id="zoeusername" value="<?php echo trim($zoeusernameold) ?>">
											<span class="form-text small">
												Renault Zoe Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="zoepasswort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="zoepasswort" id="zoepasswort" value="<?php echo trim($zoepasswortold) ?>">
											<span class="form-text small">
											Renault Zoe Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Zoe Remote wecken wenn sie eingeschlafen ist</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($wakeupzoelp1old == 0) echo " active" ?>">
													<input type="radio" name="wakeupzoelp1" id="wakeupzoelp1Off" value="0"<?php if($wakeupzoelp1old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($wakeupzoelp1old == 1) echo " active" ?>">
													<input type="radio" name="wakeupzoelp1" id="wakeupzoelp1On" value="1"<?php if($wakeupzoelp1old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmyrenault" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="myrenault_userlp1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_userlp1" id="myrenault_userlp1" value="<?php echo trim($myrenault_userlp1old) ?>">
											<span class="form-text small">
												MyRenault Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_passlp1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="myrenault_passlp1" id="myrenault_passlp1" value="<?php echo trim($myrenault_passlp1old) ?>">
											<span class="form-text small">
												MyRenault Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_locationlp1" class="col-md-4 col-form-label">Standort</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_locationlp1" id="myrenault_locationlp1" value="<?php echo trim($myrenault_locationlp1old) ?>">
											<span class="form-text small">
												MyRenault Standort, z.B. de_DE
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_countrylp1" class="col-md-4 col-form-label">Land</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_countrylp1" id="myrenault_countrylp1" value="<?php echo trim($myrenault_countrylp1old) ?>">
											<span class="form-text small">
												MyRenault Land, z.B. CH, AT, DE
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soclp1_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soclp1_vin" id="soclp1_vin" value="<?php echo trim($soclp1_vinold) ?>">
											<span class="form-text small">
												VIN des Autos. Ist nur nötig wenn es sich um ein Importfahrzeug handelt. Kann auf none belassen werden wenn die Auslesung funktioniert.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Zoe Remote wecken wenn sie eingeschlafen ist</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($wakeupmyrenaultlp1old == 0) echo " active" ?>">
													<input type="radio" name="wakeupmyrenaultlp1" id="wakeupmyrenaultlp1Off" value="0"<?php if($wakeupmyrenaultlp1old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($wakeupmyrenaultlp1old == 1) echo " active" ?>">
													<input type="radio" name="wakeupmyrenaultlp1" id="wakeupmyrenaultlp1On" value="1"<?php if($wakeupmyrenaultlp1old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socevnotify" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="evnotifyakey" class="col-md-4 col-form-label">Akey</label>
										<div class="col">
											<input class="form-control" type="text" name="evnotifyakey" id="evnotifyakey" value="<?php echo trim($evnotifyakeyold) ?>">
											<span class="form-text small">
												Akey des EVNotify Kontos
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="evnotifytoken" class="col-md-4 col-form-label">Token</label>
										<div class="col">
											<input class="form-control" type="text" name="evnotifytoken" id="evnotifytoken" value="<?php echo trim($evnotifytokenold) ?>">
											<span class="form-text small">
												Token des Kontos
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socleaf" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="leafusername" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="leafusername" id="leafusername" value="<?php echo trim($leafusernameold) ?>">
											<span class="form-text small">
												Nissan Connect Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="leafpasswort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="leafpasswort" id="leafpasswort" value="<?php echo trim($leafpasswortold) ?>">
											<span class="form-text small">
												Nissan Connect Passwort
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soci3" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="i3username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="i3username" id="i3username" value="<?php echo trim($i3usernameold) ?>">
											<span class="form-text small">
												BMW Services Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="i3passwort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="i3passwort" id="i3passwort" value="<?php echo trim($i3passwortold) ?>">
											<span class="form-text small">
												BMW Services Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="i3vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="i3vin" id="i3vin" value="<?php echo trim($i3vinold) ?>">
											<span class="form-text small">
												BMW VIN. Sie ist in voller Länge anzugeben.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soci3intervall" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
										<div class="col">
											<input class="form-control" type="text" name="soci3intervall" id="soci3intervall" value="<?php echo trim($soci3intervallold) ?>">
											<span class="form-text small">
												Verkürzt das Abfrageintervall beim Laden auf xx Minuten
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soccarnet" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="carnetuser" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="carnetuser" id="carnetuser" value="<?php echo trim($carnetuserold) ?>">
											<span class="form-text small">
												VW Carnet Benutzername. Wenn der SoC nicht korrekt angezeigt wird, z.B. weil AGB von VW geändert wurden, ist es nötig sich auf https://www.portal.volkswagen-we.com anzumelden.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="carnetpass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="carnetpass" id="carnetpass" value="<?php echo trim($carnetpassold) ?>">
											<span class="form-text small">
												VW Carnet Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soccarnetintervall" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
										<div class="col">
											<input class="form-control" type="text" name="soccarnetintervall" id="soccarnetintervall" value="<?php echo trim($soccarnetintervallold) ?>">
											<span class="form-text small">
												Verkürzt das Abfrageintervall beim Laden auf xx Minuten
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						// visibility of charge point types
						function display_lp1() {
							hideSection('llmodullp1');
							hideSection('evsecondac');
							hideSection('evseconmod');
							hideSection('evseconswifi');
							hideSection('evsecongoe');
							hideSection('evseconnrgkick');
							hideSection('evseconmastereth');
							hideSection('evseconkeba');
							hideSection('openwb12');
							hideSection('openwb12mid');
							hideSection('openwb12v2mid');
							hideSection('evseconhttp');
							hideSection('evsecontwcmanager');
							hideSection('evseconipevse');
							hideSection('openwbbuchse');
							hideSection('evseconextopenwb');

							if($('#evsecon').val() == 'ipevse') {
								showSection('evseconipevse');
								showSection('llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'extopenwb') {
								showSection('evseconextopenwb');
							}
							if($('#evsecon').val() == 'buchse') {
								showSection('openwbbuchse');
							}
							if($('#evsecon').val() == 'dac') {
								showSection('evsecondac');
								showSection('llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'modbusevse') {
								showSection('evseconmod');
								showSection('llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'simpleevsewifi') {
								showSection('evseconswifi');
							}
							if($('#evsecon').val() == 'httpevse') {
								showSection('evseconhttp');
								showSection('llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'goe') {
								showSection('evsecongoe');
							}
							if($('#evsecon').val() == 'masterethframer') {
								showSection('evseconmastereth');
							}
							if($('#evsecon').val() == 'nrgkick') {
								showSection('evseconnrgkick');
							}
							if($('#evsecon').val() == 'keba') {
								showSection('evseconkeba');
							}
							if($('#evsecon').val() == 'twcmanager') {
								showSection('evsecontwcmanager');
							}
							if($('#evsecon').val() == 'openwb12') {
								showSection('openwb12');
							}
							if($('#evsecon').val() == 'openwb12mid') {
								showSection('openwb12mid');
							}
							if($('#evsecon').val() == 'openwb12v2mid') {
								showSection('openwb12v2mid');
							}
							if($('#evsecon').val() == 'ipevse') {
								showSection('evseconipevse');
							}
						}

						// visibility of meter modules
						function display_llmp1() {
							hideSection('llmnone');
							hideSection('llmsdm');
							hideSection('llmpm3pm');
							hideSection('llswifi');
							hideSection('llsma');
							hideSection('sdm120div');
							hideSection('rs485lanlp1');
							hideSection('llmfsm');
							hideSection('httpll');
							hideSection('mpm3pmlllp1div');
							hideSection('mqttll');

							if($('#ladeleistungmodul').val() == 'mpm3pmlllp1') {
								showSection('mpm3pmlllp1div');
								hideSection('rs485lanlp1'); // BUG hide/show typo?
							}
							if($('#ladeleistungmodul').val() == 'none') {
								showSection('llmnone');
							}
							if($('#ladeleistungmodul').val() == 'mpm3pmtripple') {
								showSection('llmnone');
							}
							if($('#ladeleistungmodul').val() == 'httpll') {
								showSection('httpll');
							}
							if($('#ladeleistungmodul').val() == 'sdm630modbusll') {
								showSection('llmsdm');
								showSection('rs485lanlp1');
							}
							if($('#ladeleistungmodul').val() == 'smaemd_ll') {
								showSection('llsma');
							}
							if($('#ladeleistungmodul').val() == 'sdm120modbusll') {
								showSection('sdm120div');
								showSection('rs485lanlp1');
							}
							if($('#ladeleistungmodul').val() == 'simpleevsewifi') {
								showSection('llswifi');
							}
							if($('#ladeleistungmodul').val() == 'mpm3pmll') {
								showSection('llmpm3pm');
								showSection('rs485lanlp1');
							}
							if($('#ladeleistungmodul').val() == 'fsm63a3modbusll') {
								showSection('rs485lanlp1');
								showSection('llmfsm');
							}
							if($('#ladeleistungmodul').val() == 'mqttll') {
								showSection('mqttll');
							}
						}

						// visibility of soc modules
						function display_socmodul() {
							hideSection('socmodullp1');
							hideSection('socmnone');
							hideSection('socmhttp');
							hideSection('socleaf');
							hideSection('soci3');
							hideSection('soczoe');
							hideSection('socevnotify');
							hideSection('socmtesla');
							hideSection('soccarnet');
							hideSection('socmzerong');
							hideSection('socmaudi');
							hideSection('socmqtt');
							hideSection('socmbluelink');
							hideSection('socmkia');
							hideSection('socmuser');
							hideSection('socmpass');
							hideSection('socmyrenault');

							if($('#socmodul').val() == 'none') {
								showSection('socmnone');
							} else {
								showSection('socmodullp1', false); // do not enable all input child-elements!
							}
							if($('#socmodul').val() == 'soc_volvo') {
								showSection('socmuser');
								showSection('socmpass');
							}
							if($('#socmodul').val() == 'soc_mqtt') {
								showSection('socmqtt');
							}
							if($('#socmodul').val() == 'soc_bluelink') {
								showSection('socmbluelink');
							}
							if($('#socmodul').val() == 'soc_kia') {
								showSection('socmkia');
								showSection('socmbluelink');
							}
							if($('#socmodul').val() == 'soc_audi') {
								showSection('socmaudi');
							}
							if($('#socmodul').val() == 'soc_myrenault') {
								showSection('socmyrenault');
							}
							if($('#socmodul').val() == 'soc_http') {
								showSection('socmhttp');
							}
							if($('#socmodul').val() == 'soc_zerong') {
								showSection('socmzerong');
							}
							if($('#socmodul').val() == 'soc_leaf') {
								showSection('socleaf');
							}
							if($('#socmodul').val() == 'soc_i3') {
								showSection('soci3');
							}
							if($('#socmodul').val() == 'soc_zoe') {
								showSection('soczoe');
							}
							if($('#socmodul').val() == 'soc_evnotify') {
								showSection('socevnotify');
							}
							if($('#socmodul').val() == 'soc_tesla') {
								showSection('socmtesla');
							}
							if($('#socmodul').val() == 'soc_carnet') {
								showSection('soccarnet');
							}
						}

						$(function() {
							display_llmp1();
							display_socmodul();
							display_lp1();

							$('#ladeleistungmodul').change(function(){
								display_llmp1();
							});

							$('#evsecon').change(function(){
								display_lp1();
							});

							$('#socmodul').change( function(){
								display_socmodul();
							});
						});
					</script>
				</div>

				<!-- Ladepunkt 2 -->
				<div class="card border-primary">
					<div class="card-header bg-primary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Ladepunkt 2</div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($lastmanagementold == 0) echo " active" ?>">
											<input type="radio" name="lastmanagement" id="lastmanagementOff" value="0"<?php if($lastmanagementold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($lastmanagementold == 1) echo " active" ?>">
											<input type="radio" name="lastmanagement" id="lastmanagementOn" value="1"<?php if($lastmanagementold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body hide" id="lastmman">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="lp2name" class="col-md-4 col-form-label">Name</label>
								<div class="col">
									<input class="form-control" type="text" name="lp2name" id="lp2name" value="<?php echo trim($lp2nameold) ?>">
								</div>
							</div>
						</div>
						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="evsecons1" class="col-md-4 col-form-label">Anbindung</label>
							<div class="col">
								<select name="evsecons1" id="evsecons1" class="form-control">
									<option <?php if($evsecons1old == "modbusevse\n" && $ladeleistungs1modulold == "mpm3pmlls1\n" && $mpm3pmlls1sourceold == "/dev/ttyUSB1\n" && $mpm3pmlls1idold == "6\n") echo "selected" ?> value="openwb12s1">openWB series1/2 Duo</option>
									<option <?php if($evsecons1old == "slaveeth\n") echo "selected" ?> value="slaveeth">openWB Slave</option>
									<option <?php if($evsecons1old == "ipevse\n") echo "selected" ?> value="ipevse">openWB Satellit</option>
									<option <?php if($evsecons1old == "extopenwb\n") echo "selected" ?> value="extopenwb">externe openWB</option>
									<option <?php if($evsecons1old == "modbusevse\n" && !($ladeleistungs1modulold == "mpm3pmlls1\n" && $mpm3pmlls1sourceold == "/dev/ttyUSB1\n" && $mpm3pmlls1idold == "6\n")) echo "selected" ?> value="modbusevse">Modbus</option>
									<option <?php if($evsecons1old == "dac\n") echo "selected" ?> value="dac">DAC</option>
									<option <?php if($evsecons1old == "simpleevsewifi\n") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
									<option <?php if($evsecons1old == "goe\n") echo "selected" ?> value="goe">Go-e</option>
									<option <?php if($evsecons1old == "nrgkick\n") echo "selected" ?> value="nrgkick">NRGKick + Connect</option>
									<option <?php if($evsecons1old == "keba\n") echo "selected" ?> value="keba">Keba</option>
								</select>
							</div>
						</div>
						<div id="evseconextopenwblp2" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="lp2id" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="lp2id" id="lp2id" value="<?php echo trim($chargep2ipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Die externe openWB muss die Option "openWB ist nur ein Ladepunkt" aktiv haben!
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="chargep2cp" class="col-md-4 col-form-label">Ladepunkt an der externen openWB</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="2" step="1" name="chargep2cp" id="chargep2cp" value="<?php echo trim($chargep2cpold) ?>">
										<span class="form-text small">Ist die externe openWB eine Duo gibt diese Option an ob Ladepunkt 1 oder 2 angesprochen werden soll.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconipevselp2" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evseiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evseiplp2" id="evseiplp2" value="<?php echo trim($evseiplp2old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Aufgedruckt auf dem Label der openWB.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseidlp2" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseidlp2" id="evseidlp2" value="<?php echo trim($evseidlp2old) ?>">
										<span class="form-text small">Gültige Werte 1-254. Aufgedruckt auf dem Label der openWB.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="openwb12s1" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option, sowohl für Bausatz als auch für fertige openWB series1 oder series2.
							</div>
						</div>
						<div id="evseconnrgkicks1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="nrgkickiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="nrgkickiplp2" id="nrgkickiplp2" value="<?php echo trim($nrgkickiplp2old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Zu finden in der NRGKick App unter Einstellungen -> Info -> NRGkick Connect Infos.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkicktimeoutlp2" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="nrgkicktimeoutlp2" id="nrgkicktimeoutlp2" value="<?php echo trim($nrgkicktimeoutlp2old) ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des NRGKick Connect gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der NRGKick z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkickmaclp2" class="col-md-4 col-form-label">MAC Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$" name="nrgkickmaclp2" id="nrgkickmaclp2" value="<?php echo trim($nrgkickmaclp2old) ?>">
										<span class="form-text small">
											Gültige Werte MAC Adresse im Format: 11:22:33:AA:BB:CC<br>
											Zu finden In der NRGKick App unter Einstellungen -> BLE-Mac.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkickpwlp2" class="col-md-4 col-form-label">Password</label>
									<div class="col">
										<input class="form-control" type="password" name="nrgkickpwlp2" id="nrgkickpwlp2" value="<?php echo trim($nrgkickpwlp2old) ?>">
										<span class="form-text small">
											Password, welches in der NRGKick App festgelegt wurde.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconkebas1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="kebaiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="kebaiplp2" id="kebaiplp2" value="<?php echo trim($kebaiplp2old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Erforder eine Keba C- oder X- Series. Die Smart Home Funktion (UDP Schnittstelle) muss per DIP Switch in der Keba aktiviert sein!
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconmbs1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsesources1" class="col-md-4 col-form-label">Source</label>
									<div class="col">
										<input class="form-control" type="text" name="evsesources1" id="evsesources1" value="<?php echo trim($evsesources1old) ?>">
										<span class="form-text small">Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseids1" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseids1" id="evseids1" value="<?php echo trim($evseids1old) ?>">
										<span class="form-text small">Gültige Werte 1-254. Modbus ID der EVSE.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evselanips1" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evselanips1" id="evselanips1" value="<?php echo trim($evselanips1old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Vermutlich gleich der IP des SDM Zählers in der WB.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecondacs1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="dacregisters1" class="col-md-4 col-form-label">Dacregister</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="99" step="1" name="dacregisters1" id="dacregisters1" value="<?php echo trim($dacregisters1old) ?>">
										<span class="form-text small">
											Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP.
											Der benötigte Wert sollte <a href="/openWB/ramdisk/i2csearch">HIER</a> zu finden sein.
											Alternativ rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecoslaveeth" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="evseconswifis1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsewifiiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evsewifiiplp2" id="evsewifiiplp2" value="<?php echo trim($evsewifiiplp2old) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evsewifitimeoutlp2" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="evsewifitimeoutlp2" id="evsewifitimeoutlp2" value="<?php echo trim($evsewifitimeoutlp2old) ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort der Simple EVSE gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die SimpleEVSE z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecongoes1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="goeiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="goeiplp2" id="goeiplp2" value="<?php echo trim($goeiplp2old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="goetimeoutlp2" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="goetimeoutlp2" id="goetimeoutlp2" value="<?php echo trim($goetimeoutlp2old) ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des Go-echargers gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der Go-echarger z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="llmodullp2" class="hide">
							<hr class="border-primary">
							<div class="form-row mb-1">
								<label for="ladeleistungs1modul" class="col-md-4 col-form-label">Ladeleistungmodul</label>
								<div class="col">
									<select name="ladeleistungs1modul" id="ladeleistungs1modul" class="form-control">
										<option <?php if($ladeleistungs1modulold == "sdm630modbuslls1\n") echo "selected" ?> value="sdm630modbuslls1">SDM 630 Modbus</option>
										<option <?php if($ladeleistungs1modulold == "sdm120modbuslls1\n") echo "selected" ?> value="sdm120modbuslls1">SDM 120 Modbus</option>
										<option <?php if($ladeleistungs1modulold == "simpleevsewifis1\n") echo "selected" ?> value="simpleevsewifis1">Simple EVSE Wifi</option>
										<option <?php if($ladeleistungs1modulold == "mpm3pmlls1\n") echo "selected" ?> value="mpm3pmlls1">MPM3PM Modbus</option>
										<option <?php if($ladeleistungs1modulold == "goelp2\n") echo "selected" ?> value="goelp2">Go-e</option> <!-- BUG go-E als LL-Modul? -->
										<option <?php if($ladeleistungs1modulold == "mpm3pmtripplelp2\n") echo "selected" ?> value="mpm3pmtripplelp2">openWB Tripple</option>
										<option <?php if($ladeleistungs1modulold == "mpm3pmlllp2\n") echo "selected" ?> value="mpm3pmlllp2">openWB Satelit</option>
									</select>
								</div>
							</div>
							<div id="mpm3pmlllp2div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpmlp2ip" class="col-md-4 col-form-label">IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpmlp2ip" id="mpmlp2ip" value="<?php echo trim($mpmlp2ipold) ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse des Modbus Ethernet Konverters im Format: 192.168.0.12
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp2id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpmlp2id" id="mpmlp2id" value="<?php echo trim($mpmlp2idold) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="mpm3pmlls1div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpm3pmlls1source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="mpm3pmlls1source" id="mpm3pmlls1source" value="<?php echo trim($mpm3pmlls1sourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das MPM3PM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpm3pmlls1id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmlls1id" id="mpm3pmlls1id" value="<?php echo trim($mpm3pmlls1idold) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="swifis1div" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.
								</div>
							</div>
							<div id="sdm630s1div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm630lp2source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm630lp2source" id="sdm630lp2source" value="<?php echo trim($sdm630lp2sourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdmids1" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdmids1" id="sdmids1" value="<?php echo trim($sdmids1old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM. Für SDM230 & SDM630v2.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="sdm120s1div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm120lp2source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm120lp2source" id="sdm120lp2source" value="<?php echo trim($sdm120lp2sourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid1s1" class="col-md-4 col-form-label">ID Phase 1</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid1s1" id="sdm120modbusllid1s1" value="<?php echo trim($sdm120modbusllid1s1old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der ersten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid2s1" class="col-md-4 col-form-label">ID Phase 2</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid2s1" id="sdm120modbusllid2s1" value="<?php echo trim($sdm120modbusllid2s1old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der zweiten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid3s1" class="col-md-4 col-form-label">ID Phase 3</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid3s1" id="sdm120modbusllid3s1" value="<?php echo trim($sdm120modbusllid3s1old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der dritten Phase.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="rs485lanlp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="lllaniplp2" class="col-md-4 col-form-label">IP Adresse RS485/Lan-Konverter</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="lllaniplp2" id="lllaniplp2" value="<?php echo trim($lllaniplp2old) ?>">
											<span class="form-text small">
												Ist nur von Belang, wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant.<br>
												Gültige Werte IPs. Wenn ein LAN Konverter genutzt wird, muss die Source auf /dev/virtualcomx (z.B. /dev/virtualcom0) gesetzt werden.
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>

						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="socmodul1" class="col-md-4 col-form-label">SOC Modul</label>
							<div class="col">
								<select name="socmodul1" id="socmodul1" class="form-control">
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
									<option <?php if($socmodul1old == "soc_audilp2\n") echo "selected" ?> value="soc_audilp2">Audi</option>
									<option <?php if($socmodul1old == "soc_bluelinklp2\n") echo "selected" ?> value="soc_bluelinklp2">Hyundai Bluelink</option>
								</select>
							</div>
						</div>
						<div id="socmodullp2" class="hide">
							<!-- soc is always requested, ignoring plug stat -->
							<div id="socmnone1" class="hide">
								<!-- nothing here -->
							</div>
							<div id="socmuser2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc2user" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="soc2user" id="soc2user" value="<?php echo trim($soc2userold) ?>">
										</div>
									</div>
								</div>
							</div>
							<div id="socmpass2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc2pass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc2pass" id="soc2pass" value="<?php echo trim($soc2passold) ?>">
										</div>
									</div>
								</div>
							</div>
							<div id="socmqtt1" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.<br>
									Per MQTT zu schreiben:<br>
									<span class="text-info">openWB/set/lp/2/%Soc</span> Ladezustand in %, int, 0-100
								</div>
							</div>
							<div id="socmzeronglp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_zeronglp2_username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_zeronglp2_username" id="soc_zeronglp2_username" value="<?php echo trim($soc_zeronglp2_usernameold) ?>">
											<span class="form-text small">
												Email Adresse des Zero Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zeronglp2_password" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_zeronglp2_password" id="soc_zeronglp2_password" value="<?php echo trim($soc_zeronglp2_passwordold) ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zeronglp2_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_zeronglp2_intervall" id="soc_zeronglp2_intervall" value="<?php echo trim($soc_zeronglp2_intervallold) ?>">
											<span class="form-text small">
												Wie oft die Zero abgefragt wird wenn nicht geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zeronglp2_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Laden</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_zeronglp2_intervallladen" id="soc_zeronglp2_intervallladen" value="<?php echo trim($soc_zeronglp2_intervallladenold) ?>">
											<span class="form-text small">
												Wie oft die Zero abgefragt wird während geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmteslalp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="teslasoclp2user" class="col-md-4 col-form-label">E-Mail</label>
										<div class="col">
											<input class="form-control" type="email" name="teslasoclp2user" id="teslasoclp2user" value="<?php echo trim($socteslalp2usernameold) ?>">
											<span class="form-text small">
												Email Adresse des Tesla Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="teslasoclp2pw" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="teslasoclp2pw" id="teslasoclp2pw" value="<?php echo trim($socteslalp2pwold) ?>">
											<span class="form-text small">
												Password des Tesla Logins. Das Passwort wird nur bei der ersten Einrichtung verwendet. Sobald die Anmeldung erfolgreich war, wird die Anmeldung über Token geregelt und das Passwort durch "#TokenInUse#" ersetzt.<br>
												Wird bei Tesla direkt das Passwort geändert, kann die WB sich nicht mehr anmelden und es muss hier wieder einmalig das aktuelle Passwort eingetragen werden.<br>
												Wenn das Eingabefeld geleert wird, dann werden auch die Anmeldetoken komplett entfernt.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="teslasoclp2carnumber" class="col-md-4 col-form-label">Auto im Account</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="teslasoclp2carnumber" id="teslasoclp2carnumber" value="<?php echo trim($socteslalp2carnumberold) ?>">
											<span class="form-text small">
												Im Normalfall hier 0 eintragen. Sind mehrere Teslas im Account für den zweiten Tesla eine 1 eintragen.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="teslasoclp2intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="teslasoclp2intervall" id="teslasoclp2intervall" value="<?php echo trim($socteslalp2intervallold) ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall (in Minuten bei normaler Regelgeschwindigkeit) der Ladestand des Autos abgefragt werden soll, wenn nicht geladen wird.<br>
												Damit das Auto in den Standby gehen kann und die Energieverluste gering bleiben, sollte das Intervall mindestens eine Stunde ("60") betragen, besser 12 Stunden ("720") oder mehr.<br>
												Zu Beginn einer Ladung wird das Auto immer geweckt, um den aktuellen SoC zu erhalten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="teslasoclp2intervallladen" class="col-md-4 col-form-label">Abfrageintervall Laden</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="teslasoclp2intervallladen" id="teslasoclp2intervallladen" value="<?php echo trim($socteslalp2intervallladenold) ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall (in Minuten bei normaler Regelgeschwindigkeit) der Ladestand des Autos während des Ladens abgefragt werden soll.<br>
												Je nach Ladeleistung werden 5 - 10 Minuten empfohlen, damit eventuell eingestellte SoC-Grenzen rechtzeitig erkannt werden können.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soccarnetlp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="carnetlp2user" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="carnetlp2user" id="carnetlp2user" value="<?php echo trim($carnetlp2userold) ?>">
											<span class="form-text small">
												VW Carnet Benutzername. Wenn der SoC nicht korrekt angezeigt wird, z.B. weil AGB von VW geändert wurden, ist es nötig sich auf https://www.portal.volkswagen-we.com anzumelden.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="carnetlp2pass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="carnetlp2pass" id="carnetlp2pass" value="<?php echo trim($carnetlp2passold) ?>">
											<span class="form-text small">
												VW Carnet Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soccarnetlp2intervall" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
										<div class="col">
											<input class="form-control" type="text" name="soccarnetlp2intervall" id="soccarnetlp2intervall" value="<?php echo trim($soccarnetlp2intervallold) ?>">
											<span class="form-text small">
												Verkürzt das Abfrageintervall beim Laden auf xx Minuten
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soczoelp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="zoelp2username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="zoelp2username" id="zoelp2username" value="<?php echo trim($zoelp2usernameold) ?>">
											<span class="form-text small">
												Renault Zoe Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="zoelp2passwort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="zoelp2passwort" id="zoelp2passwort" value="<?php echo trim($zoelp2passwortold) ?>">
											<span class="form-text small">
											Renault Zoe Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Zoe Remote wecken wenn sie eingeschlafen ist</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($wakeupzoelp2old == 0) echo " active" ?>">
													<input type="radio" name="wakeupzoelp2" id="wakeupzoelp2Off" value="0"<?php if($wakeupzoelp2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($wakeupzoelp2old == 1) echo " active" ?>">
													<input type="radio" name="wakeupzoelp2" id="wakeupzoelp2On" value="1"<?php if($wakeupzoelp2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmyrenaultlp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="myrenault_userlp2" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_userlp2" id="myrenault_userlp2" value="<?php echo trim($myrenault_userlp2old) ?>">
											<span class="form-text small">
												MyRenault Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_passlp2" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="myrenault_passlp2" id="myrenault_passlp2" value="<?php echo trim($myrenault_passlp2old) ?>">
											<span class="form-text small">
												MyRenault Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_locationlp2" class="col-md-4 col-form-label">Standort</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_locationlp2" id="myrenault_locationlp2" value="<?php echo trim($myrenault_locationlp2old) ?>">
											<span class="form-text small">
												MyRenault Standort, z.B. de_DE
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_countrylp2" class="col-md-4 col-form-label">Land</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_countrylp2" id="myrenault_countrylp2" value="<?php echo trim($myrenault_countrylp2old) ?>">
											<span class="form-text small">
												MyRenault Land, z.B. CH, AT, DE
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soclp2_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soclp2_vin" id="soclp2_vin" value="<?php echo trim($soclp2_vinold) ?>">
											<span class="form-text small">
												VIN des Autos. Ist nur nötig wenn es sich um ein Importfahrzeug handelt. Kann auf none belassen werden wenn die Auslesung funktioniert.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Zoe Remote wecken wenn sie eingeschlafen ist</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($wakeupmyrenaultlp2old == 0) echo " active" ?>">
													<input type="radio" name="wakeupmyrenaultlp2" id="wakeupmyrenaultlp2Off" value="0"<?php if($wakeupmyrenaultlp2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($wakeupmyrenaultlp2old == 1) echo " active" ?>">
													<input type="radio" name="wakeupmyrenaultlp2" id="wakeupmyrenaultlp2On" value="1"<?php if($wakeupmyrenaultlp2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socevnotifylp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="evnotifyakeylp2" class="col-md-4 col-form-label">Akey</label>
										<div class="col">
											<input class="form-control" type="text" name="evnotifyakeylp2" id="evnotifyakeylp2" value="<?php echo trim($evnotifyakeylp2old) ?>">
											<span class="form-text small">
												Akey des EVNotify Kontos
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="evnotifytokenlp2" class="col-md-4 col-form-label">Token</label>
										<div class="col">
											<input class="form-control" type="text" name="evnotifytokenlp2" id="evnotifytokenlp2" value="<?php echo trim($evnotifytokenlp2old) ?>">
											<span class="form-text small">
												Token des Kontos
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmhttp1" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="hsocip1" class="col-md-4 col-form-label">Abfrage URL</label>
										<div class="col">
											<input class="form-control" type="text" name="hsocip1" id="hsocip1" value="<?php echo htmlspecialchars(trim($hsocip1old)) ?>">
											<span class="form-text small">
												Gültige Werte none, "url". URL für die Abfrage des Soc, Antwort muss der reine Zahlenwert sein.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socleaf1" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="leafusernames1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="leafusernames1" id="leafusernames1" value="<?php echo trim($leafusernames1old) ?>">
											<span class="form-text small">
												Nissan Connect Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="leafpassworts1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="leafpassworts1" id="leafpassworts1" value="<?php echo trim($leafpassworts1old) ?>">
											<span class="form-text small">
												Nissan Connect Passwort
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soci31" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="i3usernames1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="i3usernames1" id="i3usernames1" value="<?php echo trim($i3usernames1old) ?>">
											<span class="form-text small">
												BMW Services Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="i3passworts1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="i3passworts1" id="i3passworts1" value="<?php echo trim($i3passworts1old) ?>">
											<span class="form-text small">
												BMW Services Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="i3vins1" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="i3vins1" id="i3vins1" value="<?php echo trim($i3vins1old) ?>">
											<span class="form-text small">
												BMW VIN. Sie ist in voller Länge anzugeben.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soci3intervall1" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
										<div class="col">
											<input class="form-control" type="text" name="soci3intervall1" id="soci3intervall1" value="<?php echo trim($soci3intervall1old) ?>">
											<span class="form-text small">
												Verkürzt das Abfrageintervall beim Laden auf xx Minuten
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmpin2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc2pin" class="col-md-4 col-form-label">Pin</label>
										<div class="col">
											<input class="form-control" type="text" name="soc2pin" id="soc2pin" value="<?php echo trim($soc2pinold) ?>">
											<span class="form-text small">
												PIN des Accounts.
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						function display_lp2() {
							hideSection('evsecondacs1');
							hideSection('evseconmbs1');
							hideSection('evseconswifis1');
							hideSection('llmodullp2');
							hideSection('evsecongoes1');
							hideSection('evsecoslaveeth');
							hideSection('evseconkebas1');
							hideSection('evseconnrgkicks1');
							hideSection('openwb12s1');
							hideSection('evseconextopenwblp2');
							hideSection('evseconipevselp2');

							if($('#evsecons1').val() == 'ipevse') {
								showSection('evseconipevselp2');
								showSection('llmodullp2');
								display_llmp2();
							}
							if($('#evsecons1').val() == 'dac') {
								showSection('evsecondacs1');
								showSection('llmodullp2');
								display_llmp2();
							}
							if($('#evsecons1').val() == 'modbusevse') {
								showSection('evseconmbs1');
								showSection('llmodullp2');
								display_llmp2();
							}
							if($('#evsecons1').val() == 'simpleevsewifi') {
								showSection('evseconswifis1');
							}
							if($('#evsecons1').val() == 'extopenwb') {
								showSection('evseconextopenwblp2');
							}
							if($('#evsecons1').val() == 'goe') {
								showSection('evsecongoes1');
							}
							if($('#evsecons1').val() == 'slaveeth') {
								showSection('evsecoslaveeth');
							}
							if($('#evsecons1').val() == 'keba') {
								showSection('evseconkebas1');
							}
							if($('#evsecons1').val() == 'nrgkick') {
								showSection('evseconnrgkicks1');
							}
							if($('#evsecon').val() == 'openwb12s1') {
								showSection('openwb12s1');
							}
						}

						function display_llmp2() {
							hideSection('sdm630s1div');
							hideSection('sdm120s1div');
							hideSection('swifis1div');
							hideSection('mpm3pmlls1div');
							hideSection('rs485lanlp2');
							hideSection('mpm3pmlllp2div');

							if($('#ladeleistungs1modul').val() == 'sdm630modbuslls1') {
								showSection('sdm630s1div');
								showSection('rs485lanlp2');
							}
							if($('#ladeleistungs1modul').val() == 'sdm120modbuslls1') {
								showSection('sdm120s1div');
								showSection('rs485lanlp2');
							}
							if($('#ladeleistungs1modul').val() == 'simpleevsewifis1') {
								showSection('swifis1div');
							}
							if($('#ladeleistungs1modul').val() == 'goelp2') {
								showSection('swifis1div');
							}
							if($('#ladeleistungs1modul').val() == 'mpm3pmlllp2') {
								showSection('mpm3pmlllp2div');
								hideSection('rs485lanlp2'); // BUG show/hide typo?
							}
							if($('#ladeleistungs1modul').val() == 'mpm3pmlls1') {
								showSection('mpm3pmlls1div');
								showSection('rs485lanlp2');
							}
						}

						function display_socmodul1() {
							hideSection('socmodullp2');
							hideSection('socmqtt1');
							hideSection('socmuser2');
							hideSection('socmpass2');
							hideSection('socmpin2');
							hideSection('socmnone1');
							hideSection('socmhttp1');
							hideSection('socleaf1');
							hideSection('soci31');
							hideSection('socevnotifylp2');
							hideSection('soczoelp2');
							hideSection('socmteslalp2');
							hideSection('socmyrenaultlp2');
							hideSection('soccarnetlp2');
							hideSection('socmzeronglp2');

							if($('#socmodul1').val() == 'none') {
								showSection('socmnone1');
							} else {
								showSection('socmodullp2', false); // do not enable all input child-elements!
							}
							if($('#socmodul1').val() == 'soc_mqtt') {
								showSection('socmqtt1');
							}
							if($('#socmodul1').val() == 'soc_http1') {
								showSection('socmhttp1');
							}
							if($('#socmodul1').val() == 'soc_audilp2') {
								showSection('socmuser2');
								showSection('socmpass2');
							}
							if($('#socmodul1').val() == 'soc_bluelinklp2') {
								showSection('socmuser2');
								showSection('socmpass2');
								showSection('socmpin2');
							}
							if($('#socmodul1').val() == 'soc_leafs1') {
								showSection('socleaf1');
							}
							if($('#socmodul1').val() == 'soc_myrenaultlp2') {
								showSection('socmyrenaultlp2');
							}
							if($('#socmodul1').val() == 'soc_i3s1') {
								showSection('soci31');
							}
							if($('#socmodul1').val() == 'soc_evnotifys1') {
								showSection('socevnotifylp2');
							}
							if($('#socmodul1').val() == 'soc_zoelp2') {
								showSection('soczoelp2');
							}
							if($('#socmodul1').val() == 'soc_carnetlp2') {
								showSection('soccarnetlp2');
							}
							if($('#socmodul1').val() == 'soc_teslalp2') {
								showSection('socmteslalp2');
							}
							if($('#socmodul1').val() == 'soc_zeronglp2') {
								showSection('socmzeronglp2');
							}
						}

						function display_lastmanagement() {
							if($('#lastmanagementOff').prop("checked")) {
								hideSection('lastmman');
								hideSection('durchslp2');
								hideSection('nachtls1div');
							}
							else {
								showSection('lastmman');
								showSection('durchslp2');
								showSection('nachtls1div');
								display_socmodul1();
								display_llmp2 ();
								display_lp2();
							}
						}

						$(function() {
							display_lastmanagement();
							display_socmodul1();
							display_llmp2 ();
							display_lp2();

							$('input[type=radio][name=lastmanagement]').change(function() {
								display_lastmanagement();
							} );

							$('#socmodul1').change( function(){
								display_socmodul1();
							});

							$('#ladeleistungs1modul').change( function(){
								display_llmp2();
							});

							$('#evsecons1').change( function(){
								display_lp2();
							});
						});
					</script>
				</div>

				<!-- Ladepunkt 3 -->
				<div class="card border-primary">
					<div class="card-header bg-primary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Ladepunkt 3</div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($lastmanagements2old == 0) echo " active" ?>">
											<input type="radio" name="lastmanagements2" id="lastmanagements2Off" value="0"<?php if($lastmanagements2old == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($lastmanagements2old == 1) echo " active" ?>">
											<input type="radio" name="lastmanagements2" id="lastmanagements2On" value="1"<?php if($lastmanagements2old == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body hide" id="lasts2mman">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="lp3name" class="col-md-4 col-form-label">Name</label>
								<div class="col">
									<input class="form-control" type="text" name="lp3name" id="lp3name" value="<?php echo trim($lp3nameold) ?>">
								</div>
							</div>
						</div>
						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="evsecons2" class="col-md-4 col-form-label">Anbindung</label>
							<div class="col">
								<select name="evsecons2" id="evsecons2" class="form-control">
									<option <?php if($evsecons2old == "thirdeth\n") echo "selected" ?> value="thirdeth">openWB dritter Ladepunkte</option>
									<option <?php if($evsecons2old == "ipevse\n") echo "selected" ?> value="ipevse">openWB Satellit</option>
									<option <?php if($evsecons2old == "extopenwb\n") echo "selected" ?> value="extopenwb">externe openWB</option>
									<option <?php if($evsecons2old == "modbusevse\n") echo "selected" ?> value="modbusevse">Modbus</option>
									<option <?php if($evsecons2old == "dac\n") echo "selected" ?> value="dac">DAC</option>
									<option <?php if($evsecons2old == "simpleevsewifi\n") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
									<option <?php if($evsecons2old == "goe\n") echo "selected" ?> value="goe">Go-e</option>
								</select>
							</div>
						</div>
						<div id="evseconextopenwblp3" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="chargep3ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="chargep3ip" id="chargep3ip" value="<?php echo trim($chargep3ipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Die externe openWB muss die Option "openWB ist nur ein Ladepunkt" aktiv haben!
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="chargep3cp" class="col-md-4 col-form-label">Ladepunkt an der externen openWB</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="2" step="1" name="chargep3cp" id="chargep3cp" value="<?php echo trim($chargep3cpold) ?>">
										<span class="form-text small">Ist die externe openWB eine Duo gibt diese Option an ob Ladepunkt 1 oder 2 angesprochen werden soll.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconipevselp3" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evseiplp3" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evseiplp3" id="evseiplp3" value="<?php echo trim($evseiplp3old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Aufgedruckt auf dem Label der openWB.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseidlp3" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseidlp3" id="evseidlp3" value="<?php echo trim($evseidlp3old) ?>">
										<span class="form-text small">Gültige Werte 1-254. Aufgedruckt auf dem Label der openWB.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconmbs2" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsesources2" class="col-md-4 col-form-label">Source</label>
									<div class="col">
										<input class="form-control" type="text" name="evsesources2" id="evsesources2" value="<?php echo trim($evsesources2old) ?>">
										<span class="form-text small">Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseids2" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseids2" id="evseids2" value="<?php echo trim($evseids2old) ?>">
										<span class="form-text small">Gültige Werte 1-254. Modbus ID der EVSE.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evselanips2" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evselanips2" id="evselanips2" value="<?php echo trim($evselanips2old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Vermutlich gleich der IP des SDM Zählers in der WB.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecondacs2" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="dacregisters2" class="col-md-4 col-form-label">Dacregister</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="99" step="1" name="dacregisters2" id="dacregisters2" value="<?php echo trim($dacregisters2old) ?>">
										<span class="form-text small">
											Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP.
											Der benötigte Wert sollte <a href="/openWB/ramdisk/i2csearch">HIER</a> zu finden sein.
											Alternativ rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconswifis2" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsewifiiplp3" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evsewifiiplp3" id="evsewifiiplp3" value="<?php echo trim($evsewifiiplp3old) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evsewifitimeoutlp3" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="evsewifitimeoutlp3" id="evsewifitimeoutlp3" value="<?php echo trim($evsewifitimeoutlp3old) ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort der Simple EVSE gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die SimpleEVSE z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecongoes2" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="goeiplp3" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="goeiplp3" id="goeiplp3" value="<?php echo trim($goeiplp3old) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="goetimeoutlp3" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="goetimeoutlp3" id="goetimeoutlp3" value="<?php echo trim($goetimeoutlp3old) ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des Go-echargers gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der Go-echarger z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="llmodullp3" class="hide">
							<hr class="border-primary">
							<div class="form-row mb-1">
								<label for="ladeleistungss2modul" class="col-md-4 col-form-label">Ladeleistungmodul</label>
								<div class="col">
									<select name="ladeleistungss2modul" id="ladeleistungss2modul" class="form-control">
										<option <?php if($ladeleistungs2modulold == "sdm630modbuslls2\n") echo "selected" ?> value="sdm630modbuslls2">SDM 630 Modbus</option>
										<option <?php if($ladeleistungs2modulold == "sdm120modbuslls2\n") echo "selected" ?> value="sdm120modbuslls2">SDM 120 Modbus</option>
										<option <?php if($ladeleistungs2modulold == "mpm3pmlls2\n") echo "selected" ?> value="mpm3pmlls2">MPM3PM Modbus</option>
										<option <?php if($ladeleistungs2modulold == "simpleevsewifis2\n") echo "selected" ?> value="simpleevsewifis2">Simple EVSE Wifi</option>
										<option <?php if($ladeleistungs2modulold == "goelp3\n") echo "selected" ?> value="goelp3">Go-E</option> <!-- BUG go-E als LL-Modul? -->
										<option <?php if($ladeleistungs2modulold == "mpm3pmtripplelp3\n") echo "selected" ?> value="mpm3pmtripplelp3">openWB Tripple</option>
										<option <?php if($ladeleistungs2modulold == "mpm3pmlllp3\n") echo "selected" ?> value="mpm3pmlllp3">openWB Satellit</option>
									</select>
								</div>
							</div>
							<div id="mpm3pmlllp3div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpmlp3ip" class="col-md-4 col-form-label">IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpmlp3ip" id="mpmlp3ip" value="<?php echo trim($mpmlp3ipold) ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse des Modbus Ethernet Konverters im Format: 192.168.0.12
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp3id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpmlp3id" id="mpmlp3id" value="<?php echo trim($mpmlp3idold) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="mpm3pmlls2div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpm3pmlls2source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="mpm3pmlls2source" id="mpm3pmlls2source" value="<?php echo trim($mpm3pmlls2sourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das MPM3PM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpm3pmlls2id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmlls2id" id="mpm3pmlls2id" value="<?php echo trim($mpm3pmlls2idold) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="swifis2div" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.
								</div>
							</div>
							<div id="sdm630s2div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm630lp3source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm630lp3source" id="sdm630lp3source" value="<?php echo trim($sdm630lp3sourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdmids2" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdmids2" id="sdmids2" value="<?php echo trim($sdmids2old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM. Für SDM230 & SDM630v2.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="sdm120s2div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm120lp3source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm120lp3source" id="sdm120lp3source" value="<?php echo trim($sdm120lp3sourceold) ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid1s2" class="col-md-4 col-form-label">ID Phase 1</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid1s2" id="sdm120modbusllid1s2" value="<?php echo trim($sdm120modbusllid1s2old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der ersten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid2s2" class="col-md-4 col-form-label">ID Phase 2</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid2s2" id="sdm120modbusllid2s2" value="<?php echo trim($sdm120modbusllid2s2old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der zweiten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid3s2" class="col-md-4 col-form-label">ID Phase 3</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid3s2" id="sdm120modbusllid3s2" value="<?php echo trim($sdm120modbusllid3s2old) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der dritten Phase.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="rs485lanlp3" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="lllaniplp3" class="col-md-4 col-form-label">IP Adresse RS485/Lan-Konverter</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="lllaniplp3" id="lllaniplp3" value="<?php echo trim($lllaniplp3old) ?>">
											<span class="form-text small">
												Ist nur von Belang, wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant.<br>
												Gültige Werte IPs. Wenn ein LAN Konverter genutzt wird, muss die Source auf /dev/virtualcomx (z.B. /dev/virtualcom0) gesetzt werden.
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						function display_lp3 () {
							hideSection('evsecondacs2');
							hideSection('evseconmbs2');
							hideSection('evseconswifis2');
							hideSection('llmodullp3');
							hideSection('evsecongoes2');
							hideSection('evseconipevselp3');
							hideSection('evseconextopenwblp3');

							if($('#evsecons2').val() == 'dac') {
								showSection('evsecondacs2');
								showSection('llmodullp3');
								display_llmp3();
							}
							if($('#evsecons2').val() == 'modbusevse') {
								showSection('evseconmbs2');
								showSection('llmodullp3');
								display_llmp3();
							}
							if($('#evsecons2').val() == 'simpleevsewifi') {
								showSection('evseconswifis2');
							}
							if($('#evsecons2').val() == 'extopenwb') {
								showSection('evseconextopenwblp3');
							}
							if($('#evsecons2').val() == 'goe') {
								showSection('evsecongoes2');
							}
							if($('#evsecons2').val() == 'ipevse') {
								showSection('evseconipevselp3');
								showSection('llmodullp3');
								display_llmp3();
							}
						}

						function display_llmp3 () {
							hideSection('sdm630s2div');
							hideSection('sdm120s2div');
							hideSection('swifis2div');
							hideSection('rs485lanlp3');
							hideSection('mpm3pmlls2div');
							hideSection('mpm3pmlllp3div');


							if($('#ladeleistungss2modul').val() == 'mpm3pmlllp3') {
								showSection('mpm3pmlllp3div');
								showSection('rs485lanlp3');
							}
							if($('#ladeleistungss2modul').val() == 'sdm630modbuslls2') {
								showSection('sdm630s2div');
								showSection('rs485lanlp3');
							}
							if($('#ladeleistungss2modul').val() == 'sdm120modbuslls2') {
								showSection('sdm120s2div');
								showSection('rs485lanlp3');
							}
							if($('#ladeleistungss2modul').val() == 'simpleevsewifis2') {
								showSection('swifis2div');
							}
							if($('#ladeleistungss2modul').val() == 'goelp3') {
								showSection('swifis2div');
							}
							if($('#ladeleistungss2modul').val() == 'mpm3pmlls2') {
								showSection('mpm3pmlls2div');
								showSection('rs485lanlp3');
							}
						}

						function display_lastmanagement2() {
							if($('#lastmanagements2Off').prop("checked")) {
								hideSection('lasts2mman');
								hideSection('durchslp3');
							}
							else {
								showSection('lasts2mman');
								showSection('durchslp3');
								display_lp3();
								display_llmp3();
							}
						}

						$(function() {
							display_lastmanagement2();
							display_lp3();
							display_llmp3();

							$('#evsecons2').change( function(){
								display_lp3();
							});

							$('input[type=radio][name=lastmanagements2]').change(function() {
								display_lastmanagement2();
							});

							$('#ladeleistungss2modul').change( function(){
								display_llmp3();
							});
						});
					</script>
				</div>

				<?php for( $chargepointNum = 4; $chargepointNum <= 8; $chargepointNum++ ){ ?>
					<!-- Ladepunkt <?php echo $chargepointNum; ?> -->
					<div class="card border-primary">
						<div class="card-header bg-primary">
							<div class="form-group mb-0">
								<div class="form-row vaRow mb-0">
									<div class="col-4">Ladepunkt <?php echo $chargepointNum; ?></div>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-sm btn-outline-info<?php if(${'lastmanagementlp'.$chargepointNum.'old'} == 0) echo " active" ?>">
												<input type="radio" name="lastmanagementlp<?php echo $chargepointNum; ?>" id="lastmanagementlp<?php echo $chargepointNum; ?>Off" value="0"<?php if(${'lastmanagementlp'.$chargepointNum.'old'} == 0) echo " checked=\"checked\"" ?>>Aus
											</label>
											<label class="btn btn-sm btn-outline-info<?php if(${'lastmanagementlp'.$chargepointNum.'old'} == 1) echo " active" ?>">
												<input type="radio" name="lastmanagementlp<?php echo $chargepointNum; ?>" id="lastmanagementlp<?php echo $chargepointNum; ?>On" value="1"<?php if(${'lastmanagementlp'.$chargepointNum.'old'} == 1) echo " checked=\"checked\"" ?>>An
											</label>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="card-body hide" id="lastlp<?php echo $chargepointNum; ?>mman">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="lp<?php echo $chargepointNum; ?>name" class="col-md-4 col-form-label">Name</label>
									<div class="col">
										<input class="form-control" type="text" name="lp<?php echo $chargepointNum; ?>name" id="lp<?php echo $chargepointNum; ?>name" value="<?php echo trim(${'lp'.$chargepointNum.'nameold'}) ?>">
									</div>
								</div>
							</div>
							<hr class="border-primary">
							<div class="form-row mb-1">
								<label for="evseconlp<?php echo $chargepointNum; ?>" class="col-md-4 col-form-label">Anbindung</label>
								<div class="col">
									<select name="evseconlp<?php echo $chargepointNum; ?>" id="evseconlp<?php echo $chargepointNum; ?>" class="form-control">
										<option <?php if(${'evseconlp'.$chargepointNum.'old'} == "ipevse\n") echo "selected" ?> value="ipevse">openWB Satellit</option>
										<option <?php if(${'evseconlp'.$chargepointNum.'old'} == "extopenwb\n") echo "selected" ?> value="extopenwb">externe openWB</option>
									</select>
								</div>
							</div>
							<div id="evseconextopenwblp<?php echo $chargepointNum; ?>" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="chargep<?php echo $chargepointNum; ?>ip" class="col-md-4 col-form-label">IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="chargep<?php echo $chargepointNum; ?>ip" id="chargep<?php echo $chargepointNum; ?>ip" value="<?php echo trim(${'chargep'.$chargepointNum.'ipold'}) ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse im Format: 192.168.0.12<br>
												Die externe openWB muss die Option "openWB ist nur ein Ladepunkt" aktiv haben!
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="chargep<?php echo $chargepointNum; ?>cp" class="col-md-4 col-form-label">Ladepunkt an der externen openWB</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="2" step="1" name="chargep<?php echo $chargepointNum; ?>cp" id="chargep<?php echo $chargepointNum; ?>cp" value="<?php echo trim(${'chargep'.$chargepointNum.'cpold'}) ?>">
											<span class="form-text small">Ist die externe openWB eine Duo gibt diese Option an ob Ladepunkt 1 oder 2 angesprochen werden soll.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="evseconipevselp<?php echo $chargepointNum; ?>" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="evseiplp<?php echo $chargepointNum; ?>" class="col-md-4 col-form-label">EVSE IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evseiplp<?php echo $chargepointNum; ?>" id="evseiplp<?php echo $chargepointNum; ?>" value="<?php echo trim(${'evseiplp'.$chargepointNum.'old'}) ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse im Format: 192.168.0.12
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="evseidlp<?php echo $chargepointNum; ?>" class="col-md-4 col-form-label">EVSE ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="evseidlp<?php echo $chargepointNum; ?>" id="evseidlp<?php echo $chargepointNum; ?>" value="<?php echo trim(${'evseidlp'.$chargepointNum.'old'}) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID der EVSE.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp<?php echo $chargepointNum; ?>ip" class="col-md-4 col-form-label">Ladeleistung IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpmlp<?php echo $chargepointNum; ?>ip" id="mpmlp<?php echo $chargepointNum; ?>ip" value="<?php echo trim(${'mpmlp'.$chargepointNum.'ipold'}) ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse im Format: 192.168.0.12. IP Adresse des Modbus Ethernet Konverters.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp<?php echo $chargepointNum; ?>id" class="col-md-4 col-form-label">Ladeleistung ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpmlp<?php echo $chargepointNum; ?>id" id="mpmlp<?php echo $chargepointNum; ?>id" value="<?php echo trim(${'mpmlp'.$chargepointNum.'idold'}) ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
						</div>
						<script>
							function display_lp<?php echo $chargepointNum; ?> () {
								hideSection('evseconipevselp<?php echo $chargepointNum; ?>');
								hideSection('evseconextopenwblp<?php echo $chargepointNum; ?>');

								if($('#evseconlp<?php echo $chargepointNum; ?>').val() == 'extopenwb') {
									showSection('evseconextopenwblp<?php echo $chargepointNum; ?>');
								}
								if($('#evseconlp<?php echo $chargepointNum; ?>').val() == 'ipevse') {
									showSection('evseconipevselp<?php echo $chargepointNum; ?>');
								}
							}

							function display_lastmanagementlp<?php echo $chargepointNum; ?>() {
								if($('#lastmanagementlp<?php echo $chargepointNum; ?>Off').prop("checked")) {
									hideSection('lastlp<?php echo $chargepointNum; ?>mman');
								}
								else {
									showSection('lastlp<?php echo $chargepointNum; ?>mman');
									display_lp<?php echo $chargepointNum; ?>();
								}
							}

							$(function() {
								display_lastmanagementlp<?php echo $chargepointNum; ?>();

								$('#evseconlp<?php echo $chargepointNum; ?>').change( function(){
									display_lp<?php echo $chargepointNum; ?>();
								});
								$('input[type=radio][name=lastmanagementlp<?php echo $chargepointNum; ?>]').change(function() {
									display_lastmanagementlp<?php echo $chargepointNum; ?>();
								});
							});
						</script>
					</div>
				<?php } ?>

				<div class="form-row text-center">
					<div class="col">
						<button type="submit" class="btn btn-success">Speichern</button>
					</div>
				</div>
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
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
			  <small>Sie befinden sich hier: Einstellungen/Modulkonfiguration</small>
			</div>
		</footer>

		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navModulkonfigurationLpBeta').addClass('disabled');
				}
			);

		</script>

	</body>
</html>
