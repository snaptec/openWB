<html>


<head>
	<script src="../js/jquery-1.11.1.min.js"></script>
	<script src="../js/main.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB Logging</title>
	<meta name="description" content="Control your charge" />
	<meta name="author" content="Kevin Wieland" />
	<link rel="apple-touch-icon" sizes="57x57" href="../img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="../img/favicons/apple-touch-icon-60x60.png">
	<link rel="icon" type="image/png" href="../img/favicons/favicon-32x32.png" sizes="32x32">
	<link rel="icon" type="image/png" href="../img/favicons/favicon-16x16.png" sizes="16x16">
	<link rel="manifest" href="../img/favicons/manifest.json">
	<link rel="shortcut icon" href="../img/favicons/favicon.ico">
	<meta name="msapplication-TileColor" content="#00a8ff">
	<meta name="msapplication-config" content="../img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">
	<link rel="stylesheet" type="text/css" href="../css/normalize.css">
	<link rel="stylesheet" type="text/css" href="../css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="../css/owl.css">
	<link rel="stylesheet" type="text/css" href="../css/animate.css">
	<link rel="stylesheet" type="text/css" href="../fonts/font-awesome-4.1.0/css/font-awesome.min.css">
	<link rel="stylesheet" type="text/css" href="../fonts/eleganticons/et-icons.css">
	<link rel="stylesheet" type="text/css" href="../css/cardio.css">
</head>


<body>


		 <ul class="nav nav-tabs">
			 <li><a href="../index.php">Zurück</a></li>
			 <li><a href="index.php">Live</a></li>
			 <li><a href="daily.php">Daily</a></li>
			 <li class="active"><a href="monthly.php">Monthly</a></li>
			 <li><a href="yearly.php">Yearly</a></li>
		 </ul>


	<div class="preloader">
		<img src="../img/loader.gif" alt="Preloader image">
	</div> 
<section id="services">
<div class="container">


<?php
$today = date('Y-m-d');
if (isset($_GET[date])) {
	$monthdate = $_GET[date];
	$_SESSION = $monthdate;
}
else
{
	$monthdate = $today;
	$_SESSION = $monthdate;
}
?>

<div class="row col-xs-12">
	<div class="text-center">
		<br><h4> Monthly Graph</h4><br>
	</div>
</div>


<div class="row"> 
	

	<div class="col-xs-12">
		<div class="imgwrapper">	
			<img src="graph-monthly-evu.php?thedate=<?php echo $monthdate ?>"
			alt="" class="center-block img-responsive" />
		</div>
	</div>

</div>
<div class="row"> 
	

	<div class="col-xs-12">
		<div class="imgwrapper">	
			<img src="graph-monthly-pv.php?thedate=<?php echo $monthdate ?>"
			alt="" class="center-block img-responsive" />
		</div>
	</div>

</div>
<div class="row"> 
	

	<div class="col-xs-12">
		<div class="imgwrapper">	
			<img src="graph-monthly-ev.php?thedate=<?php echo $monthdate ?>"
			alt="" class="center-block img-responsive" />
		</div>
	</div>

</div>


<div class="row"> 
	

	<div class="col-xs-12">
		<div class="imgwrapper">	
			<img src="graph-monthly.php?thedate=<?php echo $monthdate ?>"
			alt="" class="center-block img-responsive" />
		</div>
	</div>

</div>

<br><br>

<form name="monthlydate" id="monthlydate" action="monthly.php" method="GET">
<div class="row col-xs-12">
	<div class="col-xs-2">
	</div>
	<div class="col-xs-8 block-center text-center .text-align:center">
<?php $monthdate = date("Y-m", strtotime($monthdate)); ?>
<input id="date" name="date" type="month" min="2018-01" value="<?php print $monthdate ?>" required="required" />
	 	
	</div>	
	<div class="col-xs-2">
	</div>
</div>
<div class="row"><br></div><br>
<div class="row col-xs-12">
	<div class="col-xs-4">
	</div>
	<div class="col-xs-4 block-center text-center .text-align:center">
<button type="submit">Go</button>
	 	
	</div>	
	<div class="col-xs-4">
	</div>
</div>






</div>
</section>
</body>
</html>
