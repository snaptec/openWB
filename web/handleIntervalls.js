// aktiviert notwendige Intervalle wenn Browser-Tab sichtbar,
// deaktiviert, wenn Tab ausgeblendet
// sofortiger einmaliger Aufruf der übergebenen Funktion,
// wenn Intervall eingerichtet wird und wenn Broser-Tab von
// unsichtbar auf sichtbar wechselt
//
// Intervalle über mySetInterval anstelle setInterval einrichten:
// <intervallID> = mysetIntervall(<Funkionsname>);

var mySetInterval, myClearInterval;

(function() {
    var data = Object.create(null),
        id = 0;
        mySetInterval = function mySetInterval(func, time) {
            data[id] = {
                nativeID: setInterval(func, time),
                func: func,
                time: time
            };
            // übergebene Funktion sofort aufrufen... nicht bis erstes Intervall warten
            func();
            return id++;
        };
        myClearInterval = function myClearInterval(id) {
            if(data[id]) {
                clearInterval(data[id].nativeID);
                delete data[id];
            }
        };
        document.addEventListener('visibilitychange', function() {
            if(document.visibilityState == 'visible') {
                for(var id in data) {
                    // wenn wieder sichtbar, alle Funktionen auf Intervall setzen
                    data[id].nativeID = setInterval(data[id].func, data[id].time);
                    // und einmal sofort aufrufen
                    data[id].func();
                }
            } else {
                // wenn Tab nicht sichtbar, alle Intervalle löschen
                for(var id in data)
                    clearInterval(data[id].nativeID);
            }
        });
})();
