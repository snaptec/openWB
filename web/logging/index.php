<html>


<head>
	<script src="../js/core.js"></script>
	<script src="../js/Chart.bundle.js"></script>
	<script src="../js/animated.js"></script>
	<script src="../js/jquery-1.11.1.min.js"></script>
	<script src="../js/owl.carousel.min.js"></script>
	<script src="../js/bootstrap.min.js"></script>
	<script src="../js/wow.min.js"></script>
	<script src="../js/typewriter.js"></script>
	<script src="../js/jquery.onepagenav.js"></script>
	<script src="../js/main.js"></script>
	<script src="longlivechart.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Live Langzeitansicht</title>
	<meta name="description" content="Control your charge" />
	<meta name="author" content="Kevin Wieland" />
	<link rel="apple-touch-icon" sizes="57x57" href="../img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="../img/favicons/apple-touch-icon-60x60.png">
	<link rel="icon" type="image/png" href="../img/favicons/favicon-32x32.png" sizes="32x32">
	<link rel="icon" type="image/png" href="../img/favicons/favicon-16x16.png" sizes="16x16">
	<link rel="manifest" href="../manifest.json">
	<link rel="shortcut icon" href="../img/favicons/favicon.ico">
	<meta name="msapplication-TileColor" content="#00a8ff">
	<meta name="msapplication-config" content="../img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">
	<meta http-equiv="refresh" content="600; URL=index.php">
	<link rel="stylesheet" type="text/css" href="../css/normalize.css">
	<link rel="stylesheet" type="text/css" href="../css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="../css/owl.css">
	<link rel="stylesheet" type="text/css" href="../css/animate.css">
	<!-- Font Awesome, all styles -->
    <link href="../fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
	<link rel="stylesheet" type="text/css" href="../fonts/eleganticons/et-icons.css">
	<link rel="stylesheet" type="text/css" href="../css/cardio.css">
</head>
<?php
	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		if(strpos($line, "graphinteractiveam=") !== false) {
			list(, $graphinteractiveamold) = explode("=", $line);
		}

		if(strpos($line, "verbraucher1_name=") !== false) {
			list(, $verbraucher1_nameold) = explode("=", $line);
		}
		if(strpos($line, "verbraucher2_name=") !== false) {
			list(, $verbraucher2_nameold) = explode("=", $line);
		}
		if(strpos($line, "grapham=") !== false) {
			list(, $graphamold) = explode("=", $line);
		}
		if(strpos($line, "lastmanagement=") !== false) {
			list(, $lastmanagementold) = explode("=", $line);
		}
		if(strpos($line, "simplemode=") !== false) {
			list(, $simplemodeold) = explode("=", $line);
		}

	}
$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
$soc1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/soc1vorhanden');
$verbraucher1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher1vorhanden');
$verbraucher2vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher2vorhanden');
$verbraucher1_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher1_nameold));
$verbraucher2_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher2_nameold));

					?>

<body>


		 <ul class="nav nav-tabs">
			 <li><a href="../index.php">Zurück</a></li>
			 <li class="active"><a href="index.php">Live</a></li>
			 <li><a href="daily.php">Daily</a></li>
			 <li><a href="monthly.php">Monthly</a></li>
			 <li><a href="yearly.php">Yearly</a></li>
		 </ul>

	<div class="preloader">
<?php if ( $simplemodeold == 1 ) {
echo '	<img src="../img/loading.gif" alt="loading...">';} else {
echo '<img src="../img/loader.gif" alt="OpenWB loading...">'; } ?>
	</div>


<div class="row">
	<div class="text-center">
		<br><h3> Langzeit Live Logging</h3><br>
	</div>
</div>

<div id="loadlivegraph" style="text-align: center; margin-top: 150px; margin-bottom: 100px;"> Graph lädt bitte warten...</div>	
	<div id="livegraphvis" style="height:600px;"><canvas id="canvas"></canvas></div>




<script>
	var lastmanagement = <?php echo $lastmanagementold ?>;
	var soc1vorhanden = <?php echo $soc1vorhanden ?>;
	var verbraucher1vorhanden = <?php echo $verbraucher1vorhanden ?>;
	var verbraucher2vorhanden = <?php echo $verbraucher2vorhanden ?>;
	var speichervorhanden = <?php echo $speichervorhanden ?>;
	var verbraucher1name = "<?php echo $verbraucher1_nameold ?>";
	var verbraucher2name = "<?php echo $verbraucher2_nameold ?>";
</script>




	<script>

</script>






</body>
</html>
