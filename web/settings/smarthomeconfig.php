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
			/**
			 * hideSection
			 * add class 'hide' to element with selector 'section' in JQuery syntax
			 * disables all contained input and select elements if 'disableChildren' is not set to false
			**/
			function hideSection(section, disableChildren=true) {
				$(section).addClass('hide');
				updateFormFields();
			}

			/**
			 * showSection
			 * remove class 'hide' from element with selector 'section' in JQuery syntax
			 * enables all contained input and select elements if 'enableChildren' is not set to false
			**/
			function showSection(section, enableChildren=true) {
				$(section).removeClass('hide');
				updateFormFields();
			}

			/**
			 * updateFormFields
			 * checks every input and select element for a parent with class 'hide'
			 * if there is a match, disable this element
			**/
			function updateFormFields() {
				$('input').each(function() {
					if( $(this).closest('.hide').length == 0 ) {
						$(this).prop("disabled", false);
					} else {
						$(this).prop("disabled", true);
					}
				});
				$('select').each(function() {
					if( $(this).closest('.hide').length == 0 ) {
						$(this).prop("disabled", false);
					} else {
						$(this).prop("disabled", true);
					}
				});
			}

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
					<div class="card-body hide" id="device<?php echo $devicenum; ?>options">
						<div class="form-group">
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
									<select class="form-control" name="device_type" id="device_typeDevices<?php echo $devicenum; ?>" data-default="shelly" value="shelly" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<option value="shelly" data-option="shelly">Shelly</option>
										<option value="tasmota" data-option="tasmota">Tasmota</option>
										<option value="acthor" data-option="acthor">Acthor</option>
										<option value="elwa" data-option="elwa">Elwa</option>
										<option value="idm" data-option="idm">Idm</option>
										<option value="stiebel" data-option="stiebel">Stiebel</option>
										<option value="http" data-option="http">Http (in Entwicklung)</option>
										<option value="pyt" data-option="pyt">Pyt (veraltet, bitte andere Option wählen)</option>
									</select>
									<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-acthor hide">
										Heizstab Acthor der Firma my-PV<br>
										Im Web Frontend vom Heizstab muss unter "Steuerungs-Einstellungen" der Parameter "Ansteuerungs-Typ = Modbus TCP" und "Zeitablauf Ansteuerung = 120 Sek" gesetzt werden.
										Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen (in 1000 Watt Schritten)
										Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
										Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von Acthor nicht zu stören.
									</span>
									<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-elwa hide">
										Heizstab ELWA-E  der Firma my-PV<br>
										Im Web Frontend vom Heizstab muss unter Steuerungs-Einstellungen der Parameter "Ansteuerungs-Typ = Modbus TCP" und "Power Timeout = 120 Sek" gesetzt werden.
										Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen.
										Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
										Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von Elwa nicht zu stören.
										Die Warmwassersicherstellung in Elwa kann genutzt werden. OpenWB erkennt dieses am Status und überträgt dann keinen Überschuss.
									</span>
									<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-idm hide">
										Wärmepumpe der Firma IDM mit Navigatorregelung 2.0<br>
										Im Web Frontend muss unter "Heizungsbauerebene / Konfiguration / PV-Signal": Auswahl "Gebäudeleittechnik / Smartfox" und unter "Heizungsbauerebene / Gebäudeleittechnik" der Parameter "Modbus TCP = Ein" und unter "Einstellungen / Photovoltaik" der Parameter "PV Überschuss = 0" gesetzt werden
										Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen
										Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
										Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von IDM nicht zu stören.
									</span>
									<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-stiebel hide">
										Wärmepumpe der Firma Stiebel mit ISG Web (Servicewelt über Modbus) und SG Ready Eingang.<br>
										Im ISG web muss unter "Einstellungen / Energiemanagement" der Parameter "SGREADY = Ein" gesetzt werden.
										Wenn die Einschaltbedingung erreicht ist wird der Sg Ready Eingang von Betriebszustand 2 auf Betriebszustand 3 geschaltet.
										Wenn die Ausbedingung erreicht ist wird der Sg Ready Eingang von Betriebszustand 3 auf Betriebszustand 2 geschaltet.
									</span>
									<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-http hide">
										Mit diesem Typ werden alle Geräte unterstützt, welche sich durch einfache Http-Aufrufe schalten lassen.<br>
										<span class="text-danger">Das Modul befindet sich noch in der Entwicklung und kann nicht genutzt werden!</span>
									</span>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-row mb-1 device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly device<?php echo $devicenum; ?>-option-tasmota device<?php echo $devicenum; ?>-option-acthor device<?php echo $devicenum; ?>-option-elwa device<?php echo $devicenum; ?>-option-idm device<?php echo $devicenum; ?>-option-stiebel device<?php echo $devicenum; ?>-option-pyt hide">
							<label for="device_ipDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">IP Adresse</label>
							<div class="col">
								<input id="device_ipDevices<?php echo $devicenum; ?>" name="device_ip" class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" data-default="192.168.1.1" value="192.168.1.1" inputmode="text"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
							</div>
						</div>
						<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-http hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="device_einschalturlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Einschalt-URL</label>
									<div class="col">
										<input id="device_einschalturlDevices<?php echo $devicenum; ?>" name="device_einschalturl" class="form-control" type="text" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Die hier angegebene URL wird aufgerufen, um das Gerät einzuschalten.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="device_ausschalturlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Ausschalt-URL</label>
									<div class="col">
										<input id="device_ausschalturlDevices<?php echo $devicenum; ?>" name="device_ausschalturl" class="form-control" type="text" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Die hier angegebene URL wird aufgerufen, um das Gerät auszuschalten.</span>
									</div>
								</div>
								<div class="form-row mb-1 device<?php echo $devicenum; ?>noDifferentMeasurement hide">
									<label for="device_leistungurlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Leistungs-URL</label>
									<div class="col">
										<input id="device_leistungurlDevices<?php echo $devicenum; ?>" name="device_leistungurl" class="form-control" type="text" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Die hier angegebene URL wird aufgerufen, um die aktuelle Leistung des Geräts zu erhalten.</span>
									</div>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Gerät kann schalten</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" id="device_canSwitchDevices<?php echo $devicenum; ?>" name="device_canSwitch" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<label class="btn btn-outline-info">
											<input type="radio" name="device_canSwitchDevices<?php echo $devicenum; ?>" id="device_canSwitch<?php echo $devicenum; ?>0" data-option="0">Nein
										</label>
										<label class="btn btn-outline-info">
											<input type="radio" name="device_canSwitchDevices<?php echo $devicenum; ?>" id="device_canSwitch<?php echo $devicenum; ?>1" data-option="1">Ja
										</label>
									</div>
									<span class="form-text small">Ist diese Option aktiviert, dann wird das Gerät anhand des Überschusses automatisch oder manuell geschaltet.</span>
								</div>
							</div>
						</div>
						<div class="device<?php echo $devicenum; ?>canSwitch">
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
										<span class="form-text small">Diese Option sorgt dafür, dass das Gerät gezielt abgeschaltet wird, wenn ein Auto geladen wird. Dem Auto steht somit entweder mehr PV-Überschuss zur Verfügung oder der Bezug verringert sich.</span>
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
							<div class="device-option-housebattery hide">
								<hr class="border-secondary">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="device_speichersocbeforestartDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Speicherbeachtung beim Einschalten</label>
										<div class="col-md-8">
											<div class="form-row vaRow mb-1">
												<label for="device_speichersocbeforestartDevices<?php echo $devicenum; ?>" class="col-2 col-form-label valueLabel" suffix="%">0 %</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" id="device_speichersocbeforestartDevices<?php echo $devicenum; ?>" name="device_speichersocbeforestart" min="0" max="100" step="5" data-default="0" value="0" data-default="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
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
												<label for="device_speichersocbeforestopDevices<?php echo $devicenum; ?>" class="col-2 col-form-label valueLabel" suffix="%">100 %</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" id="device_speichersocbeforestopDevices<?php echo $devicenum; ?>" name="device_speichersocbeforestop" min="0" max="100" step="5" data-default="100" value="100" data-default="100" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												</div>
											</div>
											<span class="form-text small">Parameter in % Ladezustand. Überhalb dieses Wertes wird das Gerät nicht abgeschaltet. 100% deaktiviert die Funktion.</span>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="form-group device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly hide">
							<hr class="border-secondary">
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
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Separate Leistungsmessung für das Gerät</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" id="device_differentMeasurementDevices<?php echo $devicenum; ?>" name="device_differentMeasurement" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<label class="btn btn-outline-info">
											<input type="radio" name="device_differentMeasurementDevices<?php echo $devicenum; ?>" id="device_differentMeasurement<?php echo $devicenum; ?>0" data-option="0">Nein
										</label>
										<label class="btn btn-outline-info">
											<input type="radio" name="device_differentMeasurementDevices<?php echo $devicenum; ?>" id="device_differentMeasurement<?php echo $devicenum; ?>1" data-option="1">Ja
										</label>
									</div>
									<span class="form-text small">Wenn diese Option aktiviert wird, wird für die Leistungserfassung einseparates Gerät abgefragt. Das kann genutzt werden, wenn z. B. ein Gerät über keine Leistungsmessung verfügt, jedoch ein Zwischenstecker mit Messung eingesetzt wird.</span>
								</div>
							</div>
						</div>
						<div class="device<?php echo $devicenum; ?>differentMeasurement hide">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Gerätetyp</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" id="device_measureTypeDevices<?php echo $devicenum; ?>" name="device_measureType" data-toggle="buttons" data-default="sdm630" value="sdm630" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<label class="btn btn-outline-info">
											<input type="radio" name="device_measureTypeDevices<?php echo $devicenum; ?>" id="device_measureTypeDevices<?php echo $devicenum; ?>Shelly" data-option="shelly">Shelly
										</label>
										<label class="btn btn-outline-info btn-toggle">
											<input type="radio" name="device_measureTypeDevices<?php echo $devicenum; ?>" id="device_measureTypeDevices<?php echo $devicenum; ?>SDM630" data-option="sdm630"> SDM630
										</label>
										<label class="btn btn-outline-info">
											<input type="radio" name="device_measureTypeDevices<?php echo $devicenum; ?>" id="device_measureTypeDevices<?php echo $devicenum; ?>http" data-option="http">Http
										</label>
									</div>
								</div>
							</div>
							<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-shelly deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm630 hide">
								<label for="device_measureipDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input id="device_measureipDevices<?php echo $devicenum; ?>" name="device_measureip" class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" data-default="192.168.1.1" value="192.168.1.1" inputmode="text"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
								</div>
							</div>
							<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm630 hide">
								<label for="device_measureidDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">ID des Zählers am Netzwerk/Modbus Wandler</label>
								<div class="col">
									<input id="device_measureidDevices<?php echo $devicenum; ?>" name="device_measureid" class="form-control naturalNumber" type="number" inputmode="decimal" required min="1" max="255" data-default="1" value="1"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
								</div>
							</div>
							<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-http hide">
								<label for="device_measureurlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Leistungs-URL</label>
								<div class="col">
									<input id="device_measureurlDevices<?php echo $devicenum; ?>" name="device_measureurld" class="form-control" data-default="" value=""  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
								</div>
							</div>
						</div>
					</div>  <!-- end card body Allgemeine Einstellungen Gerät <?php echo $devicenum; ?> -->
				</div>  <!-- end card Allgemeine Einstellungen Gerät <?php echo $devicenum; ?> -->
<?php } ?>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Übergreifende Einstellungen
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="logLevel" class="col-md-4 col-form-label">SmartHome Loglevel</label>
								<div class="col">
									<select name="logLevel" id="logLevel" class="form-control" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/">
										<option value="0" data-option="0">0</option>
										<option value="1" data-option="1">1</option>
										<option value="2" data-option="2">2</option>
									</select>
								</div>
							</div>
						</div>
					</div>
				</div>

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
		<script src = "settings/topicsToSubscribe_smarthomeconfig.js?ver=20201207" ></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20201207" ></script>
		<!-- load service -->
		<script src = "settings/setupMqttServices.js?ver=20201207" ></script>
		<!-- load mqtt handler-->
		<script src = "settings/processAllMqttMsg.js?ver=20201207" ></script>

		<script>
			<?php for( $devicenum = 1; $devicenum <= 10; $devicenum++ ) { ?>
				function visibility_device_configuredDevices<?php echo $devicenum; ?>( data ){
					// console.log("device_configuredDevices: data: "+data);
					if( typeof data == 'undefined' ){
						data = $('input[name=device_configuredDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					// console.log("device_configuredDevices: data: "+data);
					if( data == 0 ){
						hideSection('#device<?php echo $devicenum; ?>options');
					} else {
						showSection('#device<?php echo $devicenum; ?>options');
					}
				}

				function visibility_device_typeDevices<?php echo $devicenum; ?>( data ){
					// console.log("device_typeDevices: data: "+data);
					if( typeof data == 'undefined' ){
						data = $('#device_typeDevices<?php echo $devicenum; ?>').val();
					}
					// console.log("device_typeDevices: data: "+data);
					hideSection(".device<?php echo $devicenum; ?>-option");
					showSection(".device<?php echo $devicenum; ?>-option-"+data);
				}

				function visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>( data ){
					// console.log("device_differentMeasurementDevices: data: "+data);
					if( typeof data == 'undefined' ){
						data = $('input[name=device_differentMeasurementDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					// console.log("device_differentMeasurementDevices: data: "+data);
					if( data == 0 ){
						hideSection('.device<?php echo $devicenum; ?>differentMeasurement');
						showSection('.device<?php echo $devicenum; ?>noDifferentMeasurement');
					} else {
						showSection('.device<?php echo $devicenum; ?>differentMeasurement');
						hideSection('.device<?php echo $devicenum; ?>noDifferentMeasurement');
					}
				}

				function visibility_device_measureTypeDevices<?php echo $devicenum; ?>( data ){
					// console.log("device_measureTypeDevices: data: "+data);
					if( typeof data == 'undefined' ){
						data = $('input[name=device_measureTypeDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					// console.log("device_measureTypeDevices: data: "+data);
					hideSection(".deviceMeasureTypeDevices<?php echo $devicenum; ?>-option");
					showSection(".deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-"+data);
				}

				function visibility_device_canSwitchDevices<?php echo $devicenum; ?>( data ){
					console.log("device_canSwitchDevices: data: "+data);
					if( typeof data == 'undefined' ){
						data = $('input[name=device_canSwitchDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					console.log("device_canSwitchDevices: data: "+data);
					if( data == 0 ){
						hideSection('.device<?php echo $devicenum; ?>canSwitch');
					} else {
						showSection('.device<?php echo $devicenum; ?>canSwitch');
					}
				}

				function visibility_device_nameDevices<?php echo $devicenum; ?>( data ){
					if ( data != "Name" ) {
						$('#deviceHeader<?php echo $devicenum; ?>').text('Gerät <?php echo $devicenum; ?> ('+data+')');
					} else {
						$('#deviceHeader<?php echo $devicenum; ?>').text('Gerät <?php echo $devicenum; ?>');
					}
				}
			<?php } ?>

			function visibility_housebatteryConfigured( data ) {
				if ( data == 1 ) {
					showSection('.device-option-housebattery');
				} else {
					hideSection('.device-option-housebattery');
				}
			}

			function visibiltycheck(elementId, mqttpayload) {
				<?php for( $devicenum = 1; $devicenum <= 10; $devicenum++ ) { ?>
					if ( elementId == 'boolHouseBatteryConfigured' ) {
						visibility_housebatteryConfigured( mqttpayload );
					}

					if ( elementId == 'device_configuredDevices<?php echo $devicenum; ?>') {
						visibility_device_configuredDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_typeDevices<?php echo $devicenum; ?>') {
						visibility_device_typeDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_differentMeasurementDevices<?php echo $devicenum; ?>') {
						visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_measureTypeDevices<?php echo $devicenum; ?>') {
						visibility_device_measureTypeDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_canSwitchDevices<?php echo $devicenum; ?>') {
						visibility_device_canSwitchDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_nameDevices<?php echo $devicenum; ?>') {
						visibility_device_nameDevices<?php echo $devicenum; ?>( mqttpayload );
					}
				<?php } ?>
			}

			$(function() {
				<?php for( $devicenum = 1; $devicenum <= 10; $devicenum++ ) { ?>
					$('#device_configuredDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_configuredDevices<?php echo $devicenum; ?>();
					});

					$('#device_typeDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_typeDevices<?php echo $devicenum; ?>();
					});

					$('#device_differentMeasurementDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>();
					});

					$('#device_measureTypeDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_measureTypeDevices<?php echo $devicenum; ?>();
					});

					$('#device_canSwitchDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_canSwitchDevices<?php echo $devicenum; ?>();
					});

					$('#device_nameDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_nameDevices<?php echo $devicenum; ?>( $(this).val() );
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
