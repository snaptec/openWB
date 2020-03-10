<?php
$result = '';

if (filter_var($_POST['emailAddress'], FILTER_VALIDATE_EMAIL)) {
	$result = $_POST['debugMessage'] . "\n" . $_POST['emailAddress'] . "\n";
	file_put_contents('/var/www/html/openWB/ramdisk/debuguser', $result);
	header("Location: ./debugredirect.html");
} else {
	header ("Refresh: 10; ../index.php");
	?>
<!DOCTYPE html>
<html lang="de">
	<head>
		<title>Weiterleitung</title>
	</head>
	<body>
		<h1>Keine gültige Email angegeben!</h1>
		<p>Weiterleitung in 10 Sekunden...</p>
	</body>
</html>
	<?php
}
?>
