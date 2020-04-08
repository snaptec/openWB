<!DOCTYPE html>
<html lang="de">

<head>
	<!-- dark19_01 theme for openWB -->
	<!-- 2020 Michael Ortenstein -->

	<title>openWB</title>
	<?php include ("values.php");?>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="openWB">
	<meta name="apple-mobile-web-app-status-bar-style" content="default">
	<link rel="apple-touch-startup-image" href="/openWB/web/img/favicons/splash1125x2436w.png"  />
	<link rel="apple-touch-startup-image" media="(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)" href="img/favicons/splash1125x2436w.png">
	<meta name="apple-mobile-web-app-title" content="openWB">

	<meta name="description" content="openWB">
	<meta name="keywords" content="openWB">
	<meta name="author" content="Michael Ortenstein">
	<link rel="apple-touch-icon" sizes="72x72" href="img/favicons/apple-icon-72x72.png">
	<link rel="apple-touch-icon" sizes="76x76" href="img/favicons/apple-icon-76x76.png">
	<link rel="apple-touch-icon" sizes="114x114" href="img/favicons/apple-icon-114x114.png">
	<link rel="apple-touch-icon" sizes="120x120" href="img/favicons/apple-icon-120x120.png">
	<link rel="apple-touch-icon" sizes="144x144" href="img/favicons/apple-icon-144x144.png">
	<link rel="apple-touch-icon" sizes="152x152" href="img/favicons/apple-icon-152x152.png">
	<link rel="apple-touch-icon" sizes="180x180" href="img/favicons/apple-icon-180x180.png">
	<link rel="icon" type="image/png" sizes="192x192"  href="img/favicons/android-icon-192x192.png">
	<link rel="icon" type="image/png" sizes="32x32" href="img/favicons/favicon-32x32.png">
	<link rel="icon" type="image/png" sizes="96x96" href="img/favicons/favicon-96x96.png">
	<link rel="icon" type="image/png" sizes="16x16" href="img/favicons/favicon-16x16.png">
	<meta name="msapplication-TileColor" content="#ffffff">
	<meta name="msapplication-TileImage" content="/ms-icon-144x144.png">
	<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
	<link rel="manifest" href="manifest.json">
	<link rel="shortcut icon" href="img/favicons/favicon.ico">
	<!-- <link rel="apple-touch-startup-image" href="img/loader.gif"> -->
	<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">

	<!-- Bootstrap -->
	<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
	<!-- Normalize -->
	<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
	<!-- Font Awesome, all styles -->
  	<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">

    <!-- include special Theme style -->
	<link rel="stylesheet" type="text/css" href="themes/<?php echo $_COOKIE['openWBTheme'];?>/style.css?ver=20200405-b">

	<!-- important scripts to be loaded -->
	<script src="js/jquery-3.4.1.min.js"></script>
	<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
</head>

<body>

	<div class="container">

		<div class="row">
			<div class="col gradient">
				<h1 class="my-3 font-weight-bold text-center">openWB Charge Controller</h1>
			</div>
		</div>

		<div class="row verySmallTextSize text-black bg-darkgrey">
			<div id="date" class="col text-left">
				&nbsp;
			</div>
			<div class="col-5 cursor-pointer regularTextSize font-weight-bold text-center text-red">
				<span id="chargeModeSelect">
					>> Lademodus <<
				</span>
			</div>
			<div id="time" class="col text-right">
				&nbsp;
			</div>
		</div>

		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="col-sm bg-lightgreen">
				PV: <span id="pvleistung">0 W</span><span id="pvdailyyield"></span>
			</div>
			<div id="evudiv" class="col-sm bg-rose">
				EVU: <span id="bezug">0 W</span>
			</div>
		</div>

<?php
	echo '<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">';

	if ( $hausverbrauchstatold == 1 ) {
echo <<<HAUSVERBRAUCHDIV
		<div class="col-sm bg-apricot">
			Hausverbrauch: <span id="hausverbrauch">0 W</span>
		</div>
HAUSVERBRAUCHDIV;
	}
	echo '<div class="col-sm bg-lightgrey">';
	echo 'Ladeleistung: <span id="powerAllLp">lade Daten</span>';
	echo '    </div>';
	echo '</div>';
	// if speichermodul is not "none", show the info
	if ( strcmp(trim($speicherstatold),"none") != 0 ) {
echo <<<SPEICHERDIV
<div id="speicher" class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
	<div class="col-sm bg-orange">
		Speicher: <span id="speicherleistung">0 W</span><span id="speichersoc"></span>
	</div>
</div>
SPEICHERDIV;
	}  // end if speichervorhanden

	if ( ($hook1_aktivold == 1 || $hook2_aktivold == 1 || $hook3_aktivold == 1) ) {
	// if hooks for external devices are configured, show div
		echo '<div id="webhooksdiv" class="row justify-content-center regularTextSize font-weight-bold text-center text-black bg-darkgrey">';
		// generate code for all configured hooks
		for($i=1; $i <= 3; $i++) {
			if (${"hook".$i."_aktivold"} == 1) {
				$divId = "hook".$i."div";
echo <<<EXTDEVICEDIVMIDDLE
	<div id="$divId" class="col-3 m-1">
		ext. Gerät $i
	</div>

EXTDEVICEDIVMIDDLE;
			}  // end if
		}  // end for
echo '</div>';
	}  // end if hook configured
?>

		<!-- interactive chart.js -->
		<!-- will be refreshed using MQTT (in live.js)-->
		<div class="row justify-content-center my-2" id="thegraph">
			<div class="col-sm-12 text-center" style="height: 350px;">
				<div id="waitforgraphloadingdiv">
					Graph lädt, bitte warten...
				</div>
				<canvas id="canvas"></canvas>
			</div>
			<div id="graphoptiondiv" class="hide">
				<br><br>
			</div>
		</div>

		<div class="row text-center bg-darkgrey">
			<div class="col">
				<span id="lastregelungaktiv" class="regularTextSize text-red animate-alertPulsation"></span>
			</div>
		</div>

		<!-- chargepoint info header -->
		<div class="row smallTextSize bg-darkgrey text-grey font-weight-bold text-center px-0 py-1 py-md-0">
			<div class="col-4">
				Ladepunkt
			</div>
			<div class="col-3">
				Ladeleistung
			</div>
			<div class="col-3">
				geladen
			</div>
			<div class="col-2">
				SoC
			</div>
		</div>

		<!-- chargepoint info data -->
		<?php
			// generate html code dynamically for all charging points
			for( $i = 1; $i <= 8; $i++) {
				if ( $isConfiguredLp[$i] == 0 ) {
					continue;  // skip if lp not configured
				}
				echo '<!-- data-row for charging Point '.$i.' -->'."\n";
				echo '        <div id="lp'.$i.'div" class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey">'."\n";
				echo '            <div class="col-4 px-0">'."\n";
				echo '                <span class="cursor-pointer lpEnableSpan" id="lpEnableSpanLp'.$i.'" lp="'.$i.'">'."\n";
				echo '                    <span class="fas fa-xs hide" id="lp'.$i.'AutolockConfigured"></span>'."\n"; // placeholder for autolock icons
				echo '                    <span class="nameLp'.$i.' font-weight-bold" id="nameLp'.$i.'">'.$settingsArray['lp'.$i.'name'].'</span>'."\n";
				echo '                </span>'."\n";
				echo '                <span class="fa fa-xs fa-plug text-white hide" id="plugstatlp'.$i.'"></span>'."\n";
				if ( $zielladenaktivlp1old == 1 ) {
				echo '                <span class="fa fa-xs fa-flag-checkered"></span>'."\n";
				}
				echo '                <span class="fa fa-xs fa-moon hide" id="nachtladenaktivlp'.$i.'"></span>'."\n";
				echo '            </div>'."\n";
				echo '            <div class="col-3 px-0">'."\n";
				echo '                <span id="actualPowerLp'.$i.'">lade Daten</span>'."\n";
				echo '            </div>'."\n";
				echo '            <div class="col-3 px-0">'."\n";
				echo '                <span id="energyChargedLp'.$i.'">lade Daten</span><span id="kmChargedLp'.$i.'" consumption="0"></span>'."\n";
				echo '            </div>'."\n";
				// standard: soc not configured for charging point
				echo '            <div id="socNotConfiguredLp'.$i.'" class="col-2 px-0">'."\n";
				echo '              --'."\n";
				echo '            </div>'."\n";
				echo '            <div id="socConfiguredLp'.$i.'div" class="col-2 px-0 hide">'."\n";
				echo '                <span id="socLp'.$i.'"></span>'."\n";
				echo '            </div>'."\n";
				echo '        </div>'."\n\n";
				echo '        ';
			}
		?>

		<!-- removed to see if people miss it

		<div class="row justify-content-center">
			<div class="col-12">
				<hr color="white">
			</div>
		</div>

		<div class="row justify-content-center">
			<h3 class ="text-center font-weight-bold text-lightgrey">letztes zusammenhängendes Ladesegment</h3>
		</div>

		<div class="row justify-content-center regularTextSize">
			<div class="col-4">
				LP1 <span class="nameLp1"></span>
			</div>
			<div class="col-4" <?php if($isConfiguredLp[2] != 1) echo 'style="display: none;"' ?>>
				LP2 <span class="nameLp2"></span>
			</div>
			<div class="col-4 " <?php if($isConfiguredLp[3] != 1) echo 'style="display: none;"' ?>>
				LP3 <span class="nameLp3"></span>
			</div>
		</div>

		<div class="row justify-content-center regularTextSize">
			<div class="col-4">
				<span id="gelrlp1div"></span>
			</div>
			<div class="col-4" <?php if($isConfiguredLp[2] != 1) echo 'style="display: none;"' ?>>
				<span id="gelrlp2div"></span>
			</div>
			<div class="col-4" <?php if($isConfiguredLp[3] != 1) echo 'style="display: none;"' ?>>
				<span id="gelrlp3div"></span>
			</div>
		</div>

		<div class="row justify-content-center regularTextSize">
			<div class="col-4">
				<span id="aktgeladen1"></span>
			</div>
			<div class="col-4" <?php if($isConfiguredLp[2] != 1) echo 'style="display: none;"' ?>>
				<span id="aktgeladen2"></span>
			</div>
			<div class="col-4" <?php if($isConfiguredLp[3] != 1) echo 'style="display: none;"' ?>>
				<span id="aktgeladen3"></span>
			</div>
		</div>
-->

		<div id="targetChargingProgress" class="hide">
			<div class="row justify-content-center regularTextSize text-center">
				<div class="col-4" <?php if($lademstatold != 1) echo 'style="display: none;"' ?>>
					<progress id="prog1" value= "0" max=<?php echo $lademkwhold ?>></progress>
				</div>
				<div class="col-4" <?php if($lademstats1old != 1) echo 'style="display: none;"' ?>>
					<progress id="prog2" value= "0" max=<?php echo $lademkwhs1old ?>></progress>
				</div>
				<div class="col-4" <?php if($lademstats2old != 1) echo 'style="display: none;"' ?>>
					<progress id="prog3" value= "0" max=<?php echo $lademkwhs2old ?>></progress>
				</div>
			</div>

			<div class="row justify-content-center regularTextSize text-center">
				<div class="col-4" <?php if($lademstatold != 1) echo 'style="display: none;"' ?>>
					Restzeit <span id="restzeitlp1"></span>
				</div>
				<div class="col-4" <?php if($lademstats1old != 1) echo 'style="display: none;"' ?>>
					Restzeit <span id="restzeitlp2"></span>
				</div>
				<div class="col-4" <?php if($lademstats2old != 1) echo 'style="display: none;"' ?>>
					Restzeit <span id="restzeitlp3"></span>
				</div>
			</div>
		</div>

		<hr color="white">

		<!-- depending on charge mode show options -->
	    <form id="sofortladenEinstellungen" class="hide "name="sofortll" action="./tools/sofortll.php" method="POST">
		    <div id="awattardiv" class="hide"enabled="<?php echo $settingsArray["awattaraktiv"] ?>">
				<div class="row justify-content-center">
					<h3 class="font-weight-bold text-center text-lightgrey">Awattar</h3>
				</div>
				<div class="row justify-content-center">
					<div class="col-sm-12 text-center" style="height: 150px;">
						<canvas id="awattarcanvas"></canvas>
					</div>
				</div>
				<div class="row vaRow justify-content-center" id="sliderawattardiv">
					<div class="col-6 col-md-4">
						<input type="range" min="-8" max="12" step="0.10" name="awattar1s" id="awattar1s" class="custom-range">
					</div>
					<div class="col-sm-5 col-md-6 regularTextSize text-center">
						<label for="awattar1">Maximaler Preis: <span id="awattar1l"></span> Cent/kWh</label>
					</div>
					<script>
						var aslider1 = document.getElementById("awattar1s");
						var aoutput1 = document.getElementById("awattar1l");
						aoutput1.innerHTML = aslider1.value;
						aslider1.oninput = function() {
							aoutput1.innerHTML = this.value;
							AwattarMaxPriceClick();
						}
					</script>
				</div>

				<div class="row justify-content-center">
					<div class="col-12">
						<hr color="white">
					</div>
				</div>

			</div> <!--/ awattardiv -->

			<div class="row justify-content-center">
		   		<h3 class="font-weight-bold text-center text-lightgrey">Sofortladen Ladeziel-Einstellungen</h3>
		    </div>

	        <div class="row justify-content-center">
                <div class="col-4 regularTextSize text-center">
                    <label for="msmoduslp1"></label>
                    <select class="sofortladenLadezielSelektor" type="text" name="msmoduslp1" id="msmoduslp1">
                        <option <?php if($msmoduslp1old == 0) echo 'selected' ?> value="0">Aus</option>
                        <option <?php if($msmoduslp1old == 1) echo 'selected' ?> value="1">Lademenge</option>
                        <option <?php if($msmoduslp1old == 2) echo 'selected' ?> value="2">SoC</option>
                    </select>
                    <span id="msmodusmlp1" <?php if($msmoduslp1old != 1) echo 'style="display: none;"' ?>>
                        <br><br>
                        <label for="lademlp1">Lademenge</label>
                        <select type="text" name="lademlp1" id="lademlp1">
                        	<option <?php if($lademkwhold == 0) echo 'selected' ?> value="0">0</option>
                            <option <?php if($lademkwhold == 2) echo 'selected' ?> value="2">2</option>
                            <option <?php if($lademkwhold == 4) echo 'selected' ?> value="4">4</option>
                            <option <?php if($lademkwhold == 6) echo 'selected' ?> value="6">6</option>
                            <option <?php if($lademkwhold == 8) echo 'selected' ?> value="8">8</option>
                            <option <?php if($lademkwhold == 10) echo 'selected' ?> value="10">10</option>
                            <option <?php if($lademkwhold == 12) echo 'selected' ?> value="12">12</option>
                            <option <?php if($lademkwhold == 14) echo 'selected' ?> value="14">14</option>
                            <option <?php if($lademkwhold == 16) echo 'selected' ?> value="16">16</option>
                            <option <?php if($lademkwhold == 18) echo 'selected' ?> value="18">18</option>
                            <option <?php if($lademkwhold == 20) echo 'selected' ?> value="20">20</option>
                            <option <?php if($lademkwhold == 25) echo 'selected' ?> value="25">25</option>
                            <option <?php if($lademkwhold == 30) echo 'selected' ?> value="30">30</option>
                            <option <?php if($lademkwhold == 35) echo 'selected' ?> value="35">35</option>
                            <option <?php if($lademkwhold == 40) echo 'selected' ?> value="40">40</option>
                            <option <?php if($lademkwhold == 45) echo 'selected' ?> value="45">45</option>
                            <option <?php if($lademkwhold == 50) echo 'selected' ?> value="50">50</option>
                            <option <?php if($lademkwhold == 55) echo 'selected' ?> value="55">55</option>
                            <option <?php if($lademkwhold == 60) echo 'selected' ?> value="60">60</option>
                            <option <?php if($lademkwhold == 65) echo 'selected' ?> value="65">65</option>
                            <option <?php if($lademkwhold == 70) echo 'selected' ?> value="70">70</option>
                        </select> kWh
                        <br><br>
                        <button class="resetTargetChargingBtn" lp="1">Reset</button>
                    </span>
                    <span id="msmodusslp1" <?php if($msmoduslp1old != 2) echo 'style="display: none;"' ?>>
						<br><br>
                        <label for="sofortsoclp1">SoC</label>
                        <select type="text" name="sofortsoclp1" id="sofortsoclp1">
                        	<option <?php if($sofortsoclp1old == 10) echo 'selected' ?> value="10">10</option>
                            <option <?php if($sofortsoclp1old == 15) echo 'selected' ?> value="15">15</option>
                            <option <?php if($sofortsoclp1old == 20) echo 'selected' ?> value="20">20</option>
                            <option <?php if($sofortsoclp1old == 30) echo 'selected' ?> value="30">30</option>
                            <option <?php if($sofortsoclp1old == 40) echo 'selected' ?> value="40">40</option>
                            <option <?php if($sofortsoclp1old == 45) echo 'selected' ?> value="45">45</option>
                            <option <?php if($sofortsoclp1old == 50) echo 'selected' ?> value="50">50</option>
                            <option <?php if($sofortsoclp1old == 55) echo 'selected' ?> value="55">55</option>
                            <option <?php if($sofortsoclp1old == 60) echo 'selected' ?> value="60">60</option>
                            <option <?php if($sofortsoclp1old == 65) echo 'selected' ?> value="65">65</option>
                            <option <?php if($sofortsoclp1old == 70) echo 'selected' ?> value="70">70</option>
                            <option <?php if($sofortsoclp1old == 75) echo 'selected' ?> value="75">75</option>
                            <option <?php if($sofortsoclp1old == 80) echo 'selected' ?> value="80">80</option>
                            <option <?php if($sofortsoclp1old == 85) echo 'selected' ?> value="85">85</option>
                            <option <?php if($sofortsoclp1old == 90) echo 'selected' ?> value="90">90</option>
                            <option <?php if($sofortsoclp1old == 95) echo 'selected' ?> value="95">95</option>
                        </select> %
                    </span>
                    <span id="msmodusnlp1" <?php if($msmoduslp1old != 0) echo 'style="display: none;"' ?>>
                    	<br><br>
                    </span>
                </div>

				<div class="col-4 regularTextSize text-center" <?php if($isConfiguredLp[2] != 1) echo 'style="display: none;"' ?>>
                    <label for="msmoduslp2"></label>
                    <select class="sofortladenLadezielSelektor" type="text" name="msmoduslp2" id="msmoduslp2">
                    	<option <?php if($msmoduslp2old == 0) echo 'selected' ?> value="0">Aus</option>
                        <option <?php if($msmoduslp2old == 1) echo 'selected' ?> value="1">Lademenge</option>
                        <option <?php if($msmoduslp2old == 2) echo 'selected' ?> value="2">SoC</option>
                    </select>
					<div id="msmodusmlp2" <?php if($msmoduslp2old != 1) echo 'style="display: none;"' ?>>
						<br>
						<label for="lademlp2">Lademenge</label>
						<select type="text" name="lademlp2" id="lademlp2">
							<option <?php if($lademkwhs1old == 0) echo 'selected' ?> value="0">0</option>
							<option <?php if($lademkwhs1old == 2) echo 'selected' ?> value="2">2</option>
							<option <?php if($lademkwhs1old == 4) echo 'selected' ?> value="4">4</option>
							<option <?php if($lademkwhs1old == 6) echo 'selected' ?> value="6">6</option>
							<option <?php if($lademkwhs1old == 8) echo 'selected' ?> value="8">8</option>
							<option <?php if($lademkwhs1old == 10) echo 'selected' ?> value="10">10</option>
							<option <?php if($lademkwhs1old == 12) echo 'selected' ?> value="12">12</option>
							<option <?php if($lademkwhs1old == 14) echo 'selected' ?> value="14">14</option>
							<option <?php if($lademkwhs1old == 16) echo 'selected' ?> value="16">16</option>
							<option <?php if($lademkwhs1old == 18) echo 'selected' ?> value="18">18</option>
							<option <?php if($lademkwhs1old == 20) echo 'selected' ?> value="20">20</option>
							<option <?php if($lademkwhs1old == 25) echo 'selected' ?> value="25">25</option>
							<option <?php if($lademkwhs1old == 30) echo 'selected' ?> value="30">30</option>
							<option <?php if($lademkwhs1old == 35) echo 'selected' ?> value="35">35</option>
							<option <?php if($lademkwhs1old == 40) echo 'selected' ?> value="40">40</option>
							<option <?php if($lademkwhs1old == 45) echo 'selected' ?> value="45">45</option>
							<option <?php if($lademkwhs1old == 50) echo 'selected' ?> value="50">50</option>
							<option <?php if($lademkwhs1old == 55) echo 'selected' ?> value="55">55</option>
							<option <?php if($lademkwhs1old == 60) echo 'selected' ?> value="60">60</option>
							<option <?php if($lademkwhs1old == 65) echo 'selected' ?> value="65">65</option>
							<option <?php if($lademkwhs1old == 70) echo 'selected' ?> value="70">70</option>
						</select> kWh
						<br><br>
						<button class="resetTargetChargingBtn" lp="2">Reset</button>
					</div>
					<span id="msmodusslp2" <?php if($msmoduslp2old != 2) echo 'style="display: none;"' ?>>
						<br><br>
						<label for="sofortsoclp1">SoC</label>
						<select type="text" name="sofortsoclp2" id="sofortsoclp2">
						<option <?php if($sofortsoclp2old == 10) echo 'selected' ?> value="10">10</option>
							<option <?php if($sofortsoclp2old == 15) echo 'selected' ?> value="15">15</option>
							<option <?php if($sofortsoclp2old == 20) echo 'selected' ?> value="20">20</option>
							<option <?php if($sofortsoclp2old == 30) echo 'selected' ?> value="30">30</option>
							<option <?php if($sofortsoclp2old == 40) echo 'selected' ?> value="40">40</option>
							<option <?php if($sofortsoclp2old == 45) echo 'selected' ?> value="45">45</option>
							<option <?php if($sofortsoclp2old == 50) echo 'selected' ?> value="50">50</option>
							<option <?php if($sofortsoclp2old == 55) echo 'selected' ?> value="55">55</option>
							<option <?php if($sofortsoclp2old == 60) echo 'selected' ?> value="60">60</option>
							<option <?php if($sofortsoclp2old == 65) echo 'selected' ?> value="65">65</option>
							<option <?php if($sofortsoclp2old == 70) echo 'selected' ?> value="70">70</option>
							<option <?php if($sofortsoclp2old == 75) echo 'selected' ?> value="75">75</option>
							<option <?php if($sofortsoclp2old == 80) echo 'selected' ?> value="80">80</option>
							<option <?php if($sofortsoclp2old == 85) echo 'selected' ?> value="85">85</option>
							<option <?php if($sofortsoclp2old == 90) echo 'selected' ?> value="90">90</option>
							<option <?php if($sofortsoclp2old == 95) echo 'selected' ?> value="95">95</option>
						</select> %
					</span>
                  	<span id="msmodusnlp2" <?php if($msmoduslp2old != 0) echo 'style="display: none;"' ?>>
			        	<br><br>
					</span>
                </div>

            	<div class="col-4 regularTextSize text-center" <?php if($isConfiguredLp[3] != 1) echo 'style="display: none;"' ?>>
                    <label for="msmoduslp3"></label>
                    <select class="sofortladenLadezielSelektor" type="text" name="lademlp3check" id="msmoduslp3">
                    	<option <?php if($lademstats2old == 0) echo 'selected' ?> value="0">Aus</option>
                        <option <?php if($lademstats2old == 1) echo 'selected' ?> value="1">Lademenge</option>
                    </select>
					<span id="msmodusmlp3" <?php if($lademstats2old != 1) echo 'style="display: none;"' ?>>
						<br><br>
						<label for="lademlp3">Lademenge</label>
						<select type="text" name="lademlp3" id="lademlp3">
							<option <?php if($lademkwhs2old == 0) echo 'selected' ?> value="0">0</option>
							<option <?php if($lademkwhs2old == 2) echo 'selected' ?> value="2">2</option>
							<option <?php if($lademkwhs2old == 4) echo 'selected' ?> value="4">4</option>
							<option <?php if($lademkwhs2old == 6) echo 'selected' ?> value="6">6</option>
							<option <?php if($lademkwhs2old == 8) echo 'selected' ?> value="8">8</option>
							<option <?php if($lademkwhs2old == 10) echo 'selected' ?> value="10">10</option>
							<option <?php if($lademkwhs2old == 12) echo 'selected' ?> value="12">12</option>
							<option <?php if($lademkwhs2old == 14) echo 'selected' ?> value="14">14</option>
							<option <?php if($lademkwhs2old == 16) echo 'selected' ?> value="16">16</option>
							<option <?php if($lademkwhs2old == 18) echo 'selected' ?> value="18">18</option>
							<option <?php if($lademkwhs2old == 20) echo 'selected' ?> value="20">20</option>
							<option <?php if($lademkwhs2old == 25) echo 'selected' ?> value="25">25</option>
							<option <?php if($lademkwhs2old == 30) echo 'selected' ?> value="30">30</option>
							<option <?php if($lademkwhs2old == 35) echo 'selected' ?> value="35">35</option>
							<option <?php if($lademkwhs2old == 40) echo 'selected' ?> value="40">40</option>
							<option <?php if($lademkwhs2old == 45) echo 'selected' ?> value="45">45</option>
							<option <?php if($lademkwhs2old == 50) echo 'selected' ?> value="50">50</option>
							<option <?php if($lademkwhs2old == 55) echo 'selected' ?> value="55">55</option>
							<option <?php if($lademkwhs2old == 60) echo 'selected' ?> value="60">60</option>
							<option <?php if($lademkwhs2old == 65) echo 'selected' ?> value="65">65</option>
							<option <?php if($lademkwhs2old == 70) echo 'selected' ?> value="70">70</option>
						</select> kWh
						<br><br>
						<button class="resetTargetChargingBtn" lp="3">Reset</button>
					</span>
                    <span id="msmodusnlp3" <?php if($lademstats2old != 0) echo 'style="display: none;"' ?>></span>
				</div>
	  		</div>
			<div class="row justify-content-center">
				<div class="col-12">
					<hr color="white">
				</div>
			</div>


			<div class="row justify-content-center">
				<h3 class="font-weight-bold text-center text-lightgrey">Sofortladen Stromstärke</h3>
			</div>

			<div class="row justify-content-center" id="slider1div">
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp1s" id="sofortlllp1s" class="custom-range">
				</div>
				<div class="col-2 regularTextSize text-center">
					<label for="sofortlllp1">LP 1: <span id="sofortlllp1l"></span>A</label>
				</div>
				<script>
					var slider1 = document.getElementById("sofortlllp1s");
					var output1 = document.getElementById("sofortlllp1l");
					output1.innerHTML = slider1.value;
					slider1.oninput = function() {
						output1.innerHTML = this.value;
						lp1DirectChargeAmpsClick();
					}
				</script>
			</div>

			<div class="row justify-content-center" id="slider2div" <?php if($isConfiguredLp[2] != 1) echo 'style="display: none;"' ?>>
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp2s" id="sofortlllp2s" class="custom-range">
				</div>
				<div class="col-2 regularTextSize text-center">
					<label for="sofortlllp2">LP 2: <span id="sofortlllp2l"></span>A</label>
				</div>
				<script>
					var slider2 = document.getElementById("sofortlllp2s");
					var output2 = document.getElementById("sofortlllp2l");
					output2.innerHTML = slider2.value;
					slider2.oninput = function() {
						output2.innerHTML = this.value;
						lp2DirectChargeAmpsClick();
					}
				</script>
			</div>

			<div class="row justify-content-center" id="slider3div" <?php if($isConfiguredLp[3] != 1) echo 'style="display: none;"' ?>>
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp3s" id="sofortlllp3s" class="custom-range">
				</div>
				<div class="col-2 regularTextSize text-center">
					<label for="sofortlllp3">LP 3: <span id="sofortlllp3l"></span>A</label>
				</div>
				<script>
					var slider3 = document.getElementById("sofortlllp3s");
					var output3 = document.getElementById("sofortlllp3l");
					output3.innerHTML = slider3.value;
					slider3.oninput = function() {
						output3.innerHTML = this.value;
						lp3DirectChargeAmpsClick();
					}
				</script>
			</div>

			<div class="row justify-content-center" id="slider4div" <?php if($isConfiguredLp[4] != 1) echo 'style="display: none;"' ?>>
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp4s" id="sofortlllp4s" class="custom-range">
				</div>
				<div class="col-2 regularTextSize text-center">
					<label for="sofortlllp4">LP 4: <span id="sofortlllp4l"></span>A</label>
				</div>
				<script>
					var slider4 = document.getElementById("sofortlllp4s");
					var output4 = document.getElementById("sofortlllp4l");
					output4.innerHTML = slider4.value;
					slider4.oninput = function() {
						output4.innerHTML = this.value;
						lp4DirectChargeAmpsClick();
					}
				</script>
			</div>

			<div class="row justify-content-center" id="slider5div" <?php if($isConfiguredLp[5] != 1) echo 'style="display: none;"' ?>>
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp5s" id="sofortlllp5s" class="custom-range">
				</div>
				<div class="col-2 regularTextSize text-center">
					<label for="sofortlllp5">LP 5: <span id="sofortlllp5l"></span>A</label>
				</div>
				<script>
					var slider5 = document.getElementById("sofortlllp5s");
					var output5 = document.getElementById("sofortlllp5l");
					output5.innerHTML = slider5.value;
					slider5.oninput = function() {
						output5.innerHTML = this.value;
						lp5DirectChargeAmpsClick();
					}
				</script>
			</div>

			<div class="row justify-content-center" id="slider6div" <?php if($isConfiguredLp[6] != 1) echo 'style="display: none;"' ?>>
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp6s" id="sofortlllp6s" class="custom-range">
				</div>
				<div class="col-2 regularTextSize text-center">
					<label for="sofortlllp6">LP 6: <span id="sofortlllp6l"></span>A</label>
				</div>
				<script>
					var slider6 = document.getElementById("sofortlllp6s");
					var output6 = document.getElementById("sofortlllp6l");
					output6.innerHTML = slider6.value;
					slider6.oninput = function() {
						output6.innerHTML = this.value;
						lp6DirectChargeAmpsClick();
					}
				</script>
			</div>

			<div class="row justify-content-center" id="slider7div" <?php if($isConfiguredLp[7] != 1) echo 'style="display: none;"' ?>>
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp7s" id="sofortlllp7s" class="custom-range">
				</div>
				<div class="col-2 regularTextSize text-center">
					<label for="sofortlllp7">LP 7: <span id="sofortlllp7l"></span>A</label>
				</div>
				<script>
					var slider7 = document.getElementById("sofortlllp7s");
					var output7 = document.getElementById("sofortlllp7l");
					output7.innerHTML = slider7.value;
					slider7.oninput = function() {
						output7.innerHTML = this.value;
						lp7DirectChargeAmpsClick();
					}
				</script>
			</div>

			<div class="row justify-content-center" id="slider8div" <?php if($isConfiguredLp[8] != 1) echo 'style="display: none;"' ?>>
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp8s" id="sofortlllp8s" class="custom-range">
				</div>
				<div class="col-2 regularTextSize text-center">
					<label for="sofortlllp8">LP 8: <span id="sofortlllp8l"></span>A</label>
				</div>
				<script>
					var slider8 = document.getElementById("sofortlllp8s");
					var output8 = document.getElementById("sofortlllp8l");
					output8.innerHTML = slider8.value;
					slider8.oninput = function() {
						output8.innerHTML = this.value;
						lp8DirectChargeAmpsClick();
					}
				</script>
			</div>
			<br>

			<div class="row">
				<div class="col text-center">
					<button type="submit" class="btn btn-green">Save</button>
				</div>
			</div>

			<hr color="white">

		</form>


<!-- end old code-->

		<!-- a few buttons at end of page for options -->
		<!-- too many cols per row so bootstrap will linebreak -->
		<!-- and change to appropriate button layout -->
		<div class="row no-gutters justify-content-center">
			<div class="col-sm-3 py-1">
				<a href="ladelog.php"><button id="ladelogBtn" type="button" class="btn btn-lg btn-block btn-blue buttonTextSize">Ladelog</button></a>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-4 py-1">
				<a href="logging/index.php"><button id="loggingBtn" type="button" class="btn btn-lg btn-block btn-blue buttonTextSize">Logging</button></a>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-3 py-1">
				<a href="./status/status.php"><button id="statusBtn" type="button" class="btn btn-lg btn-block btn-blue buttonTextSize">Status</button></a>
			</div>
		</div>
		<div class="row no-gutters justify-content-center">
			<div class="col-sm-3 order-last order-sm-first py-1">
				<a href="./hilfe/hilfe.php"><button id="hilfeBtn" type="button" class="btn btn-lg btn-block btn-blue buttonTextSize">Hilfe</button></a>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-3 order-first order-sm-last py-1 ">
				<a href="settings/settings.php"><button id="settingsBtn" type="button" class="btn btn-lg btn-block btn-blue buttonTextSize">Einstellungen</button></a>
			</div>
		</div>
		<br>

	</div>  <!-- end container -->

	<!-- modal chargemode-select-window -->
	<div class="modal fade" id="chargeModeModal">
		<div class="modal-dialog">
			<div class="modal-content">

				<!-- modal header -->
				<div class="modal-header btn-green">
					<h4 class="modal-title">Auswahl</h4>
				</div>

				<!-- modal body -->
				<div class="modal-body">
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="chargeModeSofortBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-red" data-dismiss="modal" chargeMode="0">Sofortladen</button>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 order-first order-sm-last py-1">
							<button id="chargeModePVBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-red" data-dismiss="modal" chargeMode="2">PV</button>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="chargeModeMinPVBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-red" data-dismiss="modal" chargeMode="1">Min + PV</button>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="chargeModeStdbyBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-red" data-dismiss="modal" chargeMode="4">Standby</button>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="chargeModeStopBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-red" data-dismiss="modal" chargeMode="3">Stop</button>
						</div>
					</div>

					<hr>

					<div class="row">
						<div class="col text-center text-grey">
							Vorrang im Lademodus PV-Laden:
							<br>
							derzeit noch nicht implementiert... Einstellung unter "Einstellungen/PV-Ladeeinstellungen"
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="evPriorityBtn" type="button" class="priorityModeBtn btn btn-lg btn-block btn-red" data-dismiss="modal" priority="ev">EV</button>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="batteryPriorityBtn" type="button" class="priorityModeBtn btn btn-lg btn-block btn-red" data-dismiss="modal" priority="battery">Speicher</button>
						</div>
					</div>

				</div> <!-- /modal body -->

				<!-- no modal footer -->
			</div>
		</div>
	</div>


	<!-- load Chart.js library -->
	<script src="js/Chart.bundle.js"></script>

	<!-- load mqtt library -->
	<script src = "js/mqttws31.js" ></script>

	<!-- load respective Chart.js definition -->
	<script src="themes/<?php echo $themeCookie ?>/livechart.js?ver=20200403-c"></script>
	<script src="themes/<?php echo $themeCookie ?>/awattarchart.js?ver=20200331-a"></script>
	<!-- Data refresher -->
	<script src="themes/<?php echo $themeCookie ?>/processAllMqttMsg.js?ver=20200408-a"></script>

	<!-- some scripts -->
	<script type="text/javascript">

		function AwattarMaxPriceClick() {
			publish(document.getElementById("awattar1l").innerHTML,"openWB/set/awattar/MaxPriceForCharging");
		}
		function lp1DirectChargeAmpsClick() {
			publish(document.getElementById("sofortlllp1l").innerHTML,"openWB/set/lp1/DirectChargeAmps");
		}

		function lp2DirectChargeAmpsClick() {
			publish(document.getElementById("sofortlllp2l").innerHTML,"openWB/set/lp2/DirectChargeAmps");
		}

		function lp3DirectChargeAmpsClick() {
			publish(document.getElementById("sofortlllp3l").innerHTML,"openWB/set/lp3/DirectChargeAmps");
		}

		function lp4DirectChargeAmpsClick() {
			publish(document.getElementById("sofortlllp4l").innerHTML,"openWB/set/lp4/DirectChargeAmps");
		}

		function lp5DirectChargeAmpsClick() {
			publish(document.getElementById("sofortlllp5l").innerHTML,"openWB/set/lp5/DirectChargeAmps");
		}

		function lp6DirectChargeAmpsClick() {
			publish(document.getElementById("sofortlllp6l").innerHTML,"openWB/set/lp6/DirectChargeAmps");
		}

		function lp7DirectChargeAmpsClick() {
			publish(document.getElementById("sofortlllp7l").innerHTML,"openWB/set/lp7/DirectChargeAmps");
		}

		function lp8DirectChargeAmpsClick() {
			publish(document.getElementById("sofortlllp8l").innerHTML,"openWB/set/lp8/DirectChargeAmps");
		}

		$(document).ready(function(){

			$.getScript("themes/<?php echo $themeCookie ?>/setupMqttServices.js?ver=20200401-a");
			$.getScript("themes/<?php echo $themeCookie ?>/processHooks.js?ver=20200401-a");

			$('.lpEnableSpan').click(function(event){
				// send mqtt set to enable/disable charge point after click
				// attribut value is changed at receipt of confirmation mqttmsg
				var lp = $(this).attr("lp");
				var isEnabled = $(this).attr("isEnabled");
				switch ( isEnabled ) {
					case "1":
						publish("0", "openWB/set/lp" + lp + "/ChargePointEnabled");
						break;
					case "0":
						publish("1", "openWB/set/lp" + lp + "/ChargePointEnabled");
						break;
				}
			});

			$('#chargeModeSelect').click(function(event){
				$("#chargeModeModal").modal("show");
			});

			$('.chargeModeBtn').click(function(event){
				var chargeMode = $(this).attr("chargeMode")
				publish(chargeMode, "openWB/set/ChargeMode");
			});

			$('.priorityModeBtn').click(function(event){
				var priority = $(this).attr("priority")
				if ( priority == "ev" ) {
					// <a href="./tools/changelademodus.php?pveinbeziehen=1" class="btn btn-lg btn-block btn-green myButtonStyle">Speichervorrang</a>
				} else {
					//<a href="./tools/changelademodus.php?pveinbeziehen=0" class="btn btn-lg btn-block btn-green myButtonStyle">EV Vorrang</a>
				}
			});

			$('.resetTargetChargingBtn').click(function(event){
				var lp = $(this).attr("lp");
				$.ajax({
			        type: "POST",
			        url: './tools/resetlpladem.php',
			        data:{action:'resetlp' + lp},
			        success:function(html) {
					}
        		});
    		});

			$('.sofortladenLadezielSelektor').change(function(event){
			    // switches the visibility of the settings-divs according to dropdown selection
			    var selectorId = '#' + event.target.id;
			    var divAusId = selectorId.slice(0, 8) + 'n' + selectorId.slice(8);
			    var divSocId = selectorId.slice(0, 8) + 's' + selectorId.slice(8);
			    var divMengeId = selectorId.slice(0, 8) + 'm' + selectorId.slice(8);
			    switch ($(selectorId).val()) {
			        case '0':
			            $(divAusId).show();
			            $(divSocId).hide();
			            $(divMengeId).hide();
			            break;
			        case '1':
			            $(divAusId).hide();
			            $(divSocId).hide();
			            $(divMengeId).show();
			            break;
			        case '2':
			            $(divAusId).hide();
			            $(divSocId).show();
			            $(divMengeId).hide();
			            break;
			    }
			});

			// register an event listener for changes in visibility
			let hidden;
			let visibilityChange;
			if (typeof document.hidden !== 'undefined') { // Opera 12.10 and Firefox 18 and later support
				hidden = 'hidden';
				visibilityChange = 'visibilitychange';
			} else if (typeof document.msHidden !== 'undefined') {
				hidden = 'msHidden';
				visibilityChange = 'msvisibilitychange';
			} else if (typeof document.webkitHidden !== 'undefined') {
				hidden = 'webkitHidden';
				visibilityChange = 'webkitvisibilitychange';
			}
			window.document.addEventListener(visibilityChange, () => {
				if (!document[hidden]) {
					// once page is unhidden... reload graph completety
					initialread = 0;
					all1 = 0;
					all2 = 0;
					all3 = 0;
					all4 = 0;
					all5 = 0;
					all6 = 0;
					all7 = 0;
					all8 = 0;
					subscribeMqttGraphSegments();
				}
			});

		});
	</script>

</body>

</html>
