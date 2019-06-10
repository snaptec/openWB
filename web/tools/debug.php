<?php

	echo "Debugdaten werden gesammelt. Dieser Vorgang dauert etwa eine Minute. Die Daten werden automatisch verschickt. Automatische Weiterleitung nach dem Verschicken.";
	exec("/var/www/html/openWB/runs/senddebuginit.sh");
?>
	<script type="text/javascript">
	    setTimeout(function() { window.location = "../index.php"; }, 500);
	</script>

