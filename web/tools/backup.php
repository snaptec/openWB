
<html>
<p> Backup erfoglreich erstellt....</p>
<?php 
   exec("tar --exclude='/var/www/html/openWB/web/backup' --exclude='/var/www/html/openWB/.git' -czf /var/www/html/openWB/web/backup/backup.tar.gz /var/www/html/");
?><br> <a href="/openWB/web/backup/backup.tar.gz"> Download</a>
<br><br>
<a href="../index.php">Zurück</a>

</html>
