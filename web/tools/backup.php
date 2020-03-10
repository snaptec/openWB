<!DOCTYPE html>
<html lang="de">
	<head>
		<title>Backup</title>
	</head>
	<body>
		<p> Backup erfoglreich erstellt....</p>
		<?php 
			exec("tar --exclude='".$_SERVER['DOCUMENT_ROOT']."/openWB/web/backup' --exclude='".$_SERVER['DOCUMENT_ROOT']."/openWB/.git' -czf ".$_SERVER['DOCUMENT_ROOT']."/openWB/web/backup/backup.tar.gz ".$_SERVER['DOCUMENT_ROOT']."/");
		?>
		<p>
			<a href="/openWB/web/backup/backup.tar.gz"> Download</a><br>
			<a href="../index.php">Zurück</a>
		</p>
	</body>
</html>
