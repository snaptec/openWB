<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
		<title>openWB Einstellungen</title>
		<meta name="description" content="Control your charge" />
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
		<link rel="stylesheet" type="text/css" href="css/settings_style.css?ver=20200416-a">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
	</head>

	<body>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">

			<form id="myForm">
				<h1>Einstellungen für Sofortladen</h1>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						 Allgemeine Einstellungen
					</div>
					<div class="card-body">
						<div class="form-group mb-0">
							<div class="form-row mb-0">
								<div class="col-md-4">
									Mindeststromstärke
								</div>
								<div class="col">
									<span class="form-text small">Parameter in Ampere [A] für den minimalen Strom im Modus Sofortladen. Definiert den minimalen Ladestrom an allen Ladepunkten. Einige EV benötigen einen Mindestladestrom, da ansonsten die Ladung nicht startet. Der kleinste einstellbare Wert liegt aus technischen Gründen bei 6 A.</span>
								</div>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="minEVSECurrentAllowed" class="col-md-4 col-form-label">alle Ladepunkte</label>
							<div class="col-md-8">
								<div class="form-row vaRow mb-1">
									<label for="minEVSECurrentAllowed" class="col-2 col-form-label valueLabel" suffix="A">A</label>
									<div class="col-10">
										<input type="range" class="form-control-range rangeInput" name="minEVSECurrentAllowed" id="minEVSECurrentAllowed" min="6" max="16" step="1" value="6" data-default="6" data-topicprefix="openWB/config/get/global/">
									</div>
								</div>
							</div>
						</div>
					</div>  <!-- end card body Allgemeine Einstellungen Sofort -->
				</div>  <!-- end card Allgemeine Einstellungen Sofort -->

				<?php for( $chargepoint = 1; $chargepoint < 9; $chargepoint++ ){ // begin chargepoint loop ?>
					<div class="card border-primary lp<?php echo $chargepoint; ?>options<?php if( $chargepoint > 1 ) echo " hide"; ?>">
						<div class="card-header bg-primary">
							Einstellungen Ladepunkt <?php echo $chargepoint; ?>
						</div>
						<div class="card-body">
							<div class="form-row mb-1">
								<label for="currentLp<?php echo $chargepoint; ?>" class="col-md-4 col-form-label">Ladestrom</label>
								<div class="col-md-8">
									<div class="form-row vaRow mb-1">
										<label for="currentLp<?php echo $chargepoint; ?>" class="col-2 col-form-label valueLabel" suffix="A">A</label>
										<div class="col-10">
											<input type="range" class="form-control-range rangeInput" name="current" id="currentLp<?php echo $chargepoint; ?>" min="6" max="32" step="1" value="16" data-default="16" data-topicprefix="openWB/config/get/sofort/" data-topicsubgroup="lp/<?php echo $chargepoint; ?>/">
										</div>
									</div>
									<span class="form-text small">Parameter in Ampere [A] für den Ladestrom im Modus Sofortladen. Definiert den Ladestrom am Ladepunkt. Der kleinste einstellbare Wert liegt aus technischen Gründen bei 6 A, der größte bei 32 A. Er kann nie kleiner sein als die eingestellte Mindeststromstärke an den Ladepunkten.</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Begrenzung</label>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" id="chargeLimitationLp<?php echo $chargepoint; ?>" name="chargeLimitation" data-toggle="buttons" data-default="0" data-topicprefix="openWB/config/get/sofort/" data-topicsubgroup="lp/<?php echo $chargepoint; ?>/">
										<label class="btn btn-outline-info btn-toggle">
											<input type="radio" name="chargeLimitationLp<?php echo $chargepoint; ?>" data-option="0" value="0"> keine
										</label>
										<?php if( $chargepoint <= 2 ){ ?>
										<label class="btn btn-outline-info btn-toggle lp<?php echo $chargepoint; ?>socoptions">
											<input type="radio" name="chargeLimitationLp<?php echo $chargepoint; ?>" data-option="2" value="2"> EV-SoC
										</label>
										<?php } ?>
										<label class="btn btn-outline-info btn-toggle">
											<input type="radio" name="chargeLimitationLp<?php echo $chargepoint; ?>" data-option="1" value="1"> Energiemenge
										</label>
									</div>
									<span class="form-text small">Auswahl der Lademengen-Begrenzung im Modus Sofortladen.
										<span class="text-danger">
											Dieser Parameter kann auf der Hauptseite der openWB per Sofortzugriff im Modus Sofortladen jederzeit geändert werden.
										</span>
									</span>
								</div>
							</div>
							<div class="form-group mb-0 lp<?php echo $chargepoint; ?>limitenergy hide">
								<div class="form-row mb-1">
									<label for="energyToChargeLp<?php echo $chargepoint; ?>" class="col-md-4 col-form-label">Energie</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="energyToChargeLp<?php echo $chargepoint; ?>" class="col-2 col-form-label valueLabel" suffix="kWh">kWh</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="energyToCharge" id="energyToChargeLp<?php echo $chargepoint; ?>" min="2" max="100" step="2" value="30" data-default="30" data-topicprefix="openWB/config/get/sofort/" data-topicsubgroup="lp/<?php echo $chargepoint; ?>/">
											</div>
										</div>
										<span class="form-text small">
											Parameter in Kilowattstunden [kWh] für die Lademengenbegrenzung im Modus Sofortladen. Definiert die Energiemenge, auf die der Ladevorgang begrenzt werden soll.
											<span class="text-danger">
												Dieser Parameter kann auf der Hauptseite der openWB per Sofortzugriff im Modus Sofortladen jederzeit geändert werden.
											</span>
										</span>
									</div>
								</div>
							</div>
							<?php if( $chargepoint <= 2 ){ ?>
							<div class="form-group mb-0 lp<?php echo $chargepoint; ?>limitsoc hide">
								<div class="form-row mb-1">
									<label for="socToChargeToLp<?php echo $chargepoint; ?>" class="col-md-4 col-form-label">SoC</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="socToChargeToLp<?php echo $chargepoint; ?>" class="col-2 col-form-label valueLabel" suffix="%">%</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="socToChargeTo" id="socToChargeToLp<?php echo $chargepoint; ?>" min="5" max="100" step="5" value="90" data-default="90" data-topicprefix="openWB/config/get/sofort/" data-topicsubgroup="lp/<?php echo $chargepoint; ?>/">
											</div>
										</div>
										<span class="form-text small">
											Parameter in Prozent [%] für die Lademengenbegrenzung im Modus Sofortladen. Definiert den EV-SoC, bei dessen Überschreitung die Ladung gestoppt wird.
											<span class="text-danger">
												Dieser Parameter kann auf der Hauptseite der openWB per Sofortzugriff im Modus Sofortladen jederzeit geändert werden.
											</span>
										</span>
									</div>
								</div>
							</div>
							<?php } ?>
						</div>  <!-- end card body Einstellungen Ladepunkt <?php echo $chargepoint; ?> -->
						<script>
							$(document).ready(function(){
								$('input[type=radio][name=chargeLimitationLp<?php echo $chargepoint; ?>]').change(function(){
									if(this.value == '0') {
										hideSection('.lp<?php echo $chargepoint; ?>limitenergy');
										<?php if( $chargepoint <= 2 ){ ?>
										hideSection('.lp<?php echo $chargepoint; ?>limitsoc');
										<?php } ?>
									} else {
										if(this.value == 1) {
											showSection('.lp<?php echo $chargepoint; ?>limitenergy');
											<?php if( $chargepoint <= 2 ){ ?>
											hideSection('.lp<?php echo $chargepoint; ?>limitsoc');
											<?php } ?>
										} else {
											hideSection('.lp<?php echo $chargepoint; ?>limitenergy');
											<?php if( $chargepoint <= 2 ){ ?>
											showSection('.lp<?php echo $chargepoint; ?>limitsoc');
											<?php } ?>
										}
									}
								})
							});
						</script>
					</div>  <!-- end card Einstellungen Ladepunkt <?php echo $chargepoint; ?> -->

				<?php } // end chargepoint loop ?>

				<div class="row justify-content-center">
					<div class="col-3">
						<button id="saveSettingsBtn" type="button" class="btn btn-success">speichern</button>
					</div>
					<div class="col-1">
						&nbsp;
					</div>
					<div class="col-3">
						<button id="modalDefaultsBtn" type="button" class="btn btn-danger">Werkseinstellungen</button>
					</div>
				</div>
			</form>

			<!-- modal set-defaults-confirmation window -->
			<div class="modal fade" id="setDefaultsConfirmationModal" role="dialog">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<!-- modal header -->
						<div class="modal-header bg-danger">
							<h4 class="modal-title text-light">Achtung</h4>
						</div>
						<!-- modal body -->
						<div class="modal-body text-center">
							<p>
								Sollen für den Lademodus Sofortladen wirklich die Werkseinstellungen eingestellt werden?
							</p>
						</div>
						<!-- modal footer -->
						<div class="modal-footer d-flex justify-content-center">
							<button type="button" class="btn btn-success" data-dismiss="modal" id="saveDefaultsBtn">Fortfahren</button>
							<button type="button" class="btn btn-danger" data-dismiss="modal">Abbruch</button>
						</div>
					</div>
				</div>
			</div>

			<!-- modal set-defaults-confirmation window -->
			<div class="modal fade" id="formNotValidModal" role="dialog">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<!-- modal header -->
						<div class="modal-header bg-danger">
							<h4 class="modal-title text-light">Fehler</h4>
						</div>
						<!-- modal body -->
						<div class="modal-body text-center">
							<p>
								Es wurden fehlerhafte Eingaben gefunden, speichern ist nicht möglich! Bitte überprüfen Sie alle Eingaben.
							</p>
						</div>
						<!-- modal footer -->
						<div class="modal-footer d-flex justify-content-center">
							<button type="button" class="btn btn-primary" data-dismiss="modal">Schließen</button>
						</div>
					</div>
				</div>
			</div>

			<!-- modal no-values-changed window -->
			<div class="modal fade" id="noValuesChangedInfoModal" role="dialog">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<!-- modal header -->
						<div class="modal-header bg-info">
							<h4 class="modal-title text-light">Info</h4>
						</div>
						<!-- modal body -->
						<div class="modal-body text-center">
							<p>
								Es wurden keine geänderten Einstellungen gefunden.
							</p>
						</div>
						<!-- modal footer -->
						<div class="modal-footer d-flex justify-content-center">
							<button type="button" class="btn btn-success" data-dismiss="modal">Ok</button>
						</div>
					</div>
				</div>
			</div>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Ladeeinstellungen/Sofortladen</small>
			</div>
		</footer>

		<!-- load mqtt library -->
		<script src = "js/mqttws31.js" ></script>
		<!-- load topics -->
		<script src = "settings/topicsToSubscribe_sofortconfig.js?ver=20200503-a" ></script>
		<!-- load service -->
		<script src = "settings/setupMqttServices.js?ver=20200424-a" ></script>
		<!-- load mqtt handler-->
		<script src = "settings/processAllMqttMsg.js?ver=20200505-a" ></script>

		<script>

			$.get(
				{ url: 'settings/navbar.html', cache: false },
				function(data){
					$('#nav').replaceWith(data);
					// disable navbar entry for current page
					$('#navSofortLadeeinstellungen').addClass('disabled');
				}
			);
			function visibiltycheck(elementId, mqttpayload) {
				// do visiblity check here
				if ( elementId.match( /^boolChargePointConfiguredLp[1-9]*$/i ) ) {
					var index = elementId.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
					// now call functions or set variables corresponding to the index
					if ( mqttpayload == 1) {
						showSection('.lp' + index + 'options');
					} else {
						hideSection('.lp' + index + 'options');
					}
				}
				if ( elementId.match( /^boolSocConfiguredLp[1-9]*$/i ) ) {
					var index = elementId.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
					// now call functions or set variables corresponding to the index
					if ( mqttpayload == 1) {
						showSection('.lp' + index + 'socoptions');
					} else {
						hideSection('.lp' + index + 'socoptions');
					}
				}
				if ( elementId.match( /^chargeLimitationLp[1-2]*$/i ) ) {
					var index = elementId.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
					// now call functions or set variables corresponding to the index
					if ( mqttpayload == 0) {
						hideSection('.lp' + index + 'limitenergy');
						hideSection('.lp' + index + 'limitsoc');
					} else {
						if ( mqttpayload == 1 ) {
							showSection('.lp' + index + 'limitenergy');
							hideSection('.lp' + index + 'limitsoc');
						} else {
							hideSection('.lp' + index + 'limitenergy');
							showSection('.lp' + index + 'limitsoc');
						}
					}
				}
				if ( elementId.match( /^chargeLimitationLp[3-8]*$/i ) ) {
					var index = elementId.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
					// now call functions or set variables corresponding to the index
					if ( mqttpayload == 0) {
						hideSection('.lp' + index + 'limitenergy');
					} else {
						showSection('.lp' + index + 'limitenergy');
					}
				}
			}
			function saveSettings() {
				// sends all changed values by mqtt if valid
				var formValid = $("#myForm")[0].checkValidity();
				if ( !formValid ) {
					$('#formNotValidModal').modal();
					return;
				};
				getChangedValues();
				sendValues();
			}

			$(document).ready(function(){

				$('input').blur(function(event) {
					// check input field on blur if value is valid
					if ( event.target.checkValidity() == false ) {
						$(this).addClass('is-invalid');
					} else {
						$(this).removeClass('is-invalid');
					}
				});

				$('#saveSettingsBtn').on("click",function() {
					saveSettings();
				});

				$('#modalDefaultsBtn').on("click",function() {
					$('#setDefaultsConfirmationModal').modal();
				});

				$('#saveDefaultsBtn').on("click",function() {
					// shown in confirmation modal
					// resets all values to defaults and sends all changed values by mqtt
					setToDefaults();
					getChangedValues();
					sendValues();
				});

				$('.rangeInput').on('input', function() {
					// show slider value in label of class valueLabel
					updateLabel($(this).attr('id'));
				});

			});  // end document ready function

		</script>

	</body>
</html>
