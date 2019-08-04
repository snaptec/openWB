<html>


<?php

	echo "Update wird durchgeführt, bitte nicht vom Strom trennen";
	exec("/var/www/html/openWB/runs/update.sh &");
?>
	<head>
		<meta http-equiv="refresh" content="1;url=../index.php" />
	</head>
</html>
