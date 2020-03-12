<!DOCTYPE html>
<html lang="de">
	<head>
		<title>Debug</title>
	</head>
	<body>
		<p>
			Debugdaten werden gesammelt. Dieser Vorgang dauert etwa eine Minute.<br>
			Die Daten werden automatisch verschickt. Automatische Weiterleitung nach dem Verschicken.
		</p>
<?php
	exec("/var/www/html/openWB/runs/senddebuginit.sh");
?>
		<script>
			setTimeout(function() { window.location = "../index.php"; }, 500);
		</script>
	</body>
</html>
