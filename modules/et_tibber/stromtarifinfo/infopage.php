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
		<!-- include stromtarif-style	-->
		<link rel="stylesheet" type="text/css" href="../modules/et_tibber/stromtarifinfo/stromtarifinfo_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<script src="js/Chart.bundle.min.js"></script>

		<!-- special stromtarif scripts to be loaded -->
		<script src="../modules/et_tibber/tibber.js?ver=20210211"></script>
		<script src="../modules/et_tibber/stromtarifinfo/tibberElectricityPricechart.js?ver=20210104"></script>
		<script src="../modules/et_tibber/stromtarifinfo/tibberHourlyConsumptionchart.js?ver=20210104-b"></script>

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
								<b>letzter Datenabruf:</b><br>
								<span id="lastDataReceived"></span>
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
						Tagesbezug <span id="dateYesterday"></span>
					</div>
					<div class="card-body">
						<div class="row">
							<div class="col smallTextSize">
								Gesamtbezug:  <span id="totalConsumptionDay"></span><br>
								Gesamtkosten:  <span id="totalCostsDay"></span><br>
								&empty;-Strompreis: <span id="avgPriceDay"></span>
							</div>
						</div>
						<div class="row justify-content-center my-2">
							<div class="col-sm-12 text-center smallTextSize">
								<div id="dailyConsumptionchartCanvasDiv" class="col text-center" style="position: relative; height:250px;">
									<canvas id="consumptionchartCanvas"></canvas>
								</div>
							</div>
						</div>

					</div>
				</div>

				<div id="cardMonatsbezug" class="card border-secondary hide">
					<div class="card-header bg-secondary">
						Monatsbezug
					</div>
					<div class="card-body">
						<div class="row">
							<div class="col smallTextSize">
								Derzeit noch nicht implementiert.
							</div>
						</div>
					</div>
				</div>

				<div id="cardJahresbezug" class="card border-secondary hide">
					<div class="card-header bg-secondary">
						Jahresbezug
					</div>
					<div class="card-body">
						<div class="row">
							<div class="col">
								Derzeit noch nicht implementiert.
							</div>
						</div>
					</div>
				</div>

			</div>


		</div>  <!-- container -->

		<script>

			// load navbar, be carefull: it loads asynchonously
			$.get(
				{ url: "themes/navbar.html", cache: false },
				function(data){
					$("#nav-placeholder").replaceWith(data);
					$('#navStromtarifInfo').removeClass('hide');
					$('#navStromtarifInfo .etproviderLink').addClass('disabled');
				}
			);

			$(document).ready(function(){

				// calculate amount of datasets to be received since Tibber only sends valid data for
				// past hours/days/months
				var now = new Date();
				const hoursToReceive = now.getHours() + 24; // Tibber sends hourly data for past hours
				const daysToReceive = now.getDate() + 1;  // Tibber sends daily data for past days
				var monthsToReceive = now.getMonth();  // no index correction since Tibber sends monthly data for past months
				var tibberToken = "<?php echo $tibbertokenold; ?>";
				var tibberHomeID = "<?php echo $tibberhomeidold; ?>";
				const tibberAPI = "https://api.tibber.com/v1-beta/gql";
				const tibberQueryHead = '{ "query": "{viewer {name home(id:\\"' + tibberHomeID + '\\") {';
				const tibberQueryGetAdress = 'address {address1 postalCode city}';
				const tibberQueryGetPriceInfo = 'currentSubscription {priceInfo {current{total energy tax startsAt} today {total startsAt} tomorrow {total startsAt}}}';
				const tibberQueryGetHourlyConsumption = 'cons_hourly: consumption(resolution: HOURLY, last:' + hoursToReceive + ') {nodes {from to cost unitPrice unitPriceVAT consumption}}';
				const tibberQueryTail = '}}}"}';
				var tibberQuery = tibberQueryHead + tibberQueryGetAdress + tibberQueryGetPriceInfo + tibberQueryGetHourlyConsumption + tibberQueryTail;

				readTibberAPI(tibberToken, tibberQuery)
					.then((data) => {
	    				processTibberResponse(data)
					})
					.catch((error) => {
						$("#waitForData").hide();
						$("#dataErrorText").text(error);
						$("#dataError").show();
	  				})
			});

		</script>

	</body>
</html>
