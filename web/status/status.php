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

		<link rel="stylesheet" type="text/css" href="fonts/font-awesome-5.8.2/css/all.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="./settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20201231" ></script>
		<script>
			function getCookie(cname) {
				var name = cname + '=';
				var decodedCookie = decodeURIComponent(document.cookie);
				var ca = decodedCookie.split(';');
				for(var i = 0; i <ca.length; i++) {
					var c = ca[i];
					while (c.charAt(0) == ' ') {
						c = c.substring(1);
					}
					if (c.indexOf(name) == 0) {
						return c.substring(name.length, c.length);
					}
				}
				return '';
			}
			var themeCookie = getCookie('openWBTheme');
		</script>

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
					url: "/openWB/ramdisk/llkwhges",
					complete: function(request){
						$("#llkwhgesdiv").html(request.responseText);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvallwatt",
					complete: function(request){
						// zur Anzeige Wert positiv darstellen
						// (Erzeugung liegt als Negativwert vor)
						var value = parseInt(request.responseText) * -1;
						$("#pvwattdiv").html(""+value);
					}
				});
				$.ajax({
					url: "/openWB/ramdisk/pvallwh",
					complete: function(request){
						$("#pvkwhdiv").html((request.responseText / 1000).toFixed(2));
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
		function rfidlog() {
			$.ajax({
				url: "/openWB/ramdisk/rfid.log",
				complete: function(request){
					var lines = request.responseText.split("\n");
					var result = "";
					for(var i=0; i<lines.length; i++)
						result = lines[i] + "\n" + result;
					$("#rfiddiv").html(result);
				}
			});
		}
		rfidlog();
		function debuglog() {
			$.ajax({
				url: "/openWB/ramdisk/openWB.log",
				complete: function(request){
					var lines = request.responseText.split("\n");
					var result = "";
					for(var i=0; i<lines.length; i++)
						result = lines[i] + "\n" + result;
					$("#debugdiv").html(result);
				}
			});
		}
		debuglog();
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
		function nurpvlog() {
			$.ajax({
				url: "/openWB/ramdisk/nurpv.log",
				complete: function(request){
					var lines = request.responseText.split("\n");
					var result = "";
					for(var i=0; i<lines.length; i++)
						result = lines[i] + "\n" + result;
					$("#nurpvdiv").html(result);
				}
			});
		}
		nurpvlog();
		function soclog() {
			$.ajax({
				url: "/openWB/ramdisk/soc.log",
				complete: function(request){
					var lines = request.responseText.split("\n");
					var result = "";
					for(var i=0; i<lines.length; i++)
						result = lines[i] + "\n" + result;
					$("#socdiv").html(result);
				}
			});
		}
		soclog();
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
			$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
			foreach($lines as $line) {
				list($key, $value) = explode("=", $line, 2);
				${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
			}

			$speichervorhanden = trim( file_get_contents( $_SERVER['DOCUMENT_ROOT'] . '/openWB/ramdisk/speichervorhanden' ) );
		?>
	<div id="nav-placeholder"></div>
	<div role="main" class="container" style="margin-top: 20px">
		<h1>Status</h1>
		<form action="./tools/saveconfig.php" method="POST">

			<!-- EVU  -->
			<div class="card border-secondary">
				<div class="card-header bg-secondary">
					<div class="form-group mb-0">
						<div class="form-row vaRow mb-0">
							<div class="col-4">EVU</div>
						</div>
					</div>
				</div>
				<div class="card-body">
					<div class="table-responsive table-sm" style="width: 50%;">
						<table id="evu1">
							<tbody>
								<tr>
									<th scope="row">Schieflast [A]</th>
									<td><div id="schieflastdiv"></div></td>
								</tr>
								<tr>
									<th scope="row">Gesamtleistung [W]</th>
									<td><div id="wattbezugdiv"></div></td>
								</tr>
								<tr>
									<th scope="row">Frequenz [Hz]</th>
									<td><div id="evuhzdiv"></div></td>
								</tr>																							
								<tr>
									<th scope="row">Bezug [kWh]</th>
									<td><div id="bezugkwhdiv"></div></td>
								</tr>
								<tr>
									<th scope="row">Einspeisung [kWh]</th>
									<td><div id="einspeisungkwhdiv"></div></td>
								</tr>									
							</tbody>
						</table>
					</div>
					<script>
					$('#evu1 tr td').each(function() {
						if ($(this).text() === '0'){
							$(this).parent().hide();
						}
					});
					</script>
					<div class="table-responsive table-sm">
						<table id="evu2">
							<thead>
								<tr>
									<th scope="col"></th>
									<th scope="col">Phase 1</th>
									<th scope="col">Phase 2</th>
									<th scope="col">Phase 3</th>
								</tr>
							</head>
							<tbody>
								<tr>
									<th scope="row">Spannung [V]</th>
									<td><div id="evuv1div"></div></td>
									<td><div id="evuv2div"></div></td>
									<td><div id="evuv3div"></div></td>
								</tr>
								<tr>
									<th scope="row">Stromstärke [A]</th>
									<td><div id="bezuga1div"></div></td>
									<td><div id="bezuga2div"></div></td>
									<td><div id="bezuga3div"></div></td>
								</tr>
								<tr>
									<th scope="row">Leistung [W]</th>
									<td><div id="bezugw1div"></div></td>
									<td><div id="bezugw2div"></div></td>
									<td><div id="bezugw3div"></div></td>
								</tr>
								<tr>
									<th scope="row">Power Faktor</th>
									<td><div id="evupf1div"></div></td>
									<td><div id="evupf2div"></div></td>
									<td><div id="evupf3div"></div></td>
								</tr>
								<tr>
									<th scope="row">Test</th>
									<td>0</td>
									<td>0</td>
									<td>0</td>
								</tr>
							</tbody>
						</table>
					</div>
					<!--     $('#evu2 tr td').each(function() 
	{
		var tr = $(this);
    if (tr.find("td:eq(0)").text()=="0"
        && tr.find("td:eq(1)").text()=="0"
        && tr.find("td:eq(2)").text()=="0"
    ) tr.parent().hide();
	}
	-->
					<script>
						var tbl = document.getElementById('evu2');         //find the table
						var rows = tbl.querySelectorAll('tbody tr');        //find all rows in the table body

						for(i = 0; i < rows.length; i++) {                  //iterate through the rows

							var cells = rows[i].querySelectorAll('td');     //find all of the cells in the row

							var flag = true;                                //set flag prior to cell evaluation

							for(j = 2; j < cells.length; j++) {             //iterate through the cells (starting with the cell at position 2)
								if (cells[j].innerHTML != '0') {            //check if the cell contains '0' (set flag to false if cell is not '0')
									flag = false;                           
								}
							}

							if(flag) { 
								rows[i].classList.add('hide');              //hide the row if the falg remained true (i.e. none of the cells contained a value other than '0'
							}
						}
					</script>
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
		</div>
		<div class="row">
			<div class="col-sm-2 text-center bg-info">
				SoC LP2 [%]
			</div>
			<div class="col-sm-2 text-center bg-info">
				<div id="soclevel1"></div>
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

		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" id="ladestatuslog"><h4>Ladestatus Änderungen:</h4></span>
		</div>
		<div class="hide" style="white-space: pre-line; display: none;" id="ladestatuslogdiv"></div>

		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" id="smarthomelog"> <h4>SmartHome Log:</h4></span>
		</div>

		<div class="hide" style="white-space: pre-line; display: none;" id="smarthomediv"></div>
		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" class="cursor-pointer" id="rfidlog"> <h4>RFID Log:</h4></span>
		</div>

		<div class="hide" style="white-space: pre-line; display: none;" id="rfiddiv"></div>
		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" class="cursor-pointer" id="mqttlog"> <h4>Mqtt Log:</h4></span>
		</div>

		<div class="hide" style="white-space: pre-line; display: none;" id="mqttdiv"></div>
		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" class="cursor-pointer" id="debuglog"> <h4>Debug Log:</h4></span>
		</div>

		<div class="hide" style="white-space: pre-line; display: none;" id="debugdiv"></div>

		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" class="cursor-pointer" id="nurpvlog"> <h4>Nur PV Log:</h4></span>
		</div>

		<div class="hide" style="white-space: pre-line; display: none;" id="nurpvdiv"></div>

		<div class="row">
			<span style="cursor: pointer; text-decoration: underline;" class="cursor-pointer" id="soclog"> <h4>EV SoC Log:</h4></span>
		</div>

		<div class="hide" style="white-space: pre-line; display: none;" id="socdiv"></div>
	</div>  <!-- container -->

	<footer class="footer bg-dark text-light font-small">
		<div class="container text-center">
			<small>Sie befinden sich hier: System/Status</small>
		</div>
	</footer>

	<script>

		// load navbar
		$("#nav-placeholder").load('themes/' + themeCookie + '/navbar.html?v=20210101', disableMenuItem);
		function disableMenuItem() {
			$('#navStatus').addClass('disabled');
		}

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
		$('#rfidlog').click(function(event){
			var element = document.getElementById('rfiddiv');
			if ( element.classList.contains("hide") ) {
				$('#rfiddiv').show();
				$('#rfiddiv').removeClass("hide");
			} else {
				$('#rfiddiv').hide();
				$('#rfiddiv').addClass("hide");
			}
		});
		$('#nurpvlog').click(function(event){
			var element = document.getElementById('nurpvdiv');
			if ( element.classList.contains("hide") ) {
				$('#nurpvdiv').show();
				$('#nurpvdiv').removeClass("hide");
			} else {
				$('#nurpvdiv').hide();
				$('#nurpvdiv').addClass("hide");
			}
		});
		$('#soclog').click(function(event){
			var element = document.getElementById('socdiv');
			if ( element.classList.contains("hide") ) {
				$('#socdiv').show();
				$('#socdiv').removeClass("hide");
			} else {
				$('#socdiv').hide();
				$('#socdiv').addClass("hide");
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
		$('#debuglog').click(function(event){
			var element = document.getElementById('debugdiv');
			if ( element.classList.contains("hide") ) {
				$('#debugdiv').show();
				$('#debugdiv').removeClass("hide");
			} else {
				$('#debugdiv').hide();
				$('#debugdiv').addClass("hide");
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

	<script>
	$(document).ready(function(){

		// load scripts synchronously in order specified
		var scriptsToLoad = [
			// load Chart.js library
			'js/Chart.bundle.js',
			// load mqtt library
			'js/mqttws31.js',
			// some helper functions
			//'themes/dark/helperFunctions.js?ver=20201218',
			// functions for processing messages
			'status/processAllMqttMsg.js?ver=20201228a',
			// respective Chart.js definition live
			//'themes/dark/livechart.js?ver=20201218',
			// respective Chart.js definition awattar
			//'themes/dark/electricityPriceChart.js?ver=20201228',
			// functions performing mqtt and start mqtt-service
			'status/setupMqttServices.js?ver=20201228a',
		];
		scriptsToLoad.forEach(function(src) {
			var script = document.createElement('script');
			script.src = src;
			script.async = false;
			document.body.appendChild(script);
		});
	});  // end document ready
	</script>

</body>
</html>
