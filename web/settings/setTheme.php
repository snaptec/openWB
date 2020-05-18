<!DOCTYPE html>
<html lang="de">
	<!-- Auswahl der verfügbaren Themes zur weiteren Anzeige
		 Bilder der Theme-Vorschau müssen als "preview.png"
		 im Theme-Ordner liegen, sollten max 320x320px sein -->
	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Einstellungen</title>
		<meta name="description" content="Control your charge">
		<meta name="author" content="Michael Ortenstein">
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

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>

		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
		<!-- Owl Carousel -->
		<link rel="stylesheet" href="css/owlcarousel-2.3.4/owl.carousel.min.css">
		<link rel="stylesheet" href="css/owlcarousel-2.3.4/owl.theme.default.min.css">
		<script src="js/owlcarousel-2.3.4/owl.carousel.min.js"></script>

		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">
	</head>

	<body>

		<?php
			// support function for dynmic built of carousel content
			function dir_list($rootDir){
				// returns all directories as theme names from themes folder
				// except for themes hidden and standard
				$dirList[] = "standard";  // standard always first
				foreach( array_diff(scandir($rootDir),array('.','..')) as $subDir ) {
					if ( is_dir($rootDir.'/'.$subDir) && strcasecmp($subDir, "hidden") !== 0 && strcasecmp($subDir, "standard") !== 0) {
						$dirList[] = $subDir;
					}
				}
				return $dirList;
			}
			// call function to read all directories to $allThemes
			$allThemes = dir_list('/var/www/html/openWB/web/themes');
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">

			<div class="row">
				<div id="themeName" class="col text-center"></div>
			</div>

			<div class="row justify-content-center">
				<div class="col-sm-10">
					<div class="owl-carousel owl-theme">
						<?php
							foreach( $allThemes as $themeName ) {
								echo '                        <div><img src="themes/'.$themeName.'/preview.png" title="'.$themeName.'"></div>'."\n";
							}
						?>
					</div>
				</div>
			</div>

			<br>

			<div class="row justify-content-center">
				<button onclick="saveTheme()" class="btn btn-green">Theme übernehmen</button>
			</div>

		</div>  <!-- end container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Erscheinungsbild/Theme-Auswahl</small>
			</div>
		</footer>

		<script type="text/javascript">

			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navSetTheme').addClass('disabled');
			});

			function saveTheme() {
				var selectedTheme = $('#themeName').text();  // get theme name from div
				$.ajax({
					type: "GET",
					url: "setThemeCookie.php" ,
					data: { theme: selectedTheme },
					success : function() {
						window.location.href = "index.php";
					}
				});
			}

			themeCarousel = $('.owl-carousel').owlCarousel({
				loop: true,
				margin: 5,
				nav: true,
				items: 1,
				onInitialized: updateThemeName,
				onTranslated: updateThemeName
			});

			function updateThemeName(event) {
				// set theme name in div to img title
				var activeImg = $('.owl-carousel').find('.active').find('img');
				var title = activeImg.attr('title');
				if(title) $('#themeName').html('<h1>'+title+'</h1>');
			}
		</script>

	</body>
</html>
