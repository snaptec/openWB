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
				// https://github.com/timdorr/tesla-api/discussions/288 - https://github.com/timdorr/tesla-api/discussions/296

				$tesla_api_oauth2 = 'https://auth.tesla.com/oauth2/v3';
				$tesla_api_redirect = 'https://auth.tesla.com/void/callback';
				$tesla_api_owners = 'https://owner-api.teslamotors.com/oauth/token';
				$tesla_api_code_vlc = 86;
				$cid = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384";
				$cs = "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"; 
				$user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.216 Mobile/15E148 Safari/604.1"; //"Mozilla/5.0 (Linux; Android 9.0.0; VS985 4G Build/LRX21Y; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36";

				// openWB specific part
				$chargepoint = ( $_REQUEST['chargepoint'] ? $_REQUEST['chargepoint'] : "1" );
				$cookie_file = $_SERVER['DOCUMENT_ROOT']."/openWB/ramdisk/tesla-cookies.lp".$chargepoint;
				$token_file = __DIR__."/tokens.lp".$chargepoint;

				function tesla_connect($url, $returntransfer=1, $referer="", $http_header="", $post="", $need_header=0, $cookies="", $timeout = 10){
					global $cookie_file;

					if(!empty($post)) { $cpost = 1; } else { $cpost = 0; }
					if(is_array($http_header)) { $chheader = 1; } else { $chheader = 0; }

					$ch = curl_init();
					curl_setopt($ch, CURLOPT_URL, $url);
					curl_setopt($ch, CURLOPT_RETURNTRANSFER, $returntransfer);
					curl_setopt($ch, CURLOPT_TIMEOUT, $timeout);
					curl_setopt($ch, CURLOPT_HEADER, $need_header);
					curl_setopt($ch, CURLOPT_POST, $cpost);
					curl_setopt($ch, CURLOPT_FRESH_CONNECT, 1);
					curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
					curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
					curl_setopt($ch, CURLOPT_COOKIEFILE, $cookie_file); // set cookie file to given file
					curl_setopt($ch, CURLOPT_COOKIEJAR, $cookie_file); // set same file as cookie jar

					if(!empty($referer)) { curl_setopt($ch, CURLOPT_REFERER, $referer); }

					if($chheader == 1) { curl_setopt($ch, CURLOPT_HTTPHEADER, $http_header); }

					if($cpost == 1) { curl_setopt($ch, CURLOPT_POSTFIELDS, $post); }

					if(!empty($cookies)) { curl_setopt($ch, CURLOPT_COOKIE, $cookies); }

					if (defined('CURL_SSLVERSION_MAX_TLSv1_2')) curl_setopt ($ch, CURLOPT_SSLVERSION,CURL_SSLVERSION_MAX_TLSv1_2); // FM - force tls1.2

					$response = curl_exec($ch);
					$header = curl_getinfo($ch);
					curl_close($ch);

					return array("response" => $response, "header" => $header);
				}

				function tesla_captcha(){
					global $user_agent;
					$http_header = array('Content-Type: application/x-www-form-urlencoded', 'User-Agent: '.$user_agent, 'Origin: https://auth.tesla.com');
					$captcha = tesla_connect("https://auth.tesla.com/captcha", 1, "https://auth.tesla.com/", $http_header, "", 0);
					// $captcha = file_get_contents("https://auth.tesla.com/captcha");
					$convert = base64_encode($captcha["response"]);
					$img = "data:image/svg+xml;base64,".$convert;
					return $img;
				}

				function return_msg($code, $msg){
					return json_encode(array("success" => $code, "message" => $msg));
				}

				function tesla_oauth2_login($email, $password, $captcha, $mfa_code=""){
					global $tesla_api_oauth2, $tesla_api_redirect, $tesla_api_owners, $tesla_api_code_vlc, $cid, $cs, $user_agent;
					ob_start();

					if(empty($email)) { return return_msg(0, "Please enter your E-Mailaddress"); }
					if(empty($password)) { return return_msg(0, "Please enter your Password"); }
					if(empty($captcha)) { return return_msg(0, "Please enter the Captcha-Code"); }

					// Okay, that is the initial for the challance...

					$code_verifier = substr(hash('sha512', mt_rand()), 0, $tesla_api_code_vlc);
					$code_challenge = rtrim(strtr(base64_encode($code_verifier), '+/', '-_'), '='); 
					
					$state = rtrim(strtr(base64_encode(substr(hash('sha256', mt_rand()), 0, 12)), '+/', '-_'), '='); 

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

					$url = $tesla_api_oauth2."/authorize?".http_build_query($datas);

					$http_header = array('User-Agent: '.$user_agent);
					$response = tesla_connect($url, 1, "", $http_header, "", 1, "");



					$headers = [];
					$cookie = "";
					$data = explode("\n", rtrim($response["response"]));
					$headers['status'] = $data[0];
					array_shift($data);

					foreach($data as $part){
						$head = explode(":",$part,2);

						if ( !isset($head[1]) ) { $head[1] = null; }
							$headers[trim($head[0])] = trim($head[1]);


						if (trim($head[0]) == "Set-Cookie" OR trim($head[0]) == "set-cookie"){
							$cookie .= trim($head[1]).";";
						}
					}

					$cookie = substr($cookie, 0, -1);


					// Catch the _csrf, etc...
					$re = '/<input (.*) name="_csrf" value="(.*)"/m';
					preg_match_all($re, $response["response"], $matches, PREG_SET_ORDER, 0);

					$re = '/<input (.*) name="transaction_id" value="(.*)"/m';
					preg_match_all($re, $response["response"], $matches2, PREG_SET_ORDER, 0);

					$re = '/<input (.*) name="_phase" value="(.*)"/m';
					preg_match_all($re, $response["response"], $matches3, PREG_SET_ORDER, 0);

					$re = '/<input (.*) name="_process" value="(.*)"/m';
					preg_match_all($re, $response["response"], $matches4, PREG_SET_ORDER, 0);

					$re = '/<input (.*) name="cancel" value="(.*)"/m';
					preg_match_all($re, $response["response"], $matches5, PREG_SET_ORDER, 0);


					if(empty($matches[0][2]) OR empty($matches2[0][2]))
					{
					// Server has blocked your request, please try it again
					return return_msg(0, "Server has blocked your request, please try it again");
					}

					unset($response);
					
					// We try now the login, i hope, it's working :-)
					$http_header = array('Content-Type: application/x-www-form-urlencoded', 'User-Agent: '.$user_agent, 'Origin: https://auth.tesla.com', 'Cookie: '.$cookie);
					$post = http_build_query(array("_csrf" => $matches[0][2], "_phase" => "authenticate", "_process" => 1, "transaction_id" => $matches2[0][2], "cancel" => "", "identity" => $email, "credential" => $password, 'captcha' => $captcha));
					$response = tesla_connect($url, 0, $url, $http_header, $post, 0, $cookie); // $url
				
					if($response["header"]["http_code"] == 401) { ob_get_clean(); return return_msg(0, "Login fail! Username and/or Password wrong!"); }


					// MFA is required... let the fun beginn :-D
					$main_request = $response["header"]["http_code"];
					if($main_request == 200) 
					{
						// if(empty($mfa_code)) { ob_get_clean(); return return_msg(0, "Please enter the MFA Code or the Captcha Code is wrong!"); }

						unset($response);
						// Get the MFA Devices 
						$http_header = array('X-Requested-With: XMLHttpRequest', 'Content-Type: application/json; charset=utf-8', 'Accept: application/json', 'User-Agent: '.$user_agent, 'Origin: https://auth.tesla.com', 'Cookie: '.$cookie);
						$response = tesla_connect($tesla_api_oauth2."/authorize/mfa/factors?transaction_id=".$matches2[0][2], 1, $url, $http_header, "", 0, $cookie);
						var_dump($response);
						$factor_id = json_decode($response["response"], true);
						// We use the first MFA Device [0]
						$factor_device = $factor_id["data"][0]["id"];

						// if(empty($factor_device)) { ob_get_clean(); return return_msg(0, "Don't find the first MFA Device (if MFA needed, if not then is the Captcha Code wrong!"); }

						if(!empty($mfa_code) AND !empty($factor_device))
						{
							// Now, we are verify us
							unset($response);
							$http_header = array('Content-Type: application/json', 'User-Agent: '.$user_agent, 'Origin: https://auth.tesla.com', 'Cookie: '.$cookie);
							$post = json_encode(array("transaction_id" => $matches2[0][2], "factor_id" => $factor_device, "passcode" => $mfa_code));
							$response = tesla_connect($tesla_api_oauth2."/authorize/mfa/verify", 1, $url, $http_header, $post, 0, $cookie);

							$verify = json_decode($response["response"], true);
							
							if($verify["data"]["valid"] == true)
							{
								// And now, we try now receive the code
								unset($response);
								$http_header = array('Content-Type: application/x-www-form-urlencoded', 'User-Agent: '.$user_agent, 'Origin: https://auth.tesla.com', 'Cookie: '.$cookie);
								$post = http_build_query(array("transaction_id" => $matches2[0][2]));
								$response = tesla_connect($url, 1, $url, $http_header, $post, 0, $cookie);
							} else {
								ob_get_clean(); return return_msg(0, "Verify unsuccessful");
							}
						}
					}


					if($main_request == 200 AND empty($factor_device)) 
					{
						ob_get_clean();
						return return_msg(0, "It's looks, that the Captcha is wrong");
					}


					// Okay, if with or without MFA, this is the point, if we receive the code
					if($response["header"]["http_code"] == 302)
					{
						$code = explode($tesla_api_redirect.'?code=', $response["header"]["redirect_url"])[1];
						$code = explode("&", $code)[0];
					} else {
						ob_get_clean(); 
						return return_msg(0, "Something is wrong ... Http Header is not 302");
					}

					if(empty($code)) { ob_get_clean(); return return_msg(0, "Something is wrong ... Code not exists"); }

					// Get the Bearer token
					unset($response);
					$http_header = array('Content-Type: application/json', 'Accept: application/json', 'User-Agent: '.$user_agent, 'Cookie: '.$cookie);
					$post = json_encode(array("grant_type" => "authorization_code", "client_id" => "ownerapi", "code" => $code, "code_verifier" => $code_verifier, "redirect_uri" => $tesla_api_redirect));
					$response = tesla_connect($tesla_api_oauth2."/token", 1, $url, $http_header, $post, 0, $cookie);

					$token_res = json_decode($response["response"], true);
					$bearer_token = $token_res["access_token"];
					$refresh_token = $token_res["refresh_token"];

					if(empty($bearer_token)) { ob_get_clean(); return return_msg(0, "Bearer Token issue"); }

					// Final Step
					unset($response);
					$http_header = array('Authorization: Bearer '.$bearer_token, 'Content-Type: application/json');
					$post = json_encode(array("grant_type" => "urn:ietf:params:oauth:grant-type:jwt-bearer", "client_id" => $cid, "client_secret" => $cs));
					$response = tesla_connect($tesla_api_owners, 1, "", $http_header, $post, 0);

					$tokens = json_decode($response["response"], true);

					if(empty($tokens['access_token'])) { ob_get_clean(); return return_msg(0, "Token issue"); }

					$tokens["bearer_token"] = $bearer_token;
					$tokens["bearer_refresh_token"] = $refresh_token;
					$return_message = json_encode($tokens);

					// Output
					ob_get_clean();
					return return_msg(1, $return_message);
				}

				function tesla_oauth2_refresh($brt){
					global $tesla_api_oauth2, $tesla_api_redirect, $tesla_api_owners, $tesla_api_code_vlc, $cid, $cs;

					if(empty($brt)) { return return_msg(0, "Please enter the Bearer Refresh Token"); }

					// Get the Bearer token
					$http_header = array('Content-Type: application/json', 'Accept: application/json');
					$post = json_encode(array("grant_type" => "refresh_token", "client_id" => "ownerapi", "client_secret" => $cs, "refresh_token" => $brt, "scope" => "openid email offline_access"));
					$response = tesla_connect($tesla_api_oauth2."/token", 1, "https://auth.tesla.com/", $http_header, $post, 0);

					var_dump($response);

					$token_res = json_decode($response["response"], true);
					$bearer_token = $token_res["access_token"];
					$refresh_token = $token_res["refresh_token"];


					if(empty($bearer_token)) { return return_msg(0, "Bearer Token issue"); }

					// Final Step
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

				function html(){
					global $cookie_file;
					global $chargepoint;
					$captcha = tesla_captcha();
					?>
						<div class="card border-secondary">
							<form method="post">
								<div class="card-header bg-secondary">
									Login bei Tesla (Ladepunkt <?php echo $chargepoint; ?>)
								</div>
								<div class="card-body">
									<input type="hidden" name="go" value="login">
									<div class="form-group">
										<div class="form-row mb-1">
											<label for="username" class="col-md-4 col-form-label">E-Mail</label>
											<div class="col">
												<input class="form-control" type="email" required name="email" id="username" value="<?php echo ($_REQUEST['email'] ? $_REQUEST['email'] : '') ?>">
												<span class="form-text small">
													Email Adresse des Tesla Logins.
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="password" class="col-md-4 col-form-label">Passwort</label>
											<div class="col">
												<input class="form-control" type="password" required name="pwd" id="password" value="">
												<span class="form-text small">
													Password des Tesla Logins. Das Passwort wird nur bei der ersten Einrichtung verwendet. Sobald die Anmeldung erfolgreich war, wird die Anmeldung über Token geregelt.
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="mfapasscode" class="col-md-4 col-form-label">MFA-PassCode</label>
											<div class="col">
												<input class="form-control" type="password" name="mfa" id="mfapasscode" value="">
												<span class="form-text small">
													Optionaler PassCode für eine aktivierte 2-Faktor-Anmeldung. Der PassCode wird nur benötigt, wenn noch keine Token vorhanden sind. Nach erfolgreicher Anmeldung wid der PassCode entfernt.
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="captcha" class="col-md-4 col-form-label">Captcha-Code</label>
											<div class="col">
												<img src="<?php echo $captcha; ?>" alt="captcha"><br>
												<input class="form-control" type="text" required name="captcha" id="captcha" value="">
												<span class="form-text small">
													Bitte die Zeichen aus dem Captcha Bild eingeben.
												</span>
											</div>
										</div>
									</div>
								</div>
								<div class="card-footer">
									<div class="form-row text-center">
										<div class="col">
											<button type="submit" class="btn btn-success" value="Get Token">Anmelden</button>
										</div>
									</div>
								</div>
							</form>
						</div>
					<?php
				}

				if(isset($_REQUEST["go"])){
					switch($_REQUEST["go"]){
						case "login":
							$result = tesla_oauth2_login($_REQUEST["email"], $_REQUEST["pwd"], $_REQUEST["captcha"], $_REQUEST["mfa"]);
							// echo $result;
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
							unlink( $cookie_file );
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
							html();
						break;
					}
				} else {
					html();
				}
			?>
		</div>  <!-- container -->
	</body>
</html>
