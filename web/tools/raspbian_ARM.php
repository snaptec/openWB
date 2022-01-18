<?php
# Commands
$UPTIME="uptime";
$CPUUSE="ps aux|awk 'NR > 0 { s +=$3 }; END {print \"cpu %\",s}' | awk '{ print $3 }'";
$MEMTOT="free -m | grep 'Mem' | awk '{print $2}'";
$MEMUSE="free -m| grep 'Mem' | awk '{print $3}'";
$MEMFREE="free -m| grep 'Mem' | awk '{print $7}'";
$DISKTOT="df -h | grep root | awk '{print $2}'"; 
$DISKUSE="df -h | grep root | awk '{print $3}'";
$DISKFREE="df -h | grep root | awk '{print $4}'";
$DISKUSEDPRZ="df -h | grep root | awk '{print $5}'";
$TMPTOT="df -h | grep  ramdisk | awk '{print $2}'";
$TMPUSE="df -h | grep  ramdisk | awk '{print $3}'";
$TMPFREE="df -h | grep  ramdisk | awk '{print $4}'";
$TMPUSEDPRZ="df -h | grep  ramdisk | awk '{print $5}'";
?>
