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
		<link rel="stylesheet" type="text/css" href="logging/logging_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<script src="js/Chart.bundle.min.js"></script>
	</head>

	<body>

		<div id="nav-placeholder"></div>
		<div role="main" class="container" style="margin-top:20px">
			<h1>Debug-Logfile</h1>
			<?php
				$filepath = $_SERVER['DOCUMENT_ROOT'] . '/openWB/ramdisk/openWB.log';
				$linesToRead = 30;

				// returns last n lines from logfile
				function getLastDebugLines() {
					global $filepath, $linesToRead;
					$log = `tail -n $linesToRead $filepath`;
					return trim($log);
				}

				// returns total number of lines in logfile
				function getDebugLinesCount() {
					global $filepath;
					$file = new \SplFileObject($filepath, 'r');
					$file->seek(PHP_INT_MAX);
					return $file->key();
				}

				$debugLinesCount = getDebugLinesCount();
				$textAreaLabelText = 'Letzte 30 Log-Einträge:';
				if ( $debugLinesCount <= $linesToRead ) {
					$textAreaLabelText = 'Log-Einträge:';
				}
			?>
			<div class="row">
				<div class="col">
					Stand: <span id="timestampSpan"></span> <br>
					Insgesamt <?php echo $debugLinesCount; ?> Einträge im Debug-Log<br>
					<div class="form-group textarea">
						<label for="debugLinesArea"><?php echo $textAreaLabelText; ?></label>
						<textarea readonly class="form-control" id="debugLinesArea" rows="10" cols="1"><?php echo getLastDebugLines();?>
						</textarea>
					</div>
				</div>
			</div>
			<div class="row row justify-content-center">
				<button type="button" class="btn btn-success" id="refreshBtn">Abfrage erneuern</button>
			</div>
		</div>  <!-- container -->

		<script>

			// load navbar
			$("#nav-placeholder").load('themes/navbar.html?v=20210130', function() {
				$('#navDebuglog').addClass('disabled');
			});

			$(document).ready(function(){

				const options = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', timeZoneName: 'short' };
				var now = new Date();
		        $('#timestampSpan').text(now.toLocaleDateString(undefined, options));

				$('#refreshBtn').click(function(){
					location.reload();
				});

			});

		</script>

	</body>
</html>
