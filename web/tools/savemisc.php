<?php
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	$writeit = '0';
	if(strpos($line, "dspeed=") !== false) {
		$result .= 'dspeed='.$_POST['dspeed']."\n";
		$writeit = '1';
	}
	if(strpos($line, "netzabschaltunghz=") !== false) {
		$result .= 'netzabschaltunghz='.$_POST['netzabschaltunghz']."\n";
		$writeit = '1';
	}
	if(strpos($line, "cpunterbrechunglp1=") !== false) {
		$result .= 'cpunterbrechunglp1='.$_POST['cpunterbrechunglp1']."\n";
		$writeit = '1';
	}
	if(strpos($line, "cpunterbrechunglp2=") !== false) {
		$result .= 'cpunterbrechunglp2='.$_POST['cpunterbrechunglp2']."\n";
		$writeit = '1';
	}
	if(strpos($line, "livegraph=") !== false) {
		$result .= 'livegraph='.$_POST['livegraph']."\n";
		$writeit = '1';
	}
	if(strpos($line, "logdailywh=") !== false) {
		$result .= 'logdailywh='.$_POST['logdailywh']."\n";
		$writeit = '1';
	}
	if(strpos($line, "logeinspeisungneg=") !== false) {
		$result .= 'logeinspeisungneg='.$_POST['logeinspeisungneg']."\n";
		$writeit = '1';
	}
	if(strpos($line, "ladetaster=") !== false) {
		$result .= 'ladetaster='.$_POST['ladetaster']."\n";
		$writeit = '1';
	}
	if(strpos($line, "pushbenachrichtigung=") !== false) {
		$result .= 'pushbenachrichtigung='.$_POST['pushbenachrichtigung']."\n";
		$writeit = '1';
	}
	if(strpos($line, "settingspw=") !== false) {
		$result .= 'settingspw=\''.$_POST['settingspw']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "pushbstartl=") !== false) {
		$result .= 'pushbstartl='.$_POST['pushbstartl']."\n";
		$writeit = '1';
	}
	if(strpos($line, "pushbstopl=") !== false) {
		$result .= 'pushbstopl='.$_POST['pushbstopl']."\n";
		$writeit = '1';
	}
	if(strpos($line, "pushbplug=") !== false) {
		$result .= 'pushbplug='.$_POST['pushbplug']."\n";
		$writeit = '1';
	}
	if(strpos($line, "pushbsmarthome=") !== false) {
		$result .= 'pushbsmarthome='.$_POST['pushbsmarthome']."\n";
		$writeit = '1';
	}
	if(strpos($line, "pushovertoken=") !== false) {
		$result .= 'pushovertoken=\''.$_POST['pushovertoken']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "pushoveruser=") !== false) {
		$result .= 'pushoveruser=\''.$_POST['pushoveruser']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "grapham=") !== false) {
		$result .= 'grapham='.$_POST['grapham']."\n";
		$writeit = '1';
	}
	if(strpos($line, "graphliveam=") !== false) {
		$result .= 'graphliveam='.$_POST['graphliveam']."\n";
		$writeit = '1';
	}
	if(strpos($line, "graphinteractiveam=") !== false) {
		$result .= 'graphinteractiveam='.$_POST['graphinteractiveam']."\n";
		$writeit = '1';
	}
	if(strpos($line, "chartlegendmain=") !== false) {
		$result .= 'chartlegendmain='.$_POST['chartlegendmain']."\n";
		$writeit = '1';
	}
	if(strpos($line, "hausverbrauchstat=") !== false) {
		$result .= 'hausverbrauchstat='.$_POST['hausverbrauchstat']."\n";
		$writeit = '1';
	}
	if(strpos($line, "heutegeladen=") !== false) {
		$result .= 'heutegeladen='.$_POST['heutegeladen']."\n";
		$writeit = '1';
	}
	if(strpos($line, "bootmodus=") !== false) {
		$result .= 'bootmodus='.$_POST['bootmodus']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidakt=") !== false) {
		$result .= 'rfidakt='.$_POST['rfidakt']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp1start1=") !== false) {
		$result .= 'rfidlp1start1='.$_POST['rfidlp1start1']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp1start2=") !== false) {
		$result .= 'rfidlp1start2='.$_POST['rfidlp1start2']."\n";
		$writeit = '1';
	}

	if(strpos($line, "rfidlp1start3=") !== false) {
		$result .= 'rfidlp1start3='.$_POST['rfidlp1start3']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp1start4=") !== false) {
		$result .= 'rfidlp1start4='.$_POST['rfidlp1start4']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp1start5=") !== false) {
		$result .= 'rfidlp1start5='.$_POST['rfidlp1start5']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp2start1=") !== false) {
		$result .= 'rfidlp2start1='.$_POST['rfidlp2start1']."\n";
		$writeit = '1';
	}

	if(strpos($line, "rfidlp2start2=") !== false) {
		$result .= 'rfidlp2start2='.$_POST['rfidlp2start2']."\n";
		$writeit = '1';
	}

	if(strpos($line, "rfidlp2start3=") !== false) {
		$result .= 'rfidlp2start3='.$_POST['rfidlp2start3']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp2start4=") !== false) {
		$result .= 'rfidlp2start4='.$_POST['rfidlp2start4']."\n";
		$writeit = '1';
	}

	if(strpos($line, "rfidlp2start5=") !== false) {
		$result .= 'rfidlp2start5='.$_POST['rfidlp2start5']."\n";
		$writeit = '1';
	}

	if(strpos($line, "rfidstop=") !== false) {
		$result .= 'rfidstop='.$_POST['rfidstop']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidstandby=") !== false) {
		$result .= 'rfidstandby='.$_POST['rfidstandby']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidsofort=") !== false) {
		$result .= 'rfidsofort='.$_POST['rfidsofort']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidminpv=") !== false) {
		$result .= 'rfidminpv='.$_POST['rfidminpv']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidnurpv=") !== false) {
		$result .= 'rfidnurpv='.$_POST['rfidnurpv']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidstop2=") !== false) {
		$result .= 'rfidstop2='.$_POST['rfidstop2']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidstandby2=") !== false) {
		$result .= 'rfidstandby2='.$_POST['rfidstandby2']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidsofort2=") !== false) {
		$result .= 'rfidsofort2='.$_POST['rfidsofort2']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidminpv2=") !== false) {
		$result .= 'rfidminpv2='.$_POST['rfidminpv2']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidnurpv2=") !== false) {
		$result .= 'rfidnurpv2='.$_POST['rfidnurpv2']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidstop3=") !== false) {
		$result .= 'rfidstop3='.$_POST['rfidstop3']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidstandby3=") !== false) {
		$result .= 'rfidstandby3='.$_POST['rfidstandby3']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidsofort3=") !== false) {
		$result .= 'rfidsofort3='.$_POST['rfidsofort3']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidminpv3=") !== false) {
		$result .= 'rfidminpv3='.$_POST['rfidminpv3']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidnurpv3=") !== false) {
		$result .= 'rfidnurpv3='.$_POST['rfidnurpv3']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp1c1=") !== false) {
		$result .= 'rfidlp1c1='.$_POST['rfidlp1c1']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp1c2=") !== false) {
		$result .= 'rfidlp1c2='.$_POST['rfidlp1c2']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp1c3=") !== false) {
		$result .= 'rfidlp1c3='.$_POST['rfidlp1c3']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp2c1=") !== false) {
		$result .= 'rfidlp2c1='.$_POST['rfidlp2c1']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp2c2=") !== false) {
		$result .= 'rfidlp2c2='.$_POST['rfidlp2c2']."\n";
		$writeit = '1';
	}
	if(strpos($line, "rfidlp2c3=") !== false) {
		$result .= 'rfidlp2c3='.$_POST['rfidlp2c3']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displaypincode=") !== false) {
		$result .= 'displaypincode='.$_POST['displaypincode']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displaypinaktiv=") !== false) {
		$result .= 'displaypinaktiv='.$_POST['displaypinaktiv']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displaylp2max=") !== false) {
		$result .= 'displaylp2max='.$_POST['displaylp2max']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displaytheme=") !== false) {
		$result .= 'displaytheme='.$_POST['displaytheme']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displaytagesgraph=") !== false) {
		$result .= 'displaytagesgraph='.$_POST['displaytagesgraph']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displaylp1max=") !== false) {
		$result .= 'displaylp1max='.$_POST['displaylp1max']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displayhausmax=") !== false) {
		$result .= 'displayhausmax='.$_POST['displayhausmax']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displayhausanzeigen=") !== false) {
		$result .= 'displayhausanzeigen='.$_POST['displayhausanzeigen']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displayspeichermax=") !== false) {
		$result .= 'displayspeichermax='.$_POST['displayspeichermax']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displaypvmax=") !== false) {
		$result .= 'displaypvmax='.$_POST['displaypvmax']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displayevumax=") !== false) {
		$result .= 'displayevumax='.$_POST['displayevumax']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displaysleep=") !== false) {
		$result .= 'displaysleep='.$_POST['displaysleep']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displayEinBeimAnstecken=") !== false) {
		$result .= 'displayEinBeimAnstecken='.$_POST['displayEinBeimAnstecken']."\n";
		$writeit = '1';
	}
	if(strpos($line, "displayaktiv=") !== false) {
		$result .= 'displayaktiv='.$_POST['displayaktiv']."\n";
		$writeit = '1';
	}
	if(strpos($line, "led0sofort=") !== false) {
		$result .= 'led0sofort='.$_POST['led0sofort']."\n";
		$writeit = '1';
	}
	if(strpos($line, "led0nurpv=") !== false) {
		$result .= 'led0nurpv='.$_POST['led0nurpv']."\n";
		$writeit = '1';
	}
	if(strpos($line, "led0minpv=") !== false) {
		$result .= 'led0minpv='.$_POST['led0minpv']."\n";
		$writeit = '1';
	}
	if(strpos($line, "led0standby=") !== false) {
		$result .= 'led0standby='.$_POST['led0standby']."\n";
		$writeit = '1';
	}
	if(strpos($line, "led0stop=") !== false) {
		$result .= 'led0stop='.$_POST['led0stop']."\n";
		$writeit = '1';
	}
	if(strpos($line, "ledsofort=") !== false) {
		$result .= 'ledsofort='.$_POST['ledsofort']."\n";
		$writeit = '1';
	}
	if(strpos($line, "lednurpv=") !== false) {
		$result .= 'lednurpv='.$_POST['lednurpv']."\n";
		$writeit = '1';
	}
	if(strpos($line, "ledminpv=") !== false) {
		$result .= 'ledminpv='.$_POST['ledminpv']."\n";
		$writeit = '1';
	}
	if(strpos($line, "ledstandby=") !== false) {
		$result .= 'ledstandby='.$_POST['ledstandby']."\n";
		$writeit = '1';
	}
	if(strpos($line, "ledstop=") !== false) {
		$result .= 'ledstop='.$_POST['ledstop']."\n";
		$writeit = '1';
	}
	if(strpos($line, "ledsakt=") !== false) {
		$result .= 'ledsakt='.$_POST['ledsakt']."\n";
		$writeit = '1';
	}
	if(strpos($line, "settingspwakt=") !== false) {
		$result .= 'settingspwakt='.$_POST['settingspwakt']."\n";
		$writeit = '1';
	}

	if ( $writeit == '0') {
		$result .= $line;
	}
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
file_put_contents('/var/www/html/openWB/ramdisk/reloaddisplay', "1");
file_put_contents('/var/www/html/openWB/ramdisk/execdisplay', "1");
header("Location: ../index.php");
?>
