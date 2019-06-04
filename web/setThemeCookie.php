<?php
 	$themeCookie = $_GET['theme'];
	setcookie('openWBTheme', $themeCookie, time()+(60*60*24*365*2));
?>
