<!DOCTYPE html>
<html lang="de">
	<!-- Auswahl der verfügbaren Themes zur weiteren Anzeige
		 Bilder der Theme-Vorschau müssen als "preview.png"
		 im Theme-Ordner liegen, sollten ca. 500x280px sein -->
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
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
	</head>

	<body>

		<?php
			// support function for dynmic built of carousel content
			function dir_list($rootDir){
				// returns all directories as theme names from themes folder
				// except for themes hidden and standard
				$dirList[] = "standard";  // standard always first
				foreach( array_diff(scandir($rootDir),array('.','..')) as $subDir ) {
					if ( is_dir($rootDir.'/'.$subDir) && strcasecmp($subDir, "standard") !== 0) {
						$dirList[] = $subDir;
					}
				}
				return $dirList;
			}

			function getCarouselIndicators($dirList, $activeItem){
				$carouselIndicators = "<ul class=\"carousel-indicators\">";
				$i = 0;
				foreach( $dirList as $themeName ) {
					if( $activeItem == $themeName ){
						$active = " active";
					} else {
						$active = "";
					}
					$carouselIndicators .= "<li data-target=\"#themeselect\" data-slide-to=\"$i\" class=\"$active\"></li>";
					$i++;
				}
				$carouselIndicators .= "</ul>\n";
				return $carouselIndicators;
			}

			function getCarouselItems($dirList, $activeItem){
				$carouselItems = "<div class=\"carousel-inner\">";
				foreach( $dirList as $themeName ){
					if( $activeItem == $themeName ){
						$active = " active";
					} else {
						$active = "";
					}
					$carouselItems .= "<div class=\"carousel-item$active\">";
					$carouselItems .= "<img src=\"themes/$themeName/preview.png\" title=\"$themeName\">";
					$carouselItems .= "<div class=\"carousel-caption\"><h3>$themeName</h3></div>";
					$carouselItems .= "</div>";
				}
				$carouselItems .= "</div>\n";
				return $carouselItems;
			}

			// call function to read all directories to $allThemes
			$allThemes = dir_list($_SERVER['DOCUMENT_ROOT'] . '/openWB/web/themes');
			// set default theme
			$themeCookie = 'standard';
			// check if theme cookie exists
			if ( (isset($_COOKIE['openWBTheme'] ) === true)) {
				// check if theme exists
				if( in_array( $_COOKIE['openWBTheme'], $allThemes ) === true ){
					$themeCookie = $_COOKIE['openWBTheme'];
				}
			}
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Theme-Auswahl</h1>
			<div class="card border-secondary">
				<div class="card-header bg-secondary">
					<div class="col">Theme</div>
				</div>
				<div class="card-body">
					<div class="row justify-content-center">
						<!-- Left control -->
						<div class="col-1">
							<a class="carousel-control-prev" href="#themeselect" data-slide="prev">
								<span class="carousel-control-prev-icon"></span>
							</a>
						</div>
						<div class="col-9">
							<div id="themeselect" class="carousel slide" data-ride="carousel" data-interval="false">
								<!-- The slideshow -->
								<?php echo getCarouselItems( $allThemes, $themeCookie ); ?>
								<!-- Indicators -->
								<?php echo getCarouselIndicators( $allThemes, $themeCookie ); ?>
							</div>
						</div>
						<!-- Right control -->
						<div class="col-1">
							<a class="carousel-control-next" href="#themeselect" data-slide="next">
								<span class="carousel-control-next-icon"></span>
							</a>
						</div>
					</div>
				</div> <!-- card-body -->
				<div class="card-footer">
					<div class="row justify-content-center">
						<button id="saveButton" onclick="saveTheme()" class="btn btn-success">Theme übernehmen</button>
					</div>
				</div> <!-- card-footer -->
			</div> <!-- card -->
		</div>  <!-- end container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Erscheinungsbild/Theme-Auswahl</small>
			</div>
		</footer>

		<script>
			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navSetTheme').addClass('disabled');
				}
			);

			function saveTheme() {
				var selectedTheme = $('.carousel-item.active').find('img').attr('title');  // get theme name from active carousel item
				// console.log("selected Theme: " + selectedTheme);
				$('link[rel="stylesheet"][href^="themes/' + themeCookie + '/settings.css"]').remove();
				$('head').append('<link rel="stylesheet" href="themes/' + selectedTheme + '/settings.css?v=20200801">');
				setCookie("openWBTheme", selectedTheme, 365);
				themeCookie = selectedTheme;
				$('#saveButton').removeClass('btn-warning');
				$('#saveButton').addClass('btn-success');
			}

			function notSaved() {
				$('#saveButton').removeClass('btn-success');
				$('#saveButton').addClass('btn-warning');
			};

			$(document).ready(function(){
				$('.carousel-control-prev').click(function(){
					notSaved();
				});
				$('.carousel-control-next').click(function(){
					notSaved();
				});
				$('.carousel-indicators li').click(function(){
					notSaved();
				});
			});
		</script>

	</body>
</html>
