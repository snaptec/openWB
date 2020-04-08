<!doctype html>
<html lang="de">

	<head>
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0">
		<title>Logging Langzeitansicht</title>
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
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="logging_style.css?ver=200407-a">

		<!-- important scripts to be loaded -->
		<script src="../js/jquery-3.4.1.min.js"></script>
		<script src="../js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
	</head>

	<body>
		<?php
			include $_SERVER['DOCUMENT_ROOT'].'/openWB/web/logging/navbar.php';

			$result = '';
			$lines = file($_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf');
			foreach($lines as $line) {
				if(strpos($line, "graphinteractiveam=") !== false) {
					list(, $graphinteractiveamold) = explode("=", $line);
				}

				if(strpos($line, "verbraucher1_name=") !== false) {
					list(, $verbraucher1_nameold) = explode("=", $line);
				}
				if(strpos($line, "verbraucher2_name=") !== false) {
					list(, $verbraucher2_nameold) = explode("=", $line);
				}
				if(strpos($line, "grapham=") !== false) {
					list(, $graphamold) = explode("=", $line);
				}
				if(strpos($line, "lastmanagement=") !== false) {
					list(, $lastmanagementold) = explode("=", $line);
				}
				if(strpos($line, "simplemode=") !== false) {
					list(, $simplemodeold) = explode("=", $line);
				}

			}
			$speichervorhanden = file_get_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/speichervorhanden');
			$soc1vorhanden = file_get_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/soc1vorhanden');
			$verbraucher1vorhanden = file_get_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/verbraucher1vorhanden');
			$verbraucher2vorhanden = file_get_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/verbraucher2vorhanden');
			$verbraucher1_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher1_nameold));
			$verbraucher2_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher2_nameold));
		?>
		<div role="main" class="container" style="margin-top:20px">
			<div class="row">
				<div class="col text-center">
					<h4>Logging Langzeitansicht</h4>
				</div>
			</div>
			<div class="row">
				<div class="col" style="text-align: center;">
					<span id="displayedTimePeriodSpan"></span>
				</div>
			</div>
			<div class="row" id="thegraph">
				<div class="col">
					<div id="waitforgraphloadingdiv" style="text-align: center;">
						<br>Graph lädt, bitte warten...<br>
						<div class="spinner-grow text-muted mt-3"></div>
					</div>
					<div id="canvasdiv">
						<canvas id="canvas" style="height: 500px;"></canvas>
					</div>
				</div>
			</div>
		</div>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Logging/Langzeit</small>
			</div>
		</footer>

		<script>
			var lastmanagement = <?php echo $lastmanagementold ?>;
			var soc1vorhanden = <?php echo $soc1vorhanden ?>;
			var verbraucher1vorhanden = <?php echo $verbraucher1vorhanden ?>;
			var verbraucher2vorhanden = <?php echo $verbraucher2vorhanden ?>;
			var speichervorhanden = <?php echo $speichervorhanden ?>;
			var verbraucher1name = "<?php echo $verbraucher1_nameold ?>";
			var verbraucher2name = "<?php echo $verbraucher2_nameold ?>";
		</script>

		<!-- load Chart.js library -->

		<script src="../js/Chart.bundle.js"></script>
		<script src="../js/hammerjs@2.0.8"></script>
		<script src="../js/chartjs-plugin-zoom@0.7.4"></script>

		<!-- load mqtt library -->
		<script src = "../js/mqttws31.js" ></script>

		<!-- load respective Chart.js definition -->
		<script src="longlivechart.js?ver=200407-a"></script>

	</body>
</html>
