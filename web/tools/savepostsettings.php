<!DOCTYPE html>
<html lang="de">
	<body>
		<p>Einstellungen werden gespeichert...</p>
		<?php
		// get settings
		include $_SERVER['DOCUMENT_ROOT'].'/openWB/web/tools/settingsClass.php';
		$mySettings = new openWBSettings();
		$mySettings->setSettings($_POST);
		$mySettings->saveConfigFile();
		?>
		<!-- return to theme -->
		<p>Fertig! Sie werden nun zur Hauptseite weitergeleitet.<br>
		Sollte die Weiterleitung nicht funktionieren, nutzen Sie <a href="../index.php">diesen Link</a>.</p>
		<script>window.location.href='../index.php';</script>
	</body>
</html>
