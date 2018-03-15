<html>
<body><?php


$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
    if(substr($line, 0, 9) == 'sofortll=') {
	    $sofortllold = substr($line, 9, 2);
	    
    }
}



?>





<form name="sofortll" action="./tools/sofortll.php" method="POST">
	<label for="sofortll">Sofortmodus Ladeleistung:</label><br>
	<input type="text" name="sofortll" id="sofortll" value="<?php echo $sofortllold ?>">
	<br>
	<button type="submit" class="btn btn-primary">Save</button>	 
 </form>
</body></html>

