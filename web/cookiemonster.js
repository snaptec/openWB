/*
*
* Funktionen zur Verwaltung von Cookies
* für Auswahl des Theme
*
* 2019 Michael Ortenstein
* This file is part of openWB
*
*/

var cookieName = "openWBTheme";

// Cookie-Objekt
var themeCookie = {
    read () {
        // liest aus den Cookies das gewählte Theme und gibt dieses als
        // String zurück. Ist Cookie leer/nicht gesetzt oder Theme
        // nicht vorhanden, wird als Theme Standard gewählt
        var cookie = "";
        if (document.cookie.indexOf(cookieName) > -1) {
            // wenn ein Cookie für das Theme existiert, dieses lesen
            cookie = document.cookie.split(cookieName)[1].split("; ")[0].substr(1);
        }
        if (cookie == "") {
            // kein Cookie gefunden, dann Standard-Theme setzen
            cookie = "standard";
            this.write(cookie);
        }
        // prüfen, ob Theme existiert anhand index.html
        var reader = new XMLHttpRequest();
        var checkURL = window.location.protocol + "//" + window.location.host + "/openWB/web/themes/" + cookie + "/index.html";
        reader.open('get', checkURL, true);
        reader.onreadystatechange = checkReadyState;
        function checkReadyState() {
          if (reader.readyState === 4) {
            // prüfen, ob die Anforderung der index.html erfolg hatte
            if (!((reader.status == 200) || (reader.status === 0))) {
                // Theme nicht gefunden, letzte Chance Standard
                alert("Theme '"+cookie+"' konnte nicht gefunden werden!");
                cookie = "standard";
            }
          }
        }
        reader.send(null);
        // einmal Cookie schreiben, um Gültigkeit zu verlängern
        this.write(cookie);
        // und zurückgeben
        return cookie;
    },
    write : function (cookieValue) {
        // schreibt gewähltes Theme in Cookie
        //  Ablaufzeit = heute + 2 Jahre
        var d = new Date();
        d.setTime(d.getTime() + (2*365*24*60*60*1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = cookieName + "=" + cookieValue + "; " + expires;
    },
};
