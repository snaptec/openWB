<?php
	// if parameter extendedFilename is passed with value 1 the filename changes
	// from backup.tar.gz to openWB_backup_YYYY-MM-DD_HH-MM-SS.tar.gz
	$useExtendedFilename = 0;
	if( isset($_GET["extendedFilename"]) && $_GET["extendedFilename"] == "1") {
		$useExtendedFilename = 1;
	}
	// execute backup script
	$filename = exec("sudo -u pi " . $_SERVER['DOCUMENT_ROOT'] . "/openWB/runs/backup.sh " . $useExtendedFilename, $output, $result);
?>
<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Backup erstellen</title>
		<meta name="description" content="Control your charge" />
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
		<link rel="stylesheet" type="text/css" href="fonts/font-awesome-5.8.2/css/all.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
	</head>

	<body>
		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">

			<h1>Backup erstellen</h1>
			<?php if ($filename !== false && $result == 0) { ?>
				<div class="alert alert-success">
					Backup-Datei <?php echo $filename; ?> erfolgreich erstellt.
				</div>

				<div class="row">
					<div class="col text-center">
						<a class="btn btn-success" href="/openWB/web/backup/<?php echo $filename; ?>" target="_blank"><i class="fas fa-download"></i> Backup herunterladen</a>
					</div>
				</div>
			<?php } else { ?>
				<div class="alert alert-danger">
					Es gab einen Fehler beim Erstellen der Backup-Datei. Bitte die Logmeldungen prüfen!
				</div>
			<?php } ?>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Backup erstellen</small>
			</div>
		</footer>

		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navBackup').addClass('disabled');
				}
			);

		</script>

	</body>
</html>
