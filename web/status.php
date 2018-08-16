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


<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llkombiniert",
	        complete: function(request){
		        $("#lldiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/bezuga1",
	        complete: function(request){
		        $("#bezuga1div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/bezuga2",
	        complete: function(request){
		        $("#bezuga2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/bezuga3",
	        complete: function(request){
		        $("#bezuga3div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llsoll",
	        complete: function(request){
		        $("#llsolldiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llsolls1",
	        complete: function(request){
		        $("#llsolls1div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llsolls2",
	        complete: function(request){
		        $("#llsolls2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llas11",
	        complete: function(request){
		        $("#llas11div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llas12",
	        complete: function(request){
		        $("#llas12div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llas13",
	        complete: function(request){
		        $("#llas13div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llas21",
	        complete: function(request){
		        $("#llas21div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llas22",
	        complete: function(request){
		        $("#llas22div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llas23",
	        complete: function(request){
		        $("#llas23div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/lla1",
	        complete: function(request){
		        $("#lla1div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/lla2",
	        complete: function(request){
		        $("#lla2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/lla3",
	        complete: function(request){
		        $("#lla3div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llaktuell",
	        complete: function(request){
		        $("#llaktuelldiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llaktuells1",
	        complete: function(request){
		        $("#llaktuells1div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llaktuells2",
	        complete: function(request){
		        $("#llaktuells2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llkwh",
	        complete: function(request){
		        $("#llkwhdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llkwhs1",
	        complete: function(request){
		        $("#llkwhs1div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llkwhs2",
	        complete: function(request){
		        $("#llkwhs2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llkwhges",
	        complete: function(request){
		        $("#llkwhgesdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/pvcounter",
	        complete: function(request){
		        $("#pvcounterdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/pvkwhk",
	        complete: function(request){
		        $("#pvkwhdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/pvwatt",
	        complete: function(request){
		        $("#pvwattdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/wattbezug",
	        complete: function(request){
		        $("#wattbezugdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>


<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajaxSetup({ cache: false});
	$.ajax({
		url: "/openWB/ramdisk/soc",
	        complete: function(request){
		        $("#soclevel").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/soc1",
	        complete: function(request){
		        $("#soclevel1").html(request.responseText);
		}
	});

}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llv1",
	        complete: function(request){
		        $("#llv1div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llv2",
	        complete: function(request){
		        $("#llv2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llv3",
	        complete: function(request){
		        $("#llv3div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llvs11",
	        complete: function(request){
		        $("#llv1s1div").html(request.responseText);
		}
});
	$.ajax({
		url: "/openWB/ramdisk/llvs21",
	        complete: function(request){
		        $("#llv1s2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llvs12",
	        complete: function(request){
		        $("#llv2s1div").html(request.responseText);
		}
});
	$.ajax({
		url: "/openWB/ramdisk/llvs22",
	        complete: function(request){
		        $("#llv2s2div").html(request.responseText);
		}
	});

}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llvs13",
	        complete: function(request){
		        $("#llv3s1div").html(request.responseText);
		}
});
	$.ajax({
		url: "/openWB/ramdisk/llvs23",
	        complete: function(request){
		        $("#llv3s2div").html(request.responseText);
		}
	});

}
doInterval = setInterval(getfile, 2000);
</script>



<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llpf1",
	        complete: function(request){
		        $("#llpf1div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llpf2",
	        complete: function(request){
		        $("#llpf2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llpf3",
	        complete: function(request){
		        $("#llpf3div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>


<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/evuv1",
	        complete: function(request){
		        $("#evuv1div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/evuv2",
	        complete: function(request){
		        $("#evuv2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/evuv3",
	        complete: function(request){
		        $("#evuv3div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/evuhz",
	        complete: function(request){
		        $("#evuhzdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/evupf1",
	        complete: function(request){
		        $("#evupf1div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/evupf2",
	        complete: function(request){
		        $("#evupf2div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/evupf3",
	        complete: function(request){
		        $("#evupf3div").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>



<body>


	<div class="preloader">
		<img src="img/loader.gif" alt="Preloader image">
	</div>
<section id="services">
		<div class="container">
			<div class="row">
				<div class="col-xs-12 text-center">
					<h3> OpenWB Status </h3>
				</div>
			</div>
<br><br>	
<div class="row">
		<div class="col-xs-4 text-center">
		</div>
		<div class="col-xs-2 text-center">
			L1
		</div>
		<div class="col-xs-2 text-center">
			L2
		</div>
		<div class="col-xs-2 text-center">
			L3
		</div>

</div>
<hr>
<div class="row bg-warning">
	<div class="col-xs-4 text-center bg-warning">
		EVU Spannung in V
	</div>
	<div class="col-xs-2 text-center bg-warning">
		<div id="evuv1div"></div>
	</div>
	<div class="col-xs-2 text-center bg-warning">
		<div id="evuv2div"></div>
	</div>
	<div class="col-xs-2 text-center bg-warning">
		<div id="evuv3div"></div>
	</div>
</div>
<hr>
<div class="row bg-warning">
	<div class="col-xs-4 text-center bg-warning">
		EVU Power Faktor
	</div>
	<div class="col-xs-2 text-center bg-warning">
		<div id="evupf1div"></div>
	</div>
	<div class="col-xs-2 text-center bg-warning">
		<div id="evupf2div"></div>
	</div>
	<div class="col-xs-2 text-center bg-warning">
		<div id="evupf3div"></div>
	</div>
</div>
<hr>
<div class="row bg-warning">
	<div class="col-xs-4 text-center bg-warning">
		EVU Stromstaerke in A
	</div>
	<div class="col-xs-2 text-center bg-warning">
		<div id="bezuga1div"></div>
	</div>
	<div class="col-xs-2 text-center bg-warning">
		<div id="bezuga2div"></div>
	</div>
	<div class="col-xs-2 text-center bg-warning">
		<div id="bezuga3div"></div>
	</div>
</div>
<hr>
<div class="row bg-info">
	<div class="col-xs-4 text-center">
		Ladepunkt 1 Spannung in V
	</div>
	<div class="col-xs-2 text-center">
		<div id="llv1div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llv2div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llv3div"></div>
	</div>
</div>
<hr>
<div class="row bg-info">
	<div class="col-xs-4 text-center">
		Ladepunkt 1 Power Faktor
	</div>
	<div class="col-xs-2 text-center">
		<div id="llpf1div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llpf2div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llpf3div"></div>
	</div>
</div>
<hr>
<div class="row bg-info">
	<div class="col-xs-4 text-center">
		Ladepunkt 1 Stromstaerke in A
	</div>
	<div class="col-xs-2 text-center">
		<div id="lla1div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="lla2div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="lla3div"></div>
	</div>
</div>
<hr>
<div class="row bg-info">
	<div class="col-xs-4 text-center">
		Ladepunkt 2 Spannung in V
	</div>
	<div class="col-xs-2 text-center">
		<div id="llv1s1div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llv2s1div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llv3s1div"></div>
	</div>
</div>
<hr>
<div class="row bg-info">
	<div class="col-xs-4 text-center bg-info">
		Ladepunkt 2 Stromstaerke in A
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llas11div"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llas12div"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llas13div"></div>
	</div>
</div>
<hr>
<div class="row bg-info">
	<div class="col-xs-4 text-center">
		Ladepunkt 3 Spannung in V
	</div>
	<div class="col-xs-2 text-center">
		<div id="llv1s2div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llv2s2div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llv3s2div"></div>
	</div>
</div>
<hr>
<div class="row bg-info">
	<div class="col-xs-4 text-center bg-info">
		Ladepunkt 3 Stromstaerke in A
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llas21div"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llas22div"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llas23div"></div>
	</div>
</div>



<hr style="height:3px;background-color:#333;" />
<div class="row">
		<div class="col-xs-4 text-center">
		</div>
		<div class="col-xs-2 text-center">
			Ladepunkt 1
		</div>
		<div class="col-xs-2 text-center">
			Ladepunkt 2
		</div>
		<div class="col-xs-2 text-center">
			Ladepunkt 3
		</div>
		<div class="col-xs-2 text-center">
			Gesamt
		</div>
</div>
<hr>

<div class="row bg-info">
	<div class="col-xs-4 text-center">
		Ladestromvorgabe in A
	</div>
	<div class="col-xs-2 text-center">
		<div id="llsolldiv"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llsolls1div"></div>
	</div>
	<div class="col-xs-2 text-center">
		<div id="llsolls2div"></div>
	</div>
	<div class="col-xs-2 text-center">
	</div>


</div>
<hr>

<div class="row bg-info">
	<div class="col-xs-4 text-center bg-info">
		Ladeleistung in Watt
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llaktuelldiv"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llaktuells1div"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llaktuells2div"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
	<div id="lldiv"></div>
	</div>

</div>
<hr>
<div class="row bg-info">
	<div class="col-xs-4 text-center bg-info">
		Zählerstand in kWh
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llkwhdiv"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llkwhs1div"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llkwhs2div"></div>
	</div>
	<div class="col-xs-2 text-center bg-info">
		<div id="llkwhgesdiv"></div>
	</div>

</div>
<hr style="height:3px;border:none;color:#333;background-color:#333;" />

<div class="row bg-success">
		<div class="col-xs-2 text-center">
		PV Counter
		</div>
		<div class="col-xs-2 text-center">
			<div id="pvcounterdiv"></div>
		</div>
		<div class="col-xs-2 text-center">
			PV Leistung in Watt
		</div>
		<div class="col-xs-2 text-center">
			<div id="pvwattdiv"></div>
		</div>
		<div class="col-xs-2 text-center">
			PV Zählerstand in kWh
		</div>
		<div class="col-xs-2 text-center">
			<div id="pvkwhdiv"></div>

		</div>
</div>
<hr>
<div class="row">
		<div class="col-xs-2 text-center bg-info">
		SoC LP1 in %
		</div>
		<div class="col-xs-2 text-center bg-info">
			<div id="soclevel"></div>
		</div>
		<div class="col-xs-2 text-center bg-warning">
			EVU in Watt
		</div>
		<div class="col-xs-2 text-center bg-warning">
			<div id="wattbezugdiv"></div>
		</div>
		<div class="col-xs-2 text-center bg-warning">
			EVU in Hz
		</div>
		<div class="col-xs-2 text-center bg-warning">
			<div id="evuhzdiv"></div>

		</div>
</div>
<div class="row">
	<div class="col-xs-2 text-center bg-info">
		SoC LP2 in %
		</div>
		<div class="col-xs-2 text-center bg-info">
			<div id="soclevel1"></div>
		</div>

</div>
<hr style="height:3px;border:none;color:#333;background-color:#333;" />





<?php
echo "
</textarea> 
	</td><td width='50%'></b>
	<br>	Uptime: <span id='uptime'>--</span>
	<br>OS: ";
echo exec('uname -ors');
echo "<br>System: ";
echo exec('uname -nmi');
echo exec("cat /proc/cpuinfo | grep 'Processor' | head -n 1");
echo "
<meter id='cpu' high=85 min=0 max=100></meter> <span id='cpuuse'>--</span>%
	<br>Memory: <span id='memtot'>--</span>MB
	<meter id='mem' min='0'></meter>  <font size='-1'>(<span id='memfree'>--</span>MB free)</font>
	<br>Disk Usage: <span id='diskuse'>--</span>, <span id='diskfree'>--</span> avail.
	</td></tr>
	</table>";
?>
<script type='text/javascript'>
  function updateit() {

  $.getJSON('tools/programmloggerinfo.php', function(data){
  json = eval(data);
  document.getElementById('cpu').value= json.cpuuse;
  document.getElementById('uptime').innerHTML = json.uptime;
  document.getElementById('cpuuse').innerHTML = json.cpuuse;
  document.getElementById('memtot').innerHTML = json.memtot;
  document.getElementById('mem').max= json.memtot;
  document.getElementById('mem').value= json.memuse;
  document.getElementById('mem').high = (json.memtot*0.85);
  document.getElementById('memfree').innerHTML = json.memfree;
  document.getElementById('diskuse').innerHTML = json.diskuse;
  document.getElementById('diskfree').innerHTML = json.diskfree;
  })
  }
  $(document).ready(function() {
  updateit();
  setInterval(updateit, 1000);
  })  
</script> 

<br><br>
 <button onclick="window.location.href='./index.php'" class="btn btn-primary btn-blue">Zurück</button>
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
