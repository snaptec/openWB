<?php
file_put_contents('/var/www/html/openWB/ramdisk/wssid',$_POST['ssid']);
file_put_contents('/var/www/html/openWB/ramdisk/wpassword',$_POST['passwort']);

exec('sudo /bin/bash /var/www/html/openWB/runs/wlanconnect.sh');
?>
