<!DOCTYPE html>
<html lang="de">
	<header>
		<title>SMA SHM Installation</title>
	</header>
	<body>
		<p>
			Installation SMA SHM Komponente wird durchgeführt, bitte nicht vom Strom trennen.
		</p>
<?php
exec("/var/www/html/openWB/runs/smashm.sh");
?>
		<script type="text/javascript">
			setTimeout(function() { window.location = "../index.php"; }, 20000);
		</script>
	</body>
</html>
