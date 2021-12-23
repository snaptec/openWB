<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Tesla Login</title>
		<meta name="description" content="Control your charge" />
		<meta name="author" content="Lutz Bender" />
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

		<link rel="stylesheet" type="text/css" href="fonts/font-awesome-5.8.2/css/all.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
	</head>

	<body>
		<div role="main" class="container" style="margin-top:20px">

			<?php
				// https://raw.githubusercontent.com/teslascope/tokens/master/auth.tokens.py
				// https://github.com/timdorr/tesla-api/discussions/288
				// https://github.com/timdorr/tesla-api/discussions/296
				// https://github.com/timdorr/tesla-api/discussions/362

				$tesla_api_oauth2 = 'https://auth.tesla.com/oauth2/v3';
				$tesla_api_redirect = 'https://auth.tesla.com/void/callback';
				$tesla_api_owners = 'https://owner-api.teslamotors.com/oauth/token';
				$tesla_api_code_vlc = 86;
				$cid = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384";
				$cs = "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"; 
				$user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148";
				$cookie_file = __DIR__."/tmp/cookies.txt";

				// openWB specific part
				$chargepoint = ( $_REQUEST['chargepoint'] ? $_REQUEST['chargepoint'] : "1" );
				$cookie_file = $_SERVER['DOCUMENT_ROOT']."/openWB/ramdisk/tesla-cookies.lp".$chargepoint;
				$token_file = __DIR__."/tokens.lp".$chargepoint;

				function tesla_connect($url, $returntransfer=1, $referer="", $http_header="", $post="", $need_header=0, $cookies="", $timeout = 10)
				{
					global $cookie_file;

					if(!empty($post)) { $cpost = 1; } else { $cpost = 0; }
					if(is_array($http_header)) { $chheader = 1; } else { $chheader = 0; }

					$ch = curl_init();
					curl_setopt($ch, CURLOPT_URL, $url);
					curl_setopt($ch, CURLOPT_RETURNTRANSFER, $returntransfer);
					curl_setopt($ch, CURLOPT_TIMEOUT, $timeout);
					curl_setopt($ch, CURLOPT_HEADER, $need_header);
					curl_setopt($ch, CURLOPT_POST, $cpost);
					curl_setopt($ch, CURLOPT_FRESH_CONNECT, 0);
					curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 1);
					curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 1);
					curl_setopt($ch, CURLOPT_COOKIEFILE, $cookie_file);
					curl_setopt($ch, CURLOPT_COOKIEJAR, $cookie_file);
					// curl_setopt($ch, CURLOPT_SSLVERSION, CURL_SSLVERSION_MAX_TLSv1_2);
					if (defined('CURL_SSLVERSION_MAX_TLSv1_2')) curl_setopt ($ch, CURLOPT_SSLVERSION,CURL_SSLVERSION_MAX_TLSv1_2); // FM - force tls1.2
					curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);

					if(!empty($referer)) { curl_setopt($ch, CURLOPT_REFERER, $referer); }

					if($chheader == 1) { curl_setopt($ch, CURLOPT_HTTPHEADER, $http_header); }

					if($cpost == 1) { curl_setopt($ch, CURLOPT_POSTFIELDS, $post); }
					
					if(!empty($cookies)) { curl_setopt($ch, CURLOPT_COOKIE, $cookies); }

					$response = curl_exec($ch);
					$header = curl_getinfo($ch);
					curl_close($ch);

					return array("response" => $response, "header" => $header);

				}


				function gen_challenge()
				{
					global $tesla_api_code_vlc;

					$code_verifier = substr(hash('sha512', mt_rand()), 0, $tesla_api_code_vlc);
					$code_challenge = rtrim(strtr(base64_encode($code_verifier), '+/', '-_'), '='); 
					
					$state = rtrim(strtr(base64_encode(substr(hash('sha256', mt_rand()), 0, 12)), '+/', '-_'), '='); 

					return array("code_verifier" => $code_verifier, "code_challenge" => $code_challenge, "state" => $state);
				}


				function gen_url($code_challenge, $state)
				{
					global $tesla_api_oauth2, $tesla_api_redirect;


					$datas = array(
						'audience' => '',
						'client_id' => 'ownerapi',
						'code_challenge' => $code_challenge,
						'code_challenge_method' => 'S256',
						'locale' => 'en-US',
						'prompt' => 'login',
						'redirect_uri' => $tesla_api_redirect,
						'response_type' => 'code',
						'scope' => 'openid email offline_access',
						'state' => $state
					);

					return $tesla_api_oauth2."/authorize?".http_build_query($datas);
				}


				function return_msg($code, $msg)
				{
					return json_encode(array("success" => $code, "message" => $msg));
				}


				function login($weburl, $code_verifier, $code_challenge, $state)
				{
					global $tesla_api_redirect, $user_agent, $tesla_api_oauth2, $cid, $cs, $tesla_api_owners;

					
					$code = explode('https://auth.tesla.com/void/callback?code=', $weburl);
					$code = explode("&", $code[1])[0];


					if(empty($code)) { return return_msg(0, "Something is wrong ... Code not exists"); }

					// Get the Bearer token
					$http_header = array('Content-Type: application/json', 'Accept: application/json', 'User-Agent: '.$user_agent);
					$post = json_encode(array("grant_type" => "authorization_code", "client_id" => "ownerapi", "code" => $code, "code_verifier" => $code_verifier, "redirect_uri" => $tesla_api_redirect));
					$response = tesla_connect($tesla_api_oauth2."/token", 1, "", $http_header, $post, 0);

					$token_res = json_decode($response["response"], true);
					$bearer_token = $token_res["access_token"];
					$refresh_token = $token_res["refresh_token"];

					if(empty($bearer_token)) { return return_msg(0, "Bearer Token issue"); }

					// Final Step
					unset($response);
					$http_header = array('Authorization: Bearer '.$bearer_token, 'Content-Type: application/json');
					$post = json_encode(array("grant_type" => "urn:ietf:params:oauth:grant-type:jwt-bearer", "client_id" => $cid, "client_secret" => $cs));
					$response = tesla_connect($tesla_api_owners, 1, "", $http_header, $post, 0);

					$tokens = json_decode($response["response"], true);

					if(empty($tokens['access_token'])) { return return_msg(0, "Token issue"); }

					$tokens["bearer_token"] = $bearer_token;
					$tokens["bearer_refresh_token"] = $refresh_token;
					$return_message = json_encode($tokens);

					// Output
					return return_msg(1, $return_message);
				}


				function tesla_oauth2_refresh_token($bearer_refresh_token)
				{
					global $tesla_api_oauth2, $tesla_api_redirect, $tesla_api_owners, $tesla_api_code_vlc, $cid, $cs;


					$brt = $bearer_refresh_token;

					// Get the Bearer token
					$http_header = array('Content-Type: application/json', 'Accept: application/json');
					$post = json_encode(array("grant_type" => "refresh_token", "client_id" => "ownerapi", "refresh_token" => $brt, "scope" => "openid email offline_access"));
					$response = tesla_connect($tesla_api_oauth2."/token", 1, "https://auth.tesla.com/", $http_header, $post, 0);


					$token_res = json_decode($response["response"], true);
					$bearer_token = $token_res["access_token"];
					$refresh_token = $token_res["refresh_token"];


					if(empty($bearer_token)) { return return_msg(0, "Bearer Refresh Token is not valid"); }

					$http_header = array('Authorization: Bearer '.$bearer_token, 'Content-Type: application/json');
					$post = json_encode(array("grant_type" => "urn:ietf:params:oauth:grant-type:jwt-bearer", "client_id" => $cid, "client_secret" => $cs));
					$response = tesla_connect($tesla_api_owners, 1, "", $http_header, $post, 0);

					$tokens = json_decode($response["response"], true);

					if(empty($tokens['access_token'])) { return return_msg(0, "Token issue"); }

					$tokens["bearer_token"] = $bearer_token;
					$tokens["bearer_refresh_token"] = $refresh_token;
					$return_message = json_encode($tokens);

					// Output
					return return_msg(1, $return_message);

				}

				function html_login()
				{
					global $chargepoint;
					global $tesla_api_redirect;

					$challenge = gen_challenge();
					$code_verifier = $challenge["code_verifier"];
					$code_challenge = $challenge["code_challenge"];
					$state = $challenge["state"];
					$timestamp = time();

					?>
					<div class="card border-secondary">
						<form method="post">
							<div class="card-header bg-secondary">
								Login bei Tesla (Ladepunkt <?php echo $chargepoint; ?>)
							</div>
							<div class="card-body">
								<input type="hidden" name="go" value="login">
								<input type="hidden" name="code_verifier" value="<?php echo $code_verifier; ?>">
								<input type="hidden" name="code_challenge" value="<?php echo $code_challenge; ?>">
								<input type="hidden" name="state" value="<?php echo $state; ?>">
								<p>
									Seit der Umstellung auf reCaptcha bei der Tesla-Anmeldung kann die Anmeldung nicht mehr automatisch durchgeführt werden.<br />
									Bitte die folgenden Schritte nacheinander durchführen:
								</p>
								<ol>
									<li>Bitte <strong><a href="<?php echo $_SERVER['REQUEST_URI'] . "#" . $timestamp; ?>" onclick="teslaLogin();return false;">hier klicken</a></strong>, um sich direkt bei Tesla anzumelden. Dazu wird ein neues Fenster geöffnet. Bitte Popups im Browser erlauben!</li>
									<li>In dem neuen Fenster mit den eigenen Zugangsdaten anmelden.</li>
									<li>Wenn die Anmeldung erfolgreich war, erscheint eine <strong>"Page Not Found"</strong> Meldung der Tesla Webseite. Dann die komplette URL dieser Webseite kopieren (z. B. <strong><?php echo $tesla_api_redirect; ?>?code=.....&state=...&issuer=....</strong>)</li>
									<li>Die kopierte URL in dem Feld hier einfügen und den Login-Button klicken.</li>
								</ol>
								<div class="form-row mb-1">
									<label for="weburl" class="col-md-4 col-form-label">"Page Not Found" URL:</label>
									<div class="col">
										<input class="form-control" type="text" name="weburl" id="weburl" required>
									</div>
								</div>
								
							</div>
							<div class="card-footer">
								<div class="form-row text-center">
									<div class="col">
										<button type="submit" class="btn btn-success" value="Login">Anmelden</button>
									</div>
								</div>
							</div>
						</form>
					</div>
					<!--
						<hr>
						<h3>Refresh Token</h3>
						<form method="post">
						<input type="hidden" name="go" value="refresh">
						Please enter the Bearer Refresh-Token:<br>
						<input name="token" size="100" required><input type="submit" value="Refresh">
						</form>
					-->
					<script>
					function teslaLogin () {
						teslaLogin = window.open("<?php echo gen_url($code_challenge, $state);?>", "TeslaLogin", "width=800,height=600,status=yes,scrollbars=yes,resizable=yes");
						teslaLogin.focus();
					}
					</script>

					<?php
				}

				if(isset($_REQUEST["go"])){
					switch($_REQUEST["go"]){
						case "login":
							$result = login($_POST["weburl"], $_POST["code_verifier"], $_POST["code_challenge"], $_POST["state"]);
							$resultJson = json_decode( $result, false );
							// var_dump( $resultJson );
							// echo "Success: " . $resultJson->{'success'} . "<br>";
							if($resultJson->{'success'} == 1){
								$message = json_decode( $resultJson->{'message'}, true );
								// var_dump( $message );
								// foreach( array_keys($message) as $key ){
								// 	echo "$key: " . $message[$key] . "<br>";
								// }
								// now construct a json object with the data we need
								$token = [
									"refresh_token" => $message['bearer_refresh_token'],
									"access_token"  => $message['access_token'],
									"expires_in"    => $message['expires_in'],
									"created_at"    => $message['created_at']
								];
								// echo json_encode( $token );
								$tokenFileP = fopen( $token_file, 'w' );
								fwrite( $tokenFileP, json_encode( $token ) );
								fclose( $tokenFileP );
								?>
									<div class="alert alert-success">
										Anmeldung erfolgreich!<br>
										Die erhaltenen Token wurden gespeichert. Sie können diese Seite jetzt schließen.
									</div>
								<?php
							} else {
								// var_dump( $resultJson->{'message'} );
								?>
									<div class="alert alert-danger">
										Anmeldung fehlgeschlagen!<br>
										Meldung des servers: "<?php echo $resultJson->{'message'} ?>"
									</div>
								<?php
							}
							break;
						case "cleanup":
							if(file_exists($cookie_file)){
								unlink( $cookie_file );
							}
							if(file_exists($token_file)){
								unlink( $token_file );
							}
							?>
								<div class="alert alert-success">
									Gespeicherte Anmeldedaten wurden entfernt. Sie können diese Seite jetzt schließen.
								</div>
							<?php
							break;
						default:
							html_login();
						break;
					}
				} else {
					html_login();
				}
			?>

		</div>  <!-- container -->
	</body>
</html>
