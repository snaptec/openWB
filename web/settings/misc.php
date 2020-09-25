<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Einstellungen</title>
		<meta name="description" content="Control your charge" />
		<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
		<meta name="author" content="Kevin Wieland, Michael Ortenstein" />
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
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20200505-a" ></script>
		<script>
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

			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach($lines as $line) {
				if(strpos($line, "netzabschaltunghz=") !== false) {
					list(, $netzabschaltunghzold) = explode("=", $line);
				}
				if(strpos($line, "cpunterbrechunglp1=") !== false) {
					list(, $cpunterbrechunglp1old) = explode("=", $line);
				}
				if(strpos($line, "cpunterbrechunglp2=") !== false) {
					list(, $cpunterbrechunglp2old) = explode("=", $line);
				}
				if(strpos($line, "displayaktiv=") !== false) {
					list(, $displayaktivold) = explode("=", $line);
				}
				if(strpos($line, "displayEinBeimAnstecken=") !== false) {
					list(, $displayEinBeimAnsteckenOld) = explode("=", $line);
				}
				if(strpos($line, "displaytagesgraph=") !== false) {
					list(, $displaytagesgraphold) = explode("=", $line);
				}
				if(strpos($line, "displaytheme=") !== false) {
					list(, $displaythemeold) = explode("=", $line);
				}
				if(strpos($line, "displaysleep=") !== false) {
					list(, $displaysleepold) = explode("=", $line);
				}
				if(strpos($line, "displayevumax=") !== false) {
					list(, $displayevumaxold) = explode("=", $line);
				}
				if(strpos($line, "displaypvmax=") !== false) {
					list(, $displaypvmaxold) = explode("=", $line);
				}
				if(strpos($line, "displayspeichermax=") !== false) {
					list(, $displayspeichermaxold) = explode("=", $line);
				}
				if(strpos($line, "displayhausanzeigen=") !== false) {
					list(, $displayhausanzeigenold) = explode("=", $line);
				}
				if(strpos($line, "displayhausmax=") !== false) {
					list(, $displayhausmaxold) = explode("=", $line);
				}
				if(strpos($line, "displaylp1max=") !== false) {
					list(, $displaylp1maxold) = explode("=", $line);
				}
				if(strpos($line, "displaylp2max=") !== false) {
					list(, $displaylp2maxold) = explode("=", $line);
				}
				if(strpos($line, "displaypinaktiv=") !== false) {
					list(, $displaypinaktivold) = explode("=", $line);
				}

				if(strpos($line, "displaypincode=") !== false) {
					list(, $displaypincodeold) = explode("=", $line);
				}
				if(strpos($line, "logeinspeisungneg=") !== false) {
					list(, $logeinspeisungnegold) = explode("=", $line);
				}
				if(strpos($line, "debug=") !== false) {
					list(, $debugold) = explode("=", $line);
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
				if(strpos($line, "evsecon=") !== false) {
					list(, $evseconold) = explode("=", $line);
				}
				if(strpos($line, "dacregister=") !== false) {
					list(, $dacregisterold) = explode("=", $line);
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
				if(strpos($line, "pushbenachrichtigung=") !== false) {
					list(, $pushbenachrichtigungold) = explode("=", $line);
				}
				if(strpos($line, "pushoveruser=") !== false) {
					list(, $pushoveruserold) = explode("=", $line);
				}
				if(strpos($line, "pushovertoken=") !== false) {
					list(, $pushovertokenold) = explode("=", $line);
				}
				if(strpos($line, "pushbstartl=") !== false) {
					list(, $pushbstartlold) = explode("=", $line);
				}
				if(strpos($line, "pushbstopl=") !== false) {
					list(, $pushbstoplold) = explode("=", $line);
				}
				if(strpos($line, "pushbplug=") !== false) {
					list(, $pushbplugold) = explode("=", $line);
				}
				if(strpos($line, "pushbsmarthome=") !== false) {
					list(, $pushbsmarthomeold) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid2s1=") !== false) {
					list(, $sdm120modbusllid2s1old) = explode("=", $line);
				}
				if(strpos($line, "sdm120modbusllid3s1=") !== false) {
					list(, $sdm120modbusllid3s1old) = explode("=", $line);
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
				if(strpos($line, "ladeleistungmodul=") !== false) {
					list(, $ladeleistungmodulold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbusllid=") !== false) {
					list(, $sdm630modbusllidold) = explode("=", $line);
				}
				if(strpos($line, "sdm630modbusllsource=") !== false) {
					list(, $sdm630modbusllsourceold) = explode("=", $line);
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
				if(strpos($line, "wr_http_w_url=") !== false) {
					list(, $wr_http_w_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "wr_http_kwh_url=") !== false) {
					list(, $wr_http_kwh_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "bezug_http_w_url=") !== false) {
					list(, $bezug_http_w_urlold) = explode("=", $line, 2);
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
				if(strpos($line, "livegraph=") !== false) {
					list(, $livegraphold) = explode("=", $line);
				}
				if(strpos($line, "releasetrain=") !== false) {
					list(, $releasetrainold) = explode("=", $line);
				}
				if(strpos($line, "logdailywh=") !== false) {
					list(, $logdailywhold) = explode("=", $line);
				}
				if(strpos($line, "ladetaster=") !== false) {
					list(, $ladetasterold) = explode("=", $line);
				}
				if(strpos($line, "grapham=") !== false) {
					list(, $graphamold) = explode("=", $line);
				}
				if(strpos($line, "graphinteractiveam=") !== false) {
					list(, $graphinteractiveamold) = explode("=", $line);
				}
				if(strpos($line, "graphliveam=") !== false) {
					list(, $graphliveamold) = explode("=", $line);
				}
				if(strpos($line, "chartlegendmain=") !== false) {
					list(, $chartlegendmainold) = explode("=", $line);
				}
				if(strpos($line, "hausverbrauchstat=") !== false) {
					list(, $hausverbrauchstatold) = explode("=", $line);
				}
				if(strpos($line, "heutegeladen=") !== false) {
					list(, $heutegeladenold) = explode("=", $line);
				}

				if(strpos($line, "bootmodus=") !== false) {
					list(, $bootmodusold) = explode("=", $line);
				}
				if(strpos($line, "rfidakt=") !== false) {
					list(, $rfidaktold) = explode("=", $line);
				}
				if(strpos($line, "rfidlist=") !== false) {
					list(, $rfidlistold) = explode("=", $line);
				}
				if(strpos($line, "rfidstop=") !== false) {
					list(, $rfidstopold) = explode("=", $line);
				}

				if(strpos($line, "rfidstandby=") !== false) {
					list(, $rfidstandbyold) = explode("=", $line);
				}
				if(strpos($line, "rfidlp1start1=") !== false) {
					list(, $rfidlp1start1old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp1start2=") !== false) {
					list(, $rfidlp1start2old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp1start3=") !== false) {
					list(, $rfidlp1start3old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp1start4=") !== false) {
					list(, $rfidlp1start4old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp1start5=") !== false) {
					list(, $rfidlp1start5old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp2start1=") !== false) {
					list(, $rfidlp2start1old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp2start2=") !== false) {
					list(, $rfidlp2start2old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp2start3=") !== false) {
					list(, $rfidlp2start3old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp2start4=") !== false) {
					list(, $rfidlp2start4old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp2start5=") !== false) {
					list(, $rfidlp2start5old) = explode("=", $line);
				}

				if(strpos($line, "rfidsofort=") !== false) {
					list(, $rfidsofortold) = explode("=", $line);
				}

				if(strpos($line, "rfidnurpv=") !== false) {
					list(, $rfidnurpvold) = explode("=", $line);
				}

				if(strpos($line, "rfidminpv=") !== false) {
					list(, $rfidminpvold) = explode("=", $line);
				}
				if(strpos($line, "rfidstop2=") !== false) {
					list(, $rfidstop2old) = explode("=", $line);
				}

				if(strpos($line, "rfidstandby2=") !== false) {
					list(, $rfidstandby2old) = explode("=", $line);
				}

				if(strpos($line, "rfidsofort2=") !== false) {
					list(, $rfidsofort2old) = explode("=", $line);
				}

				if(strpos($line, "rfidnurpv2=") !== false) {
					list(, $rfidnurpv2old) = explode("=", $line);
				}

				if(strpos($line, "rfidminpv2=") !== false) {
					list(, $rfidminpv2old) = explode("=", $line);
				}
				if(strpos($line, "rfidstop3=") !== false) {
					list(, $rfidstop3old) = explode("=", $line);
				}

				if(strpos($line, "rfidstandby3=") !== false) {
					list(, $rfidstandby3old) = explode("=", $line);
				}

				if(strpos($line, "rfidsofort3=") !== false) {
					list(, $rfidsofort3old) = explode("=", $line);
				}

				if(strpos($line, "rfidnurpv3=") !== false) {
					list(, $rfidnurpv3old) = explode("=", $line);
				}

				if(strpos($line, "rfidminpv3=") !== false) {
					list(, $rfidminpv3old) = explode("=", $line);
				}

				if(strpos($line, "rfidlp1c1=") !== false) {
					list(, $rfidlp1c1old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp1c2=") !== false) {
					list(, $rfidlp1c2old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp1c3=") !== false) {
					list(, $rfidlp1c3old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp2c1=") !== false) {
					list(, $rfidlp2c1old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp2c2=") !== false) {
					list(, $rfidlp2c2old) = explode("=", $line);
				}
				if(strpos($line, "rfidlp2c3=") !== false) {
					list(, $rfidlp2c3old) = explode("=", $line);
				}
				if(strpos($line, "ledsofort=") !== false) {
					list(, $ledsofortold) = explode("=", $line);
				}
				if(strpos($line, "lednurpv=") !== false) {
					list(, $lednurpvold) = explode("=", $line);
				}

				if(strpos($line, "ledminpv=") !== false) {
					list(, $ledminpvold) = explode("=", $line);
				}

				if(strpos($line, "ledstandby=") !== false) {
					list(, $ledstandbyold) = explode("=", $line);
				}

				if(strpos($line, "ledstop=") !== false) {
					list(, $ledstopold) = explode("=", $line);
				}
				if(strpos($line, "led0sofort=") !== false) {
					list(, $led0sofortold) = explode("=", $line);
				}

				if(strpos($line, "led0nurpv=") !== false) {
					list(, $led0nurpvold) = explode("=", $line);
				}

				if(strpos($line, "led0minpv=") !== false) {
					list(, $led0minpvold) = explode("=", $line);
				}

				if(strpos($line, "led0standby=") !== false) {
					list(, $led0standbyold) = explode("=", $line);
				}

				if(strpos($line, "led0stop=") !== false) {
					list(, $led0stopold) = explode("=", $line);
				}
				if(strpos($line, "ledsakt=") !== false) {
					list(, $ledsaktold) = explode("=", $line);
				}
			}

			$bezug_http_w_urlold = str_replace( "'", "", $bezug_http_w_urlold);
			$bezug_http_ikwh_urlold = str_replace( "'", "", $bezug_http_ikwh_urlold);
			$bezug_http_ekwh_urlold = str_replace( "'", "", $bezug_http_ekwh_urlold);
			$wr_http_w_urlold = str_replace( "'", "", $wr_http_w_urlold);
			$wr_http_kwh_urlold = str_replace( "'", "", $wr_http_kwh_urlold);
			$hsocipold = str_replace( "'", "", $hsocipold);
			$pushoveruserold = str_replace( "'", "", $pushoveruserold);
			$pushovertokenold = str_replace( "'", "", $pushovertokenold);
			$lastrfid = file_get_contents('/var/www/html/openWB/ramdisk/rfidlasttag');
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Verschiedene Einstellungen</h1>
			<form action="./tools/savemisc.php" method="POST">

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Allgemeine Funktionen
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Geschwindigkeit Regelintervall</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($dspeedold == 0) echo " active" ?>">
											<input type="radio" name="dspeed" id="dspeed0" value="0"<?php if($dspeedold == 0) echo " checked=\"checked\"" ?>>Normal
										</label>
										<label class="btn btn-outline-info<?php if($dspeedold == 2) echo " active" ?>">
											<input type="radio" name="dspeed" id="dspeed2" value="2"<?php if($dspeedold == 1) echo " checked=\"checked\"" ?>>Langsam
										</label>
										<label class="btn btn-outline-info<?php if($dspeedold == 3) echo " active" ?>">
											<input type="radio" name="dspeed" id="dspeed3" value="3"<?php if($dspeedold == 1) echo " checked=\"checked\"" ?>>Sehr Langsam
										</label>
									</div>
									<span class="form-text small">
										Sollten Probleme, oder Fehlermeldungen, auftauchen, zunächst das Regelintervall auf "Normal" stellen. Werden Module genutzt, welche z.B. eine Online API zur Abfrage nutzen, oder möchte man weniger regeln, kann man das Regelintervall auf "Langsam" (20 Sekunden) herabsetzen. Die Einstellungen „Sehr Langsam“ führt zu einer Regelzeit von 60 Sekunden.<br>
										<span class="text-danger">Nicht nur die Regelung der PV geführten Ladung, sondern auch Ladestromänderung, beispielsweise “Stop“ etc., werden dann nur noch in diesem Intervall ausgeführt. Die Regelung wird insgesamt träger.</span>
									</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Ladetaster</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($ladetasterold == 0) echo " active" ?>">
											<input type="radio" name="ladetaster" id="ladetasterOff" value="0"<?php if($ladetasterold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($ladetasterold == 1) echo " active" ?>">
											<input type="radio" name="ladetaster" id="ladetasterOn" value="1"<?php if($ladetasterold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
									<span class="form-text small">Wenn aktiviert, sind nach einem Neustart die externen Taster aktiv. Wenn keine verbaut sind, diese Option ausschalten.</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Lademodus nach Start der openWB</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($bootmodusold == 0) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus3" value="3"<?php if($bootmodusold == 3) echo " checked=\"checked\"" ?>>Stop
										</label>
										<label class="btn btn-outline-info<?php if($bootmodusold == 1) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus4" value="4"<?php if($bootmodusold == 4) echo " checked=\"checked\"" ?>>Standby
										</label>
										<label class="btn btn-outline-info<?php if($bootmodusold == 0) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus2" value="2"<?php if($bootmodusold == 2) echo " checked=\"checked\"" ?>>Nur PV
										</label>
										<label class="btn btn-outline-info<?php if($bootmodusold == 0) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus1" value="1"<?php if($bootmodusold == 1) echo " checked=\"checked\"" ?>>Min + PV
										</label>
										<label class="btn btn-outline-info<?php if($bootmodusold == 0) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus0" value="0"<?php if($bootmodusold == 0) echo " checked=\"checked\"" ?>>Sofort Laden
										</label>
									</div>
									<span class="form-text small">Definiert den Lademodus nach Boot der openWB.</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Netzschutz</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($netzabschaltunghzold == 0) echo " active" ?>">
											<input type="radio" name="netzabschaltunghz" id="netzabschaltunghzOff" value="0"<?php if($netzabschaltunghzold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($netzabschaltunghzold == 1) echo " active" ?>">
											<input type="radio" name="netzabschaltunghz" id="netzabschaltunghzOn" value="1"<?php if($netzabschaltunghzold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
									<span class="form-text small">
										Diese Option ist standardmäßig aktiviert und sollte so belassen werden. Bei Unterschreitung einer kritischen Frequenz des Stromnetzes wird die Ladung nach einer zufälligen Zeit zwischen 1 und 90 Sekunden pausiert. Der Lademodus wechselt auf "Stop".
										Sobald die Frequenz wieder in einem normalen Bereich ist wird automatisch der zuletzt gewählte Lademodus wieder aktiviert.
										Ebenso wird die Ladung bei Überschreiten von 51,8 Hz unterbrochen. Dies ist dann der Fall, wenn der Energieversorger Wartungsarbeiten am (Teil-)Netz durchführt und auf einen vorübergehenden Generatorbetrieb umschaltet.
										Die Erhöhung der Frequenz wird durchgeführt, um die PV Anlagen abzuschalten.<br>
										<span class="text-danger">Die Option ist nur aktiv, wenn der Ladepunkt die Frequenz übermittelt. Jede openWB series1/2 tut dies.</span>
									</span>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									CP Unterbrechung
								</div>
								<div class="col">
									<span class="form-text small">Diese Option erfordert die verbaute Addon Platine und die korrekte Verdrahtung des CP Signals durch die Addon Platine. Sie ist für Fahrzeuge, die nach einer gewissen Zeit einer pausierten Ladung nicht von alleine die Ladung wieder beginnen. Nur aktivieren, wenn es ohne die Option Probleme gibt.</span>
								</div>
							</div>
							<div class="form-row mt-2 mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Ladepunkt 1</label>
								</div>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($cpunterbrechunglp1old == 0) echo " active" ?>">
										<input type="radio" name="cpunterbrechunglp1" id="cpunterbrechunglp1Off" value="0"<?php if($cpunterbrechunglp1old == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($cpunterbrechunglp1old == 1) echo " active" ?>">
										<input type="radio" name="cpunterbrechunglp1" id="cpunterbrechunglp1On" value="1"<?php if($cpunterbrechunglp1old == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div class="form-row mt-2" id="lp2cpdiv">
								<div class="col-md-4">
									<label class="col-form-label">Ladepunkt 2</label>
								</div>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($cpunterbrechunglp2old == 0) echo " active" ?>">
										<input type="radio" name="cpunterbrechunglp2" id="cpunterbrechunglp2Off" value="0"<?php if($cpunterbrechunglp2old == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($cpunterbrechunglp2old == 1) echo " active" ?>">
										<input type="radio" name="cpunterbrechunglp2" id="cpunterbrechunglp2On" value="1"<?php if($cpunterbrechunglp2old == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							var lp2akt = <?php echo $lastmanagementold ?>;

							if(lp2akt == '0') {
								$('#lp2cpdiv').hide();
							} else {
								$('#lp2cpdiv').show();
							}
						});
					</script>
				</div>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">RFID</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($rfidaktold == 0) echo " active" ?>">
											<input type="radio" name="rfidakt" id="rfidaktOff" value="0"<?php if($rfidaktold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($rfidaktold == 1) echo " active" ?>">
											<input type="radio" name="rfidakt" id="rfidaktOn1" autocomplete="off" value="1"<?php if($rfidaktold == 1) echo " checked=\"checked\"" ?>>An Modus 1
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($rfidaktold == 2) echo " active" ?>">
											<input type="radio" name="rfidakt" id="rfidaktOn2" autocomplete="off" value="2"<?php if($rfidaktold == 2) echo " checked=\"checked\"" ?>>An Modus 2
										</label>

									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body" id="rfidandiv">
						<div class="form-row form-group">
							<div class="col">
								Zuletzt gescannter RFID Tag: <?php echo trim( $lastrfid ) ?>
							</div>
						</div>
						<div id="rfidan2div">
							<div class="alert alert-info">
								Im Modus 2 wird eine Kommaseparierte Liste mit gültigen RFID Tags hinterlegt. Gescannt werden kann an jedem möglichen RFID Leser. Heißt auch bei mehreren Ladepunkten kann an einem zentralen RFID Leser gescannt werden. Der gescannte Tag wird dem zuletzt angeschlossenenen Auto zugewiesen, schaltet den Ladepunkt frei und vermerkt dies für das Ladelog. Wird erst gescannt und dann ein Auto angeschlossen wird der Tag dem Auto zugewiesen das als nächstes ansteckt. Wird 5 Minuten nach Scannen kein Auto angeschlossen wird der Tag verworfen. Jeder Ladepunkt wird nach abstecken automatisch wieder gesperrt.
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Erlaubte Tags als Kommaseparierte Liste ohne Leerzeichen
									</div>
								</div>
								<div class="form-row">
									<div class="col-lg-12">
										<label for="rfidlist" class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Liste
												</div>
											</div> 
											<input type="text" name="rfidlist" id="rfidlist" class="form-control" value="<?php echo trim( $rfidlistold ) ?>">
										</label>
									</div>
								</div>
							</div>
						</div>
						<div id="rfidan1div">
							<hr class="border-secondary">
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Autos zuweisen
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Ladepunkt 1
									</div>
								</div>
								<div class="form-row">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 1
												</div>
											</div> 
											<input type="text" name="rfidlp1c1" id="rfidlp1c1" class="form-control" value="<?php echo trim( $rfidlp1c1old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 2
												</div>
											</div> 
											<input type="text" name="rfidlp1c2" id="rfidlp1c2" class="form-control" value="<?php echo trim( $rfidlp1c2old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 3
												</div>
											</div> 
											<input type="text" name="rfidlp1c3" id="rfidlp1c3" class="form-control" value="<?php echo trim( $rfidlp1c3old ) ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Ladepunkt 2
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 1
												</div>
											</div> 
											<input type="text" name="rfidlp2c1" id="rfidlp2c1" class="form-control" value="<?php echo trim( $rfidlp2c1old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 2
												</div>
											</div> 
											<input type="text" name="rfidlp2c2" id="rfidlp2c2" class="form-control" value="<?php echo trim( $rfidlp2c2old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 3
												</div>
											</div>
											<input type="text" name="rfidlp2c3" id="rfidlp2c3" class="form-control" value="<?php echo trim( $rfidlp2c3old ) ?>">
										</div>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col-md-4">
										Lademodus ändern
									</div>
									<div class="col form-text small">
										Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Stop
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div> 
											<input type="text" name="rfidstop" id="rfidstop" class="form-control" value="<?php echo trim( $rfidstopold ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div> 
											<input type="text" name="rfidstop2" id="rfidstop2" class="form-control" value="<?php echo trim( $rfidstop2old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidstop3" id="rfidstop3" class="form-control" value="<?php echo trim( $rfidstop3old ) ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Standby
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidstandby" id="rfidstandby" class="form-control" value="<?php echo trim( $rfidstandbyold ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidstandby2" id="rfidstandby2" class="form-control" value="<?php echo trim( $rfidstandby2old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidstandby3" id="rfidstandby3" class="form-control" value="<?php echo trim( $rfidstandby3old ) ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Sofort Laden
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidsofort" id="rfidsofort" class="form-control" value="<?php echo trim( $rfidsofortold ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidsofort2" id="rfidsofort2" class="form-control" value="<?php echo trim( $rfidsofort2old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidsofort3" id="rfidsofort3" class="form-control" value="<?php echo trim( $rfidsofort3old ) ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Min + PV Laden
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidminpv" id="rfidminpv" class="form-control" value="<?php echo trim( $rfidminpvold ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidminpv2" id="rfidminpv2" class="form-control" value="<?php echo trim( $rfidminpv2old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidminpv3" id="rfidminpv3" class="form-control" value="<?php echo trim( $rfidminpv3old ) ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Nur PV
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidnurpv" id="rfidnurpv" class="form-control" value="<?php echo trim( $rfidnurpvold ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidnurpv2" id="rfidnurpv2" class="form-control" value="<?php echo trim( $rfidnurpv2old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidnurpv3" id="rfidnurpv3" class="form-control" value="<?php echo trim( $rfidnurpv3old ) ?>">
										</div>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col-md-4">
										Ladepunkte aktivieren
									</div>
									<div class="col form-text small">
										Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Ladepunkt 1
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidlp1start1" id="rfidlp1start1" class="form-control" value="<?php echo trim( $rfidlp1start1old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidlp1start2" id="rfidlp1start2" class="form-control" value="<?php echo trim( $rfidlp1start2old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidlp1start3" id="rfidlp1start3" class="form-control" value="<?php echo trim( $rfidlp1start3old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 4
												</div>
											</div>
											<input type="text" name="rfidlp1start4" id="rfidlp1start4" class="form-control" value="<?php echo trim( $rfidlp1start4old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 5
												</div>
											</div>
											<input type="text" name="rfidlp1start5" id="rfidlp1start5" class="form-control" value="<?php echo trim( $rfidlp1start5old ) ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Ladepunkt 2
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidlp2start1" id="rfidlp2start1" class="form-control" value="<?php echo trim( $rfidlp2start1old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidlp2start2" id="rfidlp2start2" class="form-control" value="<?php echo trim( $rfidlp2start2old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidlp2start3" id="rfidlp2start3" class="form-control" value="<?php echo trim( $rfidlp2start3old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 4
												</div>
											</div>
											<input type="text" name="rfidlp2start4" id="rfidlp2start4" class="form-control" value="<?php echo trim( $rfidlp2start4old ) ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 5
												</div>
											</div>
											<input type="text" name="rfidlp2start5" id="rfidlp2start5" class="form-control" value="<?php echo trim( $rfidlp2start5old ) ?>">
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							if($('#rfidaktOff').prop("checked")) {
								$('#rfidandiv').hide();
								$('#rfidan1div').hide();
								$('#rfidan2div').hide();
							} else {
								if($('#rfidaktOn1').prop("checked")) {
									$('#rfidandiv').show();
									$('#rfidan1div').show();
									$('#rfidan2div').hide();

								} else {
									$('#rfidandiv').show();
									$('#rfidan2div').show();
									$('#rfidan1div').hide();
								}
							}
							$('input[type=radio][name=rfidakt]').change(function(){
								$('#rfidandiv').hide();
								$('#rfidan1div').hide();
								$('#rfidan2div').hide();
								if(this.value == '0') {
									$('#rfidandiv').hide();
									$('#rfidan1div').hide();
									$('#rfidan2div').hide();
								} else {
									if(this.value == '1') {
										$('#rfidandiv').show();
										$('#rfidan1div').show();
									} else {
										$('#rfidandiv').show();
										$('#rfidan2div').show();
									}
								}
							});
						});
					</script>
				</div>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Benachrichtigungen mit Pushover</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($pushbenachrichtigungold == 0) echo " active" ?>">
											<input type="radio" name="pushbenachrichtigung" id="pushbenachrichtigungOff" value="0"<?php if($pushbenachrichtigungold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($pushbenachrichtigungold == 1) echo " active" ?>">
											<input type="radio" name="pushbenachrichtigung" id="pushbenachrichtigungOn" value="1"<?php if($pushbenachrichtigungold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="alert alert-info">
							Zur Nutzung von Pushover muss ein Konto auf Pushover.net bestehen. Nach dem Registrieren bei Pushover muss dort im Webinterface eine Applikation erstellt werden. Der Token der App, sowie das User Token nachfolgend eintragen.
						</div>
						<div id="pushban">
							<div class="form-group">
								<div class="form-row">
									<label for="pushoveruser" class="col-md-4 col-form-label">Pushover User String</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-user"></i>
												</div>
											</div> 
											<input type="text" name="pushoveruser" id="pushoveruser" value="<?php echo trim( $pushoveruserold ) ?>" placeholder="User Token" class="form-control">
										</div>
										<span class="form-text small">Hier das User Token von Pushover eintragen</span>
									</div>
								</div>
								<div class="form-row">
									<label for="pushovertoken" class="col-md-4 col-form-label">Pushover App Token</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-lock"></i>
												</div>
											</div> 
											<input type="text" name="pushovertoken" id="pushovertoken" value="<?php echo trim( $pushovertokenold ) ?>" placeholder="App Token" class="form-control">
										</div>
										<span class="form-text small">Hier das Application Token von Pushover eintragen</span>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-group">
								<div class="form-row">
									<div class="col">
										Benachrichtigungen
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Beim Starten der Ladung</label>
									</div>
									<div class="btn-group btn-group-toggle col-md-8" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($pushbstartlold == 0) echo " active" ?>">
											<input type="radio" name="pushbstartl" id="pushbstartlOff" value="0"<?php if($pushbstartlold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($pushbstartlold == 1) echo " active" ?>">
											<input type="radio" name="pushbstartl" id="pushbstartlOn" value="1"<?php if($pushbstartlold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Beim Stoppen der Ladung</label>
									</div>
									<div class="btn-group btn-group-toggle col-md-8" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($pushbstoplold == 0) echo " active" ?>">
											<input type="radio" name="pushbstopl" id="pushbstoplOff" value="0"<?php if($pushbstoplold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($pushbstoplold == 1) echo " active" ?>">
											<input type="radio" name="pushbstopl" id="pushbstoplOn" value="1"<?php if($pushbstoplold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Beim Einstecken des Fahrzeugs</label>
									</div>
									<div class="btn-group btn-group-toggle col-md-8" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($pushbplugold == 0) echo " active" ?>">
											<input type="radio" name="pushbplug" id="pushbplugOff" value="0"<?php if($pushbplugold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($pushbplugold == 1) echo " active" ?>">
											<input type="radio" name="pushbplug" id="pushbplugOn" value="1"<?php if($pushbplugold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Bei Triggern von Smart Home Aktionen</label>
									</div>
									<div class="btn-group btn-group-toggle col-md-8" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($pushbsmarthomeold == 0) echo " active" ?>">
											<input type="radio" name="pushbsmarthome" id="pushbsmarthomeOff" value="0"<?php if($pushbsmarthomeold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($pushbsmarthomeold == 1) echo " active" ?>">
											<input type="radio" name="pushbsmarthome" id="pushbsmarthomeOn" value="1"<?php if($pushbsmarthomeold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							if($('#pushbenachrichtigungOff').prop("checked")) {
								$('#pushban').hide();
							} else {
								$('#pushban').show();
							}
							$('input[type=radio][name=pushbenachrichtigung]').change(function(){
								if(this.value == '0') {
									$('#pushban').hide();
								} else {
									$('#pushban').show();
								}
							});
						});
					</script>
				</div>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">LED Ausgänge</div>
								<div class="col">
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($ledsaktold == 0) echo " active" ?>">
											<input type="radio" name="ledsakt" id="ledsaktOff" value="0"<?php if($ledsaktold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($ledsaktold == 1) echo " active" ?>">
											<input type="radio" name="ledsakt" id="ledsaktOn" value="1"<?php if($ledsaktold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body" id="ledsan">
						<div class="form-group">
							<div class="form-row">
								<div class="col">
									Ladung nicht freigegeben
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0sofort" class="col-md-4 col-form-label">Sofort Laden Modus</label>
								<div class="col">
									<select name="led0sofort" id="led0sofort" class="form-control">
										<option <?php if($led0sofortold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0sofortold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0sofortold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0sofortold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0sofortold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0sofortold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0sofortold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0sofortold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0sofortold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0sofortold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0sofortold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0sofortold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0sofortold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0sofortold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0nurpv" class="col-md-4 col-form-label">Nur PV Laden Modus</label>
								<div class="col">
									<select name="led0nurpv" id="led0nurpv" class="form-control">
										<option <?php if($led0nurpvold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0nurpvold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0nurpvold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0nurpvold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0nurpvold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0nurpvold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0nurpvold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0nurpvold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0nurpvold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0nurpvold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0nurpvold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0nurpvold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0nurpvold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0nurpvold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0minpv" class="col-md-4 col-form-label">Min + PV Laden Modus</label>
								<div class="col">
									<select name="led0minpv" id="led0minpv" class="form-control">
										<option <?php if($led0minpvold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0minpvold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0minpvold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0minpvold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0minpvold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0minpvold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0minpvold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0minpvold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0minpvold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0minpvold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0minpvold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0minpvold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0minpvold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0minpvold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0standby" class="col-md-4 col-form-label">Standby Modus</label>
								<div class="col">
									<select name="led0standby" id="led0standby" class="form-control">
										<option <?php if($led0standbyold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0standbyold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0standbyold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0standbyold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0standbyold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0standbyold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0standbyold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0standbyold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0standbyold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0standbyold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0standbyold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0standbyold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0standbyold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0standbyold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0stop" class="col-md-4 col-form-label">Stop Modus</label>
								<div class="col">
									<select name="led0stop" id="led0stop" class="form-control">
										<option <?php if($led0stopold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0stopold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0stopold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0stopold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0stopold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0stopold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0stopold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0stopold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0stopold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0stopold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0stopold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0stopold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0stopold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0stopold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row">
								<div class="col">
									Ladung freigegeben
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ledsofort" class="col-md-4 col-form-label">Sofort Laden Modus</label>
								<div class="col">
									<select name="ledsofort" id="ledsofort" class="form-control">
										<option <?php if($ledsofortold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($ledsofortold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($ledsofortold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($ledsofortold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($ledsofortold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($ledsofortold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($ledsofortold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($ledsofortold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($ledsofortold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($ledsofortold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($ledsofortold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($ledsofortold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($ledsofortold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($ledsofortold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="lednurpv" class="col-md-4 col-form-label">Nur PV Laden Modus</label>
								<div class="col">
									<select name="lednurpv" id="lednurpv" class="form-control">
										<option <?php if($lednurpvold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($lednurpvold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($lednurpvold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($lednurpvold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($lednurpvold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($lednurpvold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($lednurpvold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($lednurpvold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($lednurpvold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($lednurpvold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($lednurpvold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($lednurpvold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($lednurpvold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($lednurpvold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ledminpv" class="col-md-4 col-form-label">Min + PV Laden Modus</label>
								<div class="col">
									<select name="ledminpv" id="ledminpv" class="form-control">
										<option <?php if($ledminpvold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($ledminpvold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($ledminpvold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($ledminpvold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($ledminpvold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($ledminpvold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($ledminpvold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($ledminpvold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($ledminpvold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($ledminpvold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($ledminpvold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($ledminpvold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($ledminpvold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($ledminpvold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ledstandby" class="col-md-4 col-form-label">Standby Modus</label>
								<div class="col">
									<select name="ledstandby" id="ledstandby" class="form-control">
										<option <?php if($ledstandbyold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($ledstandbyold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($ledstandbyold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($ledstandbyold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($ledstandbyold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($ledstandbyold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($ledstandbyold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($ledstandbyold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($ledstandbyold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($ledstandbyold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($ledstandbyold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($ledstandbyold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($ledstandbyold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($ledstandbyold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ledstop" class="col-md-4 col-form-label">Stop Modus</label>
								<div class="col">
									<select name="ledstop" id="ledstop" class="form-control">
										<option <?php if($ledstopold == "aus\n") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($ledstopold == "an\n") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($ledstopold == "an1\n") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($ledstopold == "an2\n") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($ledstopold == "an3\n") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($ledstopold == "an12\n") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($ledstopold == "an13\n") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($ledstopold == "an23\n") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($ledstopold == "blink1\n") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($ledstopold == "blink2\n") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($ledstopold == "blink3\n") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($ledstopold == "blink12\n") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($ledstopold == "blink13\n") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($ledstopold == "blink23\n") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							if($('#ledsaktOff').prop("checked")) {
								$('#ledsan').hide();
							} else {
								$('#ledsan').show();
							}
							$('input[type=radio][name=ledsakt]').change(function(){
								if(this.value == '0') {
									$('#ledsan').hide();
								} else {
									$('#ledsan').show();
								}
							});
						});
					</script>
				</div>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
					<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">integriertes Display</div>
								<div class="col">
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($displayaktivold == 0) echo " active" ?>">
											<input type="radio" name="displayaktiv" id="displayaktivOff" value="0"<?php if($displayaktivold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($displayaktivold == 1) echo " active" ?>">
											<input type="radio" name="displayaktiv" id="displayaktivOn" value="1"<?php if($displayaktivold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body" id="displayan">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Tagesgraph anzeigen</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($displaytagesgraphold == 0) echo " active" ?>">
											<input type="radio" name="displaytagesgraph" id="displaytagesgraphOff" value="0"<?php if($displaytagesgraphold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($displaytagesgraphold == 1) echo " active" ?>">
											<input type="radio" name="displaytagesgraph" id="displaytagesgraphOn" value="1"<?php if($displaytagesgraphold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
									<span class="form-text small text-danger">Ja vermindert die Performance</span>
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label for="displaytheme" class="col-md-4 col-form-label">Theme des Displays</label>
								<div class="col">
									<select name="displaytheme" id="displaytheme" class="form-control">
										<option <?php if($displaythemeold == 0) echo "selected" ?> value="0">Gauges</option>
										<option <?php if($displaythemeold == 1) echo "selected" ?> value="1">Symbolfluss</option>
										<option <?php if($displaythemeold == 2) echo "selected" ?> value="2">Nur Ladeleistung, keine verstellmöglichkeit</option>
									</select>
								</div>
							</div>
							<div id="displaygauge">
								<div class="form-row vaRow mb-1">
									<label for="displayevumax" class="col-md-4 col-form-label">EVU Skala Min Max</label>
									<div class="col">
										<input type="number" min="5000" step="100" name="displayevumax" id="displayevumax" class="form-control" value="<?php echo trim( $displayevumaxold ) ?>">
									</div>
								</div>
								<div class="form-row vaRow mb-1">
									<label for="displaypvmax" class="col-md-4 col-form-label">PV Skala Max</label>
									<div class="col">
										<input type="number" min="1000" step="100" name="displaypvmax" id="displaypvmax" class="form-control" value="<?php echo trim( $displaypvmaxold ) ?>">
									</div>
								</div>
								<div class="form-row vaRow mb-1">
									<label for="displayspeichermax" class="col-md-4 col-form-label">Speicher Skala Min Max</label>
									<div class="col">
										<input type="number" min="1000" step="100" name="displayspeichermax" id="displayspeichermax" class="form-control" value="<?php echo trim( $displayspeichermaxold ) ?>">
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Hausverbrauch anzeigen</label>
									</div>
									<div class="col">
										<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($displayhausanzeigenold == 0) echo " active" ?>">
												<input type="radio" name="displayhausanzeigen" id="displayhausanzeigenOff" value="0"<?php if($displayhausanzeigenold == 0) echo " checked=\"checked\"" ?>>Nein
											</label>
											<label class="btn btn-outline-info<?php if($displayhausanzeigenold == 1) echo " active" ?>">
												<input type="radio" name="displayhausanzeigen" id="displayhausanzeigenOn" value="1"<?php if($displayhausanzeigenold == 1) echo " checked=\"checked\"" ?>>Ja
											</label>
										</div>
									</div>
								</div>
								<div class="form-row vaRow mb-1">
									<label for="displayhausmax" class="col-md-4 col-form-label">Hausverbrauch Skala Max</label>
									<div class="col">
										<input type="number" min="1000" step="100" name="displayhausmax" id="displayhausmax" class="form-control" value="<?php echo trim( $displayhausmaxold ) ?>">
									</div>
								</div>
								<div class="form-row vaRow mb-1">
									<label for="displaylp1max" class="col-md-4 col-form-label">Ladepunkt 1 Skala Max</label>
									<div class="col">
										<input type="number" min="1000" step="100" name="displaylp1max" id="displaylp1max" class="form-control" value="<?php echo trim( $displaylp1maxold ) ?>">
									</div>
								</div>
								<div class="form-row vaRow mb-1">
									<label for="displaylp2max" class="col-md-4 col-form-label">Ladepunkt 2 Skala Max</label>
									<div class="col">
										<input type="number" min="1000" step="100" name="displaylp2max" id="displaylp2max" class="form-control" value="<?php echo trim( $displaylp2maxold ) ?>">
									</div>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col">
									Pin-Sperre
								</div>
							</div>
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Pin nötig zum ändern des Lademodus</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($displaypinaktivold == 0) echo " active" ?>">
											<input type="radio" name="displaypinaktiv" id="displaypinaktivOff" value="0"<?php if($displaypinaktivold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($displaypinaktivold == 1) echo " active" ?>">
											<input type="radio" name="displaypinaktiv" id="displaypinaktivOn" value="1"<?php if($displaypinaktivold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div class="form-row vaRow mb-1" id="displaypin">
								<label for="displaypincode" class="col-md-4 col-form-label">Pin (nur Zahlen von 1-9 erlaubt)</label>
								<div class="col">
									<input type="text" pattern="[1-9]*" minlength="4" maxlength="4" size="4" name="displaypincode" id="displaypincode" class="form-control" value="<?php echo trim( $displaypincodeold ) ?>">
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col">
									Display Standby
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label for="displaysleep" class="col-md-4 col-form-label">ausschalten nach x Sekunden</label>
								<div class="col">
									<input type="number" min="5" step="5" name="displaysleep" id="displaysleep" class="form-control" value="<?php echo trim( $displaysleepold ) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">beim Einstecken des Fahrzeugs einschalten</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($displayEinBeimAnsteckenOld == 0) echo " active" ?>">
											<input type="radio" name="displayEinBeimAnstecken" id="displayEinBeimAnsteckenOff" value="0"<?php if($displayEinBeimAnsteckenOld == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($displayEinBeimAnsteckenOld == 1) echo " active" ?>">
											<input type="radio" name="displayEinBeimAnstecken" id="displayEinBeimAnsteckenOn" value="1"<?php if($displayEinBeimAnsteckenOld == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							if($('#displayaktivOff').prop("checked")) {
								$('#displayan').hide();
							} else {
								$('#displayan').show();
							}
							$('input[type=radio][name=displayaktiv]').change(function(){
								if(this.value == '0') {
									$('#displayan').hide();
								} else {
									$('#displayan').show();
								}
							});

							if($('#displaypinaktivOff').prop("checked")) {
								$('#displaypin').hide();
							} else {
								$('#displaypin').show();
							}
							$('input[type=radio][name=displaypinaktiv]').change(function(){
								if(this.value == '0') {
									$('#displaypin').hide();
								} else {
									$('#displaypin').show();
								}
							});
						});

						$(function() {
							if($('#displaytheme').val() == '0') {
								$('#displaygauge').show();
							} else {
								$('#displaygauge').hide();
							}
							$('#displaytheme').change(function(){
								if($('#displaytheme').val() == '0') {
									$('#displaygauge').show();
								} else {
									$('#displaygauge').hide();
								}
							});
						});
					</script>
				</div>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Web-Theme Optionen
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Hausverbrauch auf der Hauptseite anzeigen</label>
								</div>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($hausverbrauchstatold == 0) echo " active" ?>">
										<input type="radio" name="hausverbrauchstat" id="hausverbrauchstatOff" value="0"<?php if($hausverbrauchstatold == 0) echo " checked=\"checked\"" ?>>Nein
									</label>
									<label class="btn btn-outline-info<?php if($hausverbrauchstatold == 1) echo " active" ?>">
										<input type="radio" name="hausverbrauchstat" id="hausverbrauchstatOn" value="1"<?php if($hausverbrauchstatold == 1) echo " checked=\"checked\"" ?>>Ja
									</label>
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Heute geladen auf der Hauptseite anzeigen</label>
								</div>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($heutegeladenold == 0) echo " active" ?>">
										<input type="radio" name="heutegeladen" id="heutegeladenOff" value="0"<?php if($heutegeladenold == 0) echo " checked=\"checked\"" ?>>Nein
									</label>
									<label class="btn btn-outline-info<?php if($heutegeladenold == 1) echo " active" ?>">
										<input type="radio" name="heutegeladen" id="heutegeladenOn" value="1"<?php if($heutegeladenold == 1) echo " checked=\"checked\"" ?>>Ja
									</label>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="livegraph" class="col-md-4 col-form-label">Zeitintervall für den Live Graphen der Hauptseite</label>
								<div class="col-md-8">
									<div class="form-row vaRow mb-1">
										<label for="livegraph" class="col-2 col-form-label valueLabel" suffix="Min"><?php echo trim($livegraphold); ?> Min</label>
										<div class="col-10">
											<input type="range" class="form-control-range rangeInput" name="livegraph" id="livegraph" min="10" max="120" step="10" value="<?php echo trim($livegraphold); ?>">
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="form-row text-center">
					<div class="col">
						<button id="saveSettingsBtn" type="submit" class="btn btn-success">Speichern</button>
					</div>
				</div>
			</form>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Verschiedenes</small>
			</div>
		</footer>

		<script>
			$('.rangeInput').on('input', function() {
				// show slider value in label of class valueLabel
				updateLabel($(this).attr('id'));
			});

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navVerschiedenes').addClass('disabled');
				}
			);
		</script>

	</body>
</html>
