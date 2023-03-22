<!DOCTYPE html>
<html lang="de">
	<head>
		<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1 maximum-scale=1,user-scalable=0">
		<meta name="apple-mobile-web-app-capable" content="yes">
		<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
		<meta name="apple-mobile-web-app-title" content="OpenWB">
		<meta name="apple-mobile-web-app-status-bar-style" content="default">
		<link rel="apple-touch-startup-image" href="/openWB/web/img/favicons/splash1125x2436w.png" />
		<meta name="apple-mobile-web-app-title" content="openWB">
		<title>openWB</title>
		<meta name="description" content="openWB" />
		<meta name="keywords" content="openWB" />
		<meta name="author" content="Kevin Wieland" />
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
		<link rel="apple-touch-startup-image" href="img/loader.gif">
		<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
		<meta name="theme-color" content="#ffffff">
		<meta name="google" content="notranslate">
		<script src="js/jquery-1.11.1.min.js"></script>
		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
		<!-- Elegant Icons -->
		<!-- Main style -->
		<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
		<!-- Main style -->
		<link rel="stylesheet" type="text/css" href="css/cardio.css">
		<!-- Data refresher -->
		<script src="livefunctions.js?ver=20201201"></script>
		<script>
			$(document).ready(function(){
				/**
				 * detect touch devices and map contextmenu (long press) to normal click
				 */
				$('body').on("contextmenu", function(event){
					console.log("Contextmenu triggered");
					if( ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0) ) {
						console.log("Click event generated");
						$(event.target).trigger("click"); // fire a click event
						event.preventDefault();
					}
				});
			});
		</script>
		<style>
			/* prevent touch gestures */
			html, body {
				overscroll-behavior: none;
			}
		</style>
	</head>
	<body>
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

		<!-- begin simplemode.html -->
		<?php include ("gaugevalues.php"); ?>
		<!-- load Chart.js library -->
		<script src="js/Chart.bundle.js"></script>
		<script src="livechart_chartjs.js"></script>
		<script src="js/mqttws31.js" ></script>
		<link rel="stylesheet" href="display/simple/arrow.css">
		<link rel="stylesheet" href="display/simple/pin.css">

		<input type="hidden" name="displayevumax" id="displayevumax" value="<?php echo trim($displayevumaxold); ?>" />
		<input type="hidden" name="displaypvmax" id="displaypvmax" value="<?php echo trim($displaypvmaxold); ?>" />
		<input type="hidden" name="displayspeichermax" id="displayspeichermax" value="<?php echo trim($displayspeichermaxold); ?>" />
		<input type="hidden" name="displayhausanzeigen" id="displayhausanzeigen" value="<?php echo trim($displayhausanzeigenold); ?>" />
		<input type="hidden" name="displayhausmax" id="displayhausmax" value="<?php echo trim($displayhausmaxold); ?>" />
		<input type="hidden" name="displaylp1max" id="displaylp1max" value="<?php echo trim($displaylp1maxold); ?>" />
		<input type="hidden" name="displaylp2max" id="displaylp2max" value="<?php echo trim($displaylp2maxold); ?>" />
		<input type="hidden" name="displaypinaktiv" id="displaypinaktiv" value="<?php echo trim($displaypinaktivold); ?>" />
		<input type="hidden" name="displaypincode" id="displaypincode" value="<?php echo trim($displaypincodeold); ?>" />

		<div id="main">
			<div style="font-size: 18px; height: 20px; top: 0px; left: 740px; text-align:center; position: absolute; width: 65px; color: white;" id="theclock"></div>
			<div style="color: white; top: 0px; left: 10px; position: absolute; font-size: 18px; width: 810px;">
				<div class="row col-xs-12 text-center" style="height: 120px;">
					<div class="col-xs-2">
						<img src="img/icons/electric-tower.svg" alt="Electric Tower" style="filter: invert(1); -webkit-filter: invert(1);" width="40vw" >
					</div>
					<div class="col-xs-3">
						<div id="speedevu">
							<div id="arrowevu"></div>
						</div>
						<span id="bezugdiv"></span>
					</div>
					<div class="col-xs-2">
						<i class="fas fa-2x fa-home swhite" style="color: white;"></i><br>
						<span id="hausverbrauchdiv"></span>
					</div>
					<i class="fas fa-2x fa-solar-panel" style="color: green;"></i><br>
					<span id="pvdiv"></span>
				</div>

				<div class="row col-xs-12 text-center" style="height: 70px;">
					<div class="col-xs-2">
						<span id="lp1enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp1enabledclick()"></span><span id="stationlp1" class="fas fa-2x fa-charging-station"></span>
					</div>
					<div class="col-xs-3">
						<div id="speedlp1">
							<div id="arrowlp1"></div>
						</div>
						<span id="lllp1div"></span> <span id="pluggedladungbishergeladenlp1div"></span>kWh
					</div>
					<div class="col-xs-1">
						<i id="carlp1" class="fas fa-2x fa-car-side"></i><br><span class="nameLp1"></span>
					</div>
					<div class="col-xs-2">
						<span id="lp2enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp2enabledclick()"></span><span id="stationlp2" class="fas fa-2x fa-charging-station"></span>
					</div>
					<div class="col-xs-3">
						<div id="speedlp2">
							<div id="arrowlp2"></div>
						</div>
						<span id="lllp2div"></span> <span id="pluggedladungbishergeladenlp2div"></span>kWh
					</div>
					<div class="col-xs-1">
						<i id="carlp2" class="fas fa-2x fa-car-side"></i><br>
						<span class="nameLp2"></span>
					</div>
				</div>
				<div class="row col-xs-12 text-center" style="height: 70px;">
					<div id="lp3div">
						<div class="col-xs-2">
							<span id="lp3enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp3enabledclick()"></span><span id="stationlp3" class="fas fa-2x fa-charging-station"></span>
						</div>
						<div class="col-xs-3">
							<div id="speedlp3">
								<div id="arrowlp3"></div>
							</div>
							<span id="lllp3div"></span> <span id="pluggedladungbishergeladenlp3div"></span>kWh
						</div>
						<div class="col-xs-1">
							<i id="carlp3" class="fas fa-2x fa-car-side"></i><br><span class="nameLp3"></span>
						</div>
					</div>
					<div id="lp4div">
						<div class="col-xs-2">
							<span id="lp4enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp4enabledclick()"></span><span id="stationlp4" class="fas fa-2x fa-charging-station"></span>
						</div>
						<div class="col-xs-3">
							<div id="speedlp4">
								<div id="arrowlp4"></div>
							</div>
							<span id="lllp4div"></span> <span id="pluggedladungbishergeladenlp4div"></span>kWh
						</div>
						<div class="col-xs-1">
							<i id="carlp4" class="fas fa-2x fa-car-side"></i><br><span class="nameLp4"></span>
						</div>
					</div>
				</div>
				<div class="row col-xs-12 text-center" style="height: 70px;">
					<div id="lp5div">
						<div class="col-xs-2">
							<span id="lp5enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp5enabledclick()"></span><span id="stationlp5" class="fas fa-2x fa-charging-station"></span>
						</div>
						<div class="col-xs-3">
							<div id="speedlp5">
								<div id="arrowlp5"></div>
							</div>
							<span id="lllp5div"></span> <span id="pluggedladungbishergeladenlp5div"></span>kWh
						</div>
						<div class="col-xs-1">
							<i id="carlp5" class="fas fa-2x fa-car-side"></i><br>
							<span class="nameLp5"></span>
						</div>
					</div>
					<div id="lp6div">
						<div class="col-xs-2">
							<span id="lp6enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp6enabledclick()"></span><span id="stationlp6" class="fas fa-2x fa-charging-station"></span>
						</div>
						<div class="col-xs-3">
							<div id="speedlp6">
								<div id="arrowlp6"></div>
							</div>
							<span id="lllp6div"></span> <span id="pluggedladungbishergeladenlp6div"></span>kWh
						</div>
						<div class="col-xs-1">
							<i id="carlp6" class="fas fa-2x fa-car-side"></i><br><span class="nameLp6"></span>
						</div>
					</div>
				</div>
				<div class="row col-xs-12 text-center" style="height: 70px;">
					<div id="lp7div">
						<div class="col-xs-2">
							<span id="lp7enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp7enabledclick()"></span><span id="stationlp7" class="fas fa-2x fa-charging-station"></span>
						</div>
						<div class="col-xs-3">
							<div id="speedlp7">
								<div id="arrowlp7"></div>
							</div>
							<span id="lllp7div"></span> <span id="pluggedladungbishergeladenlp7div"></span>kWh
						</div>
						<div class="col-xs-1">
							<i id="carlp7" class="fas fa-2x fa-car-side"></i><br>
							<span class="nameLp7"></span>
						</div>
					</div>
					<div id="lp8div">
						<div class="col-xs-2">
							<span id="lp8enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp8enabledclick()"></span><span id="stationlp8" class="fas fa-2x fa-charging-station"></span>
						</div>
						<div class="col-xs-3">
							<div id="speedlp8">
								<div id="arrowlp8"></div>
							</div>
							<span id="lllp8div"></span> <span id="pluggedladungbishergeladenlp8div"></span>kWh
						</div>
						<div class="col-xs-1">
							<i id="carlp8" class="fas fa-2x fa-car-side"></i><br>
							<span class="nameLp8"></span>
						</div>
					</div>
				</div>
			</div>

			<div class="row col-xs-12 text-center" style="font-size: 15px; height: 20px; top: 320px; left: 0px; position: absolute; width: 820px; color: white; text-align:center;">
				<div class="row">
					<div id="lastregelungaktivdiv" class="col-xs-12 text-center" style="color:#990000;font-size: 30px"></div>
				</div>
			</div>

			<div class="row col-xs-12 text-center" style="font-size: 15px; height: 15px; top: 410px; left: 40px; position: absolute; width: 800px; color: white; text-align:center;"> 
				<div class=" col-xs-1"></div> 
				<div class="col-xs-2">
					<div id="sofortllbtn">
						<input type="submit" class="1sofortll btn btn-blue"  name="sofortllbtn" value="Ladestrom">
					</div>
				</div>
				<div class="col-xs-2"></div>
				<div class="col-xs-2"></div>
				<div class="col-xs-2"></div> 
				<div class="col-xs-1"></div>
			</div>
		</div>

		<div id="sofortll">
			<div class="col-xs-12 text-center" style="font-size: 22px; height: 10px; top: 10px; left: 10px; position: absolute; width: 750px; color: white; text-align:left;">
				<div id="slider1div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min="<?php echo trim($minimalstromstaerkeold); ?>" max="<?php echo trim($maximalstromstaerkeold); ?>" step="1" name="sofortlllp1s" id="sofortlllp1s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 1: <span id="sofortlllp1l"></span>A</label>  <span class="fa fa-save" style="cursor: pointer;" onclick="lp1DirectChargeAmpsClick()"></span>
					</div>
					<script>
						var slider1 = document.getElementById("sofortlllp1s");
						var output1 = document.getElementById("sofortlllp1l");
						output1.innerHTML = slider1.value;
						slider1.oninput = function() {
							output1.innerHTML = this.value;
						}
					</script>
				</div>
				<div id="slider2div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min="<?php trim($minimalstromstaerkeold); ?>" max="<?php trim($maximalstromstaerkeold); ?>" step="1" name="sofortlllp2s" id="sofortlllp2s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 2: <span id="sofortlllp2l"></span>A</label>  <span class="fa fa-save" style="cursor: pointer;" onclick="lp2DirectChargeAmpsClick()"></span>
					</div>
					<script>
						var slider2 = document.getElementById("sofortlllp2s");
						var output2 = document.getElementById("sofortlllp2l");
						output2.innerHTML = slider2.value;
						slider2.oninput = function() {
							output2.innerHTML = this.value;
						}
					</script>
				</div>
				<div id="slider3div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min="<?php trim($minimalstromstaerkeold); ?>" max="<?php trim($maximalstromstaerkeold); ?>" step="1" name="sofortlllp3s" id="sofortlllp3s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 3: <span id="sofortlllp3l"></span>A</label>  <span class="fa fa-save" style="cursor: pointer;" onclick="lp3DirectChargeAmpsClick()"></span>
					</div>
					<script>
						var slider3 = document.getElementById("sofortlllp3s");
						var output3 = document.getElementById("sofortlllp3l");
						output3.innerHTML = slider3.value;
						slider3.oninput = function() {
							output3.innerHTML = this.value;
						}
					</script>
				</div>
				<div id="slider4div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min="<?php trim($minimalstromstaerkeold); ?>" max="<?php trim($maximalstromstaerkeold); ?>" step="1" name="sofortlllp4s" id="sofortlllp4s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 4: <span id="sofortlllp4l"></span>A</label>  <span class="fa fa-save" style="cursor: pointer;" onclick="lp4DirectChargeAmpsClick()"></span>
					</div>
					<script>
						var slider4 = document.getElementById("sofortlllp4s");
						var output4 = document.getElementById("sofortlllp4l");
						output4.innerHTML = slider4.value;
						slider4.oninput = function() {
							output4.innerHTML = this.value;
						}
					</script>
				</div>
				<div id="slider5div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min="<?php trim($minimalstromstaerkeold); ?>" max="<?php trim($maximalstromstaerkeold); ?>" step="1" name="sofortlllp5s" id="sofortlllp5s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 5: <span id="sofortlllp5l"></span>A</label>  <span class="fa fa-save" style="cursor: pointer;" onclick="lp5DirectChargeAmpsClick()"></span>
					</div>
					<script>
						var slider5 = document.getElementById("sofortlllp5s");
						var output5 = document.getElementById("sofortlllp5l");
						output5.innerHTML = slider5.value;
						slider5.oninput = function() {
							output5.innerHTML = this.value;
						}
					</script>
				</div>
				<div id="slider6div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min="<?php trim($minimalstromstaerkeold); ?>" max="<?php trim($maximalstromstaerkeold); ?>" step="1" name="sofortlllp6s" id="sofortlllp6s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 6: <span id="sofortlllp6l"></span>A</label>  <span class="fa fa-save" style="cursor: pointer;" onclick="lp6DirectChargeAmpsClick()"></span>
					</div>
					<script>
						var slider6 = document.getElementById("sofortlllp6s");
						var output6 = document.getElementById("sofortlllp6l");
						output6.innerHTML = slider6.value;
						slider6.oninput = function() {
							output6.innerHTML = this.value;
						}
					</script>
				</div>
				<div id="slider7div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min="<?php trim($minimalstromstaerkeold); ?>" max="<?php trim($maximalstromstaerkeold); ?>" step="1" name="sofortlllp7s" id="sofortlllp7s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 7: <span id="sofortlllp7l"></span>A</label>  <span class="fa fa-save" style="cursor: pointer;" onclick="lp7DirectChargeAmpsClick()"></span>
					</div>
					<script>
						var slider7 = document.getElementById("sofortlllp7s");
						var output7 = document.getElementById("sofortlllp7l");
						output7.innerHTML = slider7.value;
						slider7.oninput = function() {
							output7.innerHTML = this.value;
						}
					</script>
				</div>
				<div id="slider8div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min="<?php trim($minimalstromstaerkeold); ?>" max="<?php trim($maximalstromstaerkeold); ?>" step="1" name="sofortlllp8s" id="sofortlllp8s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 8: <span id="sofortlllp8l"></span>A</label>  <span class="fa fa-save" style="cursor: pointer;" onclick="lp8DirectChargeAmpsClick()"></span>
					</div>
					<script>
						var slider8 = document.getElementById("sofortlllp8s");
						var output8 = document.getElementById("sofortlllp8l");
						output8.innerHTML = slider8.value;
						slider8.oninput = function() {
							output8.innerHTML = this.value;
						}
					</script>
				</div>
			</div>

			<div class="row col-xs-12 text-center" style="font-size: 12px; height: 10px; top: 430px; left: 50px; position: absolute; width: 750px; color: white; text-align:center;"> 
				<div class=" col-xs-8"></div>
				<div class=" col-xs-4"> 
					<input type="submit" class="1zurueck btn-blue btn btn-block" style="height: 20px; line-height: 5px !important;" name="zurueck" value="Zurück">
				</div>
			</div>
		</div>

		<div id="pin">
			<div class="dots">
				<div class="dot"></div>
				<div class="dot"></div>
				<div class="dot"></div>
				<div class="dot"></div>
			</div>
			<p>PIN</p>
			<div class="numbers">
				<div class="number">1</div>
				<div class="number">2</div>
				<div class="number">3</div>
				<div class="number">4</div>
				<div class="number">5</div>
				<div class="number">6</div>
				<div class="number">7</div>
				<div class="number">8</div>
				<div class="number">9</div>
			</div>
		</div>
		<script>
			function startTime() {
				var today = new Date();
				var h = today.getHours();
				var m = today.getMinutes();
				m = checkTime(m);
				document.getElementById('theclock').innerHTML =
				h + ":" + m;
				var t = setTimeout(startTime, 5000);
			}
			function checkTime(i) {
				if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
				return i;
			}

			startTime();
			$('#pin').hide();

			var displayhausmax = <?php echo trim($displayhausmaxold); ?>;
			var displaylp2max = <?php echo trim($displaylp2maxold); ?>;
			var displaylp1max = <?php echo trim($displaylp1maxold); ?>;
			var displaypvmax = <?php echo trim($displaypvmaxold); ?>;
			var displayevumax = <?php echo trim($displayevumaxold); ?>;
			var displayspeichermax = <?php echo trim($displayspeichermaxold); ?>;
			var displayhausanzeigen = <?php echo trim($displayhausanzeigenold); ?>;
			var displaypincode = <?php echo trim($displaypincodeold); ?>;
			var displaypinaktiv = <?php echo trim($displaypinaktivold); ?>;
			var lastmanagementold = <?php echo trim($lastmanagementold); ?>;

			if ( displayhausanzeigen == '1') {
				$('#hausanzeigen').show();
			} else {
				$('#hausanzeigen').hide();
			}
			if ( lastmanagementold == '1') {
				$('#lp2anzeigen').show();
			} else {
				$('#lp2anzeigen').hide();
			}

			var dash = 1;
			var displaylock = 1;

			function execnurpv(){
				var ajaxurl = 'tools/changelademodusd.php?pvuberschuss=1';
				$.post(ajaxurl, 'nurpv', function (response) {
					$('.actstat2 .btn').addClass("btn-green");
					$('.actstat3 .btn').addClass("btn-red");
					$('.actstat .btn').addClass("btn-red");
					$('.actstat1 .btn').addClass("btn-red");
					$('.actstat .btn').removeClass("btn-green");
					$('.actstat2 .btn').removeClass("btn-red");
					$('.actstat3 .btn').removeClass("btn-green");
					$('.actstat1 .btn').removeClass("btn-green");
					$('.actstat4 .btn').addClass("btn-red");
					$('.actstat4 .btn').removeClass("btn-green");
					$('#sofortllbtn').hide();
				});
			}

			function execminpv(){
				var ajaxurl = 'tools/changelademodusd.php?minundpv=1';
				$.post(ajaxurl, 'minpv', function (response) {
					$('.actstat2 .btn').addClass("btn-red");
					$('.actstat3 .btn').addClass("btn-red");
					$('.actstat .btn').addClass("btn-red");
					$('.actstat1 .btn').addClass("btn-green");
					$('.actstat .btn').removeClass("btn-green");
					$('.actstat2 .btn').removeClass("btn-green");
					$('.actstat3 .btn').removeClass("btn-green");
					$('.actstat1 .btn').removeClass("btn-red");
					$('.actstat4 .btn').addClass("btn-red");
					$('.actstat4 .btn').removeClass("btn-green");
					$('#sofortllbtn').hide();
				});
			}

			function execstop(){
				var ajaxurl = 'tools/changelademodusd.php?stop=1';
				$.post(ajaxurl, 'stop', function (response) {
					$('.actstat2 .btn').addClass("btn-red");
					$('.actstat3 .btn').addClass("btn-green");
					$('.actstat .btn').addClass("btn-red");
					$('.actstat1 .btn').addClass("btn-red");
					$('.actstat .btn').removeClass("btn-green");
					$('.actstat2 .btn').removeClass("btn-green");
					$('.actstat3 .btn').removeClass("btn-red");
					$('.actstat1 .btn').removeClass("btn-green");
					$('.actstat4 .btn').addClass("btn-red");
					$('.actstat4 .btn').removeClass("btn-green");
					$('#sofortllbtn').hide();
				});
			}

			function execstandby(){
				var ajaxurl = 'tools/changelademodusd.php?semistop=1';
				$.post(ajaxurl, 'standby', function (response) {
					$('.actstat2 .btn').addClass("btn-red");
					$('.actstat3 .btn').addClass("btn-red");
					$('.actstat .btn').addClass("btn-red");
					$('.actstat1 .btn').addClass("btn-red");
					$('.actstat .btn').removeClass("btn-green");
					$('.actstat2 .btn').removeClass("btn-green");
					$('.actstat3 .btn').removeClass("btn-green");
					$('.actstat1 .btn').removeClass("btn-green");
					$('.actstat4 .btn').addClass("btn-green");
					$('.actstat4 .btn').removeClass("btn-red");
					$('#sofortllbtn').hide();
				});
			}

			function execsofort(){
				var ajaxurl = 'tools/changelademodusd.php?jetzt=1';
				$.post(ajaxurl, 'sofort', function (response) {
					$('.actstat2 .btn').addClass("btn-red");
					$('.actstat3 .btn').addClass("btn-red");
					$('.actstat .btn').addClass("btn-green");
					$('.actstat1 .btn').addClass("btn-red");
					$('.actstat .btn').removeClass("btn-red");
					$('.actstat2 .btn').removeClass("btn-green");
					$('.actstat3 .btn').removeClass("btn-green");
					$('.actstat1 .btn').removeClass("btn-green");
					$('.actstat4 .btn').addClass("btn-red");
					$('.actstat4 .btn').removeClass("btn-green");
					$('#sofortllbtn').show();
				});
			}

			var displaytheme = <?php echo trim($displaythemeold); ?>;

			$('#gaugediv').hide();
			$('#symboldiv').hide();
			$('#dergraph').hide();
			$('#einstellungen').hide();
			$('#sofortll').hide();
			$('#sofortllbtn').show();
			if ( displaytheme == 3 ) {
				$('#gaugediv').show();
			}
			if ( displaytheme == 1 ) {
				$('#symboldiv').show();
			}

			var stop = 0;
			var sofort = 0;
			var standby = 0;
			var nurpv = 0;
			var minpv = 0;
			var lock = 0;

			$(document).ready(function(){

				$('.1einstellungen').click(function(){
					$('#main').hide();
					dash = 0;
					$('#einstellungen').show();
					$('#status').show();
					$('#hilfe').hide();
				});

				$('.1graph').click(function(){
					$('#main').hide();
					dash = 0;
					$('#dergraph').show();
				});

				$('.1sofortll').click(function(){
					var llsolllp1;
					$('#main').hide();
					dash = 0;
					$('#sofortll').show();
				});

				$('.1zurueck').click(function(){
					dash = 1;
					$('#dergraph').hide();
					$('#einstellungen').hide();
					$('#sofortll').hide();
					$('#main').show();
				});

				$('.1hilfe').click(function(){
					dash = 1;
					$('#dergraph').hide();
					$('#einstellungen').show();
					$('#sofortll').hide();
					$('#main').hide();
					$('#hilfe').show();
					$('#status').hide();
				});

				$('.1stop').click(function(){
					if ( lock == 0 ) {
						if ( displaypinaktiv == 1){
							$('#pin').show();
							lock = 1;
							stop = 1;
						} else {
							execstop();
						}
					}
				});

				$('.1sofort').click(function(){
					if ( lock == 0 ) {
					if ( displaypinaktiv == 1){
						$('#pin').show();
						lock = 1;
							sofort = 1;
						} else {
							execsofort();
						}
					}
				});

				$('.1standby').click(function(){
					if ( lock == 0 ) {
						if ( displaypinaktiv == 1){
							$('#pin').show();
							lock = 1;
							standby = 1;
						} else {
							execstandby();
						}
					}
				});

				$('.1nurpv').click(function(){
					if ( lock == 0 ) {
						if ( displaypinaktiv == 1){
							lock = 1;
							nurpv = 1;
							$('#pin').show();
						} else {
							execnurpv();
						}
					}
				});

				$('.1minpv').click(function(){
					if ( lock == 0 ) {
						if ( displaypinaktiv == 1){
							lock = 1;
							minpv = 1;
							$('#pin').show();
						} else {
							execminpv();
						}
					}
				});

			});

			(function () {
				var input = '',
				correct = displaypincode.toString().substr(0, 4);

				var dots = document.getElementsByClassName('dot'),
				numbers = document.getElementsByClassName('number');
				dots = Array.from(dots);
				numbers = Array.from(numbers);

				var numbersBox = document.getElementsByClassName('numbers')[0];
				$(numbersBox).on('click', '.number', function (evt) {
					var number = $(this);
					input += number.index() + 1;
					$(dots[input.length - 1]).addClass('active');
					if (input.length >= 4) {
					if (input !== correct) {
						dots.forEach(dot => $(dot).addClass('wrong'));
						$(document.body).addClass('wrong');
						setTimeout(function(){  
							$('#pin').hide(); 
						}, 1400);
					lock = 0;
					} else {
						dots.forEach(dot => $(dot).addClass('correct'));
						$(document.body).addClass('correct');
						if ( stop == 1 ) {
							stop = 0;
							execstop();
						}
						if ( sofort == 1 ) {
							sofort = 0;
							execsofort();
						}
						if ( standby == 1 ) {
							standby = 0;
							execstandby();
						}
						if ( nurpv == 1 ) {
							nurpv = 0;
							execnurpv();
						}
						if ( minpv == 1 ) {
							minpv = 0;
							execminpv();
						}
						setTimeout(function(){  
							$('#pin').hide(); 
						}, 1400);
						lock = 0;
					}
					setTimeout(function () {
						dots.forEach(dot => dot.className = 'dot');
						input = '';
					}, 900);
					setTimeout(function () {
						document.body.className = '';
					}, 1000);
					}
					setTimeout(function () {
					number.className = 'number';
					}, 1000);
				});
			})();

			var lastmanagements2 = <?php echo trim($lastmanagements2old); ?>;
			var lastmanagement = <?php echo trim($lastmanagementold); ?>;
			var soc1vorhanden = <?php echo trim($soc1vorhanden); ?>;
			var speichervorhanden = <?php echo trim($speichervorhanden); ?>;
		</script>
		<script src="display/simple/live.js?ver=20201201"></script>

		<div id="graphsettings" style="position: fixed; display: none; width: 100%; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.5); z-index: 2; cursor: pointer;">
			<div style="  position: absolute; top: 50%; left: 50%; width: 80%; font-size: 12px; color: black; text-align: center; background-color: white; border-radius: 6px 6px 6px 6px; transform: translate(-50%,-50%); -ms-transform: translate(-50%,-50%); ">
				<div class="row"><div class="col-xs-12">
					Graph Sichtbarkeit:
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp1')"><i id="graphlp1div" class="fa"></i> Ladepunkt 1</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp2')"><i id="graphlp2div" class="fa"></i> Ladepunkt 2</span>
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp3')"><i id="graphlp3div" class="fa"></i> Ladepunkt 3</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp4')"><i id="graphlp4div" class="fa"></i> Ladepunkt 4</span>
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp5')"><i id="graphlp5div" class="fa"></i> Ladepunkt 5</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp6')"><i id="graphlp6div" class="fa"></i> Ladepunkt 6</span>
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp7')"><i id="graphlp7div" class="fa"></i> Ladepunkt 7</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp8')"><i id="graphlp8div" class="fa"></i> Ladepunkt 8</span>
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLpAll')"><i id="graphlpalldiv" class="fa"></i> Alle Ladepunkte</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayHouseConsumption')"><i id="graphhausdiv" class="fa"></i>Hausverbrauch</span>
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayEvu')"><i id="graphevudiv" class="fa"></i> EVU</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayPv')"><i id="graphpvdiv" class="fa"></i> PV</span>
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplaySpeicher')"><i id="graphspeicherdiv" class="fa"></i> Speicher</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplaySpeicherSoc')"><i id="graphspeichersocdiv" class="fa"></i> Speicher SoC</span>
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp1Soc')"><i id="graphlp1socdiv" class="fa"></i> Ladepunkt 1 SoC</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLp2Soc')"><i id="graphlp2socdiv" class="fa"></i> Ladepunkt 2 SoC</span>
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLoad1')"><i id="graphload1div" class="fa"></i>Verbraucher 1</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidedataset('boolDisplayLoad2')"><i id="graphload2div" class="fa"></i>Verbraucher 2</span>
					</div>
				</div>
				<div class="row col-xs-12" style="white-space: nowrap;">
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidelegend('boolDisplayLegend')"><i id="graphlegenddiv" class="fa"></i>Legende</span>
					</div>
					<div class="col-xs-6">
						<span style="cursor: pointer;" onclick="showhidelegend('boolDisplayLiveGraph')"><i id="graphgraphdiv" class="fa"></i> Graph Anzeige</span>
					</div>
				</div>
				<div class="row">
					<div class="col-xs-12">
						Optionen:
					</div>
				</div>
				<div class="row">
					<div class="col-xs-12">
						<input type="button" value="Renew MQTT" onclick="renewMQTTclick()"/><br>
					</div>
				</div>
				<hr>
				<div class="row">
					<div class="col-xs-12">
						<input type="button" value="Schließen" onclick="off()"/>
					</div>
				</div>
			</div>
		</div>

		<div class="row col-xs-12 text-center" id="zielladenaktivlp1div" style="display: none;"></div>
		<div class="row" id="sofortlmdiv2" style="font-size: 2vw; display: none">
			<div class="col-xs-4 text-center">
				<div id="lademstatdiv">
					<progress id="prog1" value= "0" max=<?php echo trim($lademkwhold); ?>></progress>
				</div>
			</div>
			<div id="ladepunkts11111div" class="col-xs-4 text-center">
				<div id="lademstats1div">
					<progress id="prog2" value= "0" max=<?php echo trim($lademkwhs1old); ?>></progress>
				</div>
			</div>
			<div id="ladepunkts22222div" class="col-xs-4 text-center">
				<div id="lademstats2div">
					<progress id="prog3" value= "0" max=<?php echo trim($lademkwhs2old); ?>></progress>
				</div>
			</div>
		</div>
		<div class="row" id="thegraph">
			<div class="col-xs-12" style="height: 350px; width: 92%; text-align: center; margin-left: 4%;">
				<div id="waitforgraphloadingdiv" style="text-align: center; margin-top: 150px;">
					Graph lädt, bitte warten...
				</div>
				<canvas id="canvas" style="display: none;"></canvas>
			</div>
			<div id="graphoptiondiv" style="display: none;"><br><br></div>
		</div>
		<!-- end simplemode.html -->
	</body>
</html>
