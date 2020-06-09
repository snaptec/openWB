<!DOCTYPE html>
<html lang="de">
	<head>
		<title>Remote Sitzung</title>
	</head>
	<body>
		<p>
			Remote Sitzung wird gestartet		</p>
<?php
	exec("/var/www/html/openWB/runs/initremote.sh");
?>
		<script>
			setTimeout(function() { window.location = "../index.php"; }, 500);
		</script>
	</body>
</html>
