<?php
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);

	$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
	foreach($lines as $line) {
		list($key, $value) = explode("=", $line, 2);
		${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
	}

	$backupPath = "/var/www/html/openWB/web/backup/";
	$globalError = false;
	$globalErrorMessage = "";
	$globalErrorCode = 0;

	$useExtendedFilename = false;
	if( isset($_GET["extendedFilename"]) && $_GET["extendedFilename"] == "1") {
		$useExtendedFilename = true;
	}
	$filename = "";

	if ($backuptargetold == "ftp") {
		echo "<!-- Perform FTP backup...-->";
		$filename = buildBackup($useExtendedFilename, $backupPath);
		echo "<!-- File created here: ".$backupPath." // ".$filename."-->";
		echo "<!-- Uplaoding via FTP: ".$backupPath.$filename."-->";
		$globalErrorCode = ftpUpload($filename, $backupPath, $ftphostold, $ftppathold, $ftpuserold, $ftppassold);
	} else {
		echo "<!-- Building local backup... -->";
		$filename = buildBackup($useExtendedFilename, $backupPath);
		echo "<!-- File created here: ".$backupPath." // ".$filename."-->";
	}


	function ftpUpload($filename, $backupPath, $host, $path, $user, $pass) {
		$localfile = $backupPath.$filename;
		$remotefile = $filename;
		echo "Local file ".$localfile;
		echo "Upload ".$remotefile;

		$ch = curl_init();
		$fp = fopen($localfile, 'r');
		curl_setopt($ch, CURLOPT_URL, "ftp://".$user.":".$pass."@".$host.":".$path."/".$filename);
		curl_setopt($ch, CURLOPT_UPLOAD, 1);
		curl_setopt($ch, CURLOPT_INFILE, $fp);
		curl_setopt($ch, CURLOPT_INFILESIZE, filesize($localfile));
		curl_exec ($ch);
		$error_no = curl_errno($ch);
		curl_close ($ch);
		if ($error_no > 0) {
			$globalErrorMessage = "File uploaed failed.";
		}
		return $error_no;
	}

	function buildBackup($useExtendedFilename, $backupPath) {
		// if parameter extendedFilename is passed with value 1 the filename changes
		// from backup.tar.gz to openWB_backup_YYYY-MM-DD_HH-MM-SS.tar.gz
		
		echo "<!-- Putting backup into ".$backupPath."-->";
		$timestamp = date("Y-m-d") . "_" . date("H-i-s");
		if ( $useExtendedFilename ) {
			$filename = "openWB_backup_" . $timestamp . ".tar.gz" ;
		} else {
			$filename = "backup.tar.gz" ;
		}

		// first empty backup-directory
		echo "<!-- Unlinking ".$backupPath."* -->";
		array_map( "unlink", array_filter((array) glob($backupPath . "*") ) );
		// then create new backup-file
		exec("tar --exclude='/var/www/html/openWB/web/backup' --exclude='/var/www/html/openWB/.git' -czf ". $backupPath . $filename . " /var/www/html/");

		return $filename;
	}
	
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

			<?php 
						if (isset($globalErrorCode) && $globalErrorCode > 0) {
							echo '<div class="alert alert-primary" role="alert">';
							echo '<strong>Das Backup ist fehlgeschlagen:</strong><br />';
							echo $globalErrorMessage.'<br />';
							echo 'Curl Error Code: '.$globalErrorCode;
						  	echo '</div>';
						} else {
					?>
					<div class="alert alert-success">
						Backup-Datei <?php echo $filename; ?> erfolgreich
						<?php if ($backuptargetold == "ftp")  { ?>					
							auf <?php echo "ftp://".$ftphostold.$ftppathold."/".$filename ?>
						<?php } ?> erstellt.
					</div>

					<div class="row">
							
							<div class="col text-center">
								<a class="btn btn-success" href="/openWB/web/backup/<?php echo $filename; ?>" target="_blank"><i class="fas fa-download"></i> Backup herunterladen</a>
							</div>
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
				}
			);

		</script>

	</body>
</html>
