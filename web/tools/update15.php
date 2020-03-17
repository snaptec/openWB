<!DOCTYPE html>
<html lang="de">
	<head>
		<meta http-equiv="refresh" content="30;url=../index.php" />
	</head>
	<body>
		<p>Update wird durchgeführt, bitte nicht vom Strom trennen.</p>
<?php
exec("/var/www/html/openWB/runs/update15.sh > /dev/null &");
?>
		<script>
			setTimeout(function() { window.location.href = "../index.php"; }, 30000);
		</script>
	</body>
</html>
