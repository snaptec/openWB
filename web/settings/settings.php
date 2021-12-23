<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Einstellungen</title>
		<meta name="description" content="Control your charge" />
		<meta name="author" content="Michael Ortenstein" />
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
		<!-- Bootstrap Selectpicker-->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-selectpicker/bootstrap-select.min.css">

		<link rel="stylesheet" type="text/css" href="fonts/font-awesome-5.8.2/css/all.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<script src="js/bootstrap-selectpicker/bootstrap-select.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
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

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Allgemeine Einstellungen</h1>
			<form action="./settings/saveconfig.php" method="POST">

				<!-- Übergreifendes -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">openWB ist nur ein Ladepunkt</div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($isssold == 0) echo " active" ?>">
											<input type="radio" name="isss" id="isssOff" value="0"<?php if($isssold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($isssold == 1) echo " active" ?>">
											<input type="radio" name="isss" id="isssOn" value="1"<?php if($isssold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Wird hier Ja gewählt ist diese openWB nur ein Ladepunkt und übernimmt keine eigene Regelung.
							Hier ist Ja zu wählen wenn, bereits eine openWB vorhanden ist und diese nur ein weiterer Ladepunkt der vorhandenen openWB sein soll.
							<span class="text-danger">Alle in dieser openWB getätigten Einstellungen werden NICHT beachtet.</span>
							An der Haupt openWB wird als Ladepunkt "externe openWB" gewählt und die IP Adresse eingetragen.
						</div>
						<div id="isssdiv" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="ssdisplay" class="col-md-4 col-form-label">Display-Theme</label>
									<div class="col">
										<select name="ssdisplay" id="ssdisplay" class="form-control">
											<option <?php if($ssdisplayold == 0) echo "selected" ?> value="0">Normal</option>
											<option <?php if($ssdisplayold == 1) echo "selected" ?> value="1">Display der übergeordneten openWB</option>
										</select>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_isss() {
								if($('#isssOff').prop("checked")) {
									hideSection('#isssdiv');
								} else {
									showSection('#isssdiv');
								}
							}

							$('input[type=radio][name=isss]').change(function(){
								visibility_isss();
							});

							visibility_isss();
						});
					</script>
				</div>

				<!-- electricity tariff providers -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Stromanbieter</div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($etprovideraktivold == 0) echo " active" ?>">
											<input type="radio" name="etprovideraktiv" id="etprovideraktivOff" value="0"<?php if($etprovideraktivold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($etprovideraktivold == 1) echo " active" ?>">
											<input type="radio" name="etprovideraktiv" id="etprovideraktivOn" value="1"<?php if($etprovideraktivold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Ermöglicht Laden nach Strompreis. Hierfür wird ein unterstützter Anbieter benötigt. Die Funktion ist nur im Modus Sofortladen aktiv!
						</div>
						<div class="form-group mb-0" id="etproviderondiv">
							<div class="form-row mb-1">
								<label for="etprovider" class="col-md-4 col-form-label">Anbieter</label>
								<div class="col">
									<select name="etprovider" id="etprovider" class="form-control">
										<option <?php if($etproviderold == "et_awattar") echo "selected" ?> value="et_awattar">aWATTar Hourly</option>
										<option <?php if($etproviderold == "et_awattarcap") echo "selected" ?> value="et_awattarcap">aWATTar Hourly-CAP</option>
										<option <?php if($etproviderold == "et_tibber") echo "selected" ?> value="et_tibber">Tibber</option>
									</select>
								</div>
							</div>
							<div id="awattardiv" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="awattarlocation" class="col-md-4 col-form-label">Land</label>
										<div class="col">
											<select name="awattarlocation" id="awattarlocation" class="form-control">
												<option <?php if($awattarlocationold == "de") echo "selected" ?> value="de">Deutschland</option>
												<option <?php if($awattarlocationold == "at") echo "selected" ?> value="at">Österreich</option>
											</select>
										</div>
									</div>
								</div>
							</div>
							<div id="tibberdiv" class="hide">
								<script src = "../modules/et_tibber/tibber.js?ver=20210128" ></script>
								<div class="card-text alert alert-primary">
									<p>
										Ihren persönlichen Tibber-Token erhalten Sie über die <a href="https://developer.tibber.com/explorer" target="_blank">Tibber-Developer-Seite</a>.
									</p>
									<p>
										Behandeln Sie Ihren Token wie ein Passwort, da sich darüber auch persönliche Daten aus Ihrem Tibber-Account abfragen lassen! Die Home-ID können Sie (wenn bekannt)
										in das Eingabefeld selbst eintragen oder <b>nach Eingabe Ihres Token</b> durch Klick auf den Button von der openWB ermitteln lassen. Unerlaubte Zeichen werden aus dem Token und der Home-ID automatisch gelöscht.
									</p>
									<p>
										Bei einer fehlerhaften Tibber-Abfrage wird der Strompreis von der openWB bis zur nächsten erfolgreichen Abfrage mit 99.99ct/kWh festgelegt.
									</p>
									Bitte verifizieren Sie die Eingabe, bevor Sie die Einstellungen speichern.
								</div>
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="tibbertoken" class="col-md-4 col-form-label">Tibber-Token</label>
										<div class="col">
											<input class="form-control" type="text" name="tibbertoken" id="tibbertoken" value="<?php echo $tibbertokenold; ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="tibberhomeid" class="col-md-4 col-form-label">Home-ID</label>
										<div class="col">
											<input class="form-control" type="text" name="tibberhomeid" id="tibberhomeid" value="<?php echo $tibberhomeidold; ?>">
										</div>
									</div>
								</div>
								<div class="row justify-content-center">
									<button id="getTibberHomeIdBtn" type="button" class="btn btn-primary m-2">Home-ID ermitteln</button>
									<button id="verifyTibberBtn" type="button" class="btn btn-secondary m-2">Tibber-Daten verifizieren</button>
								</div>
								<script>
									$(document).ready(function(){

										$('#tibberHomesDropdown').selectpicker();

										$('#tibbertoken').change(function(){
											// after change of token check if no invalid chars were entered
											var currentVal = $(this).val();
											// !Attention! Until now there are only characters 0-9 a-Z A-Z _ and - in token.
											// Function may be needed to be adjusted in future
											newVal = currentVal.trim().replace(/[^\w-]/gi,'');
											$(this).val(newVal);
										});

										$('#tibberhomeid').change(function(){
											// after change of token check if no invalid chars were entered
											var currentVal = $(this).val();
											// !Attention! Until now there are only characters 0-9 a-Z A-Z _ and - in in homeID.
											// Function may be needed to be adjusted in future
											newVal = currentVal.trim().replace(/[^\w-]/gi,'');
											$(this).val(newVal);
										});

										$('#tibberhomeIdModalOkBtn').click(function(){
											$('#tibberhomeid').val($('#tibberHomesDropdown option:selected').val());
										});

										$('#getTibberHomeIdBtn').click(function(){
											const tibberQuery = '{ "query": "{viewer {homes{id address{address1 address2 address3 postalCode city}}}}" }';
											readTibberAPI($('#tibbertoken').val(), tibberQuery)
												.then((queryData) => {
													var homes = queryData.data.viewer.homes;
													// clear selectpicker
													$('#tibberHomesDropdown').empty();
													// and fill with received address(es)
													$(homes).each(function() {
														var homeID = this.id;
														var addressStr = this.address.address1;
														if ( this.address.address2 !== null ) {
															addressStr = addressStr + ', ' + this.address.address2;
														}
														if ( this.address.address3 !== null ) {
															addressStr = addressStr + ', ' + this.address.address3;
														}
														addressStr = addressStr + ', ' + this.address.postalCode + ' ' + this.address.city;
														$('#tibberHomesDropdown').append('<option value="' + homeID + '">' + addressStr + '</option>');
    												});
													$('#tibberhomeIdModal').find('.modal-header').removeClass('bg-danger');
													$('#tibberhomeIdModal').find('.modal-header').addClass('bg-success');
													$('#tibberhomeIdModalOkBtn').show();
													$('#tibberModalHomeIdErrorDiv').hide();
													$('#tibberModalSelectHomeIdDiv').show();
													// order of the following selectpicker commands is crucial for correct functionality!!
													// make sure formerly hidden element is now enabled,
													$('#tibberHomesDropdown').attr('disabled',false);
													$('#tibberHomesDropdown').selectpicker('refresh');
													// set the selectpicker to the first option
													$('#tibberHomesDropdown').selectpicker('val', $('#tibberHomesDropdown option:first').val());
													// show modal with unhidden div
													$('#tibberhomeIdModal').modal("show");
												})
												.catch((error) => {
													$('#tibberhomeIdModal').find('.modal-header').removeClass('bg-success');
													$('#tibberhomeIdModal').find('.modal-header').addClass('bg-danger');
													$('#tibberhomeIdModalOkBtn').hide();
													$('#tibberModalHomeIdErrorDiv').find('span').text(error);
													//$('#tibberErrorText').text(error);
													$('#tibberModalHomeIdErrorDiv').show();
													$('#tibberModalSelectHomeIdDiv').hide();
													$('#tibberhomeid').val('');
													$('#tibberhomeIdModal').modal("show");
								  				})
										});

										$('#verifyTibberBtn').click(function(){
											const tibberQuery = '{ "query": "{viewer {name home(id:\\"' + $('#tibberhomeid').val() + '\\") {address {address1}}}}" }';
											readTibberAPI($('#tibbertoken').val(), tibberQuery)
												.then((queryData) => {
													$('#tibberVerifyModal').find('.modal-header').removeClass('bg-danger');
													$('#tibberVerifyModal').find('.modal-header').addClass('bg-success');
													$('#tibberVerifyOkBtn').show();
													$('#tibberVerifyModal').find('.btn-danger').hide();
													$('#tibberModalVerifyErrorDiv').hide();
													$('#tibberModalVerifySuccessDiv').show();
													var name = queryData.data.viewer.name;
													$('#tibberModalVerifySuccessDiv').find('span').text(name);
													$('#tibberVerifyModal').modal("show");
												})
												.catch((error) => {
													$('#tibberVerifyModal').find('.modal-header').removeClass('bg-success');
													$('#tibberVerifyModal').find('.modal-header').addClass('bg-danger');
													$('#tibberVerifyOkBtn').hide();
													$('#tibberVerifyModal').find('.btn-danger').show();
													$('#tibberModalVerifyErrorDiv').find('span').text(error);
													$('#tibberModalVerifyErrorDiv').show();
													$('#tibberModalVerifySuccessDiv').hide();
													$('#tibberhomeid').val('');
													$('#tibberVerifyModal').modal("show");
												})
										});

									});  // end document ready
								</script>

								<!-- modal Tibber-homeID-window -->
								<div class="modal fade" id="tibberhomeIdModal">
									<div class="modal-dialog">
										<div class="modal-content">

											<!-- modal header -->
											<div class="modal-header">
												<h4 class="modal-title">Tibber Home-ID ermitteln</h4>
											</div>

											<!-- modal body -->
											<div class="modal-body">
												<div id="tibberModalHomeIdErrorDiv" class="row justify-content-center hide">
													<div class="col">
														<p>
															<span></span>
														</p>
														Home-ID-Ermittlung fehlgeschlagen.
													</div>
												</div>

												<div id="tibberModalSelectHomeIdDiv" class="row justify-content-center hide">
													<div class="col">
														<div class="form-group">
														<label for="tibberHomesDropdown">Bitte wählen Sie eine Adresse:</label>
														<select class="form-control selectpicker" id="tibberHomesDropdown">
														</select>
													  </div>
													</div>
												</div>

											</div>

											<!-- modal footer -->
											<div class="modal-footer d-flex justify-content-center">
												<button type="button" class="btn btn-success" data-dismiss="modal" id="tibberhomeIdModalOkBtn">Home-ID übernehmen</button>
												<button type="button" class="btn btn-danger" data-dismiss="modal">Abbruch</button>
											</div>

										</div>
									</div>
								</div>  <!-- end modal Tibber-homeID-window -->

								<!-- modal Tibber-verify-data-window -->
								<div class="modal fade" id="tibberVerifyModal">
									<div class="modal-dialog">
										<div class="modal-content">

											<!-- modal header -->
											<div class="modal-header">
												<h4 class="modal-title">Tibber-Daten verifizieren</h4>
											</div>

											<!-- modal body -->
											<div class="modal-body">
												<div id="tibberModalVerifyErrorDiv" class="row justify-content-center hide">
													<div class="col">
														<p>
															<span></span>
														</p>
														Verifizierung der Tibber-Daten fehlgeschlagen.
													</div>
												</div>

												<div id="tibberModalVerifySuccessDiv" class="row justify-content-center hide">
													<div class="col">
														<p>
															Verifizierung der Tibber-Daten erfolgreich!
														</p>
														Registrierter Account-Inhaber: <span></span>
													</div>
												</div>
											</div>

											<!-- modal footer -->
											<div class="modal-footer d-flex justify-content-center">
												<button type="button" class="btn btn-success" data-dismiss="modal" id="tibberVerifyOkBtn">OK</button>
												<button type="button" class="btn btn-danger" data-dismiss="modal">Abbruch</button>
											</div>

										</div>
									</div>
								</div>  <!-- end modal Tibber-verify-data-window -->

							</div>
						</div>
					</div>

					<script>
						$(function() {
							function visibility_electricityprovider() {
								if($('#etprovideraktivOff').prop("checked")) {
									hideSection('#etproviderondiv');
								} else {
									showSection('#etproviderondiv');
								}
							}

							function visibility_electricitytariff() {
								hideSection('#awattardiv');
								hideSection('#tibberdiv');
								switch ($('#etprovider').val()) {
									case 'et_awattar':
										showSection('#awattardiv');
									break;
									case 'et_tibber':
										showSection('#tibberdiv');
									break;
								}
							}

							$('#etprovider').change(function(){
								visibility_electricitytariff();
							});

							$('input[type=radio][name=etprovideraktiv]').change(function(){
								visibility_electricityprovider();
							});

							visibility_electricitytariff();
							visibility_electricityprovider();
						});
					</script>
				</div>

				<!-- Sperren nach Abstecken -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Ladepunkte sperren nach Abstecken
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Nachdem der Stecker gezogen wird, wird der entsprechende Ladepunkt gesperrt. Ein manuelles aktivieren des Ladepunktes ist erforderlich. Nach aktivieren bleibt der Ladepunkt solange aktiv bis ein Stecker eingesteckt und wieder abgezogen wird. Ist unabhängig davon ob geladen wird.
						</div>
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<div class="col-md-4">
									Ladepunkt 1
								</div>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($stopchargeafterdisclp1old == 0) echo " active" ?>">
										<input type="radio" name="stopchargeafterdisclp1" id="stopchargeafterdisclp1Off" value="0"<?php if($stopchargeafterdisclp1old == 0) echo " checked=\"checked\"" ?>>Nein
									</label>
									<label class="btn btn-outline-info<?php if($stopchargeafterdisclp1old == 1) echo " active" ?>">
										<input type="radio" name="stopchargeafterdisclp1" id="stopchargeafterdisclp1On" value="1"<?php if($stopchargeafterdisclp1old == 1) echo " checked=\"checked\"" ?>>Ja
									</label>
								</div>
							</div>
							<div id="lp2aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 2
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp2old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp2" id="stopchargeafterdisclp2Off" value="0"<?php if($stopchargeafterdisclp2old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp2old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp2" id="stopchargeafterdisclp2On" value="1"<?php if($stopchargeafterdisclp2old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp3aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 3
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp3old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp3" id="stopchargeafterdisclp3Off" value="0"<?php if($stopchargeafterdisclp3old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp3old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp3" id="stopchargeafterdisclp3On" value="1"<?php if($stopchargeafterdisclp3old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp4aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 4
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp4old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp4" id="stopchargeafterdisclp4Off" value="0"<?php if($stopchargeafterdisclp4old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp4old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp4" id="stopchargeafterdisclp4On" value="1"<?php if($stopchargeafterdisclp4old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp5aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 5
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp5old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp5" id="stopchargeafterdisclp5Off" value="0"<?php if($stopchargeafterdisclp5old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp5old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp5" id="stopchargeafterdisclp5On" value="1"<?php if($stopchargeafterdisclp5old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp6aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 6
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp6old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp6" id="stopchargeafterdisclp6Off" value="0"<?php if($stopchargeafterdisclp6old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp6old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp6" id="stopchargeafterdisclp6On" value="1"<?php if($stopchargeafterdisclp6old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp7aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 7
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp7old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp7" id="stopchargeafterdisclp7Off" value="0"<?php if($stopchargeafterdisclp7old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp7old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp7" id="stopchargeafterdisclp7On" value="1"<?php if($stopchargeafterdisclp7old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp8aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 8
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp8old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp8" id="stopchargeafterdisclp8Off" value="0"<?php if($stopchargeafterdisclp8old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp8old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp8" id="stopchargeafterdisclp8On" value="1"<?php if($stopchargeafterdisclp8old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							var lp2akt = <?php echo $lastmanagementold ?>;
							var lp3akt = <?php echo $lastmanagements2old ?>;
							var lp4akt = <?php echo $lastmanagementlp4old ?>;
							var lp5akt = <?php echo $lastmanagementlp5old ?>;
							var lp6akt = <?php echo $lastmanagementlp6old ?>;
							var lp7akt = <?php echo $lastmanagementlp7old ?>;
							var lp8akt = <?php echo $lastmanagementlp8old ?>;

							if(lp2akt == '0') {
								hideSection('#lp2aktdiv');
								hideSection('#loadsharingdiv');
								showSection('#loadsharingoffdiv');
								hideSection('#nachtladenlp2div');
								hideSection('#durchslp2div');
							} else {
								showSection('#lp2aktdiv');
								showSection('#loadsharingdiv');
								hideSection('#loadsharingoffdiv');
								showSection('#nachtladenlp2div');
								showSection('#durchslp2div');
							}
							if(lp3akt == '0') {
								hideSection('#lp3aktdiv');
								hideSection('#durchslp3div');
							} else {
								showSection('#lp3aktdiv');
								showSection('#durchslp3div');
							}
							if(lp4akt == '0') {
								hideSection('#lp4aktdiv');
							} else {
								showSection('#lp4aktdiv');
							}
							if(lp5akt == '0') {
								hideSection('#lp5aktdiv');
							} else {
								showSection('#lp5aktdiv');
							}
							if(lp6akt == '0') {
								hideSection('#lp6aktdiv');
							} else {
								showSection('#lp6aktdiv');
							}
							if(lp7akt == '0') {
								hideSection('#lp7aktdiv');
							} else {
								showSection('#lp7aktdiv');
							}
							if(lp8akt == '0') {
								hideSection('#lp8aktdiv');
							} else {
								showSection('#lp8aktdiv');
							}
						});
					</script>
				</div>

				<!-- Zielladen -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Zielladen (Beta)
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Ladepunkt 1</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 0) echo " active" ?>">
										<input type="radio" name="zielladenaktivlp1" id="zielladenaktivlp1Off" value="0"<?php if($zielladenaktivlp1old == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 1) echo " active" ?>">
										<input type="radio" name="zielladenaktivlp1" id="zielladenaktivlp1On" value="1"<?php if($zielladenaktivlp1old == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div id="zielladenaktivlp1div" class="hide">
								<div class="card-text alert alert-info">
									Gewünschten SoC, Ziel Uhrzeit sowie Ladegeschwindigkeit einstellen. Sicherstellen das die Akkugröße wie auch die richtige Anzahl der Phasen konfiguriert sind.
								</div>
								<div class="form-row mb-1">
									<label for="zielladensoclp1" class="col-md-4 col-form-label">Ziel-SoC</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="zielladensoclp1" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $zielladensoclp1old; ?> %</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="zielladensoclp1" id="zielladensoclp1" min="0" max="100" step="5" value="<?php echo $zielladensoclp1old; ?>">
											</div>
										</div>
										<span class="form-text small">Der SoC Wert auf den geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="zielladenuhrzeitlp1" class="col-md-4 col-form-label">Ziel-Zeitpunkt</label>
									<div class="col">
										<input class="form-control" type="text" pattern="20[0-9]{2}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9])|(?:(?!02)(?:0[1-9]|1[0-2])-(?:30))|(?:(?:0[13578]|1[02])-31)) (0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])" name="zielladenuhrzeitlp1" id="zielladenuhrzeitlp1" value="<?php echo $zielladenuhrzeitlp1old; ?>">
										<span class="form-text small">Gültige Werte YYYY-MM-DD HH:MM, z.B. 2018-12-16 06:15. Ende der gewünschten Ladezeit. Das Datum muss exakt in diesem Format mit Leerzeichen zwischen Monat und Stunde eingegeben werden.</span>
										<!--
											test datetime input (not supported by all Browsers)
											value format: YYY-MM-DDTHH:MM needs to be handled before passing to config file!
										<input class="form-control" type="datetime-local" name="zielladenuhrzeitlp1_test" id="zielladenuhrzeitlp1_test" value="<?php echo str_replace( ' ', 'T', $zielladenuhrzeitlp1old ); ?>">
										-->
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="zielladenalp1" class="col-md-4 col-form-label">Stromstärke</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="zielladenalp1" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $zielladenalp1old; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="zielladenalp1" id="zielladenalp1" min="6" max="32" step="1" value="<?php echo $zielladenalp1old; ?>">
											</div>
										</div>
										<span class="form-text small">Ampere mit denen geladen werden soll um den Ziel SoC zu erreichen.</span>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_zielladenaktivlp1() {
								if($('#zielladenaktivlp1Off').prop("checked")) {
									hideSection('#zielladenaktivlp1div');
								} else {
									showSection('#zielladenaktivlp1div');
								}
							}

							$('input[type=radio][name=zielladenaktivlp1]').change(function(){
								visibility_zielladenaktivlp1();
							});

							visibility_zielladenaktivlp1();
						});
					</script>
				</div>

				<!-- EV Daten -->
				<div class="card border-primary">
					<div class="card-header bg-primary">
						EV Daten
					</div>
					<div class="card-body">
						<div id="durchslp1div">
							<div class="form-group">
								<div class="form-row mb-1">
									<div class="col">
										Ladepunkt 1
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="durchslp1" class="col-md-4 col-form-label">Durchschnittsverbrauch in kWh/100km</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="0.1" name="durchslp1" id="durchslp1" value="<?php echo $durchslp1old ?>">
										<span class="form-text small">Gültige Werte xx.xx, z.B. 14.5. Dient zur Berechnung der geladenen Strecke.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="akkuglp1" class="col-md-4 col-form-label">Akkugröße in kWh</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" name="akkuglp1" id="akkuglp1" value="<?php echo $akkuglp1old ?>">
										<span class="form-text small">Gültige Werte xx, z.B. 41. Dient zur Berechnung der benötigten Ladezeit.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Anzahl genutzter Phasen</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 1) echo " active" ?>">
												<input type="radio" name="zielladenphasenlp1" id="zielladenphasenlp11" value="1"<?php if($zielladenphasenlp1old == 1) echo " checked=\"checked\"" ?>>1
											</label>
											<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 2) echo " active" ?>">
												<input type="radio" name="zielladenphasenlp1" id="zielladenphasenlp12" value="2"<?php if($zielladenphasenlp1old == 2) echo " checked=\"checked\"" ?>>2
											</label>
											<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 3) echo " active" ?>">
												<input type="radio" name="zielladenphasenlp1" id="zielladenphasenlp13" value="3"<?php if($zielladenphasenlp1old == 3) echo " checked=\"checked\"" ?>>3
											</label>
										</div>
										<span class="form-text small">Nur für Zielladen relevant.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="zielladenmaxalp1" class="col-md-4 col-form-label">maximale Stromstärke</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="zielladenmaxalp1" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $zielladenmaxalp1old; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="zielladenmaxalp1" id="zielladenmaxalp1" min="6" max="32" step="1" value="<?php echo $zielladenmaxalp1old; ?>">
											</div>
										</div>
										<span class="form-text small">Ampere mit denen geladen werden kann, um den Ziel SoC zu erreichen. Orientiert an der Leistung der Hausinstallation, oder der des zu ladenden Autos.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="durchslp2div" class="hide">
							<hr class="border-primary">
							<div class="form-group mb-1">
								<div class="form-row mb-1">
									<div class="col">
										Ladepunkt 2
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="durchslp2" class="col-md-4 col-form-label">Durchschnittsverbrauch in kWh/100km</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step=".1" name="durchslp2" id="durchslp2" value="<?php echo $durchslp2old ?>">
										<span class="form-text small">Gültige Werte xx.xx, z.B. 14.5. Dient zur Berechnung der geladenen Strecke.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="akkuglp2" class="col-md-4 col-form-label">Akkugröße in kWh</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" name="akkuglp2" id="akkuglp2" value="<?php echo $akkuglp2old ?>">
										<span class="form-text small">Gültige Werte xx, z.B. 41. Dient zur Berechnung der benötigten Ladezeit.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="durchslp3div" class="hide">
							<hr class="border-primary">
							<div class="form-group">
								<div class="form-row mb-1">
									<div class="col">
										Ladepunkt 3
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="durchslp3" class="col-md-4 col-form-label">Durchschnittsverbrauch in kWh/100km</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step=".1" name="durchslp3" id="durchslp3" value="<?php echo $durchslp3old ?>">
										<span class="form-text small">Gültige Werte xx.xx, z.B. 14.5. Dient zur Berechnung der geladenen Strecke.</span>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Automatische Phasenumschaltung -->
				<div class="card border-success">
					<div class="card-header bg-success">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Automatische Phasenumschaltung</div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($u1p3paktivold == 0) echo " active" ?>">
											<input type="radio" name="u1p3paktiv" id="u1p3paktivOff" value="0"<?php if($u1p3paktivold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($u1p3paktivold == 1) echo " active" ?>">
											<input type="radio" name="u1p3paktiv" id="u1p3paktivOn" value="1"<?php if($u1p3paktivold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Automatisierte Umschaltung von 1- und 3-phasiger Ladung. Nur aktivieren, wenn diese Option in der OpenWB verbaut ist. Je nach gekaufter Hardwareoption gültig für alle Ladepunkte!
						</div>
						<div id="u1p3pan" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Sofort Laden</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($u1p3psofortold == 1) echo " active" ?>">
											<input type="radio" name="u1p3psofort" id="u1p3psofort1" value="1"<?php if($u1p3psofortold == 1) echo " checked=\"checked\"" ?>>einphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3psofortold == 3) echo " active" ?>">
											<input type="radio" name="u1p3psofort" id="u1p3psofort3" value="3"<?php if($u1p3psofortold == 3) echo " checked=\"checked\"" ?>>dreiphasig
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Standby</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($u1p3pstandbyold == 1) echo " active" ?>">
											<input type="radio" name="u1p3pstandby" id="u1p3pstandby1" value="1"<?php if($u1p3pstandbyold == 1) echo " checked=\"checked\"" ?>>einphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3pstandbyold == 3) echo " active" ?>">
											<input type="radio" name="u1p3pstandby" id="u1p3pstandby3" value="3"<?php if($u1p3pstandbyold == 3) echo " checked=\"checked\"" ?>>dreiphasig
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Nachtladen</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($u1p3pnlold == 1) echo " active" ?>">
											<input type="radio" name="u1p3pnl" id="u1p3pnl1" value="1"<?php if($u1p3pnlold == 1) echo " checked=\"checked\"" ?>>einphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3pnlold == 3) echo " active" ?>">
											<input type="radio" name="u1p3pnl" id="u1p3pnl3" value="3"<?php if($u1p3pnlold == 3) echo " checked=\"checked\"" ?>>dreiphasig
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Min + PV Laden</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($u1p3pminundpvold == 1) echo " active" ?>">
											<input type="radio" name="u1p3pminundpv" id="u1p3pminundpv1" value="1"<?php if($u1p3pminundpvold == 1) echo " checked=\"checked\"" ?>>einphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3pminundpvold == 3) echo " active" ?>">
											<input type="radio" name="u1p3pminundpv" id="u1p3pminundpv3" value="3"<?php if($u1p3pminundpvold == 3) echo " checked=\"checked\"" ?>>dreiphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3pminundpvold == 4) echo " active" ?>">
											<input type="radio" name="u1p3pminundpv" id="u1p3pminundpv4" value="4"<?php if($u1p3pminundpvold == 4) echo " checked=\"checked\"" ?>>Automatikmodus
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Nur PV Laden</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($u1p3pnurpvold == 1) echo " active" ?>">
												<input type="radio" name="u1p3pnurpv" id="u1p3pnurpv1" value="1"<?php if($u1p3pnurpvold == 1) echo " checked=\"checked\"" ?>>einphasig
											</label>
											<label class="btn btn-outline-info<?php if($u1p3pnurpvold == 3) echo " active" ?>">
												<input type="radio" name="u1p3pnurpv" id="u1p3pnurpv3" value="3"<?php if($u1p3pnurpvold == 3) echo " checked=\"checked\"" ?>>dreiphasig
											</label>
											<label class="btn btn-outline-info<?php if($u1p3pnurpvold == 4) echo " active" ?>">
												<input type="radio" name="u1p3pnurpv" id="u1p3pnurpv4" value="4"<?php if($u1p3pnurpvold == 4) echo " checked=\"checked\"" ?>>Automatikmodus
											</label>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Schaltzeiten Automatikmodus</label>
									<div class="col">
										<div class="form-row vaRow mb-1">
											<label for="u1p3schaltparam" class="col-2 col-form-label valueLabel" suffix="Min"><?php echo $u1p3schaltparamold; ?> Min</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="u1p3schaltparam" id="u1p3schaltparam" min="1" max="15" step="1" value="<?php echo $u1p3schaltparamold; ?>">
											</div>
										</div>
										<span class="form-text small">Im Automatikmodus wird die PV Ladung einphasig begonnen. Um zu viele Schaltungen zu vermeiden wird Anhand dieses Wertes definiert wann die Umschaltung erfolgen soll. Ist für durchgehend x Minuten die Maximalstromstärke erreicht, wird auf dreiphasige Ladung umgestellt. Ist die Ladung nur für ein Intervall unterhalb der Maximalstromstärke, beginnt der Counter für die Umschaltung erneut. Ist die Ladung im dreiphasigen Modus für 16 - x Minuten bei der Minimalstromstärke, wird wieder auf einphasige Ladung gewechselt. Standardmäßig ist dieser Wert bei 8 min, sprich nach 8 min Maximalstromstärke wird auf 3 Phasige Ladung umgestellt und nach 16 - 8 = 8 min bei Minimalstromstärke wird wieder auf einphasige Ladung gewechselt.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="u1p3ppause" class="col-md-4 col-form-label">Pause vor und nach der Umschaltung</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="u1p3ppause" class="col-2 col-form-label valueLabel" suffix="Sek"><?php echo $u1p3ppauseold; ?> Sek</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="u1p3ppause" id="u1p3ppause" min="2" max="150" step="1" value="<?php echo $u1p3ppauseold; ?>">
											</div>
										</div>
										<span class="form-text small">
											Die Standardeinstellung ist 2 Sekunden. Falls ein Fahrzeug den Ladevorgang nach einer Umschaltung nicht zuverlässig startet, kann dieser Wert erhöht werden.
											<span class="text-danger">Achtung: experimentelle Einstellung!</span>
										</span>
									</div>
								</div>
							</div>
							<hr class="border-success">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Schieflastbeachtung</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($schieflastaktivold == 0) echo " active" ?>">
											<input type="radio" name="schieflastaktiv" id="schieflastaktivOff" value="0"<?php if($schieflastaktivold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($schieflastaktivold == 1) echo " active" ?>">
											<input type="radio" name="schieflastaktiv" id="schieflastaktivOn" value="1"<?php if($schieflastaktivold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
								<div class="form-row mb-1 hide" id="schieflastan">
									<label for="schieflastmaxa" class="col-md-4 col-form-label">Schieflastbegrenzung</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="schieflastmaxa" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $schieflastmaxaold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="schieflastmaxa" id="schieflastmaxa" min="10" max="32" step="1" value="<?php echo $schieflastmaxaold; ?>">
											</div>
										</div>
										<span class="form-text small">Gibt an mit wieviel Ampere maximal geladen wird wenn die automatische Umschaltung aktiv ist und mit einer Phase lädt.</span>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_u1p3paktiv() {
								if($('#u1p3paktivOff').prop("checked")) {
									hideSection('#u1p3pan');
								} else {
									showSection('#u1p3pan');
									visibility_schieflastaktiv();
								}
							}

							function visibility_schieflastaktiv() {
								if($('#schieflastaktivOff').prop("checked")) {
									hideSection('#schieflastan');
								} else {
									showSection('#schieflastan');
								}
							}

							$('input[type=radio][name=u1p3paktiv]').change(function(){
								visibility_u1p3paktiv();
							});

							$('input[type=radio][name=schieflastaktiv]').change(function(){
								visibility_schieflastaktiv();
							});

							visibility_u1p3paktiv();
						});
					</script>
				</div>

				<!-- Nachtlademodus -->
				<div class="card border-info">
					<div class="card-header bg-info">
						Nachtlademodus
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<div class="col">
									Aktivierung je Lademodus
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Sofort</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nlakt_sofortold == 0) echo " active" ?>">
										<input type="radio" name="nlakt_sofort" id="nlakt_sofortOff" value="0"<?php if($nlakt_sofortold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nlakt_sofortold == 1) echo " active" ?>">
										<input type="radio" name="nlakt_sofort" id="nlakt_sofortOn" value="1"<?php if($nlakt_sofortold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Min+PV</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nlakt_minpvold == 0) echo " active" ?>">
										<input type="radio" name="nlakt_minpv" id="nlakt_minpvOff" value="0"<?php if($nlakt_minpvold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nlakt_minpvold == 1) echo " active" ?>">
										<input type="radio" name="nlakt_minpv" id="nlakt_minpvOn" value="1"<?php if($nlakt_minpvold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Nur PV</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nlakt_nurpvold == 0) echo " active" ?>">
										<input type="radio" name="nlakt_nurpv" id="nlakt_nurpvOff" value="0"<?php if($nlakt_nurpvold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nlakt_nurpvold == 1) echo " active" ?>">
										<input type="radio" name="nlakt_nurpv" id="nlakt_nurpvOn" value="1"<?php if($nlakt_nurpvold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Standby</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nlakt_standbyold == 0) echo " active" ?>">
										<input type="radio" name="nlakt_standby" id="nlakt_standbyOff" value="0"<?php if($nlakt_standbyold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nlakt_standbyold == 1) echo " active" ?>">
										<input type="radio" name="nlakt_standby" id="nlakt_standbyOn" value="1"<?php if($nlakt_standbyold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
						</div>
						<hr class="border-info">
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Ladepunkt 1</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nachtladenold == 0) echo " active" ?>">
										<input type="radio" name="nachtladen" id="nachtladenOff" value="0"<?php if($nachtladenold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nachtladenold == 1) echo " active" ?>">
										<input type="radio" name="nachtladen" id="nachtladenOn" value="1"<?php if($nachtladenold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div id="nachtladenan" class="hide">
								<div class="form-row mb-1">
									<div class="col">
										Nachtladen
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nachtll" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="nachtll" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $nachtllold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="nachtll" id="nachtll" min="6" max="32" step="1" value="<?php echo $nachtllold; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div>
													<select name="nachtladenabuhr" id="nachtladenabuhr" class="form-control">
														<option <?php if($nachtladenabuhrold == 17) echo "selected" ?> value="17">17:00</option>
														<option <?php if($nachtladenabuhrold == 18) echo "selected" ?> value="18">18:00</option>
														<option <?php if($nachtladenabuhrold == 19) echo "selected" ?> value="19">19:00</option>
														<option <?php if($nachtladenabuhrold == 20) echo "selected" ?> value="20">20:00</option>
														<option <?php if($nachtladenabuhrold == 21) echo "selected" ?> value="21">21:00</option>
														<option <?php if($nachtladenabuhrold == 22) echo "selected" ?> value="22">22:00</option>
														<option <?php if($nachtladenabuhrold == 23) echo "selected" ?> value="23">23:00</option>
														<option <?php if($nachtladenabuhrold == 24) echo "selected" ?> value="24">24:00</option>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div>
													<select name="nachtladenbisuhr" id="nachtladenbisuhr" class="form-control">
														<option <?php if($nachtladenbisuhrold == 0) echo "selected" ?> value="0">0:00</option>
														<option <?php if($nachtladenbisuhrold == 1) echo "selected" ?> value="1">1:00</option>
														<option <?php if($nachtladenbisuhrold == 2) echo "selected" ?> value="2">2:00</option>
														<option <?php if($nachtladenbisuhrold == 3) echo "selected" ?> value="3">3:00</option>
														<option <?php if($nachtladenbisuhrold == 4) echo "selected" ?> value="4">4:00</option>
														<option <?php if($nachtladenbisuhrold == 5) echo "selected" ?> value="5">5:00</option>
														<option <?php if($nachtladenbisuhrold == 6) echo "selected" ?> value="6">6:00</option>
														<option <?php if($nachtladenbisuhrold == 7) echo "selected" ?> value="7">7:00</option>
														<option <?php if($nachtladenbisuhrold == 8) echo "selected" ?> value="8">8:00</option>
														<option <?php if($nachtladenbisuhrold == 9) echo "selected" ?> value="9">9:00</option>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der nachts geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nachtsoc" class="col-md-4 col-form-label">SoC Sonntag bis Donnerstag</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="nachtsoc" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $nachtsocold; ?> %</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="nachtsoc" id="nachtsoc" min="5" max="100" step="5" value="<?php echo $nachtsocold; ?>">
											</div>
										</div>
										<span class="form-text small">Wenn SoC Modul vorhanden wird Nachts bis zur Überschreitung von xx% SoC geladen in dem angegebenen Zeitfenster. Das SoC Fenster is von von Sonntag Abend bis Freitag Morgen aktiv.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nachtsoc1" class="col-md-4 col-form-label">SoC Freitag bis Sonntag</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="nachtsoc1" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $nachtsoc1old; ?> %</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="nachtsoc1" id="nachtsoc1" min="5" max="100" step="5" value="<?php echo $nachtsoc1old; ?>">
											</div>
										</div>
										<span class="form-text small">Wenn SoC Modul vorhanden wird Nachts bis zur Überschreitung von xx% SoC geladen in dem angegebenen Zeitfenster. Das SoC Fenster is von von Freitag Morgen bis Sonntag Abend aktiv.</span>
									</div>
								</div>
								<hr class="border-info">
								<div class="form-row mb-1">
									<div class="col">
										Morgensladen
									</div>
								</div>
								<?php
									function generateTimeOptions($hourStart, $minuteStart, $hourStop, $minuteStop, $minuteStep, $selectedValue) {
										$minutesOfDayStop = $hourStop * 60 + $minuteStop;
										for($minutesOfDay = $hourStart * 60 + $minuteStart; $minutesOfDay <= $minutesOfDayStop; $minutesOfDay += $minuteStep) {
											$formattedTime = sprintf('%02d:%02d', (int)($minutesOfDay / 60), $minutesOfDay  % 60);
											echo '<option value="', $formattedTime, '"', $formattedTime == $selectedValue ? ' selected' : '', '>', $formattedTime, "</option>\n";
										}
									}
									function generateMorningChargeDayOptions($dayName, $dayShortcut) {
										// mollp1 = "MOrgens Laden LadePunkt 1"
										$prefix = "mollp1$dayShortcut"
								?>
								<div class="form-row mb-1">
									<div class="col">
										<?php echo $dayName; ?>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="<?php echo $prefix; ?>ll" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="<?php echo $prefix; ?>ll" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $GLOBALS["${prefix}llold"]; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="<?php echo $prefix; ?>ll" id="<?php echo $prefix; ?>ll" min="6" max="32" step="1" value="<?php echo $GLOBALS["${prefix}llold"]; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div>
													<select name="<?php echo $prefix; ?>ab" id="<?php echo $prefix; ?>ab" class="form-control">
														<?php generateTimeOptions(3, 0, 10, 45, 15, $GLOBALS["${prefix}abold"]); ?>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div>
													<select name="<?php echo $prefix; ?>bis" id="<?php echo $prefix; ?>bis" class="form-control">
														<?php generateTimeOptions(3, 0, 11, 0, 15, $GLOBALS["${prefix}bisold"]); ?>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der am <?php echo $dayName; ?> morgens geladen werden soll.</span>
									</div>
								</div>
								<?php
									}
									generateMorningChargeDayOptions('Montag', 'mo');
									generateMorningChargeDayOptions('Dienstag', 'di');
									generateMorningChargeDayOptions('Mittwoch', 'mi');
									generateMorningChargeDayOptions('Donnerstag', 'do');
									generateMorningChargeDayOptions('Freitag', 'fr');
									generateMorningChargeDayOptions('Samstag', 'sa');
									generateMorningChargeDayOptions('Sonntag', 'so');
								?>
							</div>
						</div>

						<div id="nachtladenlp2div" class="hide">
							<hr class="border-info">
							<div class="form-group">
								<div class="form-row vaRow mb-1">
									<label class="col-md-4 col-form-label">Ladepunkt 2</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($nachtladens1old == 0) echo " active" ?>">
											<input type="radio" name="nachtladens1" id="nachtladens1Off" value="0"<?php if($nachtladens1old == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($nachtladens1old == 1) echo " active" ?>">
											<input type="radio" name="nachtladens1" id="nachtladens1On" value="1"<?php if($nachtladens1old == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
								<div id="nachtladenans1" class="hide">
									<div class="form-row mb-1">
										<div class="col">
											Nachtladen
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="nachtlls1" class="col-md-4 col-form-label">Stromstärke in A</label>
										<div class="col-md-8">
											<div class="form-row vaRow mb-1">
												<label for="nachtlls1" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $nachtlls1old; ?> A</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" name="nachtlls1" id="nachtlls1" min="6" max="32" step="1" value="<?php echo $nachtlls1old; ?>">
												</div>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
										<div class="col-md-4">
											Zeitspanne
										</div>
										<div class="col">
											<div class="form-row">
												<div class="col-sm-6">
													<div class="input-group">
														<div class="input-group-prepend">
															<div class="input-group-text">
																Anfang
															</div>
														</div>
														<select name="nachtladenabuhrs1" id="nachtladenabuhrs1" class="form-control">
															<option <?php if($nachtladenabuhrs1old == 17) echo "selected" ?> value="17">17:00</option>
															<option <?php if($nachtladenabuhrs1old == 18) echo "selected" ?> value="18">18:00</option>
															<option <?php if($nachtladenabuhrs1old == 19) echo "selected" ?> value="19">19:00</option>
															<option <?php if($nachtladenabuhrs1old == 20) echo "selected" ?> value="20">20:00</option>
															<option <?php if($nachtladenabuhrs1old == 21) echo "selected" ?> value="21">21:00</option>
															<option <?php if($nachtladenabuhrs1old == 22) echo "selected" ?> value="22">22:00</option>
															<option <?php if($nachtladenabuhrs1old == 23) echo "selected" ?> value="23">23:00</option>
															<option <?php if($nachtladenabuhrs1old == 24) echo "selected" ?> value="24">24:00</option>
														</select>
													</div>
												</div>
												<div class="col-sm-6">
													<div class="input-group">
														<div class="input-group-prepend">
															<div class="input-group-text">
																Ende
															</div>
														</div>
														<select name="nachtladenbisuhrs1" id="nachtladenbisuhrs1" class="form-control">
															<option <?php if($nachtladenbisuhrs1old == 0) echo "selected" ?> value="0">0:00</option>
															<option <?php if($nachtladenbisuhrs1old == 1) echo "selected" ?> value="1">1:00</option>
															<option <?php if($nachtladenbisuhrs1old == 2) echo "selected" ?> value="2">2:00</option>
															<option <?php if($nachtladenbisuhrs1old == 3) echo "selected" ?> value="3">3:00</option>
															<option <?php if($nachtladenbisuhrs1old == 4) echo "selected" ?> value="4">4:00</option>
															<option <?php if($nachtladenbisuhrs1old == 5) echo "selected" ?> value="5">5:00</option>
															<option <?php if($nachtladenbisuhrs1old == 6) echo "selected" ?> value="6">6:00</option>
															<option <?php if($nachtladenbisuhrs1old == 7) echo "selected" ?> value="7">7:00</option>
															<option <?php if($nachtladenbisuhrs1old == 8) echo "selected" ?> value="8">8:00</option>
															<option <?php if($nachtladenbisuhrs1old == 9) echo "selected" ?> value="9">9:00</option>
														</select>
													</div>
												</div>
											</div>
											<span class="form-text small">Zeitspanne, in der nachts geladen werden soll.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="nachtsocs1" class="col-md-4 col-form-label">SoC Sonntag bis Donnerstag</label>
										<div class="col-md-8">
											<div class="form-row vaRow mb-1">
												<label for="nachtsocs1" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $nachtsocs1old; ?> %</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" name="nachtsocs1" id="nachtsocs1" min="5" max="100" step="5" value="<?php echo $nachtsocs1old; ?>">
												</div>
											</div>
											<span class="form-text small">Wenn SoC Modul vorhanden wird Nachts in dem angegebenen Zeitfenster bis zur Überschreitung von xx% SoC geladen. Das SoC Fenster is von von Sonntag Abend bis Freitag Morgen aktiv.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="nachtsoc1s1" class="col-md-4 col-form-label">SoC Freitag bis Sonntag</label>
										<div class="col-md-8">
											<div class="form-row vaRow mb-1">
												<label for="nachtsoc1s1" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $nachtsoc1s1old; ?> %</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" name="nachtsoc1s1" id="nachtsoc1s1" min="5" max="100" step="5" value="<?php echo $nachtsoc1s1old; ?>">
												</div>
											</div>
											<span class="form-text small">Wenn SoC Modul vorhanden wird Nachts in dem angegebenen Zeitfenster bis zur Überschreitung von xx% SoC geladen. Das SoC Fenster is von von Freitag Morgen bis Sonntag Abend aktiv.</span>
										</div>
									</div>
									<hr class="border-info">
									<div class="form-row mb-1">
										<div class="col">
											Morgensladen
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="nacht2lls1" class="col-md-4 col-form-label">Stromstärke in A</label>
										<div class="col-md-8">
											<div class="form-row vaRow mb-1">
												<label for="nacht2lls1" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $nacht2lls1old; ?> A</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" name="nacht2lls1" id="nacht2lls1" min="6" max="32" step="1" value="<?php echo $nacht2lls1old; ?>">
												</div>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
										<div class="col-md-4">
											Zeitspanne
										</div>
										<div class="col">
											<div class="form-row">
												<div class="col-sm-6">
													<div class="input-group">
														<div class="input-group-prepend">
															<div class="input-group-text">
																Anfang
															</div>
														</div>
														<select name="nachtladen2abuhrs1" id="nachtladen2abuhrs1" class="form-control">
															<option <?php if($nachtladen2abuhrs1old == 3) echo "selected" ?> value="3">03:00</option>
															<option <?php if($nachtladen2abuhrs1old == 4) echo "selected" ?> value="4">04:00</option>
															<option <?php if($nachtladen2abuhrs1old == 5) echo "selected" ?> value="5">05:00</option>
															<option <?php if($nachtladen2abuhrs1old == 6) echo "selected" ?> value="6">06:00</option>
															<option <?php if($nachtladen2abuhrs1old == 7) echo "selected" ?> value="7">07:00</option>
															<option <?php if($nachtladen2abuhrs1old == 8) echo "selected" ?> value="8">08:00</option>
															<option <?php if($nachtladen2abuhrs1old == 9) echo "selected" ?> value="9">09:00</option>
														</select>
													</div>
												</div>
												<div class="col-sm-6">
													<div class="input-group">
														<div class="input-group-prepend">
															<div class="input-group-text">
																Ende
															</div>
														</div>
														<select name="nachtladen2bisuhrs1" id="nachtladen2bisuhrs1" class="form-control">
															<option <?php if($nachtladen2bisuhrs1old == 4) echo "selected" ?> value="4">04:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 5) echo "selected" ?> value="5">05:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 6) echo "selected" ?> value="6">06:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 7) echo "selected" ?> value="7">07:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 8) echo "selected" ?> value="8">08:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 9) echo "selected" ?> value="9">09:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 10) echo "selected" ?> value="10">10:00</option>
														</select>
													</div>
												</div>
											</div>
											<span class="form-text small">Zeitspanne, in der morgens geladen werden soll.</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_nachtladen() {
								if($('#nachtladenOff').prop("checked")) {
									hideSection('#nachtladenan');
								} else {
									showSection('#nachtladenan');
								}
							}

							function visibility_nachtladens1() {
								if($('#nachtladens1Off').prop("checked")) {
									hideSection('#nachtladenans1');
								} else {
									showSection('#nachtladenans1');
								}
							}

							$('input[type=radio][name=nachtladen]').change(function(){
								visibility_nachtladen();
							});

							$('input[type=radio][name=nachtladens1]').change(function(){
								visibility_nachtladens1();
							});

							visibility_nachtladen();
							visibility_nachtladens1()
						});
					</script>
				</div>

				<!-- EVU basiertes Lastmanagement -->
				<div class="card border-warning">
					<div class="card-header bg-warning">
						EVU basiertes Lastmanagement
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									maximale Stromstärken in A
								</div>
								<div class="col">
									<div class="form-row">
										<div class="col-sm-4">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														Phase 1
													</div>
												</div>
												<input type="number" min="7" step="1" name="lastmaxap1" id="lastmaxap1" class="form-control" value="<?php echo $lastmaxap1old ?>">
											</div>
										</div>
										<div class="col-sm-4">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														Phase 2
													</div>
												</div>
												<input type="number" min="7" step="1" name="lastmaxap2" id="lastmaxap2" class="form-control" value="<?php echo $lastmaxap2old ?>">
											</div>
										</div>
										<div class="col-sm-4">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														Phase 3
													</div>
												</div>
												<input type="number" min="7" step="1" name="lastmaxap3" id="lastmaxap3" class="form-control" value="<?php echo $lastmaxap3old ?>">
											</div>
										</div>
									</div>
									<span class="form-text small">Gültige Werte: ganze Zahl größer 7. Definiert die maximal erlaubte Stromstärke der einzelnen Phasen des <b>Hausanschlusses</b> im Sofort Laden Modus, sofern das EVU Modul die Werte je Phase zur Verfügung stellt. Hiermit ist nicht der Anschluss der openWB gemeint! Übliche Werte für ein EFH/MFH sind im Bereich 35 bis 63A.</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="lastmmaxw" class="col-md-4 col-form-label">maximaler Bezug in W</label>
								<div class="col">
									<input class="form-control" type="number" min="2000" max="1000000" step="1000" name="lastmmaxw" id="lastmmaxw" value="<?php echo $lastmmaxwold ?>">
									<span class="form-text small">Gültige Werte: 2000-1000000W in ganzen 1000W-Schritten. Definiert die maximal erlaubten bezogenen Watt des Hausanschlusses im Sofort Laden Modus, sofern die Bezugsleistung bekannt ist.</span>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Loadsharing -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Loadsharing
					</div>
					<div class="card-body">
						<div id="loadsharingoffdiv" class="card-text alert alert-info hide">
							Diese Einstellungen sind nur verfügbar, wenn mindestens zwei Ladepunkte konfiguriert sind.
						</div>
						<div id="loadsharingdiv" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Loadsharing für Ladepunkte 1 und 2</label>
									<div class="col">
										<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($loadsharinglp12old == 0) echo " active" ?>">
												<input type="radio" name="loadsharinglp12" id="loadsharinglp12Off" value="0"<?php if($loadsharinglp12old == 0) echo " checked=\"checked\"" ?>>Deaktiviert
											</label>
											<label class="btn btn-outline-info<?php if($loadsharinglp12old == 1) echo " active" ?>">
												<input type="radio" name="loadsharinglp12" id="loadsharinglp12On" value="1"<?php if($loadsharinglp12old == 1) echo " checked=\"checked\"" ?>>Aktiviert
											</label>
										</div>
										<span class="form-text small">
											Wenn Ladepunkt 1 und 2 sich eine Zuleitung teilen, diese Option aktivieren. Sie stellt in jedem Lademodus sicher, dass nicht mehr als 16 bzw. 32A je Phase in der Summe von Ladepunkt 1 und 2 genutzt werden.
											<span class="text-danger">Bei der OpenWB Duo muss diese Option aktiviert werden!</span>
										</span>
									</div>
								</div>
								<div id="loadsharinglp12div" class="hide">
									<div class="form-row mb-2">
										<label class="col-md-4 col-form-label">Maximaler Strom</label>
										<div class="col">
											<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($loadsharingalp12old == 16) echo " active" ?>">
													<input type="radio" name="loadsharingalp12" id="loadsharingalp1216" value="16"<?php if($loadsharingalp12old == 16) echo " checked=\"checked\"" ?>>16 Ampere
												</label>
												<label class="btn btn-outline-info<?php if($loadsharingalp12old == 32) echo " active" ?>">
													<input type="radio" name="loadsharingalp12" id="loadsharingalp1232" value="32"<?php if($loadsharingalp12old == 32) echo " checked=\"checked\"" ?>>32 Ampere
												</label>
											</div>
										</div>
									</div>
									<div class="alert alert-warning">
										<p class="text-danger">Der richtige Anschluss ist zu gewährleisten.</p>
										<div class="row">
											<div class="col-md-4">Ladepunkt 1:</div>
											<div class="col">
												<ul>
													<li>Zuleitung Phase 1 = Phase 1</li>
													<li>Zuleitung Phase 2 = Phase 2</li>
													<li>Zuleitung Phase 3 = Phase 3</li>
												</ul>
											</div>
										</div>
										<div class="row">
											<div class="col-md-4">Ladepunkt 2:</div>
											<div class="col">
												<ul>
													<li>Zuleitung Phase 1 = <span class="text-danger">Phase 2</span></li>
													<li>Zuleitung Phase 2 = <span class="text-danger">Phase 3</span></li>
													<li>Zuleitung Phase 3 = <span class="text-danger">Phase 1</span></li>
												</ul>
											</div>
										</div>
										<p>Durch das Drehen der Phasen ist sichergestellt, dass 2 einphasige Autos mit voller Geschwindigkeit laden können.</p>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_loadsharinglp12() {
								if($('#loadsharinglp12Off').prop("checked")) {
									hideSection('#loadsharinglp12div');
								} else {
									showSection('#loadsharinglp12div');
								}
							}

							$('input[type=radio][name=loadsharinglp12]').change(function(){
								visibility_loadsharinglp12();
							});

							visibility_loadsharinglp12();
						});
					</script>
				</div>

				<div class="form-row text-center">
					<div class="col">
						<button type="submit" class="btn btn-success">Speichern</button>
					</div>
				</div>
			</form>
		</div>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Einstellungen/Allgemein</small>
			</div>
		</footer>


		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navAllgemein').addClass('disabled');
				}
			);

			$(document).ready(function(){

				$('.rangeInput').on('input', function() {
					// show slider value in label of class valueLabel
					updateLabel($(this).attr('id'));
				});

			});  // end document ready

		</script>

	</body>
</html>
