Das smart SOC Modul ist vom smartEQ Modul des iobroker inspiriert.
Der js code wurde in python implementiert und etwas vereinfacht.

Es wird in OAUTh ein Token Refresh durchgeführt.
Da alle Token nur 2 Stunden gültig sind und der Refresh mit gültigem refresh_token erfolgen muss,
sollten die Intervalle in der Modulkonfiguration weniger als 2 Stunden betragen.
90 Minuten im Standby und 10 Minuten während des Ladens haben sich im Test bewährt.

Wenn die Intervalle auf mehr als 2 Stunden konfiguriert sind, wird bei der nächsten Abfrage ein Login durchgeführt.
Das benötigt deutlich mehr Zeit und es können die Token anderer Sitzungen, z.B. der smart Control App,
ungültig werden und einen neuen Login benötigen mit Eingabe von User und Passwort.

