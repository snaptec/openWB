<?php


/**
 * Support samesite cookie flag in both php 7.2 (current production) and php >= 7.3 (when we get there)
 * From: https://github.com/GoogleChromeLabs/samesite-examples/blob/master/php.md and https://stackoverflow.com/a/46971326/2308553 
 *
 * @see https://www.php.net/manual/en/function.setcookie.php
 *
 * @param string $name
 * @param string $value
 * @param int $expire
 * @param string $path
 * @param string $domain
 * @param bool $secure
 * @param bool $httponly
 * @param string $samesite
 * @return void
 */
function setCookieSameSite(
    string $name, string $value,
    int $expire, string $path, string $domain,
    bool $secure, bool $httponly, string $samesite = 'None'
) {
    if (PHP_VERSION_ID < 70300) {
        setcookie($name, $value, $expire, $path . '; samesite=' . $samesite, $domain, $secure, $httponly);
        return;
    }
    setcookie($name, $value, [
        'expires' => $expire,
        'path' => $path,
        'domain' => $domain,
        'samesite' => $samesite,
        'secure' => $secure,
        'httponly' => $httponly,
    ]);
}




	$themeCookie = $_GET['theme'];
	$expire = time()+(60*60*24*365*2);  // expiring-date to now + 2 years
	setCookieSameSite('openWBTheme', $themeCookie, $expire, '/openWB','',false,false','Lax');	
?>
