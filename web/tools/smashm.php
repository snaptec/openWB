<?php

	echo "Installation SMA SHM Komponente wird durchgeführt, bitte nicht vom Strom trennen";
	exec("/var/www/html/openWB/runs/smashm.sh");
?>
	<script type="text/javascript">
	    setTimeout(function() { window.location = "../index.php"; }, 20000);
	</script>

