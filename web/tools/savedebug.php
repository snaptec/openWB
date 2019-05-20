<?php
$result = '';


if (filter_var($_POST[debugemail], FILTER_VALIDATE_EMAIL)) {
$result = $_POST[debuguser] . "\n" . $_POST[debugemail] . "\n";
file_put_contents('/var/www/html/openWB/ramdisk/debuguser', $result);
header("Location: ./debugredirect.html");
} else {
	echo " Keine gültige Email angegeben!<br>Weiterleitung in 5 Sekunden...<br>";
	header ("Refresh: 5; ../index.php");
}	
?>



