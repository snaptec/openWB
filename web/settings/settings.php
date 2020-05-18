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

				if(strpos($line, "schieflastmaxa=") !== false) {
					list(, $schieflastmaxaold) = explode("=", $line);
				}
				if(strpos($line, "schieflastaktiv=") !== false) {
					list(, $schieflastaktivold) = explode("=", $line);
				}
				if(strpos($line, "mollp1moab=") !== false) {
					list(, $mollp1moabold) = explode("=", $line);
				}
				if(strpos($line, "mollp1mobis=") !== false) {
					list(, $mollp1mobisold) = explode("=", $line);
				}
				if(strpos($line, "mollp1moll=") !== false) {
					list(, $mollp1mollold) = explode("=", $line);
				}
				if(strpos($line, "awattarlocation=") !== false) {
					list(, $awattarlocationold) = explode("=", $line);
				}
				if(strpos($line, "awattaraktiv=") !== false) {
					list(, $awattaraktivold) = explode("=", $line);
				}
				if(strpos($line, "mollp1diab=") !== false) {
					list(, $mollp1diabold) = explode("=", $line);
				}
				if(strpos($line, "mollp1dill=") !== false) {
					list(, $mollp1dillold) = explode("=", $line);
				}
				if(strpos($line, "mollp1dibis=") !== false) {
					list(, $mollp1dibisold) = explode("=", $line);
				}
				if(strpos($line, "mollp1miab=") !== false) {
					list(, $mollp1miabold) = explode("=", $line);
				}
				if(strpos($line, "mollp1mibis=") !== false) {
					list(, $mollp1mibisold) = explode("=", $line);
				}
				if(strpos($line, "mollp1mill=") !== false) {
					list(, $mollp1millold) = explode("=", $line);
				}
				if(strpos($line, "mollp1doab=") !== false) {
					list(, $mollp1doabold) = explode("=", $line);
				}
				if(strpos($line, "mollp1dobis=") !== false) {
					list(, $mollp1dobisold) = explode("=", $line);
				}
				if(strpos($line, "mollp1doll=") !== false) {
					list(, $mollp1dollold) = explode("=", $line);
				}
				if(strpos($line, "mollp1frab=") !== false) {
					list(, $mollp1frabold) = explode("=", $line);
				}
				if(strpos($line, "mollp1frbis=") !== false) {
					list(, $mollp1frbisold) = explode("=", $line);
				}
				if(strpos($line, "mollp1frll=") !== false) {
					list(, $mollp1frllold) = explode("=", $line);
				}
				if(strpos($line, "mollp1saab=") !== false) {
					list(, $mollp1saabold) = explode("=", $line);
				}
				if(strpos($line, "mollp1sabis=") !== false) {
					list(, $mollp1sabisold) = explode("=", $line);
				}
				if(strpos($line, "mollp1sall=") !== false) {
					list(, $mollp1sallold) = explode("=", $line);
				}
				if(strpos($line, "mollp1soab=") !== false) {
					list(, $mollp1soabold) = explode("=", $line);
				}
				if(strpos($line, "mollp1sobis=") !== false) {
					list(, $mollp1sobisold) = explode("=", $line);
				}
				if(strpos($line, "mollp1soll=") !== false) {
					list(, $mollp1sollold) = explode("=", $line);
				}
				if(strpos($line, "sofortll=") !== false) {
					list(, $sofortllold) = explode("=", $line);
				}
				if(strpos($line, "dspeed=") !== false) {
					list(, $dspeedold) = explode("=", $line);
				}
				if(strpos($line, "plz=") !== false) {
					list(, $plzold) = explode("=", $line);
				}
				if(strpos($line, "sdmids1=") !== false) {
					list(, $sdmids1old) = explode("=", $line);
				}
				if(strpos($line, "minimalstromstaerke=") !== false) {
					list(, $minimalstromstaerkeold) = explode("=", $line);
				}
				if(strpos($line, "maximalstromstaerke=") !== false) {
					list(, $maximalstromstaerkeold) = explode("=", $line);
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
				if(strpos($line, "durchslp1=") !== false) {
					list(, $durchslp1old) = explode("=", $line);
				}
				if(strpos($line, "durchslp2=") !== false) {
					list(, $durchslp2old) = explode("=", $line);
				}
				if(strpos($line, "durchslp3=") !== false) {
					list(, $durchslp3old) = explode("=", $line);
				}
				if(strpos($line, "akkuglp1=") !== false) {
					list(, $akkuglp1old) = explode("=", $line);
				}
				if(strpos($line, "akkuglp2=") !== false) {
					list(, $akkuglp2old) = explode("=", $line);
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
				if(strpos($line, "nacht2ll=") !== false) {
					list(, $nacht2llold) = explode("=", $line);
				}
				if(strpos($line, "nacht2lls1=") !== false) {
					list(, $nacht2lls1old) = explode("=", $line);
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
				if(strpos($line, "nachtladen2abuhrs1=") !== false) {
					list(, $nachtladen2abuhrs1old) = explode("=", $line);
				}
				if(strpos($line, "nachtladen2bisuhrs1=") !== false) {
					list(, $nachtladen2bisuhrs1old) = explode("=", $line);
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
				if(strpos($line, "nachtladen2abuhr=") !== false) {
					list(, $nachtladen2abuhrold) = explode("=", $line);
				}
				if(strpos($line, "nachtladen2bisuhr=") !== false) {
					list(, $nachtladen2bisuhrold) = explode("=", $line);
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
				if(strpos($line, "loadsharinglp12=") !== false) {
					list(, $loadsharinglp12old) = explode("=", $line);
				}
				if(strpos($line, "loadsharingalp12=") !== false) {
					list(, $loadsharingalp12old) = explode("=", $line);
				}

				if(strpos($line, "zielladenuhrzeitlp1=") !== false) {
					list(, $zielladenuhrzeitlp1old) = explode("=", $line);
				}
				if(strpos($line, "zielladensoclp1=") !== false) {
					list(, $zielladensoclp1old) = explode("=", $line);
				}
				if(strpos($line, "zielladenalp1=") !== false) {
					list(, $zielladenalp1old) = explode("=", $line);
				}
				if(strpos($line, "zielladenphasenlp1=") !== false) {
					list(, $zielladenphasenlp1old) = explode("=", $line);
				}
				if(strpos($line, "zielladenmaxalp1=") !== false) {
					list(, $zielladenmaxalp1old) = explode("=", $line);
				}
				if(strpos($line, "zielladenaktivlp1=") !== false) {
					list(, $zielladenaktivlp1old) = explode("=", $line);
				}
				if(strpos($line, "offsetpv=") !== false) {
					list(, $offsetpvold) = explode("=", $line);
				}
				if(strpos($line, "nlakt_sofort=") !== false) {
					list(, $nlakt_sofortold) = explode("=", $line, 2);
				}
				if(strpos($line, "nlakt_nurpv=") !== false) {
					list(, $nlakt_nurpvold) = explode("=", $line, 2);
				}
				if(strpos($line, "nlakt_minpv=") !== false) {
					list(, $nlakt_minpvold) = explode("=", $line, 2);
				}
				if(strpos($line, "nlakt_standby=") !== false) {
					list(, $nlakt_standbyold) = explode("=", $line, 2);
				}
				if(strpos($line, "u1p3paktiv=") !== false) {
					list(, $u1p3paktivold) = explode("=", $line, 2);
				}
				if(strpos($line, "u1p3psofort=") !== false) {
					list(, $u1p3psofortold) = explode("=", $line, 2);
				}
				if(strpos($line, "u1p3pstandby=") !== false) {
					list(, $u1p3pstandbyold) = explode("=", $line, 2);
				}
				if(strpos($line, "u1p3pnurpv=") !== false) {
					list(, $u1p3pnurpvold) = explode("=", $line, 2);
				}
				if(strpos($line, "u1p3pminundpv=") !== false) {
					list(, $u1p3pminundpvold) = explode("=", $line, 2);
				}
				if(strpos($line, "u1p3pnl=") !== false) {
					list(, $u1p3pnlold) = explode("=", $line, 2);
				}
				if(strpos($line, "stopchargeafterdisclp1=") !== false) {
					list(, $stopchargeafterdisclp1old) = explode("=", $line, 2);
				}
				if(strpos($line, "stopchargeafterdisclp2=") !== false) {
					list(, $stopchargeafterdisclp2old) = explode("=", $line, 2);
				}
				if(strpos($line, "stopchargeafterdisclp3=") !== false) {
					list(, $stopchargeafterdisclp3old) = explode("=", $line, 2);
				}
				if(strpos($line, "stopchargeafterdisclp4=") !== false) {
					list(, $stopchargeafterdisclp4old) = explode("=", $line, 2);
				}
				if(strpos($line, "stopchargeafterdisclp5=") !== false) {
					list(, $stopchargeafterdisclp5old) = explode("=", $line, 2);
				}
				if(strpos($line, "stopchargeafterdisclp6=") !== false) {
					list(, $stopchargeafterdisclp6old) = explode("=", $line, 2);
				}
				if(strpos($line, "stopchargeafterdisclp7=") !== false) {
					list(, $stopchargeafterdisclp7old) = explode("=", $line, 2);
				}
				if(strpos($line, "stopchargeafterdisclp8=") !== false) {
					list(, $stopchargeafterdisclp8old) = explode("=", $line, 2);
				}
			}
			$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
			$bezug_http_w_urlold = str_replace( "'", "", $bezug_http_w_urlold);
			$bezug_http_ikwh_urlold = str_replace( "'", "", $bezug_http_ikwh_urlold);
			$bezug_http_ekwh_urlold = str_replace( "'", "", $bezug_http_ekwh_urlold);
			$wr_http_w_urlold = str_replace( "'", "", $wr_http_w_urlold);
			$wr_http_kwh_urlold = str_replace( "'", "", $wr_http_kwh_urlold);
			$hsocipold = str_replace( "'", "", $hsocipold);
			$zielladenuhrzeitlp1old = str_replace( "'", "", $zielladenuhrzeitlp1old);
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<div class="col-sm-12">
				<form action="./tools/savemain.php" method="POST">
					<div class="row ">
						<b><label for="awattaraktiv">Awattar aktivieren:</label></b>
						<select name="awattaraktiv" id="awattaraktiv">
							<option <?php if($awattaraktivold == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($awattaraktivold == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<div class="row">
						<p>Ermöglicht Laden nach Strompreis. Hierfür benötigt wird der Awattar Hourly Tarif sowie ein Discovergy Zähler.<br>
						Die Awattar Funktion ist nur im SofortLaden Modus aktiv!</p>
					</div>
					<div class="row ">
						<b><label for="awattarlocation">Land:</label></b>
						<select name="awattarlocation" id="awattarlocation">
							<option <?php if($awattarlocationold == "de\n") echo "selected" ?> value="de">Deutschland</option>
							<option <?php if($awattarlocationold == "at\n") echo "selected" ?> value="at">Österreich</option>
						</select>
					</div>

					<hr>

					<div class="row">
						<b><label for="stopchargeafterdisclp1">Ladepunkt 1 sperren nach Abstecken:</label></b>
						<select name="stopchargeafterdisclp1" id="stopchargeafterdisclp1">
							<option <?php if($stopchargeafterdisclp1old == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($stopchargeafterdisclp1old == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<div class="row" id="lp2aktdiv">
						<b><label for="stopchargeafterdisclp2">Ladepunkt 2 sperren nach Abstecken:</label></b>
						<select name="stopchargeafterdisclp2" id="stopchargeafterdisclp2">
							<option <?php if($stopchargeafterdisclp2old == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($stopchargeafterdisclp2old == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<div class="row" id="lp3aktdiv">
						<b><label for="stopchargeafterdisclp3">Ladepunkt 3 sperren nach Abstecken:</label></b>
						<select name="stopchargeafterdisclp3" id="stopchargeafterdisclp3">
							<option <?php if($stopchargeafterdisclp3old == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($stopchargeafterdisclp3old == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<div class="row" id="lp4aktdiv">
						<b><label for="stopchargeafterdisclp4">Ladepunkt 4 sperren nach Abstecken:</label></b>
						<select name="stopchargeafterdisclp4" id="stopchargeafterdisclp4">
							<option <?php if($stopchargeafterdisclp4old == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($stopchargeafterdisclp4old == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<div class="row" id="lp5aktdiv">
						<b><label for="stopchargeafterdisclp5">Ladepunkt 5 sperren nach Abstecken:</label></b>
						<select name="stopchargeafterdisclp5" id="stopchargeafterdisclp5">
							<option <?php if($stopchargeafterdisclp5old == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($stopchargeafterdisclp5old == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<div class="row" id="lp6aktdiv">
						<b><label for="stopchargeafterdisclp6">Ladepunkt 6 sperren nach Abstecken:</label></b>
						<select name="stopchargeafterdisclp6" id="stopchargeafterdisclp6">
							<option <?php if($stopchargeafterdisclp6old == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($stopchargeafterdisclp6old == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<div class="row" id="lp7aktdiv">
						<b><label for="stopchargeafterdisclp7">Ladepunkt 7 sperren nach Abstecken:</label></b>
						<select name="stopchargeafterdisclp7" id="stopchargeafterdisclp7">
							<option <?php if($stopchargeafterdisclp7old == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($stopchargeafterdisclp7old == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<div class="row" id="lp8aktdiv">
						<b><label for="stopchargeafterdisclp8">Ladepunkt 8 sperren nach Abstecken:</label></b>
						<select name="stopchargeafterdisclp8" id="stopchargeafterdisclp8">
							<option <?php if($stopchargeafterdisclp8old == 0) echo "selected" ?> value="0">Nein</option>
							<option <?php if($stopchargeafterdisclp8old == 1) echo "selected" ?> value="1">Ja</option>
						</select>
					</div>
					<script>
						$(function() {
							var lp2akt = <?php echo $lastmanagementold ?>;
							var lp3akt = <?php echo $lastmanagements2old ?>;
							var lp4akt = <?php echo $lastmanagementlp4old ?>;
							var lp5akt = <?php echo $lastmanagementlp5old ?>;
							var lp6akt = <?php echo $lastmanagementlp6old ?>;
							var lp7akt = <?php echo $lastmanagementlp7old ?>;
							var lp8akt = <?php echo $lastmanagementlp8old ?>;

							if(lp2akt == '0') {
								$('#lp2aktdiv').hide();
								$('#loadsharingdiv').hide();
								$('#nachtladenlp2div').hide();
							} else {
								$('#lp2aktdiv').show();
								$('#loadsharingdiv').show();
								$('#nachtladenlp2div').show();
							}
							if(lp3akt == '0') {
								$('#lp3aktdiv').hide();
							} else {
								$('#lp3aktdiv').show();
							}
							if(lp4akt == '0') {
								$('#lp4aktdiv').hide();
							} else {
								$('#lp4aktdiv').show();
							}
							if(lp5akt == '0') {
								$('#lp5aktdiv').hide();
							} else {
								$('#lp5aktdiv').show();
							}
							if(lp6akt == '0') {
								$('#lp6aktdiv').hide();
							} else {
								$('#lp6aktdiv').show();
							}
							if(lp7akt == '0') {
								$('#lp7aktdiv').hide();
							} else {
								$('#lp7aktdiv').show();
							}
							if(lp8akt == '0') {
								$('#lp8aktdiv').hide();
							} else {
								$('#lp8aktdiv').show();
							}

						});
					</script>
					<div class="row">
						Nachdem der Stecker gezogen wird, wird der entsprechende Ladepunkt gesperrt. Ein manuelles aktivieren des Ladepunktes ist erforderlich. Nach aktivieren bleibt der Ladepunkt solange aktiv bis ein Stecker eingesteckt und wieder abgezogen wird. Ist unabhängig davon ob geladen wird.
					</div>

					<hr>

					<div class="row">
						<h5>
							<b><label for="zielladenaktivlp1">Zielladen Ladepunkt 1:(BETA)</label></b>
							<select name="zielladenaktivlp1" id="zielladenaktivlp1">
								<option <?php if($zielladenaktivlp1old == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($zielladenaktivlp1old == 1) echo "selected" ?> value="1">An</option>
							</select>
						</h5>
					</div>
					<div id="zielladenaktivlp1div">
						<div class="row">
							<div class="col">
								<p><b>Beta Feature</b></p>
								<p>Gewünschten SoC, Ziel Uhrzeit sowie Ladegeschwindigkeit einstellen.<br>
								Sicherstellen das die Akkugröße wie auch die richtige Anzahl der Phasen konfiguriert sind.</p>
							</div>
						</div>

						<div class="row">
							<div class="col">
								<b><label for="zielladensoclp1">Ziel SoC an Ladepunkt 1:</label></b>
								<input type="text" name="zielladensoclp1" id="zielladensoclp1" value="<?php echo $zielladensoclp1old ?>">
								<p>
									Gültige Werte xx, z.B. 85<br>
									Der SoC Wert auf den geladen werden soll.
								</p>
							</div>
						</div>
						<div class="row">
							<div class="col">

								<b><label for="zielladenuhrzeitlp1">Zielladenuhrzeit an Ladepunkt 1:</label></b>
								<input type="text" name="zielladenuhrzeitlp1" id="zielladenuhrzeitlp1" value="<?php echo $zielladenuhrzeitlp1old ?>">
								<p>
									Gültige Werte YYYY-MM-DD HH:MM, z.B. 2018-12-16 06:15<br>
									Ende der gewünschten Ladezeit. Das Datum muss exakt in diesem Format mit Leerzeichen zwischen Monat und Stunde eingegeben werden.
								</p>
							</div>
						</div>
						<div class="row">
							<div class="col">
								<b><label for="zielladenalp1">Stromstärke in A:</label></b>
								<select name="zielladenalp1" id="zielladenalp1">
									<option <?php if($zielladenalp1old == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($zielladenalp1old == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($zielladenalp1old == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($zielladenalp1old == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($zielladenalp1old == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($zielladenalp1old == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($zielladenalp1old == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($zielladenalp1old == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($zielladenalp1old == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($zielladenalp1old == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($zielladenalp1old == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($zielladenalp1old == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($zielladenalp1old == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($zielladenalp1old == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($zielladenalp1old == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($zielladenalp1old == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($zielladenalp1old == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($zielladenalp1old == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($zielladenalp1old == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($zielladenalp1old == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($zielladenalp1old == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($zielladenalp1old == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($zielladenalp1old == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($zielladenalp1old == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($zielladenalp1old == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($zielladenalp1old == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($zielladenalp1old == 32) echo "selected" ?> value="32">32</option>
								</select>
								<p>Ampere mit denen geladen werden soll um den Ziel SoC zu erreichen.</p>
							</div>
						</div>
					</div>

					<hr>

					<div class="row">
						<div class="col">
							<h1>EV Daten</h1>
						</div>
					</div>
					<div id="durchslp1div">
						<div class="row bg-info">
							<div class="col">
								<b>Durchschnittsverbrauch deines Elektroautos in kWh an Ladepunkt 1:</b><br>
								<input type="text" name="durchslp1" id="durchslp1" value="<?php echo $durchslp1old ?>"><br>
								Gültige Werte xx.xx, z.B. 14.5<br>
								Dient zur Berechnung der geladenen Strecke.
							</div>
						</div>
						<div class="row bg-info">
							<div class="col">
								<b>Akkugröße deines Elektroautos in kWh an Ladepunkt 1 (nur für Zielladen relevant):</b><br>
								<input type="text" name="akkuglp1" id="akkuglp1" value="<?php echo $akkuglp1old ?>"><br>
								Gültige Werte xx, z.B. 41<br>
								Dient zur Berechnung der benötigten Ladezeit.
							</div>
						</div>
						<div class="row bg-info">
							<div class="col">
								<b>Anzahl der genutzt Phasen des EV an Ladepunkt 1 (nur für Zielladen relevant):</b><br>
								<select name="zielladenphasenlp1" id="zielladenphasenlp1">
									<option <?php if($zielladenphasenlp1old == 1) echo "selected" ?> value="1">1</option>
									<option <?php if($zielladenphasenlp1old == 2) echo "selected" ?> value="2">2</option>
									<option <?php if($zielladenphasenlp1old == 3) echo "selected" ?> value="3">3</option>
								</select>
							</div>
						</div>
						<div class="row bg-info">
							<div class="col">
								<b>Stromstärke in A mit der maximal geladen werden kann:</b><br>
								<select name="zielladenmaxalp1" id="zielladenmaxalp1">
									<option <?php if($zielladenmaxalp1old == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($zielladenmaxalp1old == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($zielladenmaxalp1old == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($zielladenmaxalp1old == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($zielladenmaxalp1old == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($zielladenmaxalp1old == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($zielladenmaxalp1old == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($zielladenmaxalp1old == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($zielladenmaxalp1old == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($zielladenmaxalp1old == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($zielladenmaxalp1old == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($zielladenmaxalp1old == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($zielladenmaxalp1old == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($zielladenmaxalp1old == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($zielladenmaxalp1old == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($zielladenmaxalp1old == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($zielladenmaxalp1old == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($zielladenmaxalp1old == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($zielladenmaxalp1old == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($zielladenmaxalp1old == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($zielladenmaxalp1old == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($zielladenmaxalp1old == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($zielladenmaxalp1old == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($zielladenmaxalp1old == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($zielladenmaxalp1old == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($zielladenmaxalp1old == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($zielladenmaxalp1old == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								Ampere mit denen geladen werden kann, um den Ziel SoC zu erreichen. Orientiert an der Leistung der Hausinstallation, oder der des zu ladenden Autos.
							</div>
						</div>
					</div>
					<div id="durchslp2div">
						<div class="row bg-info">
							<div class="col">
								<hr>
								<b>Durchschnittsverbrauch deines Elektroautos in kWh an Ladepunkt 2:</b><br>
								<input type="text" name="durchslp2" id="durchslp2" value="<?php echo $durchslp2old ?>"><br>
								Gültige Werte xx.xx, z.B. 14.5<br>
								Dient zur Berechnung der geladenen Strecke.
							</div>
						</div>
						<div class="row bg-info">
							<div class="col">
								<b>Akkugröße deines Elektroautos in kWh an Ladepunkt 2:</b><br>
								<input type="text" name="akkuglp2" id="akkuglp2" value="<?php echo $akkuglp2old ?>"><br>
								Gültige Werte xx, z.B. 41<br>
								Dient zur Berechnung der benötigten Ladezeit.
							</div>
						</div>
					</div>
					<div id="durchslp3div">
						<div class="row bg-info">
							<div class="col">
								<hr>
								<b>Durchschnittsverbrauch deines Elektroautos  in kWh an Ladepunkt 3:</b><br>
								<input type="text" name="durchslp3" id="durchslp3" value="<?php echo $durchslp3old ?>"><br>
								Gültige Werte xx.xx, z.B. 14.5<br>
								Dient zur Berechnung der geladenen Strecke.
							</div>
						</div>
					</div>

					<div class="row">
						<div class="col">
							<h1>Automatische Phasenumschaltung</h1>
						</div>
					</div>
					<div class="row" style="background-color:#33ffa8">
						<div class="col">
							<b>Phasenumschaltung Aktiv:</b><br>
							<select name="u1p3paktiv" id="u1p3paktiv">
								<option <?php if($u1p3paktivold == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($u1p3paktivold == 1) echo "selected" ?> value="1">An</option>
							</select><br>
							Automatisierte Umschaltung von 1- und 3-phasiger Ladung. Nur aktivieren, wenn diese Option in der OpenWB verbaut ist. Je nach gekaufter Hardwareoption gültig für alle Ladepunkte!
						</div>
					</div>
					<div id="u1p3paus">
					</div>
					<div id="u1p3pan">
						<div class="row" style="background-color:#33ffa8">
							<div class="col">
								<b><label for="u1p3psofort">Sofort Laden:</label></b>
								<select name="u1p3psofort" id="u1p3psofort">
									<option <?php if($u1p3psofortold == 1) echo "selected" ?> value="1">einphasig</option>
									<option <?php if($u1p3psofortold == 3) echo "selected" ?> value="3">dreiphasig</option>
								</select>
							</div>
						</div>
						<div class="row" style="background-color:#33ffa8">
							<div class="col">
								<b><label for="u1p3pstandby">Standby:</label></b>
								<select name="u1p3pstandby" id="u1p3pstandby">
									<option <?php if($u1p3pstandbyold == 1) echo "selected" ?> value="1">einphasig</option>
									<option <?php if($u1p3pstandbyold == 3) echo "selected" ?> value="3">dreiphasig</option>
								</select>
							</div>
						</div>
						<div class="row" style="background-color:#33ffa8">
							<div class="col">
								<b><label for="u1p3pminundpv">Min + PV Laden:</label></b>
								<select name="u1p3pminundpv" id="u1p3pminundpv">
									<option <?php if($u1p3pminundpvold == 1) echo "selected" ?> value="1">einphasig</option>
									<option <?php if($u1p3pminundpvold == 3) echo "selected" ?> value="3">dreiphasig</option>
								</select>
							</div>
						</div>
						<div class="row" style="background-color:#33ffa8">
							<div class="col">
								<b><label for="u1p3pnurpv">Nur PV Laden:</label></b>
								<select name="u1p3pnurpv" id="u1p3pnurpv">
									<option <?php if($u1p3pnurpvold == 1) echo "selected" ?> value="1">einphasig</option>
									<option <?php if($u1p3pnurpvold == 3) echo "selected" ?> value="3">dreiphasig</option>
									<option <?php if($u1p3pnurpvold == 4) echo "selected" ?> value="4">Automatikmodus</option>
								</select>
							</div>
						</div>
						<div class="row" style="background-color:#33ffa8">
							<div class="col">
								Im Automatikmodus wird die PV Ladung einphasig begonnen. Ist für durchgehend 10 Minuten die Maximalstromstärke erreicht, wird die Ladung auf dreiphasige Ladung umgestellt. Ist die Ladung nur für ein Intervall unterhalb der Maximalstromstärke, beginnt der Counter für die Umschaltung erneut. Ist die Ladung im dreiphasigen Modus für 8 Minuten bei der Minimalstromstärke, wird wieder auf einphasige Ladung gewechselt.
							</div>
						</div>
						<div class="row" style="background-color:#33ffa8">
							<div class="col">
								<b><label for="u1p3pnl">Nachtladen:</label></b>
								<select name="u1p3pnl" id="u1p3pnl">
									<option <?php if($u1p3pnlold == 1) echo "selected" ?> value="1">einphasig</option>
									<option <?php if($u1p3pnlold == 3) echo "selected" ?> value="3">dreiphasig</option>
								</select>
							</div>
						</div>
						<div class="row" style="background-color:#33ffa8">
							<div class="col">
								<b><label for="schieflastaktiv">Schieflastbeachtung:</label></b>
								<select name="schieflastaktiv" id="schieflastaktiv">
									<option <?php if($schieflastaktivold == 0) echo "selected" ?> value="0">Nein</option>
									<option <?php if($schieflastaktivold == 1) echo "selected" ?> value="1">Ja</option>
								</select>
							</div>
						</div>
						<div class="row" style="background-color:#33ffa8">
							<div class="col">
								<b>Schieflastbegrenzung in A:</b>
								<select name="schieflastmaxa" id="schieflastmaxa">
									<option <?php if($schieflastmaxaold == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($schieflastmaxaold == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($schieflastmaxaold == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($schieflastmaxaold == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($schieflastmaxaold == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($schieflastmaxaold == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($schieflastmaxaold == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($schieflastmaxaold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($schieflastmaxaold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($schieflastmaxaold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($schieflastmaxaold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($schieflastmaxaold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($schieflastmaxaold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($schieflastmaxaold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($schieflastmaxaold == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($schieflastmaxaold == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($schieflastmaxaold == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($schieflastmaxaold == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($schieflastmaxaold == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($schieflastmaxaold == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($schieflastmaxaold == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($schieflastmaxaold == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($schieflastmaxaold == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								Gibt an mit wieviel Ampere maximal geladen wird wenn die automatische Umschaltung aktiv ist und mit einer Phase lädt.
							</div>
						</div>

					</div>

					<div class="row">
						<div class="col">
							<h1>Nachtlademodus</h1>
						</div>
					</div>
					<div class="row" style="background-color:#00ada8">
						<div class="col">
							<input type='hidden' value='0' name='nlakt_sofort'>
							<input id="nlakt_sofort" name="nlakt_sofort" value="1" type="checkbox" <?php if ( $nlakt_sofortold == 1){ echo "checked"; } ?> >
							<label for="nlakt_sofort">Aktiv im Sofort Lademodus</label><br>
							<input type='hidden' value='0' name='nlakt_minpv'>
							<input id="nlakt_minpv" name="nlakt_minpv" value="1" type="checkbox" <?php if ( $nlakt_minpvold == 1){ echo "checked"; } ?> >
							<label for="nlakt_minpv">Aktiv im Min+PV Lademodus</label><br>
							<input type='hidden' value='0' name='nlakt_nurpv'>
							<input id="nlakt_nurpv" name="nlakt_nurpv" value="1" type="checkbox" <?php if ( $nlakt_nurpvold == 1){ echo "checked"; } ?> >
							<label for="nlakt_nurpv">Aktiv im NurPV Lademodus</label><br>
							<input type='hidden' value='0' name='nlakt_standby'>
						 	<input id="nlakt_standby" name="nlakt_standby" value="1" type="checkbox" <?php if ( $nlakt_standbyold == 1){ echo "checked"; } ?> >
							<label for="nlakt_standby">Aktiv im Standby Lademodus</label>
						</div>
					</div>
					<div class="row" style="background-color:#00ada8">
						<div class="col">
							<b>Nachtladen Ladepunkt 1:</b><br>
							<select name="nachtladen" id="nachtladen">
								<option <?php if($nachtladenold == 0) echo "selected" ?> value="0">Aus</option>
								<option <?php if($nachtladenold == 1) echo "selected" ?> value="1">An</option>
							</select><br>
							Definiert, ob Nachts geladen werden soll.
						</div>
					</div>

					<div id="nachtladenaus">
					</div>
					<div id="nachtladenan">
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b>Nachtladestromstärke in A:</b><br>
								<select name="nachtll" id="nachtll">
									<option <?php if($nachtllold == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($nachtllold == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($nachtllold == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($nachtllold == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($nachtllold == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($nachtllold == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($nachtllold == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($nachtllold == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($nachtllold == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($nachtllold == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($nachtllold == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($nachtllold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($nachtllold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($nachtllold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($nachtllold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($nachtllold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($nachtllold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($nachtllold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($nachtllold == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($nachtllold == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($nachtllold == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($nachtllold == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($nachtllold == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($nachtllold == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($nachtllold == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($nachtllold == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($nachtllold == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								Ampere mit der nachts geladen werden soll
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b>Nachtladen Uhrzeit ab:</b><br>
								<select name="nachtladenabuhr" id="nachtladenabuhr">
									<option <?php if($nachtladenabuhrold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($nachtladenabuhrold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($nachtladenabuhrold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($nachtladenabuhrold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($nachtladenabuhrold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($nachtladenabuhrold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($nachtladenabuhrold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($nachtladenabuhrold == 24) echo "selected" ?> value="24">24</option>
								</select><br>
								Ab wann Abends geladen werden soll
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b>Nachtladen Uhrzeit bis:</b><br>
								<select name="nachtladenbisuhr" id="nachtladenbisuhr">
									<option <?php if($nachtladenbisuhrold == 0) echo "selected" ?> value="0">0</option>
									<option <?php if($nachtladenbisuhrold == 1) echo "selected" ?> value="1">1</option>
									<option <?php if($nachtladenbisuhrold == 2) echo "selected" ?> value="2">2</option>
									<option <?php if($nachtladenbisuhrold == 3) echo "selected" ?> value="3">3</option>
									<option <?php if($nachtladenbisuhrold == 4) echo "selected" ?> value="4">4</option>
									<option <?php if($nachtladenbisuhrold == 5) echo "selected" ?> value="5">5</option>
									<option <?php if($nachtladenbisuhrold == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($nachtladenbisuhrold == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($nachtladenbisuhrold == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($nachtladenbisuhrold == 9) echo "selected" ?> value="9">9</option>
								</select><br>
								Bis wann morgens geladen werden soll
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b>Nacht SoC Sonntag bis Donnerstag:</b><br>
								<input type="text" name="nachtsoc" id="nachtsoc" value="<?php echo $nachtsocold ?>"><br>
								Gültiger Wert 1-99. Wenn SoC Modul vorhanden wird Nachts bis xx% SoC geladen in dem angegebenen Zeitfenster.<br>
								Das SoC Fenster is von von Sonntag Abend bis Freitag Morgen aktiv.
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b>Nacht SoC Freitag bis Sonntag:</b><br>
								<input type="text" name="nachtsoc1" id="nachtsoc1" value="<?php echo $nachtsoc1old ?>"><br>
								Gültiger Wert 1-99. Wenn SoC Modul vorhanden wird Nachts bis xx% SoC geladen in dem angegebenen Zeitfenster.<br>
								Das SoC Fenster is von von Freitag Morgen bis Sonntag Abend aktiv.
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b>Die SoC Grenzen gelten nicht für das morgens Laden</b><br>
								<b><label for="mollp1moll">Montag morgens Laden Stromstärke in A:</label></b>
								<select name="mollp1moll" id="mollp1moll">
									<option <?php if($mollp1mollold == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($mollp1mollold == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($mollp1mollold == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($mollp1mollold == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($mollp1mollold == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($mollp1mollold == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($mollp1mollold == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($mollp1mollold == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($mollp1mollold == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($mollp1mollold == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($mollp1mollold == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($mollp1mollold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($mollp1mollold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($mollp1mollold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($mollp1mollold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($mollp1mollold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($mollp1mollold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($mollp1mollold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($mollp1mollold == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($mollp1mollold == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($mollp1mollold == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($mollp1mollold == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($mollp1mollold == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($mollp1mollold == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($mollp1mollold == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($mollp1mollold == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($mollp1mollold == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								<b><label for="mollp1moab">ab:</label></b>
								<select name="mollp1moab" id="mollp1moab">
									<option <?php if($mollp1moabold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1moabold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1moabold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1moabold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1moabold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1moabold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1moabold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1moabold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1moabold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1moabold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1moabold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1moabold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1moabold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1moabold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1moabold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1moabold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1moabold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1moabold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1moabold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1moabold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1moabold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1moabold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1moabold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1moabold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1moabold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1moabold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1moabold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1moabold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1moabold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1moabold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1moabold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1moabold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
								</select>
								<b><label for="mollp1mobis">bis:</label></b>
								<select name="mollp1mobis" id="mollp1mobis">
									<option <?php if($mollp1mobisold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1mobisold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1mobisold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1mobisold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1mobisold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1mobisold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1mobisold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1mobisold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1mobisold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1mobisold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1mobisold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1mobisold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1mobisold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1mobisold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1mobisold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1mobisold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1mobisold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1mobisold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1mobisold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1mobisold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1mobisold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1mobisold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1mobisold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1mobisold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1mobisold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1mobisold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1mobisold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1mobisold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1mobisold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1mobisold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1mobisold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1mobisold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
									<option <?php if($mollp1mobisold == "11:00\n") echo "selected" ?> value="11:00">11:00 Uhr</option>
								</select>
								<hr>
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b><label for="mollp1dill">Dienstag morgens Laden Stromstärke in A:</label></b>
								<select name="mollp1dill" id="mollp1dill">
									<option <?php if($mollp1dillold == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($mollp1dillold == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($mollp1dillold == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($mollp1dillold == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($mollp1dillold == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($mollp1dillold == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($mollp1dillold == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($mollp1dillold == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($mollp1dillold == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($mollp1dillold == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($mollp1dillold == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($mollp1dillold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($mollp1dillold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($mollp1dillold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($mollp1dillold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($mollp1dillold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($mollp1dillold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($mollp1dillold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($mollp1dillold == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($mollp1dillold == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($mollp1dillold == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($mollp1dillold == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($mollp1dillold == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($mollp1dillold == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($mollp1dillold == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($mollp1dillold == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($mollp1dillold == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								<b><label for="mollp1diab">ab:</label></b>
								<select name="mollp1diab" id="mollp1diab">
									<option <?php if($mollp1diabold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1diabold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1diabold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1diabold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1diabold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1diabold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1diabold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1diabold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1diabold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1diabold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1diabold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1diabold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1diabold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1diabold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1diabold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1diabold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1diabold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1diabold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1diabold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1diabold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1diabold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1diabold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1diabold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1diabold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1diabold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1diabold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1diabold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1diabold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1diabold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1diabold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1diabold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1diabold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
								</select>
								<b><label for="mollp1dibis">bis:</label></b>
								<select name="mollp1dibis" id="mollp1dibis">
									<option <?php if($mollp1dibisold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1dibisold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1dibisold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1dibisold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1dibisold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1dibisold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1dibisold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1dibisold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1dibisold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1dibisold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1dibisold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1dibisold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1dibisold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1dibisold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1dibisold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1dibisold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1dibisold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1dibisold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1dibisold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1dibisold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1dibisold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1dibisold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1dibisold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1dibisold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1dibisold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1dibisold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1dibisold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1dibisold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1dibisold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1dibisold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1dibisold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1dibisold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
									<option <?php if($mollp1dibisold == "11:00\n") echo "selected" ?> value="11:00">11:00 Uhr</option>
								</select>
								<hr>
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b><label for="mollp1mill">Mittwoch morgens Laden Stromstärke in A:</label></b>
								<select name="mollp1mill" id="mollp1mill">
									<option <?php if($mollp1millold == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($mollp1millold == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($mollp1millold == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($mollp1millold == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($mollp1millold == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($mollp1millold == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($mollp1millold == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($mollp1millold == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($mollp1millold == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($mollp1millold == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($mollp1millold == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($mollp1millold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($mollp1millold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($mollp1millold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($mollp1millold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($mollp1millold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($mollp1millold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($mollp1millold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($mollp1millold == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($mollp1millold == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($mollp1millold == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($mollp1millold == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($mollp1millold == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($mollp1millold == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($mollp1millold == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($mollp1millold == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($mollp1millold == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								<b><label for="mollp1miab">ab:</label></b>
								<select name="mollp1miab" id="mollp1miab">
									<option <?php if($mollp1miabold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1miabold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1miabold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1miabold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1miabold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1miabold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1miabold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1miabold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1miabold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1miabold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1miabold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1miabold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1miabold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1miabold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1miabold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1miabold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1miabold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1miabold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1miabold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1miabold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1miabold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1miabold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1miabold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1miabold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1miabold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1miabold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1miabold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1miabold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1miabold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1miabold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1miabold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1miabold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
								</select>
								<b><label for="mollp1mibis">bis:</label></b>
								<select name="mollp1mibis" id="mollp1mibis">
									<option <?php if($mollp1mibisold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1mibisold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1mibisold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1mibisold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1mibisold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1mibisold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1mibisold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1mibisold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1mibisold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1mibisold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1mibisold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1mibisold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1mibisold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1mibisold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1mibisold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1mibisold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1mibisold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1mibisold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1mibisold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1mibisold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1mibisold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1mibisold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1mibisold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1mibisold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1mibisold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1mibisold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1mibisold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1mibisold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1mibisold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1mibisold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1mibisold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1mibisold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
									<option <?php if($mollp1mibisold == "11:00\n") echo "selected" ?> value="11:00">11:00 Uhr</option>
								</select>
								<hr>
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b><label for="mollp1doll">Donnerstag morgens Laden Stromstärke in A:</label></b>
								<select name="mollp1doll" id="mollp1doll">
									<option <?php if($mollp1dollold == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($mollp1dollold == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($mollp1dollold == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($mollp1dollold == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($mollp1dollold == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($mollp1dollold == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($mollp1dollold == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($mollp1dollold == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($mollp1dollold == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($mollp1dollold == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($mollp1dollold == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($mollp1dollold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($mollp1dollold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($mollp1dollold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($mollp1dollold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($mollp1dollold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($mollp1dollold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($mollp1dollold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($mollp1dollold == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($mollp1dollold == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($mollp1dollold == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($mollp1dollold == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($mollp1dollold == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($mollp1dollold == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($mollp1dollold == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($mollp1dollold == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($mollp1dollold == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								<b><label for="mollp1doab">ab:</label></b>
								<select name="mollp1doab" id="mollp1doab">
									<option <?php if($mollp1doabold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1doabold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1doabold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1doabold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1doabold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1doabold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1doabold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1doabold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1doabold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1doabold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1doabold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1doabold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1doabold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1doabold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1doabold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1doabold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1doabold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1doabold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1doabold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1doabold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1doabold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1doabold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1doabold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1doabold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1doabold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1doabold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1doabold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1doabold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1doabold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1doabold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1doabold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1doabold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
								</select>
								<b><label for="mollp1dobis">bis:</label></b>
								<select name="mollp1dobis" id="mollp1dobis">
									<option <?php if($mollp1dobisold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1dobisold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1dobisold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1dobisold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1dobisold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1dobisold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1dobisold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1dobisold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1dobisold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1dobisold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1dobisold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1dobisold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1dobisold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1dobisold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1dobisold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1dobisold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1dobisold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1dobisold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1dobisold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1dobisold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1dobisold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1dobisold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1dobisold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1dobisold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1dobisold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1dobisold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1dobisold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1dobisold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1dobisold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1dobisold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1dobisold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1dobisold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
									<option <?php if($mollp1dobisold == "11:00\n") echo "selected" ?> value="11:00">11:00 Uhr</option>
								</select>
								<hr>
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b><label for="mollp1frll">Freitag morgens Laden Stromstärke in A:</label></b>
								<select name="mollp1frll" id="mollp1frll">
									<option <?php if($mollp1frllold == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($mollp1frllold == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($mollp1frllold == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($mollp1frllold == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($mollp1frllold == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($mollp1frllold == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($mollp1frllold == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($mollp1frllold == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($mollp1frllold == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($mollp1frllold == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($mollp1frllold == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($mollp1frllold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($mollp1frllold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($mollp1frllold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($mollp1frllold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($mollp1frllold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($mollp1frllold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($mollp1frllold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($mollp1frllold == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($mollp1frllold == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($mollp1frllold == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($mollp1frllold == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($mollp1frllold == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($mollp1frllold == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($mollp1frllold == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($mollp1frllold == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($mollp1frllold == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								<b><label for="mollp1frab">ab:</label></b>
								<select name="mollp1frab" id="mollp1frab">
									<option <?php if($mollp1frabold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1frabold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1frabold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1frabold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1frabold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1frabold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1frabold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1frabold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1frabold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1frabold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1frabold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1frabold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1frabold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1frabold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1frabold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1frabold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1frabold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1frabold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1frabold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1frabold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1frabold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1frabold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1frabold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1frabold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1frabold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1frabold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1frabold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1frabold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1frabold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1frabold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1frabold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
								</select>
								<b><label for="mollp1frbis">bis:</label></b>
								<select name="mollp1frbis" id="mollp1frbis">
									<option <?php if($mollp1frbisold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1frbisold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1frbisold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1frbisold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1frbisold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1frbisold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1frbisold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1frbisold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1frbisold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1frbisold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1frbisold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1frbisold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1frbisold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1frbisold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1frbisold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1frbisold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1frbisold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1frbisold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1frbisold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1frbisold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1frbisold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1frbisold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1frbisold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1frbisold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1frbisold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1frbisold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1frbisold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1frbisold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1frbisold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1frbisold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1frbisold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1frbisold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
									<option <?php if($mollp1frbisold == "11:00\n") echo "selected" ?> value="11:00">11:00 Uhr</option>
								</select>
								<hr>
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b><label for="mollp1sall">Samstag morgens Laden Stromstärke in A:</label></b>
								<select name="mollp1sall" id="mollp1sall">
									<option <?php if($mollp1sallold == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($mollp1sallold == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($mollp1sallold == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($mollp1sallold == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($mollp1sallold == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($mollp1sallold == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($mollp1sallold == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($mollp1sallold == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($mollp1sallold == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($mollp1sallold == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($mollp1sallold == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($mollp1sallold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($mollp1sallold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($mollp1sallold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($mollp1sallold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($mollp1sallold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($mollp1sallold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($mollp1sallold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($mollp1sallold == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($mollp1sallold == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($mollp1sallold == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($mollp1sallold == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($mollp1sallold == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($mollp1sallold == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($mollp1sallold == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($mollp1sallold == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($mollp1sallold == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								<b><label for="mollp1saab">ab:</label></b>
								<select name="mollp1saab" id="mollp1saab">
									<option <?php if($mollp1saabold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1saabold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1saabold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1saabold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1saabold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1saabold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1saabold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1saabold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1saabold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1saabold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1saabold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1saabold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1saabold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1saabold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1saabold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1saabold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1saabold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1saabold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1saabold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1saabold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1saabold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1saabold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1saabold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1saabold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1saabold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1saabold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1saabold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1saabold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1saabold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1saabold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1saabold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1saabold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
								</select>
								<b><label for="mollp1sabis">bis:</label></b>
								<select name="mollp1sabis" id="mollp1sabis">
									<option <?php if($mollp1sabisold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1sabisold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1sabisold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1sabisold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1sabisold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1sabisold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1sabisold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1sabisold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1sabisold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1sabisold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1sabisold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1sabisold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1sabisold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1sabisold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1sabisold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1sabisold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1sabisold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1sabisold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1sabisold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1sabisold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1sabisold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1sabisold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1sabisold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1sabisold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1sabisold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1sabisold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1sabisold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1sabisold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1sabisold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1sabisold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1sabisold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1sabisold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
									<option <?php if($mollp1sabisold == "11:00\n") echo "selected" ?> value="11:00">11:00 Uhr</option>
								</select>
								<hr>
							</div>
						</div>
						<div class="row" style="background-color:#00ada8">
							<div class="col">
								<b><label for="mollp1soll">Sonntag morgens Laden Stromstärke in A:</label></b>
								<select name="mollp1soll" id="mollp1soll">
									<option <?php if($mollp1sollold == 6) echo "selected" ?> value="6">6</option>
									<option <?php if($mollp1sollold == 7) echo "selected" ?> value="7">7</option>
									<option <?php if($mollp1sollold == 8) echo "selected" ?> value="8">8</option>
									<option <?php if($mollp1sollold == 9) echo "selected" ?> value="9">9</option>
									<option <?php if($mollp1sollold == 10) echo "selected" ?> value="10">10</option>
									<option <?php if($mollp1sollold == 11) echo "selected" ?> value="11">11</option>
									<option <?php if($mollp1sollold == 12) echo "selected" ?> value="12">12</option>
									<option <?php if($mollp1sollold == 13) echo "selected" ?> value="13">13</option>
									<option <?php if($mollp1sollold == 14) echo "selected" ?> value="14">14</option>
									<option <?php if($mollp1sollold == 15) echo "selected" ?> value="15">15</option>
									<option <?php if($mollp1sollold == 16) echo "selected" ?> value="16">16</option>
									<option <?php if($mollp1sollold == 17) echo "selected" ?> value="17">17</option>
									<option <?php if($mollp1sollold == 18) echo "selected" ?> value="18">18</option>
									<option <?php if($mollp1sollold == 19) echo "selected" ?> value="19">19</option>
									<option <?php if($mollp1sollold == 20) echo "selected" ?> value="20">20</option>
									<option <?php if($mollp1sollold == 21) echo "selected" ?> value="21">21</option>
									<option <?php if($mollp1sollold == 22) echo "selected" ?> value="22">22</option>
									<option <?php if($mollp1sollold == 23) echo "selected" ?> value="23">23</option>
									<option <?php if($mollp1sollold == 24) echo "selected" ?> value="24">24</option>
									<option <?php if($mollp1sollold == 25) echo "selected" ?> value="25">25</option>
									<option <?php if($mollp1sollold == 26) echo "selected" ?> value="26">26</option>
									<option <?php if($mollp1sollold == 27) echo "selected" ?> value="27">27</option>
									<option <?php if($mollp1sollold == 28) echo "selected" ?> value="28">28</option>
									<option <?php if($mollp1sollold == 29) echo "selected" ?> value="29">29</option>
									<option <?php if($mollp1sollold == 30) echo "selected" ?> value="30">30</option>
									<option <?php if($mollp1sollold == 31) echo "selected" ?> value="31">31</option>
									<option <?php if($mollp1sollold == 32) echo "selected" ?> value="32">32</option>
								</select><br>
								<b><label for="mollp1soab">ab:</label></b>
								<select name="mollp1soab" id="mollp1soab">
									<option <?php if($mollp1soabold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1soabold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1soabold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1soabold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1soabold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1soabold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1soabold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1soabold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1soabold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1soabold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1soabold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1soabold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1soabold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1soabold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1soabold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1soabold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1soabold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1soabold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1soabold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1soabold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1soabold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1soabold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1soabold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1soabold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1soabold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1soabold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1soabold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1soabold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1soabold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1soabold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1soabold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1soabold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
								</select>
								<b><label for="mollp1sobis">bis:</label></b>
								<select name="mollp1sobis" id="mollp1sobis">
									<option <?php if($mollp1sobisold == "03:00\n") echo "selected" ?> value="03:00">03:00 Uhr</option>
									<option <?php if($mollp1sobisold == "03:15\n") echo "selected" ?> value="03:15">03:15 Uhr</option>
									<option <?php if($mollp1sobisold == "03:30\n") echo "selected" ?> value="03:30">03:30 Uhr</option>
									<option <?php if($mollp1sobisold == "03:45\n") echo "selected" ?> value="03:45">03:45 Uhr</option>
									<option <?php if($mollp1sobisold == "04:00\n") echo "selected" ?> value="04:00">04:00 Uhr</option>
									<option <?php if($mollp1sobisold == "04:15\n") echo "selected" ?> value="04:15">04:15 Uhr</option>
									<option <?php if($mollp1sobisold == "04:30\n") echo "selected" ?> value="04:30">04:30 Uhr</option>
									<option <?php if($mollp1sobisold == "04:45\n") echo "selected" ?> value="04:45">04:45 Uhr</option>
									<option <?php if($mollp1sobisold == "05:00\n") echo "selected" ?> value="05:00">05:00 Uhr</option>
									<option <?php if($mollp1sobisold == "05:15\n") echo "selected" ?> value="05:15">05:15 Uhr</option>
									<option <?php if($mollp1sobisold == "05:30\n") echo "selected" ?> value="05:30">05:30 Uhr</option>
									<option <?php if($mollp1sobisold == "05:45\n") echo "selected" ?> value="05:45">05:45 Uhr</option>
									<option <?php if($mollp1sobisold == "06:00\n") echo "selected" ?> value="06:00">06:00 Uhr</option>
									<option <?php if($mollp1sobisold == "06:15\n") echo "selected" ?> value="06:15">06:15 Uhr</option>
									<option <?php if($mollp1sobisold == "06:30\n") echo "selected" ?> value="06:30">06:30 Uhr</option>
									<option <?php if($mollp1sobisold == "06:45\n") echo "selected" ?> value="06:45">06:45 Uhr</option>
									<option <?php if($mollp1sobisold == "07:00\n") echo "selected" ?> value="07:00">07:00 Uhr</option>
									<option <?php if($mollp1sobisold == "07:15\n") echo "selected" ?> value="07:15">07:15 Uhr</option>
									<option <?php if($mollp1sobisold == "07:30\n") echo "selected" ?> value="07:30">07:30 Uhr</option>
									<option <?php if($mollp1sobisold == "07:45\n") echo "selected" ?> value="07:45">07:45 Uhr</option>
									<option <?php if($mollp1sobisold == "08:00\n") echo "selected" ?> value="08:00">08:00 Uhr</option>
									<option <?php if($mollp1sobisold == "08:15\n") echo "selected" ?> value="08:15">08:15 Uhr</option>
									<option <?php if($mollp1sobisold == "08:30\n") echo "selected" ?> value="08:30">08:30 Uhr</option>
									<option <?php if($mollp1sobisold == "08:45\n") echo "selected" ?> value="08:45">08:45 Uhr</option>
									<option <?php if($mollp1sobisold == "09:00\n") echo "selected" ?> value="09:00">09:00 Uhr</option>
									<option <?php if($mollp1sobisold == "09:15\n") echo "selected" ?> value="09:15">09:15 Uhr</option>
									<option <?php if($mollp1sobisold == "09:30\n") echo "selected" ?> value="09:30">09:30 Uhr</option>
									<option <?php if($mollp1sobisold == "09:45\n") echo "selected" ?> value="09:45">09:45 Uhr</option>
									<option <?php if($mollp1sobisold == "10:00\n") echo "selected" ?> value="10:00">10:00 Uhr</option>
									<option <?php if($mollp1sobisold == "10:15\n") echo "selected" ?> value="10:15">10:15 Uhr</option>
									<option <?php if($mollp1sobisold == "10:30\n") echo "selected" ?> value="10:30">10:30 Uhr</option>
									<option <?php if($mollp1sobisold == "10:45\n") echo "selected" ?> value="10:45">10:45 Uhr</option>
									<option <?php if($mollp1sobisold == "11:00\n") echo "selected" ?> value="11:00">11:00 Uhr</option>
								</select>
							</div>
						</div>
					</div>

					<script>
						$(function() {
							if($('#nachtladen').val() == '0') {
								$('#nachtladenaus').show();
								$('#nachtladenan').hide();
							} else {
								$('#nachtladenaus').hide();
								$('#nachtladenan').show();
							}
							$('#nachtladen').change(function(){
								if($('#nachtladen').val() == '0') {
									$('#nachtladenaus').show();
									$('#nachtladenan').hide();
								} else {
									$('#nachtladenaus').hide();
									$('#nachtladenan').show();
								}
							});
						});

						$(function() {
							if($('#u1p3paktiv').val() == '0') {
								$('#u1p3paus').show();
								$('#u1p3pan').hide();
							} else {
								$('#u1p3paus').hide();
								$('#u1p3pan').show();
							}
							$('#u1p3paktiv').change(function(){
								if($('#u1p3paktiv').val() == '0') {
									$('#u1p3paus').show();
									$('#u1p3pan').hide();
								} else {
									$('#u1p3paus').hide();
									$('#u1p3pan').show();
								}
							});
						});

						$(function() {
							if($('#zielladenaktivlp1').val() == '0') {
								$('#zielladenaktivlp1div').hide();
							} else {
								$('#zielladenaktivlp1div').show();
							}
							$('#zielladenaktivlp1').change(function(){
								if($('#zielladenaktivlp1').val() == '0') {
									$('#zielladenaktivlp1div').hide();
								} else {
									$('#zielladenaktivlp1div').show();
								}
							});
						});
					</script>
					<div id="nachtladenlp2div">
						<div id="nachtls1div">
							<div class="row" style="background-color:#00ada8">
								<div class="col">
									<b>Nachtladen Ladepunkt 2:</b><br>
									<select name="nachtladens1" id="nachtladens1">
										<option <?php if($nachtladens1old == 0) echo "selected" ?> value="0">Aus</option>
										<option <?php if($nachtladens1old == 1) echo "selected" ?> value="1">An</option>
									</select><br>
									Definiert, ob Nachts geladen werden soll. Ist auch bei Lademodus "Stop" aktiv!
								</div>
							</div>
							<div id="nachtladenauss1">
							</div>
							<div id="nachtladenans1">
								<div class="row" style="background-color:#00ada8">
									<div class="col">
										<b><label for="nachtlls1">Nachtladestromstärke in A:</label></b>
										<select name="nachtlls1" id="nachtlls1">
											<option <?php if($nachtlls1old == 6) echo "selected" ?> value="6">6</option>
											<option <?php if($nachtlls1old == 7) echo "selected" ?> value="7">7</option>
											<option <?php if($nachtlls1old == 8) echo "selected" ?> value="8">8</option>
											<option <?php if($nachtlls1old == 9) echo "selected" ?> value="9">9</option>
											<option <?php if($nachtlls1old == 10) echo "selected" ?> value="10">10</option>
											<option <?php if($nachtlls1old == 11) echo "selected" ?> value="11">11</option>
											<option <?php if($nachtlls1old == 12) echo "selected" ?> value="12">12</option>
											<option <?php if($nachtlls1old == 13) echo "selected" ?> value="13">13</option>
											<option <?php if($nachtlls1old == 14) echo "selected" ?> value="14">14</option>
											<option <?php if($nachtlls1old == 15) echo "selected" ?> value="15">15</option>
											<option <?php if($nachtlls1old == 16) echo "selected" ?> value="16">16</option>
											<option <?php if($nachtlls1old == 17) echo "selected" ?> value="17">17</option>
											<option <?php if($nachtlls1old == 18) echo "selected" ?> value="18">18</option>
											<option <?php if($nachtlls1old == 19) echo "selected" ?> value="19">19</option>
											<option <?php if($nachtlls1old == 20) echo "selected" ?> value="20">20</option>
											<option <?php if($nachtlls1old == 21) echo "selected" ?> value="21">21</option>
											<option <?php if($nachtlls1old == 22) echo "selected" ?> value="22">22</option>
											<option <?php if($nachtlls1old == 23) echo "selected" ?> value="23">23</option>
											<option <?php if($nachtlls1old == 24) echo "selected" ?> value="24">24</option>
											<option <?php if($nachtlls1old == 25) echo "selected" ?> value="25">25</option>
											<option <?php if($nachtlls1old == 26) echo "selected" ?> value="26">26</option>
											<option <?php if($nachtlls1old == 27) echo "selected" ?> value="27">27</option>
											<option <?php if($nachtlls1old == 28) echo "selected" ?> value="28">28</option>
											<option <?php if($nachtlls1old == 29) echo "selected" ?> value="29">29</option>
											<option <?php if($nachtlls1old == 30) echo "selected" ?> value="30">30</option>
											<option <?php if($nachtlls1old == 31) echo "selected" ?> value="31">31</option>
											<option <?php if($nachtlls1old == 32) echo "selected" ?> value="32">32</option>
										</select><br>
										Ampere mit der nachts geladen werden soll
									</div>
								</div>
								<div class="row" style="background-color:#00ada8">
									<div class="col">
										<b><label for="nachtladenabuhrs1">Nachtladen Uhrzeit ab:</label></b>
										<select name="nachtladenabuhrs1" id="nachtladenabuhrs1">
											<option <?php if($nachtladenabuhrs1old == 17) echo "selected" ?> value="17">17</option>
											<option <?php if($nachtladenabuhrs1old == 18) echo "selected" ?> value="18">18</option>
											<option <?php if($nachtladenabuhrs1old == 19) echo "selected" ?> value="19">19</option>
											<option <?php if($nachtladenabuhrs1old == 20) echo "selected" ?> value="20">20</option>
											<option <?php if($nachtladenabuhrs1old == 21) echo "selected" ?> value="21">21</option>
											<option <?php if($nachtladenabuhrs1old == 22) echo "selected" ?> value="22">22</option>
											<option <?php if($nachtladenabuhrs1old == 23) echo "selected" ?> value="23">23</option>
											<option <?php if($nachtladenabuhrs1old == 24) echo "selected" ?> value="24">24</option>
										</select><br>
										Ab wann Abends geladen werden soll
									</div>
								</div>
								<div class="row" style="background-color:#00ada8">
									<div class="col">
										<b><label for="nachtladenbisuhrs1">Nachtladen Uhrzeit bis:</label></b>
										<select name="nachtladenbisuhrs1" id="nachtladenbisuhrs1">
											<option <?php if($nachtladenbisuhrs1old == 0) echo "selected" ?> value="0">0</option>
											<option <?php if($nachtladenbisuhrs1old == 1) echo "selected" ?> value="1">1</option>
											<option <?php if($nachtladenbisuhrs1old == 2) echo "selected" ?> value="2">2</option>
											<option <?php if($nachtladenbisuhrs1old == 3) echo "selected" ?> value="3">3</option>
											<option <?php if($nachtladenbisuhrs1old == 4) echo "selected" ?> value="4">4</option>
											<option <?php if($nachtladenbisuhrs1old == 5) echo "selected" ?> value="5">5</option>
											<option <?php if($nachtladenbisuhrs1old == 6) echo "selected" ?> value="6">6</option>
											<option <?php if($nachtladenbisuhrs1old == 7) echo "selected" ?> value="7">7</option>
											<option <?php if($nachtladenbisuhrs1old == 8) echo "selected" ?> value="8">8</option>
											<option <?php if($nachtladenbisuhrs1old == 9) echo "selected" ?> value="9">9</option>
										</select><br>
										Bis wann morgens geladen werden soll
									</div>
								</div>
								<div class="row" style="background-color:#00ada8">
									<div class="col">
										<b>Nacht SoC Sonntag bis Donnerstag:</b><br>
										<input type="text" name="nachtsocs1" id="nachtsocs1" value="<?php echo $nachtsocs1old ?>"><br>
										Gültiger Wert 1-99. Wenn SoC Modul vorhanden wird Nachts bis xx% SoC geladen in dem angegebenen Zeitfenster.
									</div>
								</div>
								<div class="row" style="background-color:#00ada8">
									<div class="col">
										<b>Nacht SoC Freitag bis Sonntag:</b><br>
										<input type="text" name="nachtsoc1s1" id="nachtsoc1s1" value="<?php echo $nachtsoc1s1old ?>"><br>
										Gültiger Wert 1-99. Wenn SoC Modul Ladepunkt 2 vorhanden wird Nachts bis xx% SoC geladen in dem angegebenen Zeitfenster.
									</div>
								</div>
								<div class="row" style="background-color:#00ada8">
									<div class="col">
										<b><label for="nacht2lls1">Morgens Laden Stromstärke in A:</label></b>
										<select name="nacht2lls1" id="nacht2lls1">
											<option <?php if($nacht2lls1old == 6) echo "selected" ?> value="6">6</option>
											<option <?php if($nacht2lls1old == 7) echo "selected" ?> value="7">7</option>
											<option <?php if($nacht2lls1old == 8) echo "selected" ?> value="8">8</option>
											<option <?php if($nacht2lls1old == 9) echo "selected" ?> value="9">9</option>
											<option <?php if($nacht2lls1old == 10) echo "selected" ?> value="10">10</option>
											<option <?php if($nacht2lls1old == 11) echo "selected" ?> value="11">11</option>
											<option <?php if($nacht2lls1old == 12) echo "selected" ?> value="12">12</option>
											<option <?php if($nacht2lls1old == 13) echo "selected" ?> value="13">13</option>
											<option <?php if($nacht2lls1old == 14) echo "selected" ?> value="14">14</option>
											<option <?php if($nacht2lls1old == 15) echo "selected" ?> value="15">15</option>
											<option <?php if($nacht2lls1old == 16) echo "selected" ?> value="16">16</option>
											<option <?php if($nacht2lls1old == 17) echo "selected" ?> value="17">17</option>
											<option <?php if($nacht2lls1old == 18) echo "selected" ?> value="18">18</option>
											<option <?php if($nacht2lls1old == 19) echo "selected" ?> value="19">19</option>
											<option <?php if($nacht2lls1old == 20) echo "selected" ?> value="20">20</option>
											<option <?php if($nacht2lls1old == 21) echo "selected" ?> value="21">21</option>
											<option <?php if($nacht2lls1old == 22) echo "selected" ?> value="22">22</option>
											<option <?php if($nacht2lls1old == 23) echo "selected" ?> value="23">23</option>
											<option <?php if($nacht2lls1old == 24) echo "selected" ?> value="24">24</option>
											<option <?php if($nacht2lls1old == 25) echo "selected" ?> value="25">25</option>
											<option <?php if($nacht2lls1old == 26) echo "selected" ?> value="26">26</option>
											<option <?php if($nacht2lls1old == 27) echo "selected" ?> value="27">27</option>
											<option <?php if($nacht2lls1old == 28) echo "selected" ?> value="28">28</option>
											<option <?php if($nacht2lls1old == 29) echo "selected" ?> value="29">29</option>
											<option <?php if($nacht2lls1old == 30) echo "selected" ?> value="30">30</option>
											<option <?php if($nacht2lls1old == 31) echo "selected" ?> value="31">31</option>
											<option <?php if($nacht2lls1old == 32) echo "selected" ?> value="32">32</option>
										</select><br>
										Ampere mit der im zweiten Intervall geladen werden soll
									</div>
								</div>
								<div class="row" style="background-color:#00ada8">
									<div class="col">
										<b><label for="nachtladen2abuhrs1">Morgens Laden Uhrzeit ab:</label></b>
										<select name="nachtladen2abuhrs1" id="nachtladen2abuhrs1">
											<option <?php if($nachtladen2abuhrs1old == 3) echo "selected" ?> value="3">3</option>
											<option <?php if($nachtladen2abuhrs1old == 4) echo "selected" ?> value="4">4</option>
											<option <?php if($nachtladen2abuhrs1old == 5) echo "selected" ?> value="5">5</option>
											<option <?php if($nachtladen2abuhrs1old == 6) echo "selected" ?> value="6">6</option>
											<option <?php if($nachtladen2abuhrs1old == 7) echo "selected" ?> value="7">7</option>
											<option <?php if($nachtladen2abuhrs1old == 8) echo "selected" ?> value="8">8</option>
											<option <?php if($nachtladen2abuhrs1old == 9) echo "selected" ?> value="9">9</option>
										</select><br>
										Ab wann im zweiten Intervall geladen werden soll
									</div>
								</div>
								<div class="row" style="background-color:#00ada8">
									<div class="col">
										<b><label for="nachtladen2bisuhrs1">Morgens Laden Uhrzeit bis:</label></b>
										<select name="nachtladen2bisuhrs1" id="nachtladen2bisuhrs1">
											<option <?php if($nachtladen2bisuhrs1old == 4) echo "selected" ?> value="4">4</option>
											<option <?php if($nachtladen2bisuhrs1old == 5) echo "selected" ?> value="5">5</option>
											<option <?php if($nachtladen2bisuhrs1old == 6) echo "selected" ?> value="6">6</option>
											<option <?php if($nachtladen2bisuhrs1old == 7) echo "selected" ?> value="7">7</option>
											<option <?php if($nachtladen2bisuhrs1old == 8) echo "selected" ?> value="8">8</option>
											<option <?php if($nachtladen2bisuhrs1old == 9) echo "selected" ?> value="9">9</option>
											<option <?php if($nachtladen2bisuhrs1old == 10) echo "selected" ?> value="10">10</option>
										</select><br>
										Bis wann morgens im zweiten Intervall geladen werden soll
									</div>
								</div>
							</div>
							<script>
								$(function() {
									if($('#nachtladens1').val() == '0') {
										$('#nachtladenauss1').show();
										$('#nachtladenans1').hide();
									} else {
										$('#nachtladenauss1').hide();
										$('#nachtladenans1').show();
									}
									$('#nachtladens1').change(function(){
										if($('#nachtladens1').val() == '0') {
											$('#nachtladenauss1').show();
											$('#nachtladenans1').hide();
										} else {
											$('#nachtladenauss1').hide();
											$('#nachtladenans1').show();
										}
									});
								});
							</script>
						</div>
					</div>
					<div class="row">
						<div class="col">
							<h1>EVU basiertes Lastmanagement</h1>
						</div>
					</div>
					<div class="row" style="background-color:#ffffcc">
						<div class="col">
							<b><label for="lastmaxap1">Lastmanagement Max Ampere Phase 1:</label></b>
							<input type="text" name="lastmaxap1" id="lastmaxap1" value="<?php echo $lastmaxap1old ?>">
						</div>
					</div>
					<div class="row" style="background-color:#ffffcc">
						<div class="col">
							<b><label for="lastmaxap2">Lastmanagement Max Ampere Phase 2:</label></b>
							<input type="text" name="lastmaxap2" id="lastmaxap2" value="<?php echo $lastmaxap2old ?>">
						</div>
					</div>
					<div class="row" style="background-color:#ffffcc">
						<div class="col">
							<b><label for="lastmaxap3">Lastmanagement Max Ampere Phase 3:</label></b>
							<input type="text" name="lastmaxap3" id="lastmaxap3" value="<?php echo $lastmaxap3old ?>">
						</div>
					</div>
					<div class="row" style="background-color:#ffffcc">
						<div class="col">
							Gültige Werte 7-64. Definiert die maximal erlaubte Stromstärke der einzelnen Phasen des Hausanschlusses im Sofort Laden Modus, sofern das EVU Modul die Werte je Phase zur Verfügung stellt.
						</div>
					</div>
					<div class="row" style="background-color:#ffffcc">
						<div class="col">
							<b><label for="lastmmaxw">Lastmanagement maximaler Bezug:</label></b>
							<input type="text" name="lastmmaxw" id="lastmmaxw" value="<?php echo $lastmmaxwold ?>"><br>
						</div>
					</div>
					<div class="row" style="background-color:#ffffcc">
						<div class="col">
							Gültige Werte 2000-200000. Definiert die maximal erlaubten bezogenen Watt des Hausanschlusses im Sofort Laden Modus, sofern die Bezugsleistung bekannt ist.<br><br>
						</div>
					</div>

					<div id="loadsharingdiv">
						<div class="row"><hr>
							<div class="col">
								<h1>Loadsharing LP1/2</h1>
							</div>
						</div>
						<div class="row" style="background-color:#e6ccb3">
							<div class="col">
								<b><label for="loadsharinglp12">Loadsharing LP 1 / LP 2:</label></b>
								<select name="loadsharinglp12" id="loadsharinglp12">
									<option <?php if($loadsharinglp12old == 0) echo "selected" ?> value="0">Deaktiviert</option>
									<option <?php if($loadsharinglp12old == 1) echo "selected" ?> value="1">Aktiviert</option>
								</select><br>
							</div>
						</div>
						<div class="row" style="background-color:#e6ccb3">
							<div class="col">
								<b><label for="loadsharingalp12">Loadsharing Ampere LP 1 / LP 2:</label></b>
								<select name="loadsharingalp12" id="loadsharingalp12">
									<option <?php if($loadsharingalp12old == 16) echo "selected" ?> value="16">16 Ampere</option>
									<option <?php if($loadsharingalp12old == 32) echo "selected" ?> value="32">32 Ampere</option>
								</select><br>
							</div>
						</div>
						<div class="row" style="background-color:#e6ccb3">
							<div class="col">
								Wenn Ladepunkt 1 und Ladepunkt 2 sich eine Zuleitung teilen, diese Option aktivieren. Bei der OpenWB Duo muss diese Option aktiviert werden!<br>
								Sie stellt in jedem Lademodus sicher, dass nicht mehr als 16 bzw. 32A je Phase in der Summe von LP 1 und LP 2 genutzt werden.<br>
								Der richtige Anschluss ist zu gewährleisten.<br>

								Ladepunkt 1:
								<p style="text-indent :2em;" >Phase 1 Zuleitung = Phase 1 Ladepunkt 1</p>
								<p style="text-indent :2em;" >Phase 2 Zuleitung = Phase 2 Ladepunkt 1</p>
								<p style="text-indent :2em;" >Phase 3 Zuleitung = Phase 3 Ladepunkt 1</p>
								Ladepunkt 2:
								<p style="text-indent :2em;" >Phase 1 Zuleitung = Phase 2 Ladepunkt 2</p>
								<p style="text-indent :2em;" >Phase 2 Zuleitung = Phase 3 Ladepunkt 2</p>
								<p style="text-indent :2em;" >Phase 3 Zuleitung = Phase 1 Ladepunkt 2</p>
								Durch das Drehen der Phasen ist sichergestellt, dass 2 einphasige Autos mit voller Geschwindigkeit laden können.
							</div>
						</div>
					</div>
					<div class="row justify-content-center">
						<button type="submit" class="btn btn-green">Save</button>
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
			</div>
		</div>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Einstellungen/Allgemein</small>
			</div>
		</footer>


		<script type="text/javascript">

			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navAllgemein').addClass('disabled');
			});

		</script>

	</body>
</html>
