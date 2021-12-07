<!-- Erste Schritte >>> -->
<h3>Bedienung</h3>
<h4>Lademodus</h4>
<p>
	Der Lademodus bestimmt das Ladeverhalten der Wallbox und kann weiter konfiguriert werden.
</p>
<h5>Sofort</h5>
<p>
	Die Box beginnt sofort zu laden. Der Ladestrom kann vorgegeben werden, ebenso kann ein Ladelimit definiert werden. Beim Erreichen eines konfigurierten Ladelimits wird die Ladung beendet. Mögliche Ladelimits:<br>
</p>
<ul>
	<li>Ladezustand (SoC) des Fahrzeugs. Dies erfordert dass ein SoC Modul in den Einstellungen des Ladepunkts konfiguriert ist.</li>
	<li>Zugeführte Energiemenge (kWh). Eignet sich z.B. falls kein SoC Modul vorhanden ist.</li>
</ul>
<h5>PV Laden</h5>
<p>
	Geladen wird bei ausreichendem PV Überschuss. Der Ladestrom wird automatisch angepasst um den vorhandenen PV Überschuss bestmöglich zu nutzen.
	Die Ladung startet automatisch beim Erreichen der Einschaltschwelle für die Einspeisung und stoppt beim Erreichen der Abschaltschwelle oder beim Erreichen eines konfigurierten maximalen SoC.
	Je nach Fahrzeug und installierter openWB Variante kann die CP-Unterbrechung genutzt werden um Fahrzeuge für den Ladebeginn aus dem Schlaf aufzuwecken.
</p>
<h5>Min+PV Laden</h5>
<p>
	Verhält sich wie PV Laden, jedoch wird sofort mit der konfigurierten Mindeststromstärke geladen. Die Einschalt- und Abschaltschwelle haben keine Wirkung.
	Eignet sich bei kleineren PV-Anlagen oder stark wechselnder Sonneneinstrahlung um häufige Ladeunterbrechungen zu vermeiden.
</p>
<h5>Standby</h5>
<p>
	Es findet keine Ladung statt, lediglich mögliche konfigurierte Nacht-, Morgen- und Zielladungen werden durchgeführt.
</p>
<h5>Stop</h5>
<p>
	Es findet keine Ladung statt, auch keine Nacht-, Morgen- und Zielladungen.
</p>
<hr>
<h4>Ladeeinstellung</h4>
<h5>Meldung "Lastmanagement aktiv, Ladeleistung reduziert"</h5>
<p>
	Wurde innerhalb der letzten zwei Minuten das Lastmanagement aktiv, wird diese Meldung auf der Hauptseite unterhalb des Graphen angezeigt.<br>
	Sie informiert darüber, dass das Lastmanagement von openWB aktiv ist und die gewünschte bzw. eingestellte Ladeleistung derzeit nicht möglich ist.<br>
	Es besteht kein Handlungsbedarf. Wenn mehr Leistung zur Verfügung steht, regelt openWB automatisch auf den gewünschten Wert hoch.
</p>
<hr>
<h4>Ladepunktsteuerung</h4>
<p>
	Ein grüner Ladepunkt zeigt an, dass dieser grundsätzlich freigeschaltet ist. Je nach Lademodus ist eine Ladung möglich oder auch nicht.<br>
	Ein roter durchgestrichener Ladepunkt zeigt einen deaktivierten Ladepunkt an. Durch Anklicken ist der Ladepunkt manuell (de-)aktivierbar.<br>
</p>
<hr>
<h4>Interface erklärt</h4>
<p>
	Was bedeuten die Zahlen in den Klammern?<br>
	Die Zahlen in den Klammern stellen die jeweiligen Tageserträge bzw. Verbräuche dar.<br>
	Bei Netz und Speicher steht das I für Import = bezogen und das E für Export = eingespeiste Energie.<br>
</p>
<!-- <<< Erste Schritte -->
