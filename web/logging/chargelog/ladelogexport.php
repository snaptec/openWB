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
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
	</head>

	<body>
		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container">

			<h1>Ladelog Export</h1>

			<?php
				$files = glob($_SERVER['DOCUMENT_ROOT'] . "/openWB/web/logging/data/ladelog/*.csv");
				echo '<ul>'.implode('', array_map('sprintf', array_fill(0, count($files), '<li><a href="%s">%s</a></li>'), $files, $files)).'</ul>';
			?>
		</div>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Ladelog Export</small>
			</div>
		</footer>

		<script>
			$.get(
				{ url: "themes/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navLadelog').addClass('disabled');
				}
			);
		</script>
	</body>
</html>
