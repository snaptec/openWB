<!DOCTYPE html>
<html lang="de">
	<head>
		<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Status</title>
		<meta name="description" content="Control your charge" />
		<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
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
		<link rel="stylesheet" type="text/css" href="fonts/font-awesome-5.8.2/css/all.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="status/status_style.css?ver=20210209">
		<!-- local css due to async loading of theme css -->
		<style>
			#preloader {
				background-color:white;
				position:fixed;
				top:0px;
				left:0px;
				width:100%;
				height:100%;
				z-index:999999;
			}
			#preloader-inner {
				margin-top: 150px;
				text-align: center;
			}
			#preloader-image {
				max-width: 300px;
			}
			#preloader-info {
				color:grey;
			}
		</style>
		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "status/helperFunctions.js?ver=20210128" ></script>
		<script>
			function getCookie(cname) {
				var name = cname + '=';
				var decodedCookie = decodeURIComponent(document.cookie);
				var ca = decodedCookie.split(';');
				for(var i = 0; i <ca.length; i++) {
					var c = ca[i];
					while (c.charAt(0) == ' ') {
						c = c.substring(1);
					}
					if (c.indexOf(name) == 0) {
						return c.substring(name.length, c.length);
					}
				}
				return '';
			}
			var themeCookie = getCookie('openWBTheme');
			// include special Theme style
			if( '' != themeCookie ){
				$('head').append('<link rel="stylesheet" href="themes/' + themeCookie + '/settings.css?v=20210209">');
			}
		</script>

		<script>
			function readLogFile(urlStr, target) {
				$.ajax({
					url: urlStr,
					complete: function(request){
						var lines = request.responseText.split("\n");
						var result = "";
						for(var i=0; i<lines.length-1; i++)
							result = lines[i] + "\n" + result;
						$(target).text(result);
					}
				});
			}

			function loadstatuslog() {
				readLogFile("/openWB/ramdisk/ladestatus.log", "#ladestatuslogdiv");
			}

			function mqttlog() {
				readLogFile("/openWB/ramdisk/mqtt.log", "#mqttdiv");
			}

			function rfidlog() {
				readLogFile("/openWB/ramdisk/rfid.log", "#rfiddiv");
			}

			function debuglog() {
				readLogFile("/openWB/ramdisk/openWB.log", "#debugdiv");
			}

			function smarthomelog() {
				readLogFile("/openWB/ramdisk/smarthome.log", "#smarthomediv");
			}

			function nurpvlog() {
				readLogFile("/openWB/ramdisk/nurpv.log", "#nurpvdiv");
			}

			function soclog() {
				readLogFile("/openWB/ramdisk/soc.log", "#socdiv");
			}

			function llanbindunglog() {
				readLogFile("/openWB/ramdisk/isss.log", "#llanbindungdiv");
			}
		</script>

	</head>
	<body>
		<?php
			$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
			foreach($lines as $line) {
				list($key, $value) = explode("=", $line, 2);
				${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
			}

			$speichervorhanden = trim( file_get_contents( $_SERVER['DOCUMENT_ROOT'] . '/openWB/ramdisk/speichervorhanden' ) );
		?>

		<!-- Preloader with Progress Bar -->
		<div id="preloader">
			<div id="preloader-inner">
				<div class="row">
					<div class="mx-auto d-block justify-content-center">
						<img id="preloader-image" src="img/favicons/preloader-image.png" alt="openWB">
					</div>
				</div>
				<div id="preloader-info" class="row justify-content-center mt-2">
					<div class="col-10 col-sm-6">
						Bitte warten, während die Seite aufgebaut wird.
					</div>
				</div>
				<div class="row justify-content-center mt-2">
					<div class="col-10 col-sm-6">
						<div class="progress active">
							<div class="progress-bar progress-bar-success progress-bar-striped progress-bar-animated" id="preloaderbar" role="progressbar">
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Landing Page -->
		<div id="nav-placeholder"></div>
		<div role="main" class="container" style="margin-top: 20px">
			<h1>Status</h1>
			<div class="wrapper">

				<!-- Ladepunkte-->
				<?php for( $chargepointNum = 1; $chargepointNum <= 8; $chargepointNum++ ){ ?>
					<div class="card border-primary hide" id="lp<?php echo $chargepointNum ?>">
						<div class="card-header bg-primary">
							Ladepunkt <?php echo $chargepointNum . " (" . ${'lp'.$chargepointNum.'nameold'} . ")"; ?>
						</div>
						<div class="card-body">
							<div class="table-responsive">
								<table class="table table-sm ">
									<tbody>
										<tr class="faultStrLpRow hide">
											<th scope="row">Störungsbeschreibung</th>
											<td class="faultStrLp"></td>
										</tr>
										<tr class="stromvorgabeRow">
											<th scope="row">Ladestromvorgabe [A]</th>
											<td class="stromvorgabe">--</td>
										</tr>
										<tr class="ladeleistungRow">
											<th scope="row">Ladeleistung [W]</th>
											<td class="ladeleistung">--</td>
										</tr>
										<tr class="kWhCounterRow">
											<th scope="row">Zählerstand [kWh]</th>
											<td class="kWhCounter">--</td>
										</tr>
										<tr class="socRow hide">
											<th scope="row">SoC [%]</th>
											<td class="soc">--</td>
										</tr>
										<tr class="faultStrSocLpRow hide">
											<th scope="row">Störungsbeschreibung</th>
											<td class="faultStrSocLp"></td>
										</tr>
									</tbody>
								</table>
							</div>
							<div class="table-responsive">
								<table class="table">
									<thead>
										<tr>
											<th scope="col"></th>
											<th scope="col">Phase 1</th>
											<th scope="col">Phase 2</th>
											<th scope="col">Phase 3</th>
										</tr>
									</thead>
									<tbody>
										<tr class="spannungRow">
											<th scope="row">Spannung [V]</th>
											<td class="spannungP1">--</td>
											<td class="spannungP2">--</td>
											<td class="spannungP3">--</td>
										</tr>
										<tr class="stromstaerkeRow">
											<th scope="row">Stromstärke [A]</th>
											<td class="stromstaerkeP1">--</td>
											<td class="stromstaerkeP2">--</td>
											<td class="stromstaerkeP3">--</td>
										</tr>
										<tr class="powerFaktorRow hide">
											<th scope="row">Power Faktor</th>
											<td class="powerFaktorP1">--</td>
											<td class="powerFaktorP2">--</td>
											<td class="powerFaktorP3">--</td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>
				<?php } ?>

				<!-- Ladepunkte Gesamt -->
				<div class="card border-primary hide" id="lpges">
					<div class="card-header bg-primary">
						Ladepunkte Gesamt
					</div>
					<div class="card-body">
						<div class="table-responsive">
							<table class="table">
								<tbody>
									<tr id="ladeleistungAllRow">
										<th scope="row">Ladeleistung [W]</th>
										<td><div id="ladeleistungAll"></div></td>
									</tr>
									<tr id="kWhCounterAllRow">
										<th scope="row">Zählerstand [kWh]</th>
										<td><div id="kWhCounterAll"></div></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>

				<!-- EVU  -->
				<div class="card border-danger <?php if($wattbezugmodulold == "none") echo "hide" ?>">
					<div class="card-header bg-danger">
						EVU
					</div>
					<div class="card-body">
						<div class="table-responsive">
							<table class="table" id="evu1">
								<tbody>
									<tr id="faultStrEvuRow" class="hide">
										<th scope="row">Störungsbeschreibung</th>
										<td><div id="faultStrEvu"></div></td>
									</tr>
									<tr id="gesamtleistungEvuStatusId">
										<th scope="row">Gesamtleistung [W]</th>
										<td><div id="wattbezugdiv">--</div></td>
									</tr>
									<tr id="bezugEvuStatusId">
										<th scope="row">Bezug [kWh]</th>
										<td><div id="bezugkwhdiv">--</div></td>
									</tr>
									<tr id="einspeisungEvuStatusId">
										<th scope="row">Einspeisung [kWh]</th>
										<td><div id="einspeisungkwhdiv">--</div></td>
									</tr>
									<tr id="frequenzEvuStatusId">
										<th scope="row">Frequenz [Hz]</th>
										<td><div id="evuhzdiv">--</div></td>
									</tr>
									<tr id="schieflastEvuStatusId">
										<th scope="row">Schieflast [A]</th>
										<td><div id="schieflastdiv">--</div></td>
									</tr>
								</tbody>
							</table>
						</div>
						<div class="table-responsive">
							<table class="table" id="evu2">
								<thead>
									<tr>
										<th scope="col"></th>
										<th scope="col">Phase 1</th>
										<th scope="col">Phase 2</th>
										<th scope="col">Phase 3</th>
									</tr>
								</thead>
								<tbody>
									<tr id="spannungEvuStatusId">
										<th scope="row">Spannung [V]</th>
										<td><div id="evuv1div">--</div></td>
										<td><div id="evuv2div">--</div></td>
										<td><div id="evuv3div">--</div></td>
									</tr>
									<tr id="stromstaerkeEvuStatusId">
										<th scope="row">Stromstärke [A]</th>
										<td><div id="bezuga1div">--</div></td>
										<td><div id="bezuga2div">--</div></td>
										<td><div id="bezuga3div">--</div></td>
									</tr>
									<tr id="leistungEvuStatusId">
										<th scope="row">Leistung [W]</th>
										<td><div id="bezugw1div">--</div></td>
										<td><div id="bezugw2div">--</div></td>
										<td><div id="bezugw3div">--</div></td>
									</tr>
									<tr id="powerfaktorEvuStatusId">
										<th scope="row">Power Faktor</th>
										<td><div id="evupf1div">--</div></td>
										<td><div id="evupf2div">--</div></td>
										<td><div id="evupf3div">--</div></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>

				<!--PV Gesamt-Anlagendaten-->
				<div class="card border-success hide" id="pvGes">
					<div class="card-header bg-success">
						PV Gesamt-Anlagendaten
					</div>
					<div class="card-body">
						<div class="table-responsive">
							<table class="table">
								<tbody>
									<tr id="pvCounterRow">
										<th scope="row">Counter</th>
										<td><div id="pvcounterdiv">--</div></td>
									</tr>
									<tr id="leistungRow">
										<th scope="row">Leistung [W]</th>
										<td><div id="pvwattdiv">--</div></td>
									</tr>
									<tr id="gesamtertragRow">
										<th scope="row">Gesamtertrag [kWh]</th>
										<td><div id="pvkwhdiv">--</div></td>
									</tr>
									<tr id="tagesertragRow">
										<th scope="row">Tagesertrag [kWh]</th>
										<td><div id="daily_pvkwhdiv">--</div></td>
									</tr>
									<tr id="monatsertragRow">
										<th scope="row">Monatsertrag [kWh]</th>
										<td><div id="monthly_pvkwhdiv">--</div></td>
									</tr>
									<tr id="jahresertragRow">
										<th scope="row">Jahresertrag [kWh]</th>
										<td><div id="yearly_pvkwhdiv">--</div></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>

				<!--PV Wechselrichter-->
				<?php for( $inverterNum = 1; $inverterNum <= 2; $inverterNum++ ){ ?>
					<div class="card border-success hide" id="inverter<?php echo $inverterNum ?>">
						<div class="card-header bg-success">
							PV Wechselrichter 
							<?php 
							echo $inverterNum ;
							if (${'name_wechselrichter'.$inverterNum.'old'} != '') {
								echo ' (' . ${'name_wechselrichter'.$inverterNum.'old'} . ')';
							}
							?>
						</div>
						<div class="card-body">
							<div class="table-responsive">
								<table class="table">
									<tbody>
										<tr class="faultStrPvRow hide">
											<th scope="row">Störungsbeschreibung</th>
											<td class="faultStrPv"></td>
										</tr>
										<tr>
											<th scope="row">Leistung [W]</th>
											<td class="powerInverter">--</td>
										</tr>
										<tr>
											<th scope="row">Gesamtertrag [kWh]</th>
											<td><div class="yieldInverter">--</div></td>
										</tr>
										<tr class="hide">
											<th scope="row">Tagesertrag [kWh]</th>
											<td><div class="dYieldInverter">--</div></td>
										</tr>
										<tr class="hide">
											<th scope="row">Monatsertrag [kWh]</th>
											<td><div class="mYieldInverter">--</div></td>
										</tr>
										<tr class="hide">
											<th scope="row">Jahresertrag [kWh]</th>
											<td><div class="yYieldInverter">--</div></td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>
				<?php } ?>

				<!-- Speicher -->
				<div class="card border-warning hide" id="speicher">
					<div class="card-header bg-warning">
						Speicher
					</div>
					<div class="card-body">
						<div class="table-responsive">
							<table class="table">
								<tbody>
									<tr id="faultStrBatRow" class="hide">
										<th scope="row">Störungsbeschreibung</th>
										<td><div id="faultStrBat"></div></td>
									</tr>
									<tr id="geladenRow">
										<th scope="row">geladen [kWh]</th>
										<td><div id="speicherikwhdiv"></div></td>
									</tr>
									<tr id="entladenRow">
										<th scope="row">entladen [kWh]</th>
										<td><div id="speicherekwhdiv"></div></td>
									</tr>
									<tr id="wBatRow">
										<th scope="row">Leistung [W]</th>
										<td><div id="wBatDiv"></div></td>
									</tr>
									<tr id="socBatRow">
										<th scope="row">SoC [%]</th>
										<td><div id="socBatDiv"></div></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>

				<!-- Smarthome -->
				<div class="card border-info " id="Smarthome">
					<div class="card-header bg-info">
						Smart Home 2.0
					</div>
					<div class="card-body">
						<div class="table-responsive">
							<table class="table">
								<tbody>
									<tr id="wwattschaltRow">
										<th scope="row">Gesamtleistung abschaltbar [W]</th>
										<td><div id="wwattschalt"></div></td>
									</tr>
									<tr id="wwattnichtschaltRow">
										<th scope="row">Gesamtleistung übrige [W]</th>
										<td><div id="wwattnichtschalt"></div></td>
									</tr>
									<tr id="wuberschussRow">
										<th scope="row">Überschuss [W]</th>
										<td><div id="wuberschuss"></div></td>
									</tr>
									<tr id="wuberschussoffsetRow">
										<th scope="row">Überschuss mit Offset [W]</th>
										<td><div id="wuberschussoffset"></div></td>
									</tr>
									<tr id="wmaxspeicherladungRow">
										<th scope="row">Maximale Speicherladung [W]</th>
										<td><div id="wmaxspeicherladung"></div></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>

				<!--Verbraucher-->
				<?php for( $loadsNum = 1; $loadsNum <= 2; $loadsNum++ ){ ?>
					<div class="card border-secondary hide" id="loads<?php echo $loadsNum ?>">
						<div class="card-header bg-secondary">
							Verbraucher <?php echo ${'verbraucher'.$loadsNum.'_nameold'} ?>
						</div>
						<div class="card-body">
							<div class="table-responsive">
								<table class="table">
									<tbody>
										<tr class="leistungVerbraucherRow">
											<th scope="row">Leistung [W]</th>
											<td class="verbraucherWatt">--</td>
										</tr>
										<tr class="importVerbraucherRow">
											<th scope="row">Import [kWh]</th>
											<td class="importVerbraucher">--</td>
										</tr>
										<tr class="exportVerbraucherRow">
											<th scope="row">Export [kWh]</th>
											<td class="exportVerbraucher">--</td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>
				<?php } ?>
			</div> <!-- wrapper -->

			<!--Log-->
			<div id="accordion" class="accordion">
				<div class="card mb-0">
					<div class="card-header bg-secondary collapsed" data-toggle="collapse" data-target="#collapseOne">
						<a class="card-title">Ladestatus Änderungen </a>
					</div>
					<div id="collapseOne" class="card-body collapse" data-parent="#accordion">
						<button class="btn btn-info reloadLadestatusLog" style="margin-bottom:12px" type="reset">Aktualisieren <i class="fas fa-redo-alt"></i> </button>
						<pre id="ladestatuslogdiv">Lade Daten...</pre>
					</div>
					<div class="card-header bg-secondary collapsed" data-toggle="collapse" data-target="#collapseTwo">
						<a class="card-title">SmartHome Log </a>
					</div>
					<div id="collapseTwo" class="card-body collapse" data-parent="#accordion">
						<button class="btn btn-info reloadSmartHomeLog mr-3" style="margin-bottom:12px" type="reset">Aktualisieren <i class="fas fa-redo-alt"></i> </button>
						<pre id="smarthomediv">Lade Daten...</pre>
					</div>
					<div class="card-header bg-secondary collapsed" data-toggle="collapse" data-target="#collapseThree">
						<a class="card-title">RFID Log </a>
					</div>
					<div id="collapseThree" class="card-body collapse" data-parent="#accordion">
						<button class="btn btn-info reloadRfidLog" style="margin-bottom:12px" type="reset">Aktualisieren <i class="fas fa-redo-alt"></i> </button>
						<pre id="rfiddiv">Lade Daten...</pre>
					</div>
					<div class="card-header bg-secondary collapsed" data-toggle="collapse" data-target="#collapseFour">
						<a class="card-title">Mqtt Log </a>
					</div>
					<div id="collapseFour" class="card-body collapse" data-parent="#accordion">
						<button class="btn btn-info reloadMqttLog" style="margin-bottom:12px" type="reset">Aktualisieren <i class="fas fa-redo-alt"></i> </button>
						<pre id="mqttdiv">Lade Daten...</pre>
					</div>
					<div class="card-header bg-secondary collapsed" data-toggle="collapse" data-target="#collapseFive">
						<a class="card-title">Debug Log </a>
					</div>
					<div id="collapseFive" class="card-body collapse" data-parent="#accordion">
						<button class="btn btn-info reloadDebugLog" style="margin-bottom:12px" type="reset">Aktualisieren <i class="fas fa-redo-alt"></i> </button>
						<pre id="debugdiv">Lade Daten...</pre>
					</div>
					<div class="card-header bg-secondary collapsed" data-toggle="collapse" data-target="#collapseSix">
						<a class="card-title">Nur PV Log </a>
					</div>
					<div id="collapseSix" class="card-body collapse" data-parent="#accordion">
						<button class="btn btn-info reloadPvLog" style="margin-bottom:12px" type="reset">Aktualisieren <i class="fas fa-redo-alt"></i> </button>
						<pre id="nurpvdiv">Lade Daten...</pre>
					</div>
					<div class="card-header bg-secondary collapsed" data-toggle="collapse" data-target="#collapseSeven">
						<a class="card-title">EV SoC Log </a>
					</div>
					<div id="collapseSeven" class="card-body collapse" data-parent="#accordion">
						<button class="btn btn-info reloadSocLog" style="margin-bottom:12px" type="reset">Aktualisieren <i class="fas fa-redo-alt"></i> </button>
						<pre id="socdiv">Lade Daten...</pre>
					</div>
					<div class="card-header bg-secondary collapsed" data-toggle="collapse" data-target="#collapseEight">
						<a class="card-title">Nur Ladepunkt Log </a>
					</div>
					<div id="collapseEight" class="card-body collapse" data-parent="#accordion">
						<button class="btn btn-info reloadLLAnbindungLog" style="margin-bottom:12px" type="reset">Aktualisieren <i class="fas fa-redo-alt"></i> </button>
						<pre id="llanbindungdiv">Lade Daten...</pre>
					</div>
				</div>
			</div>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Status</small>
			</div>
		</footer>

		<script>

			// load navbar, be careful: it loads asynchronous
			$.get(
				{ url: "themes/navbar.html", cache: false },
				function(data){
					$("#nav-placeholder").replaceWith(data);
					$('#navStatus').addClass('disabled');
				}
			);

			$(function() {
				if('<?php echo $kostalplenticoreip2old ?>' == 'none') {
					$('#pvinverter1and2div').hide();
				}
			});

			var timeOfLastMqttMessage = 0;  // holds timestamp of last received message
			var landingpageShown = false;  // holds flag for landing page being shown

			function processPreloader(mqttTopic) {
				// sets flag for topic received in topic-array
				// and updates the preloader progress bar
				if ( !landingpageShown ) {
					var countTopicsReceived = 0;
					for ( var index = 0; index < topicsToSubscribe.length; index ++) {
						if ( topicsToSubscribe[index][0] == mqttTopic && topicsToSubscribe[index][1] == 0 ) {
							// topic found in array
							topicsToSubscribe[index][1] = 1;  // mark topic as received
						};
						if ( topicsToSubscribe[index][1] > 0 ) {
							countTopicsReceived++;
						}
					};
					// countTopicsToBeReceived holds all topics flagged 1 and not only those for preloader
					countTopicsReceived = countTopicsReceived - countTopicsNotForPreloader;
					var countTopicsToBeReceived = topicsToSubscribe.length - countTopicsNotForPreloader;
					var percentageReceived = (countTopicsReceived / countTopicsToBeReceived * 100).toFixed(0);
					var timeBetweenTwoMessages = Date.now() - timeOfLastMqttMessage;
					if ( timeBetweenTwoMessages > 3000 ) {
						console.log('timeout');
						// latest after 3 sec without new messages
						percentageReceived = 100;
						// debug output
						topicsToSubscribe.forEach((item, i) => {
							if ( item[1] == 0 ) {
								console.log('not received: ' + item[0]);
							}
						});

					}
					timeOfLastMqttMessage = Date.now();
					$("#preloaderbar").width(percentageReceived+"%");
					$("#preloaderbar").text(percentageReceived+" %");
					if ( percentageReceived == 100 ) {
						landingpageShown = true;
						setTimeout(function (){
							// delay a little bit
							$("#preloader").fadeOut(1000);
						}, 500);
					}
				}
			}

			$(document).ready(function(){

				// load scripts synchronously in order specified
				var scriptsToLoad = [
					// load mqtt library
					'js/mqttws31.js',
					// functions for processing messages
					'status/processAllMqttMsg.js?ver=20210209',
					// functions performing mqtt and start mqtt-service
					'status/setupMqttServices.js?ver=20210209',
				];
				scriptsToLoad.forEach(function(src) {
					var script = document.createElement('script');
					script.src = src;
					script.async = false;
					document.body.appendChild(script);
				});
			});  // end document ready

			$('.reloadLadestatusLog').click(function(event){
				loadstatuslog();
			});
			$('#collapseOne').on('shown.bs.collapse', function(){
				loadstatuslog();
			});
			$('.reloadSmartHomeLog').click(function(event){
				smarthomelog();
			});
			$('#collapseTwo').on('shown.bs.collapse', function(){
				smarthomelog();
			});
			$('.reloadRfidLog').click(function(event){
				rfidlog();
			});
			$('#collapseThree').on('shown.bs.collapse', function(){
				rfidlog();
			});
			$('.reloadMqttLog').click(function(event){
				mqttlog();
			});
			$('#collapseFour').on('shown.bs.collapse', function(){
				mqttlog();
			});
			$('.reloadDebugLog').click(function(event){
				debuglog();
			});
			$('#collapseFive').on('shown.bs.collapse', function(){
				debuglog();
			});
			$('.reloadPvLog').click(function(event){
				nurpvlog();
			});
			$('#collapseSix').on('shown.bs.collapse', function(){
				nurpvlog();
			});
			$('.reloadSocLog').click(function(event){
				soclog();
			});
			$('#collapseSeven').on('shown.bs.collapse', function(){
				soclog();
			});
			$('.reloadLLAnbindungLog').click(function(event){
				llanbindunglog();
			});
			$('#collapseEight').on('shown.bs.collapse', function(){
				llanbindunglog();
			});
		</script>

	</body>
</html>
