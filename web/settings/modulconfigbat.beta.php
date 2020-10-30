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
				if(strpos($line, "bezug_id=") !== false) {
					list(, $bezug_idold) = explode("=", $line);
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
				if(strpos($line, "soc_vin=") !== false) {
					list(, $soc_vinold) = explode("=", $line);
				}
				if(strpos($line, "solarworld_emanagerip=") !== false) {
					list(, $solarworld_emanageripold) = explode("=", $line);
				}
				if(strpos($line, "femskacopw=") !== false) {
					list(, $femskacopwold) = explode("=", $line);
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
				if(strpos($line, "speicherkitversion=") !== false) {
					list(, $speicherkitversionold) = explode("=", $line);
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
				if(strpos($line, "wr1extprod=") !== false) {
					list(, $wr1extprodold) = explode("=", $line);
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
				if(strpos($line, "solaredgepvslave4=") !== false) {
					list(, $solaredgeipslave4old) = explode("=", $line);
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
				if(strpos($line, "usevartamodbus=") !== false) {
					list(, $usevartamodbusold) = explode("=", $line);
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
				if(strpos($line, "froniusvar2=") !== false) {
					list(, $froniusvar2old) = explode("=", $line);
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
			$httpevseipold = str_replace( "'", "", $httpevseipold);
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
			$socpassold = str_replace( "'", "", $socpassold);
			$soc2passold = str_replace( "'", "", $soc2passold);
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Modulkonfiguration</h1>
			<form action="./tools/debugrequest.php" method="POST">

				<!-- Speicher -->
				<div class="card border-warning">
					<div class="card-header bg-warning">
						Speicher-Modul
					</div>
					<div class="card-body">
						<div class="form-row mb-1">
							<label for="speichermodul" class="col-md-4 col-form-label">Speicher-Modul</label>
							<div class="col">
								<select name="speichermodul" id="speichermodul" class="form-control">
									<option <?php if($speichermodulold == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
									<option <?php if($speichermodulold == "speicher_mpm3pm\n") echo "selected" ?> value="speicher_mpm3pm">openWB Speicher Kit</option>
									<option <?php if($speichermodulold == "speicher_http\n") echo "selected" ?> value="speicher_http">HTTP Abfrage</option>
									<option <?php if($speichermodulold == "mpm3pmspeicher\n") echo "selected" ?> value="mpm3pmspeicher">MPM3PM</option>
									<option <?php if($speichermodulold == "speicher_bydhv\n") echo "selected" ?> value="speicher_bydhv">BYD HV</option>
									<option <?php if($speichermodulold == "speicher_fronius\n") echo "selected" ?> value="speicher_fronius">Fronius Speicher (Solar Battery oder BYD HV/HVS/HVM)</option>
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
									<option <?php if($speichermodulold == "speicher_fems\n") echo "selected" ?> value="speicher_fems">openEMS / Fenecon FEMS / Kaco Hy-Control</option>
									<option <?php if($speichermodulold == "speicher_siemens\n") echo "selected" ?> value="speicher_siemens">Siemens</option>
									<option <?php if($speichermodulold == "speicher_rct\n") echo "selected" ?> value="speicher_rct">RCT</option>
									<option <?php if($speichermodulold == "speicher_sungrow\n") echo "selected" ?> value="speicher_sungrow">Sungrow Hybrid</option>
								</select>
							</div>
						</div>

						<div id="divspeicherlgessv1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="lgessv1ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="lgessv1ip" id="lgessv1ip" value="<?php echo trim($lgessv1ipold) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="lgessv1pass" class="col-md-4 col-form-label">Password</label>
									<div class="col">
										<input class="form-control" type="password" name="lgessv1pass" id="lgessv1pass" value="<?php echo trim($lgessv1passold) ?>">
										<span class="form-text small">
											Standardmäßig ist hier die Registrierungsnummer des LG ESS 1.0VI anzugeben.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="ess_api_ver" class="col-md-4 col-form-label">API-Version</label>
									<div class="col">
										<select name="ess_api_ver" id="ess_api_ver" class="form-control">
											<option <?php if($ess_api_ver_old == "10.2019\n") echo "selected" ?> value="10.2019">API-Version Oktober 2019</option>
											<option <?php if($ess_api_ver_old == "01.2020\n") echo "selected" ?> value="01.2020">API-Version Januar 2020</option>
										</select>
										<span class="form-text small">
											Falls Sie nicht wissen, welche API-Version benötigen, benutzten Sie bitte die neueste API-Version.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicherkit" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="speicherkitversion" class="col-md-4 col-form-label">Version des openWB Speicher Kits</label>
									<div class="col">
										<select name="speicherkitversion" id="speicherkitversion" class="form-control">
											<option <?php if($speicherkitversionold == 0) echo "selected" ?> value="0">Dreiphasig (MPM3PM)</option>
											<option <?php if($speicherkitversionold == 1) echo "selected" ?> value="1">Einphasig (SDM120)</option>
										</select>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichermqtt" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Per MQTT zu schreiben:<br>
								<span class="text-info">openWB/set/houseBattery/W</span> Speicherleistung in Watt, int, positiv Ladung, negativ Entladung<br>
								<span class="text-info">openWB/set/houseBattery/WhImported</span> Geladene Energie in Wh, float, nur positiv<br>
								<span class="text-info">openWB/set/houseBattery/WhExported</span> Entladene Energie in Wh, float, nur positiv<br>
								<span class="text-info">openWB/set/houseBattery/%Soc</span> Ladestand des Speichers, int, 0-100
							</div>
						</div>

						<div id="divspeichervictron" class="hide">
							<div class="alert alert-info">
								Konfiguration im Bezug Victron Modul.
							</div>
						</div>

						<div id="divspeicherfems" class="hide">
							<div class="alert alert-info">
								Konfiguration im Bezug Fenecon Modul.
							</div>
						</div>

						<div id="divspeicherip" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="speicher1_ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="speicher1_ip" id="speicher1_ip" value="<?php echo trim($speicher1_ipold) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichersiemens" class="hide">
							<div class="alert alert-info">
								Im Siemens Speicher muss als Schnittstelle <span class="text-info">openWB</span> gewählt werden.
							</div>
						</div>

						<div id="divspeichersungrow" class="hide">
							<div class="alert alert-info">
								Es muss Sungrow als PV und EVU Modul gewählt werden.
							</div>
						</div>

						<div id="divspeicherrct" class="hide">
							<div class="alert alert-info">
								Konfiguration im zugehörigen EVU Modul.
							</div>
						</div>

						<div id="divspeichervarta" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="vartaspeicherip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="vartaspeicherip" id="vartaspeicherip" value="<?php echo trim($vartaspeicheripold) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="usevartamodbus" class="col-md-4 col-form-label">Ausleseart Modbus</label>
									<div class="col">
										<select name="usevartamodbus" id="usevartamodbus" class="form-control">
											<option <?php if($usevartamodbusold == "0\n") echo "selected" ?> value="0">Nein</option>
											<option <?php if($usevartamodbusold == "1\n") echo "selected" ?> value="1">Ja</option>
										</select>
										<span class="form-text small">Für z.B. Pulse, Element, Neo.</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicheralphaess" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>

						<div id="divspeicherpw" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="speicherpwip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="speicherpwip" id="speicherpwip" value="<?php echo trim($speicherpwipold) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicherseco" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sonnenecoip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sonnenecoip" id="sonnenecoip" value="<?php echo trim($sonnenecoipold) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sonnenecoalternativ" class="col-md-4 col-form-label">Datenverbindung</label>
									<div class="col">
										<select name="sonnenecoalternativ" id="sonnenecoalternativ" class="form-control">
											<option <?php if($sonnenecoalternativold == "0\n") echo "selected" ?> value="0">Rest-API 1 (z. B. Eco 4)</option>
											<option <?php if($sonnenecoalternativold == "2\n") echo "selected" ?> value="2">Rest-API 2 (z. B. ECO 6)</option>
											<option <?php if($sonnenecoalternativold == "1\n") echo "selected" ?> value="1">JSON-API (z. B. ECO 8)</option>
										</select>
										<span class="form-text small">
											Je nach Sonnen Batterie muss die richtige Datenverbindung ausgewählt werden.
											Folgende URLs werden zum Abruf der Daten genutzt und können auch manuell über einen Browser abgefragt werden, um die richtige Einstellung zu finden:<br>
											Rest-API 1: [ip]:7979/rest/devices/battery<br>
											Rest-API 2: [ip]:7979/rest/devices/battery/M05<br>
											JSON-API: [ip]/api/v1/status
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichere3dc" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="e3dcip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^(none)|((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="e3dcip" id="e3dcip" value="<?php echo trim($e3dcipold) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="e3dcextprod" class="col-md-4 col-form-label">Externe Produktion des E3DC mit einbeziehen</label>
									<div class="col">
										<select name="e3dcextprod" id="e3dcextprod" class="form-control">
											<option <?php if($e3dcextprodold == "0\n") echo "selected" ?> value="0">Nein</option>
											<option <?php if($e3dcextprodold == "1\n") echo "selected" ?> value="1">Ja</option>
										</select>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="e3dc2ip" class="col-md-4 col-form-label">2. IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^(none)|((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="e3dc2ip" id="e3dc2ip" value="<?php echo trim($e3dc2ipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Wenn nicht vorhanden none eintragen.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichersbs25" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sbs25ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sbs25ip" id="sbs25ip" value="<?php echo trim($sbs25ipold) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichersunnyisland" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sunnyislandip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sunnyislandip" id="sunnyislandip" value="<?php echo trim($sunnyislandipold) ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichersolaredge" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="solaredgespeicherip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="solaredgespeicherip" id="solaredgespeicherip" value="<?php echo trim($solaredgespeicheripold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Solaredge Wechselrichters an dem der Speicher angeschlossen ist.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicherplenti" class="hide">
							<div class="alert alert-info">
								Ein am 1. Kostal Plenticore angeschlossener Speicher setzt einen EM300/KSEM voraus.
								Nach entsprechender Auswahl im Strombezugsmessmodul und Konfiguration der IP des WR im PV-Modul erfolgt das Auslesen des Speichers über den WR ohne weitere Einstellungen.
							</div>
						</div>

						<div id="divspeicherfronius" class="hide">
							<div class="alert alert-info">
								Die IP des Wechselrichters wird im dazugehörigen Fronius PV-Modul eingestellt.
							</div>
						</div>

						<div id="divspeicherhttp" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="speicherleistung_http" class="col-md-4 col-form-label">Leistung URL</label>
									<div class="col">
										<input class="form-control" type="text" name="speicherleistung_http" id="speicherleistung_http" value="<?php echo htmlspecialchars(trim($speicherleistung_httpold)) ?>">
										<span class="form-text small">
											Gültige Werte URL. Vollständige URL die den aktuellen Leistungswert in Watt wiedergibt.
											Erwartet wird eine Ganzzahl. Positiv heißt Speicher wird geladen und eine negative Zahl bedeutet das der Speicher entladen wird.
											Das Modul dient dazu bei NurPV Ladung eine Entladung des Speichers zu verhindern.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="speichersoc_http" class="col-md-4 col-form-label">SoC URL</label>
									<div class="col">
										<input class="form-control" type="text" name="speichersoc_http" id="speichersoc_http" value="<?php echo htmlspecialchars(trim($speichersoc_httpold)) ?>">
										<span class="form-text small">
											Gültige Werte URL. Vollständige URL die den aktuellen SoC wiedergibt.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="speicherikwh_http" class="col-md-4 col-form-label">Import Wh URL</label>
									<div class="col">
										<input class="form-control" type="text" name="speicherikwh_http" id="speicherikwh_http" value="<?php echo htmlspecialchars(trim($speicherikwh_httpold)) ?>">
										<span class="form-text small">
											Gültige Werte URL. Wenn nicht vorhanden, none eintragen.
											Vollständige URL die den Zählerstand der Batterieladung in WattStunden wiedergibt. Erwartet wird eine Ganzzahl.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="speicherekwh_http" class="col-md-4 col-form-label">Export Wh URL</label>
									<div class="col">
										<input class="form-control" type="text" name="speicherekwh_http" id="speicherekwh_http" value="<?php echo htmlspecialchars(trim($speicherekwh_httpold)) ?>">
										<span class="form-text small">
											Gültige Werte URL. Wenn nicht vorhanden, none eintragen.
											Vollständige URL die den Zählerstand der Batterieentladung in WattStunden wiedergibt. Erwartet wird eine Ganzzahl.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicherbydhv" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="bydhvuser" class="col-md-4 col-form-label">Benutzername</label>
									<div class="col">
										<input class="form-control" type="text" name="bydhvuser" id="bydhvuser" value="<?php echo trim($bydhvuserold) ?>">
									</div>
								</div>
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="bydhvpass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="bydhvpass" id="bydhvpass" value="<?php echo trim($bydhvpassold) ?>">
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bydhvip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bydhvip" id="bydhvip" value="<?php echo trim($bydhvipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichermpm3pm" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="mpm3pmspeichersource" class="col-md-4 col-form-label">Source</label>
									<div class="col">
										<input class="form-control" type="text" name="mpm3pmspeichersource" id="mpm3pmspeichersource" value="<?php echo trim($mpm3pmspeichersourceold) ?>">
										<span class="form-text small">Gültige Werte /dev/ttyUSBx , /dev/virtualcomX bei Verwendung mit Ethernet Modbus.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmspeicherid" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmspeicherid" id="mpm3pmspeicherid" value="<?php echo trim($mpm3pmspeicheridold) ?>">
										<span class="form-text small">Gültige Werte 1-254.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmspeicherpv" class="col-md-4 col-form-label">PV mit einberechnen?</label>
									<div class="col">
										<select name="mpm3pmspeicherpv" id="mpm3pmspeicherpv" class="form-control">
											<option <?php if($mpm3pmspeicherpvold == "0\n") echo "selected" ?> value="0">Keine extra Berechnung</option>
											<option <?php if($mpm3pmspeicherpvold == "1\n") echo "selected" ?> value="1">Subtrahieren der PV Leistung</option>
										</select>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmspeicherlanip" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpm3pmspeicherlanip" id="mpm3pmspeicherlanip" value="<?php echo trim($mpm3pmspeicherlanipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
							</div>
						</div>

						<script>
							function display_speichermodul() {
								hideSection('divspeichermqtt');
								hideSection('divspeicherhttp');
								hideSection('divspeichermpm3pm');
								hideSection('divspeicherbydhv');
								hideSection('divspeicherfronius');
								hideSection('divspeichere3dc');
								hideSection('divspeichersbs25');
								hideSection('divspeichersolaredge');
								hideSection('divspeicherpw');
								hideSection('divspeicherplenti');
								hideSection('divspeichersunnyisland');
								hideSection('divspeicherseco');
								hideSection('divspeicherkit');
								hideSection('divspeichervarta');
								hideSection('divspeicheralphaess');
								hideSection('divspeichervictron');
								hideSection('divspeicherlgessv1');
								hideSection('divspeicherfems');
								hideSection('divspeicherip');
								hideSection('divspeichersiemens');
								hideSection('divspeicherrct');
								hideSection('divspeichersungrow');

								if($('#speichermodul').val() == 'speicher_fems') {
									showSection('divspeicherfems');
								}
								if($('#speichermodul').val() == 'speicher_rct') {
									showSection('divspeicherrct');
								}
								if($('#speichermodul').val() == 'speicher_siemens') {
									showSection('divspeicherip');
									showSection('divspeichersiemens');
								}
								if($('#speichermodul').val() == 'speicher_sungrow') {
									showSection('divspeicherip');
									showSection('divspeichersungrow');
								}
								if($('#speichermodul').val() == 'speicher_alphaess') {
									showSection('divspeicheralphaess');
								}
								if($('#speichermodul').val() == 'speicher_mqtt') {
									showSection('divspeichermqtt');
								}
								if($('#speichermodul').val() == 'speicher_victron') {
									showSection('divspeichervictron');
								}
								if($('#speichermodul').val() == 'speicher_mpm3pm') {
									showSection('divspeicherkit');
								}
								if($('#speichermodul').val() == 'speicher_sonneneco') {
									showSection('divspeicherseco');
								}
								if($('#speichermodul').val() == 'speicher_http')   {
									showSection('divspeicherhttp');
								}
								if($('#speichermodul').val() == 'mpm3pmspeicher')   {
									showSection('divspeichermpm3pm');
								}
								if($('#speichermodul').val() == 'speicher_bydhv')   {
									showSection('divspeicherbydhv');
								}
								if($('#speichermodul').val() == 'speicher_fronius')   {
									showSection('divspeicherfronius');
								}
								if($('#speichermodul').val() == 'speicher_e3dc')   {
									showSection('divspeichere3dc');
								}
								if($('#speichermodul').val() == 'speicher_sbs25')   {
									showSection('divspeichersbs25');
								}
								if($('#speichermodul').val() == 'speicher_solaredge')   {
									showSection('divspeichersolaredge');
								}
								if($('#speichermodul').val() == 'speicher_varta')   {
									showSection('divspeichervarta');
								}
								if($('#speichermodul').val() == 'speicher_powerwall')   {
									showSection('divspeicherpw');
								}
								if($('#speichermodul').val() == 'speicher_kostalplenticore')   {
									showSection('divspeicherplenti');
								}
								if($('#speichermodul').val() == 'speicher_sunnyisland')   {
									showSection('divspeichersunnyisland');
								}
								if($('#speichermodul').val() == 'speicher_lgessv1')   {
									showSection('divspeicherlgessv1');
								}
							}

							$(function() {
								$('#speichermodul').change( function(){
									display_speichermodul();
								});

								display_speichermodul();
							});
						</script>
					</div>
				</div>

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
					$('#navModulkonfigurationBatBeta').addClass('disabled');
				}
			);

		</script>

	</body>
</html>
