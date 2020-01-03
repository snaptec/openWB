
	<script type="text/javascript">
	    setTimeout(function() { window.location = "../index.php"; }, 60000);
	</script>
<?php

	echo "Bitte eine Minute warten";
	exec("/var/www/html/openWB/runs/reboot.sh");
?>
