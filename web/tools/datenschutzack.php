<?php
// print_r($_POST); 

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	$writeit = '0';
	
	if(strpos($line, "datenschutzack=") !== false) {
		if ($_POST['datenschutzack'] == 1) {
			$result .= 'datenschutzack=1'."\n";
		} else {
			$result .= 'datenschutzack=2'."\n";
		}
		$writeit = '1';
	}
	
	if ( $writeit == '0' ) {
		$result .= $line;
	}
}
// subscribe to topic and wait for message
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
// wait for message and compare payload

if ($_POST['datenschutzack'] != 1) { ?>
	<form id="formid" action="./savemqtt.php?bridge=cloud" method="POST">
		<input type="hidden" name="ConnectionName" value="cloud"/>
		<input type="hidden" name="action" value="deleteBridge"/>
		<div class="row justify-content-center py-1">
			<button type="submit" class="btn btn-green" name="action" value="deleteBridge">Br&uuml;cke cloud l&ouml;schen</button>
		</div>
	</form>
	<script>
		function submitForm() {
			// **NOTE** set form values first
			document.getElementById('formid').submit(value="deleteBridge");
		}
		window.onload = submitForm;
	</script>
<?php
} else {
	header("Location: ../index.php");
}
?>
