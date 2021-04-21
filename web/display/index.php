<!DOCTYPE html>
<html lang="de">
	<head>
		<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1 maximum-scale=1,user-scalable=0">
		<meta name="apple-mobile-web-app-capable" content="yes">
		<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
		<meta name="apple-mobile-web-app-title" content="OpenWB">
		<meta name="apple-mobile-web-app-status-bar-style" content="default">
		<link rel="apple-touch-startup-image" href="img/favicons/splash1125x2436w.png"  />
		<meta name="apple-mobile-web-app-title" content="openWB">
		<title>openWB</title>
		<meta name="description" content="openWB" />
		<meta name="keywords" content="openWB" />
		<meta name="author" content="Kevin Wieland" />
		<link rel="apple-touch-icon" sizes="72x72" href="img/favicons/apple-icon-72x72.png">
		<link rel="apple-touch-icon" sizes="76x76" href="img/favicons/apple-icon-76x76.png">
		<link rel="apple-touch-icon" sizes="114x114" href="img/favicons/apple-icon-114x114.png">
		<link rel="apple-touch-icon" sizes="120x120" href="img/favicons/apple-icon-120x120.png">
		<link rel="apple-touch-icon" sizes="144x144" href="img/favicons/apple-icon-144x144.png">
		<link rel="apple-touch-icon" sizes="152x152" href="img/favicons/apple-icon-152x152.png">
		<link rel="apple-touch-icon" sizes="180x180" href="img/favicons/apple-icon-180x180.png">
		<link rel="icon" type="image/png" sizes="192x192"  href="img/favicons/android-icon-192x192.png">
		<link rel="icon" type="image/png" sizes="32x32" href="img/favicons/favicon-32x32.png">
		<link rel="icon" type="image/png" sizes="96x96" href="img/favicons/favicon-96x96.png">
		<link rel="icon" type="image/png" sizes="16x16" href="img/favicons/favicon-16x16.png">
		<meta name="msapplication-TileColor" content="#ffffff">
		<meta name="msapplication-TileImage" content="/ms-icon-144x144.png">
		<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
		<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
		<link rel="manifest" href="manifest.json">
		<link rel="shortcut icon" href="img/favicons/favicon.ico">
		<link rel="apple-touch-startup-image" href="img/loader.gif">
		<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
		<meta name="theme-color" content="#ffffff">
		<meta name="google" content="notranslate">
		<script src="js/jquery-3.6.0.min.js"></script>
		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
		<!-- Main style -->
		<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
		<!-- Main style -->
		<link rel="stylesheet" type="text/css" href="css/cardio.css">
		<style>
			body {
				height: 100vh;
				background: black;
				display: flex;
				align-items: center;
				justify-content: center;
				font-family: Open Sans;
			}
			#preload {
				color: white;
				font-size: 48px;
				position: absolute;
				left: 110px;
				top: 200px;
			}
			#loaded button {
				position:absolute;
				left: 250px;
				top: 165px;
				width:300px;
				height:150px;
				background-color: #4CAF50;
				border: none;
				color: white;
				border-radius: 12px;
				font-size: 24px;
			}
		</style>
	</head>
	<body>
		<div id="preload"> 
			openWB startet... bitte warten
		</div>
		<div id="loaded" style="visibility: hidden">
			<button id="goButton">Klicken zum Interface laden</button>
		</div>
		<script>
			function changevis(){
				document.getElementById("preload").style.visibility = "hidden";
				document.getElementById("loaded").style.visibility = "visible";
			}
			setTimeout(changevis, 30000);

			$('#goButton').on("click", function(event){
				window.location.href = "display/display.php";
			});
		</script>
	</body>
</html>
