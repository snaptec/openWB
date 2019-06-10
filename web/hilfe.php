<!DOCTYPE html>
<html lang="en">

<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB Help</title>
	<meta name="description" content="Control your charge" />
	<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
	<meta name="author" content="Kevin Wieland" />
	<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
	<link rel="icon" type="image/png" href="img/favicons/favicon-32x32.png" sizes="32x32">
	<link rel="icon" type="image/png" href="img/favicons/favicon-16x16.png" sizes="16x16">
	<link rel="manifest" href="manifest.json">
	<link rel="shortcut icon" href="img/favicons/favicon.ico">
	<meta name="msapplication-TileColor" content="#00a8ff">
	<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">
	<link rel="stylesheet" type="text/css" href="css/normalize.css">
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="css/owl.css">
	<link rel="stylesheet" type="text/css" href="css/animate.css">
	<!-- Font Awesome, all styles -->
  <link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
	<link rel="stylesheet" type="text/css" href="css/cardio.css">
</head>

 <script type="text/javascript">
         function ShowContent(content) {
         	document.getElementById("bedienung").style.display = 'none'
         	document.getElementById("ladeeinstellung").style.display = 'none';
         	document.getElementById("misc").style.display = 'none';
         	document.getElementById(content).style.display = 'block';
	 }
</script>
<div class="container">

<div class="row"><br>
 <ul class="nav nav-tabs">
    <li><a data-toggle="tab" href="./index.php">Zurück</a></li>
    <li><a id="lnkbedienung" href="#" onclick="return ShowContent('bedienung');" >Bedienung</a></li>
    <li><a id="lnkladeeinstellung" href="#" onclick="return ShowContent('ladeeinstellung');" >Ladeeinstellungen</a></li>
    <li><a id="lnkmisc" href="#" onclick="return ShowContent('misc');" >Misc</a></li>
  </ul><br><br>
 </div>

 <div id="bedienung" style="display:block">
	 <h3>Bedienung</h3>
		 <p> Lademodus</p><br>
			 Der Unterschied zwischen "Standby" und "Stop" ist, dass bei "Stop" keine Ladung erlaubt ist.<br>
		 Im Semistop Modus kann die Ladung durch Nachtladen und Zielladen aktiviert werden<br>
		 <hr>

	<br>
	 Etwas unklar in der Bedienung?<br>
	 Passende Erklärung parat?<br>
	 <br> Mithilfe erwünscht. Fragen oder Hilfetexte bitte im <a href="https://openwb.de/forum/">Forum</a> posten oder an info@snaptec.de

 </div>

 <div id="ladeeinstellung" style="display:none">
	 	 <h3>Ladeeinstellung</h3>


		 <p>Meldung "Lastmanagement aktiv, Ladeleistung reduziert"</p>
		<br> Wurde innerhalb der letzten 2 Minuten das Lastmanagement aktiv wird diese Meldung auf der Hauptseite unterhalb des Graphen angezeigt.<br>
		Sie dient rein der Information das das Lastmanagement von OpenWB aktiv ist und die gewünschte bzw. eingestellte Ladeleistung derzeit nicht möglich ist.<br>
		Es besteht kein Handlungsbedarf. Wenn mehr Leistung zur Verfügung steht regelt OpenWB automatisch auf den gewünschten Wert hoch.<br>
		<br><br><br>

		 Etwas unklar bei den Ladeeinstellungen?<br>
	 Passende Erklärung parat?<br>
	<br> Mithilfe erwünscht. Fragen oder Hilfetexte bitte im <a href="https://openwb.de/forum/">Forum</a> posten oder an info@snaptec.de

</div>


 <div id="misc" style="display:none">

 	 	 <h3>Misc</h3>
		 <p> EVSE Modbus Test zu finden unter Status.<br></p>
		 Der Test dient zur Hilfe bei der Erstkonfiguration.<br>Er prüft die korrekte Kommunikation zur EVSE.<br> Bei Verwendung eines Modbus/LanKonverters baut der Test zunächst die dafür benötigte Verbindung auf.<br>
		 Nutzung:<br><br>
		 Vor Test den Lademodus auf der Hauptseite auf Stop stellen.<br>
		 Für den gewünschten Ladepunkt auf Testen klicken<br>
		 <br>Die Seite lädt nun neu und man erhält nach 3-10 Sekunden automatisch eine Ergebnis:<br>
		 <br> erfolgreich = Kommunikation funktioniert
		 <br> Fehler = Kommunikation mit der EVSE nicht möglich. Korrekte Konfiguration bzw. Verkabelung prüfen
		 <br> Platzhalter konfiguriert = es ist an diesem Ladepunkt keine Modbus EVSE konfiguriert
		 <hr>

	 Sonstige Hilfe die hier stehen sollte?<br>
	 Passende Erklärung parat?<br>
	<br> Mithilfe erwünscht. Fragen oder Hilfetexte bitte im <a href="https://openwb.de/forum/">Forum</a> posten oder an info@snaptec.de





 </div>



</div>
</html>
