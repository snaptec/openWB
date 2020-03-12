<!DOCTYPE html>
<html lang="de">
	<head>
		<title>Upload</title>
	</head>
	<body>
<?php
$target_dir = "upload/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
if ($_FILES["fileToUpload"]["size"] > 50000000) {
	echo "<p>Die Datei ist zu gro&szlig;.</p>";
	$uploadOk = 0;
}
if ($uploadOk == 0) {
	echo "<p>Die Datei konnte nicht hochgeladen werden.</p>";
} else {
	if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
		echo "<p>Wiederherstellung wird durchgefuehrt, bitte warten!</p>";
	} else {
		echo "<p>Es gab einen Fehler beim Hochladen der Datei.</p>";
	}
}
sleep(5);
exec("/var/www/html/openWB/runs/restore.sh >> /var/www/html/openWB/web/tools/upload/restore.log");
?>
		<script type="text/javascript">
			setTimeout(function() { window.location = "../index.php"; }, 15000);
		</script>
	</body>
</html>