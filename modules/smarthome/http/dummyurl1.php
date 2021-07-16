<?php
$url = $_SERVER['REQUEST_URI'];
$command = escapeshellcmd("sudo /bin/bash /var/www/html/openWB/modules/smarthome/http/dummyurl1.sh $url");
$output = shell_exec($command);
echo $output;
?>
