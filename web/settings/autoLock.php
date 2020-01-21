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

		<!-- Tempus Dominus TimePicker -->
		<script type="text/javascript" src="js/moment.js"></script>
		<script type="text/javascript" src="js/tempusdominus-5.1.3/tempusdominus-bootstrap-4.min.js"></script>
		<link rel="stylesheet" type="text/css" href="css/tempusdominus-5.1.3/tempusdominus-bootstrap-4.min.css">

		<!-- clockpicker -->
		<script type="text/javascript" src="js/clockpicker/bootstrap-clockpicker.min.js"></script>
		<link rel="stylesheet" type="text/css" href="css/clockpicker/bootstrap-clockpicker.min.css">

	</head>

	<body>

		<?php include '/var/www/html/openWB/web/settings/navbar.html';?>

		<div role="main" class="container" style="margin-top:20px">
			<div class="row justify-content-center">
				<div class="form col-md-10">

					<div class="form-group px-3 pb-3" style="border:1px solid black">  <!-- group charge point 1 -->
						<h1>LP 1</h1>
						<div class="row vaRow">  <!-- row monday = _1 -->
							<div class="col-2">
					            Montag
					        </div>
							<div class="col-5">
								<div class="form-row align-items-center">
									<div class="col-auto my-1">
										<div class="form-check">
											<input class="form-check-input" type="checkbox" id="lockLp1_1">
											<label class="form-check-label pl-10" for="lockLp1_1">
										  		sperren
											</label>
										</div>
									</div>
									<div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="lockTimeLp1_1">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
											</div>
										</div>
									</div>
								</div>
					        </div>
							<div class="col-5">
								<div class="form-row align-items-center">
									<div class="col-auto my-1">
										<div class="form-check">
											<input class="form-check-input" type="checkbox" id="unlockLp1_1">
											<label class="form-check-label" for="unlockLp1_1">
										  		entsperren
											</label>
										</div>
									</div>
									<div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="unlockTimeLp1_1">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
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
						                    <input class="form-check-input" type="checkbox" id="lockLp1_2">
						                    <label class="form-check-label" for="lockLp1_2">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="lockTimeLp1_2">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
						                    <input class="form-check-input" type="checkbox" id="unlockLp1_2">
						                    <label class="form-check-label" for="unlockLp1_2">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="unlockTimeLp1_2">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
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
						                    <input class="form-check-input" type="checkbox" id="lockLp1_3">
						                    <label class="form-check-label" for="lockLp1_3">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="lockTimeLp1_3">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
						                    <input class="form-check-input" type="checkbox" id="unlockLp1_3">
						                    <label class="form-check-label" for="unlockLp1_3">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="unlockTimeLp1_3">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
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
						                    <input class="form-check-input" type="checkbox" id="lockLp1_4">
						                    <label class="form-check-label" for="lockLp1_4">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="lockTimeLp1_4">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
						                    <input class="form-check-input" type="checkbox" id="unlockLp1_4">
						                    <label class="form-check-label" for="unlockLp1_4">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="unlockTimeLp1_4">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
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
						                    <input class="form-check-input" type="checkbox" id="lockLp1_5">
						                    <label class="form-check-label" for="lockLp1_5">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="lockTimeLp1_5">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
						                    <input class="form-check-input" type="checkbox" id="unlockLp1_5">
						                    <label class="form-check-label" for="unlockLp1_5">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="unlockTimeLp1_5">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
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
						                    <input class="form-check-input" type="checkbox" id="lockLp1_6">
						                    <label class="form-check-label" for="lockLp1_6">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="lockTimeLp1_6">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
						                    <input class="form-check-input" type="checkbox" id="unlockLp1_6">
						                    <label class="form-check-label" for="unlockLp1_6">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="unlockTimeLp1_6">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
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
						                    <input class="form-check-input" type="checkbox" id="lockLp1_7">
						                    <label class="form-check-label" for="lockLp1_7">
						                        sperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="lockTimeLp1_7">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
											</div>
										</div>
						            </div>
						        </div>
						    </div>
						    <div class="col-5">
						        <div class="form-row align-items-center">
						            <div class="col-auto my-1">
						                <div class="form-check">
						                    <input class="form-check-input" type="checkbox" id="unlockLp1_7">
						                    <label class="form-check-label" for="unlockLp1_7">
						                        entsperren
						                    </label>
						                </div>
						            </div>
						            <div class="col-sm-6 my-1">
										<div class="input-group clockpicker" id="unlockTimeLp1_7">
											<input type="text" class="form-control" readonly>
											<div class="input-group-append">
												<span class="input-group-text far fa-clock vaRow"></span>
											</div>
										</div>
						            </div>

						        </div>
						    </div>
						</div>  <!-- end row sunday -->
					</div>  <!-- end form-group charge point 1 -->





				</div>  <!-- end form -->
			</div>
			<br>

			<div class="row justify-content-center">
				<button onclick="saveSettings()" class="btn btn-lg btn-green">Einstellungen übernehmen</button>
			</div>

		</div>  <!-- end container -->

		<footer class="footer bg-dark text-light font-small">
	      <div class="container text-center">
			  <small>Sie befinden sich hier: Auto-Lock</small>
	      </div>
	    </footer>

		<script type="text/javascript">

			$(function () {
				// loop through all clockpicker classes
				// find the ids and set datepicker options
				$('.clockpicker').each(function(){
					console.log('found: '+this.id);
					$('#'+this.id).clockpicker({
						placement: 'bottom',// clock popover placement
						align: 'left',      // popover arrow align
						donetext: '',    // done button text
						autoclose: true,   // auto close when minute is selected
						vibrate: true        // vibrate the device when dragging clock hand
					});
				})
			});

			$(function() {
				// if a checkbox is checked/unchecked
				// toggle respective time picker
			    $('input:checkbox').change(function() {
			      $('#console-event').html('Toggle: ' + $(this).prop('checked'))
			    })
			  })

	    	function saveSettings() {
	    	}
	    </script>

	</body>
</html>
