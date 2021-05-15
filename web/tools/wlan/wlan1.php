<?php

file_put_contents('/var/www/html/openWB/ramdisk/wlanwssid',trim($_POST[wssid]));
file_put_contents('/var/www/html/openWB/ramdisk/wlanwpassword',trim($_POST[wpassword]));
echo "Gespeichert, verbinde mit Wlan...";
exec('sudo /bin/bash /var/www/html/openWB/web/tools/wlan/wlan1.sh');

 ?>
