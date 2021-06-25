<?php
$assets = "display/yourcharge/";
$fileName = $_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf';
$file = file_get_contents($fileName);
preg_match('/displaysleep=(.+)/',  $file, $matches);
$displayTimeout = ($matches[1] ?? 91);
?>
<!DOCTYPE html>
<html lang="de">

<head>
  <base href="/openWB/web/" />
  <meta charset="UTF-8" />
  <title>openWB Display</title>
  <meta name="viewport" content=" shrink-to-fit=yes, user-scalable=no">
  <link rel="stylesheet" type="text/css" href="css/bootstrap.css" />
  <link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css" />
  <!-- Normalize -->
  <link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css" />
  <!-- Font Awesome, all styles -->
  <link rel="stylesheet" type="text/css" href="fonts/font-awesome-5.8.2/css/all.css" />
  <!-- important scripts to be loaded -->
  <script src="js/jquery-3.6.0.min.js"></script>
  <script src="<?= $assets; ?>js/jquery.sparkline.js"></script>
  <script>
    const lockTimeout = 6000000;
    let inactivityTimeout = <?= $displayTimeout * 1000 ?>;
  </script>
  <script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
  <!-- display style -->
  <link rel="stylesheet" type="text/css" href="<?= $assets; ?>css/style.css?ver=<?= date("YmdHis") ?>" />
</head>

<body>
  <main id="main">
    <!-- Side navigation -->
    <?php include("includes/navbar.php"); ?>
    <?php include("includes/sidebar.php"); ?>


    <!-- Dashboard -->
    <div id="dashboard" class="dashboard resume">
      <div class="row">
        <div class="col-xs-6">
          <?php include("includes/stats.php"); ?>
        </div>
        <div class="col-xs-6">
          <?php include("includes/charts.php"); ?>
        </div>
      </div>
    </div>

  </main>
  <?php include("includes/lock-modal.php"); ?>
  <?php include("includes/change-lock-code-modal.php"); ?>
  <?php include("includes/change-display-timeout-modal.php"); ?>
  <?php include("includes/wizard-modal.php"); ?>

  <script src="<?= $assets; ?>js/main.js">
  </script>
</body>

</html>