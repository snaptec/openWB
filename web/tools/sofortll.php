
<?php


if(isset($_POST['sofortll'])) {

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortll=") !== false) {
	       $result .= 'sofortll='.$_POST['sofortll']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortlls1=") !== false) {
	       $result .= 'sofortlls1='.$_POST['sofortlls1']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortlls2=") !== false) {
	       $result .= 'sofortlls2='.$_POST['sofortlls2']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "lademkwh=") !== false) {
	       $result .= 'lademkwh='.$_POST['lademlp1']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "lademstat=") !== false) {
	       $result .= 'lademstat='.$_POST['lademlp1check']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "lademkwhs1=") !== false) {
	       $result .= 'lademkwhs1='.$_POST['lademlp2']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "lademstats1=") !== false) {
	       $result .= 'lademstats1='.$_POST['lademlp2check']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "lademkwhs2=") !== false) {
	       $result .= 'lademkwhs2='.$_POST['lademlp3']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortsoclp1=") !== false) {
	       $result .= 'sofortsoclp1='.$_POST['sofortsoclp1']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortsoclp2=") !== false) {
	       $result .= 'sofortsoclp2='.$_POST['sofortsoclp2']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortsoclp3=") !== false) {
	       $result .= 'sofortsoclp3='.$_POST['sofortsoclp3']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortsocstatlp1=") !== false) {
	       $result .= 'sofortsocstatlp1='.$_POST['sofortsocstatlp1']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortsocstatlp2=") !== false) {
	       $result .= 'sofortsocstatlp2='.$_POST['sofortsocstatlp2']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortsocstatlp3=") !== false) {
	       $result .= 'sofortsocstatlp3='.$_POST['sofortsocstatlp3']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);



$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "lademstats2=") !== false) {
	       $result .= 'lademstats2='.$_POST['lademlp3check']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
header("Location: ../index.php");

}
?>



