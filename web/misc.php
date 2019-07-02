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
}

$bezug_http_w_urlold = str_replace( "'", "", $bezug_http_w_urlold);
$bezug_http_ikwh_urlold = str_replace( "'", "", $bezug_http_ikwh_urlold);
$bezug_http_ekwh_urlold = str_replace( "'", "", $bezug_http_ekwh_urlold);
$wr_http_w_urlold = str_replace( "'", "", $wr_http_w_urlold);
$wr_http_kwh_urlold = str_replace( "'", "", $wr_http_kwh_urlold);
$hsocipold = str_replace( "'", "", $hsocipold);
$pushoveruserold = str_replace( "'", "", $pushoveruserold);
$pushovertokenold = str_replace( "'", "", $pushovertokenold);
?>

<div class="container">
	<div class="row"><br>
		<ul class="nav nav-tabs">
			<li><a data-toggle="tab" href="./index.php">Zurück</a></li>
			<li><a href="./settings.php">Einstellungen</a></li>
  			<li><a href="./pvconfig.php">PV Ladeeinstellungen</a></li>
			<li><a href="./smarthome.php">Smart Home</a></li>
			<li><a href="./modulconfig.php">Modulkonfiguration</a></li>
			<li><a href="./setTheme.php">Theme</a></li>
			<li class="active"><a href="./misc.php">Misc</a></li>
		</ul><br><br>
	</div>
	<form action="./tools/savemisc.php" method="POST">
		<div class="row">
			<b><label for="debug">Debugmodus:</label></b>
			<select type="text" name="debug" id="debug">
				<option <?php if($debugold == 0) echo selected ?> value="0">0</option>
				<option <?php if($debugold == 1) echo selected ?> value="1">1</option>
				<option <?php if($debugold == 2) echo selected ?> value="2">2</option>
			</select>
			<br>
		</div>
		<div class="row">
			0=Debug aus, 1=Schreibe Regelwerte in das log, 2= Schreibe die Berechnungsgrundlage in das log.<br>Das Debug Log ist <a href="../ramdisk/openWB.log">HIER</a> zu finden<br> <br>
		</div>
		<div class="row">
			<b><label for="dspeed">Geschwindigkeit Regelintervall:</label></b>
			<select type="text" name="dspeed" id="dspeed">
				<option <?php if($dspeedold == 0) echo selected ?> value="0">Normal</option>
				<option <?php if($dspeedold == 1) echo selected ?> value="1">Schnell</option>
				<option <?php if($dspeedold == 2) echo selected ?> value="2">Langsam</option>
				<option <?php if($dspeedold == 3) echo selected ?> value="3">Sehr Langsam</option>
			</select>
			<br>
		</div>

		<div class="row">
			Durch verdoppeln wird das Regelintervall von 10Sek auf 5Sek gesetzt. Vorraussetzung ist, das alle Module schnell genug Antworten.<br>Ebenso müssen die BEVs die geladen werden, schnell genug auf die Ladestromänderung reagieren.<br>Sollten Probleme oder Fehlermeldungen auftauchen zunächst das Regelintervall auf Normal stellen.<br><br>Werden Module genutzt welche z.B. eine Online API zur Abfrage nutzen oder möchte man weniger regeln, kann man das Regelintervall auf langsam(=20Sekunden) herabsetzen. <br>!Bitte beachten! Nicht nur die Regelung der PV geführten Ladung sondern auch Ladestromänderung, Stop, etc.. werden dann nur noch alle 20 Sekunden ausgeführt. Die Regelung wird träger.<br> Sehr Langsam führt zu einer Regelzeit von 60 Sekunden <br>
	<br>	</div>
		<div class="row">
			<b><label for="ladetaster">Ladetaster:</label></b>
			<select type="text" name="ladetaster" id="ladetaster">
				<option <?php if($ladetasterold == 0) echo selected ?> value="0">Aus</option>
				<option <?php if($ladetasterold == 1) echo selected ?> value="1">An</option>
			</select>
			<br>
		</div>
		<div class="row">
			Wenn aktiviert sind nach einem Neustart die externen Taster aktiv. Wenn keine verbaut sind diese Option ausschalten<br> <br>
		</div>
		<div class="row">
			<b><label for="bootmodus">Lademodus nach Start der openWB:</label></b>
			<select type="text" name="bootmodus" id="bootmodus">
				<option <?php if($bootmodusold == 0) echo selected ?> value="0">Sofort Laden</option>
				<option <?php if($bootmodusold == 1) echo selected ?> value="1">Min + PV</option>
				<option <?php if($bootmodusold == 2) echo selected ?> value="2">Nur PV</option>
				<option <?php if($bootmodusold == 3) echo selected ?> value="3">Stop</option>
				<option <?php if($bootmodusold == 4) echo selected ?> value="4">Standby</option>

			</select>
			<br>
		</div>
		<div class="row">
			Definiert den Lademodus nach Boot der openWB.<br> <br>
		</div>
<hr>
<div class="row">
	<b><label for="rfidakt">RFID Lesung:</label></b>
	<select type="text" name="rfidakt" id="rfidakt">
		<option <?php if($rfidaktold == 0) echo selected ?> value="0">Deaktiviert</option>
		<option <?php if($rfidaktold == 1) echo selected ?> value="1">Aktiviert</option>
	</select>
</div>

<div id="rfidausdiv">
	<br>
</div>
<div id="rfidandiv">
	<div class="row">
	Durch scannen von RFID Tags lässt sich die Ladung einem RFID Tag zuweisen. Derzeit unterstützt werden openWB RFID Leser und go-e an LP1.<br><br>
	</div>
<?php
$lastrfid = file_get_contents('/var/www/html/openWB/ramdisk/rfidlasttag');
?>
	<div class="row">
	Zuletzt gescannter RFID Tag: <?php echo $lastrfid ?><br><br>
	</div>

	<div class="row">
       		<b><label for="rfidlp1c1">Ladepunkt 1, Auto 1:</label></b>
        	<input type="text" name="rfidlp1c1" id="rfidlp1c1" value="<?php echo $rfidlp1c1old ?>"><br>
	<br>
	</div>
	<div class="row">
		RFID Tag eintragen.<br><br>
	</div>
	<div class="row">
       		<b><label for="rfidlp1c2">Ladepunkt 1, Auto 2:</label></b>
        	<input type="text" name="rfidlp1c2" id="rfidlp1c2" value="<?php echo $rfidlp1c2old ?>"><br>
	<br>
	</div>
	<div class="row">
		RFID Tag eintragen.<br><br>
	</div>
	<div class="row">
       		<b><label for="rfidlp1c3">Ladepunkt 1, Auto 3:</label></b>
        	<input type="text" name="rfidlp1c3" id="rfidlp1c3" value="<?php echo $rfidlp1c3old ?>"><br>
	<br>
	</div>
	<div class="row">
		RFID Tag eintragen.<br><br>
	</div>
	<div class="row">
       		<b><label for="rfidlp2c1">Ladepunkt 2, Auto 1:</label></b>
        	<input type="text" name="rfidlp2c1" id="rfidlp2c1" value="<?php echo $rfidlp2c1old ?>"><br>
	<br>
	</div>
	<div class="row">
		RFID Tag eintragen.<br><br>
	</div>
	<div class="row">
       		<b><label for="rfidlp2c2">Ladepunkt 2, Auto 2:</label></b>
        	<input type="text" name="rfidlp2c2" id="rfidlp2c2" value="<?php echo $rfidlp2c2old ?>"><br>
	<br>
	</div>
	<div class="row">
		RFID Tag eintragen.<br><br>
	</div>
	<div class="row">
       		<b><label for="rfidlp2c3">Ladepunkt 2, Auto 3:</label></b>
        	<input type="text" name="rfidlp2c3" id="rfidlp2c3" value="<?php echo $rfidlp2c3old ?>"><br>
	<br>
	</div>
	<div class="row">
		RFID Tag eintragen.<br><br>
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





<div class="row"><hr>
	<h4>Benachrichtigungen mit Pushover</h4>
</div>
<div class="row">
	<b><label for="pushbenachrichtigung">Pushover Benachrichtigungen:</label></b>
	<select type="text" name="pushbenachrichtigung" id="pushbenachrichtigung">
		<option <?php if($pushbenachrichtigungold == 0) echo selected ?> value="0">Deaktiviert</option>
		<option <?php if($pushbenachrichtigungold == 1) echo selected ?> value="1">Aktiviert</option>
	</select>
</div>

<div id="pushbaus">
	<br>
</div>
<div id="pushban">
	<div class="row">
	Zur Nutzung von Pushover muss ein Konto auf Pushover.net bestehen.<br> Nach dem Registrieren bei Pushover muss dort im Webinterface eine Applikation erstellt werden.<br>
Der Token der App, sowie das User Token nachfolgend eintragen.<br><br>
	</div>
	<div class="row">
       		<b><label for="pushoveruser">Pushover User String:</label></b>
        	<input type="text" name="pushoveruser" id="pushoveruser" value="<?php echo $pushoveruserold ?>"><br>
	<br>
	</div>
	<div class="row">
		Hier das User Token von Pushover eintragen<br><br>
	</div>
	<div class="row">
       		<b><label for="pushovertoken">Pushover App Token:</label></b>
        	<input type="text" name="pushovertoken" id="pushovertoken" value="<?php echo $pushovertokenold ?>"><br>
<br>
	</div>
	<div class="row">
		Hier das Application Token von Pushover eintragen<br><br>
	</div>

	<div class="row"><hr>
		<b>Benachrichtigungseinstellungen:</b><br><br>
	</div>
	<div class="row">
		<b><label for="pushbstartl">Beim Starten der Ladung:</label></b>
	       	<select type="text" name="pushbstartl" id="pushbstartl">
 			<option <?php if($pushbstartlold == 0) echo selected ?> value="0">Nein</option>
  			<option <?php if($pushbstartlold == 1) echo selected ?> value="1">Ja</option>
		</select><br><br>

	</div>
	<div class="row">
		<b><label for="pushbstopl">Beim Stoppen der Ladung:</label></b>
	       	<select type="text" name="pushbstopl" id="pushbstopl">
 			<option <?php if($pushbstoplold == 0) echo selected ?> value="0">Nein</option>
  			<option <?php if($pushbstoplold == 1) echo selected ?> value="1">Ja</option>
		</select><br><br>

	</div>


</div><br>
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

		<div class="row"><hr>
			<h3>	Optische Einstellungen</h3> <br>
		</div>
		<div class="row">
			<b><label for="hausverbrauchstat">Hausverbrauch auf der Hauptseite anzeigen:</label></b>
			<select type="text" name="hausverbrauchstat" id="hausverbrauchstat">
				<option <?php if($hausverbrauchstatold == 0) echo selected ?> value="0">Aus</option>
				<option <?php if($hausverbrauchstatold == 1) echo selected ?> value="1">Ein</option>
			</select>
			<br>
		</div>
		<div class="row">
			<b><label for="heutegeladen">Heute geladen auf der Hauptseite anzeigen:</label></b>
			<select type="text" name="heutegeladen" id="heutegeladen">
				<option <?php if($heutegeladenold == 0) echo selected ?> value="0">Aus</option>
				<option <?php if($heutegeladenold == 1) echo selected ?> value="1">Ein</option>
			</select>
			<br>
		</div>


		<div class="row">
			<h4>	Graphen</h4> <br>
		</div>
		<div class="row">
			<b><label for="logdailywh">Anzeige Daily Graph in Watt oder Wh:</label></b>
			<select type="text" name="logdailywh" id="logdailywh">
				<option <?php if($logdailywhold == 0) echo selected ?> value="0">Watt</option>
				<option <?php if($logdailywhold == 1) echo selected ?> value="1">Wh</option>
			</select>
			<br>
		</div>
		<div class="row">
			<b><label for="logeinspeisungneg">Einspeisung im Daily Graph positiv oder negativ anzeigen:</label></b>
			<select type="text" name="logeinspeisungneg" id="logeinspeisungneg">
				<option <?php if($logeinspeisungnegold == 0) echo selected ?>value="0">Positiv</option>
				<option <?php if($logeinspeisungnegold == 1) echo selected ?> value="1">Negativ</option>
			</select>
			<br>
		</div>
<div class="row">
	<b><label for="livegraph">Zeitintervall für den Live Graphen der Hauptseite:</label></b>
	<select type="text" name="livegraph" id="livegraph">
		<option <?php if($livegraphold == 5) echo selected ?> value="5">5 Min</option>
		<option <?php if($livegraphold == 10) echo selected ?> value="10">10 Min</option>
		<option <?php if($livegraphold == 15) echo selected ?> value="15">15 Min</option>
		<option <?php if($livegraphold == 20) echo selected ?> value="20">20 Min</option>
		<option <?php if($livegraphold == 30) echo selected ?> value="30">30 Min</option>
		<option <?php if($livegraphold == 40) echo selected ?> value="40">40 Min</option>
		<option <?php if($livegraphold == 50) echo selected ?> value="50">50 Min</option>
		<option <?php if($livegraphold == 60) echo selected ?> value="60">60 Min</option>

	</select><br>
</div>

		<div class="row">
	Hinweis: je länger das Zeitintervall des Live Graphen, desto länger die Ladezeit der Hauptseite.<br>	</div>
	<div class="row"><br>
			<b><label for="graphliveam">Interaktiver Graph auf der Hauptseite:</label></b>
			<select type="text" name="graphliveam" id="graphliveam">
				<option <?php if($graphliveamold == 0) echo selected ?> value="0">Aus</option>
				<option <?php if($graphliveamold == 1) echo selected ?> value="1">Ein</option>
			</select>

	</div>
	<div class="row">
			<b><label for="chartlegendmain">Legende auf der Hauptseite anzeigen:</label></b>
			<select type="text" name="chartlegendmain" id="chartlegendmain">
				<option <?php if($chartlegendmainold == 0) echo selected ?> value="0">Aus</option>
				<option <?php if($chartlegendmainold == 1) echo selected ?> value="1">Ein</option>
			</select>
			<br>
	</div>
	<div class="row">
			<b><label for="grapham">Interaktiver Graph im Logging:</label></b>
			<select type="text" name="grapham" id="grapham">
				<option <?php if($graphamold == 0) echo selected ?> value="0">Aus</option>
				<option <?php if($graphamold == 1) echo selected ?> value="1">Ein</option>
			</select>
			<br>
	</div>
	<div class="row">
			<b><label for="graphinteractiveam">Animation im Graph:</label></b>
			<select type="text" name="graphinteractiveam" id="graphinteractiveam">
				<option <?php if($graphinteractiveamold == 0) echo selected ?> value="0">Aus</option>
				<option <?php if($graphinteractiveamold == 1) echo selected ?> value="1">Ein</option>
			</select>
			<br><br>
	</div>
		<div class="row">
	<h3>	Releasechannel</h3> <br>
		</div>
		<div class="row">
			<b><label for="releasetrain">Releasechannel:</label></b>
			<select type="text" name="releasetrain" id="releasetrain">
				<option <?php if($releasetrainold == "stable\n") echo selected ?>value="stable">stable</option>
				<option <?php if($releasetrainold == "beta\n") echo selected ?> value="beta">beta</option>
				<option <?php if($releasetrainold == "master\n") echo selected ?> value="master">Nightly</option>
			</select>
			<br>
		</div>
		<div class="row">
			Der Stable train ist der empfohlene. Im Betazweig befinden sich die Änderungen für künftige Releases. Nightly ist der aktuelle Entwicklungszweig. Man kann grundsätzlich immer  zwischen den Zweigen wechseln. Hierfür den gewünschten Zweig auswählen, Speichern und ein Update durchführen.<br><br>
		</div>

<br><br>
		<button type="submit" class="btn btn-primary btn-green">Save</button>
	</form><br><br /><hr>
	<div class="row">
		Das Backup stellt im Falle eines Hardwaredefektes die Einstellungen und Ladelogfiles wieder her<br> <br>
	</div>
	<div class="row">
		<button onclick="window.location.href='./tools/bckredirect.html'" class="btn btn-primary btn-red">Backup erstellen</button>
		<button onclick="window.location.href='./tools/upload.html'" class="btn btn-primary btn-orange">Backup wiederherstellen</button>
	</div>
	<br><br><hr>
	<div class="row">
		Auf die neuste Version updaten, Einstellungen bleiben erhalten.<br> Der Update Prozess kann bis zu einer Minute dauern, je nach Internetverbindung!<br>Zur Sicherheit vorher ein Backup erstellen.<br><br>
	</div>
	<div class="row">
		<button onclick="window.location.href='./tools/updateredirect.html'" class="btn btn-primary btn-red">UPDATE openWB</button>
	</div>
	<div class="row">
		<button onclick="window.location.href='./tools/smashmredirect.html'" class="btn btn-primary btn-red">SMA Support</button>
	</div>
	<div class="row">
		<button onclick="window.location.href='./tools/reboot.html'" class="btn btn-primary btn-red">REBOOT</button>
	</div>

<hr>
<div class="row">

<form action="./tools/savedebug.php" method="POST">
	<h3>Debug Daten senden</h3>
</div>
	<div class="row">
		Beim Debug Daten senden wird automatisiert der Debugmodus aktiviert, Daten aufgezeichnet, versendet und anschließend der Debugmodus deaktiviert.<br>
		Zusätzlich wird die Config mitgesendet. Allerdings werden sämtlich SoC Modul Einstellungen herausgefiltert um die ggf. hinterlegten Benutzername/Passwörter NICHT zu übertragen.<br>
	</div>
<div class="row">
	<textarea rows="10" cols="100" name="debuguser" id="debuguser">Fehlerbeschreibung...</textarea><br>
	<b><label for="debugmail">Email Adresse:</label></b>
	<input type="text" name="debugemail" id="debugemail" value="Email für Rückfragen"><br>

<button type="submit" class="btn btn-primary btn-green">Debug Daten senden</button>
</form><br><br /><hr>
</div>

<div class="row">
<div class="text-center">
Open Source made with love!<br>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="2K8C4Y2JTGH7U">
<input type="image" src="./img/btn_donate_SM.gif" border="0" name="submit" alt="Jetzt einfach, schnell und sicher online bezahlen – mit PayPal.">
<img alt="" border="0" src="./img/pixel.gif" width="1" height="1">
</form>
</div></div>
</div>
</body></html>
