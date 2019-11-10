<html>
	<head>
		<meta http-equiv="refresh" content="240;url=../index.php" />
	</head>
<?php
	echo "Update wird durchgeführt, bitte nicht vom Strom trennen";
	exec("/var/www/html/openWB/runs/update.sh > /dev/null &");
	header( "refresh:240;url=../index.php" );
?>
<script type="text/javascript">
   setTimeout(function() { window.location.href = "../index.php"; }, 240000);
</script>
</html>
