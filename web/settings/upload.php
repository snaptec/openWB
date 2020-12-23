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

<?php
// Returns a file size limit in bytes based on the PHP upload_max_filesize
// and post_max_size
function file_upload_max_size() {
	static $max_size = -1;

	if ($max_size < 0) {
		// Start with post_max_size.
		$post_max_size = parse_size(ini_get('post_max_size'));
		if ($post_max_size > 0) {
			$max_size = $post_max_size;
		}

		// If upload_max_size is less, then reduce. Except if upload_max_size is
		// zero, which indicates no limit.
		$upload_max = parse_size(ini_get('upload_max_filesize'));
		if ($upload_max > 0 && $upload_max < $max_size) {
			$max_size = $upload_max;
		}
	}
	return $max_size;
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
$target_file = $target_dir . basename( $_FILES["fileToUpload"]["name"] );
$uploadOk = true;
$doUpdate = false;
$imageFileType = strtolower( pathinfo( $target_file, PATHINFO_EXTENSION ) );
?>
			<div class="alert alert-info">
				Maximale Dateigröße: <?php echo file_upload_max_size(); ?> Bytes
			</div>
<?php
if ( $_FILES["fileToUpload"]["size"] > file_upload_max_size() ) {
	$uploadOk = false;
	?>
			<div class="alert alert-danger">
				Die Datei ist zu groß.
			</div>
	<?php
}
if ($uploadOk !== true) {
	?>
			<div class="alert alert-danger">
				Die Datei konnte nicht hochgeladen werden.
			</div>
	<?php
} else {
	if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
		$doUpdate = true;
		?>
			<div class="alert alert-info">
				Wiederherstellung wird durchgeführt, bitte warten! <i class="fas fa-cog fa-spin"></i>
			</div>
		<?php
	} else {
		?>
			<div class="alert alert-danger">
				Es gab einen Fehler beim Hochladen der Datei. Ist diese eventuell zu groß?
			</div>
		<?php
	}
}
?>
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
					$('#navWiederherstellen').addClass('disabled');
				}
			);

		</script>
<?php
if($doUpdate === true) {
	sleep(5);
	exec($_SERVER['DOCUMENT_ROOT']."/openWB/runs/restore.sh >> ".$_SERVER['DOCUMENT_ROOT']."/openWB/web/tools/upload/restore.log");
	?>
		<script>
			setTimeout(function() { window.location = "index.php"; }, 15000);
		</script>
	<?php
}
?>

	</body>
</html>
