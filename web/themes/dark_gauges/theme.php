<!DOCTYPE html>
<html lang="de">

<head>
	<!-- dark_gauges_1 theme for openWB -->
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
	<link rel="stylesheet" type="text/css" href="themes/<?php echo $_COOKIE['openWBTheme'];?>/style.css">

	<script>
		registerPageVisibility()
		function registerPageVisibility() {
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
					initialread = 0;
					all1 = 0;
					all2 = 0;
					all3 = 0;
					all4 = 0;
					all5 = 0;
					all6 = 0;
					all7 = 0;
					all8 = 0;
				}
			});
		}
	</script>

	<input hidden name="lastmanagement" id="lastmanagement" value="<?php echo $lastmanagementold ; ?>" />
	<input hidden name="lastmanagements2" id="lastmanagements2" value="<?php echo $lastmanagements2old ; ?>" />
	<input hidden name="speicherstat" id="speicherstat" value="<?php echo $speicherstatold ; ?>" />
	<input hidden name="lademlp1stat" id="lademlp1stat" value="<?php echo $lademstatold ; ?>" />
	<input hidden name="lademlp2stat" id="lademlp2stat" value="<?php echo $lademstats1old ; ?>" />
	<input hidden name="lademlp3stat" id="lademlp3stat" value="<?php echo $lademstats2old ; ?>" />
	<input hidden name="evuglaettungakt" id="evuglaettungakt" value="<?php echo $evuglaettungaktold ; ?>" />
	<input hidden name="nachtladenstate" id="nachtladenstate" value="<?php echo $nachtladenstate ; ?>" />
	<input hidden name="nachtladenstates1" id="nachtladenstates1" value="<?php echo $nachtladenstates1 ; ?>" />
	<input hidden name="nlakt_nurpv" id="nlakt_nurpv" value="<?php echo $nlakt_nurpvold ; ?>" />
	<input hidden name="nlakt_sofort" id="nlakt_sofort" value="<?php echo $nlakt_sofortold ; ?>" />
	<input hidden name="nlakt_minpv" id="nlakt_minpv" value="<?php echo $nlakt_minpvold ; ?>" />
	<input hidden name="nlakt_standby" id="nlakt_standby" value="<?php echo $nlakt_standbyold ; ?>" />
	<input hidden name="lademodus" id="lademodus" value="<?php echo $lademodusold ; ?>" />
	<input hidden name="hausverbrauchstat" id="hausverbrauchstat" value="<?php echo $hausverbrauchstatold ; ?>" />
	<input hidden name="speicherpvui" id="speicherpvui" value="<?php echo $speicherpvuiold ; ?>" />
	<input hidden name="zielladenaktivlp1" id="zielladenaktivlp1" value="<?php echo $zielladenaktivlp1old ; ?>" />
	<input hidden name="sofortlm" id="sofortlm" value="<?php echo $lademodusold ; ?>" />
	<input hidden name="heutegeladen" id="heutegeladen" value="<?php echo $heutegeladenold ; ?>" />

	<!-- important scripts to be loaded -->
	<script src="js/jquery-3.4.1.min.js"></script>
	<script src="js//bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
	<script src="js/RGraph.common.core.js"></script>
	<script src="js/RGraph.common.dynamic.js"></script>
	<script src="js/RGraph.common.effects.js"></script>
	<script src="js/RGraph.gauge.js"></script>
	<script src="js/RGraph.vprogress.js"></script>
</head>

<body>
	<script>

		var hook1_aktiv = <?php echo $hook1_aktivold ?>;
		var hook2_aktiv = <?php echo $hook2_aktivold ?>;
		var hook3_aktiv = <?php echo $hook3_aktivold ?>;
		var lastmanagements2 = <?php echo $lastmanagements2old ?>;
		var lastmanagement = <?php echo $lastmanagementold ?>;
		var soc1vorhanden = <?php echo $soc1vorhanden ?>;
		var verbraucher1vorhanden = <?php echo $verbraucher1vorhanden ?>;
		var verbraucher2vorhanden = <?php echo $verbraucher2vorhanden ?>;
		var speichervorhanden = <?php echo $speichervorhanden ?>;
		var awattaraktiv = <?php echo $awattaraktivold?>;
		var defaultScaleCounter = 8640;  // ca. 12 Stunden
	</script>

	<?php
		// Check ob Gauge-Skala-Cookies existiert - dann Werte übernehmen, sonst Standard setzen
		if((isset($_COOKIE['dark_gauges_1_pvData']) === true)) {
			$pvDataScaleMax = $_COOKIE['dark_gauges_1_pvData'];
		} else {
			$pvDataScaleMax = 1000;
		}

		if((isset($_COOKIE['dark_gauges_1_battData']) === true)) {
			$battDataScaleMax = $_COOKIE['dark_gauges_1_battData'];
		} else {
			$battDataScaleMax = 1000;
		}

		if((isset($_COOKIE['dark_gauges_1_evuData']) === true)) {
			$evuDataScaleMax = $_COOKIE['dark_gauges_1_evuData'];
		} else {
			$evuDataScaleMax = 1000;
		}
	?>

	<div class="container">

		<div class="row">
			<div class="col gradient">
				<h1>openWB Charge Controller</h1>
			</div>
		</div>

		<div class="row no-gutters">
			<div class="col-6 col-md-3 pvInfoStyle">
				<div>Photovoltaik</div>
				<canvas id="pvData">
					Sorry, no canvas support
				</canvas>
			</div>
			<div class="col-6 col-md-3 pvInfoStyle">
				<div>Speicher</div>
				<canvas id="battData">
					Sorry, no canvas support
				</canvas>
				<canvas id="battSocData">
					Sorry, no canvas support
				</canvas>
			</div>
			<div class="col-6 col-md-3 pvInfoStyle">
				<div>Energienetz</div>
				<canvas id="evuData">
					Sorry, no canvas support
				</canvas>
			</div>
			<div class="col-6 col-md-3 pvInfoStyle">
				<div>Hausverbrauch</div>
				<canvas id="homeData">
					Sorry, no canvas support
				</canvas>
			</div>
		</div>

		<?php
			if ( ($hook1_aktivold == 1 || $hook2_aktivold == 1 || $hook3_aktivold == 1) ) {
			// if hooks for external devices are configured, show div
				echo '<div id="webhooksdiv" class="row justify-content-center extDeviceInfoStyle bg-secondary">';
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

		<br>

		<!-- interactive chart.js -->
		<!-- will be refreshed using MQTT (in live.js)-->
		<div class="row justify-content-center" id="thegraph">
			<div class="col-sm-12" style="height: 350px; text-align: center;">
				<div id="waitforgraphloadingdiv">
					Graph lädt, bitte warten...
				</div>
				<canvas id="canvas"></canvas>
			</div>
			<div id="graphoptiondiv" style="display: none;">
				<br><br>
			</div>
		</div>

		<div class="row">
			<div id="lastregelungaktivdiv" class="col regularTextStyle animate-alertPulsation" style="color:#990000; background-color:white; display: none;">
			</div>
		</div>

		<!-- chargepoint info header -->
		<div class="row no-gutter justify-content-center chargePointInfoStyle" style="font-weight: bolder;">
			<div class="col-4">
				Ladepunkt
			</div>
			<div class="col-3">
				ist / soll
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
			for($i=1; $i <= 8; $i++) {
				$name='"$isConfiguredLp'.$i.'"';
				echo '<!-- name: '.$name.' LP'.$i.' conf='.${"isConfiguredLp$i"}.'-->';
				echo '<!-- data-row for charging Point '.$i.' -->'."\n";
				echo '        <div id="lp'.$i.'div" class="row no-gutter py-1 py-md-0 justify-content-center chargePointInfoStyle" style="display: none;">'."\n";
				echo '            <div class="col-4">'."\n";
				echo '                <span class="cursor-pointer" onclick="lp'.$i.'enabledclick()">'."\n";
				echo '                    <span class="fas fa-xs fa-key" id="lp'.$i.'AutolockConfiguredSpan" style="display: none;"></span>'."\n"; // placeholder for autolock icons
				echo '                    <span class="fa" id="lp'.$i.'enableddiv"></span>'."\n";
				echo '                    <span class="nameLp'.$i.'"></span>'."\n";
				echo '                </span>'."\n";
				echo '                <span class="fa" id="plugstatlp'.$i.'div"></span>'."\n";
				echo '                <span class="fa" id="zielladenaktivlp'.$i.'div"></span>'."\n";
				echo '                <span class="fa" id="nachtladenaktivlp'.$i.'div"></span>'."\n";
				echo '            </div>'."\n";
				echo '            <div class="col-3">'."\n";
				echo '                <span id="actualPowerLp'.$i.'div"></span><span id="targetCurrentLp'.$i.'div"></span>'."\n";
				echo '            </div>'."\n";
				echo '            <div class="col-3 text-center">'."\n";
				echo '                <span id="energyChargedLp'.$i.'div"></span>'."\n";
				echo '            </div>'."\n";
				// standard: soc not configured for charging point
				echo '            <div id="socNotConfiguredLp'.$i.'div" class="col-2">'."\n";
				echo '                --'."\n";
				echo '            </div>'."\n";
				echo '            <div id="socConfiguredLp'.$i.'div" class="col-2" style="display: none;">'."\n";
				echo '                <span id="socLp'.$i.'"></span>'."\n";
				echo '            </div>'."\n";
				echo '        </div>'."\n\n";
				echo '        ';
			}
		?>

		<div id="powerAllLpdiv" class="row justify-content-center" style="display: none;">
			<div class="col-sm-5 chargePointInfoStyle">
				Gesamt-Ladeleistung: <span id="powerAllLpspan"></span>
			</div>
		</div>

		<hr color="white">

		<div class="row">
			<div class="col">
				<h2>Lademodus</h2>
			</div>
		</div>

		<!-- display and change charging mode -->
		<!-- too many cols per row so bootstrap will linebreak -->
		<!-- and change to appropriate button layout -->
		<div class="row no-gutters justify-content-center">
			<div class="col-sm-5 py-1">
				<button id="sofortBtn" type="button" class="btn btn-lg btn-block btn-red myButtonStyle" onclick="chargeModeBtnClick(this.value)" value="0">Sofortladen</button>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-5 py-1">
				<button id="minUndPvBtn" type="button" class="btn btn-lg btn-block btn-red myButtonStyle" onclick="chargeModeBtnClick(this.value)" value="1">Min + PV</button>
			</div>
		</div>
		<div class="row no-gutters justify-content-center">
			<div class="col-sm-4 py-1">
				<button id="standbyBtn" type="button" class="btn btn-lg btn-block btn-red myButtonStyle" onclick="chargeModeBtnClick(this.value)" value="4">Standby</button>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-2 py-1">
				<button id="stopBtn" type="button" class="btn btn-lg btn-block btn-red myButtonStyle" onclick="chargeModeBtnClick(this.value)" value="3">Stop</button>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-4 order-first order-sm-last py-1">
				<button id="pvBtn" type="button" class="btn btn-lg btn-block btn-red myButtonStyle" onclick="chargeModeBtnClick(this.value)" value="2">PV</button>
			</div>
		</div>

		<div id="speicherpvuidiv" class="row no-gutters justify-content-center">
			<div class="col-sm-4 py-1">
				<?php
					if ($speicherpveinbeziehenold == 0) {
						echo '<a href="./tools/changelademodus.php?pveinbeziehen=1" class="btn btn-lg btn-block btn-green myButtonStyle">Speichervorrang</a>';
					} else {
						echo '<a href="./tools/changelademodus.php?pveinbeziehen=0" class="btn btn-lg btn-block btn-green myButtonStyle">EV Vorrang</a>';
					}
				?>
			</div>
		</div>

		<hr color="white">

<!-- old code, not optimized for mqtt -->
<!-- will be replaced once mqtt is fully functional -->

		<div class="row justify-content-center">
			<h3>letztes zusammenhängendes Ladesegment</h3>
		</div>

		<div class="row justify-content-center regularTextStyle">
			<div class="col-4">
				LP1 <span class="nameLp1"></span>
			</div>
			<div  id="ladepunkts11div" class="col-4">
				LP2 <span class="nameLp2"></span>
			</div>
			<div id="ladepunkts22div" class="col-4 ">
				LP3 <span class="nameLp3"></span>
			</div>
		</div>

		<div class="row justify-content-center regularTextStyle">
			<div class="col-4">
				<span id="gelrlp1div"></span>
			</div>
			<div id="ladepunkts111div" class="col-4">
				<span id="gelrlp2div"></span>
			</div>
			<div id="ladepunkts222div" class="col-4">
				<span id="gelrlp3div"></span>
			</div>
		</div>

		<div class="row justify-content-center regularTextStyle">
			<div class="col-4">
				<span id="aktgeladen1div"></span>
			</div>
			<div id="ladepunkts1111div" class="col-4">
				<span id="aktgeladen2div"></span>
			</div>
			<div id="ladepunkts2222div" class="col-4">
				<span id="aktgeladen3div"></span>
			</div>
		</div>

		<div id="targetChargingProgressDiv" style="display: none;">
			<div class="row justify-content-center regularTextStyle">
				<div class="col-4">
					<div id="lademstatdiv">
						<progress id="prog1" value= "0" max=<?php echo $lademkwhold ?>></progress>
					</div>
				</div>
				<div id="ladepunkts11111div" class="col-4">
					<div id="lademstats1div">
						<progress id="prog2" value= "0" max=<?php echo $lademkwhs1old ?>></progress>
					</div>
				</div>
				<div id="ladepunkts22222div" class="col-4">
					<div id="lademstats2div">
						<progress id="prog3" value= "0" max=<?php echo $lademkwhs2old ?>></progress>
					</div>
				</div>
			</div>

			<div class="row justify-content-center regularTextStyle">
				<div class="col-4">
					<div id="lademstat1div">
						Restzeit <span id="restzeitlp1div"></span>
					</div>
				</div>
				<div id="ladepunkts1111111div" class="col-4">
					<div id="lademstats1div1">
						Restzeit <span id="restzeitlp2div"></span>
					</div>
				</div>
				<div id="ladepunkts2222222div" class="col-4">
					<div id="lademstats2div1">
						Restzeit <span id="restzeitlp3div"></span>
					</div>
				</div>
			</div>
		</div>


		<!-- depending on charge mode show options -->
	    <form id="sofortlmdiv" name="sofortll" action="./tools/sofortll.php" method="POST">
		    <div id="awattardiv" style="display: none;">
			<hr color="white">
			<div class="row justify-content-center">
				<h3>Awattar</h3>
			</div>
			<div class="row justify-content-center">
				<div class="col-sm-12" style="height: 150px; text-align: center;">
					<canvas id="awattarcanvas"></canvas>
				</div>
			</div>
			<div class="row justify-content-center" id="sliderawattardiv">
				<div class="col-7">
					<input type="range" min="-1" max="12" step="0.10" name="awattar1s" id="awattar1s" class="custom-range">
				</div>
				<div class="col-2 regularTextStyle">
					<label for="awattar1">Maximaler Preis: <span id="awattar1l"></span>Cent/kWh</label>
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
			<hr color="white">
		</div>
			<div class="row justify-content-center">
		            <h3>Sofortladen Ladeziel-Einstellungen</h3>
		    </div>

	        <div class="row justify-content-center">
                <div class="col-4 regularTextStyle">
                    <label for="msmoduslp1"></label>
                    <select type="text" name="msmoduslp1" id="msmoduslp1">
                        <option <?php if($msmoduslp1old == 0) echo 'selected' ?> value="0">unbegrenzt</option>
                        <option <?php if($msmoduslp1old == 1) echo 'selected' ?> value="1">Lademenge</option>
                        <option <?php if($msmoduslp1old == 2) echo 'selected' ?> value="2">SoC</option>
                    </select>
                    <span id="msmodusmlp1">
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
                        <button onclick="rslp1()">Reset</button>
                    </span>
                    <span id="msmodusslp1"><br><br>
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
                    <span id="msmodusnlp1">
                    	<br><br>
                    </span>
                </div>

				<div class="col-4 regularTextStyle" id="ladepunkts111111div">
                    <label for="msmoduslp2"></label>
                    <select type="text" name="msmoduslp2" id="msmoduslp2">
                    	<option <?php if($msmoduslp2old == 0) echo 'selected' ?> value="0">unbegrenzt</option>
                        <option <?php if($msmoduslp2old == 1) echo 'selected' ?> value="1">Lademenge</option>
                        <option <?php if($msmoduslp2old == 2) echo 'selected' ?> value="2">SoC</option>
                    </select>
					<div id="msmodusmlp2">
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
						<button onclick="rslp2()">Reset</button>
					</div>
					<span id="msmodusslp2"><br><br>
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
                  	<span id="msmodusnlp2">
			        	<br><br>
					</span>
                </div>

            	<div class="col-4 regularTextStyle" id="ladepunkts222222div">
                    <label for="lademlp3check"></label>
                    <select type="text" name="lademlp3check" id="lademlp3check">
                    	<option <?php if($lademstats2old == 0) echo 'selected' ?> value="0">unbegrenzt</option>
                        <option <?php if($lademstats2old == 1) echo 'selected' ?> value="1">Lademenge</option>
                    </select>
					<span id="msmodusmlp3">
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
						<button onclick="rslp3()">Reset</button>
					</span>
                    <span id="msmodusnlp3"></span>
				</div>
	  		</div>

			<div class="row justify-content-center">
				<div class="col-10">
					<hr color="white">
				</div>
			</div>


			<div class="row justify-content-center">
				<h3>Sofortladen Stromstärke</h3>
			</div>

			<div class="row justify-content-center" id="slider1div">
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp1s" id="sofortlllp1s" class="custom-range">
				</div>
				<div class="col-2 regularTextStyle">
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

			<div class="row justify-content-center" id="slider2div">
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp2s" id="sofortlllp2s" class="custom-range">
				</div>
				<div class="col-2 regularTextStyle">
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

			<div class="row justify-content-center" id="slider3div">
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp3s" id="sofortlllp3s" class="custom-range">
				</div>
				<div class="col-2 regularTextStyle">
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

			<div class="row justify-content-center" id="slider4div">
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp4s" id="sofortlllp4s" class="custom-range">
				</div>
				<div class="col-2 regularTextStyle">
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

			<div class="row justify-content-center" id="slider5div">
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp5s" id="sofortlllp5s" class="custom-range">
				</div>
				<div class="col-2 regularTextStyle">
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

			<div class="row justify-content-center" id="slider6div">
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp6s" id="sofortlllp6s" class="custom-range">
				</div>
				<div class="col-2 regularTextStyle">
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

			<div class="row justify-content-center" id="slider7div">
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp7s" id="sofortlllp7s" class="custom-range">
				</div>
				<div class="col-2 regularTextStyle">
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

			<div class="row justify-content-center" id="slider8div">
				<div class="col-7">
					<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp8s" id="sofortlllp8s" class="custom-range">
				</div>
				<div class="col-2 regularTextStyle">
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

			<div class="row justify-content-center">
				<div class="col-sm-10">
					<br>
					<button type="submit" class="btn btn-lg btn-block btn-green myButtonStyle">Save</button>
				</div>
			</div>


		</form>


<!-- end old code-->

		<hr color="white">

		<!-- a few buttons at end of page for options -->
		<!-- too many cols per row so bootstrap will linebreak -->
		<!-- and change to appropriate button layout -->
		<div class="row no-gutters justify-content-center">
			<div class="col-sm-3 py-1">
				<a href="ladelog.php"><button id="ladelogBtn" type="button" class="btn btn-lg btn-block btn-blue myButtonStyle">Ladelog</button></a>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-4 py-1">
				<a href="logging/index.php"><button id="loggingBtn" type="button" class="btn btn-lg btn-block btn-blue myButtonStyle">Logging</button></a>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-3 py-1">
				<a href="./status/status.php"><button id="statusBtn" type="button" class="btn btn-lg btn-block btn-blue myButtonStyle">Status</button></a>
			</div>
		</div>
		<div class="row no-gutters justify-content-center">
			<div class="col-sm-3 order-last order-sm-first py-1">
				<a href="./hilfe/hilfe.php"><button id="hilfeBtn" type="button" class="btn btn-lg btn-block btn-blue myButtonStyle">Hilfe</button></a>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-4 py-1">
				<button id="graphOptionsBtn" type="button" class="btn btn-lg btn-block btn-blue myButtonStyle" onclick="GraphOptionsClick()">Graph Optionen</button>
			</div>
			<div class="d-none d-sm-block">
				&nbsp
			</div>
			<div class="col-sm-3 order-first order-sm-last py-1 ">
				<a href="settings/settings.php"><button id="settingsBtn" type="button" class="btn btn-lg btn-block btn-blue myButtonStyle">Einstellungen</button></a>
			</div>
		</div>

		<div class="row justify-content-center">
			<div class="col-3 versionTextStyle">
				Ver <?php echo $owbversion ?>
			</div>
			<div class="col-4 regularTextStyle">
				<a href="https://openwb.de">www.openwb.de</a>
			</div>
			<div class="col-3 versionTextStyle">
				Theme 2020 by M.Ortenstein
			</div>
		</div>

			<br><br><br><br>

		<!-- Graph-Options with Popup-Window-Look -->
		<div id="graphsettings" style="position: fixed; display: none; width: 100%; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.5); z-index: 2; cursor: pointer;">
			<div style="  position: absolute; top: 50%; left: 50%; width: 80%; font-size: 12px; color: black; text-align: center; background-color: white; border-radius: 6px 6px 6px 6px; transform: translate(-50%,-50%); -ms-transform: translate(-50%,-50%); ">
				<div class="row"><div class="col-sm-12">
					Graph Sichtbarkeit:
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp1')"><i id="graphlp1div" class="fa"></i> Ladepunkt 1</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp2')"><i id="graphlp2div" class="fa"></i> Ladepunkt 2</span>
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp3')"><i id="graphlp3div" class="fa"></i> Ladepunkt 3</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp4')"><i id="graphlp4div" class="fa"></i> Ladepunkt 4</span>
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp5')"><i id="graphlp5div" class="fa"></i> Ladepunkt 5</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp6')"><i id="graphlp6div" class="fa"></i> Ladepunkt 6</span>
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp7')"><i id="graphlp7div" class="fa"></i> Ladepunkt 7</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp8')"><i id="graphlp8div" class="fa"></i> Ladepunkt 8</span>
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLpAll')"><i id="graphlpalldiv" class="fa"></i> Alle Ladepunkte</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayHouseConsumption')"><i id="graphhausdiv" class="fa"></i>Hausverbrauch</span>
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayEvu')"><i id="graphevudiv" class="fa"></i> EVU</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayPv')"><i id="graphpvdiv" class="fa"></i> PV</span>
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplaySpeicher')"><i id="graphspeicherdiv" class="fa"></i> Speicher</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplaySpeicherSoc')"><i id="graphspeichersocdiv" class="fa"></i> Speicher SoC</span>
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp1Soc')"><i id="graphlp1socdiv" class="fa"></i> Ladepunkt 1 SoC</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp2Soc')"><i id="graphlp2socdiv" class="fa"></i> Ladepunkt 2 SoC</span>
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLoad1')"><i id="graphload1div" class="fa"></i>Verbraucher 1</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLoad2')"><i id="graphload2div" class="fa"></i>Verbraucher 2</span>
				</div>
			</div>
			<div class="row col-sm-12" style="white-space: nowrap;">
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidelegend('boolDisplayLegend')"><i id="graphlegenddiv" class="fa"></i>Legende</span>
				</div>
				<div class="col-sm-6">
					<span style="cursor: pointer;" onclick="showhidelegend('boolDisplayLiveGraph')"><i id="graphgraphdiv" class="fa"></i> Graph Anzeige</span>
				</div>
			</div>
			<div class="row">
				<div class="col-sm-12">
					Optionen:
				</div>
			</div>
			<div class="row">
				<div class="col-sm-12">
					<input type="button" value="Renew MQTT" label="Renew MQTT" onclick="renewMQTTclick()"/><br>
				</div>
			</div>
			<hr>
			<div class="row">
				<div class="col-sm-12">
					<input type="button" value="Schließen" label="Schließen" onclick="off()"/>
				</div>
			</div>
		</div>

	</container>

	<!-- some scripts -->
	<script>
		function GraphOptionsClick() {
			document.getElementById("graphsettings").style.display = "block";
		}

		function off() {
		  	document.getElementById("graphsettings").style.display = "none";
		}

		function chargeModeBtnClick(chargeMode) {
	  		publish(chargeMode,"openWB/set/ChargeMode");
  		}
	</script>

	<!-- load Chart.js library -->
	<script src="js/Chart.bundle.js"></script>

	<!-- load mqtt library -->
	<script src = "js/mqttws31.js" ></script>

	<!-- load respective Chart.js definition -->
	<script src="themes/<?php echo $_COOKIE['openWBTheme'];?>/livechart.js"></script>
	<script src="themes/<?php echo $_COOKIE['openWBTheme'];?>/awattarchart.js"></script>

	$(document).ready(function(){

		<script>

			responsiveGaugeSettings = [
				{maxWidth: 400, width: 145, height: 145,
					options: {
						radius:65, marginTop: 30, shadowBlur: 3, titleTopPos: 0.28,
						titleTopSize: 7, titleBottomSize: 6, labelsValueSize: 10, labelsSize: 8
					}
				},
				{maxWidth: 575, width: 155, height: 155,
					options: {
						radius: 70, marginTop: 30, shadowBlur: 3, titleTopPos: 0.3,
						titleTopSize: 7, titleBottomSize: 7, labelsValueSize: 10, labelsSize: 8
					}
				},
				{maxWidth: 767, width: 220, height: 220,
					options: {
						radius: 95, marginTop: 20, shadowBlur: 5, titleTopPos: 0.4,
						titleTopSize: 11, titleBottomSize: 8, labelsValueSize: 10, labelsSize: 11
					}
				},
				{maxWidth: 870, width: 160, height: 160,
					options: {
						radius: 75, marginTop: 35, shadowBlur: 4, titleTopPos: 0.31,
						titleTopSize: 9, titleBottomSize: 7, labelsValueSize: 10, labelsSize: 9
					}
				},
				{maxWidth: 991, width: 180, height: 180,
					options: {
						radius: 85, marginTop: 35, shadowBlur: 4, titleTopPos: 0.38,
						titleTopSize: 10, titleBottomSize: 8, labelsValueSize: 11, labelsSize: 9
					}
				},
				{maxWidth: 1199, width: 200, height: 200,
					options: {
						radius: 92, marginTop: 40, shadowBlur: 6, titleTopPos: 0.36,
						titleTopSize: 12, titleBottomSize: 9, labelsValueSize: 12, labelsSize: 11
					}
				},
				{maxWidth: null, width: 220, height: 220,
					options: {
						radius: 102, marginTop: 35, shadowBlur: 6, titleTopPos: 0.38,
						titleTopSize: 14, titleBottomSize: 10, labelsValueSize: 13, labelsSize: 13}
				}
			];

			responsiveProgressbarSettings = [
				{maxWidth: 400, width: 4, height: 140, shadowBlur: 4,
					options: {
						textSize: 5, marginTop: 25, marginBottom: 15
					}
				},
				{maxWidth: 575, width: 4, height: 155, shadowBlur: 4,
					options: {
						textSize: 5, marginTop: 25, marginBottom: 17
					}
				},
				{maxWidth: 767, width: 6, height: 220,
					options: {
						textSize: 7, marginTop: 28, marginBottom: 30
					}
				},
				{maxWidth: 870, width: 5, height: 160,
					options: {
						textSize: 5, marginTop: 22, marginBottom: 10,
					}
				},
				{maxWidth: 991, width: 5, height: 180,
					options: {
						textSize: 6, marginTop: 25, marginBottom: 10,
					}
				},
				{maxWidth: 1199, width: 6, height: 200,
					options: {
						textSize: 7, marginTop: 30, marginBottom: 15
					}
				},
				{maxWidth: null, width: 8, height: 220,
					options: {
						textSize: 8, marginTop: 30, marginBottom: 20
					}
				}
			];

			gaugePV = new RGraph.Gauge({
				id: 'pvData',
				min: 0,
				max: <?php echo $pvDataScaleMax?>,
				value: 0,
				options: {
					marginLeft: 0,
					marginRight: 0,
					titleTop: 'kW',
					labelsCount: 2,
					labelsSpecific: ['0', '<?php echo $pvDataScaleMax/2000?>', '<?php echo $pvDataScaleMax/1000?>'],
					tickmarksLarge: 4,
					tickmarksSmall: 20,
					shadow: true,
					shadowColor: '#E9E9E9',
					backgroundColor: 'Gradient(white:#BEFEBE)',
					borderWidth: 1,
					borderInner: '#739B73',
					centerpinColor: '#8E8E8B',
					labelsValue: true,
					labelsValueBounding: false,
					labelsValueUnitsPost: ' W',
					labelsValueBold: true,
					labelsValueItalic: true,
					titleBottomPos: 0.61,
					titleBottomBold: true,
					adjustable: false,
					textAccessible: false,
					colorsRanges: [[0, <?php echo $pvDataScaleMax?>, 'green', 3]],
					anglesStart: RGraph.PI - 0.55,
					anglesEnd: RGraph.TWOPI + 0.55
				}
			}).draw().responsive(responsiveGaugeSettings);
			gaugePV.scaleCounter = defaultScaleCounter;  // Attribut zur Gauge hinzufügen

			gaugeBatt = new RGraph.Gauge({
				id: 'battData',
				min: <?php echo $battDataScaleMax*-1?>,
				max: <?php echo $battDataScaleMax?>,
				value: 0,
				options: {
					marginLeft: 0,
					marginRight: 0,
					titleTop: 'kW',
					labelsCount: 2,
					labelsSpecific: ['<?php echo $battDataScaleMax/-1000?>', '0', '<?php echo $battDataScaleMax/1000?>'],
					tickmarksLarge: 4,
					tickmarksSmall: 20,
					shadow: true,
					shadowColor: '#E9E9E9',
					backgroundColor: 'Gradient(white:#FCBE1E)',
					borderWidth: 1,
					borderInner: '#BA8C16',
					centerpinColor: '#8E8E8B',
					labelsValue: true,
					labelsValueBounding: false,
					labelsValueUnitsPost: ' W',
					labelsValueBold: true,
					labelsValueItalic: true,
					titleBottomPos: 0.61,
					titleBottomBold: true,
					adjustable: false,
					textAccessible: false,
					colorsRanges: [[<?php echo $battDataScaleMax*-1?>, 0, 'red', 3], [0, <?php echo $battDataScaleMax?>, 'green', 3]],
					anglesStart: RGraph.PI - 0.55,
					anglesEnd: RGraph.TWOPI + 0.55
				}
			}).draw().responsive(responsiveGaugeSettings);
			gaugeBatt.scaleCounter = defaultScaleCounter;  // Attribut zur Gauge hinzufügen

			progressBarSoC = new RGraph.VProgress({
				id: 'battSocData',
				min: 0,
				max: 100,
				value: 0,
				options: {
					marginLeft: 0,
					marginRight: 0,
					title: 'SoC',
					backgroundColor: 'black',
					colors: ['Gradient(red:yellow:green)'],
					textBold: true,
					textColor: '#E9E9E9',
					labelsPosition: 'right',
					labelsCount: 5,
					labelsBold: false,
					tickmarksOuterCount: 5
				}
			}).draw().responsive(responsiveProgressbarSettings);

			gaugeEVU = new RGraph.Gauge({
				id: 'evuData',
				min: <?php echo $evuDataScaleMax*-1?>,
				max: <?php echo $evuDataScaleMax?>,
				value: 0,
				options: {
					marginLeft: 0,
					marginRight: 0,
					titleTop: 'kW',
					labelsCount: 2,
					labelsSpecific: ['<?php echo $evuDataScaleMax/-1000?>', '0', '<?php echo $evuDataScaleMax/1000?>'],
					tickmarksLarge: 4,
					tickmarksSmall: 20,
					shadow: true,
					shadowColor: '#E9E9E9',
					backgroundColor: 'Gradient(white:#FEBEBE)',
					borderWidth: 1,
					borderInner: '#A07676',
					centerpinColor: '#8E8E8B',
					labelsValue: true,
					labelsValueBounding: false,
					labelsValueUnitsPost: ' W',
					labelsValueBold: true,
					labelsValueItalic: true,
					labelsValueSize: 17,
					titleBottomPos: 0.61,
					titleBottomBold: true,
					titleBottomSize: 11,
					adjustable: false,
					textAccessible: false,
					colorsRanges: [[<?php echo $evuDataScaleMax*-1?>, 0, 'red', 3], [0, <?php echo $evuDataScaleMax?>, 'green', 3]],
					anglesStart: RGraph.PI - 0.55,
					anglesEnd: RGraph.TWOPI + 0.55
				}
			}).draw().responsive(responsiveGaugeSettings);
			gaugeEVU.scaleCounter = defaultScaleCounter;  // Attribut zur Gauge hinzufügen

			gaugeHome = new RGraph.Gauge({
				id: 'homeData',
				min: 0,
				max: 1000,
				value: 0,
				options: {
					marginLeft: 0,
					marginRight: 0,
					titleTop: 'kW',
					labelsCount: 2,
					labelsSpecific: ['0', '0.5', '1'],
					tickmarksLarge: 4,
					tickmarksSmall: 20,
					shadow: true,
					shadowColor: '#E9E9E9',
					backgroundColor: 'Gradient(white:#B5F1FF)',
					borderWidth: 1,
					borderInner: '#6E939B',
					centerpinColor: '#8E8E8B',
					labelsValue: true,
					labelsValueBounding: false,
					labelsValueUnitsPost: ' W',
					labelsValueBold: true,
					labelsValueItalic: true,
					labelsValueSize: 17,
					adjustable: false,
					textAccessible: false,
					colorsRanges: [[0, 1000, 'green', 3]],
					colorsRedWidth: 0,
					colorsYellowWidth: 0,
					anglesStart: RGraph.PI - 0.55,
					anglesEnd: RGraph.TWOPI + 0.55
				}
			}).draw().responsive(responsiveGaugeSettings);
			gaugeHome.scaleCounter = defaultScaleCounter;  // Attribut zur Gauge hinzufügen

		</script>

		<!-- Data refresher -->
		<script src="themes/<?php echo $_COOKIE['openWBTheme'];?>/processAllMqttMsg.js?ver=1.0"></script>
		<script src="themes/<?php echo $_COOKIE['openWBTheme'];?>/livefunctions.js?ver=1.0"></script>
	});  <!-- end $(document).ready -->

</body>

</html>
