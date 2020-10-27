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
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css?ver=20200416-a">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
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
			// include special Theme style
			if( '' != themeCookie ){
				$('head').append('<link rel="stylesheet" href="themes/' + themeCookie + '/settings.css?v=20200801">');
			}
		</script>
	</head>

	<body>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">

			<form id="myForm">
				<h1>Einstellungen für SmartHome Geräte</h1>
<?php for( $devicenum = 1; $devicenum < 10; $devicenum++ ) { // Limited to devices 1-9 as device 10 is not properly implemented in various parts of the code ?>
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4" id="deviceHeader<?php echo $devicenum; ?>">Gerät <?php echo $devicenum; ?></div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" id="device_configuredDevices<?php echo $devicenum; ?>" name="device_configured" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<label class="btn btn-sm btn-outline-info">
											<input type="radio" name="device_configuredDevices<?php echo $devicenum; ?>" id="device_configuredDevices<?php echo $devicenum; ?>Off" data-option="0">Aus
										</label>
										<label class="btn btn-sm btn-outline-info">
											<input type="radio" name="device_configuredDevices<?php echo $devicenum; ?>" id="device_configuredDevices<?php echo $devicenum; ?>On" data-option="1">An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body" id="device<?php echo $devicenum; ?>options" style="display: none;">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="device_ipDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input id="device_ipDevices<?php echo $devicenum; ?>" name="device_ip" class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" data-default="192.168.1.1" value="192.168.1.1" inputmode="text"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="device_nameDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Name</label>
								<div class="col">
									<input id="device_nameDevices<?php echo $devicenum; ?>" name="device_name" class="form-control" type="text" minlength="3" maxlength="12" pattern="[a-zA-Z]*" inputmode="text" value="Name" data-default="Name" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									<span class="form-text small">Der Name muss aus 3-12 Zeichen bestehen und darf nur Buchstaben enthalten.</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Gerätetyp</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" id="device_typeDevices<?php echo $devicenum; ?>" name="device_type" data-toggle="buttons" data-default="shelly" value="shelly" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<label class="btn btn-outline-info">
											<input type="radio" name="device_typeDevices<?php echo $devicenum; ?>" id="device_typeDevices<?php echo $devicenum; ?>Shelly" data-option="shelly">Shelly
										</label>
										<label class="btn btn-outline-info">
											<input type="radio" name="device_typeDevices<?php echo $devicenum; ?>" id="device_typeDevices<?php echo $devicenum; ?>Tasmota" data-option="tasmota">Tasmota
										</label>
										<label class="btn btn-outline-info btn-toggle">
											<input type="radio" name="device_typeDevices<?php echo $devicenum; ?>" id="device_typeDevices<?php echo $devicenum; ?>Pyt" data-option="pyt"> Pyt
										</label>
									</div>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="device_mineinschaltdauerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Mindesteinschaltdauer</label>
								<div class="col">
									<input id="device_mineinschaltdauerDevices<?php echo $devicenum; ?>" name="device_mineinschaltdauer" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="10000" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									<span class="form-text small">Parameter in Minuten wie lange das Gerät nach Einschalten mindestens aktiviert bleibt.</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="device_maxeinschaltdauerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Maximaleinschaltdauer</label>
								<div class="col">
									<input id="device_maxeinschaltdauerDevices<?php echo $devicenum; ?>" name="device_maxeinschaltdauer" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="1500" data-default="1440" value="1440" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									<span class="form-text small">Parameter in Minuten wie lange das Gerät pro Tag maximal aktiviert sein darf. Der Zähler wird nächtlich zurückgesetzt. 1440 Minuten sind 24 Stunden.</span>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Bei Autoladen ausschalten</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" id="device_deactivateWhileEvChargingDevices<?php echo $devicenum; ?>" name="device_deactivateWhileEvCharging" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<label class="btn btn-outline-info">
											<input type="radio" name="device_deactivateWhileEvChargingDevices<?php echo $devicenum; ?>" id="device_deactivateWhileEvCharging<?php echo $devicenum; ?>0" data-option="0">Nein
										</label>
										<label class="btn btn-outline-info">
											<input type="radio" name="device_deactivateWhileEvChargingDevices<?php echo $devicenum; ?>" id="device_deactivateWhileEvCharging<?php echo $devicenum; ?>1" data-option="1">Ja
										</label>
									</div>
									<span class="form-text small">Gibt an ob der Aktor deaktiviert werden soll um mehr Überschuss für die EV Ladung zu erhalten. ACHTUNG! Nightly Feature!</span>
								</div>
							</div>
						</div>

						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="device_einschaltschwelleDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Einschaltschwelle</label>
								<div class="col">
									<div class="form-row vaRow">
										<div class="col-auto">
											<div class="custom-control custom-checkbox">
												<input class="custom-control-input" type="checkbox" id="device_einschaltschwelleDevices<?php echo $devicenum; ?>PosNeg" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<label class="custom-control-label" for="device_einschaltschwelleDevices<?php echo $devicenum; ?>PosNeg">
													negativ
												</label>
											</div>
										</div>
										<div class="col">
											<input id="device_einschaltschwelleDevices<?php echo $devicenum; ?>" name="device_einschaltschwelle" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="50000" data-default="1500" value="0" data-signcheckbox="device_einschaltschwelleDevices<?php echo $devicenum; ?>PosNeg" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										</div>
									</div>
									<span class="form-text small">Parameter in Watt [W] für das Einschalten des Gerätes. Steigt die <b>Einspeisung</b> über den Wert Einschaltschwelle, startet das Gerät. Wenn ein Speicher vorhanden ist, wird die Speicherleistung mit in den vorhanden Überschuss mit eingerechnet.</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="device_einschaltverzoegerungDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Einschaltverzögerung</label>
								<div class="col">
									<input id="device_einschaltverzoegerungDevices<?php echo $devicenum; ?>" name="device_einschaltverzoegerung" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="1000" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									<span class="form-text small">Parameter in Minuten der bestimmt wie lange die Einschaltschwelle <b>am Stück</b> überschritten werden muss bevor das Gerät eingeschaltet wird.</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="device_ausschaltschwelleDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Ausschaltschwelle</label>
								<div class="col">
									<div class="form-row vaRow">
										<div class="col-auto">
											<div class="custom-control custom-checkbox">
												<input class="custom-control-input" type="checkbox" id="device_ausschaltschwelleDevices<?php echo $devicenum; ?>PosNeg" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<label class="custom-control-label" for="device_ausschaltschwelleDevices<?php echo $devicenum; ?>PosNeg">
													negativ
												</label>
											</div>
										</div>
										<div class="col">
											<input id="device_ausschaltschwelleDevices<?php echo $devicenum; ?>" name="device_ausschaltschwelle" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="50000" data-default="1500" value="1500" data-signcheckbox="device_ausschaltschwelleDevices<?php echo $devicenum; ?>PosNeg" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										</div>
									</div>
									<span class="form-text small">Parameter in Watt [W] für das Ausschalten des Gerätes. Steigt der <b>Bezug</b> über den Wert Ausschaltschwelle, stoppt das Gerät. Wenn ein Speicher vorhanden ist, wird die Speicherleistung mit in den vorhanden Überschuss mit eingerechnet.</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="device_ausschaltverzoegerungDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Ausschaltverzögerung</label>
								<div class="col">
									<input id="device_ausschaltverzoegerungDevices<?php echo $devicenum; ?>" name="device_ausschaltverzoegerung" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="1000"  data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									<span class="form-text small">Parameter in Minuten der bestimmt wie lange die Ausschaltschwelle <b>am Stück</b> überschritten werden muss bevor das Gerät ausgeschaltet wird.</span>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="device_speichersocbeforestartDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Speicherbeachtung beim Einschalten</label>
								<div class="col-md-8">
									<div class="form-row vaRow mb-1">
										<label for="device_speichersocbeforestartDevices<?php echo $devicenum; ?>" class="col-2 col-form-label valueLabel" suffix="%"> %</label>
										<div class="col-10">
											<input type="range" class="form-control-range rangeInput" id="device_speichersocbeforestartDevices<?php echo $devicenum; ?>" name="device_speichersocbeforestart" min="0" max="100" step="5" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										</div>
									</div>
									<span class="form-text small">Parameter in % Ladezustand. Unterhalb dieses Wertes wird das Gerät nicht eingeschaltet. 0% deaktiviert die Funktion.</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="device_speichersocbeforestopDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Speicherbeachtung beim Ausschalten</label>
								<div class="col-md-8">
									<div class="form-row vaRow mb-1">
										<label for="device_speichersocbeforestopDevices<?php echo $devicenum; ?>" class="col-2 col-form-label valueLabel" suffix="%"> %</label>
										<div class="col-10">
											<input type="range" class="form-control-range rangeInput" id="device_speichersocbeforestopDevices<?php echo $devicenum; ?>" name="device_speichersocbeforestop" min="0" max="100" step="5" data-default="100" value="100" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										</div>
									</div>
									<span class="form-text small">Parameter in % Ladezustand. Überhalb dieses Wertes wird das Gerät nicht abgeschaltet. 100% deaktiviert die Funktion.</span>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Temperatursensoren</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>" name="device_temperatur_configured" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<label class="btn btn-outline-info">
											<input type="radio" name="device_temperatur_configuredDevices<?php echo $devicenum; ?>" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>0" data-option="0">0
										</label>
										<label class="btn btn-outline-info">
											<input type="radio" name="device_temperatur_configuredDevices<?php echo $devicenum; ?>" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>1" data-option="1">1
										</label>
										<label class="btn btn-outline-info">
											<input type="radio" name="device_temperatur_configuredDevices<?php echo $devicenum; ?>" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>2" data-option="2">2
										</label>
										<label class="btn btn-outline-info">
											<input type="radio" name="device_temperatur_configuredDevices<?php echo $devicenum; ?>" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>3" data-option="3">3
										</label>
									</div>
									<span class="form-text small">Anzahl der Temperatursensoren die an einem Shelly Unterputzgerät anschließbar sind.</span>
								</div>
							</div>
						</div>
					</div>  <!-- end card body Allgemeine Einstellungen Gerät <?php echo $devicenum; ?> -->
				</div>  <!-- end card Allgemeine Einstellungen Gerät <?php echo $devicenum; ?> -->
<?php } ?>

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
								Sollen für die Geräte wirklich die Werkseinstellungen eingestellt werden?
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

			<!-- modal form-not-valid window -->
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
				<small>Sie befinden sich hier: Ladeeinstellungen/Smart Home (Beta)</small>
			</div>
		</footer>

		<!-- load mqtt library -->
		<script src = "js/mqttws31.js" ></script>
		<!-- load topics -->
		<script src = "settings/topicsToSubscribe_smarthomeconfig.js?ver=20200424-a" ></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20200918-a" ></script>
		<!-- load service -->
		<script src = "settings/setupMqttServices.js?ver=20200505-a" ></script>
		<!-- load mqtt handler-->
		<script src = "settings/processAllMqttMsg.js?ver=20200505-a" ></script>

		<script>
			
			function visibiltycheck(elementId, mqttpayload) {
<?php for( $devicenum = 1; $devicenum <= 10; $devicenum++ ) { ?>
				if ( elementId == 'device_configuredDevices<?php echo $devicenum; ?>') {
					if ( mqttpayload == 0 ) {
						$('#device<?php echo $devicenum; ?>options').hide();
					} else {
						$('#device<?php echo $devicenum; ?>options').show();
					}
				}
				if ( elementId == 'device_nameDevices<?php echo $devicenum; ?>') {
					if ( mqttpayload != "Name" ) {
						$('#deviceHeader<?php echo $devicenum; ?>').text('Gerät <?php echo $devicenum; ?> ('+mqttpayload+')');
					} else {
						$('#deviceHeader<?php echo $devicenum; ?>').text('Gerät <?php echo $devicenum; ?>');
					}
				}
<?php } ?>
			}
			$(function() {
<?php for( $devicenum = 1; $devicenum <= 10; $devicenum++ ) { ?>
				$('#device_configuredDevices<?php echo $devicenum; ?>').change(function(){
					if ($('#device<?php echo $devicenum; ?>options').is(":hidden")) {
						$('#device<?php echo $devicenum; ?>options').show();
					} else {
						$('#device<?php echo $devicenum; ?>options').hide();
					}
				});
				$('#device_nameDevices<?php echo $devicenum; ?>').change(function(){
					if (($(this).val() != "Name") && ($(this).val().length > 0)) {
						$('#deviceHeader<?php echo $devicenum; ?>').text('Gerät <?php echo $devicenum; ?> ('+$(this).val()+')');
					} else {
						$('#deviceHeader<?php echo $devicenum; ?>').text('Gerät <?php echo $devicenum; ?>');
					}
				})
<?php } ?>
			});

			$.get(
				{ url: 'settings/navbar.html', cache: false },
				function(data){
					$('#nav').replaceWith(data);
					// disable navbar entry for current page
					$('#navSmartHomeBeta').addClass('disabled');
				}
			);

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

				$('input').on("paste",function(e) {
					// prevent paste to input fields to avoid garbage
					e.preventDefault();
				});

				$('.rangeInput').on('input', function() {
					// show slider value in label of class valueLabel
					updateLabel($(this).attr('id'));
				});

				$('input.naturalNumber').on('input', function() {
					// on the fly input validation
					formatToNaturalNumber(this);
				});
			});  // end document ready function

		</script>

	</body>
</html>
