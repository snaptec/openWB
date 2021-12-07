<?php
define('checkaccess', TRUE);
include('./config_main.php');
include('./raspbian_ARM.php');

$uptime = exec($UPTIME);
$systime = exec("date +%s");
$lastreboot = exec("cat /proc/stat | grep btime | awk '{print $2}'");
$cpuuse = exec($CPUUSE);
$cputemp = exec("cat /sys/class/thermal/thermal_zone0/temp");
$cpufreq = exec("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq");
$memtot = exec($MEMTOT);
$memuse = exec($MEMUSE);
$memfree = exec($MEMFREE);
$diskuse = exec($DISKUSE);
$diskfree = exec($DISKFREE);
$ethaddr = exec("ifconfig eth0 |grep 'inet ' |awk '{print $2}'");
$wlanaddr = exec("ifconfig wlan0 |grep 'inet ' |awk '{print $2}'");
$wlanqualy = exec("iwconfig wlan0 |grep 'Link'");
$wlanbitrate = exec("iwconfig wlan0 |grep 'Bit'");
$wlanrx = exec("iwconfig wlan0 |grep 'Rx'");
$wlantx = exec("iwconfig wlan0 |grep 'Tx'");
$wlanpower = exec("iwconfig wlan0 |grep 'Power'");
$wlanmode = exec("iwconfig wlan0 |grep 'Mode'");
$wlanssid = exec("iwconfig wlan0 |grep 'ESSID'|awk '{print $4}'");
$arr = array(
	'uptime' => trim($uptime),
	'systime' => trim($systime),
	'lastreboot' => trim($lastreboot),
	'cpuuse' => trim($cpuuse),
	'cputemp' => trim($cputemp),
	'cpufreq' => trim($cpufreq),
	'memtot' => trim($memtot),
	'memuse' => trim($memuse),
	'memfree' => trim($memfree),
	'diskuse' => trim($diskuse),
	'diskfree' => trim($diskfree),
	'ethaddr' => $ethaddr,
	'wlanaddr' => $wlanaddr,
	'wlanqualy' => $wlanqualy,
	'wlanbitrate' => $wlanbitrate,
	'wlanmode' => $wlanmode,
	'wlanssid' => $wlanssid,
	'wlanpower' => $wlanpower,
	'wlanrx' => $wlanrx,
	'wlantx' => $wlantx
);

header("Content-type: application/json");
echo json_encode($arr);
?>
