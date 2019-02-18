<!DOCTYPE html>
<html lang="en">

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
	<link rel="manifest" href="img/favicons/manifest.json">
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
	<!-- Font Awesome -->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.1.0/css/font-awesome.min.css">
	<!-- Elegant Icons -->
	<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
	<!-- Main style -->
	<link rel="stylesheet" type="text/css" href="css/cardio.css">
</head>
<?php
$limit = 10;
if (isset($_GET[lines])) {
	$limit = $_GET[lines];
	$_SESSION = $limit;
} else {
	$limit = 20;
	$_SESSION = $limit;
}
?>

<body>
	<div class="preloader">
		<img src="img/loader.gif" alt="Preloader image">
	</div>
<section id="services">
		<div class="container">
			<div class="row">
				<div class="col-xs-12 text-center">
					<h3> OpenWB Ladelog </h3>
				</div>
			</div>
			<br><br>
		</div>
		<div class="row">
			<div class="col-xs-2">
				<button onclick="window.location.href='./index.php'" class="btn btn-primary btn-blue">Zurück</button>
			</div>

			<div class="col-xs-2">
			</div>
		</div>
		<br><br>
		<div class="row">
			<div class="col-xs-12 text-center">
				<div class="col-xs-2 text-center" style="font-size: 1vw">
					Startzeit
				</div>	
				<div class="col-xs-2 text-center" style="font-size: 1vw">
					Endzeit
				</div>
				<div class="col-xs-2 text-center" style="font-size: 1vw">
					Geladene km
				</div>	
				<div class="col-xs-2 text-center" style="font-size: 1vw">
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
while (($logarray = fgetcsv($file)) !== FALSE) {
	echo '<div class="row">';
		echo '<div class="col-xs-12 text-center">';
			echo '<div class="col-xs-2 text-center" style="font-size: 1.5vw">';
			print_r($logarray[0]);
			$start = strtotime($logarray[0]);
			echo '</div>';
			echo '<div class="col-xs-2 text-center" style="font-size: 1.5vw">';
			print_r($logarray[1]);
			$stop = strtotime($logarray[1]);

			echo '</div>';
			echo '<div class="col-xs-2 text-center" style="font-size: 1.5vw">';
			print_r($logarray[2]);
			$sumgelkm=$sumgelkm + $logarray[2];

			echo '</div>';
			echo '<div class="col-xs-2 text-center" style="font-size: 1.5vw">';
				print_r($logarray[3]);
				$sumkwh=$sumkwh + $logarray[3];
			echo '</div>';
			echo '<div class="col-xs-2 text-center" style="font-size: 1.5vw">';
			print_r($logarray[4]);
				$avgladel=$avgladel + $logarray[4];
				$count=$count + 1;
			echo '</div>';
			echo '<div class="col-xs-1 text-center" style="font-size: 1.5vw">';
				print_r($logarray[5]);
			echo '</div>';
			echo '<div class="col-xs-1 text-center" style="font-size: 1.5vw">';
				print_r($logarray[6]);
			echo '</div>';

		echo '</div>';
	echo '</div>';
	echo '<hr>';
$ladezeit = $ladezeit + (($stop - $start) / 60 );
	  }
fclose($file);
$avgladel = round($avgladel / $count, 3);
$ladezeit = round($ladezeit / $count, 2);
?>

<hr>
	</div>
	<div class="row">
			<div class="col-xs-12 text-center">
				<div class="col-xs-2 text-center" style="font-size: 1vw">
					Startzeit
				</div>	
				<div class="col-xs-2 text-center" style="font-size: 1vw">
					Endzeit
				</div>
				<div class="col-xs-2 text-center" style="font-size: 1vw">
					Geladene km gesamt
				</div>	
				<div class="col-xs-2 text-center" style="font-size: 1vw">
					Geladene kWh gesamt
				</div>	
				<div class="col-xs-2 text-center" style="font-size: 1vw">
					Durchschnittliche Ladeleistung kW
				</div>	
				<div class="col-xs-1 text-center" style="font-size: 1vw">
					Dirchschnittliche Ladedauer
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
				<div class="col-xs-2 text-center" style="font-size: 1.5vw">
						<?php print($sumgelkm); ?>	</div>	
				<div class="col-xs-2 text-center" style="font-size: 1.5vw">
					<?php print($sumkwh); ?>

				</div>	
				<div class="col-xs-2 text-center" style="font-size: 1.5vw">
						<?php print($avgladel); ?>
				</div>	
				<div class="col-xs-1 text-center" style="font-size: 1.5vw">
						<?php print($ladezeit); ?> Minuten
				</div>	
				<div class="col-xs-1 text-center" style="font-size: 1vw">
				</div>	
	</div>
</div>

<div class="row">
	<div class="col-xs-1">
	</div>
	<div class="col-xs-7">
	<form name="limitlines" id="limitlines" action="ladelog.php" method="GET">
		<label for="lines">Anzahl angezeigter Zeilen</label>
		<input id="lines" name="lines" type="number" min="0" value="<?php print $limit ?>" required="required" />
		<button type="submit">Go</button>
	</form>
	</div>
	<div class="col-xs-4">
	</div>
</div>

<br><br>
 <button onclick="window.location.href='./index.php'" class="btn btn-primary btn-blue">Zurück</button>
<form method="get" action="../ramdisk/tladelog">
 <button class="btn btn-primary btn-green">Download csv</button>
</form>
<br><br>

</div>
	</section>


	<div class="mobile-nav">
		<ul>
		</ul>
		<a href="#" class="close-link"><i class="arrow_up"></i></a>
	</div>
	<!-- Scripts -->
	<script src="js/owl.carousel.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="js/wow.min.js"></script>
	<script src="js/typewriter.js"></script>
	<script src="js/jquery.onepagenav.js"></script>
	<script src="js/main.js"></script>
	<script type='text/javascript'>









</body>






</html>
