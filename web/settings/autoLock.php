<!DOCTYPE html>
<html lang="de">
	<!-- Einstellungen für automatisches Sperren/Entsperren
		 der LP: ein Vorgang pro Tag -->
	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
		<title>OpenWB</title>
		<meta name="description" content="Control your charge">
		<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design">
		<meta name="author" content="Michael Ortenstein">
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

		<!-- important scripts to be loaded -->
		<script type="text/javascript" src="js/jquery-3.4.1.min.js"></script>
		<script type="text/javascript" src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>

		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
		<!-- Font Awesome, all styles -->
		<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">

		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- clockpicker -->
		<script type="text/javascript" src="js/clockpicker/bootstrap-clockpicker.min.js"></script>
		<link rel="stylesheet" type="text/css" href="css/clockpicker/bootstrap-clockpicker.min.css">

	</head>

	<body>
		<?php

			/**
			 * Simple helper to debug to the console
			 *
			 * @param  Array, String $data
			 * @return String
			 */
			function debug_to_console( $data ) {
				$output = "<script>console.log( 'Debug Objects: " . $data . "' );</script>";

				echo $output;
			}


			// read settings for input elements from config file
			// first read config-lines in array
			$settingsFile = file('/var/www/html/openWB/web/tools/debugfilewithlotofstuff.txt');
			// prepare key/value array
			$settingsArray = [];

			// convert lines to key/value array for faster manipulation
			foreach($settingsFile as $line) {
				// split line at char '='
				$splitLine = explode('=', $line);
				// trim parts
				$splitLine[0] = trim($splitLine[0]);
				// check if key is for an element used on this page
				// so check for 'lockBox' and 'lockTime' as part of identifier
				if ( strpos($splitLine[0], 'lockBoxLp') !== false || strpos($splitLine[0], 'lockTimeLp') !== false ) {
					$splitLine[1] = trim($splitLine[1]);
					// push key/value pair to new array
					$settingsArray[$splitLine[0]] = $splitLine[1];
				}
			}
			// now values can be accessed by $settingsArray[$key] = $value;
			unset($settingsFile);  // no longer needed
		?>

		<?php include '/var/www/html/openWB/web/settings/navbar.html';?>

		<div role="main" class="container" style="margin-top:20px">
			<div class="row justify-content-center">

				<form class="form col-md-10" action="./tools/saveautolock.php" method="POST">

					<div class="form-group px-3 pb-3" style="border:1px solid black">  <!-- group charge point 1 -->
						<h1>LP 1 (<span id ="nameLp1">Name LP1</span>)</h1>
						<div class="row vaRow">  <!-- row monday = _1 -->
							<div class="col-2">
					            Montag
					        </div>
							<div class="col-5">
								<div class="form-row align-items-center">
									<div class="col-auto my-1">
										<div class="form-check">
											<input type="hidden" name="lockBoxLp[1][1]" value="<?php echo $settingsArray['lockBoxLp1_1']?>">
											<input class="form-check-input" type="checkbox" id="lockBoxLp1_1" name="lockBoxLp[1][1]">
											<label class="form-check-label pl-10" for="lockBoxLp1_1">
										  		sperren
											</label>
										</div>
									</div>
									<div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="lockTimeLp1_1" name="lockTimeLp[1][1]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
									</div>
								</div>
					        </div>
							<div class="col-5">
								<div class="form-row align-items-center">
									<div class="col-auto my-1">
										<div class="form-check">
											<input type="hidden" name="unlockBoxLp[1][1]" value="off">
											<input class="form-check-input" type="checkbox" id="unlockBoxLp1_1" name="unlockBoxLp[1][1]">
											<label class="form-check-label" for="unlockBoxLp1_1">
										  		entsperren
											</label>
										</div>
									</div>
									<div class="col-sm-6 my-1">
										<div class="input-group" >
											<input class="form-control" readonly id="unlockTimeLp1_1" name="unlockTimeLp[1][1]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
	    							</div>
								</div>
					        </div>
						</div>  <!-- end row monday -->
						<hr class="d-sm-none">
						<div class="row vaRow">  <!-- row tuesday = _2 -->
						    <div class="col-2">
						        Dienstag
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="lockBoxLp[1][2]" value="off">
						                    <input class="form-check-input" type="checkbox" id="lockBoxLp1_2" name="lockBoxLp[1][2]">
						                    <label class="form-check-label" for="lockBoxLp1_2">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="lockTimeLp1_2" name="lockTimeLp[1][2]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="unlockBoxLp[1][2]" value="off">
						                    <input class="form-check-input" type="checkbox" id="unlockBoxLp1_2" name="unlockBoxLp[1][2]">
						                    <label class="form-check-label" for="unlockBoxLp1_2">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="unlockTimeLp1_2" name="unlockTimeLp[1][2]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>

						        </div>
						    </div>
						</div>  <!-- end row tuesday -->
						<hr class="d-sm-none">
						<div class="row vaRow">  <!-- row wednesday = _3 -->
						    <div class="col-2">
						        Mittwoch
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="lockBoxLp[1][3]" value="off">
						                    <input class="form-check-input" type="checkbox" id="lockBoxLp1_3" name="lockBoxLp[1][3]">
						                    <label class="form-check-label" for="lockBoxLp1_3">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="lockTimeLp1_3" name="lockTimeLp[1][3]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="unlockBoxLp[1][3]" value="off">
						                    <input class="form-check-input" type="checkbox" id="unlockBoxLp1_3" name="unlockBoxLp[1][3]">
						                    <label class="form-check-label" for="unlockBoxLp1_3">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="unlockTimeLp1_3" name="unlockTimeLp[1][3]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>

						        </div>
						    </div>
						</div>  <!-- end row wednesday -->
						<hr class="d-sm-none">
						<div class="row vaRow">  <!-- row thursday = _4 -->
						    <div class="col-2">
						        Donnerstag
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="lockBoxLp[1][4]" value="off">
						                    <input class="form-check-input" type="checkbox" id="lockBoxLp1_4" name="lockBoxLp[1][4]">
						                    <label class="form-check-label" for="lockBoxLp1_4">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="lockTimeLp1_4" name="lockTimeLp[1][4]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="unlockBoxLp[1][4]" value="off">
						                    <input class="form-check-input" type="checkbox" id="unlockBoxLp1_4" name="unlockBoxLp[1][4]">
						                    <label class="form-check-label" for="unlockBoxLp1_4">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="unlockTimeLp1_4" name="unlockTimeLp[1][4]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>

						        </div>
						    </div>
						</div>  <!-- end row thursday -->
						<hr class="d-sm-none">
						<div class="row vaRow">  <!-- row friday = _5 -->
						    <div class="col-2">
						        Freitag
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="lockBoxLp[1][5]" value="off">
						                    <input class="form-check-input" type="checkbox" id="lockBoxLp1_5" name="lockBoxLp[1][5]">
						                    <label class="form-check-label" for="lockBoxLp1_5">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="lockTimeLp1_5" name="lockTimeLp[1][5]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="unlockBoxLp[1][5]" value="off">
						                    <input class="form-check-input" type="checkbox" id="unlockBoxLp1_5" name="unlockBoxLp[1][5]">
						                    <label class="form-check-label" for="unlockBoxLp1_5">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="unlockTimeLp1_5" name="unlockTimeLp[1][5]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>

						        </div>
						    </div>
						</div>  <!-- end row friday -->
						<hr class="d-sm-none">
						<div class="row vaRow">  <!-- row saturday = _6 -->
						    <div class="col-2">
						        Samstag
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="lockBoxLp[1][6]" value="off">
						                    <input class="form-check-input" type="checkbox" id="lockBoxLp1_6" name="lockBoxLp[1][6]">
						                    <label class="form-check-label" for="lockBoxLp1_6">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="lockTimeLp1_6" name="lockTimeLp[1][6]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="unlockBoxLp[1][6]" value="off">
						                    <input class="form-check-input" type="checkbox" id="unlockBoxLp1_6" name="unlockBoxLp[1][6]">
						                    <label class="form-check-label" for="unlockBoxLp1_6">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="unlockTimeLp1_6" name="unlockTimeLp[1][6]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>

						        </div>
						    </div>
						</div>  <!-- end row saturday -->
						<hr class="d-sm-none">
						<div class="row vaRow">  <!-- row sunday = _7 -->
						    <div class="col-2">
						        Sonntag
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="lockBoxLp[1][7]" value="off">
						                    <input class="form-check-input" type="checkbox" id="lockBoxLp1_7" name="lockBoxLp[1][7]">
						                    <label class="form-check-label" for="lockBoxLp1_7">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="lockTimeLp1_7" name="lockTimeLp[1][7]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
											<input type="hidden" name="unlockBoxLp[1][7]" value="off">
						                    <input class="form-check-input" type="checkbox" id="unlockBoxLp1_7" name="unlockBoxLp[1][7]">
						                    <label class="form-check-label" for="unlockBoxLp1_7">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group">
											<input class="form-control" readonly id="unlockTimeLp1_7" name="unlockTimeLp[1][7]" placeholder="--">
											<div class="input-group-append">
												<span class="input-group-text far fa-xs fa-clock vaRow"></span>
											</div>
										</div>
						            </div>

						        </div>
						    </div>
						</div>  <!-- end row sunday -->
					</div>  <!-- end form-group charge point 1 -->




					<div class="row justify-content-center">
						<button type="submit" class="btn btn-lg btn-green">Einstellungen übernehmen</button>
					</div>

				</form>  <!-- end form -->
			</div>
			<br>


		</div>  <!-- end container -->

		<footer class="footer bg-dark text-light font-small">
	      <div class="container text-center">
			  <small>Sie befinden sich hier: Auto-Lock</small>
	      </div>
	    </footer>

		<script type="text/javascript">
			function addClockpicker(targetId) {
				// add a clickpicker to input targetID (eg #unlockTimeLp1_7)
				// and set input field to 00:00
				$(targetId).clockpicker({
					placement: 'bottom',  // clock popover placement
					align: 'left',  // popover arrow align
					donetext: '',  // done button text
					autoclose: true,  // auto close when minute is selected
					vibrate: true,  // vibrate the device when dragging clock hand
					default: '00:00'
				});
				//document.querySelector(targetId+" input[type='text']").value = "00:00";
			}

			function removeClockpicker(targetId) {
				// remove a clickpicker in input targetID (eg #unlockTimeLp1_7)
				// and set input value to --
				if ( $(targetId).length ) {
					// if clockpicker exists
					$(targetId).clockpicker('remove');
					document.querySelector(targetId).value = "";
				}
			}

			$(function() {
				// if a checkbox is checked/unchecked
				// add/remove respective clockpicker
				// and empty input field if removed
			    $('input:checkbox').change(function() {
					var boxIsChecked = $(this).prop('checked') == true;
					var clockPickerId = "#" + this.id.replace("Box", "Time");  // create matching clockpicker id
					if ( boxIsChecked ) {
						// activate clockpicker
						addClockpicker(clockPickerId);
					} else {
						// remove clockpicker
						removeClockpicker(clockPickerId);
					}
			    })
			  })

	    	function saveSettings() {
	    	}

	    </script>

	</body>
</html>
