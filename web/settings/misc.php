<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Einstellungen</title>
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
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
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

			$lastrfid = explode(',',trim( file_get_contents( '/var/www/html/openWB/ramdisk/rfidlasttag' )))[0];
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Verschiedene Einstellungen</h1>
			<form action="./settings/saveconfig.php" method="POST">

				<!-- Allgemeine Funktionen -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Allgemeine Funktionen
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Geschwindigkeit Regelintervall</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($dspeedold == 0) echo " active" ?>">
											<input type="radio" name="dspeed" id="dspeed0" value="0"<?php if($dspeedold == 0) echo " checked=\"checked\"" ?>>Normal
										</label>
										<label class="btn btn-outline-info<?php if($dspeedold == 2) echo " active" ?>">
											<input type="radio" name="dspeed" id="dspeed2" value="2"<?php if($dspeedold == 2) echo " checked=\"checked\"" ?>>Langsam
										</label>
										<label class="btn btn-outline-info<?php if($dspeedold == 3) echo " active" ?>">
											<input type="radio" name="dspeed" id="dspeed3" value="3"<?php if($dspeedold == 3) echo " checked=\"checked\"" ?>>Sehr Langsam
										</label>
									</div>
									<span class="form-text small">
										Sollten Probleme, oder Fehlermeldungen, auftauchen, zunächst das Regelintervall auf "Normal" stellen. Werden Module genutzt, welche z.B. eine Online API zur Abfrage nutzen, oder möchte man weniger regeln, kann man das Regelintervall auf "Langsam" (20 Sekunden) herabsetzen. Die Einstellungen „Sehr Langsam“ führt zu einer Regelzeit von 60 Sekunden.<br>
										<span class="text-danger">Nicht nur die Regelung der PV geführten Ladung, sondern auch Ladestromänderung, beispielsweise “Stop“ etc., werden dann nur noch in diesem Intervall ausgeführt. Die Regelung wird insgesamt träger. Ebenso können eingestellte Verzögerungen um den Faktor der Änderung langsamer ausgeführt werden. Solange es keinen triftigen Grund gibt sollte immer Normal gewählt werden.</span>
									</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Ladetaster</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($ladetasterold == 0) echo " active" ?>">
											<input type="radio" name="ladetaster" id="ladetasterOff" value="0"<?php if($ladetasterold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($ladetasterold == 1) echo " active" ?>">
											<input type="radio" name="ladetaster" id="ladetasterOn" value="1"<?php if($ladetasterold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
									<span class="form-text small">Wenn aktiviert, sind nach einem Neustart die externen Taster aktiv. Wenn keine verbaut sind, diese Option ausschalten.</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Lademodus nach Start der openWB</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($bootmodusold == 3) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus3" value="3"<?php if($bootmodusold == 3) echo " checked=\"checked\"" ?>>Stop
										</label>
										<label class="btn btn-outline-info<?php if($bootmodusold == 4) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus4" value="4"<?php if($bootmodusold == 4) echo " checked=\"checked\"" ?>>Standby
										</label>
										<label class="btn btn-outline-info<?php if($bootmodusold == 2) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus2" value="2"<?php if($bootmodusold == 2) echo " checked=\"checked\"" ?>>Nur PV
										</label>
										<label class="btn btn-outline-info<?php if($bootmodusold == 1) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus1" value="1"<?php if($bootmodusold == 1) echo " checked=\"checked\"" ?>>Min + PV
										</label>
										<label class="btn btn-outline-info<?php if($bootmodusold == 0) echo " active" ?>">
											<input type="radio" name="bootmodus" id="bootmodus0" value="0"<?php if($bootmodusold == 0) echo " checked=\"checked\"" ?>>Sofort Laden
										</label>
									</div>
									<span class="form-text small">Definiert den Lademodus nach Boot der openWB.</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Netzschutz</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($netzabschaltunghzold == 0) echo " active" ?>">
											<input type="radio" name="netzabschaltunghz" id="netzabschaltunghzOff" value="0"<?php if($netzabschaltunghzold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($netzabschaltunghzold == 1) echo " active" ?>">
											<input type="radio" name="netzabschaltunghz" id="netzabschaltunghzOn" value="1"<?php if($netzabschaltunghzold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
									<span class="form-text small">
										Diese Option ist standardmäßig aktiviert und sollte so belassen werden. Bei Unterschreitung einer kritischen Frequenz des Stromnetzes wird die Ladung nach einer zufälligen Zeit zwischen 1 und 90 Sekunden pausiert. Der Lademodus wechselt auf "Stop".
										Sobald die Frequenz wieder in einem normalen Bereich ist wird automatisch der zuletzt gewählte Lademodus wieder aktiviert.
										Ebenso wird die Ladung bei Überschreiten von 51,8 Hz unterbrochen. Dies ist dann der Fall, wenn der Energieversorger Wartungsarbeiten am (Teil-)Netz durchführt und auf einen vorübergehenden Generatorbetrieb umschaltet.
										Die Erhöhung der Frequenz wird durchgeführt, um die PV Anlagen abzuschalten.<br>
										<span class="text-danger">Die Option ist nur aktiv, wenn der Ladepunkt die Frequenz übermittelt. Jede openWB Series1/2 unterstützt dies.</span>
									</span>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									CP Unterbrechung
								</div>
								<div class="col">
									<span class="form-text small">Diese Option erfordert die verbaute Addon Platine und die korrekte Verdrahtung des CP Signals durch die Addon Platine. Sie ist für Fahrzeuge, die nach einer gewissen Zeit einer pausierten Ladung nicht von alleine die Ladung wieder beginnen. Nur aktivieren, wenn es ohne die Option Probleme gibt.</span>
								</div>
							</div>
							<div class="form-row mt-2 mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Ladepunkt 1</label>
								</div>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($cpunterbrechunglp1old == 0) echo " active" ?>">
										<input type="radio" name="cpunterbrechunglp1" id="cpunterbrechunglp1Off" value="0"<?php if($cpunterbrechunglp1old == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($cpunterbrechunglp1old == 1) echo " active" ?>">
										<input type="radio" name="cpunterbrechunglp1" id="cpunterbrechunglp1On" value="1"<?php if($cpunterbrechunglp1old == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div class="form-row mb-1 lp1cpon hide">
								<label for="cpunterbrechungdauerlp1" class="col-md-4 col-form-label">Dauer der Unterbrechung</label>
								<div class="col-md-8">
									<div class="form-row vaRow mb-1">
										<label for="cpunterbrechungdauerlp1" class="col-2 col-form-label valueLabel" suffix="Sek"><?php echo $cpunterbrechungdauerlp1old; ?> Sek</label>
										<div class="col-10">
											<input type="range" class="form-control-range rangeInput" name="cpunterbrechungdauerlp1" id="cpunterbrechungdauerlp1" min="4" max="150" step="1" value="<?php echo $cpunterbrechungdauerlp1old; ?>">
										</div>
									</div>
									<span class="form-text small">
										Die Standardeinstellung ist 4 Sekunden. Falls ein Fahrzeug den Ladevorgang nicht zuverlässig startet, kann dieser Wert erhöht werden.
										<span class="text-danger">Achtung: experimentelle Einstellung!</span>
									</span>
								</div>
							</div>
							<div id="lp2cpdiv" class="hide">
								<div class="form-row mt-2">
									<div class="col-md-4">
										<label class="col-form-label">Ladepunkt 2</label>
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($cpunterbrechunglp2old == 0) echo " active" ?>">
											<input type="radio" name="cpunterbrechunglp2" id="cpunterbrechunglp2Off" value="0"<?php if($cpunterbrechunglp2old == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($cpunterbrechunglp2old == 1) echo " active" ?>">
											<input type="radio" name="cpunterbrechunglp2" id="cpunterbrechunglp2On" value="1"<?php if($cpunterbrechunglp2old == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
								<div class="form-row mb-1 lp2cpon hide">
									<label for="cpunterbrechungdauerlp2" class="col-md-4 col-form-label">Dauer der Unterbrechung</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="cpunterbrechungdauerlp2" class="col-2 col-form-label valueLabel" suffix="Sek"><?php echo $cpunterbrechungdauerlp2old; ?> Sek</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="cpunterbrechungdauerlp2" id="cpunterbrechungdauerlp2" min="4" max="150" step="1" value="<?php echo $cpunterbrechungdauerlp2old; ?>">
											</div>
										</div>
										<span class="form-text small">
											Die Standardeinstellung ist 4 Sekunden. Falls ein Fahrzeug den Ladevorgang nicht zuverlässig startet, kann dieser Wert erhöht werden.
										<span class="text-danger">Achtung: experimentelle Einstellung!</span>
									</span>
									</div>
								</div>
							</div>
							<div class="form-row mt-2 mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Ladung nach CP Unterbrechung aktiv halten</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($cpunterbrechungmindestlaufzeitaktivold == 0) echo " active" ?>">
											<input type="radio" name="cpunterbrechungmindestlaufzeitaktiv" id="cpunterbrechungmindestlaufzeitaktivOff" value="0"<?php if($cpunterbrechungmindestlaufzeitaktivold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($cpunterbrechungmindestlaufzeitold == 1) echo " active" ?>">
											<input type="radio" name="cpunterbrechungmindestlaufzeitaktiv" id="cpunterbrechungmindestlaufzeitaktivOn" value="1"<?php if($cpunterbrechungmindestlaufzeitaktivold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
									<span class="form-text small">
										Diese Option hält die Ladung im nurPV Modus eine Zeit lang aktiv, auch wenn kurz nach der CP Unterbrechung die Mindestladeleistung unterschritten wird noch bevor die Ladung begonnen hat. 
										Dies ist immer dann hilfreich wenn der Ladestart nach CP Unterbrechung erst verzögert erfolgt, z.b. bei PSA (Peugeot, Opel).
										Wird nach CP Unterbrechung kein Ladestart registriert wird keine erneute CP Unterbrechung durchgeführt.
										<span class="text-danger">Achtung: experimentelle Einstellung!</span>
									</span>
								</div>
							</div>
							<div class="form-row mb-1 cpminlaufzeit hide">
								<label for="cpunterbrechungmindestlaufzeit" class="col-md-4 col-form-label">Mindestlaufzeit nach Unterbrechung</label>
								<div class="col-md-8">
									<div class="form-row vaRow mb-1">
										<label for="cpunterbrechungmindestlaufzeit" class="col-2 col-form-label valueLabel" suffix="Sek"><?php echo $cpunterbrechungmindestlaufzeitold; ?> Sek</label>
										<div class="col-10">
											<input type="range" class="form-control-range rangeInput" name="cpunterbrechungmindestlaufzeit" id="cpunterbrechungmindestlaufzeit" min="10" max="60" step="10" value="<?php echo $cpunterbrechungmindestlaufzeitold; ?>">
										</div>
									</div>
									<span class="form-text small">
										Die Standardeinstellung ist 30 Sekunden. Falls ein Fahrzeug den Ladevorgang nicht zuverlässig startet, kann dieser Wert erhöht werden.
										<span class="text-danger">Achtung: experimentelle Einstellung!</span>
									</span>
								</div>
							</div>

						</div>
					</div>
					<script>
						var lp2akt = <?php echo $lastmanagementold ?>;

						function visibility_lp1cp() {
							if($('#cpunterbrechunglp1Off').prop("checked")) {
								hideSection('.lp1cpon');
							} else {
								showSection('.lp1cpon', false);
							}
						}

						function visibility_lp2cp() {
							if($('#cpunterbrechunglp2Off').prop("checked")) {
								hideSection('.lp2cpon');
							} else {
								showSection('.lp2cpon', false);
							}
						}
						
						function visibility_cpminlaufzeit() {
							if($('#cpunterbrechungmindestlaufzeitaktivOff').prop("checked")) {
								hideSection('.cpminlaufzeit');
							} else {
								showSection('.cpminlaufzeit', false);
							}
						}

						$(document).ready(function(){
							if(lp2akt == '0') {
								hideSection('#lp2cpdiv');
							} else {
								showSection('#lp2cpdiv');
							}

							$('input[type=radio][name=cpunterbrechunglp1]').change(function(){
								visibility_lp1cp();
							});

							$('input[type=radio][name=cpunterbrechunglp2]').change(function(){
								visibility_lp2cp();
							});

							$('input[type=radio][name=cpunterbrechungmindestlaufzeitaktiv]').change(function(){
								visibility_cpminlaufzeit();
							});

							visibility_lp1cp();
							visibility_lp2cp();
							visibility_cpminlaufzeit();
						});
					</script>
				</div>

				<!-- RFID -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">RFID</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($rfidaktold == 0) echo " active" ?>">
											<input type="radio" name="rfidakt" id="rfidaktOff" value="0"<?php if($rfidaktold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($rfidaktold == 1) echo " active" ?>">
											<input type="radio" name="rfidakt" id="rfidaktOn1" value="1"<?php if($rfidaktold == 1) echo " checked=\"checked\"" ?>>An Modus 1
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($rfidaktold == 2) echo " active" ?>">
											<input type="radio" name="rfidakt" id="rfidaktOn2" value="2"<?php if($rfidaktold == 2) echo " checked=\"checked\"" ?>>An Modus 2
										</label>

									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body hide" id="rfidandiv">
						<div class="form-row form-group">
							<div class="col">
								Zuletzt gescannter RFID Tag: <?php echo $lastrfid ?>
							</div>
						</div>
						<div id="rfidan1div" class="hide">
							<hr class="border-secondary">
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Autos zuweisen
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Ladepunkt 1
									</div>
								</div>
								<div class="form-row">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 1
												</div>
											</div>
											<input type="text" name="rfidlp1c1" id="rfidlp1c1" class="form-control" value="<?php echo $rfidlp1c1old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 2
												</div>
											</div>
											<input type="text" name="rfidlp1c2" id="rfidlp1c2" class="form-control" value="<?php echo $rfidlp1c2old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 3
												</div>
											</div>
											<input type="text" name="rfidlp1c3" id="rfidlp1c3" class="form-control" value="<?php echo $rfidlp1c3old ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Ladepunkt 2
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 1
												</div>
											</div>
											<input type="text" name="rfidlp2c1" id="rfidlp2c1" class="form-control" value="<?php echo $rfidlp2c1old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 2
												</div>
											</div>
											<input type="text" name="rfidlp2c2" id="rfidlp2c2" class="form-control" value="<?php echo $rfidlp2c2old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Auto 3
												</div>
											</div>
											<input type="text" name="rfidlp2c3" id="rfidlp2c3" class="form-control" value="<?php echo $rfidlp2c3old ?>">
										</div>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col-md-4">
										Lademodus ändern
									</div>
									<div class="col form-text small">
										Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Stop
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidstop" id="rfidstop" class="form-control" value="<?php echo $rfidstopold ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidstop2" id="rfidstop2" class="form-control" value="<?php echo $rfidstop2old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidstop3" id="rfidstop3" class="form-control" value="<?php echo $rfidstop3old ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Standby
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidstandby" id="rfidstandby" class="form-control" value="<?php echo $rfidstandbyold ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidstandby2" id="rfidstandby2" class="form-control" value="<?php echo $rfidstandby2old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidstandby3" id="rfidstandby3" class="form-control" value="<?php echo $rfidstandby3old ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Sofort Laden
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidsofort" id="rfidsofort" class="form-control" value="<?php echo $rfidsofortold ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidsofort2" id="rfidsofort2" class="form-control" value="<?php echo $rfidsofort2old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidsofort3" id="rfidsofort3" class="form-control" value="<?php echo $rfidsofort3old ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Min + PV Laden
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidminpv" id="rfidminpv" class="form-control" value="<?php echo $rfidminpvold ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidminpv2" id="rfidminpv2" class="form-control" value="<?php echo $rfidminpv2old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidminpv3" id="rfidminpv3" class="form-control" value="<?php echo $rfidminpv3old ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Nur PV
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidnurpv" id="rfidnurpv" class="form-control" value="<?php echo $rfidnurpvold ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidnurpv2" id="rfidnurpv2" class="form-control" value="<?php echo $rfidnurpv2old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidnurpv3" id="rfidnurpv3" class="form-control" value="<?php echo $rfidnurpv3old ?>">
										</div>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col-md-4">
										Ladepunkte aktivieren
									</div>
									<div class="col form-text small">
										Kann auch in Kombination mit einem RFID Tag zur Autozuweisung genutzt werden.
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Ladepunkt 1
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidlp1start1" id="rfidlp1start1" class="form-control" value="<?php echo $rfidlp1start1old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidlp1start2" id="rfidlp1start2" class="form-control" value="<?php echo $rfidlp1start2old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidlp1start3" id="rfidlp1start3" class="form-control" value="<?php echo $rfidlp1start3old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 4
												</div>
											</div>
											<input type="text" name="rfidlp1start4" id="rfidlp1start4" class="form-control" value="<?php echo $rfidlp1start4old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 5
												</div>
											</div>
											<input type="text" name="rfidlp1start5" id="rfidlp1start5" class="form-control" value="<?php echo $rfidlp1start5old ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Ladepunkt 2
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 1
												</div>
											</div>
											<input type="text" name="rfidlp2start1" id="rfidlp2start1" class="form-control" value="<?php echo $rfidlp2start1old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 2
												</div>
											</div>
											<input type="text" name="rfidlp2start2" id="rfidlp2start2" class="form-control" value="<?php echo $rfidlp2start2old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 3
												</div>
											</div>
											<input type="text" name="rfidlp2start3" id="rfidlp2start3" class="form-control" value="<?php echo $rfidlp2start3old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 4
												</div>
											</div>
											<input type="text" name="rfidlp2start4" id="rfidlp2start4" class="form-control" value="<?php echo $rfidlp2start4old ?>">
										</div>
									</div>
									<div class="col-lg-4">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Tag 5
												</div>
											</div>
											<input type="text" name="rfidlp2start5" id="rfidlp2start5" class="form-control" value="<?php echo $rfidlp2start5old ?>">
										</div>
									</div>
								</div>
							</div>
						</div>
						<div id="rfidan2div" class="hide">
							<div class="alert alert-info">
								Im Modus 2 wird eine Kommaseparierte Liste mit gültigen RFID Tags hinterlegt. Gescannt werden kann an jedem möglichen RFID Leser. Heißt auch bei mehreren Ladepunkten kann an einem zentralen RFID Leser gescannt werden. Der gescannte Tag wird dem zuletzt angeschlossenenen Auto zugewiesen, schaltet den Ladepunkt frei und vermerkt dies für das Ladelog. Wird erst gescannt und dann ein Auto angeschlossen wird der Tag dem Auto zugewiesen das als nächstes ansteckt. Wird 5 Minuten nach Scannen kein Auto angeschlossen wird der Tag verworfen. Jeder Ladepunkt wird nach abstecken automatisch wieder gesperrt.
							</div>
							<div class="form-group mb-1">
								<div class="form-row">
									<div class="col">
										Erlaubte Tags als Kommaseparierte Liste ohne Leerzeichen
									</div>
								</div>
								<div class="form-row">
									<div class="col-lg-12">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													Liste
												</div>
											</div>
											<input type="text" name="rfidlist" id="rfidlist" class="form-control" value="<?php echo $rfidlistold ?>">
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						function visibility_rfidakt() {
							if($('#rfidaktOff').prop("checked")) {
								hideSection('#rfidandiv');
								hideSection('#rfidan1div');
								hideSection('#rfidan2div');
							} else {
								if($('#rfidaktOn1').prop("checked")) {
									showSection('#rfidandiv', false);
									showSection('#rfidan1div');
									hideSection('#rfidan2div');

								} else {
									showSection('#rfidandiv', false);
									showSection('#rfidan2div');
									hideSection('#rfidan1div');
								}
							}
						}

						$(document).ready(function(){
							$('input[type=radio][name=rfidakt]').change(function(){
								visibility_rfidakt();
							});

							visibility_rfidakt();
						});
					</script>
				</div>

				<!-- Benachrichtigungen mit Pushover -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Benachrichtigungen mit Pushover</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($pushbenachrichtigungold == 0) echo " active" ?>">
											<input type="radio" name="pushbenachrichtigung" id="pushbenachrichtigungOff" value="0"<?php if($pushbenachrichtigungold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($pushbenachrichtigungold == 1) echo " active" ?>">
											<input type="radio" name="pushbenachrichtigung" id="pushbenachrichtigungOn" value="1"<?php if($pushbenachrichtigungold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							<p>Zur Nutzung von Pushover muss ein Konto auf Pushover.net bestehen. Zudem muss im Pushover-Nutzerkonto eine Applikation openWB eingerichtet werden, um den benötigten API-Token/Key zu erhalten.</p>
							Wenn Pushover eingeschaltet ist, werden die Zählerstände aller konfigurierten Ladepunkte immer zum 1. des Monats gepusht.
						</div>
						<div id="pushban" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="pushoveruser" class="col-md-4 col-form-label">Pushover User Key</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-user"></i>
												</div>
											</div>
											<input type="text" name="pushoveruser" id="pushoveruser" value="<?php echo $pushoveruserold ?>" placeholder="User Token" class="form-control">
										</div>
									</div>
								</div>
								<div class="form-row">
									<label for="pushovertoken" class="col-md-4 col-form-label">Pushover API-Token/Key</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-lock"></i>
												</div>
											</div>
											<input type="text" name="pushovertoken" id="pushovertoken" value="<?php echo $pushovertokenold ?>" placeholder="App Token" class="form-control">
										</div>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-group">
								<div class="form-row">
									<div class="col">
										Benachrichtigungen
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Beim Starten der Ladung</label>
									</div>
									<div class="btn-group btn-group-toggle col-md-8" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($pushbstartlold == 0) echo " active" ?>">
											<input type="radio" name="pushbstartl" id="pushbstartlOff" value="0"<?php if($pushbstartlold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($pushbstartlold == 1) echo " active" ?>">
											<input type="radio" name="pushbstartl" id="pushbstartlOn" value="1"<?php if($pushbstartlold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Beim Stoppen der Ladung</label>
									</div>
									<div class="btn-group btn-group-toggle col-md-8" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($pushbstoplold == 0) echo " active" ?>">
											<input type="radio" name="pushbstopl" id="pushbstoplOff" value="0"<?php if($pushbstoplold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($pushbstoplold == 1) echo " active" ?>">
											<input type="radio" name="pushbstopl" id="pushbstoplOn" value="1"<?php if($pushbstoplold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Beim Einstecken des Fahrzeugs</label>
									</div>
									<div class="btn-group btn-group-toggle col-md-8" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($pushbplugold == 0) echo " active" ?>">
											<input type="radio" name="pushbplug" id="pushbplugOff" value="0"<?php if($pushbplugold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($pushbplugold == 1) echo " active" ?>">
											<input type="radio" name="pushbplug" id="pushbplugOn" value="1"<?php if($pushbplugold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Bei Triggern von Smart Home Aktionen</label>
									</div>
									<div class="btn-group btn-group-toggle col-md-8" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($pushbsmarthomeold == 0) echo " active" ?>">
											<input type="radio" name="pushbsmarthome" id="pushbsmarthomeOff" value="0"<?php if($pushbsmarthomeold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($pushbsmarthomeold == 1) echo " active" ?>">
											<input type="radio" name="pushbsmarthome" id="pushbsmarthomeOn" value="1"<?php if($pushbsmarthomeold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						function visibility_pushbenachrichtigung() {
							if($('#pushbenachrichtigungOff').prop("checked")) {
								hideSection('#pushban');
							} else {
								showSection('#pushban');
							}
						}

						$(document).ready(function(){
							$('input[type=radio][name=pushbenachrichtigung]').change(function(){
								visibility_pushbenachrichtigung();
							});

							visibility_pushbenachrichtigung();
						});
					</script>
				</div>

				<!-- LED Ausgänge -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">LED Ausgänge</div>
								<div class="col">
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($ledsaktold == 0) echo " active" ?>">
											<input type="radio" name="ledsakt" id="ledsaktOff" value="0"<?php if($ledsaktold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($ledsaktold == 1) echo " active" ?>">
											<input type="radio" name="ledsakt" id="ledsaktOn" value="1"<?php if($ledsaktold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body hide" id="ledsan">
						<div class="form-group">
							<div class="form-row">
								<div class="col">
									Ladung nicht freigegeben
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0sofort" class="col-md-4 col-form-label">Sofort Laden Modus</label>
								<div class="col">
									<select name="led0sofort" id="led0sofort" class="form-control">
										<option <?php if($led0sofortold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0sofortold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0sofortold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0sofortold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0sofortold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0sofortold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0sofortold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0sofortold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0sofortold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0sofortold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0sofortold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0sofortold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0sofortold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0sofortold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0nurpv" class="col-md-4 col-form-label">Nur PV Laden Modus</label>
								<div class="col">
									<select name="led0nurpv" id="led0nurpv" class="form-control">
										<option <?php if($led0nurpvold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0nurpvold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0nurpvold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0nurpvold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0nurpvold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0nurpvold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0nurpvold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0nurpvold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0nurpvold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0nurpvold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0nurpvold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0nurpvold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0nurpvold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0nurpvold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0minpv" class="col-md-4 col-form-label">Min + PV Laden Modus</label>
								<div class="col">
									<select name="led0minpv" id="led0minpv" class="form-control">
										<option <?php if($led0minpvold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0minpvold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0minpvold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0minpvold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0minpvold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0minpvold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0minpvold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0minpvold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0minpvold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0minpvold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0minpvold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0minpvold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0minpvold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0minpvold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0standby" class="col-md-4 col-form-label">Standby Modus</label>
								<div class="col">
									<select name="led0standby" id="led0standby" class="form-control">
										<option <?php if($led0standbyold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0standbyold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0standbyold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0standbyold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0standbyold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0standbyold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0standbyold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0standbyold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0standbyold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0standbyold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0standbyold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0standbyold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0standbyold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0standbyold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="led0stop" class="col-md-4 col-form-label">Stop Modus</label>
								<div class="col">
									<select name="led0stop" id="led0stop" class="form-control">
										<option <?php if($led0stopold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($led0stopold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($led0stopold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($led0stopold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($led0stopold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($led0stopold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($led0stopold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($led0stopold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($led0stopold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($led0stopold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($led0stopold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($led0stopold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($led0stopold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($led0stopold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group">
							<div class="form-row">
								<div class="col">
									Ladung freigegeben
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ledsofort" class="col-md-4 col-form-label">Sofort Laden Modus</label>
								<div class="col">
									<select name="ledsofort" id="ledsofort" class="form-control">
										<option <?php if($ledsofortold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($ledsofortold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($ledsofortold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($ledsofortold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($ledsofortold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($ledsofortold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($ledsofortold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($ledsofortold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($ledsofortold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($ledsofortold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($ledsofortold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($ledsofortold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($ledsofortold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($ledsofortold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="lednurpv" class="col-md-4 col-form-label">Nur PV Laden Modus</label>
								<div class="col">
									<select name="lednurpv" id="lednurpv" class="form-control">
										<option <?php if($lednurpvold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($lednurpvold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($lednurpvold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($lednurpvold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($lednurpvold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($lednurpvold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($lednurpvold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($lednurpvold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($lednurpvold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($lednurpvold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($lednurpvold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($lednurpvold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($lednurpvold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($lednurpvold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ledminpv" class="col-md-4 col-form-label">Min + PV Laden Modus</label>
								<div class="col">
									<select name="ledminpv" id="ledminpv" class="form-control">
										<option <?php if($ledminpvold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($ledminpvold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($ledminpvold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($ledminpvold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($ledminpvold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($ledminpvold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($ledminpvold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($ledminpvold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($ledminpvold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($ledminpvold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($ledminpvold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($ledminpvold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($ledminpvold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($ledminpvold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ledstandby" class="col-md-4 col-form-label">Standby Modus</label>
								<div class="col">
									<select name="ledstandby" id="ledstandby" class="form-control">
										<option <?php if($ledstandbyold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($ledstandbyold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($ledstandbyold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($ledstandbyold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($ledstandbyold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($ledstandbyold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($ledstandbyold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($ledstandbyold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($ledstandbyold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($ledstandbyold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($ledstandbyold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($ledstandbyold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($ledstandbyold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($ledstandbyold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="ledstop" class="col-md-4 col-form-label">Stop Modus</label>
								<div class="col">
									<select name="ledstop" id="ledstop" class="form-control">
										<option <?php if($ledstopold == "aus") echo "selected" ?> value="aus">Alle LEDs aus</option>
										<option <?php if($ledstopold == "an") echo "selected" ?> value="an">Alle LEDs an</option>
										<option <?php if($ledstopold == "an1") echo "selected" ?> value="an1">LED 1 an</option>
										<option <?php if($ledstopold == "an2") echo "selected" ?> value="an2">LED 2 an</option>
										<option <?php if($ledstopold == "an3") echo "selected" ?> value="an3">LED 3 an</option>
										<option <?php if($ledstopold == "an12") echo "selected" ?> value="an12">LED 1 & 2 an</option>
										<option <?php if($ledstopold == "an13") echo "selected" ?> value="an13">LED 1 & 3 an</option>
										<option <?php if($ledstopold == "an23") echo "selected" ?> value="an23">LED 2 & 3 an</option>
										<option <?php if($ledstopold == "blink1") echo "selected" ?> value="blink1">LED 1 blinkend</option>
										<option <?php if($ledstopold == "blink2") echo "selected" ?> value="blink2">LED 2 blinkend</option>
										<option <?php if($ledstopold == "blink3") echo "selected" ?> value="blink3">LED 3 blinkend</option>
										<option <?php if($ledstopold == "blink12") echo "selected" ?> value="blink12">LED 1 & 2 blinkend</option>
										<option <?php if($ledstopold == "blink13") echo "selected" ?> value="blink13">LED 1 & 3 blinkend</option>
										<option <?php if($ledstopold == "blink23") echo "selected" ?> value="blink23">LED 2 & 3 blinkend</option>
									</select>
								</div>
							</div>
						</div>
					</div>
					<script>
						function visibility_ledsakt() {
							if($('#ledsaktOff').prop("checked")) {
								hideSection('#ledsan');
							} else {
								showSection('#ledsan');
							}
						}

						$(document).ready(function(){
							$('input[type=radio][name=ledsakt]').change(function(){
								visibility_ledsakt();
							});

							visibility_ledsakt();
						});
					</script>
				</div>

				<!-- Display intern/extern -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Display (intern oder extern)
					</div>
					<div class="card-body">
						<div class="form-group mb-0">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">integriertes Display</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($displayaktivold == 0) echo " active" ?>">
											<input type="radio" name="displayaktiv" id="displayaktivOff" value="0"<?php if($displayaktivold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($displayaktivold == 1) echo " active" ?>">
											<input type="radio" name="displayaktiv" id="displayaktivOn" value="1"<?php if($displayaktivold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
						</div>
						<div class="hide" id="displayan">
							<div class="form-group">
								<div class="form-row mb-1">
									<div class="col">
										Display Standby
									</div>
								</div>
								<div class="form-row vaRow mb-1">
									<label for="displaysleep" class="col-md-4 col-form-label">ausschalten nach x Sekunden</label>
									<div class="col">
										<input type="number" min="5" step="5" name="displaysleep" id="displaysleep" class="form-control" value="<?php echo $displaysleepold ?>">
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">beim Einstecken des Fahrzeugs einschalten</label>
									</div>
									<div class="col">
										<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($displayEinBeimAnsteckenold == 0) echo " active" ?>">
												<input type="radio" name="displayEinBeimAnstecken" id="displayEinBeimAnsteckenOff" value="0"<?php if($displayEinBeimAnsteckenold == 0) echo " checked=\"checked\"" ?>>Nein
											</label>
											<label class="btn btn-outline-info<?php if($displayEinBeimAnsteckenold == 1) echo " active" ?>">
												<input type="radio" name="displayEinBeimAnstecken" id="displayEinBeimAnsteckenOn" value="1"<?php if($displayEinBeimAnsteckenold == 1) echo " checked=\"checked\"" ?>>Ja
											</label>
										</div>
									</div>
								</div>
							</div>
						</div>
						<hr class="border-secondary">
						<div class="form-group <?php if($ssdisplayold == 1 && $isssold == 1) echo "hide" ?>">
							<div class="form-row vaRow mb-1">
								<label for="displaytheme" class="col-md-4 col-form-label">Theme des Displays</label>
								<div class="col">
									<select name="displaytheme" id="displaytheme" class="form-control" >
										<?php if($isssold == 0) { ?>
											<option <?php if($displaythemeold == 0) echo "selected" ?> value="0">Cards</option>
											<option <?php if($displaythemeold == 3) echo "selected" ?> value="3">Gauges</option>
											<option <?php if($displaythemeold == 1) echo "selected" ?> value="1">Symbolfluss</option>
											<option <?php if($displaythemeold == 5) echo "selected" ?> value="5">Colors</option>
										<?php } ?>
										<option <?php if($displaythemeold == 2 || $isssold == 1) echo "selected" ?> value="2">Nur Ladeleistung, keine Verstellmöglichkeit</option>
									</select>
								</div>
							</div>
							<div id="displaygauge" class="hide">
								<div class="form-row vaRow mb-1">
									<label for="displayevumax" class="col-md-4 col-form-label">EVU Skala Min Max</label>
									<div class="col">
										<input type="number" min="5000" step="100" name="displayevumax" id="displayevumax" class="form-control" value="<?php echo $displayevumaxold ?>">
									</div>
								</div>
								<div class="form-row vaRow mb-1">
									<label for="displaypvmax" class="col-md-4 col-form-label">PV Skala Max</label>
									<div class="col">
										<input type="number" min="1000" step="100" name="displaypvmax" id="displaypvmax" class="form-control" value="<?php echo $displaypvmaxold ?>">
									</div>
								</div>
								<div class="form-row vaRow mb-1">
									<label for="displayspeichermax" class="col-md-4 col-form-label">Speicher Skala Min Max</label>
									<div class="col">
										<input type="number" min="1000" step="100" name="displayspeichermax" id="displayspeichermax" class="form-control" value="<?php echo $displayspeichermaxold ?>">
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										<label class="col-form-label">Hausverbrauch anzeigen</label>
									</div>
									<div class="col">
										<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($displayhausanzeigenold == 0) echo " active" ?>">
												<input type="radio" name="displayhausanzeigen" id="displayhausanzeigenOff" value="0"<?php if($displayhausanzeigenold == 0) echo " checked=\"checked\"" ?>>Nein
											</label>
											<label class="btn btn-outline-info<?php if($displayhausanzeigenold == 1) echo " active" ?>">
												<input type="radio" name="displayhausanzeigen" id="displayhausanzeigenOn" value="1"<?php if($displayhausanzeigenold == 1) echo " checked=\"checked\"" ?>>Ja
											</label>
										</div>
									</div>
								</div>
								<div class="form-row vaRow mb-1">
									<label for="displayhausmax" class="col-md-4 col-form-label">Hausverbrauch Skala Max</label>
									<div class="col">
										<input type="number" min="1000" step="100" name="displayhausmax" id="displayhausmax" class="form-control" value="<?php echo $displayhausmaxold ?>">
									</div>
								</div>
							</div>
							<?php for( $chargepoint = 1; $chargepoint < 9; $chargepoint++ ){ // begin chargepoint loop ?>
								<div id=displaylp<?php echo $chargepoint; ?> class="hide">
									<div class="form-row vaRow mb-1">
										<label for="displaylp<?php echo $chargepoint; ?>max" class="col-md-4 col-form-label">Ladepunkt <?php echo $chargepoint; ?> Skala Max</label>
										<div class="col">
											<input type="number" min="1000" step="100" name="displaylp<?php echo $chargepoint; ?>max" id="displaylp<?php echo $chargepoint; ?>max" class="form-control" value="<?php echo ${'displaylp' . $chargepoint . 'maxold'} ?>">
										</div>
									</div>
								</div>
							<?php } // end chargepoint loop ?>
							<hr class="border-secondary">
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col">
									PIN-Sperre
								</div>
							</div>
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Display mit PIN schützen</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($displaypinaktivold == 0) echo " active" ?>">
											<input type="radio" name="displaypinaktiv" id="displaypinaktivOff" value="0"<?php if($displaypinaktivold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($displaypinaktivold == 1) echo " active" ?>">
											<input type="radio" name="displaypinaktiv" id="displaypinaktivOn" value="1"<?php if($displaypinaktivold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div class="form-row mb-1 hide" id="displaypin">
								<label for="displaypincode" class="col-md-4 col-form-label">PIN (4 Stellen, nur Zahlen erlaubt)</label>
								<div class="col">
									<input type="text" pattern="[0-9]{4}" minlength="4" maxlength="4" size="4" name="displaypincode" id="displaypincode" class="form-control" value="<?php echo $displaypincodeold ?>">
								</div>
							</div>
						</div>
					</div>
					<script>
						function visibility_displayaktiv() {
							if($('#displayaktivOff').prop("checked")) {
								hideSection('#displayan');
							} else {
								showSection('#displayan');
								visibility_displaypinaktiv();
								visibility_displaytheme()
							}
						}

						function visibility_displaypinaktiv() {
							if($('#displaypinaktivOff').prop("checked")) {
								hideSection('#displaypin');
							} else {
								showSection('#displaypin');
							}
						}

						function visibility_displaytheme() {
							switch ($('#displaytheme').val()) {
								case '0': // Cards
									showSection('#displaygauge');
									for (let cp = 1; cp < 9; cp++) {
										showSection('#displaylp' + cp);
									}
									break;
								case '2': // Minimal
									hideSection('#displaygauge');
									for (let cp = 1; cp < 3; cp++) {
										showSection('#displaylp' + cp);
									}
									for (let cp = 3; cp < 9; cp++) {
										hideSection('#displaylp' + cp);
									}
									break;
								case '3': // Gauges
									showSection('#displaygauge');
									for (let cp = 1; cp < 3; cp++) {
										showSection('#displaylp' + cp);
									}
									for (let cp = 3; cp < 9; cp++) {
										hideSection('#displaylp' + cp);
									}
									break;
								default:
									hideSection('#displaygauge');
									for (let cp = 1; cp < 9; cp++) {
										hideSection('#displaylp' + cp);
									}
							}
						}

						$(document).ready(function(){
							$('input[type=radio][name=displayaktiv]').change(function(){
								visibility_displayaktiv();
							});

							$('input[type=radio][name=displaypinaktiv]').change(function(){
								visibility_displaypinaktiv();
							});

							$('#displaytheme').change(function(){
								visibility_displaytheme();
							});

							visibility_displayaktiv();
						});
					</script>
				</div>

				<!-- Web-Theme Optionen -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Web-Theme Optionen
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Hausverbrauch auf der Hauptseite anzeigen</label>
								</div>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($hausverbrauchstatold == 0) echo " active" ?>">
										<input type="radio" name="hausverbrauchstat" id="hausverbrauchstatOff" value="0"<?php if($hausverbrauchstatold == 0) echo " checked=\"checked\"" ?>>Nein
									</label>
									<label class="btn btn-outline-info<?php if($hausverbrauchstatold == 1) echo " active" ?>">
										<input type="radio" name="hausverbrauchstat" id="hausverbrauchstatOn" value="1"<?php if($hausverbrauchstatold == 1) echo " checked=\"checked\"" ?>>Ja
									</label>
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Heute geladen auf der Hauptseite anzeigen</label>
								</div>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($heutegeladenold == 0) echo " active" ?>">
										<input type="radio" name="heutegeladen" id="heutegeladenOff" value="0"<?php if($heutegeladenold == 0) echo " checked=\"checked\"" ?>>Nein
									</label>
									<label class="btn btn-outline-info<?php if($heutegeladenold == 1) echo " active" ?>">
										<input type="radio" name="heutegeladen" id="heutegeladenOn" value="1"<?php if($heutegeladenold == 1) echo " checked=\"checked\"" ?>>Ja
									</label>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="livegraph" class="col-md-4 col-form-label">Zeitintervall für den Live Graphen der Hauptseite</label>
								<div class="col-md-8">
									<div class="form-row vaRow mb-1">
										<label for="livegraph" class="col-2 col-form-label valueLabel" suffix="Min"><?php echo $livegraphold; ?> Min</label>
										<div class="col-10">
											<input type="range" class="form-control-range rangeInput" name="livegraph" id="livegraph" min="10" max="120" step="10" value="<?php echo $livegraphold; ?>">
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<!-- Ladelog Optionen -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Ladelog
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="preisjekwh" class="col-md-4 col-form-label">Preis je kWh</label>
								<div class="col">
									<input class="form-control" type="number" min="0" step="0.0001" name="preisjekwh" id="preisjekwh" value="<?php echo $preisjekwhold ?>">
									<span class="form-text small">Gültige Werte xx.xx, z.B. 0.2833. Dient zur Berechnung der Ladekosten im Ladelog.</span>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="form-row text-center">
					<div class="col">
						<button id="saveSettingsBtn" type="submit" class="btn btn-success">Speichern</button>
					</div>
				</div>
			</form>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Verschiedenes</small>
			</div>
		</footer>

		<script>
			$('.rangeInput').on('input', function() {
				// show slider value in label of class valueLabel
				updateLabel($(this).attr('id'));
			});

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navVerschiedenes').addClass('disabled');
				}
			);
		</script>

	</body>
</html>
