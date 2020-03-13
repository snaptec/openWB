<?php
if(isset($_POST["evselp1"])) {
	file_put_contents('/var/www/html/openWB/ramdisk/progevsedinlp1', 1);
	file_put_contents('/var/www/html/openWB/ramdisk/progevsedinlp12000', $_POST['lp12000']);
	file_put_contents('/var/www/html/openWB/ramdisk/progevsedinlp12007', $_POST['lp12007']);
}
if(isset($_POST["evselp2"])) {
	file_put_contents('/var/www/html/openWB/ramdisk/progevsedinlp2', 1);
	file_put_contents('/var/www/html/openWB/ramdisk/progevsedinlp22000', $_POST['lp22000']);
	file_put_contents('/var/www/html/openWB/ramdisk/progevsedinlp22007', $_POST['lp22007']);
}
header("Location: ../index.php");
?>
