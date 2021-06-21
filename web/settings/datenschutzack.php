<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Datenschutz</title>
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

			<div class="alert alert-warning">
				Einstellungen werden gespeichert...  <i class="fas fa-cog fa-spin"></i>
			</div>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Datenschutz</small>
			</div>
		</footer>

		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					// no menue entry for this page
					// $('#navXXXXXX').addClass('disabled');
				}
			);

		</script>

		<?php
			$result = '';
			$lines = file($_SERVER["DOCUMENT_ROOT"].'/openWB/openwb.conf');
			foreach($lines as $line) {
				$writeit = '0';

				if(strpos($line, "datenschutzack=") !== false) {
					if ($_POST['dataProtectionAcknoledged'] == 1) {
						$result .= 'datenschutzack=1'."\n";
					} else {
						$result .= 'datenschutzack=2'."\n";
					}
					$writeit = '1';
				}

				if ( $writeit == '0' ) {
					$result .= $line;
				}
			}

			flush();
			file_put_contents('/var/www/html/openWB/openwb.conf', $result);
			sleep(5);

			if ($_POST['dataProtectionAcknoledged'] != 1) {
				?>
				<form id="formid" action="settings/savemqtt.php?bridge=cloud" method="POST">
					<input type="hidden" name="ConnectionName" value="cloud"/>
					<input type="hidden" name="action" value="deleteBridge"/>
				</form>
				<script>
					setTimeout(function() { document.getElementById('formid').submit(value="deleteBridge"); }, 5000);
				</script>
				<?php
			} else {
				?>
				<script>
					setTimeout(function() { window.location.href="index.php"; }, 5000);
				</script>
				<?php
			}
		?>

	</body>
</html>
