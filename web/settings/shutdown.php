<?php
$cmd="/var/www/html/openWB/runs/shutdown.sh &";
//$cmd="touch /tmp/firsttouch";
$outputfile="/tmp/out.log";
$pidfile="/tmp/shutdown.pid";
exec(sprintf("%s > %s 2>&1 & echo $! >> %s", $cmd, $outputfile, $pidfile));
return 1;
?>
