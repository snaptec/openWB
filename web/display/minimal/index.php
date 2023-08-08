<!DOCTYPE html>
<html lang="de" class="theme-gray">

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
		<script src="themes/colors/js/d3.v6.min.js"></script>
		<script>
			$(document).ready(function() {
				/**
				 * detect touch devices and map contextmenu (long press) to normal click
				 */
				$('body').on("contextmenu", function(event) {
					if (('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) {
						$(event.target).trigger("click"); // fire a click event
						event.preventDefault();
					}
				});
			});
		</script>
	</head>

	<body onselectstart="return false">
		<!-- minimal.html -->
		<?php
			$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
			foreach($lines as $line) {
				list($key, $value) = explode("=", $line, 2);
				${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
			}
		?>

		<script src="display/minimal/gauge.js?ver=20230106"></script>
		<link rel="stylesheet" href="display/minimal/minimal.css?ver=20230501">
		<script src="display/minimal/pricechart.js?ver=20230501"></script>

		<div id="main">
			<!-- <div id="800x480_Frame" style="position: absolute; top: 0px; left: 0px; height: 480px; width: 800px; border:1px solid white;"> </div> -->
			<div id="800x480_Frame" style="position: absolute; top: 0px; left: 0px; height: 480px; width: 800px;">
				<?php if ($lastmanagementold == 1) { ?>
					<div id="gaugedivlp1" style="position: absolute; top: 10px; left: 10px; height: 460px; width: 380px;">
						<canvas id="lp1" style="height: 400px; top: 30px; left: 0px; position: absolute; width: 740px;"></canvas>
						<canvas id="lp1s" style="height: 400px; top: 30px; left: 0px; position: absolute; width: 740px;"></canvas>
						<div id="lp1l" style="font-size: 35px; top: 405px; left: 0px; text-align:center; position: absolute; width: 380px; color: white;">LP1</div>
						<div id="lp1st" style="font-size: 35px; top: 245px; right: 10px; text-align:right; position: absolute; width: 135px; color: white;">0</div>
						<div id="lp1t" style="font-size: 35px; top: 295px; right: 10px; text-align:right; position: absolute; width: 145px; color: white;">0</div>
						<div id="lp1symbol" style="top: 350px; right: 10px; text-align: right; position: absolute; width: 150px; font-size: 32px;">
							<i id="lp1plugstat" class="fas fa-plug" style="font-size: 32px"></i>
							<i id="lp1disabled" class="fas fa-lock text-danger"></i>
							<i id="lp1enabled" class="fas fa-unlock text-success hide"></i>
						</div>
					</div>
					<div id="gaugedivlp2" style="position: absolute; top: 10px; left: 410px; height: 460px; width: 380px;">
						<canvas id="lp2" style="height: 400px; top: 30px; left: -360px; position: absolute; width: 740px;"></canvas>
						<canvas id="lp2s" style="height: 400px; top: 30px; left: -360px; position: absolute; width: 740px;"></canvas>
						<div id="lp2l" style="font-size: 35px; top: 405px; right: 30px; text-align:center; position: absolute; width: 380px; color: white;">LP2</div>
						<div id="lp2st" style="font-size: 35px; top: 245px; left: 10px; text-align:left; position: absolute; width: 135px; color: white;">0</div>
						<div id="lp2t" style="font-size: 35px; top: 295px; left: 10px; text-align:left; position: absolute; width: 145px; color: white;">0</div>
						<div id="lp2symbol" style="top: 350px; left: 10px; text-align: left; position: absolute; width: 135px; font-size: 32px;">
							<i id="lp2disabled" class="fas fa-lock text-danger"></i>
							<i id="lp2enabled" class="fas fa-unlock text-success hide"></i>
							<i id="lp2plugstat" class="fas fa-plug"></i>
						</div>
					</div>
				<?php } else { ?>
					<div id="gaugedivlp1" style="position: absolute; top: 10px; left: 10px; height: 460px; width: 780px;">
						<canvas id="lp1" style="height: 400px; top: 30px; left: 0px; position: absolute; width: 780px;"></canvas>
						<canvas id="lp1s" style="height: 400px; top: 30px; left: 0px; position: absolute; width: 780px;"></canvas>
						<div id="lp1st" style="font-size: 35px; top: 230px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
						<div id="lp1t" style="font-size: 35px; top: 290px; left: 265px; text-align:center; position: absolute; width: 265px; color: white;">0</div>
						<div id="lp1symbol" style="top: 350px; left: 265px; text-align: center; position: absolute; width: 265px; font-size: 32px;">
							<i id="lp1plugstat" class="fas fa-plug"></i>
							<i id="lp1disabled" class="fas fa-lock text-danger"></i>
							<i id="lp1enabled" class="fas fa-unlock text-success hide"></i>
						</div>
					</div>
				<?php } ?>
				<div style="font-size: 18px; bottom: 10px; right: 10px; text-align: center; width: 60px; position: absolute; color: white;" id="theclock"></div>
				<?php if ($rfidaktold > 0 && $displayshowrfidpadold > 0) { ?>
					<div class="btn-lg btn-dark" style="top: 20px; right: 20px; position: absolute; cursor: pointer; font-size: 32px;" id="rfidcode">
						<i class="fa fa-fw fa-id-card" aria-hidden="true"></i>
					</div>
				<?php } ?>
				<?php if ($displaypinaktivold > 0) { ?>
					<div class="btn-lg btn-dark" style="top: 98px; right: 20px; position: absolute; cursor: pointer; font-size: 32px;" id="displaylock">
						<i class="fa fa-fw fa-lock text-danger" aria-hidden="true"></i>
						<i class="fa fa-fw fa-unlock text-success hide" aria-hidden="true"></i>
					</div>
				<?php } ?>
				<?php if ($displayshowpriceold > 0) { ?>
					<div id="currentPrice" style="top: 10px; left: 20px; position: absolute; font-size: 32px; color: white;" class="hide">Preis: 25 ct/kWh</div>
					<div id="etPriceLimitLp1" style="top: 50px; left: 20px; position: absolute; font-size: 14px; color: white;" class="text-success">Limit LP1: 95 ct/kWh</div>
					<div id="etPriceLimitLp2" style="top: 70px; left: 20px; position: absolute; font-size: 14px; color: white;" class="text-success">Limit LP2: 95 ct/kWh</div>
					<div class="btn-lg btn-dark" style="top: 98px; left: 20px; position: absolute; cursor: pointer; font-size: 32px;" id="etsetprice">
						<i class="fa fa-fw fa-wallet" aria-hidden="true"></i>
					</div>
				<?php } ?>
			</div>
		</div>

		<!-- modal ET-window -->
		<div class="modal" id="etModal">
			<div class="modal-dialog">
				<div class="modal-content">
					<!-- modal header -->
					<div class="modal-header bg-primary">
						<div class="col-1">&nbsp;</div>
						<div class="col justify-content-center">
							<div class="modal-title text-white text-center" style="font-size: 28px">Preislimit</div>
						</div>
						<div class="col-1 pr-0">
							<button type="button" class="btn btn-dark btn-lg" data-dismiss="modal"><i class="fas fa-times"></i></button>
						</div>
					</div>
					<!-- modal body -->
					<div class="modal-body bg-dark">
						<div class="row pt-4 pb-2 m-0 ">
							<div class="col"></div>
							<div class="col-12 pricechartColumn p-0 m-0">
								<figure id="priceChart"></figure>
							</div>
							<div class="col"></div>
						</div>
						<div class="form-row vaRow pt-2 pb-2 pl-3 m-0" id="etPriceSetLp1">
							<div class="col-4 m-0 p-0">
								<label for="maxPriceLp1" class="modalLabel maxPriceLabelName text-orange col-form-label p-0 m-0">LP1: </label>
								<label for="maxPriceLp1" class="modalLabel maxPriceLabelValue col-form-label pull-right p-0 mr-2"></label>
							</div>
							<div class="col pr-3 pt-1">
								<input type="range" class="form-control-range maxPriceInput" id="maxPriceLp1" min="-25" max="95" step="0.1" value="0" data-initialized="0">
							</div>
						</div>
						<div class="form-row vaRow pt-2 pb-2 pl-3 m-0" id="etPriceSetLp2">
							<div class="col-4 m-0 p-0">
								<label for="maxPriceLp2" class="modalLabel maxPriceLabelName text-orangered col-form-label p-0 m-0">LP2: </label>
								<label for="maxPriceLp2" class="modalLabel maxPriceLabelValue col-form-label pull-right p-0 mr-2"></label>
							</div>
							<div class="col pr-3 pt-1">
								<input type="range" class="form-control-range maxPriceInput" id="maxPriceLp2" min="-25" max="95" step="0.1" value="0" data-initialized="0">
							</div>
						</div>
						<div class="form-row vaRow pt-2 pb-2 pl-3 m-0 hide"  id="etCombineSelection">
							<div class="col-md-4">
								<label class="col-form-label">Auswahl</label>
							</div>
							<div class="col">
								<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
									<label class="btn btn-lg btn-outline-info active">
										<input type="radio" name="etCombinePrice" id="etCombinePriceOff" value="0" checked>Individuell
									</label>
									<label class="btn btn-lg btn-outline-info">
										<input type="radio" name="etCombinePrice" id="etCombinePriceOn" value="1">Gemeinsam
									</label>
								</div>
							</div>
						</div>
						<div class="col pt-2 px-3">
							<button type="button" class="btn btn-info btn-block btn-lg modal-button" data-dismiss="modal"><i class="fas fa-check"></i>&nbsp;&nbsp; OK</button>
						</div>
					</div> <!-- /modal body -->
				</div>
			</div>
		</div>

		<!-- modal code-window -->
		<div class="modal" id="codeModal">
			<div class="modal-dialog">
				<div class="modal-content">
					<!-- modal header -->
					<div class="modal-header bg-primary">
						<div class="col-1">&nbsp;</div>
						<div class="col justify-content-center">
							<div class="modal-title text-white text-center" style="font-size: 28px">Fahrzeugcode (RFID)</div>
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
				function addNumber(e) {
					var v = $("#PINbox").val();
					$("#PINbox").val(v + e.value);
				}

				function clearForm(e) {
					$("#PINbox").val("");
				}

				function submitForm(e) {
					publish(e.value, "openWB/set/system/SimulateRFID");
					$("#PINbox").val("");
					$("#codeModal").modal("hide");
				};
			</script>
		</div>

		<!-- modal lock-window -->
		<div class="modal" id="lockModal">
			<div class="modal-dialog">
				<div class="modal-content">
					<!-- modal header -->
					<div class="modal-header bg-warning">
						<div class="col-1">&nbsp;</div>
						<div class="col justify-content-center">
							<div class="modal-title text-dark text-center" style="font-size: 28px">PIN</div>
						</div>
						<div class="col-1 pr-0">
							<button type="button" class="btn btn-dark btn-lg" data-dismiss="modal"><i class="fas fa-times"></i></button>
						</div>
					</div>
					<!-- modal body -->
					<div class="modal-body">
						<div id="Lockcode" class="text-center">
							<input id="Lockbox" type="password" value="" name="Lockbox" disabled="disabled"
								class="text-center display-4" size="4">
							<br>
							<input type="button" class="PINbutton" name="1" value="1" onclick="addLockNumber(this);">
							<input type="button" class="PINbutton" name="2" value="2" onclick="addLockNumber(this);">
							<input type="button" class="PINbutton" name="3" value="3" onclick="addLockNumber(this);">
							<br>
							<input type="button" class="PINbutton" name="4" value="4" onclick="addLockNumber(this);">
							<input type="button" class="PINbutton" name="5" value="5" onclick="addLockNumber(this);">
							<input type="button" class="PINbutton" name="6" value="6" onclick="addLockNumber(this);">
							<br>
							<input type="button" class="PINbutton" name="7" value="7" onclick="addLockNumber(this);">
							<input type="button" class="PINbutton" name="8" value="8" onclick="addLockNumber(this);">
							<input type="button" class="PINbutton" name="9" value="9" onclick="addLockNumber(this);">
							<br>
							<input type="button" class="PINbutton clear" name="-" value="clear" onclick="clearLockForm(this);">
							<input type="button" class="PINbutton" name="0" value="0" onclick="addLockNumber(this);">
							<input type="button" class="PINbutton enter" name="+" value="enter" onclick="submitLockForm(Lockbox);">
						</div>
					</div> <!-- /modal body -->
				</div>
			</div>
			<script>
				function addLockNumber(e) {
					var v = $("#Lockbox").val();
					$("#Lockbox").val(v + e.value);
				}

				function clearLockForm(e) {
					$("#Lockbox").val("");
				}

				function submitLockForm(e) {
					$.get(
						{ url: "display/minimal/checklock.php?pin=" + $('#Lockbox').val(), cache: false },
						function (data) {
							if (data == 1) {
								lockDisplay(false);
								$('#lockModal').find('.modal-body').addClass('bg-success');
								$('#Lockcode').find('.enter').prop('disabled', true);
								window.setTimeout(function () {
									$('#lockModal').find('.modal-body').removeClass('bg-success');
									$('#Lockcode').find('.enter').prop('disabled', false);
									$("#Lockbox").val("");
									$("#lockModal").modal("hide");
								}, 1000);
							} else {
								$('#lockModal').find('.modal-body').addClass('bg-danger');
								$('#Lockcode').find('.enter').prop('disabled', true);
								window.setTimeout(function () {
									$('#lockModal').find('.modal-body').removeClass('bg-danger');
									$('#Lockcode').find('.enter').prop('disabled', false);
									$("#Lockbox").val("");
								}, 3000);
							}
						}
					);
				};
			</script>
		</div>

		<!-- modal lock-info-window -->
		<div class="modal" id="lockInfoModal">
			<div class="modal-dialog">
				<div class="modal-content">
					<!-- modal header -->
					<div class="modal-header bg-warning">
						<div class="col-1">&nbsp;</div>
						<div class="col justify-content-center">
							<div class="modal-title text-center">Display gesperrt</div>
						</div>
						<div class="col-1 pr-0">
							<button type="button" class="btn btn-dark btn-lg" data-dismiss="modal"><i class="fas fa-times"></i></button>
						</div>
					</div>
					<!-- modal body -->
					<div class="modal-body">
						<h4 class="text-light text-center">
							Das Display ist mit einem PIN-Code gesperrt.<br>
							Bitte tippen Sie links unten auf das <i class="fas fa-lock text-danger"></i> und
							geben den
							richtigen PIN ein.
						</h4>
					</div>
					<!-- modal footer -->
					<div class="modal-footer justify-content-center">
						<div class="row">
							<div class="col text-center">
								<button type="button" class="btn btn-lg btn-secondary" data-dismiss="modal">
									OK
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<script>
			function startTime() {
				var today = new Date();
				var h = today.getHours();
				var m = today.getMinutes();
				m = checkTime(m);
				document.getElementById('theclock').innerHTML =	h + ":" + m;
				var t = setTimeout(startTime, 5000);
			}

			function checkTime(i) {
				if (i < 10) {
					i = "0" + i
				}; // add zero in front of numbers < 10
				return i;
			}

			startTime();

			// settings specific for this WB (not available via mqtt in externalWB mode)
			var displaylp1max = <?php echo $displaylp1maxold; ?>;
			var displaylp2max = <?php echo $displaylp2maxold; ?>;
			var isDUO = <?php echo $lastmanagementold; ?>;
			var showPrice = <?php echo $displayshowpriceold; ?>;
			var showRfidPad = <?php echo $displayshowrfidpadold; ?>;
			var allowSetMaxPrice = <?php echo $displayallowsetmaxpriceold; ?>;
			var displaylocked = <?php echo $displaypinaktivold; ?>;
			var defaultPrice = <?php echo $preisjekwhold; ?> * 100;

			// externalWB mode - available via mqtt
			var parentWB = "localhost";
			var parentCP = [1 , 2];

			// price based charging related settings, will also get handed over
			// from parent in externalWB mode
			var etEnabled = 0;
			var etMaxPricesLocal = [0 , 0];
			var etMaxPricesFinal = [0 , 0];
			var etMaxPriceGlobal = 0;
			var etModes = [0 , 0];
			var etCurrentPrice = 0;
			var etPriceList = "";

			// internal variables
			var etParentLocalPriceUpdated = [0, 0];
			var etParentGlobalPriceUpdated = 0;
			var maxPriceDelayTimers = [null, null];
			var lockTimeoutHandler = null;
			var lockTimeout = 60000;

			if (isDUO == 1) {
				configuredChargePoints = 2;
			} else {
				configuredChargePoints = 1;
			}

			function lockDisplay(lock = true) {
				if (lock == false) {
					displaylocked = 0;
					$('#displaylock').find('.fa-lock').addClass('hide');
					$('#displaylock').find('.fa-unlock').removeClass('hide');
					lockTimeoutHandler = window.setTimeout(lockDisplay, lockTimeout);
				} else {
					displaylocked = 1;
					$('#displaylock').find('.fa-lock').removeClass('hide');
					$('#displaylock').find('.fa-unlock').addClass('hide');

					window.clearTimeout(lockTimeoutHandler);
					lockTimeoutHandler = null;
				}
			}

		</script>
		<script src="display/minimal/minimalgauge.js?ver=20230501"></script>
		<script>
			// ************** beginning of MQTT code *************
			$(document).ready(function() {

				// load scripts synchronously in order specified
				var scriptsToLoad = [
					// load mqtt library
					'js/mqttws31.js',
					// functions for processing messages
					'display/minimal/processAllMqttMsg.js?ver=20230501',
					// functions performing mqtt and start mqtt-service
					'display/minimal/setupMqttServices.js?ver=20230501',
				];

				scriptsToLoad.forEach(function(src) {
					var script = document.createElement('script');
					script.src = src;
					script.async = false;
					document.body.appendChild(script);
				});

				if (allowSetMaxPrice == 0) {
					$("#etCombineSelection").addClass("hide");
					$("#etCombinePriceOff").attr('disabled', true);
					$("#etCombinePriceOn").attr('disabled', true);
					$("#maxPriceLp1").attr('disabled', true);
					$("#maxPriceLp2").attr('disabled', true);
				}

				priceChart.init();
				updateMainPriceLabels();
				updateSetPriceLabels();
				$('#maxPriceLp1').val(etMaxPricesLocal[0]);
				$('#maxPriceLp2').val(etMaxPricesLocal[1]);

				$('#rfidcode').on("click", function(event) {
					$("#codeModal").modal("show");
				});

				$('input[type=radio][name=etCombinePrice]').change(function(){
					if ($('input[type="radio"][name="etCombinePrice"]:checked').val() == 1) {
						$("#maxPriceLp2").attr('disabled', true);
						$("#maxPriceLp2").val($("#maxPriceLp1").val());
						$("#maxPriceLp2").trigger("input");
					} else {
						$("#maxPriceLp2").attr('disabled', false);
					}
				});

				$('#etsetprice').on("click", function(event) {
					if (displaylocked == 0) {
						$("#etModal").modal("show");
					}else {
						$("#lockInfoModal").modal("show");
					}
				});

				$('#displaylock').on("click", function () {
					if (displaylocked == 1) {
						$("#lockModal").modal("show");
					} else {
						lockDisplay(true);
					}
				});

				$('.maxPriceInput').on('input', function() {

					var elementId = $(this).attr('id');
					var element = $('#' + $.escapeSelector(elementId));
					var value = element.val();
					var label = $('label[for="' + elementId + '"].maxPriceLabelValue');
					var index = elementId.match(/\d+$/);
					var imm = index - 1;

					if ($('input[type="radio"][name="etCombinePrice"]:checked').val() == 1 && index == 1) {
						$("#maxPriceLp2").val($("#maxPriceLp1").val());
						$("#maxPriceLp2").trigger("input");
					}

					if (etModes[imm] == 1) {
						etMaxPriceGlobal = parseFloat(value);
					} else {
						etMaxPricesLocal[imm] = parseFloat(value);
					}

					updateMainPriceLabels();
					updateSetPriceLabels();
					label.addClass('text-danger');
					if (maxPriceDelayTimers[imm]) {
						clearTimeout(maxPriceDelayTimers[imm]);
					}
					maxPriceDelayTimers[imm] = setTimeout(() => {
						label.removeClass('text-danger');
						if (etModes[imm] == 1) {
							if (parentWB == "localhost") {
								publish(value, "openWB/set/awattar/MaxPriceForCharging" );
							} else {
								etParentGlobalPriceUpdated = Date.now();
								publishToParent(value, "openWB/set/awattar/MaxPriceForCharging" );
							}
						} else {
							if (parentWB == "localhost") {
								publish(value, "openWB/config/set/sofort/lp/" + index + "/etChargeMaxPrice" );
							} else {
								etParentLocalPriceUpdated[imm] = Date.now();
								publishToParent(value, "openWB/config/set/sofort/lp/" + parentCP[imm] + "/etChargeMaxPrice" );
							}
						}
						maxPriceDelayTimers[imm] = null;
					}, 2000)

				});
			});
		</script>
	</body>

</html>
