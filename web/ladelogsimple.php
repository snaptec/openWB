<!DOCTYPE html>
<html lang="de">

<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB</title>
	<meta name="description" content="Control your charge" />
	<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
	<meta name="author" content="Kevin Wieland" />
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
	<!-- Animate.css -->
	<link rel="stylesheet" type="text/css" href="css/animate.css">
	<!-- Font Awesome, all styles -->
    <link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
	<!-- Elegant Icons -->
	<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
	<!-- Main styles -->
	<link rel="stylesheet" type="text/css" href="css/cardio.css">
</head>
<?php
$limit = 50;
if (isset($_GET['lines'])) {
	$limit = $_GET['lines'];
	$_SESSION = $limit;
} else {
	$limit = 50;
	$_SESSION = $limit;
}
if (isset($_GET['von'])) {
	$wahlstart = strtotime($_GET['von']);
} else {
	$wahlstart = strtotime("-4 weeks");
}
if (isset($_GET['bis'])) {
	$wahlstop = strtotime($_GET['bis']);
} else {
	$wahlstop = strtotime("tomorrow");
}
?>
<body>
	<div class="preloader">
		<img src="img/loading.gif" alt="Preloader image">
	</div>
	<section id="services">
		<div class="container">
			<div class="row">
				<div class="col-xs-12 text-center">
					<h3> Lade-Log </h3>
				</div>
			</div>
			<div class="row">
				<div class="col-xs-2">
					<button onclick="window.location.href='./index.php'" class="btn btn-primary btn-blue">Zurück</button>
				</div>
				<div class="col-xs-2">
				</div>
			</div>
			<div class="row">
				<div class="col-xs-12 text-center">
					<div class="col-xs-2 text-center" style="font-size: 1vw">
						Startzeit
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1vw">
						Endzeit
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
						Geladene km
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
						Geladene kWh
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1vw">
						Durchschnittliche Ladeleistung kW
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
						Ladedauer
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
						Ladepunkt
					</div>
				</div>
			</div>
			<hr>
<?php
$ifile = fopen('ladelog', "r");
$ofile = fopen('../ramdisk/tladelog', "w+");

$counter = 1;
while($counter <= $limit) {
	$line = fgetcsv($ifile);
	fputcsv($ofile, $line);
	$counter++;
}

$start = 0;
$stop = 0;
$ladezeit = 0;
$count = 0;
$avgladel = 0;
$sumkwh = 0;
$sumgelkm = 0;
$file = fopen('../ramdisk/tladelog', 'r');
$extractf = fopen('../ramdisk/ladelog.csv', "w+");
while (($logarray = fgetcsv($file)) !== FALSE) {
	$startime = str_replace('.', '-', $logarray[0]);
	$startime = strtotime(substr_replace($startime, "20", "6", 0));
	$endtime = str_replace('.', '-', $logarray[1]);
	$endtime = strtotime(substr_replace($endtime, "20", "6", 0));
	if (isset($_GET['zeitakt']) && $_GET['zeitakt'] == "on" ) {
		if ( $wahlstart < $startime && $wahlstop > $endtime) {
			fputcsv($extractf, $logarray);
			?>
			<div class="row">
				<div class="col-xs-12 text-center">
					<div class="col-xs-2 text-center" style="font-size: 1.5vw">
			<?php
			print_r($logarray[0]);
			$start = $startime;
			?>
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1.5vw">
			<?php
			print_r($logarray[1]);
			$stop = $endtime;
			?>
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
			<?php
			print_r($logarray[2]);
			$sumgelkm=$sumgelkm + $logarray[2];
			?>
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
			<?php
			print_r($logarray[3]);
			$sumkwh=$sumkwh + $logarray[3];
			?>
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1.5vw">
			<?php
			print_r($logarray[4]);
			$avgladel=$avgladel + $logarray[4];
			$count=$count + 1;
			?>
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
			<?php print_r($logarray[5]); ?>
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
			<?php print_r($logarray[6]); ?>
					</div>
				</div>
			</div>
			<hr>
			<?php
			$ladezeit = $ladezeit + (($stop - $start) / 60 );
		}
	} else {
		fputcsv($extractf, $logarray);
		?>
			<div class="row">
				<div class="col-xs-12 text-center">
					<div class="col-xs-2 text-center" style="font-size: 1.5vw">
		<?php
		print_r($logarray[0]);
		$start = $startime;
		?>
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1.5vw">
		<?php
		print_r($logarray[1]);
		$stop = $endtime;
		?>
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
		<?php
		print_r($logarray[2]);
		$sumgelkm=$sumgelkm + $logarray[2];
		?>
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
		<?php
		print_r($logarray[3]);
		$sumkwh=$sumkwh + $logarray[3];
		?>
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1.5vw">
		<?php
		print_r($logarray[4]);
		$avgladel=$avgladel + $logarray[4];
		$count=$count + 1;
		?>
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
		<?php print_r($logarray[5]); ?>
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
		<?php print_r($logarray[6]); ?>
					</div>
				</div>
			</div>
			<hr>
		<?php
		$ladezeit = $ladezeit + (($stop - $start) / 60 );
	}
}
fclose($file);
fclose($extractf);
$avgladel = round($avgladel / $count, 3);
$ladezeit = intval(round($ladezeit / $count, 2));
?>
			<hr>
			<div class="row">
				<div class="col-xs-12 text-center">
					<div class="col-xs-2 text-center" style="font-size: 1vw">
						Startzeit
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1vw">
						Endzeit
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
						Geladene km gesamt
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
						Geladene kWh gesamt
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1vw">
						Durchschnittliche Ladeleistung kW
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
						Durchschnittliche Ladedauer
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
						Ladepunkt
					</div>
				</div>
			</div>
			<div class="row">
				<div class="col-xs-12 text-center">
					<div class="col-xs-2 text-center" style="font-size: 1vw">
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1vw">
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
						<?php print($sumgelkm); ?>	</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
						<?php print($sumkwh); ?>
					</div>
					<div class="col-xs-2 text-center" style="font-size: 1.5vw">
						<?php print($avgladel); ?>
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1.5vw">
						<?php print($ladezeit); ?> Min
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
					</div>
					<div class="col-xs-1 text-center" style="font-size: 1vw">
					</div>
				</div>
			</div>
			<div class="row">
				<div class="col-xs-1">
				</div>
				<div class="col-xs-7">
					<form name="limitlines" id="limitlines" action="ladelogsimple.php" method="GET">
						<label for="lines">Anzahl berücksichtigter Ladungen</label>
						<input id="lines" name="lines" type="number" min="0" value="<?php print $limit ?>" required="required" /><br>
						<label for="zeitakt">Filter aktiv:</label>
						<input id="zeitakt" name="zeitakt" type="checkbox" <?php if (isset($_GET['zeitakt'])){ if ( $_GET['zeitakt'] == "on"){ echo "checked"; }} ?> ><br>
						<label for="von">Startdatum:</label>
						<input id="von" name="von" type="date" min="2018-01-01" value="<?php print date("Y-m-d", $wahlstart) ?>" required="required" />
						<label for="bis">Enddatum:</label>
						<input id="bis" name="bis" type="date" min="2018-01-01" value="<?php print date("Y-m-d", $wahlstop) ?>" required="required" /><br>
						<!--
						<label for="lp1akt">LP1:</label>
						<input id="lp1akt" name="lp1akt" type="checkbox" <?php if (isset($_GET['lp1akt'])){ if ( $_GET['lp1akt'] == "on"){ echo "checked"; }} ?> >
						<label for="lp2akt">LP2:</label>
						<input id="lp2akt" name="lp2akt" type="checkbox" <?php if (isset($_GET['lp2akt'])){ if ( $_GET['lp2akt'] == "on"){ echo "checked"; }} ?> >
						<label for="lp3akt">LP3:</label>
						<input id="lp3akt" name="lp3akt" type="checkbox" <?php if (isset($_GET['lp3akt'])){ if ( $_GET['lp3akt'] == "on"){ echo "checked"; }} ?> ><br>
						<label for="sofort">Sofortlademodus:</label>
						<input id="sofort" name="sofort" type="checkbox" <?php if (isset($_GET['sofort'])){ if ( $_GET['sofort'] == "on"){ echo "checked"; }} ?> ><br>
						<label for="minpv">Min+PV Lademodus:</label>
						<input id="minpv" name="minpv" type="checkbox" <?php if (isset($_GET['minpv'])){ if ( $_GET['minpv'] == "on"){ echo "checked"; }} ?> ><br>
						<label for="nurpv">NurPV Lademodus:</label>
						<input id="nurpv" name="nurpv" type="checkbox" <?php if (isset($_GET['nurpv'])){ if ( $_GET['nurpv'] == "on"){ echo "checked"; }} ?> ><br>
						<label for="standby">Standby Lademodus:</label>
						<input id="standby" name="standby" type="checkbox" <?php if (isset($_GET['standby'])){ if ( $_GET['standby'] == "on"){ echo "checked"; }} ?> ><br>
						<label for="nachtladenlp1">Nachtladen LP1:</label>
						<input id="nachtladenlp1" name="nachtladenlp1" type="checkbox" <?php if (isset($_GET['nachtladenlp1'])){ if ( $_GET['nachtladenlp1'] == "on"){ echo "checked"; }} ?> ><br>
						<label for="rfidakt">RFID:</label>
						<input id="rfidakt" name="rfidakt" type="checkbox" <?php if (isset($_GET['rfidakt'])){ if ( $_GET['rfidakt'] == "on"){ echo "checked"; }} ?> >
						<label for="rfid">TAG:</label>
						<input id="rfid" name="rfid" type="text" value="<?php if (isset($_GET['rfid'])){  echo $_GET['rfid']; } ?>" ><br>
						-->
						<button class="btn btn-primary btn-green" type="submit">Go</button>
					</form>
				</div>
				<div class="col-xs-4">
				</div>
			</div>
			<div class="row">
				<button onclick="window.location.href='./index.php'" class="btn btn-primary btn-blue">Zurück</button>
				<form method="get" action="../ramdisk/ladelog.csv">
					<button class="btn btn-primary btn-green">Download csv</button>
				</form>
			</div>
		</div>
	</section>

	<div class="mobile-nav">
		<a href="#" class="close-link"><i class="arrow_up"></i></a>
	</div>
	<!-- Scripts -->
	<script src="js/owl.carousel.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="js/wow.min.js"></script>
	<script src="js/typewriter.js"></script>
	<script src="js/jquery.onepagenav.js"></script>
	<script src="js/main.js"></script>
</body>
</html>
