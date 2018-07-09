
<?php
if(isset($_POST['minimalstromstaerke'])) {
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "pvbezugeinspeisung=") !== false) {
	    $result .= 'pvbezugeinspeisung='.$_POST[pvbezugeinspeisung]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';

$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "minimalampv=") !== false) {
	    $result .= 'minimalampv='.$_POST[minimalampv]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);


$result = '';

$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "minimalapv=") !== false) {
	    $result .= 'minimalapv='.$_POST[minimalapv]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';

$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "minimalstromstaerke=") !== false) {
	    $result .= 'minimalstromstaerke='.$_POST[minimalstromstaerke]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';

$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "maximalstromstaerke=") !== false) {
	    $result .= 'maximalstromstaerke='.$_POST[maximalstromstaerke]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtladen=") !== false) {
	    $result .= 'nachtladen='.$_POST[nachtladen]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtll=") !== false) {
	    $result .= 'nachtll='.$_POST[nachtll]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtladenabuhr=") !== false) {
	    $result .= 'nachtladenabuhr='.$_POST[nachtladenabuhr]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtladenbisuhr=") !== false) {
	    $result .= 'nachtladenbisuhr='.$_POST[nachtladenbisuhr]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtsoc=") !== false) {
	    $result .= 'nachtsoc='.$_POST[nachtsoc]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtsoc1=") !== false) {
	    $result .= 'nachtsoc1='.$_POST[nachtsoc1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "mindestuberschuss=") !== false) {
	    $result .= 'mindestuberschuss='.$_POST[mindestuberschuss]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "abschaltuberschuss=") !== false) {
	    $result .= 'abschaltuberschuss='.$_POST[abschaltuberschuss]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "abschaltverzoegerung=") !== false) {
	    $result .= 'abschaltverzoegerung='.$_POST[abschaltverzoegerung]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "lastmaxap1=") !== false) {
	    $result .= 'lastmaxap1='.$_POST[lastmaxap1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "lastmaxap2=") !== false) {
	    $result .= 'lastmaxap2='.$_POST[lastmaxap2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "lastmaxap3=") !== false) {
	    $result .= 'lastmaxap3='.$_POST[lastmaxap3]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "durchslp1=") !== false) {
	    $result .= 'durchslp1='.$_POST[durchslp1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "durchslp2=") !== false) {
	    $result .= 'durchslp2='.$_POST[durchslp2]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "durchslp3=") !== false) {
	    $result .= 'durchslp3='.$_POST[durchslp3]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtlls1=") !== false) {
	    $result .= 'nachtlls1='.$_POST[nachtlls1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtladens1=") !== false) {
	    $result .= 'nachtladens1='.$_POST[nachtladens1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtsocs1=") !== false) {
	    $result .= 'nachtsocs1='.$_POST[nachtsocs1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtsoc1s1=") !== false) {
	    $result .= 'nachtsoc1s1='.$_POST[nachtsoc1s1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtladenabuhrs1=") !== false) {
	    $result .= 'nachtladenabs1='.$_POST[nachtladenabuhrs1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "nachtladenbisuhrs1=") !== false) {
	    $result .= 'nachtladenbisuhrs1='.$_POST[nachtladenbisuhrs1]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);




}
header("Location: ../index.php");

?>



