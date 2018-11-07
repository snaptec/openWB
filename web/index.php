<!DOCTYPE html>
<html lang="en">

<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB</title>
	<meta name="description" content="OpenWB" />
	<meta name="keywords" content="OpenWB" />
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
<script src="live.js"></script>

<?php
	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		if(strpos($line, "minimalstromstaerke=") !== false) {
			list(, $minimalstromstaerkeold) = explode("=", $line);
		}
		if(strpos($line, "maximalstromstaerke=") !== false) {
			list(, $maximalstromstaerkeold) = explode("=", $line);
		}
		if(strpos($line, "sofortll=") !== false) {
			list(, $sofortllold) = explode("=", $line);
		}
		if(strpos($line, "sofortlls1=") !== false) {
			list(, $sofortlls1old) = explode("=", $line);
		}
		if(strpos($line, "sofortlls2=") !== false) {
			list(, $sofortlls2old) = explode("=", $line);
		}
		if(strpos($line, "lastmanagement=") !== false) {
			list(, $lastmanagementold) = explode("=", $line);
		}
		if(strpos($line, "lastmanagements2=") !== false) {
			list(, $lastmanagements2old) = explode("=", $line);
		}
		if(strpos($line, "lademstat=") !== false) {
			list(, $lademstatold) = explode("=", $line);
		}
		if(strpos($line, "lademstats1=") !== false) {
			list(, $lademstats1old) = explode("=", $line);
		}
		if(strpos($line, "lademkwh=") !== false) {
			list(, $lademkwhold) = explode("=", $line);
		}
		if(strpos($line, "lademkwhs1=") !== false) {
			list(, $lademkwhs1old) = explode("=", $line);
		}
		if(strpos($line, "lademstats2=") !== false) {
			list(, $lademstats2old) = explode("=", $line);
		}
		if(strpos($line, "lademkwhs2=") !== false) {
			list(, $lademkwhs2old) = explode("=", $line);
		}
		if(strpos($line, "sofortsoclp1=") !== false) {
			list(, $sofortsoclp1old) = explode("=", $line);
		}
		if(strpos($line, "sofortsoclp2=") !== false) {
			list(, $sofortsoclp2old) = explode("=", $line);
		}
		if(strpos($line, "sofortsoclp3=") !== false) {
			list(, $sofortsoclp3old) = explode("=", $line);
		}
		if(strpos($line, "sofortsocstatlp1=") !== false) {
			list(, $sofortsocstatlp1old) = explode("=", $line);
		}
		if(strpos($line, "sofortsocstatlp2=") !== false) {
			list(, $sofortsocstatlp2old) = explode("=", $line);
		}
		if(strpos($line, "sofortsocstatlp3=") !== false) {
			list(, $sofortsocstatlp3old) = explode("=", $line);
		}
		if(strpos($line, "msmoduslp1=") !== false) {
			list(, $msmoduslp1old) = explode("=", $line);
		}
		if(strpos($line, "msmoduslp2=") !== false) {
			list(, $msmoduslp2old) = explode("=", $line);
		}
		if(strpos($line, "speichermodul=") !== false) {
			list(, $speicherstatold) = explode("=", $line);
		}
	}
	$lademodusold = file_get_contents('/var/www/html/openWB/ramdisk/lademodus');
?>	

<body>


	<div class="preloader">
		<img src="img/loader.gif" alt="Preloader image">
	</div>
	
	<section id="services">
		<div class="container">
			<div class="row">
				<div class="col-xs-12 text-center">
				<h3> OpenWB Charge Controller </h3>
				</div>
			</div>
			<div class="row"><div class="col-xs-12 text-center">
				<div class="col-xs-6 text-center bg-success" style="font-size: 2vw">
					PV: <span id="pvdiv"></span>Watt 
				</div>
				<div class="col-xs-6 text-center bg-warning" style="font-size: 2vw">
					EVU: <span id="bezugdiv"></span>Watt 
				</div>

			</div></div>
			<div id="speicherstatdiv">
			<div class="row"><div class="col-xs-12 text-center">
				<div class="col-xs-4 text-center bg-info" style="font-size: 2vw">
					Speicher: 
				</div>
				<div class="col-xs-4 text-center bg-info" style="font-size: 2vw">
					<span id="speichersocdiv"></span> % SoC 
				</div>
				<div class="col-xs-4 text-center bg-info" style="font-size: 2vw">
					 <span id="speicherleistungdiv"></span>Watt 
				</div>

			</div></div>
			</div>
			<br>
			<div class="row"><div class="col-xs-6 text-center">
				<div class="imgwrapper">	
				<img id="livegraph" src="graph-live.php"
     				alt="Graph" class="img-responsive" />
				</div>
				</div>	
				<div class="col-xs-6 text-center bg-primary" style="font-size: 2vw">
					LP1: <span id="lldiv"></span>Watt, <span id="llsolldiv"></span>A <br>
					<span id="lp2lldiv">LP2: <span id="lllp2div"></span>Watt,  <span id="llsolllp2div"></span>A <br></span>
<span id="lp3lldiv">LP3: <span id="lllp3div"></span>Watt, <span id="llsolllp3div"></span>A<br></span> 
	<span id="gesamtlldiv">Gesamt: <span id="gesamtllwdiv"></span> Watt<br> </span>
	SoC: <span id="soclevel"></span>% 



				
				</div>

			</div><br>
			


			<hr>

			<div class="row">
	
			</div>



			
			<div class="col-xs-12 text-center">
				<h5>Lademodus</h5>
			</div>	
                        <div class="row">
                                <div class="col-xs-6 text-center">
					<div class="actstat">
						<a href="./tools/changelademodus.php?jetzt=1" class="btn btn-lg btn-block" style="font-size: 2vw">Sofort Laden</a>
					</div>
                           	</div>
                                <div class="col-xs-6 text-center">
                                        <div class="actstat1">
                                                <a href="./tools/changelademodus.php?minundpv=1" class="btn btn-lg btn-block" style="font-size: 2vw">Min + PV</a>
                                        </div>
				</div>
			</div>
			<div class="row" style="font-size: 2vw">
				<div class="col-xs-6 text-center">
					<div class="actstat3">
						<a href="./tools/changelademodus.php?stop=1" class="btn btn-lg btn-block" style="font-size: 2vw">Stop</a>
					</div>
				</div>
				<div class="col-xs-6 text-center">
                                        <div class="actstat2">
					        <a href="./tools/changelademodus.php?pvuberschuss=1" class="btn btn-lg btn-block" style="font-size: 2vw">Nur PV</a>
                                        </div>
				</div>
			</div>
			<div class="row">
			<hr>
			<div class="row">
				<div class="col-xs-12 text-center">
					<h5>Aktuelle / Letzte Ladung</h5>
				</div>
			</div>
			<div class="row" style="font-size: 2vw">
				<div class="col-xs-4 text-center" style="font-size: 2vw">
					Ladepunkt 1
				</div>
				<div  id="ladepunkts11div" class="col-xs-4 text-center">
					Ladepunkt 2
				</div>
				<div id="ladepunkts22div" class="col-xs-4 text-center">
					Ladepunkt 3
				</div>
			</div>
			<div class="row" style="font-size: 2vw">
				<div class="col-xs-4 text-center">
					<span id="gelrlp1div"></span>km
				</div>
				<div id="ladepunkts111div" class="col-xs-4 text-center">
					<span id="gelrlp2div"></span>km
				</div>
				<div id="ladepunkts222div" class="col-xs-4 text-center">
					<span id="gelrlp3div"></span>km
				</div>
			</div>
			<div class="row" style="font-size: 2vw">
				<div class="col-xs-4 text-center">
					<span id="aktgeladendiv"></span>kWh
				</div>
				<div id="ladepunkts1111div" class="col-xs-4 text-center">
					<span id="aktgeladens1div"></span>kWh
				</div>
				<div id="ladepunkts2222div" class="col-xs-4 text-center">
					<span id="aktgeladens2div"></span>kWh
				</div>
			</div>
			<div class="row" id="sofortlmdiv2" style="font-size: 2vw">
				<div class="col-xs-4 text-center">
					<div id="lademstatdiv">
					<progress id="prog1" value= "0" max=<?php echo $lademkwhold ?>></progress>
					</div>
				</div>
				<div id="ladepunkts11111div" class="col-xs-4 text-center">
					<div id="lademstats1div">
						<progress id="progs1" value= "0" max=<?php echo $lademkwhs1old ?>></progress>
					</div>	
				</div>
				<div id="ladepunkts22222div" class="col-xs-4 text-center">
					<div id="lademstats2div">
						<progress id="progs2" value= "0" max=<?php echo $lademkwhs2old ?>></progress>
					</div>
				</div>
			</div>
			<div class="row" id="sofortlmdiv1" style="font-size: 2vw">
				<div class="col-xs-4 text-center">
					<div id="lademstat1div">
					Restzeit <span id="restzeitlp1div"></span> 
					</div>
				</div>
				<div id="ladepunkts1111111div" class="col-xs-4 text-center">
					<div id="lademstats1div1">
					Restzeit <span id="restzeitlp2div"></span> 
					</div>	
				</div>
				<div id="ladepunkts2222222div" class="col-xs-4 text-center">
					<div id="lademstats2div1">
					Restzeit <span id="restzeitlp3div"></span> 
					</div>
				</div>
			</div>

				
			<hr>
			</div>
			<div id="sofortlmdiv">
			<form name="sofortll" action="./tools/sofortll.php" method="POST">
			<div class="row">
				<div class="col-xs-12 text-center">
					<div class="col-xs-4 text-center" style="font-size: 2vw">
						<label for="msmoduslp1">LP1</label>

						<select type="text" name="msmoduslp1" id="msmoduslp1">
						<option <?php if($msmoduslp1old == 0) echo 'selected' ?> value="0">Aus</option>
						<option <?php if($msmoduslp1old == 1) echo 'selected' ?> value="1">Lademenge</option>
						<option <?php if($msmoduslp1old == 2) echo 'selected' ?> value="2">SoC</option>
						</select> 



					<span id="msmodusmlp1">
						<br><br>
						<label for="lademlp1">Lademenge</label>
						<select type="text" name="lademlp1" id="lademlp1">
						<option <?php if($lademkwhold == 2) echo 'selected' ?> value="2">2</option>
						<option <?php if($lademkwhold == 4) echo 'selected' ?> value="4">4</option>
						<option <?php if($lademkwhold == 6) echo 'selected' ?> value="6">6</option>
						<option <?php if($lademkwhold == 8) echo 'selected' ?> value="8">8</option>					
						<option <?php if($lademkwhold == 10) echo 'selected' ?> value="10">10</option>
						<option <?php if($lademkwhold == 12) echo 'selected' ?> value="12">12</option>
						<option <?php if($lademkwhold == 14) echo 'selected' ?> value="14">14</option>
						<option <?php if($lademkwhold == 16) echo 'selected' ?> value="16">16</option>
						<option <?php if($lademkwhold == 18) echo 'selected' ?> value="18">18</option>
						<option <?php if($lademkwhold == 20) echo 'selected' ?> value="20">20</option>
						<option <?php if($lademkwhold == 25) echo 'selected' ?> value="25">25</option>
						<option <?php if($lademkwhold == 30) echo 'selected' ?> value="30">30</option>
						<option <?php if($lademkwhold == 35) echo 'selected' ?> value="35">35</option>
						<option <?php if($lademkwhold == 40) echo 'selected' ?> value="40">40</option>
						<option <?php if($lademkwhold == 45) echo 'selected' ?> value="45">45</option>
						<option <?php if($lademkwhold == 50) echo 'selected' ?> value="50">50</option>
						<option <?php if($lademkwhold == 55) echo 'selected' ?> value="55">55</option>
						<option <?php if($lademkwhold == 60) echo 'selected' ?> value="60">60</option>
						<option <?php if($lademkwhold == 65) echo 'selected' ?> value="65">65</option>
						<option <?php if($lademkwhold == 70) echo 'selected' ?> value="70">70</option>
						</select> kWh
							<br><br>
							<button><a href="./tools/resetlp1ladem.php">Reset</a></button> 
						
					</span>
					<span id="msmodusslp1"><br><br>
						<label for="sofortsoclp1">SoC</label>
						<select type="text" name="sofortsoclp1" id="sofortsoclp1">
						<option <?php if($sofortsoclp1old == 10) echo 'selected' ?> value="10">10</option>
						<option <?php if($sofortsoclp1old == 15) echo 'selected' ?> value="15">15</option>
						<option <?php if($sofortsoclp1old == 20) echo 'selected' ?> value="20">20</option>
						<option <?php if($sofortsoclp1old == 30) echo 'selected' ?> value="30">30</option>
						<option <?php if($sofortsoclp1old == 40) echo 'selected' ?> value="40">40</option>
						<option <?php if($sofortsoclp1old == 45) echo 'selected' ?> value="45">45</option>
						<option <?php if($sofortsoclp1old == 50) echo 'selected' ?> value="50">50</option>
						<option <?php if($sofortsoclp1old == 55) echo 'selected' ?> value="55">55</option>
						<option <?php if($sofortsoclp1old == 60) echo 'selected' ?> value="60">60</option>
						<option <?php if($sofortsoclp1old == 65) echo 'selected' ?> value="65">65</option>
						<option <?php if($sofortsoclp1old == 70) echo 'selected' ?> value="70">70</option>
						<option <?php if($sofortsoclp1old == 75) echo 'selected' ?> value="75">75</option>
						<option <?php if($sofortsoclp1old == 80) echo 'selected' ?> value="80">80</option>
						<option <?php if($sofortsoclp1old == 85) echo 'selected' ?> value="85">85</option>
						<option <?php if($sofortsoclp1old == 90) echo 'selected' ?> value="90">90</option>
						<option <?php if($sofortsoclp1old == 95) echo 'selected' ?> value="95">95</option>
						</select> %
						
					</span>
					<span id="msmodusnlp1">
					<br><br>
					</span>
				</div>
			
			<span id="ladepunkts111111div">
			<div class="col-xs-4 text-center" style="font-size: 2vw">
						<label for="msmoduslp2">LP2</label>

						<select type="text" name="msmoduslp2" id="msmoduslp2">
						<option <?php if($msmoduslp2old == 0) echo 'selected' ?> value="0">Aus</option>
						<option <?php if($msmoduslp2old == 1) echo 'selected' ?> value="1">Lademenge</option>
						<option <?php if($msmoduslp2old == 2) echo 'selected' ?> value="2">SoC</option>
						</select> 


					
					<span id="msmodusnlp2">
					<br><br>
					</span>
					<span id="msmodusmlp2">

						<br><br>
						<label for="lademlp2">Lademenge</label>
						<select type="text" name="lademlp2" id="lademlp2">
						<option <?php if($lademkwhs1old == 2) echo 'selected' ?> value="2">2</option>
						<option <?php if($lademkwhs1old == 4) echo 'selected' ?> value="4">4</option>
						<option <?php if($lademkwhs1old == 6) echo 'selected' ?> value="6">6</option>
						<option <?php if($lademkwhs1old == 8) echo 'selected' ?> value="8">8</option>					
						<option <?php if($lademkwhs1old == 10) echo 'selected' ?> value="10">10</option>
						<option <?php if($lademkwhs1old == 12) echo 'selected' ?> value="12">12</option>
						<option <?php if($lademkwhs1old == 14) echo 'selected' ?> value="14">14</option>
						<option <?php if($lademkwhs1old == 16) echo 'selected' ?> value="16">16</option>
						<option <?php if($lademkwhs1old == 18) echo 'selected' ?> value="18">18</option>
						<option <?php if($lademkwhs1old == 20) echo 'selected' ?> value="20">20</option>
						<option <?php if($lademkwhs1old == 25) echo 'selected' ?> value="25">25</option>
						<option <?php if($lademkwhs1old == 30) echo 'selected' ?> value="30">30</option>
						<option <?php if($lademkwhs1old == 35) echo 'selected' ?> value="35">35</option>
						<option <?php if($lademkwhs1old == 40) echo 'selected' ?> value="40">40</option>
						<option <?php if($lademkwhs1old == 45) echo 'selected' ?> value="45">45</option>
						<option <?php if($lademkwhs1old == 50) echo 'selected' ?> value="50">50</option>
						<option <?php if($lademkwhs1old == 55) echo 'selected' ?> value="55">55</option>
						<option <?php if($lademkwhs1old == 60) echo 'selected' ?> value="60">60</option>
						<option <?php if($lademkwhs1old == 65) echo 'selected' ?> value="65">65</option>
						<option <?php if($lademkwhs1old == 70) echo 'selected' ?> value="70">70</option>
						</select> kWh
						
							<br><br>
							<button><a href="./tools/resetlp2ladem.php">Reset</a></button> 
						
					</span>
					<span id="msmodusslp2"><br><br>
						<label for="sofortsoclp1">SoC</label>
						<select type="text" name="sofortsoclp2" id="sofortsoclp2">
						<option <?php if($sofortsoclp2old == 10) echo 'selected' ?> value="10">10</option>
						<option <?php if($sofortsoclp2old == 15) echo 'selected' ?> value="15">15</option>
						<option <?php if($sofortsoclp2old == 20) echo 'selected' ?> value="20">20</option>
						<option <?php if($sofortsoclp2old == 30) echo 'selected' ?> value="30">30</option>
						<option <?php if($sofortsoclp2old == 40) echo 'selected' ?> value="40">40</option>
						<option <?php if($sofortsoclp2old == 45) echo 'selected' ?> value="45">45</option>
						<option <?php if($sofortsoclp2old == 50) echo 'selected' ?> value="50">50</option>
						<option <?php if($sofortsoclp2old == 55) echo 'selected' ?> value="55">55</option>
						<option <?php if($sofortsoclp2old == 60) echo 'selected' ?> value="60">60</option>
						<option <?php if($sofortsoclp2old == 65) echo 'selected' ?> value="65">65</option>
						<option <?php if($sofortsoclp2old == 70) echo 'selected' ?> value="70">70</option>
						<option <?php if($sofortsoclp2old == 75) echo 'selected' ?> value="75">75</option>
						<option <?php if($sofortsoclp2old == 80) echo 'selected' ?> value="80">80</option>
						<option <?php if($sofortsoclp2old == 85) echo 'selected' ?> value="85">85</option>
						<option <?php if($sofortsoclp2old == 90) echo 'selected' ?> value="90">90</option>
						<option <?php if($sofortsoclp2old == 95) echo 'selected' ?> value="95">95</option>
						</select> %
				
						


					</span>
				</div>
			
		
			
			<span id="ladepunkts222222div">
					<div class="col-xs-4 text-center" style="font-size: 2vw">
			
						<label for="lademstats2">LP3</label>

						<select type="text" name="lademlp3check" id="lademlp3check">
						<option <?php if($lademstats2old == 0) echo 'selected' ?> value="0">Aus</option>
						<option <?php if($lademstats2old == 1) echo 'selected' ?> value="1">Lademenge</option>
						</select> 


					<span id="msmodusnlp3"></span>
					<span id="msmodusmlp3">
					<br><br>
					<label for="lademlp3">Lademenge</label>
					<select type="text" name="lademlp3" id="lademlp3">
					<option <?php if($lademkwhs2old == 2) echo 'selected' ?> value="2">2</option>
					<option <?php if($lademkwhs2old == 4) echo 'selected' ?> value="4">4</option>
					<option <?php if($lademkwhs2old == 6) echo 'selected' ?> value="6">6</option>
					<option <?php if($lademkwhs2old == 8) echo 'selected' ?> value="8">8</option>					
					<option <?php if($lademkwhs2old == 10) echo 'selected' ?> value="10">10</option>
					<option <?php if($lademkwhs2old == 12) echo 'selected' ?> value="12">12</option>
					<option <?php if($lademkwhs2old == 14) echo 'selected' ?> value="14">14</option>
					<option <?php if($lademkwhs2old == 16) echo 'selected' ?> value="16">16</option>
					<option <?php if($lademkwhs2old == 18) echo 'selected' ?> value="18">18</option>
					<option <?php if($lademkwhs2old == 20) echo 'selected' ?> value="20">20</option>
					<option <?php if($lademkwhs2old == 25) echo 'selected' ?> value="25">25</option>
					<option <?php if($lademkwhs2old == 30) echo 'selected' ?> value="30">30</option>
					<option <?php if($lademkwhs2old == 35) echo 'selected' ?> value="35">35</option>
					<option <?php if($lademkwhs2old == 40) echo 'selected' ?> value="40">40</option>
					<option <?php if($lademkwhs2old == 45) echo 'selected' ?> value="45">45</option>
					<option <?php if($lademkwhs2old == 50) echo 'selected' ?> value="50">50</option>
					<option <?php if($lademkwhs2old == 55) echo 'selected' ?> value="55">55</option>
					<option <?php if($lademkwhs2old == 60) echo 'selected' ?> value="60">60</option>
					<option <?php if($lademkwhs2old == 65) echo 'selected' ?> value="65">65</option>
					<option <?php if($lademkwhs2old == 70) echo 'selected' ?> value="70">70</option>
					</select> kWh
					<br><br>
						<button><a href="./tools/resetlp3ladem.php">Reset</a></button> 
				</span>	
				</span>			
			</div>

			</div>
			</div>



			<div class="row">
				<div class="col-xs-12 text-center"> 
						<div class="col-xs-12 text-center">
							<div class="col-xs-12 tex-center"><hr>
								<h5>Sofortladen Stromstärke</h5><br><br>

							</div>
							<div class="col-xs-8 text-center">
								<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortll" id="sofortll" value=<?php echo $sofortllold ?>>
							</div>
							<div class="col-xs-4 text-center">
								<label for="sofortll">Ladepunkt 1: <span id="sofortlll"></span>A</label>
							</div>
							<script>
								var slider = document.getElementById("sofortll");
								var output = document.getElementById("sofortlll");
								output.innerHTML = slider.value;
								slider.oninput = function() {
								  output.innerHTML = this.value;
								}
							</script>
						</div>
						<div id="ladepunkts1ndiv">
						<br>
						</div>
						<div id="ladepunkts1div">
						<br>
						<div class="col-xs-12 text-center">
							<div class="col-xs-8 text-center">
								<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlls1" id="sofortlls1" value=<?php echo $sofortlls1old ?>>
							</div>
							<div class="col-xs-4 text-center">
								<label for="sofortlls1">Ladepunkt 2: <span id="sofortllls1"></span>A</label>
							</div>
							<script>
								var sliders1 = document.getElementById("sofortlls1");
								var outputs1 = document.getElementById("sofortllls1");
								outputs1.innerHTML = sliders1.value;
								sliders1.oninput = function() {
								  outputs1.innerHTML = this.value;
								}
							</script>
						</div>
						</div>
						<div id="ladepunkts2ndiv">
						<br>
						</div>
						<div id="ladepunkts2div">
						<br>
						<div class="col-xs-12 text-center">
							<div class="col-xs-8 text-center">
								<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortlls2" id="sofortlls2" value=<?php echo $sofortlls2old ?>>
							</div>
							<div class="col-xs-4 text-center">
								<label for="sofortlls2">Ladepunkt 3: <span id="sofortllls2"></span>A</label>
							</div>
							<script>
								var sliders2 = document.getElementById("sofortlls2");
								var outputs2 = document.getElementById("sofortllls2");
								outputs2.innerHTML = sliders2.value;
								sliders2.oninput = function() {
								  outputs2.innerHTML = this.value;
								}
							</script>
							<br>
						</div>
						</div>
						<div class="col-xs-12 text-center"><br><br>
							<button type="submit" class="btn btn-primary btn-lg btn-block btn-grey">Save</button>	 
						</div>
						<br><br><br>
					 </form>


						<input hidden name="lastmanagement" id="lastmanagement" value="<?php echo $lastmanagementold ; ?>">
						<input hidden name="lastmanagements2" id="lastmanagements2" value="<?php echo $lastmanagements2old ; ?>">				
						<script>
						$(function() {
   						   if($('#lastmanagement').val() == '0') {
							$('#ladepunkts1ndiv').show(); 
							$('#ladepunkts1div').hide();
							$('#ladepunkts11div').hide();
							$('#ladepunkts111div').hide();
							$('#ladepunkts1111div').hide();
							$('#ladepunkts11111div').hide();
							$('#ladepunkts111111div, #ladepunkts1111111div, #lp2lldiv, #gesamtlldiv').hide();
						      } else {
							$('#ladepunkts1ndiv').hide();
							$('#ladepunkts1div').show();
							$('#ladepunkts11div').show();
							$('#ladepunkts111div').show();	
							$('#ladepunkts1111div').show();
							$('#ladepunkts11111div').show();
							$('#ladepunkts111111div, #ladepunkts1111111div, #lp2lldiv, #gesamtlldiv').show();
						      } 

						});
						</script>
						<script>
						$(function() {
   						   if($('#lastmanagements2').val() == '0') {
							$('#ladepunkts2ndiv').show(); 
							$('#ladepunkts2div').hide();
							$('#ladepunkts22div').hide();
							$('#ladepunkts222div').hide();
							$('#ladepunkts2222div').hide();
							$('#ladepunkts22222div').hide();
							$('#ladepunkts222222div, #ladepunkts2222222div, #lp3lldiv').hide();
						      } else {
							$('#ladepunkts2ndiv').hide();
							$('#ladepunkts2div').show();
							$('#ladepunkts22div').show();	
							$('#ladepunkts222div').show();	
							$('#ladepunkts2222div').show();	
							$('#ladepunkts22222div').show();
							$('#ladepunkts222222div, #ladepunkts2222222div, #lp3lldiv').show();	
						      } 

						});
						</script>
						<input hidden name="speicherstat" id="speicherstat" value="<?php echo $speicherstatold ; ?>">
						<script>
						$(function() {
   						   if($('#speicherstat').val() == 'none') {
							$('#speicherstatdiv').hide();
						      } else {
							$('#speicherstatdiv').show();

						      } 

						});
						</script>
						<input hidden name="lademlp1stat" id="lademlp1stat" value="<?php echo $lademstatold ; ?>">
						<script>
						$(function() {
   						   if($('#lademlp1stat').val() == '1') {
							$('#lademstatdiv').show();
							$('#lademstat1div').show(); 
						      } else {
							$('#lademstatdiv').hide();
							$('#lademstat1div').hide();

						      } 

						});
						</script>
						<input hidden name="lademlp2stat" id="lademlp2stat" value="<?php echo $lademstats1old ; ?>">
						<script>
						$(function() {
   						   if($('#lademlp2stat').val() == '1') {
							$('#lademstats1div, #lademstats1div1').show(); 
						      } else {
							$('#lademstats1div, #lademstats1div1').hide();
						      } 

						});
						</script>
						<input hidden name="lademlp3stat" id="lademlp3stat" value="<?php echo $lademstats2old ; ?>">
						<script>
						$(function() {
   						   if($('#lademlp3stat').val() == '1') {
							$('#lademstats2div, #lademstats2div1').show(); 
						      } else {
							$('#lademstats2div, #lademstats2div1').hide();
						      } 

						});
						</script>
				</div>
			</div> 
			<div class="row">
				<hr>
			</div>
			</div>		

	<!--	<div class="row">
				<iframe frameBorder="0" height="312" class="col-xs-12" src="/metern/index2.php"></iframe>
			</div> -->
			<div class="row">
				<div class="col-xs-4">
				<!-- master -->	Ver 0.99				</div>
				<div class="col-xs-4 text-center">
					<a href="http://openwb.de">www.openwb.de</a>

				</div>
				<div class="col-xs-4 text-right">
					<a href="settings.php">Einstellungen</a> 
				</div>
			</div>
			<div class="row">
				<div class="col-xs-4">
					<a href="ladelog.php">Ladelog</a>
				</div>

				<div class="col-xs-4 text-center">
					<a href="/metern/index.php">Logging</a>
				</div>
				<div class="col-xs-4 text-right">
					<a href="status.php">Status</a> 
				</div>

			</div>
			<div class="row">
				<div class="col-xs-4">
					<a href="ladelog.php"></a>
				</div>

				<div class="col-xs-4 text-center">
					<a href="hilfe.html">Hilfe</a>
				</div>
				<div class="col-xs-4 text-right">
					 <a href="logging/index.html">Logging (Beta)</a>
				</div>

		

			</div>	
					<br><br><br><br>
					</div>
	</section>
	<!-- Holder for mobile navigation -->
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
	<input hidden name="sofortlm" id="sofortlm" value="<?php echo $lademodusold ; ?>">
	<script>
	$(function() {
   	   if($('#sofortlm').val() == '0') {
		$('#sofortlmdiv, #sofortlmdiv1, #sofortlmdiv2').show(); 
	      } else {
		$('#sofortlmdiv, #sofortlmdiv1, #sofortlmdiv2').hide();
		      } 
		});
	</script>

	<script type='text/javascript'>
	loadText();
function loadText(){
 $.ajax({
  url:"./tools/lademodus.php",  
  type: "post", //request type,
  dataType: 'json',
  data: {call: "loadfile"},
  success:function(result){
   if(result.text == 0){
    $('.actstat .btn').addClass("btn-green");
    $('.actstat1 .btn').addClass("btn-red");
    $('.actstat2 .btn').addClass("btn-red");
    $('.actstat3 .btn').addClass("btn-red");
    $('.actstat3 .btn').removeClass("btn-green");
    $('.actstat1 .btn').removeClass("btn-green");
    $('.actstat2 .btn').removeClass("btn-green");
   }
   if(result.text == 1){
    $('.actstat1 .btn').addClass("btn-green");
    $('.actstat .btn').addClass("btn-red");    
    $('.actstat2 .btn').addClass("btn-red");
    $('.actstat3 .btn').addClass("btn-red");
    $('.actstat .btn').removeClass("btn-green");
    $('.actstat3 .btn').removeClass("btn-green");
    $('.actstat2 .btn').removeClass("btn-green");
    }
   if(result.text == 2){
    $('.actstat2 .btn').addClass("btn-green");
    $('.actstat .btn').addClass("btn-red");    
    $('.actstat1 .btn').addClass("btn-red");
    $('.actstat3 .btn').addClass("btn-red");
    $('.actstat .btn').removeClass("btn-green");
    $('.actstat3 .btn').removeClass("btn-green");
    $('.actstat1 .btn').removeClass("btn-green");    
}
     if(result.text == 3){
    $('.actstat2 .btn').addClass("btn-red");
    $('.actstat3 .btn').addClass("btn-green");
    $('.actstat .btn').addClass("btn-red");    
    $('.actstat1 .btn').addClass("btn-red");
    $('.actstat .btn').removeClass("btn-green");
    $('.actstat1 .btn').removeClass("btn-green");    
     }

  }
 });
}

</script>
<script>
$(function() {
      if($('#msmoduslp1').val() == '0') {
		$('#msmodusnlp1').show(); 
		$('#msmodusslp1').hide();
		$('#msmodusmlp1').hide();
      } 
     if($('#msmoduslp1').val() == '1') 
      {
		$('#msmodusnlp1').hide();
		$('#msmodusslp1').hide();
		$('#msmodusmlp1').show();
      } 
     if($('#msmoduslp1').val() == '2') 
      {
		$('#msmodusnlp1').hide();
		$('#msmodusslp1').show();
		$('#msmodusmlp1').hide();
      } 

	$('#msmoduslp1').change(function(){
      if($('#msmoduslp1').val() == '0') {
		$('#msmodusnlp1').show(); 
		$('#msmodusslp1').hide();
		$('#msmodusmlp1').hide();
      } 
     if($('#msmoduslp1').val() == '1') 
      {
		$('#msmodusnlp1').hide();
		$('#msmodusslp1').hide();
		$('#msmodusmlp1').show();
      } 
     if($('#msmoduslp1').val() == '2') 
      {
		$('#msmodusnlp1').hide();
		$('#msmodusslp1').show();
		$('#msmodusmlp1').hide();
      } 
	    });
});
</script>
<script>
$(function() {
      if($('#msmoduslp2').val() == '0') {
		$('#msmodusnlp2').show(); 
		$('#msmodusslp2').hide();
		$('#msmodusmlp2').hide();
      } 
     if($('#msmoduslp2').val() == '1') 
      {
		$('#msmodusnlp2').hide();
		$('#msmodusslp2').hide();
		$('#msmodusmlp2').show();
      } 
     if($('#msmoduslp2').val() == '2') 
      {
		$('#msmodusnlp2').hide();
		$('#msmodusslp2').show();
		$('#msmodusmlp2').hide();
      } 

	$('#msmoduslp2').change(function(){
      if($('#msmoduslp2').val() == '0') {
		$('#msmodusnlp2').show(); 
		$('#msmodusslp2').hide();
		$('#msmodusmlp2').hide();
      } 
     if($('#msmoduslp2').val() == '1') 
      {
		$('#msmodusnlp2').hide();
		$('#msmodusslp2').hide();
		$('#msmodusmlp2').show();
      } 
     if($('#msmoduslp2').val() == '2') 
      {
		$('#msmodusnlp2').hide();
		$('#msmodusslp2').show();
		$('#msmodusmlp2').hide();
      } 
	    });
});
</script>
<script>
$(function() {
      if($('#lademlp3check').val() == '0') {
		$('#msmodusnlp3').show(); 
		$('#msmodusmlp3').hide();
      } 
     if($('#lademlp3check').val() == '1') 
      {
		$('#msmodusnlp3').hide();
		$('#msmodusmlp3').show();
      } 
	$('#lademlp3check').change(function(){
      if($('#lademlp3check').val() == '0') {
		$('#msmodusnlp3').show(); 
		$('#msmodusmlp3').hide();
      } 
     if($('#lademlp3check').val() == '1') 
      {
		$('#msmodusnlp3').hide();
		$('#msmodusmlp3').show();
      } 
       
	    });
});
</script>



</body>

</html>



