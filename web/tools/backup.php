<?php
	// if paranmeter extendedFilename is passed with value 1 the filename changes
	// from backup.tar.gz to openWB_backup_YYYY-MM-DD_HH-MM-SS.tar.gz
	$useExtendedFilename = false;
	if( isset($_GET["extendedFilename"]) && $_GET["extendedFilename"] == "1") {
		$useExtendedFilename = true;
	}
	$backupPath = "/var/www/html/openWB/web/backup/";
	$timestamp = date("Y-m-d") . "_" . date("H-i-s");
	if ( $useExtendedFilename ) {
		$filename = "openWB_backup_" . $timestamp . ".tar.gz" ;
	} else {
		$filename = "backup.tar.gz" ;
	}

	// first empty backup-directory
	array_map( "unlink", array_filter((array) glob($backupPath . "*") ) );
	// then create new backup-file
	exec("tar --exclude='/var/www/html/openWB/web/backup' --exclude='/var/www/html/openWB/.git' -czf ". $backupPath . $filename . " /var/www/html/");
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
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
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
		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">

			<h1>Backup erstellen</h1>
			<div class="alert alert-success">
				Backup-Datei <?php echo $filename; ?> erfoglreich erstellt.
			</div>

			<div class="row">
				<div class="col text-center">
					<a class="btn btn-success" href="/openWB/web/backup/<?php echo $filename; ?>" target="_blank"><i class="fas fa-download"></i> Backup herunterladen</a>
				</div>
			</div>

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
