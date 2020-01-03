<html>
	<head>
		<meta http-equiv="refresh" content="30;url=../index.php" />
	</head>
<?php
	echo "Update wird durchgeführt, bitte nicht vom Strom trennen";
	exec("/var/www/html/openWB/runs/update15.sh > /dev/null &");
	header( "refresh:30;url=../index.php" );
?>
<script type="text/javascript">
   setTimeout(function() { window.location.href = "../index.php"; }, 30000);
</script>
</html>
