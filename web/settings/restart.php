<?php
$cmd="/var/www/html/openWB/runs/reboot.sh &";
$outputfile="/tmp/out.log";
$pidfile="/tmp/reboot.pid";
exec(sprintf("%s > %s 2>&1 & echo $! >> %s", $cmd, $outputfile, $pidfile));
return 1;
?>
