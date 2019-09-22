<!DOCTYPE html>
<html lang="en">

<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB</title>
	<meta name="description" content="Control your charge" />
	<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
	<meta name="author" content="Kevin Wieland" />
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
	<!-- Normalize -->
	<link rel="stylesheet" type="text/css" href="css/normalize.css">
	<!-- Bootstrap -->
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<!-- Owl -->
	<link rel="stylesheet" type="text/css" href="css/owl.css">
	<!-- Animate.css -->
	<link rel="stylesheet" type="text/css" href="css/animate.css">
	<!-- Font Awesome, all styles -->
  <link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
	<!-- Elegant Icons -->
	<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
	<!-- Main style -->
	<link rel="stylesheet" type="text/css" href="css/cardio.css">

</head>
<body>
<?php


$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	if(strpos($line, "sofortll=") !== false) {
		list(, $sofortllold) = explode("=", $line);
	}
	if(strpos($line, "settingspwakt=") !== false) {
		list(, $settingspwaktold) = explode("=", $line);
	}
	if(strpos($line, "settingspw=") !== false) {
		list(, $settingspwold) = explode("=", $line);
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



<div class="container">
<div class="row"><br>
 <ul class="nav nav-tabs">

    <li><a data-toggle="tab" href="./index.php">Zurück</a></li>
    <li class="active"><a href="./settings.php">Einstellungen</a></li>
    <li><a href="./pvconfig.php">PV Ladeeinstellungen</a></li>
    <li><a href="./smarthome.php">Smart Home</a></li>
    <li><a href="./modulconfig.php">Modulkonfiguration</a></li>
	<li><a href="./setTheme.php">Theme</a></li>
	<li><a href="./misc.php">Misc</a></li>
  </ul><br><br>
 </div>
<form action="./tools/savemain.php" method="POST">

<div class="col-xs-1">
</div>
<div class="col-xs-10">
	<div class="row ">

		<b><label for="plz">Postleitzahl:</label></b>
		<input type="text" name="plz" id="plz" value="<?php echo $plzold ?>"><br>
	</div>
	<div class="row">
	Gültige Werte z.B. 36124 <br> Dient zur Ermittlung des GSI Index. Weitere Infos unter: <a href="https://www.corrently.de/hintergrund/gruenstromindex">Hier</a><br>Derzeit als optische Einbindung unter Status zu finden. Künftig Laden nach GSI möglich.<br><br>
	</div><hr>
<div class="row">
	<b><h5><label for="Zielladen">Zielladen Ladepunkt 1:(BETA)</label></b>
	<select type="text" name="zielladenaktivlp1" id="zielladenaktivlp1">
		<option <?php if($zielladenaktivlp1old == 0) echo selected ?> value="0">Aus</option>
		<option <?php if($zielladenaktivlp1old == 1) echo selected ?> value="1">An</option>
	</select></h5>
</div>

<div id="zielladenaktivlp1div">
	<div class="row">
		<b>Beta Feature</b><br>
		Vorgehensweise zum testen: Lademodus auf Stop stellen. Gewünschten SoC, Ziel Uhrzeit sowie Ladegeschwindigkeit einstellen.<br>
		Sicherstellen das die Akkugröße wie auch die richtige Anzahl der Phasen konfiguriert sind.<br>
	</div>
	<div class="row">
		<b><label for="zielladensoclp1">Ziel SoC an Ladepunkt 1:</label></b>
		<input type="text" name="zielladensoclp1" id="zielladensoclp1" value="<?php echo $zielladensoclp1old ?>"><br>
	</div>
	<div class="row">
	Gültige Werte xx, z.B. 85 <br> Der SoC Wert auf den geladen werden soll.<br><br>
	</div>
	<div class="row">

		<b><label for="zielladenuhrzeitlp1">Zielladenuhrzeit an Ladepunkt 1:</label></b>
		<input type="text" name="zielladenuhrzeitlp1" id="zielladenuhrzeitlp1" value="<?php echo $zielladenuhrzeitlp1old ?>"><br>
	</div>
	<div class="row">
	Gültige Werte YYYY-MM-DD HH:MM, z.B. 2018-12-16 06:15 <br> Ende der gewünschten Ladezeit. Das Datum muss exakt in diesem Format mit Leerzeichen zwischen Monat und Stunde eingegeben werden.<br><br>
	</div>
	<div class="row">
		<b><label for="zielladenalp1">Stromstärke in A:</label></b>
		<select type="text" name="zielladenalp1" id="zielladenalp1">
			<option <?php if($zielladenalp1old == 6) echo selected ?> value="6">6</option>
			<option <?php if($zielladenalp1old == 7) echo selected ?> value="7">7</option>
			<option <?php if($zielladenalp1old == 8) echo selected ?> value="8">8</option>
			<option <?php if($zielladenalp1old == 9) echo selected ?> value="9">9</option>
			<option <?php if($zielladenalp1old == 10) echo selected ?> value="10">10</option>
			<option <?php if($zielladenalp1old == 11) echo selected ?> value="11">11</option>
			<option <?php if($zielladenalp1old == 12) echo selected ?> value="12">12</option>
			<option <?php if($zielladenalp1old == 13) echo selected ?> value="13">13</option>
			<option <?php if($zielladenalp1old == 14) echo selected ?> value="14">14</option>
			<option <?php if($zielladenalp1old == 15) echo selected ?> value="15">15</option>
			<option <?php if($zielladenalp1old == 16) echo selected ?> value="16">16</option>
			<option <?php if($zielladenalp1old == 17) echo selected ?> value="17">17</option>
			<option <?php if($zielladenalp1old == 18) echo selected ?> value="18">18</option>
			<option <?php if($zielladenalp1old == 19) echo selected ?> value="19">19</option>
			<option <?php if($zielladenalp1old == 20) echo selected ?> value="20">20</option>
			<option <?php if($zielladenalp1old == 21) echo selected ?> value="21">21</option>
			<option <?php if($zielladenalp1old == 22) echo selected ?> value="22">22</option>
			<option <?php if($zielladenalp1old == 23) echo selected ?> value="23">23</option>
			<option <?php if($zielladenalp1old == 24) echo selected ?> value="24">24</option>
			<option <?php if($zielladenalp1old == 25) echo selected ?> value="25">25</option>
			<option <?php if($zielladenalp1old == 26) echo selected ?> value="26">26</option>
			<option <?php if($zielladenalp1old == 27) echo selected ?> value="27">27</option>
			<option <?php if($zielladenalp1old == 28) echo selected ?> value="28">28</option>
			<option <?php if($zielladenalp1old == 29) echo selected ?> value="29">29</option>
			<option <?php if($zielladenalp1old == 30) echo selected ?> value="30">30</option>
			<option <?php if($zielladenalp1old == 31) echo selected ?> value="31">31</option>
			<option <?php if($zielladenalp1old == 32) echo selected ?> value="32">32</option>
		</select><br>
	</div>
	<div class="row">
	Ampere mit denen geladen werden soll um den Ziel SoC zu erreichen.<br>
	</div>

</div>

<div class="row"><hr>
	<h3>EV Daten</h3>
</div>
<div id="durchslp1">
	<div class="row bg-info">

		<b><label for="durchslp1">Durchschnittsverbrauch deines Elektroautos in kWh an Ladepunkt 1:</label></b>
		<input type="text" name="durchslp1" id="durchslp1" value="<?php echo $durchslp1old ?>"><br>
	</div>
	<div class="row bg-info">
	Gültige Werte xx.xx, z.B. 14.5 <br> Dient zur Berechnung der geladenen Strecke.<br><br>
	</div>
	<div class="row bg-info">

		<b><label for="akkuglp1">Akkugröße deines Elektroautos in kWh an Ladepunkt 1 (nur für Zielladen relevant):</label></b>
		<input type="text" name="akkuglp1" id="akkuglp1" value="<?php echo $akkuglp1old ?>"><br>
	</div>
	<div class="row bg-info">
	Gültige Werte xx, z.B. 41 <br> Dient zur Berechnung der benötigten Ladezeit.<br><br>
	</div>
	<div class="row bg-info">
		<b><label for="zielladenphasenlp1">Anzahl der genutzt Phasen des EV an Ladepunkt 1 (nur für Zielladen relevant):</label></b>
		<select type="text" name="zielladenphasenlp1" id="zielladenphasenlp1">
			<option <?php if($zielladenphasenlp1old == 1) echo selected ?> value="1">1</option>
			<option <?php if($zielladenphasenlp1old == 2) echo selected ?> value="2">2</option>
			<option <?php if($zielladenphasenlp1old == 3) echo selected ?> value="3">3</option>
		</select>
	</div>
	<div class="row bg-info">
		<b><label for="zielladenmaxalp1">Stromstärke in A mit der maximal geladen werden kann:</label></b>
		<select type="text" name="zielladenmaxalp1" id="zielladenmaxalp1">
			<option <?php if($zielladenmaxalp1old == 6) echo selected ?> value="6">6</option>
			<option <?php if($zielladenmaxalp1old == 7) echo selected ?> value="7">7</option>
			<option <?php if($zielladenmaxalp1old == 8) echo selected ?> value="8">8</option>
			<option <?php if($zielladenmaxalp1old == 9) echo selected ?> value="9">9</option>
			<option <?php if($zielladenmaxalp1old == 10) echo selected ?> value="10">10</option>
			<option <?php if($zielladenmaxalp1old == 11) echo selected ?> value="11">11</option>
			<option <?php if($zielladenmaxalp1old == 12) echo selected ?> value="12">12</option>
			<option <?php if($zielladenmaxalp1old == 13) echo selected ?> value="13">13</option>
			<option <?php if($zielladenmaxalp1old == 14) echo selected ?> value="14">14</option>
			<option <?php if($zielladenmaxalp1old == 15) echo selected ?> value="15">15</option>
			<option <?php if($zielladenmaxalp1old == 16) echo selected ?> value="16">16</option>
			<option <?php if($zielladenmaxalp1old == 17) echo selected ?> value="17">17</option>
			<option <?php if($zielladenmaxalp1old == 18) echo selected ?> value="18">18</option>
			<option <?php if($zielladenmaxalp1old == 19) echo selected ?> value="19">19</option>
			<option <?php if($zielladenmaxalp1old == 20) echo selected ?> value="20">20</option>
			<option <?php if($zielladenmaxalp1old == 21) echo selected ?> value="21">21</option>
			<option <?php if($zielladenmaxalp1old == 22) echo selected ?> value="22">22</option>
			<option <?php if($zielladenmaxalp1old == 23) echo selected ?> value="23">23</option>
			<option <?php if($zielladenmaxalp1old == 24) echo selected ?> value="24">24</option>
			<option <?php if($zielladenmaxalp1old == 25) echo selected ?> value="25">25</option>
			<option <?php if($zielladenmaxalp1old == 26) echo selected ?> value="26">26</option>
			<option <?php if($zielladenmaxalp1old == 27) echo selected ?> value="27">27</option>
			<option <?php if($zielladenmaxalp1old == 28) echo selected ?> value="28">28</option>
			<option <?php if($zielladenmaxalp1old == 29) echo selected ?> value="29">29</option>
			<option <?php if($zielladenmaxalp1old == 30) echo selected ?> value="30">30</option>
			<option <?php if($zielladenmaxalp1old == 31) echo selected ?> value="31">31</option>
			<option <?php if($zielladenmaxalp1old == 32) echo selected ?> value="32">32</option>
		</select><br>
	</div>
	<div class="row bg-info">
	Ampere mit denen geladen werden kann, um den Ziel SoC zu erreichen. Orientiert an der Leistung der Hausinstallation, oder der des zu ladenden Autos.<br>
	</div>
</div>
<div id="durchslp2">
	<div class="row bg-info"><hr>
		<b><label for="durchslp2">Durchschnittsverbrauch deines Elektroautos in kWh an Ladepunkt 2:</label></b>
		<input type="text" name="durchslp2" id="durchslp2" value="<?php echo $durchslp2old ?>"><br>
	</div>
	<div class="row bg-info">
	Gültige Werte xx.xx, z.B. 14.5 <br> Dient zur Berechnung der geladenen Strecke.<br><br>
	</div>
	<div class="row bg-info">
		<hr>
		<b><label for="akkuglp2">Akkugröße deines Elektroautos in kWh an Ladepunkt 2:</label></b>
		<input type="text" name="akkuglp2" id="akkuglp2" value="<?php echo $akkuglp2old ?>"><br>
	</div>
	<div class="row bg-info">
	Gültige Werte xx, z.B. 41 <br> Dient zur Berechnung der benötigten Ladezeit.<br><br>
	</div>

</div>
<div id="durchslp3">
	<div class="row bg-info">
		<b><label for="durchslp3">Durchschnittsverbrauch deines Elektroautos  in kWh an Ladepunkt 3:</label></b>
		<input type="text" name="durchslp3" id="durchslp3" value="<?php echo $durchslp3old ?>"><br>
	</div>
	<div class="row bg-info">
	Gültige Werte xx.xx, z.B. 14.5 <br> Dient zur Berechnung der geladenen Strecke.<br><br>
	</div>
</div>



<div class="row"><hr>
	<h3>Sofort Laden</h3>
</div>
<div class="row" style="background-color:#febebe">
	<b><label for="minimalstromstaerke">Minimalstromstärke in A:</label></b>
	<select type="text" name="minimalstromstaerke" id="minimalstromstaerke">
		<option <?php if($minimalstromstaerkeold == 6) echo selected ?> value="6">6</option>
		<option <?php if($minimalstromstaerkeold == 7) echo selected ?> value="7">7</option>
		<option <?php if($minimalstromstaerkeold == 8) echo selected ?> value="8">8</option>
		<option <?php if($minimalstromstaerkeold == 9) echo selected ?> value="9">9</option>
		<option <?php if($minimalstromstaerkeold == 10) echo selected ?> value="10">10</option>
		<option <?php if($minimalstromstaerkeold == 11) echo selected ?> value="11">11</option>
		<option <?php if($minimalstromstaerkeold == 12) echo selected ?> value="12">12</option>
		<option <?php if($minimalstromstaerkeold == 13) echo selected ?> value="13">13</option>
		<option <?php if($minimalstromstaerkeold == 14) echo selected ?> value="14">14</option>

	</select><br>
</div>
<div class="row" style="background-color:#febebe">
	Gibt an mit wieviel Ampere je Phase mindestens geladen wird, gilt auch für das Nachtladen. <br><br>
</div>
<div class="row" style="background-color:#febebe">
	<b><label for="maximalstromstaerke">Maximalstromstärke in A:</label></b>
	<select type="text" name="maximalstromstaerke" id="maximalstromstaerke">
		<option <?php if($maximalstromstaerkeold == 11) echo selected ?> value="11">11</option>
		<option <?php if($maximalstromstaerkeold == 12) echo selected ?> value="12">12</option>
		<option <?php if($maximalstromstaerkeold == 13) echo selected ?> value="13">13</option>
		<option <?php if($maximalstromstaerkeold == 14) echo selected ?> value="14">14</option>
		<option <?php if($maximalstromstaerkeold == 15) echo selected ?> value="15">15</option>
		<option <?php if($maximalstromstaerkeold == 16) echo selected ?> value="16">16</option>
		<option <?php if($maximalstromstaerkeold == 17) echo selected ?> value="17">17</option>
		<option <?php if($maximalstromstaerkeold == 18) echo selected ?> value="18">18</option>
		<option <?php if($maximalstromstaerkeold == 19) echo selected ?> value="19">19</option>
		<option <?php if($maximalstromstaerkeold == 20) echo selected ?> value="20">20</option>
		<option <?php if($maximalstromstaerkeold == 21) echo selected ?> value="21">21</option>
		<option <?php if($maximalstromstaerkeold == 22) echo selected ?> value="22">22</option>
		<option <?php if($maximalstromstaerkeold == 23) echo selected ?> value="23">23</option>
		<option <?php if($maximalstromstaerkeold == 24) echo selected ?> value="24">24</option>
		<option <?php if($maximalstromstaerkeold == 25) echo selected ?> value="25">25</option>
		<option <?php if($maximalstromstaerkeold == 26) echo selected ?> value="26">26</option>
		<option <?php if($maximalstromstaerkeold == 27) echo selected ?> value="27">27</option>
		<option <?php if($maximalstromstaerkeold == 28) echo selected ?> value="28">28</option>
		<option <?php if($maximalstromstaerkeold == 29) echo selected ?> value="29">29</option>
		<option <?php if($maximalstromstaerkeold == 30) echo selected ?> value="30">30</option>
		<option <?php if($maximalstromstaerkeold == 31) echo selected ?> value="31">31</option>
		<option <?php if($maximalstromstaerkeold == 32) echo selected ?> value="32">32</option>
	</select><br>

</div>
<div class="row" style="background-color:#febebe">
	Gibt an mit wieviel Ampere Maximal geladen wird.<br><br>
</div>

<div class="row"><hr>
	<h3>Automatische Phasenumschaltung</h3>
</div>
<div class="row" style="background-color:#33ffa8">
	<b><h5><label for="u1p3paktiv">Phasenumschaltung Aktiv:</label></b>
	<select type="text" name="u1p3paktiv" id="u1p3paktiv">
		<option <?php if($u1p3paktivold == 0) echo selected ?> value="0">Aus</option>
		<option <?php if($u1p3paktivold == 1) echo selected ?> value="1">An</option>
	</select></h5>
</div>
<div class="row" style="background-color:#33ffa8">
	Automatisierte Umschaltung von 1- und 3-phasiger Ladung. Nur aktivieren, wenn diese Option in der OpenWB verbaut ist. Ist nur an Ladepunkt 1 aktiv!<br><br>
</div>
<div id="u1p3paus">
	<br>
</div>
<div id="u1p3pan">
<div class="row" style="background-color:#33ffa8">
	<b><label for="u1p3psofort">Sofort Laden:</label></b>
	<select type="text" name="u1p3psofort" id="u1p3psofort">
		<option <?php if($u1p3psofortold == 1) echo selected ?> value="1">einphasig</option>
		<option <?php if($u1p3psofortold == 3) echo selected ?> value="3">dreiphasig</option>
	</select>
</div>
<div class="row" style="background-color:#33ffa8">
	<b><label for="u1p3pstandby">Standby:</label></b>
	<select type="text" name="u1p3pstandby" id="u1p3pstandby">
		<option <?php if($u1p3pstandbyold == 1) echo selected ?> value="1">einphasig</option>
		<option <?php if($u1p3pstandbyold == 3) echo selected ?> value="3">dreiphasig</option>
	</select>
</div>
<div class="row" style="background-color:#33ffa8">
	<b><label for="u1p3pminundpv">Min + PV Laden:</label></b>
	<select type="text" name="u1p3pminundpv" id="u1p3pminundpv">
		<option <?php if($u1p3pminundpvold == 1) echo selected ?> value="1">einphasig</option>
		<option <?php if($u1p3pminundpvold == 3) echo selected ?> value="3">dreiphasig</option>
	</select>
</div>
<div class="row" style="background-color:#33ffa8">
	<b><label for="u1p3pnurpv">Nur PV Laden:</label></b>
	<select type="text" name="u1p3pnurpv" id="u1p3pnurpv">
		<option <?php if($u1p3pnurpvold == 1) echo selected ?> value="1">einphasig</option>
		<option <?php if($u1p3pnurpvold == 3) echo selected ?> value="3">dreiphasig</option>
		<option <?php if($u1p3pnurpvold == 3) echo selected ?> value="4">Automatikmodus</option>
	</select>
</div>
<div class="row" style="background-color:#33ffa8">
Im Automatikmodus wird die PV Ladung einphasig begonnen. Ist für durchgehend 10 Minuten die Maximalstromstärke erreicht wird die Ladung auf dreiphasige Ladung umgestellt. Ist die Ladung nur für ein Intervall unterhalb der Maximalstromstärke beginnt der Counter für die Umschaltung erneut. Ist die Ladung im dreiphasigen Modus für 8 Minuten bei der Minimalstromstärke wird wieder auf einphasige Ladung gewechselt.<br><br>
</div>

<div class="row" style="background-color:#33ffa8">
	<b><label for="u1p3pnl">Nachtladen:</label></b>
	<select type="text" name="u1p3pnl" id="u1p3pnl">
		<option <?php if($u1p3pnlold == 1) echo selected ?> value="1">einphasig</option>
		<option <?php if($u1p3pnlold == 3) echo selected ?> value="3">dreiphasig</option>
	</select>
</div>



</div>



<div class="row"><hr>
	<h3>Nachtlademodus</h3>
</div>
<div class="row" style="background-color:#00ada8">
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
	<label for="nlakt_standby">Aktiv im Standby Lademodus</label><br>
</div><br>
<div class="row" style="background-color:#00ada8">
	<b><h5><label for="nachtladen">Nachtladen Ladepunkt 1:</label></b>
	<select type="text" name="nachtladen" id="nachtladen">
		<option <?php if($nachtladenold == 0) echo selected ?> value="0">Aus</option>
		<option <?php if($nachtladenold == 1) echo selected ?> value="1">An</option>
	</select></h5>
</div>
<div class="row" style="background-color:#00ada8">
	Definiert, ob Nachts geladen werden soll.<br><br>
</div>
<div id="nachtladenaus">
	<br>
</div>
<div id="nachtladenan">
	<div class="row" style="background-color:#00ada8">
       		<b><label for="nachtll">Nachtladestromstärke in A:</label></b>
        	<select type="text" name="nachtll" id="nachtll">
         	        <option <?php if($nachtllold == 6) echo selected ?> value="6">6</option>
	       	        <option <?php if($nachtllold == 7) echo selected ?> value="7">7</option>
        	        <option <?php if($nachtllold == 8) echo selected ?> value="8">8</option>
        	        <option <?php if($nachtllold == 9) echo selected ?> value="9">9</option>
        	        <option <?php if($nachtllold == 10) echo selected ?> value="10">10</option>
			<option <?php if($nachtllold == 11) echo selected ?> value="11">11</option>
        	        <option <?php if($nachtllold == 12) echo selected ?> value="12">12</option>
        	        <option <?php if($nachtllold == 13) echo selected ?> value="13">13</option>
        	        <option <?php if($nachtllold == 14) echo selected ?> value="14">14</option>
        	        <option <?php if($nachtllold == 15) echo selected ?> value="15">15</option>
        	        <option <?php if($nachtllold == 16) echo selected ?> value="16">16</option>
        	        <option <?php if($nachtllold == 17) echo selected ?> value="17">17</option>
        	        <option <?php if($nachtllold == 18) echo selected ?> value="18">18</option>
        		<option <?php if($nachtllold == 19) echo selected ?> value="19">19</option>
               		<option <?php if($nachtllold == 20) echo selected ?> value="20">20</option>
                	<option <?php if($nachtllold == 21) echo selected ?> value="21">21</option>
                	<option <?php if($nachtllold == 22) echo selected ?> value="22">22</option>
                	<option <?php if($nachtllold == 23) echo selected ?> value="23">23</option>
                	<option <?php if($nachtllold == 24) echo selected ?> value="24">24</option>
                	<option <?php if($nachtllold == 25) echo selected ?> value="25">25</option>
                	<option <?php if($nachtllold == 26) echo selected ?> value="26">26</option>
                	<option <?php if($nachtllold == 27) echo selected ?> value="27">27</option>
                	<option <?php if($nachtllold == 28) echo selected ?> value="28">28</option>
                	<option <?php if($nachtllold == 29) echo selected ?> value="29">29</option>
                	<option <?php if($nachtllold == 30) echo selected ?> value="30">30</option>
                	<option <?php if($nachtllold == 31) echo selected ?> value="31">31</option>
                	<option <?php if($nachtllold == 32) echo selected ?> value="32">32</option>
       		</select><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Ampere mit der nachts geladen werden soll<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtladenabuhr">Nachtladen Uhrzeit ab:</label></b>
	       	<select type="text" name="nachtladenabuhr" id="nachtladenabuhr">
 			<option <?php if($nachtladenabuhrold == 17) echo selected ?> value="17">17</option>
 			<option <?php if($nachtladenabuhrold == 18) echo selected ?> value="18">18</option>
 			<option <?php if($nachtladenabuhrold == 19) echo selected ?> value="19">19</option>
 			<option <?php if($nachtladenabuhrold == 20) echo selected ?> value="20">20</option>
 			<option <?php if($nachtladenabuhrold == 21) echo selected ?> value="21">21</option>
 			<option <?php if($nachtladenabuhrold == 22) echo selected ?> value="22">22</option>
			<option <?php if($nachtladenabuhrold == 23) echo selected ?> value="23">23</option>
			<option <?php if($nachtladenabuhrold == 24) echo selected ?> value="24">24</option>
		</select><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Ab wann Abends geladen werden soll<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtladenbisuhr">Nachtladen Uhrzeit bis:</label></b>
	       	<select type="text" name="nachtladenbisuhr" id="nachtladenbisuhr">
			<option <?php if($nachtladenbisuhrold == 0) echo selected ?> value="0">0</option>
			<option <?php if($nachtladenbisuhrold == 1) echo selected ?> value="1">1</option>
  			<option <?php if($nachtladenbisuhrold == 2) echo selected ?> value="2">2</option>
	 		<option <?php if($nachtladenbisuhrold == 3) echo selected ?> value="3">3</option>
 			<option <?php if($nachtladenbisuhrold == 4) echo selected ?> value="4">4</option>
 			<option <?php if($nachtladenbisuhrold == 5) echo selected ?> value="5">5</option>
 			<option <?php if($nachtladenbisuhrold == 6) echo selected ?> value="6">6</option>
 			<option <?php if($nachtladenbisuhrold == 7) echo selected ?> value="7">7</option>
 			<option <?php if($nachtladenbisuhrold == 8) echo selected ?> value="8">8</option>
			<option <?php if($nachtladenbisuhrold == 9) echo selected ?> value="9">9</option>
		</select><br>

	</div>
	<div class="row" style="background-color:#00ada8">
		Bis wann morgens geladen werden soll<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtsoc">Nacht SOC Sonntag bis Donnerstag:</label></b>
		<input type="text" name="nachtsoc" id="nachtsoc" value="<?php echo $nachtsocold ?>"><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Gültiger Wert 1-99. Wenn SOC Modul vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br>Das SoC Fenster is von von Sonntag Abend bis Freitag Morgen aktiv.<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtsoc1">Nacht SOC Freitag bis Sonntag:</label></b>
		<input type="text" name="nachtsoc1" id="nachtsoc1" value="<?php echo $nachtsoc1old ?>"><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Gültiger Wert 1-99. Wenn SOC Modul vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br>Das SoC Fenster is von von Freitag Morgen bis Sonntag Abend aktiv<br><br>
	</div><br>
	<div class="row" style="background-color:#00ada8">
       		<b><label for="nacht2ll">Morgens Laden Stromstärke in A:</label></b>
        	<select type="text" name="nacht2ll" id="nacht2ll">
         	        <option <?php if($nacht2llold == 6) echo selected ?> value="6">6</option>
	       	        <option <?php if($nacht2llold == 7) echo selected ?> value="7">7</option>
        	        <option <?php if($nacht2llold == 8) echo selected ?> value="8">8</option>
        	        <option <?php if($nacht2llold == 9) echo selected ?> value="9">9</option>
        	        <option <?php if($nacht2llold == 10) echo selected ?> value="10">10</option>
			<option <?php if($nacht2llold == 11) echo selected ?> value="11">11</option>
        	        <option <?php if($nacht2llold == 12) echo selected ?> value="12">12</option>
        	        <option <?php if($nacht2llold == 13) echo selected ?> value="13">13</option>
        	        <option <?php if($nacht2llold == 14) echo selected ?> value="14">14</option>
        	        <option <?php if($nacht2llold == 15) echo selected ?> value="15">15</option>
        	        <option <?php if($nacht2llold == 16) echo selected ?> value="16">16</option>
        	        <option <?php if($nacht2llold == 17) echo selected ?> value="17">17</option>
        	        <option <?php if($nacht2llold == 18) echo selected ?> value="18">18</option>
        		<option <?php if($nacht2llold == 19) echo selected ?> value="19">19</option>
               		<option <?php if($nacht2llold == 20) echo selected ?> value="20">20</option>
                	<option <?php if($nacht2llold == 21) echo selected ?> value="21">21</option>
                	<option <?php if($nacht2llold == 22) echo selected ?> value="22">22</option>
                	<option <?php if($nacht2llold == 23) echo selected ?> value="23">23</option>
                	<option <?php if($nacht2llold == 24) echo selected ?> value="24">24</option>
                	<option <?php if($nacht2llold == 25) echo selected ?> value="25">25</option>
                	<option <?php if($nacht2llold == 26) echo selected ?> value="26">26</option>
                	<option <?php if($nacht2llold == 27) echo selected ?> value="27">27</option>
                	<option <?php if($nacht2llold == 28) echo selected ?> value="28">28</option>
                	<option <?php if($nacht2llold == 29) echo selected ?> value="29">29</option>
                	<option <?php if($nacht2llold == 30) echo selected ?> value="30">30</option>
                	<option <?php if($nacht2llold == 31) echo selected ?> value="31">31</option>
                	<option <?php if($nacht2llold == 32) echo selected ?> value="32">32</option>
       		</select><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Ampere mit der im zweiten Intervall geladen werden soll<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtladen2abuhr">Morgens Laden Uhrzeit ab:</label></b>
	       	<select type="text" name="nachtladen2abuhr" id="nachtladen2abuhr">
 			<option <?php if($nachtladen2abuhrold == 3) echo selected ?> value="3">3</option>
 			<option <?php if($nachtladen2abuhrold == 4) echo selected ?> value="4">4</option>
 			<option <?php if($nachtladen2abuhrold == 5) echo selected ?> value="5">5</option>
 			<option <?php if($nachtladen2abuhrold == 6) echo selected ?> value="6">6</option>
 			<option <?php if($nachtladen2abuhrold == 7) echo selected ?> value="7">7</option>
 			<option <?php if($nachtladen2abuhrold == 8) echo selected ?> value="8">8</option>
			<option <?php if($nachtladen2abuhrold == 9) echo selected ?> value="9">9</option>
		</select><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Ab wann im zweiten Intervall geladen werden soll<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtladen2bisuhr">Morgens Laden Uhrzeit bis:</label></b>
	       	<select type="text" name="nachtladen2bisuhr" id="nachtladen2bisuhr">

 			<option <?php if($nachtladen2bisuhrold == 4) echo selected ?> value="4">4</option>
 			<option <?php if($nachtladen2bisuhrold == 5) echo selected ?> value="5">5</option>
 			<option <?php if($nachtladen2bisuhrold == 6) echo selected ?> value="6">6</option>
 			<option <?php if($nachtladen2bisuhrold == 7) echo selected ?> value="7">7</option>
 			<option <?php if($nachtladen2bisuhrold == 8) echo selected ?> value="8">8</option>
			<option <?php if($nachtladen2bisuhrold == 9) echo selected ?> value="9">9</option>
			<option <?php if($nachtladen2bisuhrold == 10) echo selected ?> value="10">10</option>
		</select><br>

	</div>
	<div class="row" style="background-color:#00ada8">
		Bis wann morgens im zweiten Intervall geladen werden soll<br><br>
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
</script>
<script>
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
</script>

<script>
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
<div id="nachtls1div"><br><br><br>
<div class="row" style="background-color:#00ada8">
	<b><h5><label for="nachtladens1">Nachtladen Ladepunkt 2:</label></b>
	<select type="text" name="nachtladens1" id="nachtladens1">
		<option <?php if($nachtladens1old == 0) echo selected ?> value="0">Aus</option>
		<option <?php if($nachtladens1old == 1) echo selected ?> value="1">An</option>
	</select></h5>
</div>
<div class="row" style="background-color:#00ada8">
	Definiert, ob Nachts geladen werden soll. Ist auch bei Lademodus "Stop" aktiv!<br><br>
</div>
<div id="nachtladenauss1">
	<br>
</div>
<div id="nachtladenans1">
	<div class="row" style="background-color:#00ada8">
       		<b><label for="nachtlls1">Nachtladestromstärke in A:</label></b>
        	<select type="text" name="nachtlls1" id="nachtlls1">
         	        <option <?php if($nachtlls1old == 6) echo selected ?> value="6">6</option>
	       	        <option <?php if($nachtlls1old == 7) echo selected ?> value="7">7</option>
        	        <option <?php if($nachtlls1old == 8) echo selected ?> value="8">8</option>
        	        <option <?php if($nachtlls1old == 9) echo selected ?> value="9">9</option>
        	        <option <?php if($nachtlls1old == 10) echo selected ?> value="10">10</option>
			<option <?php if($nachtlls1old == 11) echo selected ?> value="11">11</option>
        	        <option <?php if($nachtlls1old == 12) echo selected ?> value="12">12</option>
        	        <option <?php if($nachtlls1old == 13) echo selected ?> value="13">13</option>
        	        <option <?php if($nachtlls1old == 14) echo selected ?> value="14">14</option>
        	        <option <?php if($nachtlls1old == 15) echo selected ?> value="15">15</option>
        	        <option <?php if($nachtlls1old == 16) echo selected ?> value="16">16</option>
        	        <option <?php if($nachtlls1old == 17) echo selected ?> value="17">17</option>
        	        <option <?php if($nachtlls1old == 18) echo selected ?> value="18">18</option>
        		<option <?php if($nachtlls1old == 19) echo selected ?> value="19">19</option>
               		<option <?php if($nachtlls1old == 20) echo selected ?> value="20">20</option>
                	<option <?php if($nachtlls1old == 21) echo selected ?> value="21">21</option>
                	<option <?php if($nachtlls1old == 22) echo selected ?> value="22">22</option>
                	<option <?php if($nachtlls1old == 23) echo selected ?> value="23">23</option>
                	<option <?php if($nachtlls1old == 24) echo selected ?> value="24">24</option>
                	<option <?php if($nachtlls1old == 25) echo selected ?> value="25">25</option>
                	<option <?php if($nachtlls1old == 26) echo selected ?> value="26">26</option>
                	<option <?php if($nachtlls1old == 27) echo selected ?> value="27">27</option>
                	<option <?php if($nachtlls1old == 28) echo selected ?> value="28">28</option>
                	<option <?php if($nachtlls1old == 29) echo selected ?> value="29">29</option>
                	<option <?php if($nachtlls1old == 30) echo selected ?> value="30">30</option>
                	<option <?php if($nachtlls1old == 31) echo selected ?> value="31">31</option>
                	<option <?php if($nachtlls1old == 32) echo selected ?> value="32">32</option>
       		</select><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Ampere mit der nachts geladen werden soll<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtladenabuhrs1">Nachtladen Uhrzeit ab:</label></b>
	       	<select type="text" name="nachtladenabuhrs1" id="nachtladenabuhrs1">
 			<option <?php if($nachtladenabuhrs1old == 17) echo selected ?> value="17">17</option>
 			<option <?php if($nachtladenabuhrs1old == 18) echo selected ?> value="18">18</option>
 			<option <?php if($nachtladenabuhrs1old == 19) echo selected ?> value="19">19</option>
 			<option <?php if($nachtladenabuhrs1old == 20) echo selected ?> value="20">20</option>
 			<option <?php if($nachtladenabuhrs1old == 21) echo selected ?> value="21">21</option>
 			<option <?php if($nachtladenabuhrs1old == 22) echo selected ?> value="22">22</option>
			<option <?php if($nachtladenabuhrs1old == 23) echo selected ?> value="23">23</option>
			<option <?php if($nachtladenabuhrs1old == 24) echo selected ?> value="24">24</option>
		</select><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Ab wann Abends geladen werden soll<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtladenbisuhrs1">Nachtladen Uhrzeit bis:</label></b>
	       	<select type="text" name="nachtladenbisuhrs1" id="nachtladenbisuhrs1">
 			<option <?php if($nachtladenbisuhrs1old == 0) echo selected ?> value="0">0</option>
			<option <?php if($nachtladenbisuhrs1old == 1) echo selected ?> value="1">1</option>
  			<option <?php if($nachtladenbisuhrs1old == 2) echo selected ?> value="2">2</option>
	 		<option <?php if($nachtladenbisuhrs1old == 3) echo selected ?> value="3">3</option>
 			<option <?php if($nachtladenbisuhrs1old == 4) echo selected ?> value="4">4</option>
 			<option <?php if($nachtladenbisuhrs1old == 5) echo selected ?> value="5">5</option>
 			<option <?php if($nachtladenbisuhrs1old == 6) echo selected ?> value="6">6</option>
 			<option <?php if($nachtladenbisuhrs1old == 7) echo selected ?> value="7">7</option>
 			<option <?php if($nachtladenbisuhrs1old == 8) echo selected ?> value="8">8</option>
			<option <?php if($nachtladenbisuhrs1old == 9) echo selected ?> value="9">9</option>
		</select><br>

	</div>
	<div class="row" style="background-color:#00ada8">
		Bis wann morgens geladen werden soll an Ladepunkt 2<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtsocs1">Nacht SOC Sonntag bis Donnerstag:</label></b>
		<input type="text" name="nachtsocs1" id="nachtsocs1" value="<?php echo $nachtsocs1old ?>"><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Gültiger Wert 1-99. Wenn SOC Modul vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtsoc1s1">Nacht SOC Freitag bis Sonntag:</label></b>
		<input type="text" name="nachtsoc1s1" id="nachtsoc1s1" value="<?php echo $nachtsoc1s1old ?>"><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Gültiger Wert 1-99. Wenn SOC Modul Ladepunkt 2 vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br><br>
	</div><br>
	<div class="row" style="background-color:#00ada8">
       		<b><label for="nacht2lls1">Morgens Laden Stromstärke in A:</label></b>
        	<select type="text" name="nacht2lls1" id="nacht2lls1">
         	        <option <?php if($nacht2lls1old == 6) echo selected ?> value="6">6</option>
	       	        <option <?php if($nacht2lls1old == 7) echo selected ?> value="7">7</option>
        	        <option <?php if($nacht2lls1old == 8) echo selected ?> value="8">8</option>
        	        <option <?php if($nacht2lls1old == 9) echo selected ?> value="9">9</option>
        	        <option <?php if($nacht2lls1old == 10) echo selected ?> value="10">10</option>
			<option <?php if($nacht2lls1old == 11) echo selected ?> value="11">11</option>
        	        <option <?php if($nacht2lls1old == 12) echo selected ?> value="12">12</option>
        	        <option <?php if($nacht2lls1old == 13) echo selected ?> value="13">13</option>
        	        <option <?php if($nacht2lls1old == 14) echo selected ?> value="14">14</option>
        	        <option <?php if($nacht2lls1old == 15) echo selected ?> value="15">15</option>
        	        <option <?php if($nacht2lls1old == 16) echo selected ?> value="16">16</option>
        	        <option <?php if($nacht2lls1old == 17) echo selected ?> value="17">17</option>
        	        <option <?php if($nacht2lls1old == 18) echo selected ?> value="18">18</option>
        		<option <?php if($nacht2lls1old == 19) echo selected ?> value="19">19</option>
               		<option <?php if($nacht2lls1old == 20) echo selected ?> value="20">20</option>
                	<option <?php if($nacht2lls1old == 21) echo selected ?> value="21">21</option>
                	<option <?php if($nacht2lls1old == 22) echo selected ?> value="22">22</option>
                	<option <?php if($nacht2lls1old == 23) echo selected ?> value="23">23</option>
                	<option <?php if($nacht2lls1old == 24) echo selected ?> value="24">24</option>
                	<option <?php if($nacht2lls1old == 25) echo selected ?> value="25">25</option>
                	<option <?php if($nacht2lls1old == 26) echo selected ?> value="26">26</option>
                	<option <?php if($nacht2lls1old == 27) echo selected ?> value="27">27</option>
                	<option <?php if($nacht2lls1old == 28) echo selected ?> value="28">28</option>
                	<option <?php if($nacht2lls1old == 29) echo selected ?> value="29">29</option>
                	<option <?php if($nacht2lls1old == 30) echo selected ?> value="30">30</option>
                	<option <?php if($nacht2lls1old == 31) echo selected ?> value="31">31</option>
                	<option <?php if($nacht2lls1old == 32) echo selected ?> value="32">32</option>
       		</select><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Ampere mit der im zweiten Intervall geladen werden soll<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtladen2abuhrs1">Morgens Laden Uhrzeit ab:</label></b>
	       	<select type="text" name="nachtladen2abuhrs1" id="nachtladen2abuhrs1">
 			<option <?php if($nachtladen2abuhrs1old == 3) echo selected ?> value="3">3</option>
 			<option <?php if($nachtladen2abuhrs1old == 4) echo selected ?> value="4">4</option>
 			<option <?php if($nachtladen2abuhrs1old == 5) echo selected ?> value="5">5</option>
 			<option <?php if($nachtladen2abuhrs1old == 6) echo selected ?> value="6">6</option>
 			<option <?php if($nachtladen2abuhrs1old == 7) echo selected ?> value="7">7</option>
 			<option <?php if($nachtladen2abuhrs1old == 8) echo selected ?> value="8">8</option>
			<option <?php if($nachtladen2abuhrs1old == 9) echo selected ?> value="9">9</option>
		</select><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		Ab wann im zweiten Intervall geladen werden soll<br><br>
	</div>
	<div class="row" style="background-color:#00ada8">
		<b><label for="nachtladen2bisuhrs1">Morgens Laden Uhrzeit bis:</label></b>
	       	<select type="text" name="nachtladen2bisuhrs1" id="nachtladen2bisuhrs1">

 			<option <?php if($nachtladen2bisuhrs1old == 4) echo selected ?> value="4">4</option>
 			<option <?php if($nachtladen2bisuhrs1old == 5) echo selected ?> value="5">5</option>
 			<option <?php if($nachtladen2bisuhrs1old == 6) echo selected ?> value="6">6</option>
 			<option <?php if($nachtladen2bisuhrs1old == 7) echo selected ?> value="7">7</option>
 			<option <?php if($nachtladen2bisuhrs1old == 8) echo selected ?> value="8">8</option>
			<option <?php if($nachtladen2bisuhrs1old == 9) echo selected ?> value="9">9</option>
			<option <?php if($nachtladen2bisuhrs1old == 10) echo selected ?> value="10">10</option>
		</select><br>

	</div>
	<div class="row" style="background-color:#00ada8">
		Bis wann morgens im zweiten Intervall geladen werden soll<br><br>
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

<div class="row"><hr>
	<h4>EVU basiertes Lastmanagement</h4>
</div>

	<div class="row">
		<b><label for="lastmaxap1">Lastmanagement Max Ampere Phase 1:</label></b>
		<input type="text" name="lastmaxap1" id="lastmaxap1" value="<?php echo $lastmaxap1old ?>"><br>
	</div>
	<div class="row">
		<b><label for="lastmaxap2">Lastmanagement Max Ampere Phase 2:</label></b>
		<input type="text" name="lastmaxap2" id="lastmaxap2" value="<?php echo $lastmaxap2old ?>"><br>
	</div>
		<div class="row">
		<b><label for="lastmaxap3">Lastmanagement Max Ampere Phase 3:</label></b>
		<input type="text" name="lastmaxap3" id="lastmaxap3" value="<?php echo $lastmaxap3old ?>"><br>
	</div>
	<div class="row">
Gültige Werte 7-64. Definiert die maximal erlaubte Stromstärke der einzelnen Phasen das Hausanschlusses im Sofort Laden Modus, sofern das EVU Modul die Werte je Phase zur Verfuegung stellt.
	</div><br><br>

<div class="row"><hr>
	<h4>Loadsharing LP1/2</h4>
</div>
<div class="row">
	<b><label for="loadsharinglp12">Loadsharing LP 1 / LP 2:</label></b>
	<select type="text" name="loadsharinglp12" id="loadsharinglp12">
		<option <?php if($loadsharinglp12old == 0) echo selected ?> value="0">Deaktiviert</option>
		<option <?php if($loadsharinglp12old == 1) echo selected ?> value="1">Aktiviert</option>
	</select>
</div>
<div class="row">
	<b><label for="loadsharingalp12">Loadsharing Ampere LP 1 / LP 2:</label></b>
	<select type="text" name="loadsharingalp12" id="loadsharingalp12">
		<option <?php if($loadsharingalp12old == 16) echo selected ?> value="16">16 Ampere</option>
		<option <?php if($loadsharingalp12old == 32) echo selected ?> value="32">32 Ampere</option>
	</select>
</div>
<div class="row">
	Wenn Ladepunkt 1 und Ladepunkt 2 sich eine Zuleitung teilen, diese Option aktivieren. Bei der OpenWB Duo muss diese Option aktiviert werden!<br>
	Sie stellt in jedem Lademodus sicher, dass nicht mehr als 16 bzw. 32A je Phase in der Summe von LP 1 und LP 2 genutzt werden.<br>
	Der richtige Anschluss ist zu gewährleisten.<br>

	Ladepunkt 1: <br>
	<p style="text-indent :2em;" >Phase 1 Zuleitung = Phase 1 Ladepunkt 1</p>
	<p style="text-indent :2em;" >Phase 2 Zuleitung = Phase 2 Ladepunkt 1</p>
	<p style="text-indent :2em;" >Phase 3 Zuleitung = Phase 3 Ladepunkt 1</p>
	Ladepunkt 2: <br>
	<p style="text-indent :2em;" >Phase 1 Zuleitung = Phase 2 Ladepunkt 2</p>
	<p style="text-indent :2em;" >Phase 2 Zuleitung = Phase 3 Ladepunkt 2</p>
	<p style="text-indent :2em;" >Phase 3 Zuleitung = Phase 1 Ladepunkt 2</p>
	Durch das Drehen der Phasen ist sichergestellt, dass 2 einphasige Autos mit voller Geschwindigkeit laden können.<br>

</div>




</div>
<div class="col-xs-1">
</div>

<button type="submit" class="btn btn-primary btn-green">Save</button>
 </form><br><br />

<br><br>
<br><br>

 <button onclick="window.location.href='./index.php'" class="btn btn-primary btn-blue">Zurück</button>
<br><br>
<div class="row">
<div class="text-center">
Open Source made with love!<br>
Jede Spende hilft die Weiterentwicklung von openWB vorranzutreiben<br>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="2K8C4Y2JTGH7U">
<input type="image" src="./img/btn_donate_SM.gif" border="0" name="submit" alt="Jetzt einfach, schnell und sicher online bezahlen – mit PayPal.">
<img alt="" border="0" src="./img/pixel.gif" width="1" height="1">
</form>
</div></div>



</div>
<script>
	var settingspwaktold = <?php echo $settingspwaktold ?>;

	var settingspwold = <?php echo $settingspwold ?>;
if ( settingspwaktold == 1 ) {
passWord();
}
function passWord() {
var testV = 1;
var pass1 = prompt('Einstellungen geschützt, bitte Password eingeben:','');

while (testV < 3) {
	if (!pass1) 
		history.go(-1);
	if (pass1 == settingspwold) {
		break;
	} 
	testV+=1;
	var pass1 = prompt('Passwort falsch','Password');
}
if (pass1!="password" & testV == 3) 
	history.go(-1);
return " ";
} 
</script>
</body></html>
