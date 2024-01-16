Das smart SOC Modul ist vom smartEQ Modul des iobroker inspiriert.
Der js code wurde in python implementiert und etwas vereinfacht.

Das Modul unterstützt die Authentication mit Passwort oder 2-Factor-Authentication (2FA).
Die Passwort-Authentication wird benutzt wenn ein Passwort konfiguriert ist.
Wenn das Passwort leer ist, wird die 2FA benutzt, die in 2 Schritten durchgeführt wird.
Zu Beginn sind Passwort und PIN leer.
Das SOC-Modul fordert eine PIN (6-stellige Zahl) an.
Vom Authentication Server wird die PIN per email gesendet.
Die PIN ist vom Anwender in die Konfiguration des SOC-Moduls einzutragen.
Das SOC-Modul benutzt nach Speichern die PIN um die Authentication abzuschliessen.
Die PIN ist 15 Minuten gültig, daher ist dies zügig zu machen.


Für beide Methoden gilt:
Bei erfolgreicher Authentication wird vom Authentication Server ein refresh token und access token erzeugt.
Bei Ablauf des access token wird in OAUTh ein Token Refresh durchgeführt, der ein neues Paar token erzeugt.

Der access Token ist nur 2 Stunden gültig.
Der refresh Token ist länger gültig, ist aber nur ein mal nutzbar.
Daher muss der refresh token immer gespeichert werden wenn der access token ungültig ist.
Daher ist es empfohlen, die Intervalle in der Modulkonfiguration auf weniger als 2 Stunden zu setzen.
90 Minuten im Standby und 10 Minuten während des Ladens haben sich im Test bewährt.


