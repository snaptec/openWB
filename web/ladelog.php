<html lang="de">

<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB</title>
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
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="ladelog_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
</head>

<body>
                <?php
                        include $_SERVER['DOCUMENT_ROOT'].'/openWB/web/navbar.php';
                ?>
 		<div role="main" class="container" style="margin-top:20px">
                        <div class="row">
                                <div class="col" style="text-align: center;">
                                        <h4>Ladelog Monatsansicht</h4>
                                </div>
                        </div>
			<div class="row justify-content-center">
				<div class="col-8 col-sm-6 col-md-5 col-lg-4">
					<div class="input-group mb-3">
					<!--	<i class="far fa-caret-square-left fa-lg vaRow mr-4" title="vorheriger Monat" id="prevmonth"></i> -->
						<input class="form-control datepicker" id="theDate" type="text" readonly>
						<div class="input-group-append">
							<span class="input-group-text far fa-calendar-alt fa-lg vaRow"></span>
						</div>
					<!--	<i class="far fa-caret-square-right fa-lg vaRow ml-4" title="nächster Monat" id="nextmonth"></i> -->
					</div>
				</div>
			</div>
			<div class="row justify-content-center">
				<label class="checkbox-inline"><input type="checkbox" id="showlp1" value="" checked>Ladepunkt 1</label>
				<label class="checkbox-inline"><input type="checkbox" id="showlp2" value="" checked>Ladepunkt 2</label>
				<label class="checkbox-inline"><input type="checkbox" id="showlp3" value="" checked>Ladepunkt 3</label>
			</div>
			<div class="row justify-content-center">
				<label class="checkbox-inline"><input type="checkbox" id="showsofort" value="" checked>Sofort Laden</label>
				<label class="checkbox-inline"><input type="checkbox" id="showminpv" value="" checked>Min und PV</label>
				<label class="checkbox-inline"><input type="checkbox" id="shownurpv" value="" checked>Nur PV</label>
				<label class="checkbox-inline"><input type="checkbox" id="showstandby" value="" checked>Standby</label>
				<label class="checkbox-inline"><input type="checkbox" id="shownacht" value="" checked>Nachtladen</label>

			</div>
			<div class="row justify-content-center">
				<label class="checkbox-inline"><input type="checkbox" id="showrfid" value="">RFID</label><input type="text" id="rfidtag" value="">
			</div>
		<div id="ladelogtablediv"></div>
		</div>





<!--	</section> -->

	<div class="mobile-nav">
		<a href="#" class="close-link"><i class="arrow_up"></i></a>
	</div>
	<!-- Scripts -->
        <script src="js/bootstrap-datepicker/bootstrap-datepicker.min.js"></script>
        <script src="js/bootstrap-datepicker/bootstrap-datepicker.de.min.js"></script>
	<script src="js/mqttws31.js"></script>
	<script src="ladelog.js"></script>
	<script src="js/owl.carousel.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="js/wow.min.js"></script>
	<script src="js/typewriter.js"></script>
	<script src="js/jquery.onepagenav.js"></script>
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
					//window.location.href = "monthly.php?date=" + parsedDate.getFullYear() + '-' + mm;
					selectladelogclick(parsedDate.getFullYear()+mm);
				}
				var month = parsedDate.toLocaleDateString('de-DE', { month: 'long'});
				var theDate = month + ' ' + parsedDate.getFullYear();
				setTimeout(
					function() {
						selectladelogclick(parsedDate.getFullYear() + mm);
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
					var dateToParseStr = e.date.getFullYear() + '-' + mm;
					//window.location.href = "monthly.php?date=" + dateToParseStr;
					parsedDate = e.date;
					console.log(parsedDate);
					selectladelogclick(dateToParseStr);
				});


				$('#prevmonth').click(function(e) {
					// on click of prev month button
					let dateToParse = new Date(parsedDate.getTime());  // copy currently selected date
					dateToParse.setMonth(parsedDate.getMonth() - 1);  // and substract month
					if ( dateToParse >= earliestDate ) {
						let mm = String(dateToParse.getMonth() + 1).padStart(2, '0'); //January is 0!
						let dateToParseStr = dateToParse.getFullYear() + '-' + mm;
						var month = dateToParse.toLocaleDateString('de-DE', { month: 'long'});
						$('#theDate').val(month + ' ' + dateToParse.getFullYear());
						selectladelogclick(dateToParseStr);
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
						selectladelogclick(dateToParseStr);
					}
				});

			})
		</script>

</body>
		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Ladelog</small>
			</div>
		</footer>
</html>
