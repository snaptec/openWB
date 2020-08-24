<?php
$url = $_SERVER['REQUEST_URI'];
echo "url $url" ;
$command = escapeshellcmd("sudo /bin/bash /var/www/html/openWB/web/tools/trace/modtrace.sh $url"); 
$output = shell_exec($command); 
echo $output;
?>