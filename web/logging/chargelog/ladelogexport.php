<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>OpenWB Ladelog</title>
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
		<script>
			function getCookie(cname) {
				var name = cname + '=';
				var decodedCookie = decodeURIComponent(document.cookie);
				var ca = decodedCookie.split(';');
				for (var i = 0; i < ca.length; i++) {
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
			if ('' != themeCookie) {
				$('head').append('<link rel="stylesheet" href="themes/' + themeCookie + '/settings.css?v=20210209">');
			}
		</script>
	</head>

	<body>
		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container">

			<h1>Lade-Log Export</h1>

			<div class="card border-secondary">
				<div class="card-header bg-secondary">
					Aufgezeichnete Logdateien
				</div>
				<div class="card-body">
					<?php
						$files = glob($_SERVER['DOCUMENT_ROOT'] . "/openWB/web/logging/data/ladelog/*.csv");
						$rowClasses = "";
						foreach ($files as $current) {
					?>
						<div class="row<?php echo $rowClasses; ?>">
							<label class="col-6 col-form-label">
								<?php
									preg_match('/\/var\/www\/html\/openWB\/web\/logging\/data\/ladelog\/([0-9]{4})([0-9]{2})\.csv/', $current, $m);
									$year = $m[1];
									$month = $m[2];
									setlocale(LC_TIME, "de_DE.UTF-8");
									$month_name = strftime('%B', mktime(0, 0, 0, $month, 1, $year));
									echo $month_name, " ", $year;
								?>
							</label>
							<div class="col-6 text-right">
								<a class="btn downloadBtn btn-info" style="margin-bottom:12px" href=<?php echo preg_split('/\/var\/www\/html\/openWB\/web\//', $current)[1]; ?> download><i class="fas fa-download"></i> Download</a>
							</div>
						</div>
					<?php
						$rowClasses = " border-top pt-2";
						}
					?>
				</div>
			</div>
		</div>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: <a href="logging/chargelog/ladelog.php">Lade-Log</a> - Lade-Log Export</small>
			</div>
		</footer>

		<script>
			$.get({
					url: "themes/navbar.html",
					cache: false
				},
				function(data) {
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navLadelog').addClass('disabled');
				}
			);
		</script>
	</body>

</html>
