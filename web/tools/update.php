
	<script type="text/javascript">
	    setTimeout(function() { window.location = "../index.php"; }, 10000);
	</script>
<?php

	echo "Update wird durchgeführt, bitte nicht vom Strom trennen";
	exec("/var/www/html/openWB/runs/update.sh &");
?>
