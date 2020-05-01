<!DOCTYPE html>
<html lang="de">

<head>
	<!-- standard theme for openWB -->
	<!-- 2020 Michael Ortenstein -->

	<title>openWB</title>
	<?php
	include $_SERVER['DOCUMENT_ROOT'].'/openWB/web/values.php';
	?>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0">
	<meta name="apple-mobile-web-app-capable" content="yes">
	<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
	<meta name="apple-mobile-web-app-title" content="openWB">
	<meta name="apple-mobile-web-app-status-bar-style" content="default">
	<link rel="apple-touch-startup-image" href="/openWB/web/img/favicons/splash1125x2436w.png"  />
	<link rel="apple-touch-startup-image" media="(-webkit-device-pixel-ratio: 3)" href="img/favicons/splash1125x2436w.png">
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
	<!-- important scripts to be loaded -->
	<script src="js/jquery-3.4.1.min.js"></script>
	<script src="js//bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
</head>

<body>
	<?php include $_SERVER['DOCUMENT_ROOT'].'/openWB/web/themes/standard/navbar.php'; ?>
	<input type="hidden" name="lastmanagement" id="lastmanagement" value="<?php echo trim($lastmanagementold); ?>" />
	<input type="hidden" name="lastmanagements2" id="lastmanagements2" value="<?php echo trim($lastmanagements2old); ?>" />
	<input type="hidden" name="speicherstat" id="speicherstat" value="<?php echo trim($speicherstatold); ?>" />
	<input type="hidden" name="lademlp1stat" id="lademlp1stat" value="<?php echo trim($lademstatold); ?>" />
	<input type="hidden" name="lademlp2stat" id="lademlp2stat" value="<?php echo trim($lademstats1old); ?>" />
	<input type="hidden" name="lademlp3stat" id="lademlp3stat" value="<?php echo trim($lademstats2old); ?>" />
	<input type="hidden" name="evuglaettungakt" id="evuglaettungakt" value="<?php echo trim($evuglaettungaktold); ?>" />
	<input type="hidden" name="nachtladenstate" id="nachtladenstate" value="<?php echo trim($nachtladenstate); ?>" />
	<input type="hidden" name="nachtladenstates1" id="nachtladenstates1" value="<?php echo trim($nachtladenstates1); ?>" />
	<input type="hidden" name="nlakt_nurpv" id="nlakt_nurpv" value="<?php echo trim($nlakt_nurpvold); ?>" />
	<input type="hidden" name="nlakt_sofort" id="nlakt_sofort" value="<?php echo trim($nlakt_sofortold); ?>" />
	<input type="hidden" name="nlakt_minpv" id="nlakt_minpv" value="<?php echo trim($nlakt_minpvold); ?>" />
	<input type="hidden" name="nlakt_standby" id="nlakt_standby" value="<?php echo trim($nlakt_standbyold); ?>" />
	<input type="hidden" name="lademodus" id="lademodus" value="<?php echo trim($lademodusold); ?>" />
	<input type="hidden" name="hausverbrauchstat" id="hausverbrauchstat" value="<?php echo trim($hausverbrauchstatold); ?>" />
	<input type="hidden" name="speicherpvui" id="speicherpvui" value="<?php echo trim($speicherpvuiold); ?>" />
	<input type="hidden" name="zielladenaktivlp1" id="zielladenaktivlp1" value="<?php echo trim($zielladenaktivlp1old); ?>" />
	<input type="hidden" name="sofortlm" id="sofortlm" value="<?php echo trim($lademodusold); ?>" />
	<input type="hidden" name="heutegeladen" id="heutegeladen" value="<?php echo trim($heutegeladenold); ?>" />

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
	</script>

	<div class="container">

		<div class="row justify-content-center">
			<div class="col-sm-6 pvInfoStyle" style="background-color:#befebe;">
				PV: <span id="pvdiv"></span>
			</div>
			<div id="evudiv" class="col-sm-6 pvInfoStyle" style="background-color:#febebe;" >
				EVU: <span id="bezugdiv"></span>
			</div>
		</div>

		<?php
		if ( $hausverbrauchstatold == 1 ) {
			?>
		<div class="row justify-content-center">
			<div class="col-sm-12 pvInfoStyle" style="background-color:#fefedf;">
				Hausverbrauch: <span id="hausverbrauchdiv"></span>
			</div>
		</div>
			<?php
		}
		// if speichermodul is not "none", show the info
		if ( strcmp(trim($speicherstatold),"none") != 0 ) {
			?>
		<div id="speicherdiv" class="row justify-content-center">
			<div class="col-sm-12 pvInfoStyle" style="background-color:#fcbe1e;">
				Speicher: <span id="speicherleistungdiv"></span><span id="speichersocdiv"></span>
			</div>
		</div>
			<?php
		}  // end if speichervorhanden

		if ( ($hook1_aktivold == 1 || $hook2_aktivold == 1 || $hook3_aktivold == 1) ) {
			// if hooks for external devices are configured, show div
			?>
		<div id="webhooksdiv" class="row justify-content-center extDeviceInfoStyle bg-light">
			<?php
			// generate code for all configured hooks
			for($i=1; $i <= 3; $i++) {
				if (${"hook".$i."_aktivold"} == 1) {
					$divId = "hook".$i."div";
					?>
			<div id="<?php echo $divId; ?>" class="col-3 m-1">
				ext. Gerät <?php echo $i; ?>
			</div>
					<?php
				}  // end if
			}  // end for
			?>
		</div>
			<?php
			}  // end if hook configured
		?>

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
				?>
		<!-- data-row for charging Point '<?php echo $i; ?>' -->
		<div id="lp<?php echo $i; ?>div" class="row no-gutter py-1 py-md-0 justify-content-center chargePointInfoStyle" style="display: none;">
			<div class="col-4">
				<span class="cursor-pointer" onclick="lp<?php echo $i; ?>enabledclick()">
					<span class="fas fa-xs fa-key" id="lp<?php echo $i; ?>AutolockConfiguredSpan" style="display: none;"></span> <!-- placeholder for autolock icons -->
					<span class="fa" id="lp<?php echo $i; ?>enableddiv"></span>
					<span class="nameLp<?php echo $i; ?>"></span>
				</span>
				<span class="fa" id="plugstatlp<?php echo $i; ?>div"></span>
				<span class="fa" id="zielladenaktivlp<?php echo $i; ?>div"></span>
				<span class="fa" id="nachtladenaktivlp<?php echo $i; ?>div"></span>
			</div>
			<div class="col-3">
				<span id="actualPowerLp<?php echo $i; ?>div"></span>
                                <span id="phasesInUse<?php echo $i; ?>div"></span>
				<span id="targetCurrentLp<?php echo $i; ?>div"></span>
			</div>
			<div class="col-3 text-center">
				<span id="energyChargedLp<?php echo $i; ?>div"></span>
			</div>
			<!-- standard: soc not configured for charging point -->
			<div id="socNotConfiguredLp<?php echo $i; ?>div" class="col-2">
				--
			</div>
			<div id="socConfiguredLp<?php echo $i; ?>div" class="col-2" style="display: none;">
				<span id="socLp<?php echo $i; ?>"></span>
			</div>
		</div>
				<?php
			}
		?>

		<div id="powerAllLpdiv" class="row justify-content-center" style="display: none;">
			<div class="col-sm-5 chargePointInfoStyle">
				Gesamt-Ladeleistung: <span id="powerAllLpspan"></span>
			</div>
		</div>

		<hr style="color: white;">

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
				&nbsp;
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
				&nbsp;
			</div>
			<div class="col-sm-2 py-1">
				<button id="stopBtn" type="button" class="btn btn-lg btn-block btn-red myButtonStyle" onclick="chargeModeBtnClick(this.value)" value="3">Stop</button>
			</div>
			<div class="d-none d-sm-block">
				&nbsp;
			</div>
			<div class="col-sm-4 order-first order-sm-last py-1">
				<button id="pvBtn" type="button" class="btn btn-lg btn-block btn-red myButtonStyle" onclick="chargeModeBtnClick(this.value)" value="2">PV</button>
			</div>
		</div>
		<div id="nurpv70div" class="row no-gutters justify-content-center" style="display: none;">
			<div class="col-sm-4 py-1">
				<button id="nurpv70Btn" type="button" class="btn btn-lg btn-block myButtonStyle" onclick="changenurpv70Click()">70% beachten</button>
			</div>
		</div>
		<div id="speicherpvuidiv" class="row no-gutters justify-content-center">
			<div class="col-sm-4 py-1">
				<?php
					if ($speicherpveinbeziehenold == 0) {
						?>
				<a href="./tools/changelademodus.php?pveinbeziehen=1" class="btn btn-lg btn-block btn-green myButtonStyle">Speichervorrang</a>
						<?php
					} else {
						?>
				<a href="./tools/changelademodus.php?pveinbeziehen=0" class="btn btn-lg btn-block btn-green myButtonStyle">EV Vorrang</a>
						<?php
					}
				?>
			</div>
		</div>

		<hr style="color: white;">

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
				<hr style="color: white;">
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
						<input type="range" min="-8" max="12" step="0.10" name="awattar1s" id="awattar1s" class="custom-range">
					</div>
					<div class="col-2 regularTextStyle">
						<label for="awattar1s">Maximaler Preis: <span id="awattar1l"></span>Cent/kWh</label>
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
				<hr style="color: white;">
			</div>
			<div class="row justify-content-center">
				<h3>Sofortladen Ladeziel-Einstellungen</h3>
			</div>

			<div class="row justify-content-center">
				<div class="col-4 regularTextStyle">
					<label for="msmoduslp1"></label>
					<select name="msmoduslp1" id="msmoduslp1">
						<option <?php if($msmoduslp1old == 0) echo 'selected' ?> value="0">unbegrenzt</option>
						<option <?php if($msmoduslp1old == 1) echo 'selected' ?> value="1">Lademenge</option>
						<option <?php if($msmoduslp1old == 2) echo 'selected' ?> value="2">SoC</option>
					</select><br>
					<span id="msmodusmlp1">
						<label for="lademlp1">Lademenge</label>
						<select name="lademlp1" id="lademlp1">
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
						</select> kWh<br>
						<button onclick="rslp1()">Reset</button>
					</span>
					<span id="msmodusslp1"><br><br>
						<label for="sofortsoclp1">SoC</label>
						<select name="sofortsoclp1" id="sofortsoclp1">
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
					</span>
				</div>

				<div class="col-4 regularTextStyle" id="ladepunkts111111div">
					<label for="msmoduslp2"></label>
					<select name="msmoduslp2" id="msmoduslp2">
						<option <?php if($msmoduslp2old == 0) echo 'selected' ?> value="0">unbegrenzt</option>
						<option <?php if($msmoduslp2old == 1) echo 'selected' ?> value="1">Lademenge</option>
						<option <?php if($msmoduslp2old == 2) echo 'selected' ?> value="2">SoC</option>
					</select>
					<div id="msmodusmlp2">
						<label for="lademlp2">Lademenge</label>
						<select name="lademlp2" id="lademlp2">
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
						</select> kWh<br>
						<button onclick="rslp2()">Reset</button>
					</div>
					<span id="msmodusslp2">
						<label for="sofortsoclp2">SoC</label>
						<select name="sofortsoclp2" id="sofortsoclp2">
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
					</span>
				</div>

				<div class="col-4 regularTextStyle" id="ladepunkts222222div">
					<label for="lademlp3check"></label>
					<select name="lademlp3check" id="lademlp3check">
						<option <?php if($lademstats2old == 0) echo 'selected' ?> value="0">unbegrenzt</option>
						<option <?php if($lademstats2old == 1) echo 'selected' ?> value="1">Lademenge</option>
					</select><br>
					<span id="msmodusmlp3">
						<label for="lademlp3">Lademenge</label>
						<select name="lademlp3" id="lademlp3">
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
						</select> kWh<br>
						<button onclick="rslp3()">Reset</button>
					</span>
					<span id="msmodusnlp3"></span>
				</div>
	  		</div>

			<div class="row justify-content-center">
				<div class="col-10">
					<hr style="color: white;">
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
					<label for="sofortlllp1s">LP 1: <span id="sofortlllp1l"></span>A</label>
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
					<label for="sofortlllp2s">LP 2: <span id="sofortlllp2l"></span>A</label>
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
					<label for="sofortlllp3s">LP 3: <span id="sofortlllp3l"></span>A</label>
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
					<label for="sofortlllp4s">LP 4: <span id="sofortlllp4l"></span>A</label>
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
					<label for="sofortlllp5s">LP 5: <span id="sofortlllp5l"></span>A</label>
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
					<label for="sofortlllp6s">LP 6: <span id="sofortlllp6l"></span>A</label>
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
					<label for="sofortlllp7s">LP 7: <span id="sofortlllp7l"></span>A</label>
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
					<label for="sofortlllp8s">LP 8: <span id="sofortlllp8l"></span>A</label>
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
					<button type="submit" class="btn btn-lg btn-block btn-green myButtonStyle">Save</button>
				</div>
			</div>

		</form>

		<!-- end old code-->



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
					<input type="button" value="Renew MQTT" onclick="renewMQTTclick()"/><br>
				</div>
			</div>
			<hr>
			<div class="row">
				<div class="col-sm-12">
					<input type="button" value="Schließen" onclick="off()"/>
				</div>
			</div>
		</div>

		</div>
	</div><!-- container -->
	<footer class="footer bg-dark text-light font-small">
		<!-- no text for footer -->
	</footer>
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
		function changenurpv70Click() {
			if ( nurpv70status == 0 ) {
				publish("1","openWB/set/NurPV70Status");
			} else {
				publish("0","openWB/set/NurPV70Status");
			}
		}
	</script>

	<!-- load Chart.js library -->
	<script src="js/Chart.bundle.js"></script>

	<!-- load mqtt library -->
	<script src = "js/mqttws31.js" ></script>

	<!-- load respective Chart.js definition -->
	<script src="themes/<?php echo $themeCookie ?>/livechart.js?ver=1.0"></script>
	<script src="themes/<?php echo $themeCookie ?>/awattarchart.js?ver=1.0"></script>
	<!-- Data refresher -->
	<script src="themes/<?php echo $themeCookie ?>/processAllMqttMsg.js?ver=1.0"></script>
	<script src="themes/<?php echo $themeCookie ?>/livefunctions.js?ver=1.0"></script>
</body>

</html>
