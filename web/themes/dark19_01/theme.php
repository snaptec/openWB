<?php
				setcookie('openWBTheme', 'dark', time()+(60*60*24*365*2));
				$_COOKIE['openWBTheme'] = 'dark';
				$themeCookie = 'dark';
		// redirect da cookie neu gesetzt
		header( "refresh:5;url=../../index.php" );
?>
<!DOCTYPE html>
<html lang="de">
	<head>
	</head>
	<body>
		<h4 style="text-align:center;">Theme umbenannt</h4>
		<p style="text-align:center;">
			Weiterleitung erfolgt automatisch
		</p>
	</body>
</html>
