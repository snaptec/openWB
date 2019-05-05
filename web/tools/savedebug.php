<?php
$result = '';
$result = $_POST[debuguser] . "\n" . $_POST[debugemail];
file_put_contents('/var/www/html/openWB/ramdisk/debuguser', $result);






header("Location: ./debugredirect.html");
?>



