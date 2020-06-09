<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Status</title>
		<meta name="description" content="Control your charge" />
		<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
		<meta name="author" content="Kevin Wieland, Michael Ortenstein" />
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

		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="./status/status_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>

		<script>
			var doInterval;

			function getfile() {
				$.ajaxSetup({ cache: false});
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
				$.ajax({
					url: "/openWB/ramdisk/schieflast",
					complete: function(request){
						$("#schieflastdiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/bezuga1",
					complete: function(request){
						$("#bezuga1div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/bezuga2",
					complete: function(request){
						$("#bezuga2div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/bezuga3",
					complete: function(request){
						$("#bezuga3div").html(request.responseText);
					}
				});
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
				$.ajax({
					url: "/openWB/ramdisk/llsoll",
					complete: function(request){
						$("#llsolldiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llsolls1",
					complete: function(request){
						$("#llsolls1div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llsolls2",
					complete: function(request){
						$("#llsolls2div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llas11",
					complete: function(request){
						$("#llas11div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llas12",
					complete: function(request){
						$("#llas12div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llas13",
					complete: function(request){
						$("#llas13div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llas21",
					complete: function(request){
						$("#llas21div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llas22",
					complete: function(request){
						$("#llas22div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llas23",
					complete: function(request){
						$("#llas23div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/lla1",
					complete: function(request){
						$("#lla1div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/lla2",
					complete: function(request){
						$("#lla2div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/lla3",
					complete: function(request){
						$("#lla3div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llaktuell",
					complete: function(request){
						$("#llaktuelldiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llaktuells1",
					complete: function(request){
						$("#llaktuells1div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llaktuells2",
					complete: function(request){
						$("#llaktuells2div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llkwh",
					complete: function(request){
						$("#llkwhdiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llkwhs1",
					complete: function(request){
						$("#llkwhs1div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llkwhs2",
					complete: function(request){
						$("#llkwhs2div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llkwhges",
					complete: function(request){
						$("#llkwhgesdiv").html(request.responseText);
					}
				});
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
				$.ajax({
					url: "/openWB/ramdisk/einspeisungkwh",
					complete: function(request){
						var eefinal = request.responseText;
						eefinal = (eefinal / 1000).toFixed(3);
						$("#einspeisungkwhdiv").html(eefinal);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/bezugkwh",
					complete: function(request){
						var eifinal = request.responseText;
						eifinal = (eifinal / 1000).toFixed(3);
						$("#bezugkwhdiv").html(eifinal);
					}
				});
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
				$.ajax({
					url: "/openWB/ramdisk/pvcounter",
					complete: function(request){
						$("#pvcounterdiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvwatt",
					complete: function(request){
						// zur Anzeige Wert positiv darstellen
						// (Erzeugung liegt als Negativwert vor)
						var value = parseInt(request.responseText) * -1;
						$("#pvwattdiv").html(""+value);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvkwh",
					complete: function(request){
						$("#pvkwhdiv").html((request.responseText / 1000).toFixed(2));
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/daily_pvkwhk",
					complete: function(request){
						$("#daily_pvkwhdiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/monthly_pvkwhk",
					complete: function(request){
						$("#monthly_pvkwhdiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/yearly_pvkwhk",
					complete: function(request){
						$("#yearly_pvkwhdiv").html(request.responseText);
						if ( request.responseText > 100 ) {
							$('#pvpartlycounterdiv').show();
						}
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvwatt1",
					complete: function(request){
						// zur Anzeige Wert positiv darstellen
						// (Erzeugung liegt als Negativwert vor)
						var value = parseInt(request.responseText) * -1;
						$("#pvwattdiv1").html(""+value);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvkwhk1",
					complete: function(request){
						$("#pvkwhdiv1").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/daily_pvkwhk1",
					complete: function(request){
						$("#daily_pvkwhdiv1").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/monthly_pvkwhk1",
					complete: function(request){
						$("#monthly_pvkwhdiv1").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/yearly_pvkwhk1",
					complete: function(request){
						$("#yearly_pvkwhdiv1").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvwatt2",
					complete: function(request){
						// zur Anzeige Wert positiv darstellen
						// (Erzeugung liegt als Negativwert vor)
						var value = parseInt(request.responseText) * -1;
						$("#pvwattdiv2").html(""+value);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvkwhk2",
					complete: function(request){
						$("#pvkwhdiv2").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/daily_pvkwhk2",
					complete: function(request){
						$("#daily_pvkwhdiv2").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/monthly_pvkwhk2",
					complete: function(request){
						$("#monthly_pvkwhdiv2").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/yearly_pvkwhk2",
					complete: function(request){
						$("#yearly_pvkwhdiv2").html(request.responseText);
					}
				});
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
				$.ajax({
					url: "/openWB/ramdisk/llv1",
					complete: function(request){
						$("#llv1div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llv2",
					complete: function(request){
						$("#llv2div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llv3",
					complete: function(request){
						$("#llv3div").html(request.responseText);
					}
				});
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
				$.ajax({
					url: "/openWB/ramdisk/llpf1",
					complete: function(request){
						$("#llpf1div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llpf2",
					complete: function(request){
						$("#llpf2div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/llpf3",
					complete: function(request){
						$("#llpf3div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/evuv1",
					complete: function(request){
						$("#evuv1div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/evuv2",
					complete: function(request){
						$("#evuv2div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/evuv3",
					complete: function(request){
						$("#evuv3div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/evuhz",
					complete: function(request){
						$("#evuhzdiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/evupf1",
					complete: function(request){
						$("#evupf1div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/evupf2",
					complete: function(request){
						$("#evupf2div").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/evupf3",
					complete: function(request){
						$("#evupf3div").html(request.responseText);
					}
				});
			}
		doInterval = setInterval(getfile, 2000);

		function loadstatuslog() {
			$.ajax({
				url: "/openWB/ramdisk/ladestatus.log",
				complete: function(request){
					var lines = request.responseText.split("\n");
					var result = "";
					for(var i=0; i<lines.length; i++)
						result = lines[i] + "\n" + result;
					$("#ladestatuslogdiv").html(result);
				}
			});
		}
		loadstatuslog();
		function mqttlog() {
			$.ajax({
				url: "/openWB/ramdisk/mqtt.log",
				complete: function(request){
					var lines = request.responseText.split("\n");
					var result = "";
					for(var i=0; i<lines.length; i++)
						result = lines[i] + "\n" + result;
					$("#mqttdiv").html(result);
				}
			});
		}
		mqttlog();
		function smarthomelog() {
			$.ajax({
				url: "/openWB/ramdisk/smarthome.log",
				complete: function(request){
					var lines = request.responseText.split("\n");
					var result = "";
					for(var i=0; i<lines.length; i++)
						result = lines[i] + "\n" + result;
					$("#smarthomediv").html(result);
				}
			});
		}
		smarthomelog();
	</script>

	<?php
		$owbversion = file_get_contents('/var/www/html/openWB/web/version');
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
			if (strpos($line, "lastmanagement=") !== false) {
				list(, $lastmanagementold) = explode("=", $line);
			}
			if (strpos($line, "lastmanagements2=") !== false) {
				list(, $lastmanagements2old) = explode("=", $line);
			}
			if (strpos($line, "simplemode=") !== false) {
				list(, $simplemodeold) = explode("=", $line);
			}
			if (strpos($line, "verbraucher1_name=") !== false) {
				list(, $verbraucher1_nameold) = explode("=", $line);
			}
			if (strpos($line, "verbraucher2_name=") !== false) {
				list(, $verbraucher2_nameold) = explode("=", $line);
			}
			if (strpos($line, "name_wechselrichter1=") !== false) {
				list(, $name_wechselrichter1old) = explode("=", $line);
				# entferne EOL von String
				$name_wechselrichter1old = trim(preg_replace('/\s+/', '', $name_wechselrichter1old));
			}
			if (strpos($line, "name_wechselrichter2=") !== false) {
				list(, $name_wechselrichter2old) = explode("=", $line);
				# entferne EOL von String
				$name_wechselrichter2old = trim(preg_replace('/\s+/', '', $name_wechselrichter2old));
			}
			if (strpos($line, "kostalplenticoreip2=") !== false) {
				# wird benötigt, für Anzeige der getrennten WR-Daten an/aus
				list(, $kostalplenticoreip2old) = explode("=", $line);
				# entferne EOL von String
				$kostalplenticoreip2old = trim(preg_replace('/\s+/', '', $kostalplenticoreip2old));
			}
		}
?>
<script>
	$(function() {
		var lp2akt = <?php echo $lastmanagementold ?>;
		var lp3akt = <?php echo $lastmanagements2old ?>;
		
		if(lp2akt == '0') {
			$('#ladepunkt2div').hide();
		} else {
			$('#ladepunkt2div').show();
		}
		if(lp2akt == '0') {
			$('#ladepunkt3div').hide();
		} else {
			$('#ladepunkt3div').show();
		}
	});
</script>

</head>
<body>
	<?php
		include '/var/www/html/openWB/web/status/navbar.php';
	?>

	<div role="main" class="container" style="margin-top: 20px; display: block;">
		<div class="row">
			<div class="col-sm-12 text-center">
				<h3> Status </h3>
			</div>
		</div>
		<div class="row">
			<div class="col-sm-4 text-center"></div>
			<div class="col-sm-2 text-center">
				Phase 1
			</div>
			<div class="col-sm-2 text-center">
				Phase 2
			</div>
			<div class="col-sm-2 text-center">
				Phase 3
			</div>
		</div>
		<hr>
		<div class="row" style="background-color:#febebe">
			<div class="col-sm-4 text-center">
				EVU Spannung [V]
			</div>
			<div class="col-sm-2 text-center">
				<div id="evuv1div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="evuv2div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="evuv3div"></div>
			</div>
		</div>
		<hr>
		<div class="row" style="background-color:#febebe">
			<div class="col-sm-4 text-center">
				EVU Stromstärke [A]
			</div>
			<div class="col-sm-2 text-center">
				<div id="bezuga1div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="bezuga2div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="bezuga3div"></div>
			</div>
		</div>
		<div class="row" style="background-color:#febebe">
			<div class="col-sm-4 text-center">
			EVU Schieflast [A]</div>
			<div class="col-sm-2 text-center">
			</div>
			<div class="col-sm-2 text-center">
				<div id="schieflastdiv"></div>
			</div>
			<div class="col-sm-2 text-center">
			</div>
		</div>
		<hr>
		<div class="row" style="background-color:#febebe">
			<div class="col-sm-4 text-center">
				EVU Leistung [W]
			</div>
			<div class="col-sm-2 text-center">
				<div id="bezugw1div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="bezugw2div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="bezugw3div"></div>
			</div>
		</div>
		<hr>
		<div class="row" style="background-color:#febebe">
			<div class="col-sm-4 text-center">
				EVU Power Faktor
			</div>
			<div class="col-sm-2 text-center">
				<div id="evupf1div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="evupf2div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="evupf3div"></div>
			</div>
		</div>
		<hr>
		<div class="row bg-info">
			<div class="col-sm-4 text-center">
				LP1 <?php echo $lp1nameold ?>  Spannung [V]
			</div>
			<div class="col-sm-2 text-center">
				<div id="llv1div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="llv2div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="llv3div"></div>
			</div>
		</div>
		<hr>
		<div class="row bg-info">
			<div class="col-sm-4 text-center">
				LP1 <?php echo $lp1nameold ?>  Power Faktor
			</div>
			<div class="col-sm-2 text-center">
				<div id="llpf1div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="llpf2div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="llpf3div"></div>
			</div>
		</div>
		<hr>
		<div class="row bg-info">
			<div class="col-sm-4 text-center">
				LP1 <?php echo $lp1nameold ?>  Stromstärke [A]
			</div>
			<div class="col-sm-2 text-center">
				<div id="lla1div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="lla2div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="lla3div"></div>
			</div>
		</div>
		<div id="ladepunkt2div">
			<hr>
			<div class="row bg-info">
				<div class="col-sm-4 text-center">
					LP2 <?php echo $lp2nameold ?>  Spannung [V]
				</div>
				<div class="col-sm-2 text-center">
					<div id="llv1s1div"></div>
				</div>
				<div class="col-sm-2 text-center">
					<div id="llv2s1div"></div>
				</div>
				<div class="col-sm-2 text-center">
					<div id="llv3s1div"></div>
				</div>
			</div>
			<hr>
			<div class="row bg-info">
				<div class="col-sm-4 text-center bg-info">
					LP2 <?php echo $lp2nameold ?> Stromstärke [A]
				</div>
				<div class="col-sm-2 text-center bg-info">
					<div id="llas11div"></div>
				</div>
				<div class="col-sm-2 text-center bg-info">
					<div id="llas12div"></div>
				</div>
				<div class="col-sm-2 text-center bg-info">
					<div id="llas13div"></div>
				</div>
			</div>
		</div>
		<div id="ladepunkt3div">
			<hr>
			<div class="row bg-info">
				<div class="col-sm-4 text-center">
					LP3 <?php echo $lp3nameold ?> Spannung [V]
				</div>
				<div class="col-sm-2 text-center">
					<div id="llv1s2div"></div>
				</div>
				<div class="col-sm-2 text-center">
					<div id="llv2s2div"></div>
				</div>
				<div class="col-sm-2 text-center">
					<div id="llv3s2div"></div>
				</div>
			</div>
			<hr>
			<div class="row bg-info">
				<div class="col-sm-4 text-center bg-info">
					LP3 <?php echo $lp3nameold ?> Stromstärke [A]
				</div>
				<div class="col-sm-2 text-center bg-info">
					<div id="llas21div"></div>
				</div>
				<div class="col-sm-2 text-center bg-info">
					<div id="llas22div"></div>
				</div>
				<div class="col-sm-2 text-center bg-info">
					<div id="llas23div"></div>
				</div>
			</div>
		</div>
		<hr style="height:3px;background-color:#333;" />
		<div class="row">
			<div class="col-sm-4 text-center"></div>
			<div class="col-sm-2 text-center">
				Ladepunkt 1
			</div>
			<div class="col-sm-2 text-center">
				Ladepunkt 2
			</div>
			<div class="col-sm-2 text-center">
				Ladepunkt 3
			</div>
			<div class="col-sm-2 text-center">
				Gesamt
			</div>
		</div>
		<hr>
		<div class="row bg-info">
			<div class="col-sm-4 text-center">
				Ladestromvorgabe [A]
			</div>
			<div class="col-sm-2 text-center">
				<div id="llsolldiv"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="llsolls1div"></div>
			</div>
			<div class="col-sm-2 text-center">
				<div id="llsolls2div"></div>
			</div>
			<div class="col-sm-2 text-center"></div>
		</div>
		<hr>
		<div class="row bg-info">
			<div class="col-sm-4 text-center bg-info">
				Ladeleistung [W]
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="llaktuelldiv"></div>
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="llaktuells1div"></div>
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="llaktuells2div"></div>
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="lldiv"></div>
			</div>
		</div>
		<hr>
		<div class="row bg-info">
			<div class="col-sm-4 text-center bg-info">
				Zählerstand [kWh]
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="llkwhdiv"></div>
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="llkwhs1div"></div>
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="llkwhs2div"></div>
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="llkwhgesdiv"></div>
			</div>
		</div>
		<hr>
		<div class="row bg-info">
			<div class="col-sm-4 text-center bg-info">
				EVSE Modbus Test<br>siehe Hilfe -> Misc
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="evsedintestlp1div"></div>
				<?php
				$filename = '/var/www/html/openWB/ramdisk/evsedintestlp1';
				if (file_exists($filename)) {
					echo "last check " . date("H:i", filemtime($filename));
				}
				?>
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="evsedintestlp2div"></div>
				<?php
				$filename = '/var/www/html/openWB/ramdisk/evsedintestlp2';
				if (file_exists($filename)) {
					echo "last check " . date("H:i", filemtime($filename));
				}
				?>
			</div>
			<div class="col-sm-2 text-center bg-info">
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
				<div class="col-sm-4 text-center bg-info"></div>
				<div class="col-sm-2 text-center bg-info">
					<input type="submit" name="testlp1" value="Testen" >
				</div>
				<div class="col-sm-2 text-center bg-info">
					<input type="submit" name="testlp2" value="Testen" >
				</div>
				<div class="col-sm-2 text-center bg-info">
					<input type="submit" name="testlp3" value="Testen" >
				</div>
			</div>
		</form>

		<hr style="height:3px;border:none;color:#333;background-color:#333;" />
		<div class="row" style="background-color:#BEFEBE">
			<div class="col text-center bold">
				PV Gesamt-Anlagendaten
			</div>
		</div>
		<div class="row" style="background-color:#BEFEBE">
			<div class="col-sm-2 text-center">
				PV Counter
			</div>
			<div class="col-sm-2 text-center">
				<div id="pvcounterdiv"></div>
			</div>
			<div class="col-sm-2 text-center">
				PV Leistung [W]
			</div>
			<div class="col-sm-2 text-center">
				<div id="pvwattdiv"></div>
			</div>
			<div class="col-sm-2 text-center">
				PV Gesamtertrag [kWh]
			</div>
			<div class="col-sm-2 text-center">
				<div id="pvkwhdiv"></div>
			</div>
		</div>
		<div id="pvpartlycounterdiv" style="display: none;">
			<div class="row" style="background-color:#BEFEBE">
				<div class="col-sm-2 text-center">
					PV Tagesertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="daily_pvkwhdiv"></div>
				</div>
				<div class="col-sm-2 text-center">
					PV Monatsertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="monthly_pvkwhdiv"></div>
				</div>
				<div class="col-sm-2 text-center">
					PV Jahresertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="yearly_pvkwhdiv"></div>
				</div>
			</div>
		</div>
		<div class="row" style="background-color:#FCBE1E">
			<div class="col-sm-2 text-center">
			</div>
			<div class="col-sm-2 text-center">
				Speicher
			</div>
			<div class="col-sm-2 text-center">
				geladen [kWh]
			</div>
			<div class="col-sm-2 text-center">
				<div id="speicherikwhdiv"></div>
			</div>
			<div class="col-sm-2 text-center">
				entladen [kWh]
			</div>
			<div class="col-sm-2 text-center">
				<div id="speicherekwhdiv"></div>
			</div>
		</div>
		<hr>
		<div id="pvinverter1and2div">
			<div class="row" style="background-color:#BEFEBE">
				<div class="col text-center bold">
					PV Anlagendaten Wechselrichter 1
					<?php
						if ($name_wechselrichter1old != '') {
							echo ' (';
							echo $name_wechselrichter1old;
							echo ')';
						}
					?>
				</div>
			</div>
			<div class="row" style="background-color:#BEFEBE">
				<div class="col-sm-2 text-center">
				</div>
				<div class="col-sm-2 text-center">
				</div>
				<div class="col-sm-2 text-center">
					PV Leistung [W]
				</div>
				<div class="col-sm-2 text-center">
					<div id="pvwattdiv1"></div>
				</div>
				<div class="col-sm-2 text-center">
					PV Gesamtertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="pvkwhdiv1"></div>
				</div>
			</div>
			<div class="row" style="background-color:#BEFEBE">
				<div class="col-sm-2 text-center">
					PV Tagesertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="daily_pvkwhdiv1"></div>
				</div>
				<div class="col-sm-2 text-center">
					PV Monatsertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="monthly_pvkwhdiv1"></div>
				</div>
				<div class="col-sm-2 text-center">
					PV Jahresertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="yearly_pvkwhdiv1"></div>
				</div>
			</div>
			<hr>
			<div class="row" style="background-color:#BEFEBE">
				<div class="col text-center bold">
					PV Anlagendaten Wechselrichter 2
					<?php
						if ($name_wechselrichter2old != '') {
							echo ' (';
							echo $name_wechselrichter2old;
							echo ')';
						}
					?>
				</div>
			</div>
			<div class="row" style="background-color:#BEFEBE">
				<div class="col-sm-2 text-center">
				</div>
				<div class="col-sm-2 text-center">
				</div>
				<div class="col-sm-2 text-center">
					PV Leistung [W]
				</div>
				<div class="col-sm-2 text-center">
					<div id="pvwattdiv2"></div>
				</div>
				<div class="col-sm-2 text-center">
					PV Gesamtertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="pvkwhdiv2"></div>
				</div>
			</div>
			<div class="row" style="background-color:#BEFEBE">
				<div class="col-sm-2 text-center">
					PV Tagesertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="daily_pvkwhdiv2"></div>
				</div>
				<div class="col-sm-2 text-center">
					PV Monatsertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="monthly_pvkwhdiv2"></div>
				</div>
				<div class="col-sm-2 text-center">
					PV Jahresertrag [kWh]
				</div>
				<div class="col-sm-2 text-center">
					<div id="yearly_pvkwhdiv2"></div>
				</div>
			</div>
			<hr>
		</div>
		<div class="row">
			<div class="col-sm-2 text-center bg-info">
				SoC LP1 [%]
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="soclevel"></div>
			</div>
			<div class="col-sm-2 text-center" style="background-color:#febebe">
				EVU [W]
			</div>
			<div class="col-sm-2 text-center" style="background-color:#febebe">
				<div id="wattbezugdiv"></div>
			</div>
			<div class="col-sm-2 text-center" style="background-color:#febebe">
				EVU [Hz]
			</div>
			<div class="col-sm-2 text-center" style="background-color:#febebe">
				<div id="evuhzdiv"></div>
			</div>
		</div>
		<div class="row">
			<div class="col-sm-2 text-center bg-info">
				SoC LP2 [%]
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="soclevel1"></div>
			</div>
			<div class="col-sm-2 text-center" style="background-color:#febebe">
				EVU Bezug [kWh]
			</div>
			<div class="col-sm-2 text-center" style="background-color:#febebe">
				<div id="bezugkwhdiv"></div>
			</div>
			<div class="col-sm-2 text-center" style="background-color:#febebe">
				EVU Einspeisung [kWh]
			</div>
			<div class="col-sm-2 text-center" style="background-color:#febebe">
				<div id="einspeisungkwhdiv"></div>
			</div>
		</div>
		<div class="row">
			<div class="col-sm-2 text-center ">
				<?php echo $verbraucher1_nameold ?> [W]
			</div>
			<div class="col-sm-2 text-center ">
				<div id="verbraucher1wattdiv"></div>
			</div>
			<div class="col-sm-2 text-center">
				<?php echo $verbraucher1_nameold ?> Import [kWh]
			</div>
			<div class="col-sm-2 text-center">
				<div id="verbraucher1whdiv"></div>
			</div>
			<div class="col-sm-2 text-center">
				<?php echo $verbraucher1_nameold ?>Export [kWh]
			</div>
			<div class="col-sm-2 text-center">
				<div id="verbraucher1whediv"></div>
			</div>
		</div>
		<div class="row">
			<div class="col-sm-2 text-center ">
				<?php echo $verbraucher2_nameold ?> [W]
			</div>
			<div class="col-sm-2 text-center ">
				<div id="verbraucher2wattdiv"></div>
			</div>
			<div class="col-sm-2 text-center">
				<?php echo $verbraucher2_nameold ?> Import [kWh]
			</div>
			<div class="col-sm-2 text-center">
				<div id="verbraucher2whdiv"></div>
			</div>
			<div class="col-sm-2 text-center">
				<?php echo $verbraucher2_nameold ?> Export [kWh]
			</div>
			<div class="col-sm-2 text-center">
				<div id="verbraucher2whediv"></div>
			</div>
		</div>
		<hr style="height:3px;border:none;color:#333;background-color:#333;" />
		<p>
			Uptime: <span id='uptime'>--</span><br>
			OS: <?php echo exec('uname -ors'); ?><br>
			System: <?php echo exec('uname -nmi'); ?> <?php echo exec("cat /proc/cpuinfo | grep 'Processor' | head -n 1"); ?>
			<meter id='cpu' high=85 min=0 max=100 value=0></meter> <span id='cpuuse'>--</span>%<br>
			Memory: <span id='memtot'>--</span>MB
			<meter id='mem' min='0' value=0></meter> <span style="font-size: small;">(<span id='memfree'>--</span>MB free)</span><br>
			Disk Usage: <span id='diskuse'>--</span>, <span id='diskfree'>--</span> avail.<br>
			openWB Version <?php echo $owbversion ?>
		</p>
		<script>
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

		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" id="ladestatuslog"><h4>Ladestatus Änderungen:</h4></span>
		</div>
		<div class="hide" style="white-space: pre-line; display: none;" id="ladestatuslogdiv"></div>
		
		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" id="smarthomelog"> <h4>SmartHome Log:</h4></span>
		</div>

		<div class="hide" style="white-space: pre-line; display: none;" id="smarthomediv"></div>
		
		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" class="cursor-pointer" id="mqttlog"> <h4>Mqtt Log:</h4></span>
		</div>

		<div class="hide" style="white-space: pre-line; display: none;" id="mqttdiv"></div>

	</div>  <!-- container -->

	<footer class="footer bg-dark text-light font-small">
		<!-- no text for footer -->
	</footer>

	<script>
		$(function() {
			if('<?php echo $kostalplenticoreip2old ?>' == 'none') {
				$('#pvinverter1and2div').hide();
			}
		});
		$('#mqttlog').click(function(event){
			var element = document.getElementById('mqttdiv'); 
			if ( element.classList.contains("hide") ) { 
				$('#mqttdiv').show();
				$('#mqttdiv').removeClass("hide");
			} else {
				$('#mqttdiv').hide(); 
				$('#mqttdiv').addClass("hide");
			}
		});
		$('#ladestatuslog').click(function(event){
			var element = document.getElementById('ladestatuslogdiv'); 
			if ( element.classList.contains("hide") ) { 
				$('#ladestatuslogdiv').show();
				$('#ladestatuslogdiv').removeClass("hide");
			} else {
				$('#ladestatuslogdiv').hide(); 
				$('#ladestatuslogdiv').addClass("hide");
			}
		});
		$('#smarthomelog').click(function(event){
			var element = document.getElementById('smarthomediv'); 
			if ( element.classList.contains("hide") ) { 
				$('#smarthomediv').show();
				$('#smarthomediv').removeClass("hide");
			} else {
				$('#smarthomediv').hide(); 
				$('#smarthomediv').addClass("hide");
			}
		});

	</script>
</body>
</html>
