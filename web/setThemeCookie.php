<?php
	$themeCookie = $_GET['theme'];
	$expire = time()+(60*60*24*365*2);  // expiring-date to now + 2 years
	setcookie('openWBTheme', $themeCookie, $expire, '/openWB/');
?>
