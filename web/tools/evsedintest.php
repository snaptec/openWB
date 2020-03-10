<?php
if(isset($_POST["testlp1"])) {
	file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/evsedintestlp1', ausstehend);
}
if(isset($_POST["testlp2"])) {
	file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/evsedintestlp2', ausstehend);
}
if(isset($_POST["testlp3"])) {
	file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/evsedintestlp3', ausstehend);
}

header("Location: ../status/status.php");
?>
