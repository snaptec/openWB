<?php
$result = '';

if (filter_var($_POST[emailAddress], FILTER_VALIDATE_EMAIL)) {
$result = $_POST[debugMessage] . "\n" . $_POST[emailAddress] . "\n";
file_put_contents('/var/www/html/openWB/ramdisk/debuguser', $result);
header("Location: ./debugredirect.html");
} else {
	echo " <h1>Keine gültige Email angegeben!</h1><br>Weiterleitung in 10 Sekunden...<br>";
	header ("Refresh: 10; ../index.php");
}
?>
