<header>
	<!-- Fixed navbar -->
	<nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
		<a class="navbar-brand" href="index.php">
			<span>openWB</span>
		</a>
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar">
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="collapsibleNavbar">
			<ul class="navbar-nav">
				<li class="nav-item">
					<a class="nav-link" data-select="" href="logging/index.php">Langzeit</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" data-select="" href="logging/daily.php">Tag</a>
				</li>
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbarDropMonth" data-toggle="dropdown">
						Monat
					</a>
					<div class="dropdown-menu">
						<a class="dropdown-item" id="navMonth" href="logging/monthlyv1.php">Übersicht</a>
						<a class="dropdown-item" id="navMonthDetail" href="logging/monthlyv2.php">Aufteilung</a>
					</div>
				</li>
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbarDropYear" data-toggle="dropdown">
						Jahr
					</a>
					<div class="dropdown-menu">
						<a class="dropdown-item" id="navYear" href="logging/yearlyv1.php">Übersicht</a>
						<a class="dropdown-item" id="navYearDetail" href="logging/yearlyv2.php">Aufteilung</a>
					</div>
				</li>
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbarDropOld" data-toggle="dropdown">
						Alte Diagramme
					</a>
					<div class="dropdown-menu">
						<a class="dropdown-item" id="navOldMonth" href="logging/monthly.php">Monat</a>
						<a class="dropdown-item" id="navOldYear" href="logging/yearly.php">Jahr</a>
					</div>
				</li>
			</ul>
		</div>
	</nav>
</header>
