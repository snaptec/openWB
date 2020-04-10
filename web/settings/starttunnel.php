<?php
$result = '';

if (isset($_POST['token'])) {
	$result = $_POST['token'] . "\n";
	file_put_contents('/var/www/html/openWB/ramdisk/remotetoken', $result);
	header("Location: ./remoteredirect.html");
} else {
	header ("Refresh: 10; ../index.php");
	?>
<!DOCTYPE html>
<html lang="de">
	<head>
		<title>Weiterleitung</title>
	</head>
	<body>
		<h1>Keine Token angegeben!</h1>
		<p>Weiterleitung in 10 Sekunden...</p>
	</body>
</html>
	<?php
}
?>
