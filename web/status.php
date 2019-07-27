<!DOCTYPE html>
<html lang="en">

<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<script src="js/core.js"></script>
	<script src="js/charts.js"></script>
	<script src="js/animated.js"></script>

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
		$.ajax({
			url: "/openWB/ramdisk/evsedintestlp1",
	    	complete: function(request){
		    	$("#evsedintestlp1div").html(request.responseText);
				}
		});
		$.ajax({
			url: "/openWB/ramdisk/evsedintestlp2",
	    	complete: function(request){
		    	$("#evsedintestlp2div").html(request.responseText);
				}
		});
		$.ajax({
			url: "/openWB/ramdisk/evsedintestlp3",
	    	complete: function(request){
		    	$("#evsedintestlp3div").html(request.responseText);
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
			url: "/openWB/ramdisk/bezugw1",
	    	complete: function(request){
					// zur Anzeige Wert um "Bezug"/"Einspeisung" ergänzen
					var value = parseInt(request.responseText);
					var valueStr = "";
					if(value<0) {
						value = value * -1;
						valueStr = valueStr+value+" (E)"
					} else if (value>0) {
						valueStr = valueStr+value+" (B)"
					} else  {
						// Bezug = 0
						valueStr = valueStr+value
					}
		    	$("#bezugw1div").html(valueStr);
				}
		});
	}
	doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
	var doInterval;
	function getfile() {
		$.ajax({
			url: "/openWB/ramdisk/bezugw2",
	    	complete: function(request){
					// zur Anzeige Wert um "Bezug"/"Einspeisung" ergänzen
					var value = parseInt(request.responseText);
					var valueStr = "";
					if(value<0) {
						value = value * -1;
						valueStr = valueStr+value+" (E)"
					} else if (value>0) {
						valueStr = valueStr+value+" (B)"
					} else  {
						// Bezug = 0
						valueStr = valueStr+value
					}
		    	$("#bezugw2div").html(valueStr);
				}
		});
	}
	doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
	var doInterval;
	function getfile() {
		$.ajax({
			url: "/openWB/ramdisk/bezugw3",
	    	complete: function(request){
					// zur Anzeige Wert um "Bezug"/"Einspeisung" ergänzen
					var value = parseInt(request.responseText);
					var valueStr = "";
					if(value<0) {
						value = value * -1;
						valueStr = valueStr+value+" (E)"
					} else if (value>0) {
						valueStr = valueStr+value+" (B)"
					} else  {
						// Bezug = 0
						valueStr = valueStr+value
					}
		    	$("#bezugw3div").html(valueStr);
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
			url: "/openWB/ramdisk/verbraucher1_watt",
	    	complete: function(request){
		    	$("#verbraucher1wattdiv").html(request.responseText);
				}
	});
		$.ajax({
			url: "/openWB/ramdisk/verbraucher1_wh",
				complete: function(request){

					var vfinal = request.responseText;
					vfinal = (vfinal / 1000).toFixed(3);
	
		    	$("#verbraucher1whdiv").html(vfinal);
				}
		});
		$.ajax({
			url: "/openWB/ramdisk/verbraucher1_whe",
				complete: function(request){

					var vefinal = request.responseText;
					vefinal = (vefinal / 1000).toFixed(3);
	
		    	$("#verbraucher1whediv").html(vefinal);

				}
		});
	}
	doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
	var doInterval;
	function getfile() {
		$.ajax({
			url: "/openWB/ramdisk/verbraucher2_watt",
	    	complete: function(request){
		    	$("#verbraucher2wattdiv").html(request.responseText);
				}
	});
		$.ajax({
			url: "/openWB/ramdisk/verbraucher2_wh",
				complete: function(request){

					var vfinal = request.responseText;
					vfinal = (vfinal / 1000).toFixed(3);
	
		    	$("#verbraucher2whdiv").html(vfinal);
				}
		});
		$.ajax({
			url: "/openWB/ramdisk/verbraucher2_whe",
				complete: function(request){

					var vefinal = request.responseText;
					vefinal = (vefinal / 1000).toFixed(3);
	
		    	$("#verbraucher2whediv").html(vefinal);

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
			url: "/openWB/ramdisk/einspeisungkwh",
				complete: function(request){
					var eefinal = request.responseText;
					eefinal = (eefinal / 1000).toFixed(3);
	
		    	$("#einspeisungkwhdiv").html(eefinal);
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
					var eifinal = request.responseText;
					eifinal = (eifinal / 1000).toFixed(3);
		    	$("#bezugkwhdiv").html(eifinal);
				}
		});
	}
	doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
	var doInterval;
	function getfile() {
		$.ajax({
			url: "/openWB/ramdisk/daily_pvkwhk",
	    	complete: function(request){
		    	$("#daily_pvkwhdiv").html(request.responseText);
				}
		});
	}
	doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
	var doInterval;
	function getfile() {
		$.ajax({
			url: "/openWB/ramdisk/speicherikwh",
				complete: function(request){
					var sgfinal = request.responseText;
					sgfinal = (sgfinal / 1000).toFixed(3);
		    	$("#speicherikwhdiv").html(sgfinal);
				}
	});
		$.ajax({
			url: "/openWB/ramdisk/speicherekwh",
				complete: function(request){
					var sefinal = request.responseText;
					sefinal = (sefinal / 1000).toFixed(3);
		    	$("#speicherekwhdiv").html(sefinal);
				}
		});

	}
	doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
	var doInterval;
	function getfile() {
		$.ajax({
			url: "/openWB/ramdisk/monthly_pvkwhk",
	    	complete: function(request){
		    	$("#monthly_pvkwhdiv").html(request.responseText);
				}
		});
	}
	doInterval = setInterval(getfile, 2000);
</script>

<script type='text/javascript'>
	var doInterval;
	function getfile() {
		$.ajax({
			url: "/openWB/ramdisk/yearly_pvkwhk",
	    	complete: function(request){
		    	$("#yearly_pvkwhdiv").html(request.responseText);
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
					// zur Anzeige Wert positiv darstellen
					// (Erzeugung liegt als Negativwert vor)
					var value = parseInt(request.responseText) * -1;
		    	$("#pvwattdiv").html(""+value);
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
					// zur Anzeige Wert um "Bezug"/"Einspeisung" ergänzen
					var value = parseInt(request.responseText);
					var valueStr = "";
					if(value<0) {
						value = value * -1;
						valueStr = valueStr+value+" (E)"
					} else if (value>0) {
						valueStr = valueStr+value+" (B)"
					} else  {
						// Bezug = 0
						valueStr = valueStr+value
					}
		    	$("#wattbezugdiv").html(valueStr);
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
<script type='text/javascript'>
	function loadstatuslog() {
		$.ajax({
			url: "/openWB/ramdisk/ladestatus.log",
	    	complete: function(request){
		    	$("#ladestatuslogdiv").html(request.responseText);
				}
		});
	}
loadstatuslog();
</script>


<?php
    $result = '';
    $lines = file('/var/www/html/openWB/openwb.conf');
    foreach ($lines as $line) {
        if (strpos($line, "lp1name=") !== false) {
            list(, $lp1nameold) = explode("=", $line);
        }
        if (strpos($line, "lp2name=") !== false) {
            list(, $lp2nameold) = explode("=", $line);
        }
        if (strpos($line, "lp3name=") !== false) {
            list(, $lp3nameold) = explode("=", $line);
	}
        if (strpos($line, "verbraucher1_name=") !== false) {
            list(, $verbraucher1_nameold) = explode("=", $line);
        }
        if (strpos($line, "verbraucher2_name=") !== false) {
            list(, $verbraucher2_nameold) = explode("=", $line);
        }
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
					<h3> OpenWB Status </h3>
				</div>
			</div>
			<br><br>
			<div class="row">
				<div class="col-xs-4 text-center"></div>
				<div class="col-xs-2 text-center">
					Phase 1
				</div>
				<div class="col-xs-2 text-center">
					Phase 2
				</div>
				<div class="col-xs-2 text-center">
					Phase 3
				</div>
			</div>
			<hr>
			<div class="row" style="background-color:#febebe">
				<div class="col-xs-4 text-center">
					EVU Spannung [V]
				</div>
				<div class="col-xs-2 text-center">
					<div id="evuv1div"></div>
				</div>
				<div class="col-xs-2 text-center">
					<div id="evuv2div"></div>
				</div>
				<div class="col-xs-2 text-center">
					<div id="evuv3div"></div>
				</div>
			</div>
			<hr>
			<div class="row" style="background-color:#febebe">
				<div class="col-xs-4 text-center">
					EVU Stromstärke [A]
				</div>
				<div class="col-xs-2 text-center">
					<div id="bezuga1div"></div>
				</div>
				<div class="col-xs-2 text-center">
					<div id="bezuga2div"></div>
				</div>
				<div class="col-xs-2 text-center">
					<div id="bezuga3div"></div>
				</div>
			</div>
			<hr>
			<div class="row" style="background-color:#febebe">
				<div class="col-xs-4 text-center">
					EVU Leistung [W]
				</div>
				<div class="col-xs-2 text-center">
					<div id="bezugw1div"></div>
				</div>
				<div class="col-xs-2 text-center">
					<div id="bezugw2div"></div>
				</div>
				<div class="col-xs-2 text-center">
					<div id="bezugw3div"></div>
				</div>
			</div>
			<hr>
			<div class="row" style="background-color:#febebe">
				<div class="col-xs-4 text-center">
					EVU Power Faktor
				</div>
				<div class="col-xs-2 text-center">
					<div id="evupf1div"></div>
				</div>
				<div class="col-xs-2 text-center">
					<div id="evupf2div"></div>
				</div>
				<div class="col-xs-2 text-center">
					<div id="evupf3div"></div>
				</div>
			</div>
			<hr>
			<div class="row bg-info">
				<div class="col-xs-4 text-center">
					LP1 <?php echo $lp1nameold ?>  Spannung [V]
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
					LP1 <?php echo $lp1nameold ?>  Power Faktor
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
					LP1 <?php echo $lp1nameold ?>  Stromstärke [A]
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
					LP2 <?php echo $lp2nameold ?>  Spannung [V]
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
					LP2 <?php echo $lp2nameold ?> Stromstärke [A]
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
					LP3 <?php echo $lp3nameold ?> Spannung [V]
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
					LP3 <?php echo $lp3nameold ?> Stromstärke [A]
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
				<div class="col-xs-4 text-center"></div>
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
					Ladestromvorgabe [A]
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
				<div class="col-xs-2 text-center"></div>
			</div>
			<hr>
			<div class="row bg-info">
				<div class="col-xs-4 text-center bg-info">
					Ladeleistung [W]
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
					Zählerstand [kWh]
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
			<hr>
			<div class="row bg-info">
				<div class="col-xs-4 text-center bg-info">
					EVSE Modbus Test<br>siehe Hilfe -> Misc
				</div>
				<div class="col-xs-2 text-center bg-info">
					<div id="evsedintestlp1div"></div>
					<?php
            $filename = '/var/www/html/openWB/ramdisk/evsedintestlp1';
            if (file_exists($filename)) {
            	echo "last check " . date("H:i", filemtime($filename));
            }
        	?>
				</div>
				<div class="col-xs-2 text-center bg-info">
					<div id="evsedintestlp2div"></div>
					<?php
            $filename = '/var/www/html/openWB/ramdisk/evsedintestlp2';
            if (file_exists($filename)) {
            	echo "last check " . date("H:i", filemtime($filename));
            }
        	?>
				</div>
				<div class="col-xs-2 text-center bg-info">
					<div id="evsedintestlp3div"></div>
					<?php
            $filename = '/var/www/html/openWB/ramdisk/evsedintestlp3';
            if (file_exists($filename)) {
            	echo "last check " . date("H:i", filemtime($filename));
            }
        	?>
				</div>
			</div>
			<form action="tools/evsedintest.php" method="post">
				<div class="row bg-info">
					<div class="col-xs-4 text-center bg-info"></div>
					<div class="col-xs-2 text-center bg-info">
						<input type="submit" name="testlp1" value="Testen" ></input>
					</div>
					<div class="col-xs-2 text-center bg-info">
						<input type="submit" name="testlp2" value="Testen" ></input>
					</div>
					<div class="col-xs-2 text-center bg-info">
						<input type="submit" name="testlp3" value="Testen" ></input>
					</div>
				</div>
			</form>

			<hr style="height:3px;border:none;color:#333;background-color:#333;" />
			<div class="row" style="background-color:#BEFEBE">
				<div class="col-xs-2 text-center">
					PV Counter
				</div>
				<div class="col-xs-2 text-center">
					<div id="pvcounterdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
					PV Leistung [W]
				</div>
				<div class="col-xs-2 text-center">
					<div id="pvwattdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
					PV Gesamtertrag [kWh]
				</div>
				<div class="col-xs-2 text-center">
					<div id="pvkwhdiv"></div>
				</div>
			</div>
			<div class="row" style="background-color:#BEFEBE">
				<div class="col-xs-2 text-center">
					PV Tagesertrag [kWh]
				</div>
				<div class="col-xs-2 text-center">
					<div id="daily_pvkwhdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
					PV Monatsertrag [kWh]
				</div>
				<div class="col-xs-2 text-center">
					<div id="monthly_pvkwhdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
					PV Jahresertrag [kWh]
				</div>
				<div class="col-xs-2 text-center">
					<div id="yearly_pvkwhdiv"></div>
				</div>
			</div>
			<div class="row">
				<div class="col-xs-2 text-center">
					Speicher geladen [kWh]
				</div>
				<div class="col-xs-2 text-center">
					<div id="speicherikwhdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
					Speicher entladen [kWh]
				</div>
				<div class="col-xs-2 text-center">
					<div id="speicherekwhdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
					
				</div>
				<div class="col-xs-2 text-center">
					
				</div>
			</div>
			<hr>
			<div class="row">
				<div class="col-xs-2 text-center bg-info">
					SoC LP1 [%]
				</div>
				<div class="col-xs-2 text-center bg-info">
					<div id="soclevel"></div>
				</div>
				<div class="col-xs-2 text-center" style="background-color:#febebe">
					EVU [W]
				</div>
				<div class="col-xs-2 text-center" style="background-color:#febebe">
					<div id="wattbezugdiv"></div>
				</div>
				<div class="col-xs-2 text-center" style="background-color:#febebe">
					EVU [Hz]
				</div>
				<div class="col-xs-2 text-center" style="background-color:#febebe">
					<div id="evuhzdiv"></div>
				</div>
			</div>
			<div class="row">
				<div class="col-xs-2 text-center bg-info">
					SoC LP2 [%]
				</div>
				<div class="col-xs-2 text-center bg-info">
					<div id="soclevel1"></div>
				</div>
				<div class="col-xs-2 text-center" style="background-color:#febebe">
					EVU Bezug [kWh]
				</div>
				<div class="col-xs-2 text-center" style="background-color:#febebe">
					<div id="bezugkwhdiv"></div>
				</div>
				<div class="col-xs-2 text-center" style="background-color:#febebe">
					EVU Einspeisung [kWh]
				</div>
				<div class="col-xs-2 text-center" style="background-color:#febebe">
					<div id="einspeisungkwhdiv"></div>
				</div>

			</div>
			<div class="row">
				<div class="col-xs-2 text-center ">
					<?php echo $verbraucher1_nameold ?> [W]
				</div>
				<div class="col-xs-2 text-center ">
					<div id="verbraucher1wattdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
					<?php echo $verbraucher1_nameold ?> Import [kWh]
				</div>
				<div class="col-xs-2 text-center">
					<div id="verbraucher1whdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
					<?php echo $verbraucher1_nameold ?>Export [kWh]

				</div>
				<div class="col-xs-2 text-center">
										<div id="verbraucher1whediv"></div>	</div>

			</div>
			<div class="row">
				<div class="col-xs-2 text-center ">
					<?php echo $verbraucher2_nameold ?> [W]
				</div>
				<div class="col-xs-2 text-center ">
					<div id="verbraucher2wattdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
				<?php echo $verbraucher2_nameold ?> Import [kWh]
				</div>
				<div class="col-xs-2 text-center">
					<div id="verbraucher2whdiv"></div>
				</div>
				<div class="col-xs-2 text-center">
					<?php echo $verbraucher2_nameold ?> Export [kWh]

				</div>
				<div class="col-xs-2 text-center">
										<div id="verbraucher2whediv"></div>	</div>

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
	<div class="row">
		<div style="height:300px;" id="gsidiv"></div>
	</div>
	<div class="row">
		Ladestatus Änderungen:
	</div>
	<div style="white-space: pre-line;" id="ladestatuslogdiv"></div>


		</div>
	</section>

	<div class="mobile-nav">
		<ul></ul>
		<a href="#" class="close-link"><i class="arrow_up"></i></a>
	</div>
	<!-- Scripts -->
	<script src="js/owl.carousel.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="js/wow.min.js"></script>
	<script src="js/typewriter.js"></script>
	<script src="js/jquery.onepagenav.js"></script>
	<script src="js/main.js"></script>
					<script src="gsigraph.js"></script>
				</body>
</html>
