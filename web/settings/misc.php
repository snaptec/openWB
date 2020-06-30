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
			<div class="col-sm-12">
				<form action="./tools/savemisc.php" method="POST">
					<div class="row">
						<b><label for="dspeed">Geschwindigkeit Regelintervall:</label></b>
						<select name="dspeed" id="dspeed">
							<option <?php if($dspeedold == 0) echo "selected" ?> value="0">Normal</option>
							<option <?php if($dspeedold == 2) echo "selected" ?> value="2">Langsam</option>
							<option <?php if($dspeedold == 3) echo "selected" ?> value="3">Sehr Langsam</option>
						</select>
					</div>

					<div class="row">
						Sollten Probleme, oder Fehlermeldungen, auftauchen, zunächst das Regelintervall auf "Normal" stellen.<br>
						Werden Module genutzt, welche z.B. eine Online API zur Abfrage nutzen, oder möchte man weniger regeln, kann man das Regelintervall auf "Langsam" (=20Sekunden) herabsetzen. <br>
						!Bitte beachten! Nicht nur die Regelung der PV geführten Ladung, sondern auch Ladestromänderung, beispielsweise “Stop“etc, werden dann nur noch alle 20 Sekunden ausgeführt. Die Regelung wird träger.<br>
						Die Einstellungen „Sehr Langsam“ führt zu einer Regelzeit von 60Sek.
					</div>
					<div class="row">
						<b><label for="ladetaster">Ladetaster:</label></b>
						<select name="ladetaster" id="ladetaster">
							<option <?php if($ladetasterold == 0) echo "selected" ?> value="0">Aus</option>
							<option <?php if($ladetasterold == 1) echo "selected" ?> value="1">An</option>
						</select>
					</div>
					<div class="row">
						Wenn aktiviert, sind nach einem Neustart die externen Taster aktiv. Wenn keine verbaut sind, diese Option ausschalten.
					</div>
					<div class="row">
						<b><label for="bootmodus">Lademodus nach Start der openWB:</label></b>
						<select name="bootmodus" id="bootmodus">
							<option <?php if($bootmodusold == 0) echo "selected" ?> value="0">Sofort Laden</option>
							<option <?php if($bootmodusold == 1) echo "selected" ?> value="1">Min + PV</option>
							<option <?php if($bootmodusold == 2) echo "selected" ?> value="2">Nur PV</option>
							<option <?php if($bootmodusold == 3) echo "selected" ?> value="3">Stop</option>
							<option <?php if($bootmodusold == 4) echo "selected" ?> value="4">Standby</option>
						</select>
					</div>
					<div class="row">
						Definiert den Lademodus nach Boot der openWB.
					</div>
					<div class="row">
						<b><label for="netzabschaltunghz">Netzschutz:</label></b>
						<select name="netzabschaltunghz" id="netzabschaltunghz">
							<option <?php if($netzabschaltunghzold == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($netzabschaltunghzold == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>
					<div class="row">
						Diese Option ist standardmäßig aktiviert und sollte so belassen werden. Bei Unterschreitung einer kritischen Frequenz des Stromnetzes wird die Ladung nach einer zufälligen Zeit zwischen 1 und 90 Sekunden pausiert. Der Lademodus wechselt auf "Stop".<br>
						Sobald die Frequenz wieder in einem normalen Bereich ist wird automatisch der zuletzt gewählte Lademodus wieder aktiviert.<br>
						Ebenso wird die Ladung bei Überschreiten von 51,8 Hz unterbrochen. <br>
						Dies ist dann der Fall, wenn der Energieversorger Wartungsarbeiten am (Teil-)Netz durchführt und auf einen vorübergehenden Generatorbetrieb umschaltet.<br>
						Die Erhöhung der Frequenz wird durchgeführt, um die PV Anlagen abzuschalten.<br>
						Die Option ist nur aktiv, wenn der Ladepunkt die Frequenz übermittelt. Jede openWB series1/2 tut dies.
					</div>
					<div class="row">
						<b><label for="cpunterbrechunglp1">CP Unterbrechung LP1:</label></b>
						<select name="cpunterbrechunglp1" id="cpunterbrechunglp1">
							<option <?php if($cpunterbrechunglp1old == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($cpunterbrechunglp1old == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>
					<div class="row">
						<b><label for="cpunterbrechunglp2">CP Unterbrechung LP2:</label></b>
						<select name="cpunterbrechunglp2" id="cpunterbrechunglp2">
							<option <?php if($cpunterbrechunglp2old == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($cpunterbrechunglp2old == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>
					<div class="row">
						Diese Option erfordert die verbaute Addon Platine und die korrekte Verdrahtung des CP Signals durch die Addon Platine.<br>
						Sie ist für Fahrzeuge, die nach einer gewissen Zeit einer pausierten Ladung nicht von alleine die Ladung wieder beginnen. Nur aktivieren, wenn es ohne die Option Probleme gibt.
					</div>

					<hr>

					<div class="row">
						<b><label for="rfidakt">RFID Lesung:</label></b>
						<select name="rfidakt" id="rfidakt">
							<option <?php if($rfidaktold == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($rfidaktold == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>

					<div id="rfidausdiv">
					</div>
					<div id="rfidandiv">
						<div class="row">
							Durch scannen von RFID Tags lässt sich die Ladung einem RFID Tag zuweisen. Derzeit unterstützt werden openWB RFID Leser und go-e an LP1.<br>
							Wenn die Option RFID mitgekauft wurde befindet sich dieser unten mittig. Das Scannen wird durch einen Piepton sowie das angehen des Displays (sofern vorhanden) signalisiert.
						</div>
						<div class="row">
							Zuletzt gescannter RFID Tag: <?php echo $lastrfid ?>
						</div>
						<div class="row">
							<b><label for="rfidlp1c1">Ladepunkt 1, Auto 1:</label></b>
							<input type="text" name="rfidlp1c1" id="rfidlp1c1" value="<?php echo $rfidlp1c1old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen.
						</div>
						<div class="row">
							<b><label for="rfidlp1c2">Ladepunkt 1, Auto 2:</label></b>
							<input type="text" name="rfidlp1c2" id="rfidlp1c2" value="<?php echo $rfidlp1c2old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen.
						</div>
						<div class="row">
							<b><label for="rfidlp1c3">Ladepunkt 1, Auto 3:</label></b>
							<input type="text" name="rfidlp1c3" id="rfidlp1c3" value="<?php echo $rfidlp1c3old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen.
						</div>
						<div class="row">
							<b><label for="rfidlp2c1">Ladepunkt 2, Auto 1:</label></b>
							<input type="text" name="rfidlp2c1" id="rfidlp2c1" value="<?php echo $rfidlp2c1old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen.
						</div>
						<div class="row">
							<b><label for="rfidlp2c2">Ladepunkt 2, Auto 2:</label></b>
							<input type="text" name="rfidlp2c2" id="rfidlp2c2" value="<?php echo $rfidlp2c2old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen.
						</div>
						<div class="row">
							<b><label for="rfidlp2c3">Ladepunkt 2, Auto 3:</label></b>
							<input type="text" name="rfidlp2c3" id="rfidlp2c3" value="<?php echo $rfidlp2c3old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen.
						</div>
						<div class="row">
							<b><label for="rfidstop">Ändere Lademodus auf Stop:</label></b><br>
							<input type="text" name="rfidstop" id="rfidstop" value="<?php echo $rfidstopold ?>"><br>
							<input type="text" name="rfidstop2" id="rfidstop2" value="<?php echo $rfidstop2old ?>"><br>
							<input type="text" name="rfidstop3" id="rfidstop3" value="<?php echo $rfidstop3old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
						</div>
						<div class="row">
							<b><label for="rfidstandby">Ändere Lademodus auf Standby:</label></b><br>
							<input type="text" name="rfidstandby" id="rfidstandby" value="<?php echo $rfidstandbyold ?>"><br>
							<input type="text" name="rfidstandby2" id="rfidstandby2" value="<?php echo $rfidstandby2old ?>"><br>
							<input type="text" name="rfidstandby3" id="rfidstandby3" value="<?php echo $rfidstandby3old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
						</div>
						<div class="row">
							<b><label for="rfidsofort">Ändere Lademodus auf Sofort Laden:</label></b><br>
							<input type="text" name="rfidsofort" id="rfidsofort" value="<?php echo $rfidsofortold ?>"><br>
							<input type="text" name="rfidsofort2" id="rfidsofort2" value="<?php echo $rfidsofort2old ?>"><br>
							<input type="text" name="rfidsofort3" id="rfidsofort3" value="<?php echo $rfidsofort3old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
						</div>
						<div class="row">
							<b><label for="rfidminpv">Ändere Lademodus auf Min + PV Laden:</label></b><br>
							<input type="text" name="rfidminpv" id="rfidminpv" value="<?php echo $rfidminpvold ?>"><br>
							<input type="text" name="rfidminpv2" id="rfidminpv2" value="<?php echo $rfidminpv2old ?>"><br>
							<input type="text" name="rfidminpv3" id="rfidminpv3" value="<?php echo $rfidminpv3old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
						</div>
						<div class="row">
							<b><label for="rfidnurpv">Ändere Lademodus auf Nur PV:</label></b><br>
							<input type="text" name="rfidnurpv" id="rfidnurpv" value="<?php echo $rfidnurpvold ?>"><br>
							<input type="text" name="rfidnurpv2" id="rfidnurpv2" value="<?php echo $rfidnurpv2old ?>"><br>
							<input type="text" name="rfidnurpv3" id="rfidnurpv3" value="<?php echo $rfidnurpv3old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
						</div>
						<div class="row">
							<b><label for="rfidlp1start1">Aktiviere Ladepunkt 1:</label></b><br>
						</div>
						<div class="row">
							<input type="text" name="rfidlp1start1" id="rfidlp1start1" value="<?php echo $rfidlp1start1old ?>">
						</div>
						<div class="row">
							<input type="text" name="rfidlp1start2" id="rfidlp1start2" value="<?php echo $rfidlp1start2old ?>">
						</div>
						<div class="row">
							<input type="text" name="rfidlp1start3" id="rfidlp1start3" value="<?php echo $rfidlp1start3old ?>">
						</div>
						<div class="row">					
							<input type="text" name="rfidlp1start4" id="rfidlp1start4" value="<?php echo $rfidlp1start4old ?>">
						</div>
						<div class="row">
							<input type="text" name="rfidlp1start5" id="rfidlp1start5" value="<?php echo $rfidlp1start5old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
						</div>
						<div class="row">
						<b><label for="rfidlp2start1">Aktiviere Ladepunkt 2:</label></b>
						</div>
						<div class="row">
							<input type="text" name="rfidlp2start1" id="rfidlp2start1" value="<?php echo $rfidlp2start1old ?>">
						</div>
						<div class="row">
							<input type="text" name="rfidlp2start2" id="rfidlp2start2" value="<?php echo $rfidlp2start2old ?>">
						</div>
						<div class="row">
							<input type="text" name="rfidlp2start3" id="rfidlp2start3" value="<?php echo $rfidlp2start3old ?>">
						</div>
						<div class="row">					
							<input type="text" name="rfidlp2start4" id="rfidlp2start4" value="<?php echo $rfidlp2start4old ?>">
						</div>
						<div class="row">
							<input type="text" name="rfidlp2start5" id="rfidlp2start5" value="<?php echo $rfidlp2start5old ?>">
						</div>
						<div class="row">
							RFID Tag eintragen. Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
						</div>

					</div>

					<script>
						$(function() {
							if($('#rfidakt').val() == '0') {
								$('#rfidausdiv').show();
								$('#rfidandiv').hide();
							} else {
								$('#rfidausdiv').hide();
								$('#rfidandiv').show();
							}

							$('#rfidakt').change(function(){
								if($('#rfidakt').val() == '0') {
									$('#rfidausdiv').show();
									$('#rfidandiv').hide();
								} else {
									$('#rfidausdiv').hide();
									$('#rfidandiv').show();
								}
							});
						});
					</script>

					<div class="row">
						<div class="col">
							<h4>Benachrichtigungen mit Pushover</h4>
						</div>
					</div>
					<div class="row">
						<div class="col">
							<b><label for="pushbenachrichtigung">Pushover Benachrichtigungen:</label></b>
							<select name="pushbenachrichtigung" id="pushbenachrichtigung">
								<option <?php if($pushbenachrichtigungold == 0) echo "selected" ?> value="0">Deaktiviert</option>
								<option <?php if($pushbenachrichtigungold == 1) echo "selected" ?> value="1">Aktiviert</option>
							</select>
						</div>
					</div>

					<div id="pushbaus">
					</div>
					<div id="pushban">
						<div class="row">
							Zur Nutzung von Pushover muss ein Konto auf Pushover.net bestehen.<br>
							Nach dem Registrieren bei Pushover muss dort im Webinterface eine Applikation erstellt werden.<br>
							Der Token der App, sowie das User Token nachfolgend eintragen.
						</div>
						<div class="row">
							<b><label for="pushoveruser">Pushover User String:</label></b>
							<input type="text" name="pushoveruser" id="pushoveruser" value="<?php echo $pushoveruserold ?>">
						</div>
						<div class="row">
							Hier das User Token von Pushover eintragen
						</div>
						<div class="row">
							<b><label for="pushovertoken">Pushover App Token:</label></b>
							<input type="text" name="pushovertoken" id="pushovertoken" value="<?php echo $pushovertokenold ?>">
						</div>
						<div class="row">
							Hier das Application Token von Pushover eintragen
						</div>
						<div class="row">
							
							<b>Benachrichtigungseinstellungen:</b>
						</div>
						<div class="row">
							<b><label for="pushbstartl">Beim Starten der Ladung:</label></b>
							<select name="pushbstartl" id="pushbstartl">
								<option <?php if($pushbstartlold == 0) echo "selected" ?> value="0">Nein</option>
								<option <?php if($pushbstartlold == 1) echo "selected" ?> value="1">Ja</option>
							</select>
						</div>
						<div class="row">
							<b><label for="pushbstopl">Beim Stoppen der Ladung:</label></b>
							<select name="pushbstopl" id="pushbstopl">
								<option <?php if($pushbstoplold == 0) echo "selected" ?> value="0">Nein</option>
								<option <?php if($pushbstoplold == 1) echo "selected" ?> value="1">Ja</option>
							</select>
						</div>
						<div class="row">
							<b><label for="pushbplug">Beim Einstecken des Fahrzeugs:</label></b>
							<select name="pushbplug" id="pushbplug">
								<option <?php if($pushbplugold == 0) echo "selected" ?> value="0">Nein</option>
								<option <?php if($pushbplugold == 1) echo "selected" ?> value="1">Ja</option>
							</select>
						</div>
						<div class="row">
							<b><label for="pushbsmarthome">Bei Triggern von Smart Home Aktionen:</label></b>
							<select name="pushbsmarthome" id="pushbsmarthome">
								<option <?php if($pushbsmarthomeold == 0) echo "selected" ?> value="0">Nein</option>
								<option <?php if($pushbsmarthomeold == 1) echo "selected" ?> value="1">Ja</option>
							</select>
						</div>
					</div>
					<script>
						$(function() {
							if($('#pushbenachrichtigung').val() == '0') {
								$('#pushbaus').show();
								$('#pushban').hide();
							} else {
								$('#pushbaus').hide();
								$('#pushban').show();
							}
							$('#pushbenachrichtigung').change(function(){
								if($('#pushbenachrichtigung').val() == '0') {
									$('#pushbaus').show();
									$('#pushban').hide();
								} else {
									$('#pushbaus').hide();
									$('#pushban').show();
								}
							});
						});
					</script>
					<div class="row">
						<div class="col">
							<hr>
							<h4>LED Ausgänge</h4>
						</div>
					</div>
					<div class="row">
						<b><label for="ledsakt">LED Ausgänge:</label></b>
						<select name="ledsakt" id="ledsakt">
							<option <?php if($ledsaktold == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($ledsaktold == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>

					<div id="ledsan">
						<div class="row">
							<b><label for="led0sofort">Ladung nicht freigegeben, Sofort Laden Modus:</label></b>
							<select name="led0sofort" id="led0sofort">
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
						<div class="row">
							<b><label for="led0nurpv">Ladung nicht freigegeben, Nur PV Laden Modus:</label></b>
							<select name="led0nurpv" id="led0nurpv">
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
						<div class="row">
							<b><label for="led0minpv">Ladung nicht freigegeben, Min + PV Laden Modus:</label></b>
							<select name="led0minpv" id="led0minpv">
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
						<div class="row">
							<b><label for="led0standby">Ladung nicht freigegeben, Standby Modus:</label></b>
							<select name="led0standby" id="led0standby">
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
						<div class="row">
							<b><label for="led0stop">Ladung nicht freigegeben, Stop Modus:</label></b>
							<select name="led0stop" id="led0stop">
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
						<div class="row">
							<b><label for="ledsofort">Ladung freigegeben, Sofort Laden Modus:</label></b>
							<select name="ledsofort" id="ledsofort">
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
						<div class="row">
							<b><label for="lednurpv">Ladung freigegeben, Nur PV Laden Modus:</label></b>
							<select name="lednurpv" id="lednurpv">
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
						<div class="row">
							<b><label for="ledminpv">Ladung freigegeben, Min + PV Laden Modus:</label></b>
							<select name="ledminpv" id="ledminpv">
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
						<div class="row">
							<b><label for="ledstandby">Ladung freigegeben, Standby Modus:</label></b>
							<select name="ledstandby" id="ledstandby">
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
						<div class="row">
							<b><label for="ledstop">Ladung freigegeben, Stop Modus:</label></b>
							<select name="ledstop" id="ledstop">
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

					<div class="row">
						<div class="col">
							<hr>
							<h4>integriertes Display</h4>
						</div>
					</div>
					<div class="row">
						<b><label for="displayaktiv">Display installiert:</label></b>
						<select name="displayaktiv" id="displayaktiv">
							<option <?php if($displayaktivold == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($displayaktivold == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<div id="displayan">
						<div class="row">
							<b><label for="displaytagesgraph">Tagesgraph anzeigbar (Ja vermindert die Performance):</label></b>
							<select name="displaytagesgraph" id="displaytagesgraph">
								<option <?php if($displaytagesgraphold == 0) echo "selected" ?> value="0">Nein</option>
								<option <?php if($displaytagesgraphold == 1) echo "selected" ?> value="1">Ja</option>
							</select>
						</div>
						<div class="row">
							<b><label for="displaytheme">Theme des Displays:</label></b>
							<select name="displaytheme" id="displaytheme">
								<option <?php if($displaythemeold == 0) echo "selected" ?> value="0">Gauges</option>
								<option <?php if($displaythemeold == 1) echo "selected" ?> value="1">Symbolfluss</option>
								<option <?php if($displaythemeold == 2) echo "selected" ?> value="2">Nur Ladeleistung, keine verstellmöglichkeit</option>
							</select>
						</div>
						<div id="displaygauge">
							<div class="row">
								<b><label for="displayevumax">EVU Skala Min Max:</label></b>
								<input type="text" name="displayevumax" id="displayevumax" value="<?php echo $displayevumaxold ?>">
							</div>
							<div class="row">
								<b><label for="displaypvmax">PV Skala Max:</label></b>
								<input type="text" name="displaypvmax" id="displaypvmax" value="<?php echo $displaypvmaxold ?>">
							</div>
							<div class="row">
								<b><label for="displayspeichermax">Speicher Skala Min Max:</label></b>
								<input type="text" name="displayspeichermax" id="displayspeichermax" value="<?php echo $displayspeichermaxold ?>">
							</div>
							<div class="row">
								<b><label for="displayhausanzeigen">Hausverbrauch anzeigen:</label></b>
								<select name="displayhausanzeigen" id="displayhausanzeigen">
									<option <?php if($displayhausanzeigenold == 0) echo "selected" ?> value="0">Nein</option>
									<option <?php if($displayhausanzeigenold == 1) echo "selected" ?> value="1">Ja</option>
								</select>
							</div>
							<div class="row">
								<b><label for="displayhausmax">Hausverbrauch Skala Max:</label></b>
								<input type="text" name="displayhausmax" id="displayhausmax" value="<?php echo $displayhausmaxold ?>">
							</div>
							<div class="row">
								<b><label for="displaylp1max">Ladepunkt 1 Skala Max:</label></b>
								<input type="text" name="displaylp1max" id="displaylp1max" value="<?php echo $displaylp1maxold ?>">
							</div>
							<div class="row">
								<b><label for="displaylp2max">Ladepunkt 2 Skala Max:</label></b>
								<input type="text" name="displaylp2max" id="displaylp2max" value="<?php echo $displaylp2maxold ?>">
							</div>
						</div>
						<div class="row">
							<b><label for="displaypinaktiv">Pin nötig zum ändern des Lademodus:</label></b>
							<select name="displaypinaktiv" id="displaypinaktiv">
								<option <?php if($displaypinaktivold == 0) echo "selected" ?> value="0">Nein</option>
								<option <?php if($displaypinaktivold == 1) echo "selected" ?> value="1">Ja</option>
							</select>
						</div>
						<div class="row">
							<b><label for="displaypincode">Pin (4-stellig, nur Zahlen erlaubt von 1-9):</label></b>
							<input type="text" name="displaypincode" id="displaypincode" value="<?php echo $displaypincodeold ?>">
						</div>
						<div class="row">
							<b><label for="displaysleep">Display ausschalten nach x Sekunden:</label></b>
							<input type="text" name="displaysleep" id="displaysleep" value="<?php echo $displaysleepold ?>">
						</div>
						<div class="row">
							<b><label for="displayEinBeimAnstecken">Display beim Einstecken des Fahrzeugs einschalten<br/><small>(f&uuml;r oben konfigurierte Dauer):</small></label></b>
							<select name="displayEinBeimAnstecken" id="displayEinBeimAnstecken">
								<option <?php if($displayEinBeimAnsteckenOld == 0) echo "selected" ?> value="0">Nein</option>
								<option <?php if($displayEinBeimAnsteckenOld == 1) echo "selected" ?> value="1">Ja</option>
							</select>
						</div>
					</div>

					<div class="row">
						<div class="col">
							<hr>
							<h3>Optische Einstellungen</h3>
						</div>
					</div>
					<div class="row">
						<b><label for="hausverbrauchstat">Hausverbrauch auf der Hauptseite anzeigen:</label></b>
						<select name="hausverbrauchstat" id="hausverbrauchstat">
							<option <?php if($hausverbrauchstatold == 0) echo "selected" ?> value="0">Aus</option>
							<option <?php if($hausverbrauchstatold == 1) echo "selected" ?> value="1">Ein</option>
						</select>
					</div>
					<div class="row">
						<b><label for="heutegeladen">Heute geladen auf der Hauptseite anzeigen:</label></b>
						<select name="heutegeladen" id="heutegeladen">
							<option <?php if($heutegeladenold == 0) echo "selected" ?> value="0">Aus</option>
							<option <?php if($heutegeladenold == 1) echo "selected" ?> value="1">Ein</option>
						</select>
					</div>

					<div class="row">
						<h4>Graphen</h4>
					</div>

					<div class="row">
						<b><label for="livegraph">Zeitintervall für den Live Graphen der Hauptseite:</label></b>
						<select name="livegraph" id="livegraph">
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


					<!--
					<div class="row">
						<b><label for="chartlegendmain">Legende auf der Hauptseite anzeigen (nur für interaktivem Graph):</label></b>
						<select name="chartlegendmain" id="chartlegendmain">
							<option <?php if($chartlegendmainold == 0) echo "selected" ?> value="0">Aus</option>
							<option <?php if($chartlegendmainold == 1) echo "selected" ?> value="1">Ein</option>
						</select>
					</div>
					-->
					<div id="nonintdaily">
					<!--
						<div class="row">
							<b><label for="logdailywh">Anzeige Daily Graph in Watt oder Wh:</label></b>
							<select name="logdailywh" id="logdailywh">
								<option <?php if($logdailywhold == 0) echo "selected" ?> value="0">Watt</option>
								<option <?php if($logdailywhold == 1) echo "selected" ?> value="1">Wh</option>
							</select>
						</div>
						<div class="row">
							<b><label for="logeinspeisungneg">Einspeisung im Daily Graph positiv oder negativ anzeigen:</label></b>
							<select name="logeinspeisungneg" id="logeinspeisungneg">
								<option <?php if($logeinspeisungnegold == 0) echo "selected" ?>value="0">Positiv</option>
								<option <?php if($logeinspeisungnegold == 1) echo "selected" ?> value="1">Negativ</option>
							</select>
						</div>
					</div>
					<div id="nonintdaily">
						<div class="row">
							<b><label for="graphinteractiveam">Animation im Graph:</label></b>
							<select name="graphinteractiveam" id="graphinteractiveam">
								<option <?php if($graphinteractiveamold == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($graphinteractiveamold == 1) echo "selected" ?> value="1">Ein</option>
							</select>
						</div>
					-->
					</div>
					<script>
						$(function() {
							if($('#grapham').val() == '0') {
								$('#nonintdaily').show();
								$('#intdaily').hide();
							} else {
								$('#nonintdaily').hide();
									$('#intdaily').show();
							}

							$('#grapham').change(function(){
								if($('#grapham').val() == '0') {
									$('#nonintdaily').show();
									$('#intdaily').hide();
								} else {
									$('#nonintdaily').hide();
									$('#intdaily').show();
								}
							});
						});
					</script>

					<button type="submit" class="btn btn-green">Save</button>
				</form>
			</div>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Verschiedenes</small>
			</div>
		</footer>


		<script type="text/javascript">

			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navVerschiedenes').addClass('disabled');
			});

		</script>


	</body>
</html>
