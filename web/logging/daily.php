<?php header( 'Refresh:600;' ); ?>
<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0">
		<title>Logging Tagesansicht</title>
		<meta name="author" content="Kevin Wieland, Michael Ortenstein" />
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
					<h4>Logging Tagesansicht</h4>
				</div>
			</div>
			<div class="row justify-content-center">
				<div class="col-8 col-sm-6 col-md-5 col-lg-4">
					<div class="input-group mb-3">
						<i class="far fa-caret-square-left fa-lg vaRow mr-4" title="vorheriger Tag" id="prevday"></i>
						<input class="form-control datepicker" id="theDate" type="text" readonly>
					  	<div class="input-group-append">
					    	<span class="input-group-text far fa-calendar-alt fa-lg vaRow"></span>
					  	</div>
						<i class="far fa-caret-square-right fa-lg vaRow ml-4" title="nächster Tag" id="nextday"></i>
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
				<small>Sie befinden sich hier: Logging/Tag</small>
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
				// GET expects date format Y-m-d like 2020-10-08
				// get parsed date and format nicely for input field
				var earliestDate = new Date('2018/01/01 00:00:00');
				var url_string = window.location.href;
				var url = new URL(url_string);
				var parsedDateString = url.searchParams.get('date');
				var pattern = /^[0-9]{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$/;
				var reloadNeeded = false;
				if ( parsedDateString == null || parsedDateString.match(pattern) == null ) {
					// nothing parsed or format not valid, so set date to today
					var parsedDate = new Date();
					parsedDate.setHours(0,0,0,0);  // make sure time is all 0 for later comparisons
				} else {
					var parsedDate = new Date(parsedDateString);
					parsedDate.setHours(0,0,0,0);  // make sure time is all 0 for later comparisons
					if ( parsedDate < earliestDate ) {
						// date parsed was too early so set to today
						parsedDate = new Date();
						reloadNeeded = true;
					}
				}
				var dd = String(parsedDate.getDate()).padStart(2, '0');  // format with leading zeros
				var mm = String(parsedDate.getMonth() + 1).padStart(2, '0'); //January is 0!
				if ( reloadNeeded ) {
					// date parsed was too early so reload with today
					window.location.href = "logging/daily.php?date=" + parsedDate.getFullYear() + '-' + mm + '-' + dd;
				}
				var niceDate = dd + '.' + mm + '.' + parsedDate.getFullYear();  // now full date with leading zeros
				var dayOfWeek = parsedDate.toLocaleDateString('de-DE', { weekday: 'short'});
				var theDate = dayOfWeek + ', ' + niceDate;
				$('#theDate').val(theDate);  // set value of input field
				// config the datepicker
				$('.datepicker').datepicker({
					format: 'D, dd.mm.yyyy',
					language: 'de-DE',
					startDate: '01.01.2018',
					endDate: '0d',
					daysOfWeekHighlighted: '0',
					todayBtn: true,
					todayHighlight: true,
					autoclose: true
				})
				.on('changeDate', function(e) {
					// `e` here contains the extra attributes
					let dd = String(e.date.getDate()).padStart(2, '0');
					let mm = String(e.date.getMonth() + 1).padStart(2, '0'); //January is 0!
					let dateToParseStr = e.date.getFullYear() + '-' + mm + '-' + dd;
					window.location.href = "logging/daily.php?date=" + dateToParseStr;
				});

				$('#prevday').click(function(e) {
					// on click of prev day button
					if ( initialread == 1 ) {
						if ( parsedDate > earliestDate ) {
							parsedDate.setDate(parsedDate.getDate() - 1);  // subtract 1 day from currently selected date
							let dd = String(parsedDate.getDate()).padStart(2, '0');
							let mm = String(parsedDate.getMonth() + 1).padStart(2, '0'); //January is 0!
							let dateToParseStr = parsedDate.getFullYear() + '-' + mm + '-' + dd;
							window.location.href = "logging/daily.php?date=" + dateToParseStr;
						}
					}
				});

				$('#nextday').click(function(e) {
					// on click of next day button
					if ( initialread == 1 ) {
						let today = new Date();
						today.setHours(0,0,0,0);  // make sure time is all 0 for later comparisons
						if ( parsedDate < today ) {
							parsedDate.setDate(parsedDate.getDate() + 1);  // add 1 day from currently selected date
							let dd = String(parsedDate.getDate()).padStart(2, '0');
							let mm = String(parsedDate.getMonth() + 1).padStart(2, '0'); //January is 0!
							let dateToParseStr = parsedDate.getFullYear() + '-' + mm + '-' + dd;
							window.location.href = "logging/daily.php?date=" + dateToParseStr;
						}
					}
				});

				// load graph
				$.getScript("logging/dailychart.js?ver=20210209");
			})
		</script>

	</body>

</html>
