<?php
	$gauge_to_scale = $_GET['name'];
	$max_value = $_GET['value'];
	setcookie($gauge_to_scale, $max_value, time()+(60*60*24*365*2));
?>
