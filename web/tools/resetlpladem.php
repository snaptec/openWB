<?php
if($_POST['action'] == 'resetlp1') {
	file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/gelrlp1', 0);
	file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/aktgeladen', 0);
}
if($_POST['action'] == 'resetlp2') {
	file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/gelrlp2', 0);
	file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/aktgeladens1', 0);
}
if($_POST['action'] == 'resetlp3') {
	file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/gelrlp3', 0);
	file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/aktgeladens2', 0);
}
?>
