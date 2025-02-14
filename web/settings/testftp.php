<?php
#ini_set('display_errors', 1);
#ini_set('display_startup_errors', 1);
#error_reporting(E_ALL);
$ftp = ftp_connect($_GET['ftphost']); 
$login_result = ftp_login($ftp, $_GET['ftpuser'], $_GET['ftppass']); 

if ((!$ftp) || (!$login_result)) { 
    echo "0";
} else {
    $res = ftp_chdir($ftp, $_GET['ftppath']);
    if (!$res) {
      echo "1";
    } else {
      echo "2";
    }
}
?>