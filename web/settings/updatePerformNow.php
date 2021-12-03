<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
	exit('Diese Seite muss als HTTP-POST aufgerufen werden.');
}
exec("/var/www/html/openWB/runs/update.sh > /dev/null &");
?>
