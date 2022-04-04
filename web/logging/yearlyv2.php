<?php header( 'Refresh:600;' ); ?>
<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0">
		<title>Logging Jahresansicht Aufteilung (nighlty)</title>
		<meta name="author" content="Kevin Wieland, Michael Ortestein" />
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
		<!-- Bootstrap-Datepicker -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-datepicker/bootstrap-datepicker3.min.css">
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="logging/logging_style.css?ver=20210209">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
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
	</head>

	<body>

		<?php
			include $_SERVER['DOCUMENT_ROOT'].'/openWB/web/logging/navbar.php';
		?>

		<div role="main" class="container" style="margin-top:20px">
			<div class="row">
				<div class="col" style="text-align: center;">
					<h4>Logging Jahresansicht Aufteilung</h4>
				</div>
			</div>
			<div class="row justify-content-center">
				<div class="col-6 col-sm-3">
					<div class="input-group mb-3">
						<input class="form-control datepicker" id="theDate" type="text" readonly>
						<div class="input-group-append">
							<span class="input-group-text far fa-calendar-alt fa-lg vaRow"></span>
						</div>
					</div>
				</div>
			</div>

			<div class="row" id="thegraph">
				<div class="col">
					<div id="waitforgraphloadingdiv" style="text-align: center;">
						<br>Graph lädt, bitte warten...<br>
						<div class="spinner-grow text-muted mt-3"></div>
					</div>
					<div id="canvasdiv">
						<canvas id="canvas" style="height: 400px;"></canvas>
					</div>
				</div>
			</div>
		</div>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Logging/Jahr</small>
			</div>
		</footer>

		<!-- load Chart.js library -->
		<script src="js/Chart.bundle.min.js"></script>
		<script src="js/hammerjs@2.0.8"></script>
		<script src="js/chartjs-plugin-zoom@0.7.4"></script>
		<!-- load Bootstrap-Datepicker library -->
		<script src="js/bootstrap-datepicker/bootstrap-datepicker.min.js"></script>
		<script src="js/bootstrap-datepicker/bootstrap-datepicker.de.min.js"></script>

		<!-- load mqtt library -->
		<script src = "js/mqttws31.js" ></script>

		<!-- get parsed date, setup datepicker and load respective Chart.js definition -->
		<script>
			$(document).ready(function(){
				// GET expects date format Y like 2020
				// get parsed date and format nicely for input field
				const EARLIESTDATE = '01/01/2018';  // no earlier date
				// TODO: set earliest date to first occurrence of valid logging data
				var LATESTDATE = '12/31/' + new Date().getFullYear();
				var earliestDate = new Date(EARLIESTDATE);
				var latestDate = new Date(LATESTDATE);
				var url_string = window.location.href;
				var url = new URL(url_string);
				var parsedDateString = url.searchParams.get('date');
				var pattern = /^[0-9]{4}$/;
				var reloadNeeded = false;
				if ( parsedDateString == null || parsedDateString.match(pattern) == null ) {
					// nothing parsed or format not valid, so set date to today
					var parsedDate = new Date();
				} else {
					var parsedDate = new Date(parsedDateString);
					if ( (parsedDate < earliestDate) || (parsedDate > latestDate) ) {
						// date parsed was out of valid range so set to today
						parsedDate = new Date();
						reloadNeeded = true;
					}
				}
				if ( reloadNeeded ) {
					// date parsed was too early so reload with today
					alert('reloadNeeded! date: '+parsedDate.getFullYear());
					window.location.href = "logging/yearlyv2.php?date=" + parsedDate.getFullYear();
				}
				var theDate = parsedDate.getFullYear();
				$('#theDate').val(theDate);  // set value of input field
				// config the datepicker
				$('.datepicker').datepicker({
					format: 'yyyy',
					language: "de-DE",
					startDate: earliestDate.getFullYear().toString(),
					endDate: latestDate.getFullYear().toString(),
					startView: 'years',
					minViewMode: 'years',
					maxViewMode: 'years',
					todayBtn: false,
					todayHighlight: true,
					autoclose: true
				})
				.on('changeDate', function(e) {
					// `e` here contains the extra attributes
					var dateToParse = e.date.getFullYear();
					window.location.href = "logging/yearlyv2.php?date=" + dateToParse;
				});

				// load graph
				$.getScript("logging/yearlychartv1.js?ver=20210209");
			})
		</script>

	</body>

</html>
