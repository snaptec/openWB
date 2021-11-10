<?php

class Battery_API {

	private $token_file_prefix = 'token';
	private $token_file_suffix = '.json';
	private $token_file = 'token.json';

	private $auth_api = 'https://customer.bmwgroup.com/gcdm/oauth/authenticate';
	// private $vehicle_api = 'https://www.bmw-connecteddrive.de/api/vehicle';
	// quick fix: .de url broken after 11.03.2021
	private $vehicle_api = 'https://www.bmw-connecteddrive.com/api/vehicle';

	private $auth;
	private $token;
	private $json;

	function __construct ( $chargepoint, $user, $password, $vin ) {

		$this->auth = array(
							"username" => $user,
							"password" => $password,
							"vehicle" => $vin
						);
		$this->token = $this->get_token();
		$this->json = $this->get_vehicle_data();

		$this->send_response_json();
	}


	function check_security() {
		if ( empty( $_SERVER['HTTP_REFERER'] ) OR strcmp( parse_url( $_SERVER['HTTP_REFERER'], PHP_URL_HOST ), $_SERVER['SERVER_NAME'] ) !== 0 ) {
			http_response_code( 403 ) && exit;
		}
	}


	function cache_remote_token( $token_data ) {
		file_put_contents(
			$this->token_file,
			json_encode( $token_data )
		);
	}


	function get_cached_token() {
		return json_decode(
			@file_get_contents(
				$this->token_file
			)
		);
	}


	function get_token() {
		// Get cached token
		if ( $cached_token_data = $this->get_cached_token() ) {
			if ( $cached_token_data->expires > time() ) {
				$token = $cached_token_data->token;
			}
		}

		// Get remote token
		if ( empty( $token ) ) {
			$token_data = $this->get_remote_token();
			$token = $token_data->token;

			$this->cache_remote_token( $token_data );
		}

		return $token;
	}


	function get_remote_token() {
		// Init cURL
		$ch = curl_init();

		// Set cURL options
		curl_setopt( $ch, CURLOPT_URL, $this->auth_api );
		curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, false );
		curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
		curl_setopt( $ch, CURLOPT_HEADER, true );
		curl_setopt( $ch, CURLOPT_NOBODY, true );
		curl_setopt( $ch, CURLOPT_COOKIESESSION, true );
		curl_setopt( $ch, CURLOPT_POST, true );
		curl_setopt( $ch, CURLOPT_HTTPHEADER, array( 'Content-Type: application/x-www-form-urlencoded' ) );
		curl_setopt( $ch, CURLOPT_POSTFIELDS, 'username=' . urlencode( $this->auth["username"]) . '&password=' . urlencode( $this->auth["password"]) . '&client_id=dbf0a542-ebd1-4ff0-a9a7-55172fbfce35&redirect_uri=https%3A%2F%2Fwww.bmw-connecteddrive.com%2Fapp%2Fdefault%2Fstatic%2Fexternal-dispatch.html&response_type=token&scope=authenticate_user%20fupo&state=eyJtYXJrZXQiOiJkZSIsImxhbmd1YWdlIjoiZGUiLCJkZXN0aW5hdGlvbiI6ImxhbmRpbmdQYWdlIn0&locale=DE-de' );

		// Exec curl request
		$response = curl_exec( $ch );

		// Close connection
		curl_close( $ch );

		// Extract token
		preg_match( '/access_token=([\w\d]+).*token_type=(\w+).*expires_in=(\d+)/', $response, $matches );

		// Check token type
		if ( empty( $matches[2] ) OR $matches[2] !== 'Bearer' ) {
			http_response_code( 424 ) && exit;
		}

		return (object) array(
			'token' => $matches[1],
			'expires' => time() + $matches[3]
		);
	}


	function get_vehicle_data() {
		// Init cURL
		$ch_1 = curl_init();
		$ch_2 = curl_init();

		// Set cURL options
		curl_setopt( $ch_1, CURLOPT_URL, $this->vehicle_api . '/dynamic/v1/' . $this->auth["vehicle"] . '?offset=-60' );
		curl_setopt( $ch_1, CURLOPT_HTTPHEADER, array( 'Content-Type: application/json' , 'Authorization: Bearer ' . $this->token ) );
		curl_setopt( $ch_1, CURLOPT_RETURNTRANSFER, true );
		curl_setopt( $ch_1, CURLOPT_FOLLOWLOCATION, true );

		curl_setopt( $ch_2, CURLOPT_URL, $this->vehicle_api . '/navigation/v1/' . $this->auth["vehicle"] );
		curl_setopt( $ch_2, CURLOPT_HTTPHEADER, array( 'Content-Type: application/json' , 'Authorization: Bearer ' . $this->token ) );
		curl_setopt( $ch_2, CURLOPT_RETURNTRANSFER, true );
		curl_setopt( $ch_2, CURLOPT_FOLLOWLOCATION, true );

		// Build the multi-curl handle
		$mh = curl_multi_init();
		curl_multi_add_handle( $mh, $ch_1 );
		curl_multi_add_handle( $mh, $ch_2 );

		// Execute all queries simultaneously
		$running = null;
		do {
			curl_multi_exec( $mh, $running );
		} while ( $running );

		// Close the handles
		curl_multi_remove_handle( $mh, $ch_1 );
		curl_multi_remove_handle( $mh, $ch_2 );
		curl_multi_close( $mh );

		// all of our requests are done, we can now access the results
		$response_1 = curl_multi_getcontent( $ch_1 );
		$response_2 = curl_multi_getcontent( $ch_2 );

		// Decode response
		$json = (object)array_merge(
			json_decode( $response_1, true )['attributesMap'],
			json_decode( $response_2, true )
		);

		// Exit if error
		if ( json_last_error() ) {
			http_response_code( 500 ) && exit;
		}

		return $json;
	}


	function send_response_json() {
		// Set JSON vars
		$attributes = $this->json;

		$updateTimestamp = $attributes->updateTime_converted_timestamp / 1000;

		if( date( 'I', $updateTimestamp ) == 1 ) {
			$updateTimestamp -= 3600;
		}

		$updateTime = date( 'd.m.Y H:i', $updateTimestamp );
		$electricRange = intval( $attributes->beRemainingRangeElectricKm );
		$chargingLevel = intval( $attributes->chargingLevelHv );
		$chargingActive = intval( $attributes->charging_status === 'CHARGINGACTIVE' );
		$chargingError = intval( $attributes->charging_status === 'CHARGINGERROR' );
		//$chargingTimeRemaining = intval( $attributes->chargingTimeRemaining );
		//$chargingTimeRemaining = ( $chargingTimeRemaining ? ( date( 'H:i', mktime( 0, $chargingTimeRemaining ) ) ) : '0:00' );

		$stateOfCharge = number_format( round( $attributes->soc, 2 ), 2, ',', '.');
		$stateOfChargeMax = number_format( round( $attributes->socmax, 2 ), 2, ',', '.');

		// Send Header
		//header('Access-Control-Allow-Origin: https://' . $_SERVER['SERVER_NAME'] );
		header('Content-Type: application/json; charset=utf-8');

		// Send JSON
		die(
			json_encode(
				array(
					'updateTime' => $updateTime,
					'electricRange' => $electricRange,
					'chargingLevel' => $chargingLevel,
					'chargingActive' => $chargingActive,
					'chargingError' => $chargingError,
					//'chargingTimeRemaining' => $chargingTimeRemaining,
					'stateOfCharge' => $stateOfCharge,
					'stateOfChargeMax' => $stateOfChargeMax
				)
			)
		);
	}
}

$shortopts = "c:u:p:v:";
$longopts = array( "chargepoint:", "username:", "password:", "vin:" );
$cliargs = getopt( $shortopts, $longopts );

if( array_key_exists( "chargepoint", $cliargs ) ){
	$chargepoint = $cliargs["chargepoint"];
} else if( array_key_exists( "c", $cliargs ) ) {
	$chargepoint = $cliargs["c"];
}
if( array_key_exists( "username", $cliargs ) ){
	$username = $cliargs["username"];
} else if( array_key_exists( "u", $cliargs ) ) {
	$username = $cliargs["u"];
}
if( array_key_exists( "password", $cliargs ) ){
	$password = $cliargs["password"];
} else if( array_key_exists( "p", $cliargs ) ) {
	$password = $cliargs["p"];
}
if( array_key_exists( "vin", $cliargs ) ){
	$vin = $cliargs["vin"];
} else if( array_key_exists( "v", $cliargs ) ) {
	$vin = $cliargs["v"];
}
new Battery_API( $chargepoint, $username, $password, $vin );
