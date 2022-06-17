<?php

function makedatetime($start,$f)
{
  //echo "$start;$f;";
  
   preg_match('/(.*)-(.*)/',$start,$xx);
   $day=$xx[1];
   $vonuhr=$xx[2];
   preg_match('/(.*)-(.*)/',$f,$xx);
   $bisuhr=$xx[2];
   
   echo "$day;$vonuhr - $bisuhr;";
}



 if( $_GET['do']=='export')
 {
   $dates='';
   $year=0;
   $fn='';

   if( isset($_GET['date']) )
   {
      $dates=str_replace("-","",$_GET['date']);   
      $fin="/var/www/html/openWB/web/logging/data/ladelog/$dates.csv";
      $file=file($fin);
      asort($file);
      $fn='Ladelog_'.$dates.'.csv';
   }
   else if ( isset($_GET['year']) )
   {
      $year=str_replace("-","",$_GET['year']);
   
      $files = glob($_SERVER['DOCUMENT_ROOT'] . "/openWB/web/logging/data/ladelog/*.csv");
      asort($files);
      $rowClasses = "";
      $file=[];
      foreach ($files as $current) 
      {
        preg_match('/\/var\/www\/html\/openWB\/web\/logging\/data\/ladelog\/([0-9]{4})([0-9]{2})\.csv/',$current,$m);
        if( $m[1] == $year )
        { 
          $onef = file($current);
          asort($onef);
          foreach($onef as $line)
             if( trim($line) > '')
               $file[]=$line;
        }  
      }
      $fn='Ladelog_'.$year.'.csv';
   }

   
   header('Content-Type: application/csv; charset=UTF-8');
   header('Content-Disposition: attachment;filename="'.$fn.'";');

   // Haben wir den Kilometerstand vom Ladestart im Ladelog ?   
   if(file_exists('/var/www/html/openWB/ramdisk/soc1KM'))
       $head="Tag;Zeit;Km;Kwh;Lade Kw;Ladezeit;Ladepunkt;Lademodus;RFID;Km-Stand\n";
   else 
       $head="Tag;Zeit;Km;Kwh;Lade Kw;Ladezeit;Ladepunkt;Lademodus;RFID\n";

  // kopfzeile mit ;
   echo str_replace(",",";",$head);
   // daten mit ; und "," als dezimaltrenner
   foreach($file as $line)
     {
       if(trim($line)=='') continue;
       $fields=explode(",",$line);
       $idx=0;
       foreach($fields as $f)
         {    $idx++;
              $f=trim($f);
              switch($idx)
              {
               case 1: $starts=$f;
                       break;
               case 2: makedatetime($starts,$f);
                       break;
               case 6: echo str_replace('H','Std',$f).";";
                       break;
               case 8:
                       switch ((int)$f) 
                       {
                        case 0: echo "Sofort;";
                                break;
                        case 1: echo "Min+PV;";
                                break;
                        case 2: echo "Nur PV;";
                                break;
                        case 7: echo "Nachtladen;";
                                break;
                        default:
                               echo str_replace('.',',',$f).";";
                      }
                      break;
             default:
                     echo str_replace('.',',',$f).";";
                     break;
            }
        } 
        echo "\n";
    }
    exit;
 }

//header( 'Refresh:600;' ); 
?>
<!DOCTYPE html>
<html lang="de">

	<head>
	<base href="/openWB/web/">
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>OpenWB Ladelog</title>
		<meta name="description" content="Control your charge" />
		<meta name="author" content="Kevin Wieland" />
		<!-- Favicons (created with http://realfavicongenerator.net/)-->
		<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
		<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
		<link rel="icon" type="image/png" href="img/favicons/favicon-32x32.png" sizes="32x32">
		<link rel="icon" type="image/png" href="img/favicons/favicon-16x16.png" sizes="16x16">
		<link rel="manifest" href="manifest.json">
		<link rel="shortcut icon" href="img/favicons/favicon.ico">
		<meta name="msapplication-TileColor" content="#00a8ff">
		<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
		<meta name="theme-color" content="#ffffff">
		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
		<!-- Bootstrap-Datepicker -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-datepicker/bootstrap-datepicker3.min.css">
		<!-- Bootstrap-Toggle -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap4-toggle/bootstrap4-toggle.min.css">
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="logging/chargelog/ladelog_style.css?ver=20210202">
		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<script>
			function getCookie(cname) {
				var name = cname + '=';
				var decodedCookie = decodeURIComponent(document.cookie);
				var ca = decodedCookie.split(';');
				for(var i = 0; i <ca.length; i++) {
					var c = ca[i];
					while (c.charAt(0) == ' ') {
						c = c.substring(1);
					}
					if (c.indexOf(name) == 0) {
						return c.substring(name.length, c.length);
					}
				}
				return '';
			}
			var themeCookie = getCookie('openWBTheme');
			// include special Theme style
			if( '' != themeCookie ){
				$('head').append('<link rel="stylesheet" href="themes/' + themeCookie + '/settings.css?v=20210209">');
			}
		</script>
	</head>

	<body>
		<div id="nav"></div> <!-- placeholder for navbar -->
		<div role="main" class="container">
			<h1>Lade-Log Export</h1>
			<div class="card border-secondary">
				<div class="card-header bg-secondary">
					Aufgezeichnete Logdateien
				</div>
				<div class="card-body">
					<?php
						$years=[];
						$files = glob($_SERVER['DOCUMENT_ROOT'] . "/openWB/web/logging/data/ladelog/*.csv");
						arsort($files);
						$rowClasses = "";
						foreach ($files as $current) {
					?>
						<div class="row<?php echo $rowClasses; ?>">
							<label class="col-6 col-form-label">
								<?php 
									preg_match('/\/var\/www\/html\/openWB\/web\/logging\/data\/ladelog\/([0-9]{4})([0-9]{2})\.csv/',$current,$m);
									$years[$m[1]]='found'; 
									$month = $m[2];
									setlocale(LC_TIME, "de_DE.UTF-8");
									$month_name = strftime('%B', mktime(0, 0, 0, $month));
									echo "$month_name ", $m[1];
								?>
							</label>
							<div class="col-6 text-right">
								<a class="btn downloadBtn btn-info" style="margin-bottom:12px" 
								 href="logging/chargelog/ladelogexport.php<?php
									echo "?date=" . pathinfo($current)['filename'] ."&do=export\">";
									?><i class="fas fa-download"></i> Download</a>
							</div>
						</div>
					<?php
						$rowClasses = " border-top pt-2";
						}

					   foreach( $years as $e=>$dumy)
						{
						    echo "<div class=\"row $rowClasses \">";
							echo "<label class=\"col-6 col-form-label\">Ganzes Jahr $e</label>";
							echo "<div class=\"col-6 text-right\">";
							echo " <a class=\"btn downloadBtn btn-info\" style=\"margin-bottom:12px;\" "; 
							echo "       href=\"logging/chargelog/ladelogexport.php?year=$e&do=export\">";
							echo " <i class=\"fas fa-download\"></i> Download</a>";
							echo "</div>";
							echo "</div>";
						 }
					?>

				</div>
			</div>
		</div>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: <a href="logging/chargelog/ladelog.php">Lade-Log</a> - Lade-Log Export</small>
			</div>
		</footer>

		<script>
			$.get(
				{ url: "themes/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navlogExport').addClass('disabled');
				}
			);
		</script>
	</body>
</html>
