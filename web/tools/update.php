<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<title>openWB Update</title>

		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
		<!-- include reboot-style -->
		<link rel="stylesheet" type="text/css" href="tools/reboot.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
	</head>

	<body>

		<header>
			<!-- Fixed navbar -->
			<nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
				<div class="navbar-brand">
					openWB
				</div>
			</nav>
		</header>

		<div role="main" class="container" style="margin-top:20px">
			<div class="row">
				<div class="col text-center">
					<h1>Update</h1>
				</div>
			</div>
			<div class="row">
				<div class="col text-center">
					<p id="infoText"></p>
				</div>
			</div>
			<br>
			<div class="row">
				<div class="cssload-loader text-center">
					<div class="cssload-inner cssload-one"></div>
					<div class="cssload-inner cssload-two"></div>
					<div class="cssload-inner cssload-three"></div>
				</div>
			</div>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
			</div>
		</footer>

		<script>
			$(document).ready(function(){
				$("#infoText").text("Update der openWB angefordert...");
				$.get({ url: "./tools/updatePerformNow.php", cache: false }).done(function() {
					setTimeout(function() { window.location.href = "./index.php"; }, 20000);
				})
			});
		</script>

	</body>
</html>
