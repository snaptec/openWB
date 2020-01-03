<!DOCTYPE html>
<html lang="en">
<!-- Auswahl der verfügbaren Themes zur weiteren Anzeige
   	 Bilder der Theme-Vorschau müssen als "preview.png"
   	 im Theme-Ordner liegen, sollten max 320x320px sein -->
<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB</title>
	<meta name="description" content="Control your charge" />
	<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
	<meta name="author" content="Michael Ortenstein" />
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
	<!-- Normalize -->
	<link rel="stylesheet" type="text/css" href="css/normalize.css">
	<!-- Bootstrap -->
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<!-- Owl -->
	<link rel="stylesheet" type="text/css" href="css/owl.css">
	<!-- Main style -->
	<link rel="stylesheet" type="text/css" href="css/cardio.css">
</head>

<body>

	<div class="container">
		<div class="row"><br>
			<ul class="nav nav-tabs">
				<li><a data-toggle="tab" href="./index.php">Zurück</a></li>
				<li><a href="./settings.php">Einstellungen</a></li>
  				<li><a href="./pvconfig.php">PV Ladeeinstellungen</a></li>
				<li><a href="./smarthome.php">Smart Home</a></li>
				<li><a href="./modulconfig.php">Modulkonfiguration</a></li>
				<li class="active"><a href="./setTheme.php">Theme</a></li>
				<li><a href="./mqtt.php">MQTT</a></li>
				<li><a href="./misc.php">Misc</a></li>
			</ul>
			<br><br>
		</div>

		<h3>aktives Theme</h3>
		<div class="row">
  			<div class="col-sm-4">
    			<div class="thumbnail">
      				<img src="./themes/<?php echo $_COOKIE['openWBTheme']?>/preview.png" height="120" alt="Theme Vorschau"/>
      				<div class="caption">
        				<h4 class="text-center"><?php echo $_COOKIE['openWBTheme']?></h4>
      				</div>
    			</div>
  			</div>
		</div>
		<br>

		<h3>Theme-Auswahl</h3>
		<div class="row">
			<div>
				<b>verfügbare Themes: </b>
				<br>
				<select onchange="$('#themePreview').attr('src', './themes/'+this.options[this.selectedIndex].value+'/preview.png');" id="themeSelector">
		        	<?php
						function dir_list($d){
							// gibt alle Verzeichnisse (=Themes) im Theme-Ordner zurück
   							foreach(array_diff(scandir($d),array('.','..')) as $f)if(is_dir($d.'/'.$f))$l[]=$f;
   							return $l;
						}
		        	// alle Themes lesen
		        	$allThemes = dir_list('./themes');
		        	// und Themes ins Dropdwon
		        	foreach($allThemes as $theme){
		        		?>
		        		<option value=<?php echo $theme;?>><?php echo $theme;?></option>
		        		<?php
		        		}
		        		?>
		    	</select>
			</div>
			<br>

  			<div class="col-sm-4">
    			<div class="thumbnail" style="min-height: 150px">
					<!-- immer zunächst das erste Theme des Dropdown-Selectors als Preview anzeigen -->
      				<img id="themePreview" src="./themes/<?php echo $allThemes[0]?>/preview.png" alt="Theme Vorschau"/>
    			</div>
  			</div>
		</div>
		<br><br>

		<button onclick="setThemeClicked()" class="btn btn-primary btn-green">Theme übernehmen</button>
		<button onclick="window.location.href='./index.php'" class="btn btn-primary btn-blue">Zurück</button>
	</div>

	<script language="javascript">
    	function setThemeClicked() {
			var selector = document.getElementById("themeSelector");
			var selectedTheme = selector.options[selector.selectedIndex].value;
        	$.ajax({
            	type: "GET",
            	url: "setThemeCookie.php" ,
            	data: { theme: selectedTheme },
            	success : function() {
            		window.location.href = "./index.php";
				}
        	});
    	}
    </script>

</body>
</html>
