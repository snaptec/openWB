<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>openWB Einstellungen</title>
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
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=202103291" ></script>
	</head>

	<body>
		<?php
			$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
			foreach($lines as $line) {
				list($key, $value) = explode("=", $line, 2);
				${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
			}
		?>
		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>OpenWB Backup</h1>
			<div class="card border-secondary">
				<form class="form" id="backupform" action="./settings/saveconfig.php" method="POST">
					<div class="card-header bg-secondary">
						Backup-Ziel
						
					</div>
					<div class="card-body">
						<div class="form-group mb-1">
							<div class="form-row mb-1">
								<label for="backuptarget" class="col-md-4 col-form-label">Backup-Ziel</label>
								<div class="col">
									<select name="backuptarget" id="backuptarget" class="form-control">
												<option value="local" <?php if ($backuptargetold == "local") echo "selected" ?>>/var/www/html/openWB/backup</option>
												<option value="ftp"  <?php if ($backuptargetold == "ftp") echo "selected" ?>>FTP</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="nightlybackup" class="col-md-4 col-form-label">Nächtliches Backup</label>
								<div class="col">
									<input type="hidden" value="0" name="nightlybackup" />
									<input id="nightlybackupchk" name="nightlybackup" class="" type="checkbox" value="1" <?php if ($nightlybackupold == 1) echo "checked=\"checked\"" ?> />
								</div>
							</div>
							<div class="form-row mb-1" id="shortfilename">
								<label for="nightlybackup" class="col-md-4 col-form-label">Kurzer Dateiname</label>
								<div class="col">
									<input type="hidden" value="0" name="shortbackupfilename" />
									<input id="shortbackupfilenamechk" name="shortbackupfilename" class="" type="checkbox" value="1" <?php if ($shortbackupfilenameold == 1)  echo "checked=\"checked\"" ?> />
									<span class="form-text small">Wenn aktiviert, wird die Datei unter den Namen backup.tar.gz am Zielort abgelegt. Wenn nicht aktiviert, wird die Datei unter dem Muster "openWB_backup_$jahr-$monat-$tag-$hourofday-$minute.tar.gz" abgelegt (Beispiel: openWB_backup_2023-11-30_17-19-11.tar.gz)</span>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body" id="ftpcreds">
					<div class="form-group">
							<div class="form-row mb-1">
								<label for="ftphost" class="col-md-4 col-form-label">FTP Host</label>
								<div class="col">
									<input id="ftphost" class="form-control" type="text" name="ftphost" value="<?= $ftphostold ?>">
									<span class="form-text small">Der FTP-Host als voller DNS-Name oder IP-Adresse</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ftppath" class="col-md-4 col-form-label">Remote Pfad auf FTP-Server</label>
								<div class="col">
								
									<input id="ftppath" name="ftppath" value="<?= $ftppathold ?>" class="form-control" type="text" />
									<span class="form-text small">Der Pfad auf dem Zielsystem, zB /Backups/openwb</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="ftpuser" class="col-md-4 col-form-label">FTP Username</label>
								<div class="col">
									<input id="ftpuser" name="ftpuser" value="<?= $ftpuserold ?>" class="form-control" />
									<span class="form-text small">Der Nutzername für das FTP-System</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ftppass" class="col-md-4 col-form-label">FTP Passwort</label>
								<div class="col">
									<input id="ftppass" name="ftppass" class="form-control" type="password" value="<?= $ftppassold ?>" />
									<span class="form-text small">Das FTP-Passwort, gespeichert in der openwb.conf</span>
								</div>
							</div>
							
						</div>
					</div>
					<div class="card-footer text-center">
					<button type="button" id="savecreds" class="btn btn-primary" onclick="location.href='./settings/savebackup.php';">Backup jetzt erstellen</button> <button type="button" id="savecreds" class="btn btn-success" onclick="checkFTP()">Einstellungen speichern</button>
					</div>
				</form>
			</div>

			
			</div>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Backup</small>
			</div>
		</footer>

		<script>

			$('#backuptarget').on('change', function() {
				if (this.value == "ftp") {
					showSection($("#ftpcreds"));
				} else {
					hideSection($("#ftpcreds"));				
				}
			});

			$('#nightlybackupchk').on('change', function() {
				if (this.checked) {
					showSection($("#shortfilename"));
				} else {
					hideSection($("#shortfilename"));				
				}
	
			});

			function checkFTP() {
				$.get(
				{ url: "./settings/testftp.php?ftphost="+$("#ftphost").val()+"&ftppath="+$("#ftppath").val()+"&ftpuser="+$("#ftpuser").val()+"&ftppass="+$("#ftppass").val(), cache: false },
				function(data){
					if (data == 0) {
						alert("Nutzername/Passwort oder Host-Adresse nicht korrekt. Einstellungen können nicht gespeichert werden!");
						return;
					} else if (data == 1) {
						alert("Nutzername/Passwort korrekt, aber Verzeichnis kann nicht gefunden bzw. in das Verzeichnis kann nicht gewechselt werden. Einstellungen können nicht gespeichert werden!");
						return;
					}
					//submit!
					$('#backupform').submit();
				}
			);
			}

			$(document).ready(function(){
				if ($('#backuptarget').val() == "local") {
					hideSection($("#ftpcreds"));		
				}
				console.log("Check: ", $('#nightlybackupchk').is(':checked'));
				if (!$('#nightlybackupchk').is(':checked')) {
					hideSection($("#shortfilename"));
				}
			});

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navOpenwbCloud').addClass('disabled');
				}
			);		
		</script>

	</body>
</html>
