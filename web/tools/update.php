<?php

	echo "Update wird durchgeführt, bitte nicht vom Strom trennen";
	exec("/var/www/html/openWB/runs/update.sh");
?>
	<script type="text/javascript">
	    setTimeout(function() { window.location = "../index.html"; }, 30000);
	</script>

