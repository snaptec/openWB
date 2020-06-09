<!DOCTYPE html>
<html lang="de">

	<head>
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0">
		<title>Logging Jahresansicht</title>
		<meta name="author" content="Kevin Wieland, Michael Ortestein" />
		<link rel="apple-touch-icon" sizes="57x57" href="../img/favicons/apple-touch-icon-57x57.png">
		<link rel="apple-touch-icon" sizes="60x60" href="../img/favicons/apple-touch-icon-60x60.png">
		<link rel="icon" type="image/png" href="../img/favicons/favicon-32x32.png" sizes="32x32">
		<link rel="icon" type="image/png" href="../img/favicons/favicon-16x16.png" sizes="16x16">
		<link rel="manifest" href="../manifest.json">
		<link rel="shortcut icon" href="../img/favicons/favicon.ico">
		<meta name="msapplication-TileColor" content="#00a8ff">
		<meta name="msapplication-config" content="../img/favicons/browserconfig.xml">
		<meta name="theme-color" content="#ffffff">
		<meta http-equiv="refresh" content="600; URL=index.php">

		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="../css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="../css/normalize-8.0.1.css">
		<!-- Bootstrap-Datepicker -->
		<link rel="stylesheet" type="text/css" href="../css/bootstrap-datepicker/bootstrap-datepicker3.min.css">
		<!-- Font Awesome, all styles -->
		<link href="../fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="logging_style.css">

		<!-- important scripts to be loaded -->
		<script src="../js/jquery-3.4.1.min.js"></script>
		<script src="../js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
	</head>

	<body>

		<?php
			include $_SERVER['DOCUMENT_ROOT'].'/openWB/web/logging/navbar.php';
		?>

		<div role="main" class="container" style="margin-top:20px">
			<div class="row">
				<div class="col" style="text-align: center;">
					<h4>Logging Jahresansicht</h4>
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
						<br>Feature noch nicht vollständig implementiert...
					</div>
					<canvas id="canvas" style="height: 400px;"></canvas>
				</div>
			</div>
		</div>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Logging/Jahr</small>
			</div>
		</footer>

		<!-- load Chart.js library -->
		<script src="../js/Chart.bundle.js"></script>

		<!-- load Bootstrap-Datepicker library -->
		<script src="../js/bootstrap-datepicker/bootstrap-datepicker.min.js"></script>
		<script src="../js/bootstrap-datepicker/bootstrap-datepicker.de.min.js"></script>

		<!-- load mqtt library -->
		<script src = "../js/mqttws31.js" ></script>

		<!-- get parsed date, setup datepicker and load respective Chart.js definition -->
		<script>
			$(document).ready(function(){
				// GET expects date format Y like 2020
				// get parsed date and format nicely for input field
				const EARLIESTDATE = '01.01.2015';  // no earlier date choosable
				var url_string = window.location.href;
				var url = new URL(url_string);
				var parsedDateString = url.searchParams.get('date');
				var pattern = /^[0-9]{4}$/;
				var reloadNeeded = false;
				if ( parsedDateString == null || parsedDateString.match(pattern) == null ) {
					// nothing parsed or format not valid, so set date to today
					var parsedDate = new Date();
				} else {
					var earliestDate = new Date (EARLIESTDATE);
					var parsedDate = new Date(parsedDateString);
					if ( parsedDate < earliestDate ) {
						// date parsed was too early so set to today
						parsedDate = new Date();
						reloadNeeded = true;
					}
				}
				if ( reloadNeeded ) {
					// date parsed was too early so reload with today
					window.location.href = "yearly.php?date=" + parsedDate.getFullYear();
				}
				var theDate = parsedDate.getFullYear();
				$('#theDate').val(theDate);  // set value of input field
				// config the datepicker
				$('.datepicker').datepicker({
					format: 'MM yyyy',
					language: "de-DE",
					startDate: EARLIESTDATE,
					endDate: '0d',
					startView: 'years',
					minViewMode: 'years',
					todayBtn: true,
					todayHighlight: true,
					autoclose: true
				})
				.on('changeDate', function(e) {
					// `e` here contains the extra attributes
					var dateToParse = e.date.getFullYear();
					window.location.href = "yearly.php?date=" + dateToParse;
				});

				// load graph
				// TODO: implement yearlychart.js
				// $.getScript("yearlychart.js");
			})
		</script>

	</body>

</html>
