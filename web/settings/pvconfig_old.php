<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Einstellungen</title>
		<meta name="description" content="Control your charge" />
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
				if(strpos($line, "speicherpveinbeziehen=") !== false) {
					list(, $speicherpveinbeziehenold) = explode("=", $line);
				}
				if(strpos($line, "nurpv70dynact=") !== false) {
					list(, $nurpv70dynactold) = explode("=", $line);
				}
				if(strpos($line, "nurpv70dynw=") !== false) {
					list(, $nurpv70dynwold) = explode("=", $line);
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
				if(strpos($line, "adaptpv=") !== false) {
					list(, $adaptpvold) = explode("=", $line, 2);
				}
				if(strpos($line, "adaptfaktor=") !== false) {
					list(, $adaptfaktorold) = explode("=", $line, 2);
				}
				if(strpos($line, "speichersocnurpv=") !== false) {
					list(, $speichersocnurpvold) = explode("=", $line, 2);
				}
				if(strpos($line, "speichersocminpv=") !== false) {
					list(, $speichersocminpvold) = explode("=", $line, 2);
				}
				if(strpos($line, "speichersochystminpv=") !== false) {
					list(, $speichersochystminpvold) = explode("=", $line, 2);
				}
				if(strpos($line, "speicherwattnurpv=") !== false) {
					list(, $speicherwattnurpvold) = explode("=", $line, 2);
				}

			}
			$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
			$bezug_http_w_urlold = str_replace( "'", "", $bezug_http_w_urlold);
			$bezug_http_ikwh_urlold = str_replace( "'", "", $bezug_http_ikwh_urlold);
			$bezug_http_ekwh_urlold = str_replace( "'", "", $bezug_http_ekwh_urlold);
			$wr_http_w_urlold = str_replace( "'", "", $wr_http_w_urlold);
			$wr_http_kwh_urlold = str_replace( "'", "", $wr_http_kwh_urlold);
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<div class="col-sm-12">
				<form action="./tools/savepv.php" method="POST">

					<div class="row">
						<h3>PV Regelung</h3>
					</div>
					<div class="row" style="background-color:#befebe">
						Die Kombination aus Mindestüberschuss und Abschaltüberschuss sollte sinnvoll gewählt werden.<br>
						Ansonsten wird im 10 Sekunden Takt die Ladung gestartet und gestoppt.<br>
						Ein sinnvoller Wert für den Mindestüberschuss ist beispielsweise 1320, für den Abschaltüberschuss 900.
					</div>
					<div class="row" style="background-color:#befebe">
						<b><label for="mindestuberschuss">Mindestüberschuss:</label></b>
						<input type="text" name="mindestuberschuss" id="mindestuberschuss" value="<?php echo $mindestuberschussold ?>">
					</div>
					<div class="row" style="background-color:#befebe">
						Gültige Werte 0-9999. Mindestüberschuss in Watt bevor im Lademodus "Nur PV" die Ladung beginnt.<br>
						Soll wenig bis kein Netzbezug vorhanden sein, macht ein Wert um 1300-1600 Sinn.
					</div>
					<div class="row" style="background-color:#befebe">
						<b><label for="abschaltuberschuss">Abschaltüberschuss:</label></b>
						<input type="text" name="abschaltuberschuss" id="abschaltuberschuss" value="<?php echo $abschaltuberschussold ?>">
					</div>
					<div class="row" style="background-color:#befebe">
						Gültige Werte 0-9999. Der Wert bestimmt ab wieviel Watt Bezug abgeschaltet werden soll.<br>
						Zunächst wird in jedem Zyklus die Ladeleistung stufenweise bis auf Minimalstromstärke reduziert. Danach greift die Abschaltung.<br>
						Der Wert gibt an wieviel Watt insgesamt bezogen werden bevor abgeschaltet wird.
					</div>
					<div class="row" style="background-color:#befebe">
						<b><label for="einschaltverzoegerung">Einschaltverzögerung:</label></b>
						<input type="text" name="einschaltverzoegerung" id="einschaltverzoegerung" value="<?php echo $einschaltverzoegerungold ?>">
					</div>
					<div class="row" style="background-color:#befebe">
						Gültige Werte Zeit in Sekunden in 10ner Schritten. Die Verzögerung gibt an um wieviel Sekunden (0,10,20,30,...300,310,320, usw.) im "Nur PV" Modus gewartet wird bis die Ladung startet.<br>
						Gibt man hier 40 Sekunden an, muss über die gesamte Spanne von 40 Sekunden der Überschuss größer als der Einschaltüberschuss sein.<br>
					</div>

					<div class="row" style="background-color:#befebe">
						<b><label for="abschaltverzoegerung">Abschaltverzögerung:</label></b>
						<input type="text" name="abschaltverzoegerung" id="abschaltverzoegerung" value="<?php echo $abschaltverzoegerungold ?>">
					</div>

					<div class="row" style="background-color:#befebe">
						Gültige Werte Zeit in Sekunden in 10ner Schritten. Die Verzögerung gibt an um wieviel Sekunden (0,10,20,30,...300,310,320, usw.) im "Nur PV" Modus die Abschaltung hinausgezögert wird. <br>
						Gibt man hier 120 Sekunden an, muss über die gesamte Spanne von 120 Sekunden der Bezug größer als der Abschaltüberschuss sein. <br>
						Ist der Bezug nach 20 Sekunden kurzzeitig kleiner als der Abschaltüberschuss, beginnen die 120 Sekunden erneut.<br>
						Es wird empfohlen, die Abschaltverzögerung nicht zu gering zu setzen, da dies unter ungünstigen Umständen ein häufiges Starten/Stoppen zur Folge hat.
					</div>
					<div class="row" style="background-color:#befebe">
						<b><label for="minimalampv">Minimalstromstärke fuer den Min + PV Laden Modus:</label></b>
						<select name="minimalampv" id="minimalampv">
							<option <?php if($minimalampvold == 6) echo "selected" ?> value="6">6</option>
							<option <?php if($minimalampvold == 7) echo "selected" ?> value="7">7</option>
							<option <?php if($minimalampvold == 8) echo "selected" ?> value="8">8</option>
							<option <?php if($minimalampvold == 9) echo "selected" ?> value="9">9</option>
							<option <?php if($minimalampvold == 10) echo "selected" ?> value="10">10</option>
							<option <?php if($minimalampvold == 11) echo "selected" ?> value="11">11</option>
							<option <?php if($minimalampvold == 12) echo "selected" ?> value="12">12</option>
							<option <?php if($minimalampvold == 13) echo "selected" ?> value="13">13</option>
							<option <?php if($minimalampvold == 14) echo "selected" ?> value="14">14</option>
							<option <?php if($minimalampvold == 15) echo "selected" ?> value="15">15</option>
							<option <?php if($minimalampvold == 16) echo "selected" ?> value="16">16</option>
						</select>
					</div>

					<div class="row" style="background-color:#befebe">
						Definiert die minimal erlaubte Stromstärke in Ampere je Phase für den "Min + PV Laden" Modus. Bei manchen Fahrzeugen, z.B. der Zoe, sind 7-12A nötig, sonst wird die Ladung nicht gestartet.
					</div>
					<div class="row" style="background-color:#befebe">
						<b><label for="minimalapv">Minimalstromstärke fuer den Nur PV Laden Modus LP1:</label></b>
						<select name="minimalapv" id="minimalapv">
							<option <?php if($minimalapvold == 6) echo "selected" ?> value="6">6</option>
							<option <?php if($minimalapvold == 7) echo "selected" ?> value="7">7</option>
							<option <?php if($minimalapvold == 8) echo "selected" ?> value="8">8</option>
							<option <?php if($minimalapvold == 9) echo "selected" ?> value="9">9</option>
							<option <?php if($minimalapvold == 10) echo "selected" ?> value="10">10</option>
							<option <?php if($minimalapvold == 11) echo "selected" ?> value="11">11</option>
							<option <?php if($minimalapvold == 12) echo "selected" ?> value="12">12</option>
							<option <?php if($minimalapvold == 13) echo "selected" ?> value="13">13</option>
							<option <?php if($minimalapvold == 14) echo "selected" ?> value="14">14</option>
							<option <?php if($minimalapvold == 15) echo "selected" ?> value="15">15</option>
							<option <?php if($minimalapvold == 16) echo "selected" ?> value="16">16</option>
						</select>
					</div>
					<div class="row" style="background-color:#befebe">
						<b><label for="minimalalp2pv">Minimalstromstärke fuer den Nur PV Laden Modus LP2:</label></b>
						<select name="minimalalp2pv" id="minimalalp2pv">
							<option <?php if($minimalalp2pvold == 6) echo "selected" ?> value="6">6</option>
							<option <?php if($minimalalp2pvold == 7) echo "selected" ?> value="7">7</option>
							<option <?php if($minimalalp2pvold == 8) echo "selected" ?> value="8">8</option>
							<option <?php if($minimalalp2pvold == 9) echo "selected" ?> value="9">9</option>
							<option <?php if($minimalalp2pvold == 10) echo "selected" ?> value="10">10</option>
							<option <?php if($minimalalp2pvold == 11) echo "selected" ?> value="11">11</option>
							<option <?php if($minimalalp2pvold == 12) echo "selected" ?> value="12">12</option>
						</select>
					</div>

					<div class="row" style="background-color:#befebe">
						Definiert die minimal erlaubte Stromstärke in Ampere je Phase für den "Nur PV Laden" Modus. Bei manchen Fahrzeugen, z.B. der Zoe, sind 7-12A nötig, sonst wird die Ladung nicht gestartet.
					</div>

					<div class="row" style="background-color:#befebe">
						<b><label for="maximalstromstaerke">Maximalstromstärke in A:</label></b>
						<select name="maximalstromstaerke" id="maximalstromstaerke">
							<option <?php if($maximalstromstaerkeold == 11) echo "selected" ?> value="11">11</option>
							<option <?php if($maximalstromstaerkeold == 12) echo "selected" ?> value="12">12</option>
							<option <?php if($maximalstromstaerkeold == 13) echo "selected" ?> value="13">13</option>
							<option <?php if($maximalstromstaerkeold == 14) echo "selected" ?> value="14">14</option>
							<option <?php if($maximalstromstaerkeold == 15) echo "selected" ?> value="15">15</option>
							<option <?php if($maximalstromstaerkeold == 16) echo "selected" ?> value="16">16</option>
							<option <?php if($maximalstromstaerkeold == 17) echo "selected" ?> value="17">17</option>
							<option <?php if($maximalstromstaerkeold == 18) echo "selected" ?> value="18">18</option>
							<option <?php if($maximalstromstaerkeold == 19) echo "selected" ?> value="19">19</option>
							<option <?php if($maximalstromstaerkeold == 20) echo "selected" ?> value="20">20</option>
							<option <?php if($maximalstromstaerkeold == 21) echo "selected" ?> value="21">21</option>
							<option <?php if($maximalstromstaerkeold == 22) echo "selected" ?> value="22">22</option>
							<option <?php if($maximalstromstaerkeold == 23) echo "selected" ?> value="23">23</option>
							<option <?php if($maximalstromstaerkeold == 24) echo "selected" ?> value="24">24</option>
							<option <?php if($maximalstromstaerkeold == 25) echo "selected" ?> value="25">25</option>
							<option <?php if($maximalstromstaerkeold == 26) echo "selected" ?> value="26">26</option>
							<option <?php if($maximalstromstaerkeold == 27) echo "selected" ?> value="27">27</option>
							<option <?php if($maximalstromstaerkeold == 28) echo "selected" ?> value="28">28</option>
							<option <?php if($maximalstromstaerkeold == 29) echo "selected" ?> value="29">29</option>
							<option <?php if($maximalstromstaerkeold == 30) echo "selected" ?> value="30">30</option>
							<option <?php if($maximalstromstaerkeold == 31) echo "selected" ?> value="31">31</option>
							<option <?php if($maximalstromstaerkeold == 32) echo "selected" ?> value="32">32</option>
						</select>
					</div>
					<div class="row" style="background-color:#befebe">
						Gibt an mit wieviel Ampere maximal geladen wird.
					</div>

					<div class="row" style="background-color:#befebe">
						<b><label for="minnurpvsoclp1">Minimal SoC fuer den Nur PV Laden Modus:</label></b>
						<select name="minnurpvsoclp1" id="minnurpvsoclp1">
							<option <?php if($minnurpvsoclp1old == 0) echo "selected" ?> value="0">0</option>
							<option <?php if($minnurpvsoclp1old == 5) echo "selected" ?> value="5">5</option>
							<option <?php if($minnurpvsoclp1old == 10) echo "selected" ?> value="10">10</option>
							<option <?php if($minnurpvsoclp1old == 15) echo "selected" ?> value="15">15</option>
							<option <?php if($minnurpvsoclp1old == 20) echo "selected" ?> value="20">20</option>
							<option <?php if($minnurpvsoclp1old == 25) echo "selected" ?> value="25">25</option>
							<option <?php if($minnurpvsoclp1old == 30) echo "selected" ?> value="30">30</option>
							<option <?php if($minnurpvsoclp1old == 35) echo "selected" ?> value="35">35</option>
							<option <?php if($minnurpvsoclp1old == 40) echo "selected" ?> value="40">40</option>
							<option <?php if($minnurpvsoclp1old == 45) echo "selected" ?> value="45">45</option>
							<option <?php if($minnurpvsoclp1old == 50) echo "selected" ?> value="50">50</option>
							<option <?php if($minnurpvsoclp1old == 55) echo "selected" ?> value="55">55</option>
							<option <?php if($minnurpvsoclp1old == 60) echo "selected" ?> value="60">60</option>
							<option <?php if($minnurpvsoclp1old == 65) echo "selected" ?> value="65">65</option>
							<option <?php if($minnurpvsoclp1old == 70) echo "selected" ?> value="70">70</option>
							<option <?php if($minnurpvsoclp1old == 75) echo "selected" ?> value="75">75</option>
							<option <?php if($minnurpvsoclp1old == 80) echo "selected" ?> value="80">80</option>
						</select>
					</div>
					<div class="row" style="background-color:#befebe">
						Definiert einen Mindest-SoC-Wert (EV) bis zu welchem im "Nur PV" Modus immer geladen wird, auch, wenn keine PV Leistung zur Verfügung steht.<br>
						Ist nur aktiv, wenn nur ein Ladepunkt konfiguriert ist!
					</div>

					<div class="row" style="background-color:#befebe">
						<b><label for="maxnurpvsoclp1">Maximal SoC fuer den Nur PV Laden Modus:</label></b>
						<select name="maxnurpvsoclp1" id="maxnurpvsoclp1">
							<option <?php if($maxnurpvsoclp1old == 50) echo "selected" ?> value="50">50</option>
							<option <?php if($maxnurpvsoclp1old == 55) echo "selected" ?> value="55">55</option>
							<option <?php if($maxnurpvsoclp1old == 60) echo "selected" ?> value="60">60</option>
							<option <?php if($maxnurpvsoclp1old == 65) echo "selected" ?> value="65">65</option>
							<option <?php if($maxnurpvsoclp1old == 70) echo "selected" ?> value="70">70</option>
							<option <?php if($maxnurpvsoclp1old == 75) echo "selected" ?> value="75">75</option>
							<option <?php if($maxnurpvsoclp1old == 80) echo "selected" ?> value="80">80</option>
							<option <?php if($maxnurpvsoclp1old == 85) echo "selected" ?> value="85">85</option>
							<option <?php if($maxnurpvsoclp1old == 90) echo "selected" ?> value="90">90</option>
							<option <?php if($maxnurpvsoclp1old == 95) echo "selected" ?> value="95">95</option>
							<option <?php if($maxnurpvsoclp1old == 100) echo "selected" ?> value="100">100</option>
							<option <?php if($maxnurpvsoclp1old == 101) echo "selected" ?> value="101">Deaktiviert</option>

						</select>
					</div>
					<div class="row" style="background-color:#befebe">
						Definiert einen Maximal-SoC-Wert bis zu welchem im "Nur PV" Modus geladen wird.<br>
						Ist nur aktiv, wenn nur ein Ladepunkt konfiguriert ist!
					</div>
					<div class="row" style="background-color:#befebe">
						<b><label for="minnurpvsocll">Stromstärke fuer den Nur PV Laden Modus wenn Mindest SoC noch nicht erreicht:</label></b>
						<select name="minnurpvsocll" id="minnurpvsocll">
							<option <?php if($minnurpvsocllold == 6) echo "selected" ?> value="6">6</option>
							<option <?php if($minnurpvsocllold == 7) echo "selected" ?> value="7">7</option>
							<option <?php if($minnurpvsocllold == 8) echo "selected" ?> value="8">8</option>
							<option <?php if($minnurpvsocllold == 9) echo "selected" ?> value="9">9</option>
							<option <?php if($minnurpvsocllold == 10) echo "selected" ?> value="10">10</option>
							<option <?php if($minnurpvsocllold == 11) echo "selected" ?> value="11">11</option>
							<option <?php if($minnurpvsocllold == 12) echo "selected" ?> value="12">12</option>
							<option <?php if($minnurpvsocllold == 13) echo "selected" ?> value="13">13</option>
							<option <?php if($minnurpvsocllold == 14) echo "selected" ?> value="14">14</option>
							<option <?php if($minnurpvsocllold == 15) echo "selected" ?> value="15">15</option>
							<option <?php if($minnurpvsocllold == 16) echo "selected" ?> value="16">16</option>
							<option <?php if($minnurpvsocllold == 17) echo "selected" ?> value="17">17</option>
							<option <?php if($minnurpvsocllold == 18) echo "selected" ?> value="18">18</option>
							<option <?php if($minnurpvsocllold == 19) echo "selected" ?> value="19">19</option>
							<option <?php if($minnurpvsocllold == 20) echo "selected" ?> value="20">20</option>
							<option <?php if($minnurpvsocllold == 21) echo "selected" ?> value="21">21</option>
							<option <?php if($minnurpvsocllold == 22) echo "selected" ?> value="22">22</option>
							<option <?php if($minnurpvsocllold == 23) echo "selected" ?> value="23">23</option>
							<option <?php if($minnurpvsocllold == 24) echo "selected" ?> value="24">24</option>
							<option <?php if($minnurpvsocllold == 25) echo "selected" ?> value="25">25</option>
							<option <?php if($minnurpvsocllold == 26) echo "selected" ?> value="26">26</option>
							<option <?php if($minnurpvsocllold == 27) echo "selected" ?> value="27">27</option>
							<option <?php if($minnurpvsocllold == 28) echo "selected" ?> value="28">28</option>
							<option <?php if($minnurpvsocllold == 29) echo "selected" ?> value="29">29</option>
							<option <?php if($minnurpvsocllold == 30) echo "selected" ?> value="30">30</option>
							<option <?php if($minnurpvsocllold == 31) echo "selected" ?> value="31">31</option>
							<option <?php if($minnurpvsocllold == 32) echo "selected" ?> value="32">32</option>
						</select>
					</div>
					<div class="row" style="background-color:#befebe">
						Definiert die Ladeleistung, wenn Mindest-SoC im "Nur PV Laden" Modus noch nicht erreicht ist.<br>
						Ist nur aktiv, wenn nur ein Ladepunkt konfiguriert ist!
					</div>

					<div class="row" style="background-color:#befebe">
						<b><label for="pvbezugeinspeisung">PV Lademodus:</label></b>
						<select name="pvbezugeinspeisung" id="pvbezugeinspeisung">
							<option <?php if($pvbezugeinspeisungold == 0) echo "selected" ?> value="0">Einspeisung</option>
							<option <?php if($pvbezugeinspeisungold == 1) echo "selected" ?> value="1">Bezug</option>
							<option <?php if($pvbezugeinspeisungold == 2) echo "selected" ?> value="2">Manueller Offset</option>
						</select>
					</div>
					<div class="row" style="background-color:#befebe">
						Definiert die Regelung des PV Modus. Bei Einspeisung wird von 0-230W Einspeisung geregelt und bei Bezug von 230W Bezug bis 0W.<br>
						Die Werte sind beispielhaft für einphasiges Laden und definieren die Schwellen für das Hoch- und Runterregeln des Ladestroms.
					</div>

					<div class="row" style="background-color:#befebe">
						<b><label for="offsetpv">Manuelles Offset in Watt:</label></b>
						<input type="text" name="offsetpv" id="offsetpv" value="<?php echo $offsetpvold ?>">
					</div>
					<div class="row" style="background-color:#befebe">
						Manuelles Offset in Watt für die PV Regelmodi zum Einbau eines zusätzlichen Regelpuffers. Verschiebt den Nullpunkt der Regelung. <br>
						Bei „PV-Lademodus“ muss „Manueller Offset" aktiviert sein.<br>
						Erlaubte Werte: Ganzzahl in Watt, Minus als Vorzeichen, z.B.: -200, 200, 356, usw.<br>
						z.B.: bei "200" wird von 200W-430W Einspeisung geregelt, anstatt von 0-230W wie beim Modus „Einspeisung". Negative Werte entsprechend in die Richtung „Bezug“.
					</div>

					<div id="speicherpvrangdiv">
							<div class="row" style="background-color:#fcbe1e">
								<b>Speicherladeoptionen</b>
							</div>
							<div class="row" style="background-color:#fcbe1e">
								<b><label for="speicherpveinbeziehen">Speicherbeachtung PV Lademodus:</label></b>
								<select name="speicherpveinbeziehen" id="speicherpveinbeziehen">
									<option <?php if($speicherpveinbeziehenold == 0) echo "selected" ?> value="0">Speicher hat Vorrang</option>
									<option <?php if($speicherpveinbeziehenold == 1) echo "selected" ?> value="1">EV hat Vorrang</option>
								</select><br>
								<b><label for="speicherpveinbeziehen">Auf der Hauptseite anzeigen:</label></b>
								<select name="speicherpvui" id="speicherpvui">
									<option <?php if($speicherpvuiold == 0) echo "selected" ?> value="0">Nein</option>
									<option <?php if($speicherpvuiold == 1) echo "selected" ?> value="1">Ja</option>
								</select>
							</div>
							<div class="row" style="background-color:#fcbe1e">
								Beeinflusst die Regelung des PV Modus in Verbindung mit einem Speicher.<br>
								Bei der Option "Speicher hat Vorrang" wird die EV Ladung erst gestartet, wenn der Speicher mit seiner maximalen Leistung lädt und der eingestellte Mindestüberschuss erreicht ist.<br>
								Bei der Option "EV hat Vorrang" wird die Speicherladeleistung mit in den verfügbaren Überschuss eingerechnet, es ist jedoch möglich, eine Mindestladung zu garantieren.
							</div>
							<div id="speicherevvdiv">
								<div class="row" style="background-color:#fcbe1e">
									<b><label for="speichermaxwatt">Mindestwatt Speicher:</label></b>
									<input type="text" name="speichermaxwatt" id="speichermaxwatt" value="<?php echo $speichermaxwattold ?>">
								</div>
								<div class="row" style="background-color:#fcbe1e">
									Definiert einen Wert, der trotz Vorrang des EV immer als Ladeleistung für den Speicher vorgehalten wird. Verfügbarer Überschuss über diesem Wert wird der EV Ladung zugerechnet.
								</div>
							</div>
							<div class="row" style="background-color:#fcbe1e">
								<b>Speicherentladeoptionen</b>
							</div>	<div class="row" style="background-color:#fcbe1e">
								<b><label for="speichersocnurpv">Speicher Entlade SoC NurPV:</label></b>
								<input type="text" name="speichersocnurpv" id="speichersocnurpv" value="<?php echo $speichersocnurpvold ?>">
							</div>
							<div class="row" style="background-color:#fcbe1e">
								<b><label for="speicherwattnurpv">Speicher Entlade Watt:</label></b>
								<input type="text" name="speicherwattnurpv" id="speicherwattnurpv" value="<?php echo $speicherwattnurpvold ?>">
							</div>
							<div class="row" style="background-color:#fcbe1e">
								Definiert einen SoC bis zu dem bei laufender „Nur PV“ Ladung der Speicher mit xxxx(W) Leistung entladen wird.<br>
								Zum Deaktivieren dieser Funktion (Speicher soll nicht entladen werden) den SoC auf 100 setzen.
							</div>
							<div class="row" style="background-color:#fcbe1e">
								<b><label for="speichersocminpv">Speicher Entlade SoC Min + PV:</label></b>
								<input type="text" name="speichersocminpv" id="speichersocminpv" value="<?php echo $speichersocminpvold ?>">
							</div>
							<div class="row" style="background-color:#fcbe1e">
								Im "Min + PV" Modus wird die Ladung erst gestartet, wenn der SoC über dem eingestellten Wert liegt.<br>
								Zum Deaktivieren der Funktion den Wert auf 0 setzen.
							</div>
							<div class="row" style="background-color:#fcbe1e">
								<b><label for="speichersochystminpv">Speicher Entlade SoC Min + PV Hysterese:</label></b>
								<input type="text" name="speichersochystminpv" id="speichersochystminpv" value="<?php echo $speichersochystminpvold ?>">
							</div>
							<div class="row" style="background-color:#fcbe1e">
								Die Hysterese legt fest ab welchem SoC bei Unterschreitung die Ladung wieder beendet wird.<br>
								Zum Deaktivieren der Funktion den Wert auf 0 setzen.
							</div>
					</div>
					<input type="hidden" name="speicherpvrang" id="speicherpvrang" value="<?php echo trim($speichervorhanden); ?>">
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
					<div class="row" style="background-color:#befebe">
						<b><label for="adaptpv">Adaptives Nur PV Laden:</label></b>
						<select name="adaptpv" id="adaptpv">
							<option <?php if($adaptpvold == 0) echo "selected" ?> value="0">Aus</option>
							<option <?php if($adaptpvold == 1) echo "selected" ?> value="1">An</option>
						</select>
					</div>
					<div class="row" style="background-color:#befebe">
						Beeinflusst die Regelung des "Nur PV" Modus, wenn folgende Bedingungen erfüllt sind:
						<ul>
							<li>- Laden im "Nur PV" Modus</li>
							<li>- zwei EVs laden gleichzeitig</li>
							<li>- für beide ist ein SoC verfügbar</li>
							<li>- beide EVs laden mit der selben Anzahl Phasen</li>
						</ul>
					</div>
					<div id="adaptpvdiv">
						<div class="row" style="background-color:#befebe">
							<b><label for="adaptfaktor">Faktor:</label></b>
							<input type="text" name="adaptfaktor" id="adaptfaktor" value="<?php echo $adaptfaktorold ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Defniert den Faktor zur Berechnung des Ladestroms. Herangezogen wird die Differenz der beiden SoC Werte. Für jeden Faktor Wert wird der Ladestrom um ein Ampere gesenkt, bzw. erhöht.<br>
							Beispiel:<br>
							Zur verfügung stehende Ladeleistung 16A, Faktor 5, SoC EV 1 69 %, SoC EV 2 33 %<br>
							Die Differenz beträgt 36 %, geteilt durch Faktor 5 ergibt den Wert 7.<br>
							Nun wird EV 1 mit 9A geladen (16A - 7A) und EV 2 mit 23A (16A + 7A).<br>
							Je näher die SoC Werte sind, je geringer wird der Unterschied.<br>
							Das leerere EV wird so bevorzugt.<br>
							Es wird maximal bis zur Minimal bzw. Maximalstromstärke angepasst.
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
					<div class="row" style="background-color:#befebe">
						<b><label for="nurpv70dynact">Regelziel 70% Grenze beim PV Laden:</label></b>
						<select name="nurpv70dynact" id="nurpv70dynact">
							<option <?php if($nurpv70dynactold == 0) echo "selected" ?> value="0">Aus</option>
							<option <?php if($nurpv70dynactold == 1) echo "selected" ?> value="1">An</option>
						</select>
					</div>
					<div class="row" style="background-color:#befebe">
							Wenn aktiviert wird im Nur PV Modus erst mit der Ladung begonnen wenn der eingestellte Wert erreicht ist.<br>Die Grenze gilt dann als Regelpunkt
					</div>
					<div id="70pvdiv">
						<div class="row" style="background-color:#befebe">
							<b><label for="nurpv70dynw">70% Grenze:</label></b>
							<input type="text" name="nurpv70dynw" id="nurpv70dynw" value="<?php echo $nurpv70dynwold ?>">
						</div>
						<div class="row" style="background-color:#befebe">
							Defniert den Wert in Watt für die 70% Grenze. Bei einer 9,9kWP PV Anlage macht hier z.B. 6900 Watt Sinn.<br>Der PV-Regler wird diesen Wert versuchen niemals zu überschreiten.<br>
						</div>
					</div>
					<script>
						$(function() {
							if($('#nurpv70dynact').val() == '1') {
								$('#70pvdiv').show();
							} else {
								$('#70pvdiv').hide();
							}
							$('#nurpv70dynact').change(function(){
								if($('#nurpv70dynact').val() == '1') {
									$('#70pvdiv').show();
								} else {
									$('#70pvdiv').hide();
								}
							});
						});
					</script>


					<button type="submit" class="btn btn-green">Save</button>
				</form>

				<div class="row justify-content-center">
					<div class="col text-center">
						Open Source made with love!<br>
						Jede Spende hilft die Weiterentwicklung von openWB vorranzutreiben<br>
						<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
							<input type="hidden" name="cmd" value="_s-xclick">
							<input type="hidden" name="hosted_button_id" value="2K8C4Y2JTGH7U">
							<input type="image" src="./img/btn_donate_SM.gif" name="submit" alt="Jetzt einfach, schnell und sicher online bezahlen – mit PayPal.">
							<img alt="" src="./img/pixel.gif" width="1" height="1">
						</form>
					</div>
				</div>
			</div>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Einstellungen/PV-Ladeeinstellungen</small>
			</div>
		</footer>


		<script type="text/javascript">

			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navPVLadeeinstellungen_alt').addClass('disabled');
			});

		</script>

	</body>
</html>
