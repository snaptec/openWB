<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Backup wiederherstellen</title>
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
			<h1>openWB aus Backup wiederherstellen</h1>
			<div class="alert alert-warning">
				Wiederherstellen der openWB-Einstellungen und Log-Daten aus einer Backup-Datei (Dateiendung gz).<br>
				Sollte die Wiederherstellung fehlschlagen, bitte ein Update der openWB auf die gewünschte Version durchführen. Im Anschluss die openWB neu starten und das Wiederherstellen erneut versuchen.
			</div>

			<?php
				// Returns a file size limit in bytes based on the PHP upload_max_filesize
				// and post_max_size
				function file_upload_max_size() {
					static $max_size = -1;
					static $sizeLimit = "";

					if ($max_size < 0) {
						// Start with post_max_size.
						$post_max_size = parse_size(ini_get('post_max_size'));
						if ($post_max_size > 0) {
							$max_size = $post_max_size;
							$sizeLimit = "post_max_size";
						}

						// If upload_max_size is less, then reduce. Except if upload_max_size is
						// zero, which indicates no limit.
						$upload_max = parse_size(ini_get('upload_max_filesize'));
						if ($upload_max > 0 && $upload_max < $max_size) {
							$max_size = $upload_max;
							$sizeLimit = "upload_max_filesize";
						}
					}
					return array($max_size, $sizeLimit);
				}

				function parse_size($size) {
					$unit = preg_replace('/[^bkmgtpezy]/i', '', $size); // Remove the non-unit characters from the size.
					$size = preg_replace('/[^0-9\.]/', '', $size); // Remove the non-numeric characters from the size.
					if ($unit) {
						// Find the position of the unit in the ordered string which is the power of magnitude to multiply a kilobyte by.
						return round($size * pow(1024, stripos('bkmgtpezy', $unit[0])));
					} else {
						return round($size);
					}
				}

				$target_dir = $_SERVER['DOCUMENT_ROOT'] . "/openWB/web/tools/upload/";
				$targetPath = $target_dir . "backup.tar.gz";
				$uploadOk = false;
				list($max_size, $sizeLimit) = file_upload_max_size();
				$maxSizeMB = number_format(($max_size / (1024 * 1024)), 2, ',', '.');  // german format
			?>
			<div class="alert alert-info">
				max. erlaubte Dateigröße: <?php echo $maxSizeMB ?> MB (begrenzt durch "<?php echo $sizeLimit ?>")
			</div>

			<div class="card border-secondary">
				<form action="settings/upload.php" method="POST" enctype="multipart/form-data">
					<div class="card-header bg-secondary">
						Backup-Datei
					</div>
					<div class="card-body">
						<input type="hidden" name="MAX_FILE_SIZE" value="300000000">
						<div class="input-group">
							<div class="input-group-prepend">
								<span class="input-group-text"><i class="fas fa-file-archive"></i></span>
							</div>
							<div class="custom-file">
								<input type="file" class="custom-file-input" name="fileToUpload" id="fileToUpload" accept="application/gzip" required="required">
								<label class="custom-file-label" for="fileToUpload"><i class="fas fa-search"></i> Datei auswählen</label>
							</div>
						</div>
					</div>
					<div class="card-footer text-center">
						<button id="submitBtn" type="submit" class="btn btn-success disabled">
							<i class="fas fa-upload"></i> Wiederherstellung starten
						</button>
					</div>
				</form>
			</div>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Backup wiederherstellen</small>
			</div>
		</footer>

		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$("#navWiederherstellen").addClass("disabled");
				}
			);

			$(document).ready(function() {

				$("#fileToUpload").on("change",function(e){
					//get the file name without path
					if (this.value !== "") {
						var fileName = this.value.match(/[^\\/]*$/)[0];
						var fileExt = this.value.match(/\.([^\.]+)$/)[1];
						if (fileExt == "gz") {
							//replace the "Choose a file" label
							$(this).next(".custom-file-label").text(fileName);
							$("#submitBtn").removeClass("disabled");
							return;
						}
					}
					$("#submitBtn").addClass("disabled");
					$(this).next(".custom-file-label").text("Datei auswählen");
				})

				$("#submitBtn").click(function(){
					if (!$(this).hasClass("disabled")) {
						$(this).addClass("disabled");
						$(this).text("Bitte warten, Backup wird geladen");
						$(this).parents("form").submit();
					}
				});

			})

		</script>

	</body>
</html>
