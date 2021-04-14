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
		<link rel="apple-touch-startup-image" href="/openWB/web/img/favicons/splash1125x2436w.png"  />
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
		<script src="js/jquery-3.6.0.min.js"></script>
		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
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
	</head>
	<body>
		<input type="hidden" name="lastmanagement" id="lastmanagement" value="<?php echo $lastmanagementold; ?>" />
		<input type="hidden" name="lastmanagements2" id="lastmanagements2" value="<?php echo $lastmanagements2old; ?>" />
		<input type="hidden" name="speicherstat" id="speicherstat" value="<?php echo $speicherstatold; ?>" />
		<input type="hidden" name="lademlp1stat" id="lademlp1stat" value="<?php echo $lademstatold; ?>" />
		<input type="hidden" name="lademlp2stat" id="lademlp2stat" value="<?php echo $lademstats1old; ?>" />
		<input type="hidden" name="lademlp3stat" id="lademlp3stat" value="<?php echo $lademstats2old; ?>" />
		<input type="hidden" name="evuglaettungakt" id="evuglaettungakt" value="<?php echo $evuglaettungaktold; ?>" />
		<input type="hidden" name="nachtladenstate" id="nachtladenstate" value="<?php echo $nachtladenstate; ?>" />
		<input type="hidden" name="nachtladenstates1" id="nachtladenstates1" value="<?php echo $nachtladenstates1; ?>" />
		<input type="hidden" name="nlakt_nurpv" id="nlakt_nurpv" value="<?php echo $nlakt_nurpvold; ?>" />
		<input type="hidden" name="nlakt_sofort" id="nlakt_sofort" value="<?php echo $nlakt_sofortold; ?>" />
		<input type="hidden" name="nlakt_minpv" id="nlakt_minpv" value="<?php echo $nlakt_minpvold; ?>" />
		<input type="hidden" name="nlakt_standby" id="nlakt_standby" value="<?php echo $nlakt_standbyold; ?>" />
		<input type="hidden" name="lademodus" id="lademodus" value="<?php echo $lademodusold; ?>" />
		<input type="hidden" name="hausverbrauchstat" id="hausverbrauchstat" value="<?php echo $hausverbrauchstatold; ?>" />
		<input type="hidden" name="speicherpvui" id="speicherpvui" value="<?php echo $speicherpvuiold; ?>" />
		<input type="hidden" name="zielladenaktivlp1" id="zielladenaktivlp1" value="<?php echo $zielladenaktivlp1old; ?>" />
		<input type="hidden" name="sofortlm" id="sofortlm" value="<?php echo $lademodusold; ?>" />
		<input type="hidden" name="heutegeladen" id="heutegeladen" value="<?php echo $heutegeladenold; ?>" />

		<!-- minimal.html -->
		<?php include ("gaugevalues.php"); ?>
		<script src="display/minimal/gauge.min.js"></script>
		<link rel="stylesheet" href="display/minimal/minimal.css">

		<input type="hidden" name="displayevumax" id="displayevumax" value="<?php echo $displayevumaxold; ?>" />
		<input type="hidden" name="displaypvmax" id="displaypvmax" value="<?php echo $displaypvmaxold; ?>" />
		<input type="hidden" name="displayspeichermax" id="displayspeichermax" value="<?php echo $displayspeichermaxold; ?>" />
		<input type="hidden" name="displayhausanzeigen" id="displayhausanzeigen" value="<?php echo $displayhausanzeigenold; ?>" />
		<input type="hidden" name="displayhausmax" id="displayhausmax" value="<?php echo $displayhausmaxold; ?>" />
		<input type="hidden" name="displaylp1max" id="displaylp1max" value="<?php echo $displaylp1maxold; ?>" />
		<input type="hidden" name="displaylp2max" id="displaylp2max" value="<?php echo $displaylp2maxold; ?>" />
		<input type="hidden" name="displaypinaktiv" id="displaypinaktiv" value="<?php echo $displaypinaktivold; ?>" />
		<input type="hidden" name="displaypincode" id="displaypincode" value="<?php echo $displaypincodeold; ?>" />

		<div id="main">
			<div style="font-size: 18px; height: 20px; top: 0px; left: 740px; text-align:center; position: absolute; width: 65px; color: white;" id="theclock"></div>
			<div id="gaugediv">
				<canvas id="lp1" style="height: 600px; top: -150px; left: 20px; position: absolute; width: 760px;"></canvas>
				<div id="lp1t" style="font-size: 35px; height: 170px; top: 300px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
				<canvas id="lp1s" style="height: 520px; top: -80px; left: 30px; position: absolute; width: 740px;"></canvas>
				<div id="lp1st" style="font-size: 35px; height: 200px; top: 230px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
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
				if (i < 10) {
					i = "0" + i
				};  // add zero in front of numbers < 10
				return i;
			}

			startTime();

			var displayhausmax = <?php echo $displayhausmaxold; ?>;
			var displaylp2max = <?php echo $displaylp2maxold; ?>;
			var displaylp1max = <?php echo $displaylp1maxold; ?>;
			var displaypvmax = <?php echo $displaypvmaxold; ?>;
			var displayevumax = <?php echo $displayevumaxold; ?>;
			var displayspeichermax = <?php echo $displayspeichermaxold; ?>;
			var displayhausanzeigen = <?php echo $displayhausanzeigenold; ?>;
			var displaypincode = <?php echo $displaypincodeold; ?>;
			var displaypinaktiv = <?php echo $displaypinaktivold; ?>;
			// var lastmanagementold = <?php echo $lastmanagementold; ?>;
		</script>
		<script src="display/minimal/minimalgauge.js"></script>
		<script>
			var doInterval;

			function getfile() {
				$.ajax({
					url: "/openWB/ramdisk/llaktuell",
					complete: function(request){
						var lp1w = request.responseText;
						gaugelp1.set(lp1w);
						if ( lp1w > 999 ) {
							lp1w= lp1w / 1000;
							$("#lp1t").html(lp1w.toFixed(2) + " kW");
						} else {
							$("#lp1t").html(request.responseText + " W");
						}
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/soc",
					complete: function(request){
						var lp1s = request.responseText;
						gaugelp1s.set(lp1s);
						$("#lp1st").html(request.responseText + "%");
					}
				});
			};

			doInterval = setInterval(getfile, 10000);
			getfile();

			var lastmanagements2 = <?php echo $lastmanagements2old; ?>;
			var lastmanagement = <?php echo $lastmanagementold; ?>;
			var soc1vorhanden = <?php echo $soc1vorhanden; ?>;
		</script>
		<script src="display/minimal/alllive.js?vers=20201201"></script>
		<script>
			// ************** beginning of MQTT code *************
			$(document).ready(function(){

				// load scripts synchronously in order specified
				var scriptsToLoad = [
					// load mqtt library
					'js/mqttws31.js',
					// functions for processing messages
					'display/minimal/processAllMqttMsg.js?ver=20201201',
					// functions performing mqtt and start mqtt-service
					'display/minimal/setupMqttServices.js?ver=20201201',
				];

				scriptsToLoad.forEach(function(src) {
					var script = document.createElement('script');
					script.src = src;
					script.async = false;
					document.body.appendChild(script);
				});

			});
		</script>
	</body>
</html>
