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
		url: "/openWB/ramdisk/anzahlphasen",
	        complete: function(request){
		        $("#anzahlphasendiv").html(request.responseText);
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
		url: "/openWB/ramdisk/bezugkwh",
	        complete: function(request){
		        $("#bezugkwhdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/einspeisungkwh",
	        complete: function(request){
		        $("#einspeisungkwhdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/lademodus",
	        complete: function(request){
		        $("#lademodusdiv").html(request.responseText);
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
		url: "/openWB/ramdisk/pvkwh",
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
		url: "/openWB/ramdisk/llaltnv",
	        complete: function(request){
		        $("#llaltnvdiv").html(request.responseText);
		}
	});
}
doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
var doInterval;
function getfile() {
	$.ajax({
		url: "/openWB/ramdisk/llhz",
	        complete: function(request){
		        $("#llhzdiv").html(request.responseText);
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
	<div class="row">
				<div class="col-xs-6 text-center">		
		                	<button type="button" class="btn btn-primary btn-lg btn-block btn-orange"> EVU in Watt
                        			<div id="wattbezugdiv"></div>
					</button>
				</div>
	<div class="col-xs-6 text-center">
                                	<button type="button" class="btn btn-primary btn-lg btn-block btn-orange">Bezug Wh
					<div id="bezugkwhdiv"></div>
					</button>
				</div>
	</div>

	<div class="row">
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-orange">EVU Frequenz in Hz
                     			<div id="evuhzdiv"></div>
			</button>
		</div>
	<div class="col-xs-6 text-center">
                                	<button type="button" class="btn btn-primary btn-lg btn-block btn-orange">Einspeisung Wh
					<div id="einspeisungkwhdiv"></div>
					</button>
				</div>

	</div>
	<div class="row">
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-orange">Volt je Phase EVU
             			<div id="evuv1div"></div><div id="evuv2div"></div><div id="evuv3div"></div>
			</button>
		</div>
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-orange">Power Faktor je Phase EVU
             			<div id="evupf1div"></div><div id="evupf2div"></div><div id="evupf3div"></div>
			</button>
		</div>


	</div>
	<div class="row">
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-orange">Ampere je Phase Bezug
             			<div id="bezuga1div"></div><div id="bezuga2div"></div><div id="bezuga3div"></div>
			</button>
		</div>
	</div>
	<div class="row">
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Volt je Phase Ladepunkt 1
             			<div id="llv1div"></div><div id="llv2div"></div><div id="llv3div"></div>
			</button>
		</div>
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Power Faktor je Phase Ladepunkt 1
             			<div id="llpf1div"></div><div id="llpf2div"></div><div id="llpf3div"></div>
			</button>
		</div>


	</div>

	<div class="row">
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Durchschnittliche Phase zu Neutral Volt
                     			<div id="llaltnvdiv"></div>
			</button>
		</div>
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ladepunkt 1 Frequenz in Hz
                     			<div id="llhzdiv"></div>
			</button>
		</div>

	</div>


	<div class="row">
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ampere je Phase Ladepunkt 1
             			<div id="lla1div"></div><div id="lla2div"></div><div id="lla3div"></div>
			</button>
		</div>
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ampere je Phase Ladepunkt 2
             			<div id="llas11div"></div><div id="llas12div"></div><div id="llas13div"></div>
			</button>
		</div>


	</div>

	<div class="row">
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ladeleistung Punkt 1 in Watt
                     			<div id="llaktuelldiv"></div>
			</button>
		</div>
		<div class="col-xs-6 text-center">		
	               	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ladeleistung Punkt 2 in Watt
                     			<div id="llaktuells1div"></div>
			</button>
		</div>

	</div>
	<div class="row">
				<div class="col-xs-6 text-center">		
		                	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ladeleistung in Watt
                        			<div id="lldiv"></div>
					</button>
				</div>
	<div class="col-xs-6 text-center">
                                	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">SOC in %
					<div id="soclevel"></div>
					</button>
				</div>
	</div>
	<div class="row">
				<div class="col-xs-6 text-center">		
		                	<button type="button" class="btn btn-primary btn-lg btn-block btn-green">PVleistung in Watt
                        			<div id="pvwattdiv"></div>
					</button>
				</div>
	<div class="col-xs-6 text-center">
                                	<button type="button" class="btn btn-primary btn-lg btn-block btn-green">PV Wh
					<div id="pvkwhdiv"></div>
					</button>
				</div>
	</div>

<?php
echo "
</textarea> 
	</td><td width='50%'></b>
	<br><hr align=left size=1 width='90%'>
	Uptime: <span id='uptime'>--</span>
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
