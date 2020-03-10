<?php
file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/wssid',$_POST['ssid']);
file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/wpassword',$_POST['passwort']);

exec('sudo /bin/bash '.$_SERVER['DOCUMENT_ROOT'].'/openWB/runs/wlanconnect.sh');
?>
