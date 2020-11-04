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

				<!-- EVU -->
				<div class="card border-danger">
					<div class="card-header bg-danger">
						Strombezugsmessmodul (EVU-Übergabepunkt)
					</div>
					<div class="card-body">
						<div class="form-row mb-1">
							<label for="wattbezugmodul" class="col-md-4 col-form-label">Strombezugsmodul</label>
							<div class="col">
								<select name="wattbezugmodul" id="wattbezugmodul" class="form-control">
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
									<option <?php if($wattbezugmodulold == "bezug_fems\n") echo "selected" ?> value="bezug_fems">openEMS / Fenecon FEMS / Kaco Hy-Control</option>
									<option <?php if($wattbezugmodulold == "bezug_solarworld\n") echo "selected" ?> value="bezug_solarworld">Solarworld</option>
									<option <?php if($wattbezugmodulold == "bezug_siemens\n") echo "selected" ?> value="bezug_siemens">Siemens Speicher</option>
									<option <?php if($wattbezugmodulold == "bezug_powerdog\n") echo "selected" ?> value="bezug_powerdog">Powerdog</option>
									<option <?php if($wattbezugmodulold == "bezug_rct\n") echo "selected" ?> value="bezug_rct">RCT</option>
									<option <?php if($wattbezugmodulold == "bezug_varta\n") echo "selected" ?> value="bezug_varta">Varta Speicher</option>
								</select>
							</div>
						</div>
						<div id="wattbezugalphaess" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="wattbezugsonneneco" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich. Es muss beim Speicher die alternative Methode ausgewählt werden, da die Daten nur von der JSON-API übergeben werden.
							</div>
						</div>
						<div id="wattbezugvarta" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich. Es muss beim Speicher Varta ausgewählt werden.
							</div>
						</div>
						<div id="wattbezugmqtt" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Per MQTT zu schreiben:<br>
								<span class="text-info">openWB/set/evu/W</span> Bezugsleistung in Watt, int, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/APhase1</span> Strom in Ampere für Phase 1, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/APhase2</span> Strom in Ampere für Phase 2, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/APhase3</span> Strom in Ampere für Phase 3, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/WhImported</span> Bezogene Energie in Wh, float, Punkt als Trenner, nur positiv<br>
								<span class="text-info">openWB/set/evu/WhExported</span> Eingespeiste Energie in Wh, float, Punkt als Trenner, nur positiv<br>
								<span class="text-info">openWB/set/evu/VPhase1</span> Spannung in Volt für Phase 1, float, Punkt als Trenner<br>
								<span class="text-info">openWB/set/evu/VPhase2</span> Spannung in Volt für Phase 2, float, Punkt als Trenner<br>
								<span class="text-info">openWB/set/evu/VPhase3</span> Spannung in Volt für Phase 3, float, Punkt als Trenner<br>
								<span class="text-info">openWB/set/evu/HzFrequenz</span> Netzfrequenz in Hz, float, Punkt als Trenner<br>
							</div>
						</div>
						<div id="wattbezuglgessv1" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen Speichermodul des LG ESS 1.0VI erforderlich. Als PV-Modul auch LG ESS 1.0VI wählen!
							</div>
						</div>
						<div id="wattbezugip" class="hide">
							<div class="form-row mb-1">
								<label for="bezug1_ip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bezug1_ip" id="bezug1_ip" value="<?php echo trim($bezug1_ipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsiemens" class="hide">
							<div class="card-text alert alert-info">
								IP Adresse des Siemens Speichers eingeben. Im Siemens Speicher muss die Schnittstelle openWB gewählt werden.
							</div>
						</div>
						<div id="wattbezugrct" class="hide">
							<div class="card-text alert alert-info">
								IP Adresse des RCT Speichers eingeben.
							</div>
						</div>
						<div id="wattbezugpowerdog" class="hide">
							<div class="card-text alert alert-info">
								IP Adresse des Powerdog eingeben. Im Powerdog muss die Schnittstelle ModbusTCP aktiviert werden.
							</div>
						</div>
						<div id="wattbezugethmpm3pm" class="hide">
							<div class="form-row mb-1">
								<label for="evukitversion" class="col-md-4 col-form-label">Version des openWB evu Kits</label>
								<div class="col">
									<select name="evukitversion" id="evukitversion" class="form-control">
										<option <?php if($evukitversionold == 0) echo "selected" ?> value="0">EVU Kit MPM3PM</option>
										<option <?php if($evukitversionold == 1) echo "selected" ?> value="1">EVU Kit var 2 Lovato</option>
										<option <?php if($evukitversionold == 2) echo "selected" ?> value="2">EVU Kit SDM</option>
									</select>
								</div>
							</div>
						</div>
						<div id="wattbezugsolarview" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen PV Modul erforderlich.
							</div>
						</div>
						<div id="wattbezugpowerwall" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich. Mit diesem Modul ist kein Lastmanagement / Hausanschlussüberwachung möglich.
							</div>
						</div>
						<div id="wattbezugvictrongx" class="hide">
							<div class="form-row mb-1">
								<label for="bezug_victronip" class="col-md-4 col-form-label">Victron IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bezug_victronip" id="bezug_victronip" value="<?php echo trim($bezug_victronipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										IP Adresse des Victron, z.B. GX.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="bezug_id" class="col-md-4 col-form-label">ID</label>
								<div class="col">
									<input class="form-control" type="text" name="bezug_id" id="bezug_id" value="<?php echo trim($bezug_idold) ?>">
									<span class="form-text small">Gültige Werte ID. ID Adresse</span>
								</div>
							</div>
						</div>
						<div id="wattbezugfems" class="hide">
							<div class="form-row mb-1">
								<label for="femsip" class="col-md-4 col-form-label">Fenecon IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="femsip" id="femsip" value="<?php echo trim($femsipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										IP Adresse des Fenecon FEMS.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="femskacopw" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="femskacopw" id="femskacopw" value="<?php echo htmlspecialchars(trim($femskacopwold)) ?>">
									<span class="form-text small">
										Bei Nutzung von Fenecon FEMS ist das Passwort im Normalfall user, bei Kaco mit Hy-Control ist das Passwort meist admin.
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsolarworld" class="hide">
							<div class="form-row mb-1">
								<label for="solarworld_emanagerip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="solarworld_emanagerip" id="solarworld_emanagerip" value="<?php echo trim($solarworld_emanageripold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										IP Adresse des Solarworld eManager.
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugdiscovergy" class="hide">
							<div class="form-row mb-1">
								<label for="discovergyuser" class="col-md-4 col-form-label">Discovergy Username (Email)</label>
								<div class="col">
									<input class="form-control" type="email" name="discovergyuser" id="discovergyuser" value="<?php echo htmlspecialchars(trim($discovergyuserold)) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="discovergypass" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="discovergypass" id="discovergypass" value="<?php echo htmlspecialchars(trim($discovergypassold)) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="discovergyevuid" class="col-md-4 col-form-label">Meter ID</label>
								<div class="col">
									<input class="form-control" type="text" name="discovergyevuid" id="discovergyevuid" value="<?php echo trim($discovergyevuidold) ?>">
									<span class="form-text small">
										Gültige Werte ID. Um die ID herauszufinden mit dem Browser die Adresse "https://api.discovergy.com/public/v1/meters" aufrufen und dort Benutzername und Passwort eingeben.
										Hier wird nun u.a. die ID des Zählers angezeigt.
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugkostalsmartenergymeter" class="hide">
							<div class="form-row mb-1">
								<label for="ksemip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="ksemip" id="ksemip" value="<?php echo trim($ksemipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugkostalpiko" class="hide">
							<div class="card-text alert alert-info">
								IP Adresse wird im PV Modul konfiguriert. Angeschlossenes Meter erforderlich. Der WR liefert Werte nur solange er auch PV Leistung liefert. Nachts geht er in den Standby.
								Die Hausanschlussüberwachung ist nur aktiv wenn der Wechselrichter auch aktiv ist. Ein extra PV-Modul muss nicht mehr ausgewählt werden.
							</div>
						</div>
						<div id="wattbezugplentihaus" class="hide">
							<div class="card-text alert alert-info">
								Dieses Modul erfordert als 1. PV-Modul das Modul "Kostal Plenticore". Dieses wird automatisch fest eingestellt. Der EM300 bzw. das KSEM muss am 1. Plenticore angeschlossen sein.
								Ein am 1. Plenticore angeschlossener Speicher wird ebenfalls ohne weitere Einstellung ausgelesen, das Speicher-Modul wird dazu entsprechend voreingestellt.
								Am 2. Plenticore darf kein Speicher angeschlossen sein, da dies die weiteren Berechnungen verfälscht.
								Die Einbauposition des EM300/KSEM (Hausverbrauchs-Zweig = Pos. 1 oder Netzanschluss-Zweig = Pos. 2) ist anzugeben.
							</div>
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Einbauposition</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($kostalplenticorehausold == 0) echo " active" ?>">
												<input type="radio" name="kostalplenticorehaus" id="kostalplenticorehausOff" value="0"<?php if($kostalplenticorehausold == 0) echo " checked=\"checked\"" ?>>Pos. 1
											</label>
											<label class="btn btn-outline-info<?php if($kostalplenticorehausold == 1) echo " active" ?>">
												<input type="radio" name="kostalplenticorehaus" id="kostalplenticorehausOn" value="1"<?php if($kostalplenticorehausold == 1) echo " checked=\"checked\"" ?>>Pos. 2
											</label>
										</div>
										<span class="form-text small">
											Hausverbrauchs-Zweig = Pos. 1 oder Netzanschluss-Zweig = Pos. 2
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugmpm3pm" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="mpm3pmevusource" class="col-md-4 col-form-label">MPM3PM Zähler EVU Source</label>
									<div class="col">
										<input class="form-control" type="text" name="mpm3pmevusource" id="mpm3pmevusource" value="<?php echo trim($mpm3pmevusourceold) ?>">
										<span class="form-text small">
											Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
											Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmevuid" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmevuid" id="mpm3pmevuid" value="<?php echo trim($mpm3pmevuidold) ?>">
										<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Einbauposition</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($mpm3pmevuhausold == 0) echo " active" ?>">
												<input type="radio" name="mpm3pmevuhaus" id="mpm3pmevuhausOff" value="0"<?php if($mpm3pmevuhausold == 0) echo " checked=\"checked\"" ?>>Pos. 1
											</label>
											<label class="btn btn-outline-info<?php if($mpm3pmevuhausold == 1) echo " active" ?>">
												<input type="radio" name="mpm3pmevuhaus" id="mpm3pmevuhausOn" value="1"<?php if($mpm3pmevuhausold == 1) echo " checked=\"checked\"" ?>>Pos. 2
											</label>
										</div>
										<span class="form-text small">
											Wenn der MPM3PM EVU Zähler im Hausverbrauchszweig NACH den Ladepunkten angeschlossen ist, Pos. 2 auswählen.
											Z.B. auch zu nutzen wenn der Ladepunkt an einem seperaten Rundsteuerempfänger(=extra Zähler) angeschlossen ist.
											Bei gesetzter Pos. 2 werden die Ladeströme der Ladepunkte zu den Strömen gemessen am EVU Zähler hinzuaddiert.
											Somit ist ein Lastmanagement / Hausanschlussüberwachung möglich. Auf korrekte Verkabelung ist zu achten!<br>
											EVU L1, LP1 L1, LP2 L2<br>
											EVU L2, LP1 L2, LP2 L3<br>
											EVU L3, LP1 L3, LP2 L1
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugnone" class="hide">
							<div class="form-row mb-1">
								<label for="hausbezugnone" class="col-md-4 col-form-label">Angenommener Hausverbrauch</label>
								<div class="col">
									<input class="form-control" type="number" min="0" step="100" name="hausbezugnone" id="hausbezugnone" value="<?php echo htmlspecialchars(trim($hausbezugnoneold)) ?>">
									<span class="form-text small">
										Gültige Werte Zahl. Wenn keine EVU Messung vorhanden ist kann hier ein Hausgrundverbrauch festgelegt werden.
										Daraus resultierend agiert die PV Regelung bei vorhandenem PV-Modul
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsdm" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sdm630modbusbezugsource" class="col-md-4 col-form-label">SDM Zähler EVU Source</label>
									<div class="col">
										<input class="form-control" type="text" name="sdm630modbusbezugsource" id="sdm630modbusbezugsource" value="<?php echo trim($sdm630modbusbezugsourceold) ?>">
										<span class="form-text small">
											Gültige Werte /dev/ttyUSBx, /dev/virtualcomx. Das "x" steht für den Adapter. Dies kann 0,1,2, usw sein. Serieller Port an dem der SDM angeschlossen ist.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sdm630modbusbezugid" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="sdm630modbusbezugid" id="sdm630modbusbezugid" value="<?php echo trim($sdm630modbusbezugidold) ?>">
										<span class="form-text small">
											Gültige Werte 1-254. Modbus ID des SDM. Getestet sind SDM230 & SDM630v2.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sdm630modbusbezuglanip" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sdm630modbusbezuglanip" id="sdm630modbusbezuglanip" value="<?php echo trim($sdm630modbusbezuglanipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Ist die Source "virtualcomX" wird automatisch ein Lan Konverter genutzt.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugvz" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="vzloggerip" class="col-md-4 col-form-label">Vzlogger IP Adresse inkl Port</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5]):[0-9]+$" name="vzloggerip" id="vzloggerip" value="<?php echo trim($vzloggeripold) ?>">
										<span class="form-text small">
											Gültige Werte IP:Port z.B. 192.168.0.12:8080
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="vzloggerline" class="col-md-4 col-form-label">Vzlogger Watt Zeile</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" name="vzloggerline" id="vzloggerline" value="<?php echo trim($vzloggerlineold) ?>">
										<span class="form-text small">
											Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br>
											Nun zählen in welcher Zeile die aktullen Watt stehen und diesen hier eintragen.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="vzloggerkwhline" class="col-md-4 col-form-label">Vzlogger Bezug kWh Zeile</label>
									<div class="col">
										<input class="form-control" type="text" name="vzloggerkwhline" id="vzloggerkwhline" value="<?php echo trim($vzloggerkwhlineold) ?>">
										<span class="form-text small">
											Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br>
											Nun zählen in welcher Zeile die Gesamt kWh stehen und diesen hier eintragen. Der Wert dient rein dem Logging.
											Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="vzloggerekwhline" class="col-md-4 col-form-label">Vzlogger Einspeisung kWh Zeile</label>
									<div class="col">
										<input class="form-control" type="text" name="vzloggerekwhline" id="vzloggerekwhline" value="<?php echo trim($vzloggerekwhlineold) ?>">
										<span class="form-text small">
											Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br>
											Nun zählen in welcher Zeile die Gesamt eingespeisten kWh stehen und diesen hier eintragen.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezughttp" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="bezug_http_w_url" class="col-md-4 col-form-label">Vollständige URL für den Watt Bezug</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_w_url" id="bezug_http_w_url" value="<?php echo htmlspecialchars(trim($bezug_http_w_urlold)) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Watt sein.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_ikwh_url" class="col-md-4 col-form-label">Vollständige URL für den kWh Bezug</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_ikwh_url" id="bezug_http_ikwh_url" value="<?php echo htmlspecialchars(trim($bezug_http_ikwh_urlold)) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Der Wert muss in WattStunden sein. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_ekwh_url" class="col-md-4 col-form-label">Vollständige URL für die kWh Einspeisung</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_ekwh_url" id="bezug_http_ekwh_url" value="<?php echo htmlspecialchars(trim($bezug_http_ekwh_urlold)) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Der Wert muss in WattStunden sein. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_l1_url" class="col-md-4 col-form-label">Vollständige URL für die Ampere Phase 1</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_l1_url" id="bezug_http_l1_url" value="<?php echo htmlspecialchars(trim($bezug_http_l1_urlold)) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Ampere sein. Bei nicht Nutzung auf none setzen.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_l2_url" class="col-md-4 col-form-label">Vollständige URL für die Ampere Phase 2</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_l2_url" id="bezug_http_l2_url" value="<?php echo htmlspecialchars(trim($bezug_http_l2_urlold)) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Ampere sein. Bei nicht Nutzung auf none setzen.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_l3_url" class="col-md-4 col-form-label">Vollständige URL für die Ampere Phase 3</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_l3_url" id="bezug_http_l3_url" value="<?php echo htmlspecialchars(trim($bezug_http_l3_urlold)) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Ampere sein. Bei nicht Nutzung auf none setzen.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugsmartme" class="hide">
							<div class="form-row mb-1">
								<label for="bezug_smartme_user" class="col-md-4 col-form-label">Smartme Benutzername</label>
								<div class="col">
									<input class="form-control" type="text" name="bezug_smartme_user" id="bezug_smartme_user" value="<?php echo htmlspecialchars(trim($bezug_smartme_userold)) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="bezug_smartme_pass" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="bezug_smartme_pass" id="bezug_smartme_pass" value="<?php echo htmlspecialchars(trim($bezug_smartme_passold)) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="bezug_smartme_url" class="col-md-4 col-form-label">Smartme Url</label>
								<div class="col">
									<input class="form-control" type="text" name="bezug_smartme_url" id="bezug_smartme_url" value="<?php echo trim($bezug_smartme_urlold) ?>">
								</div>
							</div>
						</div>
						<div id="wattbezugshm" class="hide">
							<div class="form-row mb-1">
								<label for="smaeshmbezugid" class="col-md-4 col-form-label">Seriennummer</label>
								<div class="col">
									<input class="form-control" type="text" name="smaeshmbezugid" id="smaeshmbezugid" value="<?php echo trim($smashmbezugidold) ?>">
									<span class="form-text small">
										Gültige Werte: Seriennummer. Hier die Seriennummer des SMA Meter für Bezug/Einspeisung anzugeben.
										Ist nur erforderlich wenn mehrere SMA HomeManager in Betrieb sind, ansonsten none eintragen. Funktioniert auch mit Energy Meter statt Home Manager.
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsmartfox" class="hide">
							<div class="form-row mb-1">
								<label for="bezug_smartfox_ip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bezug_smartfox_ip" id="bezug_smartfox_ip" value="<?php echo trim($bezug_smartfox_ipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsma" class="hide">
							<div class="form-row mb-1">
								<label for="smaemdbezugid" class="col-md-4 col-form-label">Seriennummer des SMA Energy Meter</label>
								<div class="col">
									<input class="form-control" type="text" name="smaemdbezugid" id="smaemdbezugid" value="<?php echo trim($smaemdbezugidold) ?>">
									<span class="form-text small">
										Gültige Werte Seriennummer. Hier die Seriennummer des SMA Meter für Bezug/Einspeisung angeben<br>
										Infos zum SMA Energy Meter <a href="https://github.com/snaptec/openWB#extras">HIER</a>
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugfronius" class="hide">
							<div class="card-text alert alert-info">
								Die IP des Wechselrichters wird im dazugehörigen Fronius PV-Modul eingestellt.
							</div>
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Meter ID</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($froniuserzeugungold == 0) echo " active" ?>">
												<input type="radio" name="froniuserzeugung" id="froniuserzeugung0" value="0"<?php if($froniuserzeugungold == 0) echo " checked=\"checked\"" ?>>0
											</label>
											<label class="btn btn-outline-info<?php if($froniuserzeugungold == 1) echo " active" ?>">
												<input type="radio" name="froniuserzeugung" id="froniuserzeugung1" value="1"<?php if($froniuserzeugungold == 1) echo " checked=\"checked\"" ?>>1
											</label>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kompatibilitätsmodus für die Primo Reihe</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($froniusprimoold == 0) echo " active" ?>">
												<input type="radio" name="froniusprimo" id="froniusprimoOff" value="0"<?php if($froniusprimoold == 0) echo " checked=\"checked\"" ?>>Aus
											</label>
											<label class="btn btn-outline-info<?php if($froniusprimoold == 1) echo " active" ?>">
												<input type="radio" name="froniusprimo" id="froniusprimoOn" value="1"<?php if($froniusprimoold == 1) echo " checked=\"checked\"" ?>>An
											</label>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kompatibilitätsmodus für Gen24 / neuere Symo</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($froniusvar2old == 0) echo " active" ?>">
												<input type="radio" name="froniusvar2" id="froniusvar2Off" value="0"<?php if($froniusvar2old == 0) echo " checked=\"checked\"" ?>>Aus
											</label>
											<label class="btn btn-outline-info<?php if($froniusvar2old == 1) echo " active" ?>">
												<input type="radio" name="froniusvar2" id="froniusvar2On" value="1"<?php if($froniusvar2old == 1) echo " checked=\"checked\"" ?>>An
											</label>
										</div>
										<span class="form-text small">
											Gegebenenfalls auch für alte Modelle nach einem Softwareupdate erforderlich.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugjson" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="bezugjsonurl" class="col-md-4 col-form-label">Bezug URL</label>
									<div class="col">
										<input class="form-control" type="text" name="bezugjsonurl" id="bezugjsonurl" value="<?php echo htmlspecialchars(trim($bezugjsonurlold)) ?>">
										<span class="form-text small">
											Gültige Werte URL. Vollständige URL die die Json Antwort enthält.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezugjsonwatt" class="col-md-4 col-form-label">Json Abfrage für Watt</label>
									<div class="col">
										<input class="form-control" type="text" name="bezugjsonwatt" id="bezugjsonwatt" value="<?php echo htmlspecialchars(trim($bezugjsonwattold)) ?>">
										<span class="form-text small">
											Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
											Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> so muss hier <span class="text-info">.PowerOut</span> eingetragen werden.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezugjsonkwh" class="col-md-4 col-form-label">Json Abfrage für Bezug kWh</label>
									<div class="col">
										<input class="form-control" type="text" name="bezugjsonkwh" id="bezugjsonkwh" value="<?php echo htmlspecialchars(trim($bezugjsonkwhold)) ?>">
										<span class="form-text small">
											Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
											Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> so muss hier <span class="text-info">.PowerProduced</span> eingetragen werden.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="einspeisungjsonkwh" class="col-md-4 col-form-label">Json Abfrage für Einspeisung kWh</label>
									<div class="col">
										<input class="form-control" type="text" name="einspeisungjsonkwh" id="einspeisungjsonkwh" value="<?php echo htmlspecialchars(trim($einspeisungjsonkwhold)) ?>">
										<span class="form-text small">
											Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
											Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> so muss hier <span class="text-info">.PowerSelfSupplied</span> eingetragen werden.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugsolarlog" class="hide">
							<div class="card-text alert alert-info">
								Die zugehörige IP Adresse ist im PV Modul einzustellen.
							</div>
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kompatibilitätsmodus bei vorhandenem Speicher</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($bezug_solarlog_speichervold == 0) echo " active" ?>">
												<input type="radio" name="bezug_solarlog_speicherv" id="bezug_solarlog_speichervOff" value="0"<?php if($bezug_solarlog_speichervold == 0) echo " checked=\"checked\"" ?>>Nein
											</label>
											<label class="btn btn-outline-info<?php if($bezug_solarlog_speichervold == 1) echo " active" ?>">
												<input type="radio" name="bezug_solarlog_speicherv" id="bezug_solarlog_speichervOn" value="1"<?php if($bezug_solarlog_speichervold == 1) echo " checked=\"checked\"" ?>>Ja
											</label>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugsolaredge" class="hide">
							<div class="form-row mb-1">
								<label for="solaredgeip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="solaredgeip" id="solaredgeip" value="<?php echo trim($solaredgeipold) ?>">
									<span class="form-text small">
										Gültige Werte IP.<br>
										Hierfür muss ein EVU Zähler am SolarEdge Wechselrichter per Modbus angebunden sein.<br>
										Ebenso muss ModbusTCP am Wechselrichter aktiviert werden.<br>
										Der Zähler muss an erster Position im Wechselrichter konfiguriert sein, sonst ist eine Auslesung nicht möglich.
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezuge3dc" class="hide">
							<div class="card-text alert alert-info">
								Die IP des Speichers wird im dazugehörigen E3DC Speicher-Modul eingestellt.<br>
								Es kann nötig sein in den Einstellungen des E3DC ModbusTCP zu aktivieren.<br>
								Das Protokoll in den E3DC Einstellungen ist auf E3DC zu stellen.
							</div>
						</div>
						<div id="wattbezugsbs25" class="hide">
							<div class="card-text alert alert-info">
								Die IP des Speichers wird im dazugehörigen SMA SBS Speicher-Modul eingestellt.
							</div>
						</div>

						<div id="evuglaettungdiv" class="hide">
							<hr class="border-danger">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">EVU Glättung</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($evuglaettungaktold == 0) echo " active" ?>">
												<input type="radio" name="evuglaettungakt" id="evuglaettungaktOff" value="0"<?php if($evuglaettungaktold == 0) echo " checked=\"checked\"" ?>>Aus
											</label>
											<label class="btn btn-outline-info<?php if($evuglaettungaktold == 1) echo " active" ?>">
												<input type="radio" name="evuglaettungakt" id="evuglaettungaktOn" value="1"<?php if($evuglaettungaktold == 1) echo " checked=\"checked\"" ?>>An
											</label>
										</div>
									</div>
								</div>
								<div id="evuglaettungandiv">
									<div class="form-row mb-1">
										<label for="evuglaettung" class="col-md-4 col-form-label">Zeitspanne</label>
										<div class="col">
											<input class="form-control" type="number" min="10" step="10" name="evuglaettung" id="evuglaettung" value="<?php echo trim($evuglaettungold) ?>">
											<span class="form-text small">
												Gültige Werte: Zeit in Sekunden, z.B. 30,50,200.<br>
												Kombiniert die EVU Werte der letzten x Sekunden und bildet einen Mittelwert darüber.
												Sinnvoll, wenn öfter kurze Lastspitzen auftreten.
												Der Durchschnittswert wird auf der Hauptseite in Klammern angezeigt.
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>

						<script>
							function display_evuglaettung() {
								if($('#evuglaettungaktOff').prop("checked")) {
									hideSection('evuglaettungandiv');
								} else {
									showSection('evuglaettungandiv');
								}
							}

							/*
							function enable_pv_selector() {
								// enable das Dropdown-Element zur Auswahl des PV-Moduls
								document.getElementById("pvwattmodul").disabled=false;
							}

							function disable_pv_selector() {
								// disable das Dropdown-Element zur Auswahl des PV-Moduls
								document.getElementById("pvwattmodul").disabled=true;
							}
							*/

							function display_wattbezugmodul() {
								hideSection('evuglaettungdiv');
								hideSection('wattbezugvz');
								hideSection('wattbezugsdm');
								hideSection('wattbezugnone');
								hideSection('wattbezughttp');
								hideSection('wattbezugsma');
								hideSection('wattbezugsolarworld');
								hideSection('wattbezugfronius');
								hideSection('wattbezugjson');
								hideSection('wattbezugmpm3pm');
								hideSection('wattbezugsolarlog');
								hideSection('wattbezugsolaredge');
								hideSection('wattbezugshm');
								hideSection('wattbezugsmartme');
								hideSection('wattbezugsbs25');
								hideSection('wattbezuge3dc');
								hideSection('wattbezugethmpm3pm');
								hideSection('wattbezugplentihaus');
								hideSection('wattbezugkostalpiko');
								hideSection('wattbezugkostalsmartenergymeter');
								hideSection('wattbezugsmartfox');
								hideSection('wattbezugpowerwall');
								hideSection('wattbezugvictrongx');
								hideSection('wattbezugsolarview');
								hideSection('wattbezugdiscovergy');
								hideSection('wattbezuglgessv1');
								hideSection('wattbezugmqtt');
								hideSection('wattbezugsonneneco');
								hideSection('wattbezugvarta');
								hideSection('wattbezugfems');
								hideSection('wattbezugsiemens');
								hideSection('wattbezugpowerdog');
								hideSection('wattbezugrct');
								hideSection('wattbezugip');
								hideSection('wattbezugalphaess');

								// Auswahl PV-Modul generell erlauben
								//enable_pv_selector();
								if($('#wattbezugmodul').val() != 'none') {
									showSection('evuglaettungdiv');
									display_evuglaettung();
								} else {
									showSection('wattbezugnone');
								}
								if($('#wattbezugmodul').val() == 'bezug_alphaess') {
									showSection('wattbezugalphaess');
								}
								if($('#wattbezugmodul').val() == 'bezug_sonneneco') {
									showSection('wattbezugsonneneco');
								}
								if($('#wattbezugmodul').val() == 'bezug_varta') {
									showSection('wattbezugvarta');
								}
								if($('#wattbezugmodul').val() == 'bezug_siemens') {
									showSection('wattbezugsiemens');
									showSection('wattbezugip');

								}
								if($('#wattbezugmodul').val() == 'bezug_rct') {
									showSection('wattbezugrct');
									showSection('wattbezugip');

								}
								if($('#wattbezugmodul').val() == 'bezug_powerdog') {
									showSection('wattbezugpowerdog');
									showSection('wattbezugip');

								}
								if($('#wattbezugmodul').val() == 'bezug_fems') {
									showSection('wattbezugfems');
								}
								if($('#wattbezugmodul').val() == 'bezug_solarworld') {
									showSection('wattbezugsolarworld');
								}

								if($('#wattbezugmodul').val() == 'bezug_solarview') {
									showSection('wattbezugsolarview');
								}
								if($('#wattbezugmodul').val() == 'bezug_discovergy') {
									showSection('wattbezugdiscovergy');
								}
								if($('#wattbezugmodul').val() == 'bezug_mqtt') {
									showSection('wattbezugmqtt');
								}
								if($('#wattbezugmodul').val() == 'bezug_victrongx') {
									showSection('wattbezugvictrongx');
								}
								if($('#wattbezugmodul').val() == 'vzlogger') {
									showSection('wattbezugvz');
								}
								if($('#wattbezugmodul').val() == 'sdm630modbusbezug')   {
									showSection('wattbezugsdm');
								}
								if($('#wattbezugmodul').val() == 'bezug_http')   {
									showSection('wattbezughttp');
								}
								if($('#wattbezugmodul').val() == 'smaemd_bezug')   {
									showSection('wattbezugsma');
								}
								if($('#wattbezugmodul').val() == 'bezug_fronius_sm')   {
									showSection('wattbezugfronius');
								}
								if($('#wattbezugmodul').val() == 'bezug_fronius_s0')   {
									showSection('wattbezugfronius');
								}
								if($('#wattbezugmodul').val() == 'bezug_json')   {
									showSection('wattbezugjson');
								}
								if($('#wattbezugmodul').val() == 'bezug_mpm3pm')   {
									showSection('wattbezugmpm3pm');
								}
								if($('#wattbezugmodul').val() == 'bezug_solarlog')   {
									showSection('wattbezugsolarlog');
								}
								if($('#wattbezugmodul').val() == 'bezug_solaredge')   {
									showSection('wattbezugsolaredge');
								}
								if($('#wattbezugmodul').val() == 'bezug_smashm')   {
									showSection('wattbezugshm');
								}
								if($('#wattbezugmodul').val() == 'bezug_smartme')   {
									showSection('wattbezugsmartme');
								}
								if($('#wattbezugmodul').val() == 'bezug_e3dc')   {
									showSection('wattbezuge3dc');
								}
								if($('#wattbezugmodul').val() == 'bezug_ethmpm3pm')   {
									showSection('wattbezugethmpm3pm');
								}
								if($('#wattbezugmodul').val() == 'bezug_sbs25')   {
									showSection('wattbezugsbs25');
								}
								if($('#wattbezugmodul').val() == 'bezug_kostalplenticoreem300haus')   {
									showSection('wattbezugplentihaus');
									// keine Auswahl PV-Modul in dieser Konfiguration
									// Plenticore immer fix auswählen
									//document.getElementById('pvwattmodul').value = 'wr_plenticore';
									// und Einstellung sperren
									//disable_pv_selector();
									//display_pvwattmodul();
									// passendes Speichermodul 'optisch' voreinstellen, da automatisch alle Werte
									// mit aus dem WR gelesen werden
									//document.getElementById('speichermodul').value = 'speicher_kostalplenticore';
									//display_speichermodul();
								}
								if($('#wattbezugmodul').val() == 'bezug_kostalpiko')   {
									showSection('wattbezugkostalpiko');
								}
								if($('#wattbezugmodul').val() == 'bezug_ksem')   {
									showSection('wattbezugkostalsmartenergymeter');
								}
								if($('#wattbezugmodul').val() == 'bezug_smartfox')   {
									showSection('wattbezugsmartfox');
								}
								if($('#wattbezugmodul').val() == 'bezug_powerwall')   {
									showSection('wattbezugpowerwall');
								}
								if($('#wattbezugmodul').val() == 'bezug_lgessv1')   {
									showSection('wattbezuglgessv1');
								}
							}

							$(function() {
								display_wattbezugmodul();

								$('#wattbezugmodul').change( function(){
									display_wattbezugmodul();
								});

								$('input[type=radio][name=evuglaettungakt]').change(function() {
									display_evuglaettung();
								});
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
					$('#navModulkonfigurationEvuBeta').addClass('disabled');
				}
			);

		</script>

	</body>
</html>
