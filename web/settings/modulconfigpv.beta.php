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

				<!-- PV Module 1 -->
				<div class="card border-success">
					<div class="card-header bg-success">
						PV-Modul 1
					</div>
					<div class="card-body">
						<div class="form-row mb-1">
							<label for="pvwattmodul" class="col-md-4 col-form-label">PV-Modul</label>
							<div class="col">
								<select name="pvwattmodul" id="pvwattmodul" class="form-control">
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
									<option <?php if($pvwattmodulold == "wr_fems\n") echo "selected" ?> value="wr_fems">openEMS / Fenecon FEMS / Kaco Hy-Control</option>
									<option <?php if($pvwattmodulold == "wr_solarworld\n") echo "selected" ?> value="wr_solarworld">Solarworld</option>
									<option <?php if($pvwattmodulold == "wr_siemens\n") echo "selected" ?> value="wr_siemens">Siemens Speicher</option>
									<option <?php if($pvwattmodulold == "wr_powerdog\n") echo "selected" ?> value="wr_powerdog">Powerdog</option>
									<option <?php if($pvwattmodulold == "wr_rct\n") echo "selected" ?> value="wr_rct">RCT</option>
									<option <?php if($pvwattmodulold == "wr_huawei\n") echo "selected" ?> value="wr_huawei">Huawei</option>
									<option <?php if($pvwattmodulold == "wr_shelly\n") echo "selected" ?> value="wr_shelly">Shelly</option>
								</select>
							</div>
						</div>
						<div id="pvmqtt" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Per MQTT zu schreiben:<br>
								<span class="text-info">openWB/set/pv/W</span> PVleistung in Watt, int, negativ<br>
								<span class="text-info">openWB/set/pv/WhCounter</span> Erzeugte Energie in Wh, float, nur positiv
							</div>
						</div>
						<div id="pvlgessv1" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen Speichermodul des LG ESS 1.0VI erforderlich. Als EVU-Modul auch LG ESS 1.0VI wählen!
							</div>
						</div>
						<div id="pvip" class="hide">
							<div class="form-row mb-1">
								<label for="pv1_ipa" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="pv1_ipa" id="pv1_ipa" value="<?php echo trim($pv1_ipaold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="pvsiemens" class="hide">
							<!-- nothing here, just generic IP -->
						</div>
						<div id="pvpowerdog" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen EVU Modul.
							</div>
						</div>
						<div id="pvrct" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen EVU Modul.
							</div>
						</div>
						<div id="pvfems" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen EVU Modul des FEMS erforderlich.
							</div>
						</div>
						<div id="pvsolarworld" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen EVU Modul des Solarworld erforderlich.
							</div>
						</div>
						<div id="pvyouless" class="hide">
							<div class="form-row mb-1">
								<label for="wryoulessip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wryoulessip" id="wryoulessip" value="<?php echo trim($wryoulessipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="pvsunways" class="hide">
							<div class="form-row mb-1">
								<label for="wrsunwaysip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wrsunwaysip" id="wrsunwaysip" value="<?php echo trim($wrsunwaysipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrsunwayspw" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="wrsunwayspw" id="wrsunwayspw" value="<?php echo htmlspecialchars(trim($wrsunwayspwold)) ?>">
								</div>
							</div>
						</div>
						<div id="pvsolarlog" class="hide">
							<div class="form-row mb-1">
								<label for="bezug_solarlog_ip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bezug_solarlog_ip" id="bezug_solarlog_ip" value="<?php echo trim($bezug_solarlog_ipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										Wenn ein Eigenverbrauchszähler installiert ist bitte EVU SolarLog Modul nutzen. Wenn nicht dann dieses Modul.
									</span>
								</div>
							</div>
						</div>
						<div id="pvdiscovergy" class="hide">
							<div class="form-row mb-1">
								<label for="discovergypvid" class="col-md-4 col-form-label">Meter ID des Zählers</label>
								<div class="col">
									<input class="form-control" type="text" name="discovergypvid" id="discovergypvid" value="<?php echo htmlspecialchars(trim($discovergypvidold)) ?>">
									<span class="form-text small">
										Gültige Werte ID. Um die ID herauszufinden mit dem Browser die Adresse "https://api.discovergy.com/public/v1/meters" aufrufen und dort Benutzername und Passwort eingeben. Hier wird nun u.a. die ID des Zählers angezeigt.<br>
										Die Benutzerdaten werden im Discovergy EVU Modul konfiguriert.
									</span>
								</div>
							</div>
						</div>
						<div id="pvsolarview" class="hide">
							<div class="form-row mb-1">
								<label for="solarview_hostname" class="col-md-4 col-form-label">Hostname/IP des SolarView TCP-Servers</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|[a-zA-Z0-9.\-_]+$" name="solarview_hostname" id="solarview_hostname" value="<?php echo trim($solarview_hostnameold) ?>">
									<span class="form-text small">
										Gültige Werte Hostname oder IP-Adresse.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solarview_port" class="col-md-4 col-form-label">Port des Solarview TCP-Servers</label>
								<div class="col">
									<input class="form-control" type="number" name="solarview_port" id="solarview_port" value="<?php echo htmlspecialchars(trim($solarview_portold)) ?>">
									<span class="form-text small">
										Gültige Werte Port, z.B. 15000.
									</span>
								</div>
							</div>
						</div>
						<div id="pvpowerwall" class="hide">
							<div class="card-text alert alert-info">
								Keine Einstellung nötig. Die IP wird im Speichermodul konfiguriert.
							</div>
						</div>
						<div id="pvmpmevu" class="hide">
							<div class="form-row mb-1">
								<label for="pvkitversion" class="col-md-4 col-form-label">Version des openWB PV Kits</label>
								<div class="col">
									<select name="pvkitversion" id="pvkitversion" class="form-control">
										<option <?php if($pvkitversionold == 0) echo "selected" ?> value="0">PV Kit</option>
										<option <?php if($pvkitversionold == 1) echo "selected" ?> value="1">PV Kit v2</option>
									</select>
								</div>
							</div>
						</div>
						<div id="pvplenti" class="hide">
							<div class="form-row mb-1">
								<label for="kostalplenticoreip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="kostalplenticoreip" id="kostalplenticoreip" value="<?php echo trim($kostalplenticoreipold) ?>">
									<span class="form-text small">
										Gültige Werte: IP-Adresse des 1. Kostal Plenticore. An diesem muss (wenn vorhanden) der EM300/das KSEM und ggf. Speicher angeschlossen sein.
										Modbus/Sunspec (TCP) muss im WR aktiviert sein (Port 1502, Unit-ID 71).
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="name_wechselrichter1" class="col-md-4 col-form-label">Name</label>
								<div class="col">
									<input class="form-control" type="text" name="name_wechselrichter1" id="name_wechselrichter1" value="<?php echo trim($name_wechselrichter1old) ?>">
									<span class="form-text small">
										Freie Bezeichnung des Wechselrichters zu Anzeigezwecken, kann leer bleiben.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="kostalplenticoreip2" class="col-md-4 col-form-label">WR 2 IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="kostalplenticoreip2" id="kostalplenticoreip2" value="<?php echo trim($kostalplenticoreip2old) ?>">
									<span class="form-text small">
										Gültige Werte: IP-Adresse des 2. Kostal Plenticore oder "none". An diesem WR darf kein Speicher angeschlossen sein.
										Wenn nur ein WR genutzt wird, muss der Wert "none" gesetzt werden, ansonsten muss Modbus/Sunspec (TCP) im WR aktiviert sein (Port 1502, Unit-ID 71).
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="name_wechselrichter2" class="col-md-4 col-form-label">WR 2 Name</label>
								<div class="col">
									<input class="form-control" type="text" name="name_wechselrichter2" id="name_wechselrichter2" value="<?php echo trim($name_wechselrichter2old) ?>">
									<span class="form-text small">
										Freie Bezeichnung des zweiten Wechselrichters zu Anzeigezwecken, kann leer bleiben.
									</span>
								</div>
							</div>
						</div>
						<div id="pvsmartme" class="hide">
							<div class="form-row mb-1">
								<label for="wr_smartme_user" class="col-md-4 col-form-label">Smartme Benutzername</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_smartme_user" id="wr_smartme_user" value="<?php echo trim($wr_smartme_userold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_smartme_pass" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="wr_smartme_pass" id="wr_smartme_pass" value="<?php echo htmlspecialchars(trim($wr_smartme_passold)) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_smartme_url" class="col-md-4 col-form-label">Smartme URL</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_smartme_url" id="wr_smartme_url" value="<?php echo trim($wr_smartme_urlold) ?>">
								</div>
							</div>
						</div>
						<div id="pvpiko2" class="hide">
							<div class="form-row mb-1">
								<label for="wr_piko2_user" class="col-md-4 col-form-label">Benutzername</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_piko2_user" id="wr_piko2_user" value="<?php echo trim($wr_piko2_userold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_piko2_pass" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="wr_piko2_pass" id="wr_piko2_pass" value="<?php echo htmlspecialchars(trim($wr_piko2_passold)) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_piko2_url" class="col-md-4 col-form-label">URL</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_piko2_url" id="wr_piko2_url" value="<?php echo trim($wr_piko2_urlold) ?>">
								</div>
							</div>
						</div>
						<div id="pvwrjson" class="hide">
							<div class="form-row mb-1">
								<label for="wrjsonurl" class="col-md-4 col-form-label">WR URL</label>
								<div class="col">
									<input class="form-control" type="text" name="wrjsonurl" id="wrjsonurl" value="<?php echo trim($wrjsonurlold) ?>">
									<span class="form-text small">
										Gültige Werte URL. Vollständige URL die die Json Antwort enthält.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrjsonwatt" class="col-md-4 col-form-label">Json Abfrage für Watt</label>
								<div class="col">
									<input class="form-control" type="text" name="wrjsonwatt" id="wrjsonwatt" value="<?php echo htmlspecialchars(trim($wrjsonwattold)) ?>">
									<span class="form-text small">
										Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
										Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> So muss hier <span class="text-info">.PowerOut</span> eingetragen werden.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrjsonkwh" class="col-md-4 col-form-label">Json Abfrage für kWh</label>
								<div class="col">
									<input class="form-control" type="text" name="wrjsonkwh" id="wrjsonkwh" value="<?php echo trim($wrjsonkwhold) ?>">
									<span class="form-text small">
										Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
										Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> So muss hier <span class="text-info">.PowerProduced</span> eingetragen werden.
									</span>
								</div>
							</div>
						</div>
						<div id="pvwrkostalpiko" class="hide">
							<div class="form-row mb-1">
								<label for="wrkostalpikoip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wrkostalpikoip" id="wrkostalpikoip" value="<?php echo trim($wrkostalpikoipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="pvwrtri9000" class="hide">
							<div class="form-row mb-1">
								<label for="tri9000ip" class="col-md-4 col-form-label">WR 1 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="tri9000ip" id="tri9000ip" value="<?php echo trim($tri9000ipold) ?>">
									<span class="form-text small">
										Gültige Werte: IPs. IP Adresse des SMA WR, ggf. muss der modbusTCP im WR noch aktiviert werden (normalerweise deaktiviert, entweder direkt am Wechselrichter, per Sunny Portal oder über das Tool "Sunny Explorer").
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Handelt es sich um eine SMA Webbox?</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($wrsmawebboxold == 0) echo " active" ?>">
											<input type="radio" name="wrsmawebbox" id="wrsmawebboxNo" value="0"<?php if($wrsmawebboxold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($wrsmawebboxold == 1) echo " active" ?>">
											<input type="radio" name="wrsmawebbox" id="wrsmawebboxYes" value="1"<?php if($wrsmawebboxold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
									<span class="form-text small">
										Diese Option aktivieren wenn ein Solaredge SmartMeter verbaut ist welches vorhandene Bestands PV Anlagen erfasst.
										Das Meter muss an Position 2 konfiguriert sein.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrsma2ip" class="col-md-4 col-form-label">WR 2 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="wrsma2ip" id="wrsma2ip" value="<?php echo trim($wrsma2ip) ?>">
									<span class="form-text small">
										Gültige Werte: IP Adresse oder "none". IP des zweiten SMA Wechselrichters. Wenn nur ein WR genutzt wird, muss der Wert "none" gesetzt werden.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrsma3ip" class="col-md-4 col-form-label">WR 3 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="wrsma3ip" id="wrsma3ip" value="<?php echo trim($wrsma3ip) ?>">
									<span class="form-text small">
										Gültige Werte: IP Adresse oder "none". IP des dritten SMA Wechselrichters. Wenn weniger WR genutzt werden, muss der Wert "none" gesetzt werden.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrsma4ip" class="col-md-4 col-form-label">WR 4 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="wrsma4ip" id="wrsma4ip" value="<?php echo trim($wrsma4ip) ?>">
									<span class="form-text small">
										Gültige Werte: IP Adresse oder "none". IP des vierten SMA Wechselrichters. Wenn weniger WR genutzt werden, muss der Wert "none" gesetzt werden.
									</span>
								</div>
							</div>
						</div>
						<div id="pvwrsolaredge" class="hide">
							<div class="form-row mb-1">
								<label for="solaredgepvip" class="col-md-4 col-form-label">WR Solaredge IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="solaredgepvip" id="solaredgepvip" value="<?php echo trim($solaredgepvipold) ?>">
									<span class="form-text small">
										Gültige Werte: IPs. IP Adresse des SolarEdge Wechselrichters. Modbus TCP muss am WR aktiviert werden, der Port ist auf 502 zu stellen.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Externes Meter mit auslesen</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($wr1extprodold == 0) echo " active" ?>">
											<input type="radio" name="wr1extprod" id="wr1extprodNo" value="0"<?php if($wr1extprodold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($wr1extprodold == 1) echo " active" ?>">
											<input type="radio" name="wr1extprod" id="wr1extprodYes" value="1"<?php if($wr1extprodold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
									<span class="form-text small">
										Diese Option aktivieren wenn ein Solaredge SmartMeter verbaut ist welches vorhandene Bestands PV Anlagen erfasst.
										Das Meter muss an Position 2 konfiguriert sein.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgepvslave1" class="col-md-4 col-form-label">WR 1 Solaredge ID</label>
								<div class="col">
									<input class="form-control" type="number" min="0" step="1" name="solaredgepvslave1" id="solaredgepvslave1" value="<?php echo trim($solaredgeipslave1old) ?>">
									<span class="form-text small">
										Gültige Werte Zahl. ID des SolarEdge Wechselrichters. Normalerweise 1.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgepvslave2" class="col-md-4 col-form-label">WR 2 Solaredge ID</label>
								<div class="col">
									<input class="form-control" type="text" name="solaredgepvslave2" id="solaredgepvslave2" value="<?php echo trim($solaredgeipslave2old) ?>">
									<span class="form-text small">
										Gültige Werte Zahl oder none. ID des zweiten SolarEdge Wechselrichters. Wenn nur ein WR genutzt wird auf none setzen.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgepvslave3" class="col-md-4 col-form-label">WR 3 Solaredge ID</label>
								<div class="col">
									<input class="form-control" type="text" name="solaredgepvslave3" id="solaredgepvslave3" value="<?php echo trim($solaredgeipslave3old) ?>">
									<span class="form-text small">
										Gültige Werte Zahl oder none. ID des dritten SolarEdge Wechselrichters. Wenn weniger WR genutzt werden auf none setzen.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgepvslave4" class="col-md-4 col-form-label">WR 4 Solaredge ID</label>
								<div class="col">
									<input class="form-control" type="text" name="solaredgepvslave4" id="solaredgepvslave4" value="<?php echo trim($solaredgeipslave4old) ?>">
									<span class="form-text small">
										Gültige Werte Zahl oder none. ID des vierten SolarEdge Wechselrichters. Wenn weniger WR genutzt werden auf none setzen.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgewr2ip" class="col-md-4 col-form-label">WR 2 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="solaredgewr2ip" id="solaredgewr2ip" value="<?php echo trim($solaredgewr2ipold) ?>">
									<span class="form-text small">
										Gültige Werte IP oder none. IP des zweiten SolarEdge Wechselrichters. Ist nur nötig, wenn 2 Wechselrichter genutzt werden die nicht per Modbus miteinander verbunden sind.
									</span>
								</div>
							</div>
						</div>
						<div id="pvwrfronius" class="hide">
							<div class="form-row mb-1">
								<label for="wrfroniusip" class="col-md-4 col-form-label">WR Fronius IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wrfroniusip" id="wrfroniusip" value="<?php echo trim($wrfroniusipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12. IP Adresse des Fronius Wechselrichters. Werden hier und im Feld unten zwei verschiedene Adressen eingetragen, muss hier die Adresse des Wechselrichters stehen, an dem das SmartMeter angeschlossen ist.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrfronius2ip" class="col-md-4 col-form-label">WR Fronius 2 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="wrfronius2ip" id="wrfronius2ip" value="<?php echo trim($wrfronius2ipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12. IP Adresse des zweiten Fronius Wechselrichters. Sind nur Symos in Nutzung, welche über Fronius Solar Net / DATCOM miteinander verbunden sind, reicht die Angabe der Adresse eines Wechselrichters im ersten Feld. Sind aber z.B. Symo und Symo Hybrid im Einsatz, müssen diese beide angegeben werden (hier dann die Adresse des Wechselrichters, an dem das SmartMeter NICHT angeschlossen ist). Ist kein zweiter Wechselrichter vorhanden, dann bitte hier "none" eintragen.
									</span>
								</div>
							</div>
						</div>
						<div id="pvmpm3pm" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="mpm3pmpvsource" class="col-md-4 col-form-label">MPM3PM Wechselrichterleistung Source</label>
									<div class="col">
										<input class="form-control" type="text" name="mpm3pmpvsource" id="mpm3pmpvsource" value="<?php echo trim($mpm3pmpvsourceold) ?>">
										<span class="form-text small">
											Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM angeschlossen ist. Meist /dev/ttyUSB0<br>
											Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmpvid" class="col-md-4 col-form-label">MPM3PM Wechselrichterleistung ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmpvid" id="mpm3pmpvid" value="<?php echo trim($mpm3pmpvidold) ?>">
										<span class="form-text small">
											Gültige Werte 1-254. Modbus ID des MPM3PM.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmpvlanip" class="col-md-4 col-form-label">IP des Modbus/Lan Konverter</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpm3pmpvlanip" id="mpm3pmpvlanip" value="<?php echo trim($mpm3pmpvlanipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Ist die Source "virtualcomX" wird automatisch ein Lan Konverter genutzt.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="pvethsdm120" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="wr_sdm120ip" class="col-md-4 col-form-label">SDM Modbus IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wr_sdm120ip" id="wr_sdm120ip" value="<?php echo trim($wr_sdm120ipold) ?>">
										<span class="form-text small">
											Gültige Werte IP. IP Adresse des ModbusLAN Konverters.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="wr_sdm120id" class="col-md-4 col-form-label">SDM Modbus ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="wr_sdm120id" id="wr_sdm120id" value="<?php echo trim($wr_sdm120idold) ?>">
										<span class="form-text small">
											Gültige Werte 1-254. Modbus ID des SDM.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="pvsdmwr" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sdm630modbuswrsource" class="col-md-4 col-form-label">SDM Modbus Wechselrichterleistung Source</label>
									<div class="col">
										<input class="form-control" type="text" name="sdm630modbuswrsource" id="sdm630modbuswrsource" value="<?php echo trim($sdm630modbuswrsourceold) ?>">
										<span class="form-text small">
											Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der SDM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
											Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sdm630modbuswrid" class="col-md-4 col-form-label">SDM Modbus Wechselrichterleistung ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="sdm630modbuswrid" id="sdm630modbuswrid" value="<?php echo trim($sdm630modbuswridold) ?>">
										<span class="form-text small">
											Gültige Werte 1-254. Modbus ID des SDM. Getestet SDM230 & SDM630v2.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sdm630modbuswrlanip" class="col-md-4 col-form-label">IP des Modbus/Lan Konverter</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sdm630modbuswrlanip" id="sdm630modbuswrlanip" value="<?php echo trim($sdm630modbuswrlanipold) ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Ist die Source "virtualcomX" wird automatisch ein Lan Konverter genutzt.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="pvvzl" class="hide">
							<div class="form-row mb-1">
								<label for="vzloggerpvip" class="col-md-4 col-form-label">IP Adresse und Port</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5]):[1-9][0-9]*$" name="vzloggerpvip" id="vzloggerpvip" value="<?php echo trim($vzloggerpvipold) ?>">
									<span class="form-text small">
										Gültige Werte IP:Port z.B. 192.168.0.12:8080.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="vzloggerpvline" class="col-md-4 col-form-label">Vzloggerpv Zeile</label>
								<div class="col">
									<input class="form-control" type="number" min="1" step="1" name="vzloggerpvline" id="vzloggerpvline" value="<?php echo trim($vzloggerpvlineold) ?>">
									<span class="form-text small">
										Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br>
										Nun zählen in welcher Zeile der gewünschte Wert steht und diesen hier eintragen.
									</span>
								</div>
							</div>
						</div>
						<div id="pvhttp" class="hide">
							<div class="form-row mb-1">
								<label for="wr_http_w_url" class="col-md-4 col-form-label">Vollständige URL für die Wechselrichter Watt</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_http_w_url" id="wr_http_w_url" value="<?php echo htmlspecialchars(trim($wr_http_w_urlold)) ?>">
									<span class="form-text small">
										Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als wird der Wert auf null gesetzt. Der Wert muss in Watt sein.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_http_kwh_url" class="col-md-4 col-form-label">Vollständige URL für die Wechselrichter absolut kWh</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_http_kwh_url" id="wr_http_kwh_url" value="<?php echo htmlspecialchars(trim($wr_http_kwh_urlold)) ?>">
									<span class="form-text small">
										Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Der Wert muss in WattStunden sein. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
									</span>
								</div>
							</div>
						</div>
						<div id="pvsma" class="hide">
							<div class="form-row mb-1">
								<label for="smaemdpvid" class="col-md-4 col-form-label">Seriennummer des SMA Energy Meter</label>
								<div class="col">
									<input class="form-control" type="text" name="smaemdpvid" id="smaemdpvid" value="<?php echo trim($smaemdpvidold) ?>">
									<span class="form-text small">
									Gültige Werte Seriennummer. Hier die Seriennummer des SMA Meter für die PV angeben.
									</span>
								</div>
							</div>
						</div>

						<script>
							function display_pvwattmodul() {
								hideSection('pvvzl');
								hideSection('pvsdmwr');
								hideSection('pvwrfronius');
								hideSection('pvhttp');
								hideSection('pvsma');
								hideSection('pvwrjson');
								hideSection('pvmpm3pm');
								hideSection('pvwrkostalpiko');
								hideSection('pvwrsolaredge');
								hideSection('pvsmartme');
								hideSection('pvwrtri9000');
								hideSection('pvplenti');
								hideSection('pvsolarlog');
								hideSection('pvpiko2');
								hideSection('pvpowerwall');
								hideSection('pvmpmevu');
								hideSection('pvethsdm120');
								hideSection('pvsolarview');
								hideSection('pvdiscovergy');
								hideSection('pvyouless');
								hideSection('pvlgessv1');
								hideSection('pvmqtt');
								hideSection('pvsunways');
								hideSection('pvfems');
								hideSection('pvsolarworld');
								hideSection('pvip');
								hideSection('pvsiemens');
								hideSection('pvrct');
								hideSection('pvpowerdog');
								if($('#pvwattmodul').val() == 'wr_siemens') {
									showSection('pvip');
									showSection('pvsiemens');
								}
								if($('#pvwattmodul').val() == 'wr_huawei') {
									showSection('pvip');
								}
								if($('#pvwattmodul').val() == 'wr_shelly') {
									showSection('pvip');
								}

								if($('#pvwattmodul').val() == 'wr_powerdog') {
									showSection('pvpowerdog');
								}
								if($('#pvwattmodul').val() == 'wr_rct') {
									showSection('pvrct');
								}
								if($('#pvwattmodul').val() == 'wr_fems') {
									showSection('pvfems');
								}
								if($('#pvwattmodul').val() == 'wr_solarworld') {
									showSection('pvsolarworld');
								}
								if($('#pvwattmodul').val() == 'wr_sunways') {
									showSection('pvsunways');
								}
								if($('#pvwattmodul').val() == 'wr_mqtt') {
									showSection('pvmqtt');
								}
								if($('#pvwattmodul').val() == 'wr_youless120') {
									showSection('pvyouless');
								}
								if($('#pvwattmodul').val() == 'wr_solarview') {
									showSection('pvsolarview');
								}
								if($('#pvwattmodul').val() == 'wr_discovergy') {
									showSection('pvdiscovergy');
								}
								if($('#pvwattmodul').val() == 'wr_ethsdm120') {
									showSection('pvethsdm120');
								}
								if($('#pvwattmodul').val() == 'wr_ethmpm3pmaevu') {
									showSection('pvmpmevu');
								}
								if($('#pvwattmodul').val() == 'vzloggerpv') {
									showSection('pvvzl');
								}
								if($('#pvwattmodul').val() == 'sdm630modbuswr')   {
									showSection('pvsdmwr');
								}
								if($('#pvwattmodul').val() == 'wr_fronius')   {
									showSection('pvwrfronius');
								}
								if($('#pvwattmodul').val() == 'wr_http')   {
									showSection('pvhttp');
								}
								if($('#pvwattmodul').val() == 'smaemd_pv')   {
									showSection('pvsma');
								}
								if($('#pvwattmodul').val() == 'wr_json')   {
									showSection('pvwrjson');
								}
								if($('#pvwattmodul').val() == 'mpm3pmpv')   {
									showSection('pvmpm3pm');
								}
								if($('#pvwattmodul').val() == 'wr_kostalpiko')   {
									showSection('pvwrkostalpiko');
								}
								if($('#pvwattmodul').val() == 'wr_solaredge')   {
									showSection('pvwrsolaredge');
								}
								if($('#pvwattmodul').val() == 'wr_smartme')   {
									showSection('pvsmartme');
								}
								if($('#pvwattmodul').val() == 'wr_tripower9000')   {
									showSection('pvwrtri9000');
								}
								if($('#pvwattmodul').val() == 'wr_plenticore')   {
									showSection('pvplenti');
								}
								if($('#pvwattmodul').val() == 'wr_solarlog')   {
									showSection('pvsolarlog');
								}
								if($('#pvwattmodul').val() == 'wr_kostalpikovar2')   {
									showSection('pvpiko2');
								}
								if($('#pvwattmodul').val() == 'wr_powerwall')   {
									showSection('pvpowerwall');
								}
								if($('#pvwattmodul').val() == 'wr_lgessv1')   {
									showSection('pvlgessv1');
								}
							}

							$(function() {
								display_pvwattmodul();

								$('#pvwattmodul').change( function(){
									display_pvwattmodul();
								} );
							});
						</script>
					</div>
				</div>

				<!-- PV Module 2 -->
				<div class="card border-success">
					<div class="card-header bg-success">
						PV-Modul 2
					</div>
					<div class="card-body">
						<div class="form-row mb-1">
							<label for="pv2wattmodul" class="col-md-4 col-form-label">PV-Modul</label>
							<div class="col">
								<select name="pv2wattmodul" id="pv2wattmodul" class="form-control">
									<option <?php if($pv2wattmodulold == "none\n") echo "selected" ?> value="none">Nicht vorhanden</option>
									<option <?php if($pv2wattmodulold == "wr2_ethlovatoaevu\n") echo "selected" ?> value="wr2_ethlovatoaevu">Lovato an openWB EVU Kit</option>
									<option <?php if($pv2wattmodulold == "wr2_ethlovato\n") echo "selected" ?> value="wr2_ethlovato">openWB PV Kit v2</option>
									<option <?php if($pv2wattmodulold == "wr2_smamodbus\n") echo "selected" ?> value="wr2_smamodbus">SMA Wechselrichter</option>
									<option <?php if($pv2wattmodulold == "wr2_kostalsteca\n") echo "selected" ?> value="wr2_kostalsteca">Kostal Piko MP oder Steca Grid Coolcept</option>
									<option <?php if($pv2wattmodulold == "wr2_victron\n") echo "selected" ?> value="wr2_victron">Victron MPPT</option>
									<option <?php if($pv2wattmodulold == "wr2_ethsdm120\n") echo "selected" ?> value="wr2_ethsdm120">SDM120 an Netzwerk Modbus Adapter</option>
									<option <?php if($pv2wattmodulold == "wr2_solaredge\n") echo "selected" ?> value="wr2_solaredge">Solaredge</option>
								</select>
							</div>
						</div>
						<div id="pv2noconfig" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="pv2ipdiv" class="hide">
							<div class="form-row mb-1">
								<label for="pv2ip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="pv2ip" id="pv2ip" value="<?php echo trim($pv2ipold) ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="pv2iddiv" class="hide">
							<div class="form-row mb-1">
								<label for="pv2id" class="col-md-4 col-form-label">Modbus ID</label>
								<div class="col">
									<input class="form-control" type="number" min="0" step="1" name="pv2id" id="pv2id" value="<?php echo trim($pv2idold) ?>">
									<span class="form-text small">Gültige Werte ID. ID Adresse</span>
								</div>
							</div>
						</div>

						<script>
							function display_pv2wattmodul() {
								hideSection('pv2noconfig');
								hideSection('pv2ipdiv');
								hideSection('pv2iddiv');

								if($('#pv2wattmodul').val() == 'wr2_ethlovatoaevu') {
									showSection('pv2noconfig');
								}
								if($('#pv2wattmodul').val() == 'wr2_ethlovato') {
									showSection('pv2noconfig');
								}
								if($('#pv2wattmodul').val() == 'wr2_smamodbus') {
									showSection('pv2ipdiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_kostalsteca') {
									showSection('pv2ipdiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_victron') {
									showSection('pv2ipdiv');
									showSection('pv2iddiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_solaredge') {
									showSection('pv2ipdiv');
									showSection('pv2iddiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_ethsdm120') {
									showSection('pv2ipdiv');
									showSection('pv2iddiv');
								}
							}
							$(function() {
								display_pv2wattmodul();

								$('#pv2wattmodul').change( function(){
									display_pv2wattmodul();
								} );
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
					$('#navModulkonfigurationPvBeta').addClass('disabled');
				}
			);

		</script>

	</body>
</html>
