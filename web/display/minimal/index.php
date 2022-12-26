<!DOCTYPE html>
<html lang="de">
	<head>
		<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1 maximum-scale=1,user-scalable=0">
		<title>openWB</title>
		<meta name="description" content="openWB" />
		<meta name="keywords" content="openWB" />
		<meta name="author" content="Kevin Wieland" />
		<link rel="shortcut icon" href="img/favicons/favicon.ico">
		<script src="js/jquery-3.6.0.min.js"></script>
		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<script>
			$(document).ready(function(){
				/**
				 * detect touch devices and map contextmenu (long press) to normal click
				 */
				$('body').on("contextmenu", function(event){
					console.log("Contextmenu triggered");
					if( ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0) ) {
						console.log("Click event generated");
						$(event.target).trigger("click"); // fire a click event
						event.preventDefault();
					}
				});
			});
		</script>
	</head>
	<body>

		<!-- minimal.html -->
		<?php include ("gaugevalues.php"); ?>
		<script src="display/minimal/gauge.min.js?ver=20220510"></script>
		<link rel="stylesheet" href="display/minimal/minimal.css?ver=20220510">

		<div id="main">
			<div id="gaugedivlp1" style="position: absolute; top: 10px; left: 10px; bottom: 10px; right: 50%;">
				<canvas id="lp1" style="height: 600px; top: -150px; left: 20px; position: absolute; width: 760px;"></canvas>
				<div id="lp1t" style="font-size: 35px; top: 290px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
				<canvas id="lp1s" style="height: 520px; top: -80px; left: 30px; position: absolute; width: 740px;"></canvas>
				<div id="lp1st" style="font-size: 35px; top: 230px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
				<div style="top: 350px; left: 265px; text-align: center; position: absolute; width: 265px; font-size: 32px;">
					<i id="lp1plugstat" class="fas fa-plug"></i>
					<i id="lp1disabled" class="fas fa-lock" style="color: red"></i>
					<i id="lp1enabled" class="fas fa-unlock hide" style="color: green"></i>
				</div>
			</div>
			<div style="font-size: 18px; top: 0px; right: 10px; text-align: right; position: absolute; color: white;" id="theclock"></div>
			<?php if ($rfidaktold > 0) { ?>
				<div class="btn-lg btn-dark" style="top: 50px; right: 10px; position: absolute; cursor: pointer; font-size: 32px;" id="code1">
					<i class="fa fa-fw fa-calculator" aria-hidden="true"></i>
				</div>
			<?php } ?>
		</div>

		<!-- modal code-window -->
		<div class="modal" id="codeModal">
			<div class="modal-dialog">
				<div class="modal-content">
					<!-- modal header -->
					<div class="modal-header bg-warning">
						<div class="col-1">&nbsp;</div>
						<div class="col justify-content-center">
							<div class="modal-title text-dark text-center">Code zur Freischaltung eingeben</div>
						</div>
						<div class="col-1 pr-0">
							<button type="button" class="btn btn-dark btn-lg" data-dismiss="modal"><i class="fas fa-times"></i></button>
						</div>
					</div>
					<!-- modal body -->
					<div class="modal-body">
						<div id="PINcode" class="text-center">
							<input id="PINbox" type="text" value="" name="PINbox" disabled="disabled">
							<br>
							<input type="button" class="PINbutton" name="1" value="1" id="1" onclick="addNumber(this);">
							<input type="button" class="PINbutton" name="2" value="2" id="2" onclick="addNumber(this);">
							<input type="button" class="PINbutton" name="3" value="3" id="3" onclick="addNumber(this);">
							<br>
							<input type="button" class="PINbutton" name="4" value="4" id="4" onclick="addNumber(this);">
							<input type="button" class="PINbutton" name="5" value="5" id="5" onclick="addNumber(this);">
							<input type="button" class="PINbutton" name="6" value="6" id="6" onclick="addNumber(this);">
							<br>
							<input type="button" class="PINbutton" name="7" value="7" id="7" onclick="addNumber(this);">
							<input type="button" class="PINbutton" name="8" value="8" id="8" onclick="addNumber(this);">
							<input type="button" class="PINbutton" name="9" value="9" id="9" onclick="addNumber(this);">
							<br>
							<input type="button" class="PINbutton clear" name="-" value="clear" id="-" onclick="clearForm(this);">
							<input type="button" class="PINbutton" name="0" value="0" id="0" onclick="addNumber(this);">
							<input type="button" class="PINbutton enter" name="+" value="OK" id="+" onclick="submitForm(PINbox);">
						</div>
					</div> <!-- /modal body -->
				</div>
			</div>
			<script>
				function addNumber(e){
					var v = $( "#PINbox" ).val();
					$( "#PINbox" ).val( v + e.value );
				}

				function clearForm(e){
					$( "#PINbox" ).val( "" );
				}

				function submitForm(e) {
					publish( e.value, "openWB/set/system/SimulateRFID" );
					$( "#PINbox" ).val( "" );
					$("#codeModal").modal("hide");
				};
			</script>
		</div>

		<script>
			function startTime() {
				var today = new Date();
				var h = today.getHours();
				var m = today.getMinutes();
				m = checkTime(m);
				document.getElementById('theclock').innerHTML =
				h + ":" + m;
				var t = setTimeout(startTime, 5000);
			}

			function checkTime(i) {
				if (i < 10) {
					i = "0" + i
				};  // add zero in front of numbers < 10
				return i;
			}

			startTime();

			var displaylp1max = <?php echo trim($displaylp1maxold); ?>;
			// var displaylp2max = <?php echo trim($displaylp2maxold); ?>;
			var displaypincode = <?php echo trim($displaypincodeold); ?>;
			var displaypinaktiv = <?php echo trim($displaypinaktivold); ?>;
			var rfidakt = <?php echo trim($rfidaktold); ?>;
			var isssakt = <?php echo trim($isssold); ?>;
		</script>
		<script src="display/minimal/minimalgauge.js?ver=20220510"></script>
		<script>
			// ************** beginning of MQTT code *************
			$(document).ready(function(){

				// load scripts synchronously in order specified
				var scriptsToLoad = [
					// load mqtt library
					'js/mqttws31.js',
					// functions for processing messages
					'display/minimal/processAllMqttMsg.js?ver=20220510',
					// functions performing mqtt and start mqtt-service
					'display/minimal/setupMqttServices.js?ver=20220510',
				];

				scriptsToLoad.forEach(function(src) {
					var script = document.createElement('script');
					script.src = src;
					script.async = false;
					document.body.appendChild(script);
				});

				$('#code1').on("click", function(event){
					console.log("code button clicked");
					$("#codeModal").modal("show");
				});
			});
		</script>
	</body>
</html>
