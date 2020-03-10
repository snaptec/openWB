<?php
if($_POST['action'] == 'resetlp1') {
	file_put_contents('/var/www/html/openWB/ramdisk/gelrlp1', 0);
	file_put_contents('/var/www/html/openWB/ramdisk/aktgeladen', 0);
}
if($_POST['action'] == 'resetlp2') {
	file_put_contents('/var/www/html/openWB/ramdisk/gelrlp2', 0);
	file_put_contents('/var/www/html/openWB/ramdisk/aktgeladens1', 0);
}
if($_POST['action'] == 'resetlp3') {
	file_put_contents('/var/www/html/openWB/ramdisk/gelrlp3', 0);
	file_put_contents('/var/www/html/openWB/ramdisk/aktgeladens2', 0);
}
?>
