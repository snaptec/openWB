/**
 * Functions to update graph and gui values via MQTT-messages
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 * @author Lutz Bender
 */

function reloadDisplay() {
    /** @function reloadDisplay
     * triggers a reload of the current page
     */
    // wait some seconds to allow other instances receive this message
    console.log("reloading display...");
    setTimeout(function(){
        publish( "0", "openWB/set/system/reloadDisplay" );
        // wait again to give the broker some time and avoid a reload loop
        setTimeout(function(){
            location.reload();
        }, 2000);
    }, 2000);
}

function handlevar(mqttmsg, mqttpayload) {
	//console.log("Topic: "+mqttmsg+" Message: "+mqttpayload);
	// receives all messages and calls respective function to process them
	if ( mqttmsg.match( /^openwb\/system\//i) ) { processSystemMessages(mqttmsg, mqttpayload); }
}  // end handlevar

function processSystemMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
	if ( mqttmsg == 'openWB/system/reloadDisplay' ) {
		if( mqttpayload == '1' ){
			reloadDisplay();
		}
	}
}
