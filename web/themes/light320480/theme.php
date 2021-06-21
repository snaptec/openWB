<!DOCTYPE html>
<html lang="en">

<head>
	<title>openWB</title>
	<?php include ("values.php");?>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0">
         <meta name="apple-mobile-web-app-capable" content="yes">
         <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
         <meta name="apple-mobile-web-app-title" content="openWB">
	<meta name="apple-mobile-web-app-status-bar-style" content="default">
	<link rel="apple-touch-startup-image" href="/openWB/web/img/favicons/splash1125x2436w.png"  />
	<link rel="apple-touch-startup-image" media="(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)" href="img/favicons/splash1125x2436w.png">
	<meta name="apple-mobile-web-app-title" content="openWB">

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
	<!-- <link rel="apple-touch-startup-image" href="img/loader.gif"> -->
	<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">
	<!-- Normalize -->
	<link rel="stylesheet" type="text/css" href="css/normalize.css">
	<!-- Bootstrap -->
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<!-- Owl -->
	<link rel="stylesheet" type="text/css" href="css/owl.css">
	<!-- Animate.css -->
	<link rel="stylesheet" type="text/css" href="css/animate.css">
	<!-- Font Awesome, all styles -->
  <link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
	<!-- Elegant Icons -->
	<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
	<!-- Main style -->
	<link rel="stylesheet" type="text/css" href="css/cardio.css">
	<link rel="stylesheet" type="text/css" href="css/pwa.css">

    <!-- include special Theme style -->
	<link rel="stylesheet" type="text/css" href="themes/<?php echo $_COOKIE['openWBTheme'];?>/style.css">

	<!-- important Scripts to be loaded first-->
	<script src="js/jquery-1.11.1.min.js"></script>
	<script src="js/owl.carousel.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="js/wow.min.js"></script>
	<script src="js/typewriter.js"></script>
	<script src="js/jquery.onepagenav.js"></script>
	<script src="js/main.js"></script>
</head>

<script>
	var hook1_aktiv = <?php echo $hook1_aktivold ?>;
	var hook2_aktiv = <?php echo $hook2_aktivold ?>;
	var hook3_aktiv = <?php echo $hook3_aktivold ?>;
	var activetheme = "<?php echo $themeCookie ?>";
	registerPageVisibility()
	function registerPageVisibility() {
		let hidden;
	        let visibilityChange;
	        if (typeof document.hidden !== 'undefined') { // Opera 12.10 and Firefox 18 and later support
		        hidden = 'hidden';
		        visibilityChange = 'visibilitychange';
		} else if (typeof document.msHidden !== 'undefined') {
			hidden = 'msHidden';
		        visibilityChange = 'msvisibilitychange';
		} else if (typeof document.webkitHidden !== 'undefined') {
		        hidden = 'webkitHidden';
		        visibilityChange = 'webkitvisibilitychange';
		}
		window.document.addEventListener(visibilityChange, () => {
	        if (!document[hidden]) {
				initialread = 0;
				all1 = 0;
				all2 = 0;
				all3 = 0;
				all4 = 0;
				all5 = 0;
				all6 = 0;
				all7 = 0;
				all8 = 0;
			}
		});
	}
</script>

<input hidden name="lastmanagement" id="lastmanagement" value="<?php echo $lastmanagementold ; ?>" />
<input hidden name="lastmanagements2" id="lastmanagements2" value="<?php echo $lastmanagements2old ; ?>" />
<input hidden name="speicherstat" id="speicherstat" value="<?php echo $speicherstatold ; ?>" />
<input hidden name="lademlp1stat" id="lademlp1stat" value="<?php echo $lademstatold ; ?>" />
<input hidden name="lademlp2stat" id="lademlp2stat" value="<?php echo $lademstats1old ; ?>" />
<input hidden name="lademlp3stat" id="lademlp3stat" value="<?php echo $lademstats2old ; ?>" />
<input hidden name="evuglaettungakt" id="evuglaettungakt" value="<?php echo $evuglaettungaktold ; ?>" />
<input hidden name="nachtladenstate" id="nachtladenstate" value="<?php echo $nachtladenstate ; ?>" />
<input hidden name="nachtladenstates1" id="nachtladenstates1" value="<?php echo $nachtladenstates1 ; ?>" />
<input hidden name="nlakt_nurpv" id="nlakt_nurpv" value="<?php echo $nlakt_nurpvold ; ?>" />
<input hidden name="nlakt_sofort" id="nlakt_sofort" value="<?php echo $nlakt_sofortold ; ?>" />
<input hidden name="nlakt_minpv" id="nlakt_minpv" value="<?php echo $nlakt_minpvold ; ?>" />
<input hidden name="nlakt_standby" id="nlakt_standby" value="<?php echo $nlakt_standbyold ; ?>" />
<input hidden name="lademodus" id="lademodus" value="<?php echo $lademodusold ; ?>" />
<input hidden name="hausverbrauchstat" id="hausverbrauchstat" value="<?php echo $hausverbrauchstatold ; ?>" />
<input hidden name="speicherpvui" id="speicherpvui" value="<?php echo $speicherpvuiold ; ?>" />
<input hidden name="zielladenaktivlp1" id="zielladenaktivlp1" value="<?php echo $zielladenaktivlp1old ; ?>" />
<input hidden name="sofortlm" id="sofortlm" value="<?php echo $lademodusold ; ?>" />
<input hidden name="heutegeladen" id="heutegeladen" value="<?php echo $heutegeladenold ; ?>" />


<body>
	<div class="preloader">
		<img src="img/loader.gif" alt="Preloader image">
	</div>

<?php
	// das gewählte Theme einbinden
	include 'themes/'.$_COOKIE['openWBTheme'].'/themebody.html';
?>
		</div>

	<!-- Holder for mobile navigation -->
	<div class="mobile-nav">
		<ul>
		</ul>
		<a href="#" class="close-link"><i class="arrow_up"></i></a>
	</div>

	<!-- load Chart.js library -->
	<script src="js/Chart.bundle.js"></script>

	<!-- load mqtt library -->
	<script src = "js/mqttws31.js" ></script>

	<!-- load respective Chart.js definition since function declarations are used by global live.js-->
	<script src="livechart_chartjs.js?version=9"></script>
	<!-- Data refresher -->
	<script src="live.js?vers=14"></script>
	<script src="livefunctions.js?vers=7"></script>
</body>

</html>
