<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>openWB Stromtarif-Info</title>
		<meta name="author" content="Michael Ortenstein" />
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
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
		<!-- Bootstrap-Datepicker -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-datepicker/bootstrap-datepicker3.min.css">
		<!-- include stromtarif-style	-->
		<link rel="stylesheet" type="text/css" href="../modules/et_tibber/stromtarifinfo/stromtarifinfo_style.css?ver=20211108">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<script src="js/Chart.bundle.min.js"></script>

		<!-- load Bootstrap-Datepicker library -->
		<script src="js/bootstrap-datepicker/bootstrap-datepicker.min.js"></script>
		<script src="js/bootstrap-datepicker/bootstrap-datepicker.de.min.js"></script>

		<!-- special stromtarif scripts to be loaded -->
		<script src="../modules/et_tibber/tibber.js?ver=20211108"></script>
		<script src="../modules/et_tibber/stromtarifinfo/tibberElectricityPricechart.js?ver=20211108"></script>
		<script src="../modules/et_tibber/stromtarifinfo/tibberHourlyConsumptionchart.js?ver=20211108"></script>

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
				$('head').append('<link rel="stylesheet" href="themes/' + themeCookie + '/settings.css?v=20200801">');
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
		?>

		<div id="nav-placeholder"></div>
		<div role="main" class="container" style="margin-top:20px">
			<h1>Stromtarif-Info Tibber</h1>
			<div id="waitForData">
				<span>Tibber-Daten werden abgerufen, bitte warten... </span>
				<div class="spinner-border spinner-border-sm" role="status">
  					<span class="sr-only"></span>
				</div>
			</div>
			<div id="dataError" class="alert alert-danger hide" role="alert">
				Fehler bei der Abfrage der Tibber-API (<span id="dataErrorText"></span>).
			</div>

			<div id="validData" style="display: none;">

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Allgemein
					</div>
					<div class="card-body">
						<div class="row">
							<div class="col smallTextSize">
								<p>
									<b>Objekt:</b><br>
									<span id="name">--</span><br>
									<span id="street"></span><br>
									<span id="city"></span><br>
								</p>
							</div>
						</div>
					</div>
				</div>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Strompreisentwicklung
					</div>
					<div class="card-body">
						<div class="row">
							<div class="col smallTextSize">
								aktueller Preis: <span id="currentPrice">--</span><br>
								Börsenanteil: <span id="currentEnergyPrice">--</span><br>
								Steuern/Gebühren: <span id="currentTax">--</span><br>
								Preis gültig seit: <span id="currentValidSince">--</span>
							</div>
						</div>

						<div class="row justify-content-center my-2">
							<div class="col-sm-12 text-center smallTextSize">
								<div id="noPricechartDiv">
									Keine Daten für Preis-Chart verfügbar.
								</div>
								<div id="electricityPricechartCanvasDiv" class="col text-center" style="position: relative; height:250px;">
									<canvas id="electricityPricechartCanvas"></canvas>
								</div>
							</div>
						</div>

					</div>
				</div>


				<div id="cardTagesbezug" class="card border-secondary hide">
					<div class="card-header bg-secondary">
						Tagesbezug
					</div>
					<div class="card-body">
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
						<div class="row">
							<div class="col smallTextSize">
								Gesamtbezug:  <span id="totalConsumptionDay"></span><br>
								Gesamtkosten:  <span id="totalCostsDay"></span><br>
								&empty;-Strompreis: <span id="avgPriceDay"></span>
							</div>
						</div>
						<div class="row justify-content-center my-2">
							<div class="col-sm-12 text-center smallTextSize">
								<div id="noDailychartDiv" class="hide">
									Keine Daten für Tagesbezugs-Chart verfügbar.
								</div>
								<div id="dailyConsumptionchartCanvasDiv" class="col text-center" style="position: relative; height:250px;">
									<canvas id="consumptionchartCanvas"></canvas>
								</div>
							</div>
						</div>

					</div>
				</div>

			</div>

		</div>  <!-- container -->

		<script>
			var initialDataRead = true;
			// load navbar, be carefull: it loads asynchonously
			$.get(
				{ url: "themes/navbar.html", cache: false },
				function(data){
					$("#nav-placeholder").replaceWith(data);
					$('#navStromtarifInfo').removeClass('hide');
					$('#navStromtarifInfo .etproviderLink').addClass('disabled');
				}
			);

			function getDateAsBase64 (dateToProcess) {
				// returns date as base64-encoded formatted string
				// format of ISO string is like 2021-11-04T23:00:00.000+01:00
				var timeString = dateToProcess.toISOString().replace('Z', '');  // now formatted like 2021-11-04T23:00:00.000, offset missing
				// calculate tz offset and get formatted string
				var timezone_offset_min = dateToProcess.getTimezoneOffset(),
					offset_hrs = parseInt(Math.abs(timezone_offset_min/60)),
					offset_min = Math.abs(timezone_offset_min%60),
					timezone_standard;
				if (offset_hrs < 10)
					offset_hrs = '0' + offset_hrs;
				if (offset_min < 10)
					offset_min = '0' + offset_min;
				// Add an opposite sign to the offset
				// If offset is 0, it means timezone is UTC
				if (timezone_offset_min < 0)
					timezone_standard = '+' + offset_hrs + ':' + offset_min;
				else if(timezone_offset_min > 0)
					timezone_standard = '-' + offset_hrs + ':' + offset_min;
				else if(timezone_offset_min == 0)
					timezone_standard = 'Z';
				// Timezone difference now in hours and minutes, String such as +5:30 or -6:00 or Z
				timeString += timezone_standard;  // now formatted like 2021-11-04T23:00:00.000+01:00
				return btoa(timeString);
			}

			function requestData (theDate) {
				var tibberToken = "<?php echo $tibbertokenold; ?>";
				var tibberHomeID = "<?php echo $tibberhomeidold; ?>";
				var timeStringBase64 = getDateAsBase64(theDate);
				var tibberAPI = "https://api.tibber.com/v1-beta/gql";
				if (initialDataRead) {
					// reads complete Dataset including home-info and price chart
					initialDataRead = false;
					var tibberQueryHead = '{ "query": "{viewer {name home(id:\\"' + tibberHomeID + '\\") {';
					var tibberQueryGetAdress = 'address {address1 postalCode city} ';
					var tibberQueryGetPriceInfo = 'currentSubscription {priceInfo {current{total energy tax startsAt} today {total startsAt} tomorrow {total startsAt}}} ';
				} else {
					var tibberQueryHead = '{ "query": "{viewer {home(id:\\"' + tibberHomeID + '\\") {';
					var tibberQueryGetAdress = '';
					var tibberQueryGetPriceInfo = '';
				}
				var tibberQueryGetHourlyConsumption = 'cons_hourly: consumption(resolution: HOURLY, after:\\"' + timeStringBase64 + '\\", first: 25) {nodes {from to cost unitPrice unitPriceVAT consumption}}';
				var tibberQueryTail = '}}}" }';
				var tibberQuery = tibberQueryHead + tibberQueryGetAdress + tibberQueryGetPriceInfo + tibberQueryGetHourlyConsumption + tibberQueryTail;

				$("#dataError").hide();
				readTibberAPI(tibberToken, tibberQuery)
					.then((data) => {
						processTibberResponse(data, theDate)
					})
					.catch((error) => {
						$("#waitForData").hide();
						$("#dataErrorText").text(error);
						$("#dataError").show();
						$('#validData').hide();
					})
			}

			$(document).ready(function(){
				// config the datepicker
				$('#theDate').datepicker({
					format: 'D, dd.mm.yyyy',
					language: 'de-DE',
					startDate: '01.01.2019',
					endDate: '0d',
					daysOfWeekHighlighted: '0',
					todayBtn: true,
					todayHighlight: true,
					autoclose: true
				})
				.on('changeDate', function(e) {
					// `e` here contains the extra attributes
					requestData(e.date);
				});
				// set initial date to yesterday and end date to today, this triggers 'onchange'
				$('#theDate').datepicker('setEndDate', new Date(new Date().setHours(0, 0, 0, 0)));
				var theDate = new Date(new Date().setHours(0, 0, 0, 0));  // set to midnight
				theDate.setDate(theDate.getDate() - 1);  // yesterday
				$('#theDate').datepicker('setDate', theDate);

				$('#prevday').click(function(e) {
					// on click of prev day button
					let currentDateSelected = new Date($('#theDate').datepicker('getDate').setHours(0,0,0,0));
					let datepickerStartDate = new Date($('#theDate').datepicker('getStartDate').setHours(0,0,0,0));
					if ( currentDateSelected > datepickerStartDate ) {
						currentDateSelected.setDate(currentDateSelected.getDate() - 1);  // substract 1 day from currently selected date
						$('#theDate').datepicker('setDate', currentDateSelected);
					}
				});

				$('#nextday').click(function(e) {
					// on click of next day button
					let currentDateSelected = new Date($('#theDate').datepicker('getDate').setHours(0,0,0,0));
					let datepickerEndDate = new Date($('#theDate').datepicker('getEndDate').setHours(0,0,0,0));
					datepickerEndDate.setDate(datepickerEndDate.getDate() - 1);  // stop forwarding one day before
					if ( currentDateSelected < datepickerEndDate ) {
						currentDateSelected.setDate(currentDateSelected.getDate() + 1);  // add 1 day to currently selected date
						$('#theDate').datepicker('setDate', currentDateSelected);
					}
				});
			});

		</script>

	</body>
</html>
