<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>OpenWB Ladeprotokoll</title>
		<meta name="description" content="Control your charge" />
		<meta name="author" content="Kevin Wieland" />
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
		<!-- Bootstrap-Datepicker -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-datepicker/bootstrap-datepicker3.min.css">
		<!-- Bootstrap-Toggle -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap4-toggle/bootstrap4-toggle.min.css">
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="logging/chargelog/ladelog_style.css?ver=20210202">
		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<script src="js/bootstrap-datepicker/bootstrap-datepicker.min.js"></script>
		<script src="js/bootstrap-datepicker/bootstrap-datepicker.de.min.js"></script>
		<script src="js/bootstrap4-toggle/bootstrap4-toggle.min.js"></script>
		<script src="js/mqttws31.js"></script>
		<script src="logging/chargelog/helperFunctions.js?ver=20210202"></script>
		<script src="logging/chargelog/ladelog.js?ver=20220721"></script>
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

		<div id="nav"></div> <!-- placeholder for navbar -->

 		<div role="main" class="container">

			<h1>Ladeprotokoll Monatsansicht</h1>

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

			<div class="card border-secondary">
				<div class="card-header bg-secondary collapsed" data-toggle="collapse" data-target="#collapseFilter">
					<i class="fas fa-filter"></i> Filter
				</div>
				<div id="collapseFilter" class="card-body collapse">
					<div class="wrapper">
						<?php for( $index = 1; $index <= 8; $index++ ){ ?>
						<div class="row vaRow" id="chargep<?php echo $index; ?>">
							<div class="col">
								<label for="showlp<?php echo $index; ?>">Ladepunkt <?php echo $index; ?><span class="chargepName"></span></label>
							</div>
							<div class="col">
								<input type="checkbox" class="filterSetting" data-toggle="toggle" data-on="Ja" data-off="Nein" data-onstyle="success" data-offstyle="danger" data-style="w-100" id="showlp<?php echo $index; ?>" value="" checked>
							</div>
						</div>
						<?php } ?>
					</div>
					<hr>
					<div class="wrapper">
						<div class="row vaRow">
							<div class="col">
								<label for="showsofort">Sofort Laden</label>
							</div>
							<div class="col">
								<input type="checkbox" class="filterSetting" data-toggle="toggle" data-on="Ja" data-off="Nein" data-onstyle="success" data-offstyle="danger" data-style="w-100" id="showsofort" value="" checked>
							</div>
						</div>
						<div class="row vaRow">
							<div class="col">
								<label for="showminpv">Min und PV</label>
							</div>
							<div class="col">
								<input type="checkbox" class="filterSetting" data-toggle="toggle" data-on="Ja" data-off="Nein" data-onstyle="success" data-offstyle="danger" data-style="w-100" id="showminpv" value="" checked>
							</div>
						</div>
						<div class="row vaRow">
							<div class="col">
								<label for="shownurpv">Nur PV</label>
							</div>
							<div class="col">
								<input type="checkbox" class="filterSetting" data-toggle="toggle" data-on="Ja" data-off="Nein" data-onstyle="success" data-offstyle="danger" data-style="w-100" id="shownurpv" value="" checked>
							</div>
						</div>
						<div class="row vaRow">
							<div class="col">
								<label for="showstandby">Standby</label>
							</div>
							<div class="col">
								<input type="checkbox" class="filterSetting" data-toggle="toggle" data-on="Ja" data-off="Nein" data-onstyle="success" data-offstyle="danger" data-style="w-100" id="showstandby" value="" checked>
							</div>
						</div>
						<div class="row vaRow">
							<div class="col">
								<label for="shownacht">Nachtladen</label>
							</div>
							<div class="col">
								<input type="checkbox" class="filterSetting" data-toggle="toggle" data-on="Ja" data-off="Nein" data-onstyle="success" data-offstyle="danger" data-style="w-100" id="shownacht" value="" checked>
							</div>
						</div>
					</div>
					<div id="rfidFilter">
						<hr>
						<div class="row vaRow">
							<div class="col">
								<label for="showrfid">RFID</label>
							</div>
							<div class="col mb-2">
								<input type="checkbox" class="filterSetting" data-toggle="toggle" data-on="Ja" data-off="Nein" data-onstyle="success" data-offstyle="danger" data-style="w-100" id="showrfid" value="">
							</div>
							<div class="col-md-6 mb-2">
								<div class="input-group">
									<div class="input-group-prepend">
										<div class="input-group-text">
											<i class="fas fa-tag"></i>
										</div>
									</div> 
									<input class="form-control filterSetting" type="text" id="rfidtag" disabled value="">
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="card border-secondary">
				<div class="card-header bg-secondary">
					<i class="fas fa-clipboard-list"></i> Ladeprotokoll
					<i class="loading fas fa-cog fa-spin"></i>
				</div>
				<div id="ladelogtablediv" class="card-body text-monospace">
				</div>
			</div>

		</div><!-- main container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Lade-Log - <a href="logging/chargelog/ladelogexport.php">Ladeprotokoll Export</a></small>
			</div>
		</footer>

		<!-- get parsed date, setup datepicker and load lade log -->
		<script>
			var parsedDate;
			var dateToParseStr;
			var earliestDate = new Date('2018/01/01 00:00:00');

			$(document).ready(function(){
				// GET expects date format Y-m like 2020-10
				// get parsed date and format nicely for input field
				var url_string = window.location.href;
				var url = new URL(url_string);
				parsedDateString = url.searchParams.get('date');
				var pattern = /^[0-9]{4}\-(0[1-9]|1[012])$/;
				var reloadNeeded = false;
				if ( parsedDateString == null || parsedDateString.match(pattern) == null ) {
					// nothing parsed or format not valid, so set date to today
					parsedDate = new Date();
					parsedDate.setHours(0,0,0,0);  // make sure time is all 0 for later comparisons
					parsedDate.setDate(1);  // // make sure day is 1 for later comparisons
				} else {
					parsedDate = new Date(parsedDateString);
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
					selectChargeLogClick(parsedDate.getFullYear()+mm);
				}
				var month = parsedDate.toLocaleDateString('de-DE', { month: 'long'});
				dateToParseStr = parsedDate.getFullYear() + '-' + mm;
				var theDate = month + ' ' + parsedDate.getFullYear();
				setTimeout(
					function() {
						selectChargeLogClick(dateToParseStr);
					}, 1000);
				
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
					dateToParseStr = e.date.getFullYear() + '-' + mm;
					//window.location.href = "monthly.php?date=" + dateToParseStr;
					parsedDate = e.date;
					selectChargeLogClick(dateToParseStr);
				});

			});

			$.get(
				{ url: "themes/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navLadelog').addClass('disabled');
				}
			);

			$('#showrfid').change(function() {
				$('#rfidtag').prop('disabled', !this.checked);
			});

			$('.filterSetting').change(function() {
				// refresh charge log
				selectChargeLogClick(dateToParseStr);
			});

			$('#prevmonth').click(function(e) {
				// on click of prev month button
				let dateToParse = new Date(parsedDate.getTime());  // copy currently selected date
				dateToParse.setMonth(parsedDate.getMonth() - 1);  // and subtract month
				if ( dateToParse >= earliestDate ) {
					let mm = String(dateToParse.getMonth() + 1).padStart(2, '0'); //January is 0!
					dateToParseStr = dateToParse.getFullYear() + '-' + mm;
					var month = dateToParse.toLocaleDateString('de-DE', { month: 'long'});
					parsedDate = dateToParse;
					$('#theDate').val(month + ' ' + dateToParse.getFullYear());
					selectChargeLogClick(dateToParseStr);
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
					dateToParseStr = dateToParse.getFullYear() + '-' + mm;
					var month = dateToParse.toLocaleDateString('de-DE', { month: 'long'});
					parsedDate = dateToParse;
					$('#theDate').val(month + ' ' + dateToParse.getFullYear());
					selectChargeLogClick(dateToParseStr);
				}
			});

		</script>

	</body>
</html>
