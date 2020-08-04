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
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
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
			<form action="./tools/savemisc.php" method="POST">
				<div class="card">
					<div class="card-header bg-secondary font-weight-bold">
						Allgemeine Funktionen
					</div>
					<div class="card-body">
						<div class="row form-group">
							<label for="dspeed" class="col-6 col-form-label">Geschwindigkeit Regelintervall:</label>
							<div class="col-6">
								<select name="dspeed" id="dspeed" class="form-control">
									<option <?php if($dspeedold == 0) echo "selected" ?> value="0">Normal</option>
									<option <?php if($dspeedold == 2) echo "selected" ?> value="2">Langsam</option>
									<option <?php if($dspeedold == 3) echo "selected" ?> value="3">Sehr Langsam</option>
								</select>
							</div>
						</div>
						<div class="row form-group">
							Sollten Probleme, oder Fehlermeldungen, auftauchen, zunächst das Regelintervall auf "Normal" stellen.<br>
							Werden Module genutzt, welche z.B. eine Online API zur Abfrage nutzen, oder möchte man weniger regeln, kann man das Regelintervall auf "Langsam" (=20Sekunden) herabsetzen. <br>
							!Bitte beachten! Nicht nur die Regelung der PV geführten Ladung, sondern auch Ladestromänderung, beispielsweise “Stop“etc, werden dann nur noch alle 20 Sekunden ausgeführt. Die Regelung wird träger.<br>
							Die Einstellungen „Sehr Langsam“ führt zu einer Regelzeit von 60Sek.
						</div>
						<div class="row form-group">
							<label for="ladetaster" class="col-6 col-form-label">Ladetaster:</label>
							<div class="col-6">
								<select name="ladetaster" id="ladetaster" class="form-control">
									<option <?php if($ladetasterold == 0) echo "selected" ?> value="0">Aus</option>
									<option <?php if($ladetasterold == 1) echo "selected" ?> value="1">An</option>
								</select>
							</div>
						</div>
						<div class="row form-group">
							Wenn aktiviert, sind nach einem Neustart die externen Taster aktiv. Wenn keine verbaut sind, diese Option ausschalten.
						</div>
						<div class="row form-group">
							<label for="bootmodus" class="col-6 col-form-label">Lademodus nach Start der openWB:</label>
							<div class="col-6">
								<select name="bootmodus" id="bootmodus" class="form-control">
									<option <?php if($bootmodusold == 0) echo "selected" ?> value="0">Sofort Laden</option>
									<option <?php if($bootmodusold == 1) echo "selected" ?> value="1">Min + PV</option>
									<option <?php if($bootmodusold == 2) echo "selected" ?> value="2">Nur PV</option>
									<option <?php if($bootmodusold == 3) echo "selected" ?> value="3">Stop</option>
									<option <?php if($bootmodusold == 4) echo "selected" ?> value="4">Standby</option>
								</select>
							</div>
						</div>
						<div class="row form-group">
							Definiert den Lademodus nach Boot der openWB.
						</div>
						<div class="row form-group">
							<label for="netzabschaltunghz" class="col-6 col-form-label">Netzschutz:</label>
							<div class="col-6">
								<select name="netzabschaltunghz" id="netzabschaltunghz" class="form-control">
									<option <?php if($netzabschaltunghzold == 0) echo "selected" ?> value="0">Deaktiviert</option>
									<option <?php if($netzabschaltunghzold == 1) echo "selected" ?> value="1">Aktiviert</option>
								</select>
							</div>
						</div>
						<div class="row form-group">
							Diese Option ist standardmäßig aktiviert und sollte so belassen werden. Bei Unterschreitung einer kritischen Frequenz des Stromnetzes wird die Ladung nach einer zufälligen Zeit zwischen 1 und 90 Sekunden pausiert. Der Lademodus wechselt auf "Stop".<br>
							Sobald die Frequenz wieder in einem normalen Bereich ist wird automatisch der zuletzt gewählte Lademodus wieder aktiviert.<br>
							Ebenso wird die Ladung bei Überschreiten von 51,8 Hz unterbrochen. <br>
							Dies ist dann der Fall, wenn der Energieversorger Wartungsarbeiten am (Teil-)Netz durchführt und auf einen vorübergehenden Generatorbetrieb umschaltet.<br>
							Die Erhöhung der Frequenz wird durchgeführt, um die PV Anlagen abzuschalten.<br>
							Die Option ist nur aktiv, wenn der Ladepunkt die Frequenz übermittelt. Jede openWB series1/2 tut dies.
						</div>
						<div class="row form-group">
							<label for="cpunterbrechunglp1" class="col-6 col-form-label">CP Unterbrechung LP1:</label>
							<div class="col-6">
								<select name="cpunterbrechunglp1" id="cpunterbrechunglp1" class="form-control">
									<option <?php if($cpunterbrechunglp1old == 0) echo "selected" ?> value="0">Deaktiviert</option>
									<option <?php if($cpunterbrechunglp1old == 1) echo "selected" ?> value="1">Aktiviert</option>
								</select>
							</div>
						</div>
						<div class="row form-group">
							<label for="cpunterbrechunglp2" class="col-6 col-form-label">CP Unterbrechung LP2:</label>
							<div class="col-6">
								<select name="cpunterbrechunglp2" id="cpunterbrechunglp2" class="form-control">
									<option <?php if($cpunterbrechunglp2old == 0) echo "selected" ?> value="0">Deaktiviert</option>
									<option <?php if($cpunterbrechunglp2old == 1) echo "selected" ?> value="1">Aktiviert</option>
								</select>
							</div>
						</div>
						<div class="row form-group">
							Diese Option erfordert die verbaute Addon Platine und die korrekte Verdrahtung des CP Signals durch die Addon Platine.<br>
							Sie ist für Fahrzeuge, die nach einer gewissen Zeit einer pausierten Ladung nicht von alleine die Ladung wieder beginnen. Nur aktivieren, wenn es ohne die Option Probleme gibt.
						</div>
					</div>
				</div>

				<div class="card">
					<div class="card-header bg-secondary font-weight-bold">
						RFID
					</div>
					<div class="card-body">
						<div class="row form-group">
							<label for="rfidakt" class="col-6 col-form-label">RFID Lesung:</label>
							<div class="col-6">
								<select name="rfidakt" id="rfidakt" class="form-control">
									<option <?php if($rfidaktold == 0) echo "selected" ?> value="0">Deaktiviert</option>
									<option <?php if($rfidaktold == 1) echo "selected" ?> value="1">Aktiviert</option>
								</select>
							</div>
						</div>
						<div id="rfidandiv">
							<div class="row form-group">
								Durch scannen von RFID Tags lässt sich die Ladung einem RFID Tag zuweisen. Derzeit unterstützt werden openWB RFID Leser und go-e an LP1.<br>
								Wenn die Option RFID mitgekauft wurde befindet sich dieser unten mittig. Das Scannen wird durch einen Piepton sowie das angehen des Displays (sofern vorhanden) signalisiert.
							</div>
							<div class="row form-group">
								Zuletzt gescannter RFID Tag: <?php echo trim( $lastrfid ) ?>
							</div>
							<div class="row form-group">
								<label for="rfidlp1c1" class="col-6 col-form-label">Ladepunkt 1, Auto 1:</label>
								<div class="col-6">
									<input type="text" name="rfidlp1c1" id="rfidlp1c1" class="form-control" value="<?php echo trim( $rfidlp1c1old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen.
							</div>
							<div class="row form-group">
								<label for="rfidlp1c2" class="col-6 col-form-label">Ladepunkt 1, Auto 2:</label>
								<div class="col-6">
									<input type="text" name="rfidlp1c2" id="rfidlp1c2" class="form-control" value="<?php echo trim( $rfidlp1c2old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen.
							</div>
							<div class="row form-group">
								<label for="rfidlp1c3" class="col-6 col-form-label">Ladepunkt 1, Auto 3:</label>
								<div class="col-6">
									<input type="text" name="rfidlp1c3" id="rfidlp1c3" class="form-control" value="<?php echo trim( $rfidlp1c3old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen.
							</div>
							<div class="row form-group">
								<label for="rfidlp2c1" class="col-6 col-form-label">Ladepunkt 2, Auto 1:</label>
								<div class="col-6">
									<input type="text" name="rfidlp2c1" id="rfidlp2c1" class="form-control" value="<?php echo trim( $rfidlp2c1old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen.
							</div>
							<div class="row form-group">
								<label for="rfidlp2c2" class="col-6 col-form-label">Ladepunkt 2, Auto 2:</label>
								<div class="col-6">
									<input type="text" name="rfidlp2c2" id="rfidlp2c2" class="form-control" value="<?php echo trim( $rfidlp2c2old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen.
							</div>
							<div class="row form-group">
								<label for="rfidlp2c3" class="col-6 col-form-label">Ladepunkt 2, Auto 3:</label>
								<div class="col-6">
									<input type="text" name="rfidlp2c3" id="rfidlp2c3" class="form-control" value="<?php echo trim( $rfidlp2c3old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen.
							</div>
							<div class="row form-group">
								<label for="rfidstop" class="col-6 col-form-label">Ändere Lademodus auf Stop:</label>
								<div class="col-6">
									<input type="text" name="rfidstop" id="rfidstop" class="form-control" value="<?php echo trim( $rfidstopold ) ?>">
									<input type="text" name="rfidstop2" id="rfidstop2" class="form-control" value="<?php echo trim( $rfidstop2old ) ?>">
									<input type="text" name="rfidstop3" id="rfidstop3" class="form-control" value="<?php echo trim( $rfidstop3old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
							</div>
							<div class="row form-group">
								<label for="rfidstandby" class="col-6 col-form-label">Ändere Lademodus auf Standby:</label>
								<div class="col-6">
									<input type="text" name="rfidstandby" id="rfidstandby" class="form-control" value="<?php echo trim( $rfidstandbyold ) ?>">
									<input type="text" name="rfidstandby2" id="rfidstandby2" class="form-control" value="<?php echo trim( $rfidstandby2old ) ?>">
									<input type="text" name="rfidstandby3" id="rfidstandby3" class="form-control" value="<?php echo trim( $rfidstandby3old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
							</div>
							<div class="row form-group">
								<label for="rfidsofort" class="col-6 col-form-label">Ändere Lademodus auf Sofort Laden:</label>
								<div class="col-6">
									<input type="text" name="rfidsofort" id="rfidsofort" class="form-control" value="<?php echo trim( $rfidsofortold ) ?>">
									<input type="text" name="rfidsofort2" id="rfidsofort2" class="form-control" value="<?php echo trim( $rfidsofort2old ) ?>">
									<input type="text" name="rfidsofort3" id="rfidsofort3" class="form-control" value="<?php echo trim( $rfidsofort3old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
							</div>
							<div class="row form-group">
								<label for="rfidminpv" class="col-6 col-form-label">Ändere Lademodus auf Min + PV Laden:</label>
								<div class="col-6">
									<input type="text" name="rfidminpv" id="rfidminpv" class="form-control" value="<?php echo trim( $rfidminpvold ) ?>">
									<input type="text" name="rfidminpv2" id="rfidminpv2" class="form-control" value="<?php echo trim( $rfidminpv2old ) ?>">
									<input type="text" name="rfidminpv3" id="rfidminpv3" class="form-control" value="<?php echo trim( $rfidminpv3old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
							</div>
							<div class="row form-group">
								<label for="rfidnurpv" class="col-6 col-form-label">Ändere Lademodus auf Nur PV:</label>
								<div class="col-6">
									<input type="text" name="rfidnurpv" id="rfidnurpv" class="form-control" value="<?php echo trim( $rfidnurpvold ) ?>">
									<input type="text" name="rfidnurpv2" id="rfidnurpv2" class="form-control" value="<?php echo trim( $rfidnurpv2old ) ?>">
									<input type="text" name="rfidnurpv3" id="rfidnurpv3" class="form-control" value="<?php echo trim( $rfidnurpv3old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
							</div>
							<div class="row form-group">
								<label for="rfidlp1start1" class="col-6 col-form-label">Aktiviere Ladepunkt 1:</label>
								<div class="col-6">
									<input type="text" name="rfidlp1start1" id="rfidlp1start1" class="form-control" value="<?php echo trim( $rfidlp1start1old ) ?>">
									<input type="text" name="rfidlp1start2" id="rfidlp1start2" class="form-control" value="<?php echo trim( $rfidlp1start2old ) ?>">
									<input type="text" name="rfidlp1start3" id="rfidlp1start3" class="form-control" value="<?php echo trim( $rfidlp1start3old ) ?>">
									<input type="text" name="rfidlp1start4" id="rfidlp1start4" class="form-control" value="<?php echo trim( $rfidlp1start4old ) ?>">
									<input type="text" name="rfidlp1start5" id="rfidlp1start5" class="form-control" value="<?php echo trim( $rfidlp1start5old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
							</div>
							<div class="row form-group">
								<label for="rfidlp2start1" class="col-6 col-form-label">Aktiviere Ladepunkt 2:</label>
								<div class="col-6">
									<input type="text" name="rfidlp2start1" id="rfidlp2start1" class="form-control" value="<?php echo trim( $rfidlp2start1old ) ?>">
									<input type="text" name="rfidlp2start2" id="rfidlp2start2" class="form-control" value="<?php echo trim( $rfidlp2start2old ) ?>">
									<input type="text" name="rfidlp2start3" id="rfidlp2start3" class="form-control" value="<?php echo trim( $rfidlp2start3old ) ?>">
									<input type="text" name="rfidlp2start4" id="rfidlp2start4" class="form-control" value="<?php echo trim( $rfidlp2start4old ) ?>">
									<input type="text" name="rfidlp2start5" id="rfidlp2start5" class="form-control" value="<?php echo trim( $rfidlp2start5old ) ?>">
								</div>
							</div>
							<div class="row form-group">
								RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
							</div>
						</div>
					</div>
					<script>
						$(function() {
							if($('#rfidakt').val() == '0') {
								$('#rfidandiv').hide();
							} else {
								$('#rfidandiv').show();
							}

							$('#rfidakt').change(function(){
								if($('#rfidakt').val() == '0') {
									$('#rfidandiv').hide();
								} else {
									$('#rfidandiv').show();
								}
							});
						});
					</script>
				</div>

				<div class="card">
					<div class="card-header bg-secondary font-weight-bold">
						Benachrichtigungen mit Pushover
					</div>
					<div class="card-body">
						<div class="row form-group">
							<label for="pushbenachrichtigung" class="col-6 col-form-label">Pushover Benachrichtigungen:</label>
							<div class="col-6">
								<select name="pushbenachrichtigung" id="pushbenachrichtigung" class="form-control">
									<option <?php if($pushbenachrichtigungold == 0) echo "selected" ?> value="0">Deaktiviert</option>
									<option <?php if($pushbenachrichtigungold == 1) echo "selected" ?> value="1">Aktiviert</option>
								</select>
							</div>
						</div>
						<div id="pushban">
							<div class="row form-group">
								Zur Nutzung von Pushover muss ein Konto auf Pushover.net bestehen.<br>
								Nach dem Registrieren bei Pushover muss dort im Webinterface eine Applikation erstellt werden.<br>
								Der Token der App, sowie das User Token nachfolgend eintragen.
							</div>
							<div class="row form-group">
								<label for="pushoveruser" class="col-6 col-form-label">Pushover User String:</label>
								<div class="col-6">
									<input type="text" name="pushoveruser" id="pushoveruser" class="form-control" value="<?php echo trim( $pushoveruserold ) ?>">
								</div>
							</div>
							<div class="row form-group">
								Hier das User Token von Pushover eintragen
							</div>
							<div class="row form-group">
								<label for="pushovertoken" class="col-6 col-form-label">Pushover App Token:</label>
								<div class="col-6">
									<input type="text" name="pushovertoken" id="pushovertoken" class="form-control" value="<?php echo trim( $pushovertokenold ) ?>">
								</div>
							</div>
							<div class="row form-group">
								Hier das Application Token von Pushover eintragen
							</div>
							<div class="row form-group">
								<b>Benachrichtigungseinstellungen:</b>
							</div>
							<div class="row form-group">
								<label for="pushbstartl" class="col-6 col-form-label">Beim Starten der Ladung:</label>
								<div class="col-6">
									<select name="pushbstartl" id="pushbstartl" class="form-control">
										<option <?php if($pushbstartlold == 0) echo "selected" ?> value="0">Nein</option>
										<option <?php if($pushbstartlold == 1) echo "selected" ?> value="1">Ja</option>
									</select>
								</div>
							</div>
							<div class="row form-group">
								<label for="pushbstopl" class="col-6 col-form-label">Beim Stoppen der Ladung:</label>
								<div class="col-6">
									<select name="pushbstopl" id="pushbstopl" class="form-control">
										<option <?php if($pushbstoplold == 0) echo "selected" ?> value="0">Nein</option>
										<option <?php if($pushbstoplold == 1) echo "selected" ?> value="1">Ja</option>
									</select>
								</div>
							</div>
							<div class="row form-group">
								<label for="pushbplug" class="col-6 col-form-label">Beim Einstecken des Fahrzeugs:</label>
								<div class="col-6">
									<select name="pushbplug" id="pushbplug" class="form-control">
										<option <?php if($pushbplugold == 0) echo "selected" ?> value="0">Nein</option>
										<option <?php if($pushbplugold == 1) echo "selected" ?> value="1">Ja</option>
									</select>
								</div>
							</div>
							<div class="row form-group">
								<label for="pushbsmarthome" class="col-6 col-form-label">Bei Triggern von Smart Home Aktionen:</label>
								<div class="col-6">
									<select name="pushbsmarthome" id="pushbsmarthome" class="form-control">
										<option <?php if($pushbsmarthomeold == 0) echo "selected" ?> value="0">Nein</option>
										<option <?php if($pushbsmarthomeold == 1) echo "selected" ?> value="1">Ja</option>
									</select>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							if($('#pushbenachrichtigung').val() == '0') {
								$('#pushban').hide();
							} else {
								$('#pushban').show();
							}
							$('#pushbenachrichtigung').change(function(){
								if($('#pushbenachrichtigung').val() == '0') {
									$('#pushban').hide();
								} else {
									$('#pushban').show();
								}
							});
						});
					</script>
				</div>

				<div class="card">
					<div class="card-header bg-secondary font-weight-bold">
						LED Ausgänge
					</div>
					<div class="card-body">
						<div class="row form-group">
							<label for="ledsakt" class="col-6 col-form-label">LED Ausgänge:</label>
							<div class="col-6">
								<select name="ledsakt" id="ledsakt" class="form-control">
									<option <?php if($ledsaktold == 0) echo "selected" ?> value="0">Nein</option>
									<option <?php if($ledsaktold == 1) echo "selected" ?> value="1">Ja</option>
								</select>
							</div>
						</div>

						<div id="ledsan">
							<div class="row form-group">
								<label for="led0sofort" class="col-6 col-form-label">Ladung nicht freigegeben, Sofort Laden Modus:</label>
								<div class="col-6">
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
							<div class="row form-group">
								<label for="led0nurpv" class="col-6 col-form-label">Ladung nicht freigegeben, Nur PV Laden Modus:</label>
								<div class="col-6">
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
							<div class="row form-group">
								<label for="led0minpv" class="col-6 col-form-label">Ladung nicht freigegeben, Min + PV Laden Modus:</label>
								<div class="col-6">
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
							<div class="row form-group">
								<label for="led0standby" class="col-6 col-form-label">Ladung nicht freigegeben, Standby Modus:</label>
								<div class="col-6">
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
							<div class="row form-group">
								<label for="led0stop" class="col-6 col-form-label">Ladung nicht freigegeben, Stop Modus:</label>
								<div class="col-6">
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
							<div class="row form-group">
								<label for="ledsofort" class="col-6 col-form-label">Ladung freigegeben, Sofort Laden Modus:</label>
								<div class="col-6">
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
							<div class="row form-group">
								<label for="lednurpv" class="col-6 col-form-label">Ladung freigegeben, Nur PV Laden Modus:</label>
								<div class="col-6">
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
							<div class="row form-group">
								<label for="ledminpv" class="col-6 col-form-label">Ladung freigegeben, Min + PV Laden Modus:</label>
								<div class="col-6">
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
							<div class="row form-group">
								<label for="ledstandby" class="col-6 col-form-label">Ladung freigegeben, Standby Modus:</label>
								<div class="col-6">
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
							<div class="row form-group">
								<label for="ledstop" class="col-6 col-form-label">Ladung freigegeben, Stop Modus:</label>
								<div class="col-6">
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
							if($('#ledsakt').val() == '0') {
								$('#ledsan').hide();
							} else {
								$('#ledsan').show();
							}
							$('#ledsakt').change(function(){
								if($('#ledsakt').val() == '0') {
									$('#ledsan').hide();
								} else {
									$('#ledsan').show();
								}
							});
						});
					</script>
				</div>

				<div class="card">
					<div class="card-header bg-secondary font-weight-bold">
						integriertes Display
					</div>
					<div class="card-body">
						<div class="row form-group">
							<label for="displayaktiv" class="col-6 col-form-label">Display installiert:</label>
							<div class="col-6">
								<select name="displayaktiv" id="displayaktiv" class="form-control">
									<option <?php if($displayaktivold == 0) echo "selected" ?> value="0">Nein</option>
									<option <?php if($displayaktivold == 1) echo "selected" ?> value="1">Ja</option>
								</select>
							</div>
						</div>
						<div id="displayan">
							<div class="row form-group">
								<label for="displaytagesgraph" class="col-6 col-form-label">Tagesgraph anzeigbar (Ja vermindert die Performance):</label>
								<div class="col-6">
									<select name="displaytagesgraph" id="displaytagesgraph" class="form-control">
										<option <?php if($displaytagesgraphold == 0) echo "selected" ?> value="0">Nein</option>
										<option <?php if($displaytagesgraphold == 1) echo "selected" ?> value="1">Ja</option>
									</select>
								</div>
							</div>
							<div class="row form-group">
								<label for="displaytheme" class="col-6 col-form-label">Theme des Displays:</label>
								<div class="col-6">
									<select name="displaytheme" id="displaytheme" class="form-control">
										<option <?php if($displaythemeold == 0) echo "selected" ?> value="0">Gauges</option>
										<option <?php if($displaythemeold == 1) echo "selected" ?> value="1">Symbolfluss</option>
										<option <?php if($displaythemeold == 2) echo "selected" ?> value="2">Nur Ladeleistung, keine verstellmöglichkeit</option>
									</select>
								</div>
							</div>
							<div id="displaygauge">
								<div class="row form-group">
									<label for="displayevumax" class="col-6 col-form-label">EVU Skala Min Max:</label>
									<div class="col-6">
										<input type="text" name="displayevumax" id="displayevumax" class="form-control" value="<?php echo trim( $displayevumaxold ) ?>">
									</div>
								</div>
								<div class="row form-group">
									<label for="displaypvmax" class="col-6 col-form-label">PV Skala Max:</label>
									<div class="col-6">
										<input type="text" name="displaypvmax" id="displaypvmax" class="form-control" value="<?php echo trim( $displaypvmaxold ) ?>">
									</div>
								</div>
								<div class="row form-group">
									<label for="displayspeichermax" class="col-6 col-form-label">Speicher Skala Min Max:</label>
									<div class="col-6">
										<input type="text" name="displayspeichermax" id="displayspeichermax" class="form-control" value="<?php echo trim( $displayspeichermaxold ) ?>">
									</div>
								</div>
								<div class="row form-group">
									<label for="displayhausanzeigen" class="col-6 col-form-label">Hausverbrauch anzeigen:</label>
									<div class="col-6">
										<select name="displayhausanzeigen" id="displayhausanzeigen" class="form-control">
											<option <?php if($displayhausanzeigenold == 0) echo "selected" ?> value="0">Nein</option>
											<option <?php if($displayhausanzeigenold == 1) echo "selected" ?> value="1">Ja</option>
										</select>
									</div>
								</div>
								<div class="row form-group">
									<label for="displayhausmax" class="col-6 col-form-label">Hausverbrauch Skala Max:</label>
									<div class="col-6">
										<input type="text" name="displayhausmax" id="displayhausmax" class="form-control" value="<?php echo trim( $displayhausmaxold ) ?>">
									</div>
								</div>
								<div class="row form-group">
									<label for="displaylp1max" class="col-6 col-form-label">Ladepunkt 1 Skala Max:</label>
									<div class="col-6">
										<input type="text" name="displaylp1max" id="displaylp1max" class="form-control" value="<?php echo trim( $displaylp1maxold ) ?>">
									</div>
								</div>
								<div class="row form-group">
									<label for="displaylp2max" class="col-6 col-form-label">Ladepunkt 2 Skala Max:</label>
									<div class="col-6">
										<input type="text" name="displaylp2max" id="displaylp2max" class="form-control" value="<?php echo trim( $displaylp2maxold ) ?>">
									</div>
								</div>
							</div>
							<div class="row form-group">
								<label for="displaypinaktiv" class="col-6 col-form-label">Pin nötig zum ändern des Lademodus:</label>
								<div class="col-6">
									<select name="displaypinaktiv" id="displaypinaktiv" class="form-control">
										<option <?php if($displaypinaktivold == 0) echo "selected" ?> value="0">Nein</option>
										<option <?php if($displaypinaktivold == 1) echo "selected" ?> value="1">Ja</option>
									</select>
								</div>
							</div>
							<div class="row form-group">
								<label for="displaypincode" class="col-6 col-form-label">Pin (4-stellig, nur Zahlen erlaubt von 1-9):</label>
								<div class="col-6">
									<input type="text" name="displaypincode" id="displaypincode" class="form-control" value="<?php echo trim( $displaypincodeold ) ?>">
								</div>
							</div>
							<div class="row form-group">
								<label for="displaysleep" class="col-6 col-form-label">Display ausschalten nach x Sekunden:</label>
								<div class="col-6">
									<input type="text" name="displaysleep" id="displaysleep" class="form-control" value="<?php echo trim( $displaysleepold ) ?>">
								</div>
							</div>
							<div class="row form-group">
								<label for="displayEinBeimAnstecken" class="col-6 col-form-label">Display beim Einstecken des Fahrzeugs einschalten<br/><small>(f&uuml;r oben konfigurierte Dauer):</small></label>
								<div class="col-6">
									<select name="displayEinBeimAnstecken" id="displayEinBeimAnstecken" class="form-control">
										<option <?php if($displayEinBeimAnsteckenOld == 0) echo "selected" ?> value="0">Nein</option>
										<option <?php if($displayEinBeimAnsteckenOld == 1) echo "selected" ?> value="1">Ja</option>
									</select>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							if($('#displayaktiv').val() == '0') {
								$('#displayan').hide();
							} else {
								$('#displayan').show();
							}
							$('#displayaktiv').change(function(){
								if($('#displayaktiv').val() == '0') {
									$('#displayan').hide();
								} else {
									$('#displayan').show();
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

				<div class="card">
					<div class="card-header bg-secondary font-weight-bold">
						Theme Optionen
					</div>
					<div class="card-body">
						<div class="form-group row">
							<label for="hausverbrauchstat" class="col-6 col-form-label">Hausverbrauch auf der Hauptseite anzeigen:</label>
							<div class="col-6">
								<select name="hausverbrauchstat" id="hausverbrauchstat" class="form-control">
									<option <?php if($hausverbrauchstatold == 0) echo "selected" ?> value="0">Aus</option>
									<option <?php if($hausverbrauchstatold == 1) echo "selected" ?> value="1">Ein</option>
								</select>
							</div>
						</div>
						<div class="form-group row">
							<label for="heutegeladen" class="col-6 col-form-label">Heute geladen auf der Hauptseite anzeigen:</label>
							<div class="col-6">
								<select name="heutegeladen" id="heutegeladen" class="form-control">
									<option <?php if($heutegeladenold == 0) echo "selected" ?> value="0">Aus</option>
									<option <?php if($heutegeladenold == 1) echo "selected" ?> value="1">Ein</option>
								</select>
							</div>
						</div>
						<div class="form-group row mb-0">
							<label for="livegraph" class="col-6 col-form-label">Zeitintervall für den Live Graphen der Hauptseite:</label>
							<div class="col-6">
								<select name="livegraph" id="livegraph" class="form-control">
									<option <?php if($livegraphold == 5) echo "selected" ?> value="5">5 Min</option>
									<option <?php if($livegraphold == 10) echo "selected" ?> value="10">10 Min</option>
									<option <?php if($livegraphold == 15) echo "selected" ?> value="15">15 Min</option>
									<option <?php if($livegraphold == 20) echo "selected" ?> value="20">20 Min</option>
									<option <?php if($livegraphold == 30) echo "selected" ?> value="30">30 Min</option>
									<option <?php if($livegraphold == 40) echo "selected" ?> value="40">40 Min</option>
									<option <?php if($livegraphold == 50) echo "selected" ?> value="50">50 Min</option>
									<option <?php if($livegraphold == 60) echo "selected" ?> value="60">60 Min</option>
									<option <?php if($livegraphold == 70) echo "selected" ?> value="70">70 Min</option>
									<option <?php if($livegraphold == 80) echo "selected" ?> value="80">80 Min</option>
									<option <?php if($livegraphold == 90) echo "selected" ?> value="90">90 Min</option>
									<option <?php if($livegraphold == 100) echo "selected" ?> value="100">100 Min</option>
									<option <?php if($livegraphold == 110) echo "selected" ?> value="110">110 Min</option>
									<option <?php if($livegraphold == 120) echo "selected" ?> value="120">120 Min</option>
								</select>
							</div>
						</div>
					</div>
				</div>

				<div class="row text-center">
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
			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navVerschiedenes').addClass('disabled');
			});
		</script>

	</body>
</html>
