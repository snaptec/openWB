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
	<link rel="manifest" href="img/favicons/manifest.json">
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
	if(strpos($line, "speicherpveinbeziehen=") !== false) {
		list(, $speicherpveinbeziehenold) = explode("=", $line);
	}
	if(strpos($line, "speicherpvui=") !== false) {
		list(, $speicherpvuiold) = explode("=", $line);
	}

	if(strpos($line, "speichermaxwatt=") !== false) {
		list(, $speichermaxwattold) = explode("=", $line);
	}
	if(strpos($line, "pvbezugeinspeisung=") !== false) {
		list(, $pvbezugeinspeisungold) = explode("=", $line);
	}
	if(strpos($line, "sofortll=") !== false) {
		list(, $sofortllold) = explode("=", $line);
	}
	if(strpos($line, "minimalampv=") !== false) {
		list(, $minimalampvold) = explode("=", $line);
	}
	if(strpos($line, "minimalapv=") !== false) {
		list(, $minimalapvold) = explode("=", $line);
	}
	if(strpos($line, "minimalalp2pv=") !== false) {
		list(, $minimalalp2pvold) = explode("=", $line);
	}

	if(strpos($line, "minimalstromstaerke=") !== false) {
		list(, $minimalstromstaerkeold) = explode("=", $line);
	}
	if(strpos($line, "maximalstromstaerke=") !== false) {
		list(, $maximalstromstaerkeold) = explode("=", $line);
	}

	if(strpos($line, "evselanips1=") !== false) {
		list(, $evselanips1old) = explode("=", $line);
	}
	if(strpos($line, "lastmanagement=") !== false) {
		list(, $lastmanagementold) = explode("=", $line);
	}
	if(strpos($line, "mindestuberschuss=") !== false) {
		list(, $mindestuberschussold) = explode("=", $line);
	}
	if(strpos($line, "abschaltuberschuss=") !== false) {
		list(, $abschaltuberschussold) = explode("=", $line);
	}
	if(strpos($line, "abschaltverzoegerung=") !== false) {
		list(, $abschaltverzoegerungold) = explode("=", $line);
	}
	if(strpos($line, "einschaltverzoegerung=") !== false) {
		list(, $einschaltverzoegerungold) = explode("=", $line);
	}

	if(strpos($line, "minnurpvsocll=") !== false) {
		list(, $minnurpvsocllold) = explode("=", $line);
	}
	if(strpos($line, "minnurpvsoclp1=") !== false) {
		list(, $minnurpvsoclp1old) = explode("=", $line);
	}
	if(strpos($line, "maxnurpvsoclp1=") !== false) {
		list(, $maxnurpvsoclp1old) = explode("=", $line);
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
	if(strpos($line, "hook1ein_url=") !== false) {
		list(, $hook1ein_urlold) = explode("=", $line, 2);
	}
	if(strpos($line, "hook1aus_url=") !== false) {
		list(, $hook1aus_urlold) = explode("=", $line, 2);
	}
	if(strpos($line, "hook1ein_watt=") !== false) {
		list(, $hook1ein_wattold) = explode("=", $line, 2);
	}
	if(strpos($line, "hook1aus_watt=") !== false) {
		list(, $hook1aus_wattold) = explode("=", $line, 2);
	}
	if(strpos($line, "hook1_aktiv=") !== false) {
		list(, $hook1_aktivold) = explode("=", $line, 2);
	}
	if(strpos($line, "adaptpv=") !== false) {
		list(, $adaptpvold) = explode("=", $line, 2);
	}
	if(strpos($line, "adaptfaktor=") !== false) {
		list(, $adaptfaktorold) = explode("=", $line, 2);
	}


}
$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
$bezug_http_w_urlold = str_replace( "'", "", $bezug_http_w_urlold);
$bezug_http_ikwh_urlold = str_replace( "'", "", $bezug_http_ikwh_urlold);
$bezug_http_ekwh_urlold = str_replace( "'", "", $bezug_http_ekwh_urlold);
$wr_http_w_urlold = str_replace( "'", "", $wr_http_w_urlold);
$wr_http_kwh_urlold = str_replace( "'", "", $wr_http_kwh_urlold);
$hook1ein_urlold = str_replace( "'", "", $hook1ein_urlold);
$hook1aus_urlold = str_replace( "'", "", $hook1aus_urlold);






?>



<div class="container">
<div class="row"><br>
 <ul class="nav nav-tabs">
    <li><a data-toggle="tab" href="./index.php">Zurück</a></li>
    <li><a href="./settings.php">Einstellungen</a></li>
    <li class="active"><a href="./pvconfig.php">PV Ladeeinstellungen</a></li>
    <li><a href="./modulconfig.php">Modulkonfiguration</a></li>
	<li><a href="./settheme.php">Theme</a></li>
	<li><a href="./misc.php">Misc</a></li>
  </ul><br><br>
 </div>
<form action="./tools/savepv.php" method="POST">

<div class="col-xs-1">
</div>
<div class="col-xs-10">




<div class="row">
	<h3>PV Regelung</h3>
</div>
<div class="row" style="background-color:#befebe">
	Die Kombination aus Mindestüberschuss und Abschaltüberschuss sollte sinnvoll gewählt werden.<br>
	Ansonsten wird im 10 Sekunden Takt die Ladung gestartet und gestoppt.<br>
	Es macht z.B. 1320 Watt mindestuberschuss und 900 Watt abschaltuberschuss Sinn<br>
</div>
<div class="row" style="background-color:#befebe">
	<b><label for="mindestuberschuss">Mindestüberschuss:</label></b>
	<input type="text" name="mindestuberschuss" id="mindestuberschuss" value="<?php echo $mindestuberschussold ?>"><br>
</div>
<div class="row" style="background-color:#befebe">
	Gültige Werte 0-9999. Mindestüberschuss in Watt bevor im Lademodus "Nur PV" die Ladung beginnt.<br> Soll wenig bis kein Netzbezug vorhanden sein macht ein Wert um 1300-1600 Sinn.<br><br>
</div>
<div class="row" style="background-color:#befebe">
	<b><label for="abschaltuberschuss">Abschaltüberschuss:</label></b>
	<input type="text" name="abschaltuberschuss" id="abschaltuberschuss" value="<?php echo $abschaltuberschussold ?>"><br>
</div>
<div class="row" style="background-color:#befebe">
	Gültige Werte 0-9999. Ab wieviel Watt Bezug abgeschaltet werden soll.<br>
Zunächst wird in jedem Zyklus die Ladeleistung Stufenweise bis auf Minimalstromstaerke reduziert. Danach greift die Abschaltung.<br>
Der Wert gibt an wieviel Watt insgesamt bezogen werden bevor abgeschaltet wird.<br><br>


</div>
<div class="row" style="background-color:#befebe">
	<b><label for="einschaltverzoegerung">Einschaltverzögerung:</label></b>
	<input type="text" name="einschaltverzoegerung" id="einschaltverzoegerung" value="<?php echo $einschaltverzoegerungold ?>"><br>
</div>
<div class="row" style="background-color:#befebe">
Gültige Werte Zeit in Sekunden in 10ner Schritten. Die Verzögerung gibt an um wieviel Sekunden (0,10,20,30,...300,310,320, usw.) im Nur PV Modus gewartet wird bis die Ladung startet.
<br> Gibt man hier 40 Sekunden an, muss über die gesamte Spanne von 40 Sekunden der Überschuss größer als der Einschaltüberschuss sein.<br>
</div><br>

<div class="row" style="background-color:#befebe">
	<b><label for="abschaltverzoegerung">Abschaltverzögerung:</label></b>
	<input type="text" name="abschaltverzoegerung" id="abschaltverzoegerung" value="<?php echo $abschaltverzoegerungold ?>"><br>
</div>

<div class="row" style="background-color:#befebe">
Gültige Werte Zeit in Sekunden in 10ner Schritten. Die Verzögerung gibt an um wieviel Sekunden (0,10,20,30,...300,310,320, usw.) im Nur PV Modus die Abschaltung hinausgezögert wird.
<br> Gibt man hier 40 Sekunden an, muss über die gesamte Spanne von 40 Sekunden der Bezug größer als der Abschaltüberschuss sein. <br> Ist der Bezug nach 20 Sekunden kurzzeitig kleiner als der Abschaltüberschuss beginnen die 40 Sekunden erneut.<br>
</div><br>
<div class="row" style="background-color:#befebe">
	<b><label for="minimalampv">Minimalstromstärke fuer den Min + PV Laden Modus:</label></b>
	<select type="text" name="minimalampv" id="minimalampv">
		<option <?php if($minimalampvold == 6) echo selected ?> value="6">6</option>
		<option <?php if($minimalampvold == 7) echo selected ?> value="7">7</option>
		<option <?php if($minimalampvold == 8) echo selected ?> value="8">8</option>
		<option <?php if($minimalampvold == 9) echo selected ?> value="9">9</option>
		<option <?php if($minimalampvold == 10) echo selected ?> value="10">10</option>
		<option <?php if($minimalampvold == 11) echo selected ?> value="11">11</option>
		<option <?php if($minimalampvold == 12) echo selected ?> value="12">12</option>
		<option <?php if($minimalampvold == 13) echo selected ?> value="13">13</option>
		<option <?php if($minimalampvold == 14) echo selected ?> value="14">14</option>
		<option <?php if($minimalampvold == 15) echo selected ?> value="15">15</option>
		<option <?php if($minimalampvold == 16) echo selected ?> value="16">16</option>
	</select><br>

</div>

<div class="row" style="background-color:#befebe">
Definiert die Minimal erlaubte Stromstaerke in A je Phase fuer den Min + PV Laden Modus.<br>
</div>
<div class="row" style="background-color:#befebe">
	<b><label for="minimalapv">Minimalstromstärke fuer den Nur PV Laden Modus LP1:</label></b>
	<select type="text" name="minimalapv" id="minimalapv">
		<option <?php if($minimalapvold == 6) echo selected ?> value="6">6</option>
		<option <?php if($minimalapvold == 7) echo selected ?> value="7">7</option>
		<option <?php if($minimalapvold == 8) echo selected ?> value="8">8</option>
		<option <?php if($minimalapvold == 9) echo selected ?> value="9">9</option>
		<option <?php if($minimalapvold == 10) echo selected ?> value="10">10</option>
		<option <?php if($minimalapvold == 11) echo selected ?> value="11">11</option>
		<option <?php if($minimalapvold == 12) echo selected ?> value="12">12</option>
		<option <?php if($minimalapvold == 13) echo selected ?> value="13">13</option>
		<option <?php if($minimalapvold == 14) echo selected ?> value="14">14</option>
		<option <?php if($minimalapvold == 15) echo selected ?> value="15">15</option>
		<option <?php if($minimalapvold == 16) echo selected ?> value="16">16</option>
	</select><br>


</div>
<div class="row" style="background-color:#befebe">
	<b><label for="minimalalp2pv">Minimalstromstärke fuer den Nur PV Laden Modus LP2:</label></b>
	<select type="text" name="minimalalp2pv" id="minimalalp2pv">
		<option <?php if($minimalalp2pvold == 6) echo selected ?> value="6">6</option>
		<option <?php if($minimalalp2pvold == 7) echo selected ?> value="7">7</option>
		<option <?php if($minimalalp2pvold == 8) echo selected ?> value="8">8</option>
		<option <?php if($minimalalp2pvold == 9) echo selected ?> value="9">9</option>
		<option <?php if($minimalalp2pvold == 10) echo selected ?> value="10">10</option>
	</select><br>


</div>


<div class="row" style="background-color:#befebe">
Definiert die Minimal erlaubte Stromstaerke in A je Phase fuer den Nur PV Laden Modus.<br>
</div>

<div class="row" style="background-color:#befebe">
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
<div class="row" style="background-color:#befebe">
	Gibt an mit wieviel Ampere Maximal geladen wird.<br><br>
</div>

<br>

<div class="row" style="background-color:#befebe">
	<b><label for="minnurpvsoclp1">Minimal SoC fuer den Nur PV Laden Modus:</label></b>
	<select type="text" name="minnurpvsoclp1" id="minnurpvsoclp1">
		<option <?php if($minnurpvsoclp1old == 0) echo selected ?> value="0">0</option>
		<option <?php if($minnurpvsoclp1old == 5) echo selected ?> value="5">5</option>
		<option <?php if($minnurpvsoclp1old == 10) echo selected ?> value="10">10</option>
		<option <?php if($minnurpvsoclp1old == 15) echo selected ?> value="15">15</option>
		<option <?php if($minnurpvsoclp1old == 20) echo selected ?> value="20">20</option>
		<option <?php if($minnurpvsoclp1old == 25) echo selected ?> value="25">25</option>
		<option <?php if($minnurpvsoclp1old == 30) echo selected ?> value="30">30</option>
		<option <?php if($minnurpvsoclp1old == 35) echo selected ?> value="35">35</option>
		<option <?php if($minnurpvsoclp1old == 40) echo selected ?> value="40">40</option>
		<option <?php if($minnurpvsoclp1old == 45) echo selected ?> value="45">45</option>
		<option <?php if($minnurpvsoclp1old == 50) echo selected ?> value="50">50</option>
		<option <?php if($minnurpvsoclp1old == 55) echo selected ?> value="55">55</option>
		<option <?php if($minnurpvsoclp1old == 60) echo selected ?> value="60">60</option>
		<option <?php if($minnurpvsoclp1old == 65) echo selected ?> value="65">65</option>
		<option <?php if($minnurpvsoclp1old == 70) echo selected ?> value="70">70</option>
		<option <?php if($minnurpvsoclp1old == 75) echo selected ?> value="75">75</option>
		<option <?php if($minnurpvsoclp1old == 80) echo selected ?> value="80">80</option>
	</select>
	</div>
	<div class="row" style="background-color:#befebe">
	Definiert einen Mindest SoC Wert (EV) bis zu welchem im Nur PV Modus immer geladen wird - auch wenn keine PV Leistung zur Verfügung steht.<br> Ist nur aktiv wenn nur ein Ladepunkt konfiguriert ist!
	</div><br>


<div class="row" style="background-color:#befebe">
	<b><label for="maxnnurpvsoclp1">Maximal SoC fuer den Nur PV Laden Modus:</label></b>
	<select type="text" name="maxnurpvsoclp1" id="maxnurpvsoclp1">
		<option <?php if($maxnurpvsoclp1old == 50) echo selected ?> value="50">50</option>
		<option <?php if($maxnurpvsoclp1old == 55) echo selected ?> value="55">55</option>
		<option <?php if($maxnurpvsoclp1old == 60) echo selected ?> value="60">60</option>
		<option <?php if($maxnurpvsoclp1old == 65) echo selected ?> value="65">65</option>
		<option <?php if($maxnurpvsoclp1old == 70) echo selected ?> value="70">70</option>
		<option <?php if($maxnurpvsoclp1old == 75) echo selected ?> value="75">75</option>
		<option <?php if($maxnurpvsoclp1old == 80) echo selected ?> value="80">80</option>
		<option <?php if($maxnurpvsoclp1old == 85) echo selected ?> value="85">85</option>
		<option <?php if($maxnurpvsoclp1old == 90) echo selected ?> value="90">90</option>
		<option <?php if($maxnurpvsoclp1old == 95) echo selected ?> value="95">95</option>
		<option <?php if($maxnurpvsoclp1old == 100) echo selected ?> value="100">100</option>
	</select>
	</div>
	<div class="row" style="background-color:#befebe">
	Definiert einen Maximal SoC Wert bis zu welchem im Nur PV Modus geladen wird.<br> Ist nur aktiv wenn nur ein Ladepunkt konfiguriert ist!
	</div>
<br>
<div class="row" style="background-color:#befebe">
	<b><label for="minnurpvsocll">Stromstärke fuer den Nur PV Laden Modus wenn Mindest SoC noch nicht erreicht:</label></b>
	<select type="text" name="minnurpvsocll" id="minnurpvsocll">
		<option <?php if($minnurpvsocllold == 6) echo selected ?> value="6">6</option>
		<option <?php if($minnurpvsocllold == 7) echo selected ?> value="7">7</option>
		<option <?php if($minnurpvsocllold == 8) echo selected ?> value="8">8</option>
		<option <?php if($minnurpvsocllold == 9) echo selected ?> value="9">9</option>
		<option <?php if($minnurpvsocllold == 10) echo selected ?> value="10">10</option>
		<option <?php if($minnurpvsocllold == 11) echo selected ?> value="11">11</option>
		<option <?php if($minnurpvsocllold == 12) echo selected ?> value="12">12</option>
		<option <?php if($minnurpvsocllold == 13) echo selected ?> value="13">13</option>
		<option <?php if($minnurpvsocllold == 14) echo selected ?> value="14">14</option>
		<option <?php if($minnurpvsocllold == 15) echo selected ?> value="15">15</option>
		<option <?php if($minnurpvsocllold == 16) echo selected ?> value="16">16</option>
		<option <?php if($minnurpvsocllold == 17) echo selected ?> value="17">17</option>
		<option <?php if($minnurpvsocllold == 18) echo selected ?> value="18">18</option>
		<option <?php if($minnurpvsocllold == 19) echo selected ?> value="19">19</option>
		<option <?php if($minnurpvsocllold == 20) echo selected ?> value="20">20</option>
		<option <?php if($minnurpvsocllold == 21) echo selected ?> value="21">21</option>
		<option <?php if($minnurpvsocllold == 22) echo selected ?> value="22">22</option>
		<option <?php if($minnurpvsocllold == 23) echo selected ?> value="23">23</option>
		<option <?php if($minnurpvsocllold == 24) echo selected ?> value="24">24</option>
		<option <?php if($minnurpvsocllold == 25) echo selected ?> value="25">25</option>
		<option <?php if($minnurpvsocllold == 26) echo selected ?> value="26">26</option>
		<option <?php if($minnurpvsocllold == 27) echo selected ?> value="27">27</option>
		<option <?php if($minnurpvsocllold == 28) echo selected ?> value="28">28</option>
		<option <?php if($minnurpvsocllold == 29) echo selected ?> value="29">29</option>
		<option <?php if($minnurpvsocllold == 30) echo selected ?> value="30">30</option>
		<option <?php if($minnurpvsocllold == 31) echo selected ?> value="31">31</option>
		<option <?php if($minnurpvsocllold == 32) echo selected ?> value="32">32</option>
	</select></div>
	<div class="row" style="background-color:#befebe">
	Definiert die Ladeleistung wenn Mindest SoC im Nur PV Laden Modus noch nicht erreicht ist.<br> Ist nur aktiv wenn nur ein Ladepunkt konfiguriert ist!
	</div>



<br><br>
	<div class="row" style="background-color:#befebe">
		<b><label for="pvbezugeinspeisung">PV Lademodus:</label></b>
	       	<select type="text" name="pvbezugeinspeisung" id="pvbezugeinspeisung">
 			<option <?php if($pvbezugeinspeisungold == 0) echo selected ?> value="0">Einspeisung</option>
  			<option <?php if($pvbezugeinspeisungold == 1) echo selected ?> value="1">Bezug</option>
			<option <?php if($pvbezugeinspeisungold == 2) echo selected ?> value="2">Manueller Offset</option>
		</select><br>

	</div>
	<div class="row" style="background-color:#befebe">
		Definiert die Regelung des PV Mdous. Bei Einspeisung wird von 0-230W Einspeisung geregelt und bei Bezug von 230W Bezug bis 0W. Die Werte sind beispielhaft fuer einphasiges Laden und definieren die Schwellen fuer das Hoch und Runterregeln des Ladestroms.<br><br>
	</div>

	<div class="row" style="background-color:#befebe">
		<b><label for="offsetpv">Manuelles Offset in Watt:</label></b>
		<input type="text" name="offsetpv" id="offsetpv" value="<?php echo $offsetpvold ?>"><br>
	</div>
	<div class="row" style="background-color:#befebe">
Manuelles Offset in Watt für die PV Regelmodi zum Einbau eines zusätzlichen Regelpuffers. Verschiebt den Nullpunkt der Regelung. <br>
Bei PV-Lademodus muss „Manueller Offset" aktiviert sein.<br>
Erlaubte Werte: Ganzzahl in Watt, minus als Vorzeichen, z.B.: -200, 200, 356, usw.<br>
z.B.: bei "200" wird von 200 W-430 W Einspeisung geregelt, anstatt von 0-230 W wie beim Modus „Einspeisung". negative Werte entsprechend in die Richtung „Bezug".<br><br>

</div>


<div id="speicherpvrangdiv">
	<br><br><div class="row" style="background-color:#fcbe1e">
		<b><label for="speicherpveinbeziehen">Speicherbeachtung PV Lademodus:</label></b>
	       	<select type="text" name="speicherpveinbeziehen" id="speicherpveinbeziehen">
 			<option <?php if($speicherpveinbeziehenold == 0) echo selected ?> value="0">Speicher hat Vorrang</option>
  			<option <?php if($speicherpveinbeziehenold == 1) echo selected ?> value="1">EV hat Vorrang</option>
		</select><br>
		<b><label for="speicherpveinbeziehen">Auf der Hauptseite anzeigen:</label></b>
		<select type="text" name="speicherpvui" id="speicherpvui">
 			<option <?php if($speicherpvuiold == 0) echo selected ?> value="0">Nein</option>
  			<option <?php if($speicherpvuiold == 1) echo selected ?> value="1">Ja</option>
		</select><br>

	</div>
	<div class="row" style="background-color:#fcbe1e">
		Beeinflusst die Regelung des PV Mdous in Verbindung mit einem Speicher. Bei der Option Speicher hat Vorrang wird die EV Ladung erst gestartet wenn der Speicher mit seiner maximalen Leistung lädt und der eingestellte Mindestüberschuss erreicht ist.<br>Bei der Option EV hat Vorrang wird die Speicherladeleistung mit in den verfügbaren Überschuss eingerechnet, es ist jedoch möglich eine Mindestladung zu garantieren.
	<br><br>
	</div>
	<div id="speicherevvdiv">
		<div class="row" style="background-color:#fcbe1e">
			<b><label for="speichermaxwatt">Mindestwatt Speicher:</label></b>
			<input type="text" name="speichermaxwatt" id="speichermaxwatt" value="<?php echo $speichermaxwattold ?>"><br>
		</div>
		<div class="row" style="background-color:#fcbe1e">
		Definiert einen Wert, der trotz Vorrang des EV immer als Ladeleistung für den Speicher vorgehalten wird. Verfügbarer Überschuss über diesem Wert wird der EV Ladung zugerechnet.<br><br>
		</div>
	</div>

</div>

<input hidden name="speicherpvrang" id="speicherpvrang" value="<?php echo $speichervorhanden ; ?>">
<script>
$(function() {
   if($('#speicherpvrang').val() == '1') {
	$('#speicherpvrangdiv').show();
      } else {
	$('#speicherpvrangdiv').hide();
      }
});
$(function() {
   if($('#speicherpveinbeziehen').val() == '1') {
	$('#speicherevvdiv').show();
      } else {
	$('#speicherevvdiv').hide();
      }
	$('#speicherpveinbeziehen').change(function(){
	   if($('#speicherpveinbeziehen').val() == '1') {
	$('#speicherevvdiv').show();
      } else {
	$('#speicherevvdiv').hide();
      }
	});
});
</script>
<br><br><div class="row" style="background-color:#befebe">
	<b><label for="adaptpv">Adaptives Nur PV Laden:</label></b>
	<select type="text" name="adaptpv" id="adaptpv">
		<option <?php if($adaptpvold == 0) echo selected ?> value="0">Aus</option>
		<option <?php if($adaptpvold == 1) echo selected ?> value="1">An</option>
	</select><br>

</div>
<div class="row" style="background-color:#befebe">
	Beeinflusst die Regelung des Nur PV Modus wenn folgende Bedingungen erfüllt sind:<br>- Laden im Nur PV Modus<br>- zwei EVs Laden gleichzeitig<br>- für beide ist ein SoC verfügbar<br>- beide EVs laden mit der selben Anzahl Phasen
<br><br>
</div>
<div id="adaptpvdiv">
	<div class="row" style="background-color:#befebe">
		<b><label for="adaptfaktor">Faktor:</label></b>
		<input type="text" name="adaptfaktor" id="adaptfaktor" value="<?php echo $adaptfaktorold ?>"><br>
	</div>
	<div class="row" style="background-color:#befebe">
	Defniert den Faktor zur Berechnung des Ladestroms. Herangezogen wird die Differenz der beiden SoC Werte. Für jeden Faktor Wert wird der Ladestrom um ein Ampere gesenkt, bzw. erhöht.<br>Beispiel:<br>
Zur verfügung stehende Ladeleistung 16A, Faktor 5, SoC EV 1 69 %, SoC EV 2 33 %<br>
Die Differenz beträgt 36 %, geteilt durch Faktor 5 ergibt den Wert 7.<br> Nun wird EV 1 mit 9A geladen (16A - 7A) und EV 2 mit 23A (16A + 7A).<br>Je näher die SoC Werte sind, je geringer wird der Unterschied.<br>Das leerere EV wird so bevorzugt.<br>Es wird maximal bis zur Minimal bzw. Maximalstromstärke angepasst.<br><br>
	</div>
</div>
<script>

$(function() {
   if($('#adaptpv').val() == '1') {
	$('#adaptpvdiv').show();
      } else {
	$('#adaptpvdiv').hide();
      }
	$('#adaptpv').change(function(){
	   if($('#adaptpv').val() == '1') {
	$('#adaptpvdiv').show();
      } else {
	$('#adaptpvdiv').hide();
      }
	});
});
</script>


<div class="row"><hr>
	<h4>Steuerung externer Geräte</h4>
</div>
<div class="row">
	<b><label for="hook1_aktiv">Externes Gerät 1:</label></b>
	<select type="text" name="hook1_aktiv" id="hook1_aktiv">
		<option <?php if($hook1_aktivold == 0) echo selected ?> value="0">Deaktiviert</option>
		<option <?php if($hook1_aktivold == 1) echo selected ?> value="1">Aktiviert</option>
	</select>
</div>

<div id="hook1ausdiv">
	<br>
</div>
<div id="hook1andiv">
	<div class="row">
	Externe Geräte lassen sich per definierter URL (Webhook) an- und ausschalten in Abhängigkeit des Überschusses<br><br>
	</div>
	<div class="row">
       		<b><label for="hook1ein_watt">Gerät 1 Einschaltschwelle:</label></b>
        	<input type="text" name="hook1ein_watt" id="hook1ein_watt" value="<?php echo $hook1ein_wattold ?>"><br>
	<br>
	</div>
	<div class="row">
		Einschaltschwelle in Watt bei die unten stehende URL aufgerufen wird.<br><br>
	</div>
	<div class="row">
       		<b><label for="hook1ein_url">Gerät 1 Einschalturl:</label></b>
        	<input type="text" name="hook1ein_url" id="hook1ein_url" value="<?php echo htmlspecialchars($hook1ein_urlold) ?>"><br>
	<br>
	</div>
	<div class="row">
		Einschalturl die aufgerufen wird bei entsprechendem Überschuss.<br><br>
	</div>
	<div class="row">
       		<b><label for="hook1aus_watt">Gerät 1 Ausschaltschwelle:</label></b>
        	<input type="text" name="hook1aus_watt" id="hook1aus_watt" value="<?php echo $hook1aus_wattold ?>"><br>
	<br>
	</div>
	<div class="row">
		Ausschaltschwelle in Watt bei die unten stehende URL aufgerufen wird. Soll die Abschaltung bei Bezug stattfinden eine negative Zahl eingeben.<br><br>
	</div>
	<div class="row">
       		<b><label for="hook1aus_url">Gerät 1 Ausschalturl:</label></b>
        	<input type="text" name="hook1aus_url" id="hook1aus_url" value="<?php echo htmlspecialchars($hook1aus_urlold) ?>"><br>
	<br>
	</div>
	<div class="row">
		Ausschalturl die aufgerufen wird bei entsprechendem Überschuss.<br><br>
	</div>

</div><br>
<script>
$(function() {
      if($('#hook1_aktiv').val() == '0') {
		$('#hook1ausdiv').show();
		$('#hook1andiv').hide();
      } else {
		$('#hook1ausdiv').hide();
	       	$('#hook1andiv').show();
      }

	$('#hook1_aktiv').change(function(){
	      if($('#hook1_aktiv').val() == '0') {
			$('#hook1ausdiv').show();
			$('#hook1andiv').hide();
	      } else {
			$('#hook1ausdiv').hide();
		       	$('#hook1andiv').show();
	      }
	    });
});
</script>




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
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="2K8C4Y2JTGH7U">
<input type="image" src="./img/btn_donate_SM.gif" border="0" name="submit" alt="Jetzt einfach, schnell und sicher online bezahlen – mit PayPal.">
<img alt="" border="0" src="./img/pixel.gif" width="1" height="1">
</form>
</div></div>



</div>
</body></html>
