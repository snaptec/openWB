<!DOCTYPE html>
<html lang="de">
	<head>
		<title>Backup</title>
	</head>
	<body>
		<p> Backup erfoglreich erstellt....</p>
		<?php 
			exec("tar --exclude='/var/www/html/openWB/web/backup' --exclude='/var/www/html/openWB/.git' -czf /var/www/html/openWB/web/backup/backup.tar.gz /var/www/html/");
		?>
		<p>
			<a href="/openWB/web/backup/backup.tar.gz"> Download</a><br>
			<a href="../index.php">Zurück</a>
		</p>
	</body>
</html>
