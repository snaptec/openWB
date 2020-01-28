<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>OpenWB</title>
		<meta name="description" content="Control your charge" />
		<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
		<meta name="author" content="Kevin Wieland, Michael Ortenstein" />
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
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
	</head>

	<body>

		<?php

			include '/var/www/html/openWB/web/settings/navbar.php';

			// read actual version # from releasetrains
			$stableVersion = file_get_contents('/var/www/html/openWB/ramdisk/vstable');
			$betaVersion = file_get_contents('/var/www/html/openWB/ramdisk/vbeta');
			$nightlyVersion = file_get_contents('/var/www/html/openWB/ramdisk/vnightly');
			$installedVersion = file_get_contents('/var/www/html/openWB/web/version');

			// read selected releasetrain from config file
			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach($lines as $line) {
				if(strpos($line, "releasetrain=") !== false) {
					list(, $releasetrain) = explode("=", $line);
				}
			}
			$releasetrain = trim($releasetrain);

			if ( $releasetrain == "" ) {
				// if no releasetrain set, set stable
				$releasetrain="stable";
			}


		?>

		<div role="main" class="container" style="margin-top:20px">
			<div class="row">
				<div class="col">
					<h1>Versionsübersicht</h1>
				</div>
			</div>
			<div class="row">
				<div class="col">
					<b>installierte Version: <?php echo $installedVersion ?><br></b>
					verfügbare Stable: <?php echo $stableVersion ?><br>
					verfügbare Beta: <?php echo $betaVersion ?><br>
					verfügbare Nightly: <?php echo $nightlyVersion ?><br>
				</div>
			</div>

			<div class="row">
				<div class="col">
					<h1>Versionserläuterung</h1>
				</div>
			</div>
			<div class="row">
				<div class="col">
						<b>Stable</b><br>
						Die Stable-Version ist die empfohlene. Sie wurde einschließlich aller Features ausgiebigen Tests unterzogen und als fehlerfrei bewertet.
					<br>
						<b>Beta</b><br>
						Die Beta-Version beinhaltet neue Features für zukünftige Stable-Versionen, befindet sich aber noch in der Testphase. Fehlverhalten ist nicht ausgeschlossen.
					<br>
						<b>Nightly</b><br>
						Die Nightly-Version beinhaltet Neuentwicklungen, die teils nur eingeschränkt getestet sind. Fehlverhalten ist wahrscheinlich.
				</div>
			</div>

			<div class="row">
				<div class="col">
					<h1>Versionsauswahl</h1>
				</div>
			</div>
			<form class="form" action="tools/savedoupdate.php" method="POST">
				<div class="row">
					<div class="col-3">
						<div class="form-check mb-2">
							<input class="form-check-input" type="radio" name="releasetrainCheckbox" id="stableCheckbox" value="stable" <?php if($releasetrain == "stable") echo checked?>>
							<label class="form-check-label" for="stableCheckbox">
							    Stable
							</label>
						</div>
						<div class="form-check mb-2">
							<input class="form-check-input" type="radio" name="releasetrainCheckbox" id="betaCheckbox" value="beta" <?php if($releasetrain == "beta") echo checked?>>
							<label class="form-check-label" for="betaCheckbox">
								Beta
							</label>
						</div>
						<div class="form-check">
							<input class="form-check-input" type="radio" name="releasetrainCheckbox" id="nightlyCheckbox" value="master" <?php if($releasetrain == "master") echo checked?>>
							<label class="form-check-label" for="nightlyCheckbox">
								Nightly
							</label>
						</div>
					</div>
					<div class="col-2 vaRow">
						<button type="submit" class="btn btn-lg btn-green">Update</button>
					</div>
				</div>
				<br>
			</form>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
		  <div class="container text-center">
			  <small>Sie befinden sich hier: System/Update</small>
		  </div>
		</footer>

	</body>
</html>
