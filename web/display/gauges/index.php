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
		<link rel="apple-touch-startup-image" href="img/favicons/splash1125x2436w.png"  />
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
		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
		<!-- Elegant Icons -->
		<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
		<!-- Main style -->
		<link rel="stylesheet" type="text/css" href="css/cardio.css">
		<!-- Data refresher -->
		<script src="livefunctions.js"></script>
		<style>
			#PINform input:focus,
			#PINform select:focus,
			#PINform textarea:focus,
			#PINform button:focus {
				outline: none;
			}
			#PINform {
				background: #ededed;
				position: absolute;
				width: 650px; height: 300px;
				left: 250px;
				margin-left: -180px;
				top: 50%;
				margin-top: -215px;
				padding: 10px;
				-webkit-box-shadow: 0px 5px 5px -0px rgba(0,0,0,0.3);
				-moz-box-shadow: 0px 5px 5px -0px rgba(0,0,0,0.3);
				box-shadow: 0px 5px 5px -0px rgba(0,0,0,0.3);
			}
			#PINbox {
				background: #ededed;
				margin: 3.5%;
				width: 92%;
				font-size: 4em;
				text-align: center;
				border: 1px solid #d5d5d5;
			}
			.PINbutton {
				background: #ededed;
				color: #7e7e7e;
				border: none;
				border-radius: 50%;
				font-size: 1.5em;
				text-align: center;
				width: 60px;
				height: 60px;
				margin: 7px 20px;
				padding: 0;
				box-shadow: #506CE8 0 0 1px 1px;
			}
			.clear, .enter {
				font-size: 1em;
			}
			.PINbutton:hover {
				box-shadow: #506CE8 0 0 1px 1px;
			}
			.PINbutton:active {
				background: #506CE8;
				color: #fff;
			}
			.clear:hover {
				box-shadow: #ff3c41 0 0 1px 1px;
			}
			.clear:active {
				background: #ff3c41;
				color: #fff;
			}
			.enter:hover {
				box-shadow: #47cf73 0 0 1px 1px;
			}
			.enter:active {
				background: #47cf73;
				color: #fff;
			}
			.shadow{
				-webkit-box-shadow: 0px 5px 5px -0px rgba(0,0,0,0.3);
				-moz-box-shadow: 0px 5px 5px -0px rgba(0,0,0,0.3);
				box-shadow: 0px 5px 5px -0px rgba(0,0,0,0.3);
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

		<?php include ("gaugevalues.php"); ?>
		<script src="display/gauges/gauge.min.js"></script>
		<link rel="stylesheet" href="display/gauges/arrow.css">
		<link rel="stylesheet" href="display/gauges/pin.css">

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
			<div id="gaugediv">
				<?php if ( $speicherstatold != "none\n" ){ ?>
					<canvas id="evu" style="height: 200px; top: -50px; left: 0px; position: absolute; width: 265px;"></canvas>
					<div id="evut" style="font-size: 15px; height: 200px; top: 100px; left: 0px; position: absolute; width: 265px; color: white; text-align:center;">0</div>
					<div style="font-size: 15px; height: 200px; top: 75px; left: 0px; text-align:center; position: absolute; width: 265px; color: white;">EVU</div>

					<canvas id="pv" style="height: 200px; top: -50px; left: 265px; position: absolute; width: 265px;"></canvas>
					<div id="pvt" style="font-size: 15px; height: 200px; top: 100px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
					<div style="font-size: 15px; height: 200px; top: 75px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">PV</div>
				<?php } else { ?>
					<canvas id="evu" style="height: 200px; top: -50px; left: 132px; position: absolute; width: 265px;"></canvas>
					<div id="evut" style="font-size: 15px; height: 200px; top: 100px; left: 132px; position: absolute; width: 265px; color: white; text-align:center;">0</div>
					<div style="font-size: 15px; height: 200px; top: 75px; left: 132px; text-align:center; position: absolute; width: 265px; color: white;">EVU</div>

					<canvas id="pv" style="height: 200px; top: -50px; left: 397px; position: absolute; width: 265px;"></canvas>
					<div id="pvt" style="font-size: 15px; height: 200px; top: 100px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
					<div style="font-size: 15px; height: 200px; top: 75px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;">PV</div>
				<?php } ?>

				<div id="speicherstatdiv">
					<canvas id="speicher" style="height: 200px; top: -50px; left: 530px; position: absolute; width: 265px;"></canvas>
					<div id="speichert" style="font-size: 15px; height: 200px; top: 100px; left: 530px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
					<div style="font-size: 15px; height: 200px; top: 75px; left: 530px; text-align:center; position: absolute; width: 265px; color: white;">Speicher</div>
					<canvas id="speichers" style="height: 200px; top: -50px; left: 530px; position: absolute; width: 265px;"></canvas>
					<div id="speicherst" style="font-size: 15px; height: 100px; top: 60px; left: 530px; text-align:center; position: absolute; width: 265px; color: white;"></div>
				</div>

				<?php
				if ( $displayhausanzeigenold == "1\n" ) {
					if ( $lastmanagementold == "1\n" ) {
						?>
						<div id="hausanzeigen">
							<canvas id="haus" style="height: 200px; top: 120px; left: 0px; position: absolute; width: 265px;"></canvas>
							<div id="haust" style="font-size: 15px; height: 200px; top: 270px; left: 0px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
							<div style="font-size: 15px; height: 200px; top: 250px; left: 0px; text-align:center; position: absolute; width: 265px; color: white;">Hausverbrauch</div>
						</div>
						<canvas id="lp1" style="height: 200px; top: 120px; left: 265px; position: absolute; width: 265px;"></canvas>
						<div id="lp1t" style="font-size: 15px; height: 200px; top: 270px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
						<?php
						if ( $displaythemeold == 3 ) {
							?>
							<div style="font-size: 15px; height: 200px; top: 250px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;"><span id="lp1enableddiv" class="fa" style="cursor: pointer; outline:none;" onclick="lp1checkenabledclick()"></span><?php echo $lp1nameold; ?><span id="plugstatlp1div"></span></div>
							<canvas id="lp1s" style="height: 200px; top: 120px; left: 265px; position: absolute; width: 265px;"></canvas>
							<div id="lp1st" style="font-size: 15px; height: 200px; top: 230px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>

							<canvas id="lp2" style="height: 200px; top: 120px; left: 530px; position: absolute; width: 265px;"></canvas>

							<div id="lp2t" style="15px; height: 100px; top: 270px; left: 530px; text-align:center; position: absolute; width: 265px; color: white;"></div>
							<div style="font-size: 15px; height: 100px; top: 250px; left: 530px; text-align:center; position: absolute; width: 265px; color: white;"><span id="lp2enableddiv" class="fa" style="cursor: pointer; outline:none;" onclick="lp2checkenabledclick()"></span><?php echo $lp2nameold; ?><span id="plugstatlp2div"></span></div>
							<canvas id="lp2s" style="height: 200px; top: 120px; left: 530px; position: absolute; width: 265px;"></canvas>
							<div id="lp2st" style="15px; height: 100px; top: 230px; left: 530px; text-align:center; position: absolute; width: 265px; color: white;"></div>
							<?php
						}
					} else {
						?>
						<div id="hausanzeigen">
							<canvas id="haus" style="height: 200px; top: 120px; left: 132px; position: absolute; width: 265px;"></canvas>
							<div id="haust" style="font-size: 15px; height: 200px; top: 270px; left: 132px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
							<div style="font-size: 15px; height: 200px; top: 250px; left: 132px; text-align:center; position: absolute; width: 265px; color: white;">Hausverbrauch</div>
						</div>
						<canvas id="lp1" style="height: 200px; top: 120px; left: 397px; position: absolute; width: 265px;"></canvas>
						<div id="lp1t" style="font-size: 15px; height: 200px; top: 270px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
						<?php
						if ( $displaythemeold == 3 ) {
							?>
							<div style="font-size: 15px; height: 200px; top: 250px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;"><span id="lp1enableddiv" class="fa" style="cursor: pointer; outline:none;" onclick="lp1checkenabledclick()"></span><?php echo $lp1nameold; ?><span id="plugstatlp1div"></span></div>
							<canvas id="lp1s" style="height: 200px; top: 120px; left: 397px; position: absolute; width: 265px;"></canvas>
							<div id="lp1st" style="font-size: 15px; height: 200px; top: 230px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;">0</div>

							<div id="lp2anzeigen">
								<canvas id="lp2" style="height: 200px; top: 120px; left: 530px; position: absolute; width: 265px;"></canvas>

								<div id="lp2t" style="15px; height: 100px; top: 270px; left: 530px; text-align:center; position: absolute; width: 265px; color: white;"></div>
								<div style="font-size: 15px; height: 100px; top: 250px; left: 530px; text-align:center; position: absolute; width: 265px; color: white;"><span id="lp2enableddiv" class="fax" style="cursor: pointer; outline:none;" onclick="lp2checkenabledclick()"></span><?php echo $lp2nameold; ?><span id="plugstatlp2div"></span></div>
								<canvas id="lp2s" style="height: 200px; top: 120px; left: 530px; position: absolute; width: 265px;"></canvas>
								<div id="lp2st" style="15px; height: 100px; top: 230px; left: 530px; text-align:center; position: absolute; width: 265px; color: white;"></div>
							</div>
							<?php
						}
					}
				} else {
					if ( $lastmanagementold == "1\n" ) {
						?>
						<div id="hausanzeigen">
							<canvas id="haus" style="height: 200px; top: 120px; left: 0px; position: absolute; width: 265px;"></canvas>
							<div id="haust" style="font-size: 15px; height: 200px; top: 270px; left: 0px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
							<div style="font-size: 15px; height: 200px; top: 250px; left: 0px; text-align:center; position: absolute; width: 265px; color: white;">Hausverbrauch</div>
						</div>
						<canvas id="lp1" style="height: 200px; top: 120px; left: 132px; position: absolute; width: 265px;"></canvas>
						<div id="lp1t" style="font-size: 15px; height: 200px; top: 270px; left: 132px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
						<?php
						if ( $displaythemeold == 3 ) {
							?>
							<div style="font-size: 15px; height: 200px; top: 250px; left: 132px; text-align:center; position: absolute; width: 265px; color: white;"><span id="lp1enableddiv" class="fa" style="cursor: pointer; outline:none;" onclick="lp1checkenabledclick()"></span><?php echo $lp1nameold; ?><span id="plugstatlp1div"></span></div>
							<canvas id="lp1s" style="height: 200px; top: 120px; left: 132px; position: absolute; width: 265px;"></canvas>
							<div id="lp1st" style="font-size: 15px; height: 200px; top: 230px; left: 132px; text-align:center; position: absolute; width: 265px; color: white;">0</div>

							<div id="lp2anzeigen">
								<canvas id="lp2" style="height: 200px; top: 120px; left: 397px; position: absolute; width: 265px;"></canvas>
								<div id="lp2t" style="15px; height: 100px; top: 270px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;"></div>
								<div style="font-size: 15px; height: 100px; top: 250px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;"><span id="lp2enableddiv" class="fa" style="cursor: pointer; outline:none;" onclick="lp2checkenabledclick()"></span><?php echo $lp2nameold; ?><span id="plugstatlp2div"></span></div>
								<canvas id="lp2s" style="height: 200px; top: 120px; left: 397px; position: absolute; width: 265px;"></canvas>
								<div id="lp2st" style="15px; height: 100px; top: 230px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;"></div>
							</div>
							<?php
						}
					} else {
						?>
						<div id="hausanzeigen">
							<canvas id="haus" style="height: 200px; top: 120px; left: 0px; position: absolute; width: 265px;"></canvas>
							<div id="haust" style="font-size: 15px; height: 200px; top: 270px; left: 0px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
							<div style="font-size: 15px; height: 200px; top: 250px; left: 0px; text-align:center; position: absolute; width: 265px; color: white;">Hausverbrauch</div>
						</div>
						<canvas id="lp1" style="height: 200px; top: 120px; left: 265px; position: absolute; width: 265px;"></canvas>
						<div id="lp1t" style="font-size: 15px; height: 200px; top: 270px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
						<?php
						if ( $displaythemeold == 3 ) {
							?>
							<div style="font-size: 15px; height: 200px; top: 250px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;"><span id="lp1enableddiv" class="fa" style="cursor: pointer; outline:none;" onclick="lp1checkenabledclick()"></span><?php echo $lp1nameold; ?><span id="plugstatlp1div"></span></div>
							<canvas id="lp1s" style="height: 200px; top: 120px; left: 265px; position: absolute; width: 265px;"></canvas>
							<div id="lp1st" style="font-size: 15px; height: 200px; top: 230px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>

							<div id="lp2anzeigen">
								<canvas id="lp2" style="height: 200px; top: 120px; left: 397px; position: absolute; width: 265px;"></canvas>
								<div id="lp2t" style="15px; height: 100px; top: 270px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;"></div>
								<div style="font-size: 15px; height: 100px; top: 250px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;"></span>'.$lp2nameold.'<span id="plugstatlp2div"></div>
								<canvas id="lp2s" style="height: 200px; top: 120px; left: 397px; position: absolute; width: 265px;"></canvas>
								<div id="lp2st" style="15px; height: 100px; top: 230px; left: 397px; text-align:center; position: absolute; width: 265px; color: white;"></div>
							</div>
							<?php
						}
					}
				}
				?>
			</div>

			<div id="symboldiv" style="color: white; top: 0px; left: 10px; position: absolute; font-size: 18px; width: 810px;">
				<div class="row col-xs-12 text-center" style="height: 50px;">
					<div class="col-xs-4">
					</div>
					<div class="col-xs-4">
						<i class="fas fa-2x fa-solar-panel" style="color: green;"></i><br>
						<span id="pvdiv"></span>
					</div>
					<div class="col-xs-4">
					</div>
				</div>
				<div class="row col-xs-12 text-center" style="height: 50px;">
					<div class="col-xs-6">
					</div>
					<div class="col-xs-1 text-center">
						<div id="speedpv">
							<div id="arrowpv"></div>
 						</div>
					</div>
					<div class="col-xs-5">
					</div>
				</div>
				<div class="row col-xs-12 text-center" style="height: 50px;">
					<div class="col-xs-2">
						<img src="img/icons/electric-tower.svg" style="filter: invert(1); -webkit-filter: invert(1);" width="40vw" >
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
					<div id="speicherstat2div">
						<div class="col-xs-3">
							<div id="speedspeicher">
								<div id="arrowspeicher"></div>
 							</div>
							<span id="speicherleistungdiv"></span>
						</div>
						<div class="col-xs-2">
							<span id="speichersocstatdiv" class="fas fa-2x"></span><br>
							<span id="speichersocdiv"></span> %
						</div>
					</div>
				</div>
				<div class="row col-xs-12 text-center" style="height: 40px;">
					<div class="col-xs-6">
					</div>
					<div class="col-xs-1 text-center">
						<div id="speedlpg">
							<div id="arrowlpg"></div>
						</div>
					</div>
					<div class="col-xs-5">
					</div>
				</div>
				<div class="row col-xs-12 text-center" style="height: 40px;">
					<div class="col-xs-5">
					</div>
					<div class="col-xs-2 text-center">
						<span id="gesamtllwdiv"></span><br>
					</div>
					<div class="col-xs-5">
					</div>
				</div>
				<?php
					if ( $lastmanagementold == "1\n" ) {
						?>
						<div class="row col-xs-12 text-center" style="height: 50px;">
							<div class="col-xs-2">
								<span id="lp1enableddiv" class="fa fa-2x" style="cursor: pointer; outline:none;" onclick="lp1checkenabledclick()"></span><span id="stationlp1" class="fas fa-2x fa-charging-station"></span>
							</div>
							<div class="col-xs-2">
								<div id="speedlp1">
									<div id="arrowlp1"></div>
 								</div>
								<span id="lllp1div"></span>
							</div>
							<div class="col-xs-1">
								<i id="carlp1" class="fas fa-2x fa-car-side"></i><br>
								<?php echo $lp1nameold; ?>
							</div>
							<div class="col-xs-1">
								<div id="socenabledlp1">
									<span id="socstatlp1div" class="fas fa-2x"></span><br>
									<span id="soclevel"></span>%
								</div>
							</div>
							<div class="col-xs-2">
								<span id="lp2enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp2checkenabledclick()"></span><span id="stationlp2" class="fas fa-2x fa-charging-station"></span>	
							</div>
							<div class="col-xs-2">
								<div id="speedlp2">
									<div id="arrowlp2"></div>
 								</div>
								<span id="lllp2div"></span>
							</div>
							<div class="col-xs-1">
								<i id="carlp2" class="fas fa-2x fa-car-side"></i><br>
								<?php echo $lp2nameold; ?>
							</div>
							<div class="col-xs-1">
								<div id="socenabledlp2">
									<span id="socstatlp2div" class="fas fa-2x"></span><br>
									<span id="soc1level"></span>%
								</div>
							</div>
						</div>
						<?php
					} else {
						?>
						<div class="row col-xs-12 text-center" style="height: 100px;">
							<div class="col-xs-2">
								<span id="lp1enableddiv" class="fa fa-2x" style="cursor: pointer;" onclick="lp1enabledclick()"></span><span id="stationlp1" class="fas fa-2x fa-charging-station"></span>
							</div>
							<div class="col-xs-3">
								<div id="speedlp1">
									<div id="arrowlp1"></div>
 								</div>
								<span id="lllp1div"></span>
							</div>
							<div class="col-xs-2">
								<i id="carlp1" class="fas fa-2x fa-car-side"></i><br>
								<?php echo $lp1nameold; ?>
							</div>
							<div class="col-xs-2">
								<div id="socenabledlp1">
									<span id="socstatlp1div" class="fas fa-2x"></span><br>
									<span id="soclevel"></span>%
								</div>
							</div>
							<div class="col-xs-3">
							</div>
						</div>
						<?php
					}
				?>
			</div>

			<div class="row col-xs-12 text-center" style="font-size: 15px; height: 20px; top: 380px; left: 0px; position: absolute; width: 820px; color: white; text-align:center;"> 
				<div class="row"> 
					<div id="lastregelungaktivdiv" class="col-xs-12 text-center" style="color:#990000;font-size: 30px"> 
					</div> 
				</div>
			</div>
			<div class="row col-xs-12 text-center" style="font-size: 15px; height: 20px; top: 320px; left: 00px; position: absolute; width: 800px; color: white; text-align:center;"> 
				<div class="col-xs-2">
					<div id="sofortllbtn">
						<input type="submit" class="1sofortll btn btn-blue btn-block"  name="sofortllbtn" value="Ladestrom">
					</div>
				</div>
				<div class="col-xs-2">
					<input id="pinpad" type="button" class="btn btn-blue btn-block" value="Code eingeben" onclick="$('#PINcode').show();" />
				</div>
				<div class="col-xs-3">
					<input id="lp1checkenabled" type="button" class="btn btn-blue btn-block" value="LP1 (de-)aktivieren" onclick="lp1checkenabledclick();" />
				</div>
				<?php
					if ( $lastmanagementold == "1\n" ) {
						?>
						<div class="col-xs-3">
							<input id="lp2checkenabled" type="button" class="btn btn-blue btn-block" value="LP2 (de-)aktivieren" onclick="lp2checkenabledclick();" />
						</div>
						<?php
					} else {
						?>
						<div class="col-xs-2"></div>
						<?php
					}
				?>
				<div class=" col-xs-2"> 
					<input type="submit" class="1einstellungen btn btn-blue btn-block"  name="graph" value="Status">
				</div> 
			</div>

			<div class="row">
				<div class="container" style="left:20px;bottom:0px;position:absolute;">
					<div class="col-xs-3 text-center">
						<div class="actstat">
							<input type="submit" class="1sofort btn btn-lg btn-block" style="font-size: 2vw" name="sofort" value="Sofort Laden">
						</div>
					</div>
					<div class="col-xs-2 text-center">
						<div class="actstat4">
							<input type="submit" class="1standby btn btn-lg btn-block" style="font-size: 2vw" name="standby" value="Standby">
						</div>
					</div>
					<div class="col-xs-2 text-center">
						<div class="actstat3">
							<input type="submit" class="1stop btn btn-lg btn-block" style="font-size: 2vw" name="stop" value="Stop">
						</div>
					</div>
					<div class="col-xs-2 text-center">
						<div class="actstat1">
							<input type="submit" class="1minpv btn btn-lg btn-block" style="font-size: 2vw" name="minpv" value="Min + PV">
						</div>
					</div>
					<div class="col-xs-3 text-center">
						<div class="actstat2">
							<input type="submit" class="1nurpv btn btn-lg btn-block" style="font-size: 2vw" name="nurpv" value="Nur PV">
						</div>
					</div>
				</div>
			</div>
		</div>

		<div id="sofortll" style="display: none;">
			<div class="col-xs-12 text-center" style="font-size: 22px; height: 10px; top: 30px; left: 50px; position: absolute; width: 750px; color: white; text-align:left;">
				<div id="slider1div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp1s" id="sofortlllp1s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 1: <span id="sofortlllp1l"></span>A</label>  
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
				<div id="slider2div" class="col-xs-12 text-center">
					<div class="col-xs-8 text-center">
						<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlllp2s" id="sofortlllp2s">
					</div>
					<div class="col-xs-4 text-center">
						<label>LP 2: <span id="sofortlllp2l"></span>A</label>  
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
			</div>
			<div class="row col-xs-12 text-center" style="font-size: 12px; height: 10px; top: 430px; left: 50px; position: absolute; width: 750px; color: white; text-align:center;"> 
				<div class=" col-xs-8">
				</div>
				<div class=" col-xs-2"> 
					<input type="submit" class="1sllspeichern btn-blue btn btn-block" style="height: 10px; line-height: 3px !important;" name="sllspeichern" value="Speichern">
				</div>
				<div class=" col-xs-2"> 
					<input type="submit" class="1zurueck btn-blue btn btn-block" style="height: 10px; line-height: 3px !important;" name="zurueck" value="Zurück">
				</div> 
			</div>
		</div>

		<div id="einstellungen">
			<div id="status" style="display: none;">
				<div style="font-size: 25px; height: 20px; top: 0px; left: 0px; text-align:center; position: absolute; width: 800px; color: white;">Status</div>
				<div class="row col-xs-12 text-left" style="font-size: 22px; height: 10px; top: 30px; left: 50px; position: absolute; width: 750px; color: white; text-align:left;"> 
					IP Adresse der openWB: <span id="ethaddr"></span> <span id="wlanaddr"></span>
				</div>
				<div class="row col-xs-12 text-left" style="font-size: 22px; height: 10px; top: 50px; left: 50px; position: absolute; width: 750px; color: white; text-align:left;"> 
					Uptime: <span id='uptime'>--</span><br>
					CPU: <meter id="cpu" high="85" min="0" max="100" value="0"></meter> <span id='cpuuse'>--</span>%<br>
					Memory: <span id='memtot'>--</span>MB <meter id="mem" min="0" value="0"></meter> <font size='-1'>(<span id='memfree'>--</span>MB free)</font><br>
					Disk Usage: <span id='diskuse'>--</span>, <span id='diskfree'>--</span> avail.<br>
					openWB Version: <?php echo $owbversion; ?>
				</div>
				<div id="backend" class="row col-xs-12 text-left" style="font-size: 22px; height: 100px; top: 250px; left: 50px; position: absolute; width: 750px; color: white; text-align:left;"> 
					Backend: <span class="connectionState">-</span><br>
					Verbindungsversuche: <span class="counter">-</span><br>
					<button class="btn btn-block btn-red reloadBtn" type="button">Display neu Laden</button>
				</div>
				<script>
					function updateit() {
						$.getJSON('tools/programmloggerinfo.php', function(data){
							json = eval(data);
							document.getElementById('cpu').value= json.cpuuse;
							document.getElementById('uptime').innerHTML = json.uptime;
							document.getElementById('cpuuse').innerHTML = json.cpuuse;
							document.getElementById('memtot').innerHTML = json.memtot;
							document.getElementById('mem').max= json.memtot;
							document.getElementById('mem').value= json.memuse;
							document.getElementById('mem').high = (json.memtot*0.85);
							document.getElementById('memfree').innerHTML = json.memfree;
							document.getElementById('diskuse').innerHTML = json.diskuse;
							document.getElementById('diskfree').innerHTML = json.diskfree;
							document.getElementById('ethaddr').innerHTML = json.ethaddr; 
							document.getElementById('wlanaddr').innerHTML = json.wlanaddr; 
						})
					};

					$(document).ready(function() {
						updateit();
						setInterval(updateit, 10000);
					});

					$('#backend .reloadBtn').click(function() {
						location.reload();
					});
				</script>
			</div>

			<div id="hilfe" style="display: none;">
				<div style="font-size: 25px; height: 20px; top: 0px; left: 0px; text-align:center; position: absolute; width: 800px; color: white;">Hilfe</div>
				<div class="row col-xs-12 text-left" style="font-size: 22px; height: 10px; top: 30px; left: 50px; position: absolute; width: 750px; color: white; text-align:left;"> 
					Symbollegende:<br>
					<i class="fas fa-charging-station"></i> keine Ladung freigegeben, 
					<i class="fas fa-charging-station" style="color: green;"></i>Ladung freigegeben<br>
					<i class="fas fa-car-side"></i>Auto nicht angesteckt,<i class="fas fa-car-side" style="color: blue;"></i>Auto angesteckt<br>
					<i class="fas fa-battery-half"></i>Auto nicht ladend,<i class="fas fa-battery-half" style="color: green"></i> Auto ladend
				</div>
			</div>
			<div class="row col-xs-12 text-center" style="font-size: 12px; height: 10px; top: 430px; left: 50px; position: absolute; width: 750px; color: white; text-align:center;"> 
				<div class=" col-xs-8">
				</div>
				<div class=" col-xs-2"> 
					<input type="submit" class="1hilfe btn-blue btn btn-block" style="height: 10px; line-height: 3px !important;" name="hilfe" value="Hilfe">
				</div> 
				<div class=" col-xs-2"> 
					<input type="submit" class="1zurueck btn-blue btn btn-block" style="height: 10px; line-height: 3px !important;" name="zurueck" value="Zurück">
				</div> 
			</div>
		</div>

		<div id="dergraph">
			<?php
				$result = '';
				$lines = file('/var/www/html/openWB/openwb.conf');
				foreach($lines as $line) {
					if(strpos($line, "grapham=") !== false) {
						list(, $graphamold) = explode("=", $line);
					}
					if(strpos($line, "graphinteractiveam=") !== false) {
						list(, $graphinteractiveamold) = explode("=", $line);
					}
					if(strpos($line, "lastmanagement=") !== false) {
						list(, $lastmanagementold) = explode("=", $line);
					}
					if(strpos($line, "lastmanagements2=") !== false) {
						list(, $lastmanagements2old) = explode("=", $line);
					}
					if(strpos($line, "verbraucher1_name=") !== false) {
						list(, $verbraucher1_nameold) = explode("=", $line);
					}
					if(strpos($line, "verbraucher2_name=") !== false) {
						list(, $verbraucher2_nameold) = explode("=", $line);
					}
					if(strpos($line, "verbraucher3_name=") !== false) {
						list(, $verbraucher3_nameold) = explode("=", $line);
					}
				}

				$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
				$soc1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/soc1vorhanden');
				$verbraucher1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher1vorhanden');
				$verbraucher2vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher2vorhanden');
				$verbraucher3vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher3vorhanden');
				$verbraucher1_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher1_nameold));
				$verbraucher2_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher2_nameold));
				$verbraucher3_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher3_nameold));
			?>
			<div style="height:440px; width:800px;" id="dailydiv"></div>
				<div class="row col-xs-12 text-center" style="font-size: 12px; height: 10px; top: 430px; left: 50px; position: absolute; width: 750px; color: white; text-align:center;"> 
					<div class=" col-xs-10">
					</div> 
					<div class=" col-xs-2"> 
						<input type="submit" class="1zurueck btn-blue btn btn-block" style="height: 10px; line-height: 3px !important;" name="zurueck" value="Zurück">
					</div> 
				</div>
			</div>

			<div id="pin" style="display: none;">
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
			</script>
			<?php if ( $displaythemeold == 3 ) { ?>
				<script src="display/gauges/graphgauge.js"></script>
			<?php } ?>
			<script>
				var displaytheme = <?php echo $displaythemeold ?>;
				var doInterval;

				function getfile() {
					if (displaytheme == 3) {
						$.ajaxSetup({ cache: false});
						$.ajax({
							url: "/openWB/ramdisk/wattbezug",
							complete: function(request){
								var wattbezug = request.responseText;
								var intbezug = parseInt(wattbezug, 10);
								gauge.set(wattbezug);
								if (intbezug > 0) {
									$("#evut").html(request.responseText + " W<br>Bezug");
								} else {
									wattbezug = wattbezug * -1; 
									$("#evut").html(wattbezug + " W<br>Einspeisung");
								};
							}
						});
						$.ajax({
							url: "/openWB/ramdisk/pvallwatt",
							complete: function(request){
								var pvwatt = request.responseText;
								pvwatt = pvwatt * -1;
								gaugepv.set(pvwatt);
								$("#pvt").html(pvwatt + " W");
							}
						});
						$.ajax({
							url: "/openWB/ramdisk/speicherleistung",
							complete: function(request){
								var speicherwatt = request.responseText;
								gaugespeicher.set(speicherwatt);
								if ( speicherwatt > 0) {
									$("#speichert").html(request.responseText + " W<br>Ladung");
								} else {
									speicherwatt = speicherwatt * -1;
									$("#speichert").html(speicherwatt + " W<br>Entladung");
								}
							}
						});
						$.ajax({
							url: "/openWB/ramdisk/speichersoc",
							complete: function(request){
								var speichers = request.responseText;
								gaugespeichers.set(speichers);
								$("#speicherst").html(request.responseText + "%");
							}
						});
						$.ajax({
							url: "/openWB/ramdisk/hausverbrauch",
							complete: function(request){
								var hausverbrauch = request.responseText;
								gaugehaus.set(hausverbrauch);
								$("#haust").html(request.responseText + " W");
							}
						});
						$.ajax({
							url: "/openWB/ramdisk/llaktuell",
							complete: function(request){
								var lp1w = request.responseText;
								gaugelp1.set(lp1w);
								$("#lp1t").html(request.responseText + " W");
							}
						});
						$.ajax({
							url: "/openWB/ramdisk/llaktuells1",
							complete: function(request){
								var lp2w = request.responseText;
								gaugelp2.set(lp2w);
								$("#lp2t").html(request.responseText + " W");

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
						$.ajax({
							url: "/openWB/ramdisk/soc1",
							complete: function(request){
								var lp2s = request.responseText;
								gaugelp2s.set(lp2s);
								$("#lp2st").html(request.responseText + "%");
							}
						});
					}
				}

				doInterval = setInterval(getfile, 10000);
				getfile();

				var displaytheme = <?php echo $displaythemeold ?>;

				$('#gaugediv').hide();
				$('#symboldiv').hide();
				$('#dergraph').hide();
				$('#einstellungen').hide();
				$('#sofortll').hide();
				$('#sofortllbtn').hide();
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
						$('#sofortll').show();
						dash = 0;

						$('.1sllspeichern').click(function(){
							var ajaxurl = 'tools/changelademodusd.php?sofortlllp1=' + slider1.value;
							$.post(ajaxurl, 'sofortlllp1', function (response) {
								$('#dergraph').hide();
								$('#einstellungen').hide();
								$('#sofortll').hide();
								$('#main').show();
							});
						});
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

				function lp1checkenabledclick(){
					if ( lock == 0 ) {
						if ( displaypinaktiv == 1){
							lock = 1;
							lp1enab = 1;
							$('#pin').show();
						} else {
							lp1enabledclick();
						}
					}
				};

				function lp2checkenabledclick(){
					if ( lock == 0 ) {
						if ( displaypinaktiv == 1){
							lock = 1;
							lp2enab = 1;
							$('#pin').show();
						} else {
							lp2enabledclick();
						}
					}
				};

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
								stop = 0;
								lp1enab = 0;
								minpv = 0;
								nurpv = 0;
								sofort = 0;
								standby = 0;
								lp2enab = 0;
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
								if ( lp1enab == 1 ) {
									lp1enab = 0;
									lp1enabledclick();
								}
								if ( lp2enab == 1 ) {
									lp2enab = 0;
									lp2enabledclick();
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

				var lastmanagements2 = <?php echo $lastmanagements2old ?>;
				var lastmanagement = <?php echo $lastmanagementold ?>;
				var soc1vorhanden = <?php echo $soc1vorhanden ?>;
				var speichervorhanden = <?php echo $speichervorhanden ?>;
				var verbraucher1vorhanden = <?php echo $verbraucher1vorhanden ?>;
				var verbraucher1name = "<?php echo $verbraucher1_nameold ?> (I)";
				var verbrauchere1name = "<?php echo $verbraucher1_nameold ?> (E)";
				var verbraucher2vorhanden = <?php echo $verbraucher2vorhanden ?>;
				var verbraucher2name = "<?php echo $verbraucher2_nameold ?> (I)";
				var verbrauchere2name = "<?php echo $verbraucher2_nameold ?> (E)";
				var verbraucher3vorhanden = <?php echo $verbraucher3vorhanden ?>;
				var verbraucher3name = "<?php echo $verbraucher3_nameold ?>";
			</script>

			<script src="livechart_chartjs.js"></script>
			<script src="js/mqttws31.js"></script>
			<script src="js/Chart.bundle.min.js"></script>
			<script src="display/gauges/alllive.js?vers=20201201"></script>
			<script src="display/gauges/symbollive.js?vers=20201201"></script>
			<script src="display/gauges/live.js?vers=20210301"></script>

			<div id="graphsettings" style="position: fixed; display: none; width: 100%; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.5); z-index: 2; cursor: pointer;">
				<div style="position: absolute; top: 50%; left: 50%; width: 80%; font-size: 12px; color: black; text-align: center; background-color: white; border-radius: 6px 6px 6px 6px; transform: translate(-50%,-50%); -ms-transform: translate(-50%,-50%); ">
					<div class="row">
						<div class="col-xs-12">
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
			<div class="row" id="sofortlmdiv2" style="font-size: 2vw; display: none"></div>
			<div style="display: none;">
				<div class="row" id="thegraph" style="display: none;">
					<div class="col-xs-12" style="height: 350px; width: 92%; text-align: center; margin-left: 4%;">
						<div id="waitforgraphloadingdiv" style="text-align: center; margin-top: 150px;">
							Graph lädt, bitte warten...
						</div>
						<canvas id="canvas" style="display: none;"></canvas>
					</div>
					<div id="graphoptiondiv" style="display: none;"><br><br></div>
					<div style="display: none;" id="lp3enableddiv"></div>
					<div style="display: none;" id="lp4enableddiv"></div>
					<div style="display: none;" id="lp5enableddiv"></div>
					<div style="display: none;" id="lp6enableddiv"></div>
					<div style="display: none;" id="lp7enableddiv"></div>
					<div style="display: none;" id="lp8enableddiv"></div>
					<div style="display: none;" id="sofortlllp3s"></div>
					<div style="display: none;" id="sofortlllp4s"></div>
					<div style="display: none;" id="sofortlllp5s"></div>
					<div style="display: none;" id="sofortlllp6s"></div>
					<div style="display: none;" id="sofortlllp7s"></div>
					<div style="display: none;" id="sofortlllp8s"></div>
					<div style="display: none;" id="sofortlllp3l"></div>
					<div style="display: none;" id="sofortlllp4l"></div>
					<div style="display: none;" id="sofortlllp5l"></div>
					<div style="display: none;" id="sofortlllp6l"></div>
					<div style="display: none;" id="sofortlllp7l"></div>
					<div style="display: none;" id="sofortlllp8l"></div>
					<div style="display: none;" id="lademstatdiv"></div>
					<div style="display: none;" id="ladepunkts11111div"></div>
					<div style="display: none;" id="ladepunkts22222div"></div>
				</div>
			</div>

			<div id="PINcode" style="display: none;"></div>

			<script>
				$( "#PINcode" ).html(
					"<form action='' method='' name='PINform' id='PINform' autocomplete='off' draggable='true'>" +
						"<input id='PINbox' type='text' value='' name='PINbox' disabled />" +
						"<br/>" +
						"<input type='button' class='PINbutton' name='1' value='1' id='1' onClick=addNumber(this); />" +
						"<input type='button' class='PINbutton' name='2' value='2' id='2' onClick=addNumber(this); />" +
						"<input type='button' class='PINbutton' name='3' value='3' id='3' onClick=addNumber(this); />" +
						"<input type='button' class='PINbutton' name='4' value='4' id='4' onClick=addNumber(this); />" +
						"<input type='button' class='PINbutton' name='5' value='5' id='5' onClick=addNumber(this); />" +
						"<input type='button' class='PINbutton' name='6' value='6' id='6' onClick=addNumber(this); />" +
						"<br>" +
						"<input type='button' class='PINbutton' name='7' value='7' id='7' onClick=addNumber(this); />" +
						"<input type='button' class='PINbutton' name='8' value='8' id='8' onClick=addNumber(this); />" +
						"<input type='button' class='PINbutton' name='9' value='9' id='9' onClick=addNumber(this); />" +
						"<input type='button' class='PINbutton' name='0' value='0' id='0' onClick=addNumber(this); />" +
						"<input type='button' class='PINbutton clear' name='-' value='clear' id='-' onClick=clearForm(this); />" +

						"<input type='button' class='PINbutton enter' name='+' value='enter' id='+' onClick=submitForm(PINbox); />" +
					"</form>"
				);

				function addNumber(e){
					//document.getElementById('PINbox').value = document.getElementById('PINbox').value+element.value;
					var v = $( "#PINbox" ).val();
					$( "#PINbox" ).val( v + e.value );
				}
				function clearForm(e){
					//document.getElementById('PINbox').value = "";
					$( "#PINbox" ).val( "" );
					$('#PINcode').hide();	
				}
				function submitForm(e) {
					sendrfidtag(e.value);	
					$( "#PINbox" ).val( "" );
					$('#PINcode').hide();	
				};
			</script>
	</body>
</html>
