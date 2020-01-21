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
		<title>OpenWB</title>
		<meta name="description" content="Control your charge">
		<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design">
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

		<?php include '/var/www/html/openWB/web/settings/navbar.html';?>

		<div role="main" class="container" style="margin-top:20px">
			<div>
				<div class="row justify-content-center">
					<div class="col-xl-3 col-md-4 justify-content-center">
						<b class="regularTextStyle">verfügbare Themes:</b>
						<br>
						<select onchange="$('#themePreview').attr('src', 'themes/'+this.options[this.selectedIndex].value+'/preview.png');" id="themeSelector">
							<option value="standard">Standard-Theme</option>
							<?php

								function dir_list($rootDir){
									// returns all directories as theme names from themes folder except for folder called hidden,
									foreach( array_diff(scandir($rootDir),array('.','..')) as $subDir ) {
										if ( is_dir($rootDir.'/'.$subDir) && strcasecmp($subDir, "hidden") !== 0 ) {
											$dirList[]=$subDir;
										}
									}
									return $dirList;
								}

								// call function to read all directories
								$allThemes = dir_list('/var/www/html/openWB/web/themes');
								// and put result in dropdown, standard always first
								foreach( $allThemes as $theme ) {
									if ( strcasecmp($theme, "standard") !== 0 ) {
										echo '                    <option value="'.$theme.'">'.$theme.'</option>'."\n";
									}
								}
							?>
						</select>
					</div>
					<div class="col-xl-4 col-md-4 justify-content-center">
						<!-- display standard theme = first entry initially -->
						<img id="themePreview" class="img-fluid" src="themes/standard/preview.png" alt="Theme Vorschau"/>
					</div>
				</div>

				<br>
			</div>

			<div class="row justify-content-center">
				<button onclick="setThemeClicked()" class="btn btn-lg btn-green">Einstellungen speichern</button>
			</div>

		</div>  <!-- end container -->

		<footer class="footer bg-dark text-light font-small">
	      <div class="container text-center">
			  <small>Sie befinden sich hier: Einstellungen/Theme</small>
	      </div>
	    </footer>

		<script language="javascript">
	    	function setThemeClicked() {
				var selector = document.getElementById("themeSelector");
				var selectedTheme = selector.options[selector.selectedIndex].value;
	        	$.ajax({
	            	type: "GET",
	            	url: "setThemeCookie.php" ,
	            	data: { theme: selectedTheme },
	            	success : function() {
	            		window.location.href = "index.php";
					}
	        	});
	    	}
	    </script>

	</body>
</html>
