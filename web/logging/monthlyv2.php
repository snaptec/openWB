<?php header( 'Refresh:600;' ); ?>
<!doctype html>
<html lang="de">

	<head>
		<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0">
		<title>Logging Monatsansicht Aufteilung (nightly)</title>
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
					<h4>Logging Monatsansicht Aufteilung (nightly)</h4>
				</div>
			</div>
			<div class="row justify-content-center">
				<div class="col-8 col-sm-6 col-md-5 col-lg-4">
					<div class="input-group mb-3">
						<i class="far fa-caret-square-left fa-lg vaRow mr-4" title="vorheriger Monat" id="prevmonth"></i>
						<input class="form-control datepicker" id="theDate" type="text" readonly>
						<div class="input-group-append">
							<span class="input-group-text far fa-calendar-alt fa-lg vaRow"></span>
						</div>
						<i class="far fa-caret-square-right fa-lg vaRow ml-4" title="nächster Monat" id="nextmonth"></i>
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
			  <small>Sie befinden sich hier: Logging/Monat</small>
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
				// GET expects date format Y-m like 2020-10
				// get parsed date and format nicely for input field
				var earliestDate = new Date('2018/01/01 00:00:00');
				var url_string = window.location.href;
				var url = new URL(url_string);
				var parsedDateString = url.searchParams.get('date');
				var pattern = /^[0-9]{4}\-(0[1-9]|1[012])$/;
				var reloadNeeded = false;
				if ( parsedDateString == null || parsedDateString.match(pattern) == null ) {
					// nothing parsed or format not valid, so set date to today
					var parsedDate = new Date();
					parsedDate.setHours(0,0,0,0);  // make sure time is all 0 for later comparisons
					parsedDate.setDate(1);  // // make sure day is 1 for later comparisons
				} else {
					var parsedDate = new Date(parsedDateString);
					parsedDate.setHours(0,0,0,0);  // make sure time is all 0 for later comparisons
					parsedDate.setDate(1);  // // make sure day is 1 for later comparisons
					if ( parsedDate < earliestDate ) {
						// date parsed was too early so set to today
						parsedDate = new Date();
						reloadNeeded = true;
					}
				}
				var mm = String(parsedDate.getMonth() + 1).padStart(2, '0'); // January is 0!, string with leading zeros
				if ( reloadNeeded ) {
					// date parsed was too early so reload with today
					window.location.href = "logging/monthlyv2.php?date=" + parsedDate.getFullYear() + '-' + mm;
				}
				var month = parsedDate.toLocaleDateString('de-DE', { month: 'long'});
				var theDate = month + ' ' + parsedDate.getFullYear();
				$('#theDate').val(theDate);  // set value of input field
				// config the datepicker
				$('.datepicker').datepicker({
					format: 'MM yyyy',
					language: 'de-DE',
					startDate: '01.2018',
					endDate: '0d',
					startView: 'months',
    				minViewMode: 'months',
					todayBtn: true,
					todayHighlight: true,
					autoclose: true
				})
				.on('changeDate', function(e) {
					// `e` here contains the extra attributes
					var mm = String(e.date.getMonth() + 1).padStart(2, '0'); //January is 0!, string with leading zeros
					var dateToParseStr = e.date.getFullYear() + '-' + mm;
					window.location.href = "logging/monthlyv2.php?date=" + dateToParseStr;
				});

				$('#prevmonth').click(function(e) {
					// on click of prev month button
					let dateToParse = new Date(parsedDate.getTime());  // copy currently selected date
					dateToParse.setMonth(parsedDate.getMonth() - 1);  // and substract month
					if ( dateToParse >= earliestDate ) {
						let mm = String(dateToParse.getMonth() + 1).padStart(2, '0'); //January is 0!
						let dateToParseStr = dateToParse.getFullYear() + '-' + mm;
						window.location.href = "logging/monthlyv2.php?date=" + dateToParseStr;
					}
				});

				$('#nextmonth').click(function(e) {
					// on click of next month button
					let dateToParse = new Date(parsedDate.getTime());  // copy currently selected date
					dateToParse.setMonth(parsedDate.getMonth() + 1);  // and add month
					let today = new Date();
					today.setHours(0,0,0,0);  // make sure time is all 0 for later comparisons
					if ( dateToParse <= today ) {
						let mm = String(dateToParse.getMonth() + 1).padStart(2, '0'); //January is 0!
						let dateToParseStr = dateToParse.getFullYear() + '-' + mm;
						window.location.href = "logging/monthlyv2.php?date=" + dateToParseStr;
					}
				});

				// load graph
				$.getScript("logging/monthlychartv1.js?ver=20210209");
			})
		</script>

	</body>

</html>
