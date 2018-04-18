<?php
$target_dir = "upload/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
if ($_FILES["fileToUpload"]["size"] > 50000000) {
	echo "Sorry, your file is too large.";
	$uploadOk = 0;
}
if ($uploadOk == 0) {
	echo "Sorry, your file was not uploaded.";
} else {
	if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
		echo "Wiederherstellung wird durchgefuehrt, bitte warten!";
	} else {
		echo "Sorry, there was an error uploading your file.";
	}
}
sleep(5);
exec("/var/www/html/openWB/runs/restore.sh >> /var/www/html/openWB/web/tools/upload/restore.log");

?>
	<script type="text/javascript">
	    setTimeout(function() { window.location = "../index.php"; }, 15000);
	</script>
