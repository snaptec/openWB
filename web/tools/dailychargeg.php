<?php
$daydate1 = $_GET['thedate'];
$daydate = date("Ymd", strtotime($daydate1));
$csv = array_map('str_getcsv', file('/var/www/html/openWB/web/logging/data/daily/'.$daydate.'.csv'));
$firstev = $csv[0][7];
$lastev = end($csv)[7];
$dailyevg = number_format((($lastev - $firstev) / 1000), 2);
print($dailyevg);
?>
