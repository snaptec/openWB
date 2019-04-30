<?php
$daydate1 = $_GET[thedate];
$daydate = date("Ymd", strtotime($daydate1));
$llgfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-llg.csv';
$llg = file($llgfile, FILE_IGNORE_NEW_LINES);

$firstev = reset($llg);
$lastev = end($llg);
$dailyevg = number_format((($lastev - $firstev) / 1000), 2);
print($dailyevg);
?>


