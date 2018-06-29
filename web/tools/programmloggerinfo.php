<?php
define('checkaccess', TRUE);
include('./config_main.php');
include('./raspbian_ARM.php');

$uptime   = exec($UPTIME);
$cpuuse   = exec($CPUUSE);
$memtot   = exec($MEMTOT);
$memuse   = exec($MEMUSE);
$memfree  = exec($MEMFREE);
$diskuse  = exec($DISKUSE);
$diskfree = exec($DISKFREE);

$arr = array(
	    'uptime' => trim($uptime),
	        'cpuuse' => trim($cpuuse),
		    'memtot' => trim($memtot),
		        'memuse' => trim($memuse),
			    'memfree' => trim($memfree),
			        'diskuse' => trim($diskuse),
				    'diskfree' => trim($diskfree)
			    );

header("Content-type: text/json");
echo json_encode($arr);
?>
