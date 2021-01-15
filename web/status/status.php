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
		<link rel="stylesheet" type="text/css" href="./settings/settings_style.css">
		<!-- local css due to async loading of theme css -->
		<style type="text/css">
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
			#thegraph > div {
				height: 350px;
			}
			#electricityPriceChartCanvasDiv {
				height: 150px;
			}
		</style>
		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20201231" ></script>
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
		</script>

		<script>
			var doInterval;

			function getfile() {
				$.ajaxSetup({ cache: false});


				$.ajax({
					url: "/openWB/ramdisk/llkwhges",
					complete: function(request){
						$("#llkwhgesdiv").html(request.responseText);
					}
				});

				$.ajax({
					url: "/openWB/ramdisk/pvallwh",
					complete: function(request){
						$("#pvkwhdiv").html((request.responseText / 1000).toFixed(2));
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/monthly_pvkwhk",
					complete: function(request){
						$("#monthly_pvkwhdiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/yearly_pvkwhk",
					complete: function(request){
						$("#yearly_pvkwhdiv").html(request.responseText);
						if ( request.responseText > 100 ) {
							$('#pvpartlycounterdiv').show();
						}
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvwatt1",
					complete: function(request){
						// zur Anzeige Wert positiv darstellen
						// (Erzeugung liegt als Negativwert vor)
						var value = parseInt(request.responseText) * -1;
						$("#pvwattdiv1").html(""+value);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvkwhk1",
					complete: function(request){
						$("#pvkwhdiv1").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/daily_pvkwhk1",
					complete: function(request){
						$("#daily_pvkwhdiv1").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/monthly_pvkwhk1",
					complete: function(request){
						$("#monthly_pvkwhdiv1").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/yearly_pvkwhk1",
					complete: function(request){
						$("#yearly_pvkwhdiv1").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvwatt2",
					complete: function(request){
						// zur Anzeige Wert positiv darstellen
						// (Erzeugung liegt als Negativwert vor)
						var value = parseInt(request.responseText) * -1;
						$("#pvwattdiv2").html(""+value);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvkwhk2",
					complete: function(request){
						$("#pvkwhdiv2").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/daily_pvkwhk2",
					complete: function(request){
						$("#daily_pvkwhdiv2").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/monthly_pvkwhk2",
					complete: function(request){
						$("#monthly_pvkwhdiv2").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/yearly_pvkwhk2",
					complete: function(request){
						$("#yearly_pvkwhdiv2").html(request.responseText);
					}
				});
			}
			doInterval = setInterval(getfile, 2000);

			function loadstatuslog() {
				$.ajax({
					url: "/openWB/ramdisk/ladestatus.log",
					complete: function(request){
						var lines = request.responseText.split("\n");
						var result = "";
						for(var i=0; i<lines.length; i++)
							result = lines[i] + "\n" + result;
						$("#ladestatuslogdiv").html(result);
					}
				});
			}
			loadstatuslog();
			function mqttlog() {
				$.ajax({
					url: "/openWB/ramdisk/mqtt.log",
					complete: function(request){
						var lines = request.responseText.split("\n");
						var result = "";
						for(var i=0; i<lines.length; i++)
							result = lines[i] + "\n" + result;
						$("#mqttdiv").html(result);
					}
				});
			}
			mqttlog();
			function rfidlog() {
				$.ajax({
					url: "/openWB/ramdisk/rfid.log",
					complete: function(request){
						var lines = request.responseText.split("\n");
						var result = "";
						for(var i=0; i<lines.length; i++)
							result = lines[i] + "\n" + result;
						$("#rfiddiv").html(result);
					}
				});
			}
			rfidlog();
			function debuglog() {
				$.ajax({
					url: "/openWB/ramdisk/openWB.log",
					complete: function(request){
						var lines = request.responseText.split("\n");
						var result = "";
						for(var i=0; i<lines.length; i++)
							result = lines[i] + "\n" + result;
						$("#debugdiv").html(result);
					}
				});
			}
			debuglog();
			function smarthomelog() {
				$.ajax({
					url: "/openWB/ramdisk/smarthome.log",
					complete: function(request){
						var lines = request.responseText.split("\n");
						var result = "";
						for(var i=0; i<lines.length; i++)
							result = lines[i] + "\n" + result;
						$("#smarthomediv").html(result);
					}
				});
			}
			smarthomelog();
			function nurpvlog() {
				$.ajax({
					url: "/openWB/ramdisk/nurpv.log",
					complete: function(request){
						var lines = request.responseText.split("\n");
						var result = "";
						for(var i=0; i<lines.length; i++)
							result = lines[i] + "\n" + result;
						$("#nurpvdiv").html(result);
					}
				});
			}
			nurpvlog();
			function soclog() {
				$.ajax({
					url: "/openWB/ramdisk/soc.log",
					complete: function(request){
						var lines = request.responseText.split("\n");
						var result = "";
						for(var i=0; i<lines.length; i++)
							result = lines[i] + "\n" + result;
						$("#socdiv").html(result);
					}
				});
			}
			soclog();
		</script>

		<?php
			$owbversion = file_get_contents('/var/www/html/openWB/web/version');
			$result = '';
			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach ($lines as $line) {
				if (strpos($line, "lp1name=") !== false) {
					list(, $lp1nameold) = explode("=", $line);
				}
				if (strpos($line, "lp2name=") !== false) {
					list(, $lp2nameold) = explode("=", $line);
				}
				if (strpos($line, "lp3name=") !== false) {
					list(, $lp3nameold) = explode("=", $line);
				}
				if (strpos($line, "lastmanagement=") !== false) {
					list(, $lastmanagementold) = explode("=", $line);
				}
				if (strpos($line, "lastmanagements2=") !== false) {
					list(, $lastmanagements2old) = explode("=", $line);
				}
				if (strpos($line, "simplemode=") !== false) {
					list(, $simplemodeold) = explode("=", $line);
				}
				if (strpos($line, "verbraucher1_name=") !== false) {
					list(, $verbraucher1_nameold) = explode("=", $line);
				}
				if (strpos($line, "verbraucher2_name=") !== false) {
					list(, $verbraucher2_nameold) = explode("=", $line);
				}
				if (strpos($line, "name_wechselrichter1=") !== false) {
					list(, $name_wechselrichter1old) = explode("=", $line);
					# entferne EOL von String
					$name_wechselrichter1old = trim(preg_replace('/\s+/', '', $name_wechselrichter1old));
				}
				if (strpos($line, "name_wechselrichter2=") !== false) {
					list(, $name_wechselrichter2old) = explode("=", $line);
					# entferne EOL von String
					$name_wechselrichter2old = trim(preg_replace('/\s+/', '', $name_wechselrichter2old));
				}
				if (strpos($line, "kostalplenticoreip2=") !== false) {
					# wird benötigt, für Anzeige der getrennten WR-Daten an/aus
					list(, $kostalplenticoreip2old) = explode("=", $line);
					# entferne EOL von String
					$kostalplenticoreip2old = trim(preg_replace('/\s+/', '', $kostalplenticoreip2old));
				}
			}
		?>
		<script>
			$(function() {
				var lp2akt = <?php echo $lastmanagementold ?>;
				var lp3akt = <?php echo $lastmanagements2old ?>;

				if(lp2akt == '0') {
					$('#ladepunkt2div').hide();
				} else {
					$('#ladepunkt2div').show();
				}
				if(lp2akt == '0') {
					$('#ladepunkt3div').hide();
				} else {
					$('#ladepunkt3div').show();
				}
			});
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
		<!-- style instead of css due to async loading of theme css -->
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
			<form action="./tools/saveconfig.php" method="POST">

				<!-- EVU  -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div>EVU</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="table-responsive">
							<table class="table table-sm w-50" id="evu1">
								<tbody>
									<tr id="schieflastEvuStatusId">
										<th scope="row">Schieflast [A]</th>
										<td><div id="schieflastdiv"></div></td>
									</tr>
									<tr id="gesamtleistungEvuStatusId">
										<th scope="row">Gesamtleistung [W]</th>
										<td><div id="wattbezugdiv"></div></td>
									</tr>
									<tr id="frequenzEvuStatusId">
										<th scope="row">Frequenz [Hz]</th>
										<td><div id="evuhzdiv"></div></td>
									</tr>																							
									<tr id="bezugEvuStatusId">
										<th scope="row">Bezug [kWh]</th>
										<td><div id="bezugkwhdiv"></div></td>
									</tr>
									<tr id="einspeisungEvuStatusId">
										<th scope="row">Einspeisung [kWh]</th>
										<td><div id="einspeisungkwhdiv"></div></td>
									</tr>									
								</tbody>
							</table>
						</div>
						<div class="table-responsive">
							<table class="table table-sm" id="evu2">
								<thead>
									<tr>
										<th scope="col"></th>
										<th scope="col">Phase 1</th>
										<th scope="col">Phase 2</th>
										<th scope="col">Phase 3</th>
									</tr>
								</head>
								<tbody>
									<tr id =spannungEvuStatusId>
										<th scope="row">Spannung [V]</th>
										<td><div id="evuv1div"></div></td>
										<td><div id="evuv2div"></div></td>
										<td><div id="evuv3div"></div></td>
									</tr>
									<tr id =stromstaerkeEvuStatusId>
										<th scope="row">Stromstärke [A]</th>
										<td><div id="bezuga1div"></div></td>
										<td><div id="bezuga2div"></div></td>
										<td><div id="bezuga3div"></div></td>
									</tr>
									<tr id =leistungEvuStatusId>
										<th scope="row">Leistung [W]</th>
										<td><div id="bezugw1div"></div></td>
										<td><div id="bezugw2div"></div></td>
										<td><div id="bezugw3div"></div></td>
									</tr>
									<tr id =powerfaktorEvuStatusId>
										<th scope="row">Power Faktor</th>
										<td><div id="evupf1div"></div></td>
										<td><div id="evupf2div"></div></td>
										<td><div id="evupf3div"></div></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>

				<!-- Ladepunkte-->
				<?php for( $chargepointNum = 1; $chargepointNum <= 8; $chargepointNum++ ){ ?>
					<div class="card border-secondary" id="lp<?php echo $chargepointNum ?>">
						<div class="card-header bg-secondary">
							<div class="form-group mb-0">
								<div class="form-row vaRow mb-0">
									<div>Ladepunkt <?php echo $chargepointNum ?></div>
								</div>
							</div>
						</div>
						<div class="card-body">
							<div class="table-responsive">
								<table class="table table-sm w-50">
									<tbody>
										<tr class=stromvorgabeRow>
											<th scope="row">Ladestromvorgabe [A]</th>
											<td class=stromvorgabe></td>
										</tr>
										<tr class=ladeleistungRow>
											<th scope="row">Ladeleistung [W]</th>
											<td class=ladeleistung></td>
										</tr>
										<tr class=kWhCounterRow>
											<th scope="row">Zählerstand [kWh]</th>
											<td class="kWhCounter"></td>
										</tr>
										<tr class=socRow>
											<th scope="row">SoC [%]</th>
											<td class=soc></td>
										</tr>
									</tbody>
								</table>
							</div>
							<div class="table-responsive">
								<table class="table table-sm">
									<thead>
										<tr>
											<th scope="col"></th>
											<th scope="col">Phase 1</th>
											<th scope="col">Phase 2</th>
											<th scope="col">Phase 3</th>
										</tr>
									</head>
									<tbody>
										<tr class=spannungRow>
											<th scope="row">Spannung [V]</th>
											<td class=spannungP1></td>
											<td class=spannungP2></td>
											<td class=spannungP3></td>
										</tr>
										<tr class=powerFaktorRow>
											<th scope="row">Power Faktor</th>
											<td class=powerFaktorP1></td>
											<td class=powerFaktorP2></td>
											<td class=powerFaktorP3></td>
										</tr>
										<tr class=stromstaerkeRow>
											<th scope="row">Stromstärke [A]</th>
											<td class=stromstaerkeP1></td>
											<td class=stromstaerkeP2></td>
											<td class=stromstaerkeP3></td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>
				<?php } ?>

				<!-- Ladepunkte Gesamt -->
				<div class="card border-secondary" id="lpges">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div>Ladepunkte Gesamt</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="table-responsive">
							<table class="table table-sm w-50">
								<tbody>
									<tr id=ladeleistungAllRow>
										<th scope="row">Ladeleistung [W]</th>
										<td><div id="ladeleistungAll"></div></td>
									</tr>
									<tr id=kWhCounterAllRow>
										<th scope="row">Zählerstand [kWh]</th>
										<td><div id="kWhCounterAll"></div></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>

				<!--PV Gesamt-Anlagendaten-->
				<div class="card border-secondary" id="pvGes">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div>PV Gesamt-Anlagendaten</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="table-responsive">
							<table class="table table-sm ">
								<tbody>
									<tr id=pvCounterRow>
										<th scope="row">Counter</th>
										<td><div id="pvcounterdiv"></div></td>
									</tr>
									<tr id=leistungRow>
										<th scope="row">Leistung [W]</th>
										<td><div id="pvwattdiv"></div></td>
									</tr>
									<tr id=gesamtertragRow>
										<th scope="row">Gesamtertrag [kWh]</th>
										<td><div id="pvkwhdiv"></div></td>
									</tr>
									<tr id=tagesertragRow>
										<th scope="row">Tagesertrag [kWh]</th>
										<td><div id="daily_pvkwhdiv"></div></td>
									</tr>
									<tr id=monatsertragRow>
										<th scope="row">Monatsertrag [kWh]</th>
										<td><div id="monthly_pvkwhdiv"></div></td>
									</tr>
									<tr id=jahresertragRow>
										<th scope="row">Jahresertrag [kWh]</th>
										<td><div id="yearly_pvkwhdiv"></div></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>

					<!--PV Wechselrichter-->
					<?php for( $inverterNum = 1; $inverterNum <= 2; $inverterNum++ ){ ?>
					<div class="card border-secondary" id="inverter<?php echo $inverterNum ?>">
						<div class="card-header bg-secondary">
							<div class="form-group mb-0">
								<div class="form-row vaRow mb-0">
									<div>PV Wechselrichter 
										<?php 
										echo $inverterNum ;
										if (${'name_wechselrichter'.$inverterNum.'old'} != '') {
											echo ' (';
											echo ${'name_wechselrichter'.$inverterNum.'old'};
											echo ')';
										}
										?>
									</div>
								</div>
							</div>
						</div>
						<div class="card-body">
							<div class="table-responsive">
								<table class="table table-sm w-50">
									<tbody>
										<tr class=leistungPvRow>
											<th scope="row">Leistung [W]</th>
											<td class=></td>
										</tr>
										<tr class=gesamtertragPvRow>
											<th scope="row">Gesamtertrag [kWh]</th>
											<td class=></td>
										</tr>
										<tr id=tagesertragPvRow>
										<th scope="row">Tagesertrag [kWh]</th>
										<td><div id=""></div></td>
										</tr>
										<tr id=monatsertragPvRow>
											<th scope="row">Monatsertrag [kWh]</th>
											<td><div id=""></div></td>
										</tr>
										<tr id=jahresertragPvRow>
											<th scope="row">Jahresertrag [kWh]</th>
											<td><div id=""></div></td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>
				<?php } ?>

				<!-- Speicher -->
				<div class="card border-secondary" id="speicher">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div>Speicher</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="table-responsive">
							<table class="table table-sm w-50">
								<tbody>
									<tr id=geladenRow>
										<th scope="row">geladen [kWh]</th>
										<td><div id="speicherikwhdiv"></div></td>
									</tr>
									<tr id=entladenRow>
										<th scope="row">entladen [kWh]</th>
										<td><div id="speicherekwhdiv"></div></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>

				<!--Verbraucher-->
				<?php for( $loadsNum = 1; $loadsNum <= 2; $loadsNum++ ){ ?>
					<div class="card border-secondary" id="loads<?php echo $loadsNum ?>">
						<div class="card-header bg-secondary">
							<div class="form-group mb-0">
								<div class="form-row vaRow mb-0">
									<div>Verbraucher <?php echo ${'verbraucher'.loadsNum.'_nameold'} ?></div>
								</div>
							</div>
						</div>
						<div class="card-body">
							<div class="table-responsive">
								<table class="table table-sm w-50">
									<tbody>
										<tr class=leistungVerbraucherRow>
											<th scope="row">Leistung [W]</th>
											<td class=verbraucherWatt></td>
										</tr>
										<tr class=importVerbraucherRow>
											<th scope="row">Import [kWh]</th>
											<td class=importVerbraucher></td>
										</tr>
										<tr class=exportVerbraucherRow>
											<th scope="row">Export [kWh]</th>
											<td class=exportVerbraucher></td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>
				<?php } ?>

				<!--Log-->
				<div id="accordion" class="accordion">
					<div class="card mb-0">
						<div class="card-header bg-secondary collapsed" data-toggle="collapse" href="#collapseOne">
							<a class="card-title">Ladestatus Änderungen </a>
						</div>
						<div id="collapseOne" class="card-body collapse" style="white-space: pre-line " data-parent="#accordion">
						<div id="ladestatuslogdiv"></div>
						</div>
						
						<div class="card-header bg-secondary collapsed" data-toggle="collapse" href="#collapseTwo">
							<a class="card-title">SmartHome Log </a>
						</div>
						<div id="collapseTwo" class="card-body collapse" style="white-space: pre-line " data-parent="#accordion">
						<div id="smarthomediv"></div>
						</div>
						
						<div class="card-header bg-secondary collapsed" data-toggle="collapse" href="#collapseThree">
							<a class="card-title">RFID Log </a>
						</div>
						<div id="collapseThree" class="card-body collapse" style="white-space: pre-line " data-parent="#accordion">
						<div id="rfiddiv"></div>
						</div>

						<div class="card-header bg-secondary collapsed" data-toggle="collapse" href="#collapseFour">
							<a class="card-title">Mqtt Log </a>
						</div>
						<div id="collapseFour" class="card-body collapse" style="white-space: pre-line " data-parent="#accordion">
						<div id="mqttdiv"></div>
						</div>
						
						<div class="card-header bg-secondary collapsed" data-toggle="collapse" href="#collapseFive">
							<a class="card-title">Debug Log </a>
						</div>
						<div id="collapseFive" class="card-body collapse" style="white-space: pre-line " data-parent="#accordion">
						<div id="debugdiv"></div>
						</div>
						
						<div class="card-header bg-secondary collapsed" data-toggle="collapse" href="#collapseSix">
							<a class="card-title">Nur PV Log </a>
						</div>
						<div id="collapseSix" class="card-body collapse" style="white-space: pre-line " data-parent="#accordion">
						<div id="nurpvdiv"></div>
						</div>
						
						<div class="card-header bg-secondary collapsed" data-toggle="collapse" href="#collapseSeven">
							<a class="card-title">EV SoC Log </a>
						</div>
						<div id="collapseSeven" class="card-body collapse" style="white-space: pre-line " data-parent="#accordion">
						<div id="socdiv"></div>
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

			// load navbar
			$("#nav-placeholder").load('themes/' + themeCookie + '/navbar.html?v=20210101', disableMenuItem);
			function disableMenuItem() {
				$('#navStatus').addClass('disabled');
			}

			$(function() {
				if('<?php echo $kostalplenticoreip2old ?>' == 'none') {
					$('#pvinverter1and2div').hide();
				}
			});
		</script>

		<script>
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
						//console.log('topics received', topicsToSubscribe[index][0], countTopicsReceived);
					}
				};
				// countTopicsToBeReceived holds all topics flagged 1 and not only those for preloader
				countTopicsReceived = countTopicsReceived - countTopicsNotForPreloader;
				var countTopicsToBeReceived = topicsToSubscribe.length - countTopicsNotForPreloader;
				var percentageReceived = (countTopicsReceived / countTopicsToBeReceived * 100).toFixed(0);
				var timeBetweenTwoMesagges = Date.now() - timeOfLastMqttMessage;
				if ( timeBetweenTwoMesagges > 3000 ) {
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
				// load Chart.js library
				'js/Chart.bundle.js',
				// load mqtt library
				'js/mqttws31.js',
				// some helper functions
				//'themes/dark/helperFunctions.js?ver=20201218',
				// functions for processing messages
				'status/processAllMqttMsg.js?ver=20201228a',
				// respective Chart.js definition live
				//'themes/dark/livechart.js?ver=20201218',
				// respective Chart.js definition awattar
				//'themes/dark/electricityPriceChart.js?ver=20201228',
				// functions performing mqtt and start mqtt-service
				'status/setupMqttServices.js?ver=20201228a',
			];
			scriptsToLoad.forEach(function(src) {
				var script = document.createElement('script');
				script.src = src;
				script.async = false;
				document.body.appendChild(script);
			});
		});  // end document ready
		</script>

	</body>
</html>
