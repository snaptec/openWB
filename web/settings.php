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
	<!-- Font Awesome -->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.1.0/css/font-awesome.min.css">
	<!-- Elegant Icons -->
	<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
	<!-- Main style -->
	<link rel="stylesheet" type="text/css" href="css/cardio.css">
</head>
<body>
<?php


$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {


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
	if(strpos($line, "minnurpvsocll=") !== false) {
		list(, $minnurpvsocllold) = explode("=", $line);
	}
	if(strpos($line, "minnurpvsoclp1=") !== false) {
		list(, $minnurpvsoclp1old) = explode("=", $line);
	}
	if(strpos($line, "maxnurpvsoclp1=") !== false) {
		list(, $maxnurpvsoclp1old) = explode("=", $line);
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
	if(strpos($line, "loadsharinglp12=") !== false) {
		list(, $loadsharinglp12old) = explode("=", $line);
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
    <li><a data-toggle="tab" href="./index.php">Zurueck</a></li>
    <li class="active"><a href="./settings.php">Ladeeinstellungen</a></li>
    <li><a href="./modulconfig.php">Modulkonfiguration</a></li>
    <li><a href="./misc.php">Misc</a></li>
  </ul><br><br>
 </div>

     
<form action="./tools/savemain.php" method="POST">

<div class="col-xs-1">
</div>
<div class="col-xs-10">
<div class="row">
	<b><label for="minimalstromstaerke">Minimalstromstärke in A:</label></b>
	<select type="text" name="minimalstromstaerke" id="minimalstromstaerke">
		<option <?php if($minimalstromstaerkeold == 6) echo selected ?> value="6">6</option>
		<option <?php if($minimalstromstaerkeold == 7) echo selected ?> value="7">7</option>
		<option <?php if($minimalstromstaerkeold == 8) echo selected ?> value="8">8</option>
		<option <?php if($minimalstromstaerkeold == 9) echo selected ?> value="9">9</option>
		<option <?php if($minimalstromstaerkeold == 10) echo selected ?> value="10">10</option>
	</select><br>
</div>
<div class="row">
	Gibt an mit wieviel Ampere je Phase im Sofort Laden Modus mindestens geladen wird.<br><br>
</div>
<div class="row">
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
<div class="row">
	Gibt an mit wieviel Ampere Maximal geladen wird.<br><br>
</div>

<div id="durchslp1">
	<div class="row">
		<hr>
		<b><label for="durchslp1">Durchschnittsverbrauch deines Elektroautos in kWh an Ladepunkt 1:</label></b>
		<input type="text" name="durchslp1" id="durchslp1" value="<?php echo $durchslp1old ?>"><br>
	</div>
	<div class="row">
	Gültige Werte xx.xx, z.B. 14.5 <br> Dient zur Berechnung der geladenen Strecke.<br><br>
	</div>
</div>
<div id="durchslp2">
	<div class="row">
		<b><label for="durchslp2">Durchschnittsverbrauch deines Elektroautos in kWh an Ladepunkt 2:</label></b>
		<input type="text" name="durchslp2" id="durchslp2" value="<?php echo $durchslp2old ?>"><br>
	</div>
	<div class="row">
	Gültige Werte xx.xx, z.B. 14.5 <br> Dient zur Berechnung der geladenen Strecke.<br><br>
	</div>
</div>
<div id="durchslp3">
	<div class="row">
		<b><label for="durchslp3">Durchschnittsverbrauch deines Elektroautos  in kWh an Ladepunkt 3:</label></b>
		<input type="text" name="durchslp3" id="durchslp3" value="<?php echo $durchslp3old ?>"><br>
	</div>
	<div class="row">
	Gültige Werte xx.xx, z.B. 14.5 <br> Dient zur Berechnung der geladenen Strecke.<br><br>
	</div>
</div>
<div class="row"><hr>
	<h3>Nachtlademodus</h3>
</div>


<div class="row">
	<b><label for="nachtladen">Nachtladen Ladepunkt 1:</label></b>
	<select type="text" name="nachtladen" id="nachtladen">
		<option <?php if($nachtladenold == 0) echo selected ?> value="0">Aus</option>
		<option <?php if($nachtladenold == 1) echo selected ?> value="1">An</option>
	</select>
</div>
<div class="row">
	Definiert ob Nachts geladen werden soll. Ist auch bei Lademodus "Stop" aktiv!<br><br>
</div>
<div id="nachtladenaus">
	<br>
</div>
<div id="nachtladenan">
	<div class="row">
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
	<div class="row">
		Ampere mit der nachts geladen werden soll<br><br>
	</div>
	<div class="row">
		<b><label for="nachtladenabuhr">Nachtladen Uhrzeit ab:</label></b>
	       	<select type="text" name="nachtladenabuhr" id="nachtladenabuhr">
 			<option <?php if($nachtladenabuhrold == 17) echo selected ?> value="17">17</option>
 			<option <?php if($nachtladenabuhrold == 18) echo selected ?> value="18">18</option>
 			<option <?php if($nachtladenabuhrold == 19) echo selected ?> value="19">19</option>
 			<option <?php if($nachtladenabuhrold == 20) echo selected ?> value="20">20</option>
 			<option <?php if($nachtladenabuhrold == 21) echo selected ?> value="21">21</option>
 			<option <?php if($nachtladenabuhrold == 22) echo selected ?> value="22">22</option>
			<option <?php if($nachtladenabuhrold == 23) echo selected ?> value="23">23</option>
		</select><br>
	</div>
	<div class="row">
		Ab wann Abends geladen werden soll<br><br>
	</div>
	<div class="row">
		<b><label for="nachtladenbisuhr">Nachtladen Uhrzeit bis:</label></b>
	       	<select type="text" name="nachtladenbisuhr" id="nachtladenbisuhr">
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
	<div class="row">
		Bis wann morgens geladen werden soll<br><br>
	</div>
	<div class="row">
		<b><label for="nachtsoc">Nacht SOC Sonntag bis Donnerstag:</label></b>
		<input type="text" name="nachtsoc" id="nachtsoc" value="<?php echo $nachtsocold ?>"><br>
	</div>
	<div class="row">
		Gültiger Wert 1-99. Wenn SOC Modul vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br><br>
	</div>
	<div class="row">
		<b><label for="nachtsoc1">Nacht SOC Freitag bis Sonntag:</label></b>
		<input type="text" name="nachtsoc1" id="nachtsoc1" value="<?php echo $nachtsoc1old ?>"><br>
	</div>
	<div class="row">
		Gültiger Wert 1-99. Wenn SOC Modul vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br><br>
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

<div id="nachtls1div">
<div class="row">
	<b><label for="nachtladens1">Nachtladen Ladepunkt 2:</label></b>
	<select type="text" name="nachtladens1" id="nachtladens1">
		<option <?php if($nachtladens1old == 0) echo selected ?> value="0">Aus</option>
		<option <?php if($nachtladens1old == 1) echo selected ?> value="1">An</option>
	</select>
</div>
<div class="row">
	Definiert ob Nachts geladen werden soll. Ist auch bei Lademodus "Stop" aktiv!<br><br>
</div>
<div id="nachtladenauss1">
	<br>
</div>
<div id="nachtladenans1">
	<div class="row">
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
	<div class="row">
		Ampere mit der nachts geladen werden soll<br><br>
	</div>
	<div class="row">
		<b><label for="nachtladenabuhrs1">Nachtladen Uhrzeit ab:</label></b>
	       	<select type="text" name="nachtladenabuhrs1" id="nachtladenabuhrs1">
 			<option <?php if($nachtladenabuhrs1old == 17) echo selected ?> value="17">17</option>
 			<option <?php if($nachtladenabuhrs1old == 18) echo selected ?> value="18">18</option>
 			<option <?php if($nachtladenabuhrs1old == 19) echo selected ?> value="19">19</option>
 			<option <?php if($nachtladenabuhrs1old == 20) echo selected ?> value="20">20</option>
 			<option <?php if($nachtladenabuhrs1old == 21) echo selected ?> value="21">21</option>
 			<option <?php if($nachtladenabuhrs1old == 22) echo selected ?> value="22">22</option>
			<option <?php if($nachtladenabuhrs1old == 23) echo selected ?> value="23">23</option>
		</select><br>
	</div>
	<div class="row">
		Ab wann Abends geladen werden soll<br><br>
	</div>
	<div class="row">
		<b><label for="nachtladenbisuhrs1">Nachtladen Uhrzeit bis:</label></b>
	       	<select type="text" name="nachtladenbisuhrs1" id="nachtladenbisuhrs1">
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
	<div class="row">
		Bis wann morgens geladen werden soll an Ladepunkt 2<br><br>
	</div>
	<div class="row">
		<b><label for="nachtsocs1">Nacht SOC Sonntag bis Donnerstag:</label></b>
		<input type="text" name="nachtsocs1" id="nachtsocs1" value="<?php echo $nachtsocs1old ?>"><br>
	</div>
	<div class="row">
		Gültiger Wert 1-99. Wenn SOC Modul vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br><br>
	</div>
	<div class="row">
		<b><label for="nachtsoc1s1">Nacht SOC Freitag bis Sonntag:</label></b>
		<input type="text" name="nachtsoc1s1" id="nachtsoc1s1" value="<?php echo $nachtsoc1s1old ?>"><br>
	</div>
	<div class="row">
		Gültiger Wert 1-99. Wenn SOC Modul Ladepunkt 2 vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br><br>
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
	<h3>PV Regelung</h3>
</div>
<div class="row">
	Die Kombination aus Mindestüberschuss und Abschaltüberschuss sollte sinnvoll gewählt werden.<br>
	Ansonsten wird im 10 Sekunden Takt die Ladung gestartet und gestoppt.<br>
	Es macht z.B. 1320 Watt mindestuberschuss und 900 Watt abschaltuberschuss Sinn<br>
</div>
<div class="row">
	<b><label for="mindestuberschuss">Mindestüberschuss:</label></b>
	<input type="text" name="mindestuberschuss" id="mindestuberschuss" value="<?php echo $mindestuberschussold ?>"><br>
</div>
<div class="row">
	Gültige Werte 0-9999. Mindestüberschuss in Watt bevor im Lademodus "Nur PV" die Ladung beginnt.<br> Soll wenig bis kein Netzbezug vorhanden sein macht ein Wert um 1300-1600 Sinn.<br><br>
</div>
<div class="row">
	<b><label for="abschaltuberschuss">Abschaltüberschuss:</label></b>
	<input type="text" name="abschaltuberschuss" id="abschaltuberschuss" value="<?php echo $abschaltuberschussold ?>"><br>
</div>
<div class="row">
	Gültige Werte 0-9999. Ab wieviel Watt Bezug abgeschaltet werden soll.<br>
Zunächst wird in jedem Zyklus die Ladeleistung Stufenweise bis auf Minimalstromstaerke reduziert. Danach greift die Abschaltung.<br>
Der Wert gibt an wieviel Watt insgesamt bezogen werden bevor abgeschaltet wird.<br><br>


</div>
<div class="row">
	<b><label for="abschaltverzoegerung">Abschaltverzögerung:</label></b>
	<input type="text" name="abschaltverzoegerung" id="abschaltverzoegerung" value="<?php echo $abschaltverzoegerungold ?>"><br>
</div>

<div class="row">
Gültige Werte Zeit in Sekunden in 10ner Schritten. Die Verzögerung gibt an um wieviel Sekunden (0,10,20,30,...300,310,320, usw.) im Nur PV Modus die Abschaltung hinausgezögert wird.
<br> Gibt man hier 40 Sekunden an, muss über die gesamte Spanne von 40 Sekunden der Bezug größer als der Abschaltüberschuss sein. <br> Ist der Bezug nach 20 Sekunden kurzzeitig kleiner als der Abschaltüberschuss beginnen die 40 Sekunden erneut.<br>
</div><br>
<div class="row">
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

<div class="row">
Definiert die Minimal erlaubte Stromstaerke in A je Phase fuer den Min + PV Laden Modus.<br>
</div>
<div class="row">
	<b><label for="minimalapv">Minimalstromstärke fuer den Nur PV Laden Modus:</label></b>
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

<div class="row">
Definiert die Minimal erlaubte Stromstaerke in A je Phase fuer den Nur PV Laden Modus.<br>
</div><br>
<div class="row">
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
	<div class="row">
	Definiert einen Mindest SoC Wert bis zu welchem im Nur PV Modus immer geladen wird - auch wenn keine PV Leistung zur Verfügung steht.<br> Ist nur aktiv wenn nur ein Ladepunkt konfiguriert ist!
	</div><br>


<div class="row">
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
	<div class="row">
	Definiert einen Maximal SoC Wert bis zu welchem im Nur PV Modus geladen wird.<br> Ist nur aktiv wenn nur ein Ladepunkt konfiguriert ist!
	</div>
<br>
<div class="row">
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
	<div class="row">
	Definiert die Ladeleistung wenn Mindest SoC im Nur PV Laden Modus noch nicht erreicht ist.<br> Ist nur aktiv wenn nur ein Ladepunkt konfiguriert ist!
	</div>



<br><br>
	<div class="row">
		<b><label for="pvbezugeinspeisung">PV Lademodus:</label></b>
	       	<select type="text" name="pvbezugeinspeisung" id="pvbezugeinspeisung">
 			<option <?php if($pvbezugeinspeisungold == 0) echo selected ?> value="0">Einspeisung</option>
  			<option <?php if($pvbezugeinspeisungold == 1) echo selected ?> value="1">Bezug</option>
		</select><br>

	</div>
	<div class="row">
		Definiert die Regelung des PV Mdous. Bei Einspeisung wird von 0-230W Einspeisung geregelt und bei Bezug von 230W Bezug bis 0W. Die Werte sind beispielhaft fuer einphasiges Laden und definieren die Schwellen fuer das Hoch und Runterregeln des Ladestroms.<br><br>
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
	Wenn Ladepunkt 1 und Ladepunkt 2 sich eine Zuleitung teilen diese Option aktivieren. Bei der OpenWB Duo muss diese Option aktiviert werden!<br>
	Sie stellt in jedem Lademodus sicher das nicht mehr als 32A je Phase in der Summe von LP 1 und LP 2 genutzt werden.<br>
	Der richtige Anschluss ist zu gewährleisten.<br>
	Ladepunkt 1: <br>
	<p style="text-indent :2em;" >Phase 1 Zuleitung = Phase 1 Ladepunkt 1</p>
	<p style="text-indent :2em;" >Phase 2 Zuleitung = Phase 2 Ladepunkt 1</p>
	<p style="text-indent :2em;" >Phase 3 Zuleitung = Phase 3 Ladepunkt 1</p>
	Ladepunkt 2: <br>
	<p style="text-indent :2em;" >Phase 1 Zuleitung = Phase 2 Ladepunkt 2</p>
	<p style="text-indent :2em;" >Phase 2 Zuleitung = Phase 3 Ladepunkt 2</p>
	<p style="text-indent :2em;" >Phase 3 Zuleitung = Phase 1 Ladepunkt 2</p>
	Durch das drehen der Phasen ist sichergestellt das 2 einphasige Autos mit voller Geschwindigkeit Laden können.<br>

</div>

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
 			<option <?php if($pushbstoptlold == 0) echo selected ?> value="0">Nein</option>
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

