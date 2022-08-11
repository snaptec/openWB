<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
	error_log('Diese Seite muss als HTTP-POST aufgerufen werden.');
	exit('Diese Seite muss als HTTP-POST aufgerufen werden.');
}
exec("sudo -u pi /var/www/html/openWB/runs/update.sh > /dev/null &");
