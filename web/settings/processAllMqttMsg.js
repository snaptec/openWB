/**
 * processes mqtt messages
 *
 * @author Michael Ortenstein
 */

function checkAllSaved(topic, value) {
    /** @function checkAllSaved
     * checks if received value equals the last saved and removes key from array
     * @param {string} topic - the complete mqtt topic
     * @param {string} value - the value for the topic
     * @requires global var:changedValues - is declared with proxy in helperFunctions.js
     */
    topic = topic.replace('/get/', '/set/');
    if ( changedValues.hasOwnProperty(topic) && changedValues[topic] == value ) {
        // received topic-value-pair equals one that was send before
        delete changedValues[topic];  // delete it
        // proxy will initiate redirect to main page if array is now empty
    }
};

function processMessages(mqttmsg, mqttpayload) {
    /** @function processMessages
     * sets input fields, range sliders and button-groups to values by mqtt
     * @param {string} mqttmsg - the complete mqtt topic
     * @param {string} mqttpayload - the value for the topic
     * @requires function:setInputValue - is declared in pvconfig.html
     * @requires function:setToggleBtnGroup  - is declared in pvconfig.html
     */
    // console.log("new message: "+mqttmsg+": "+mqttpayload);
    checkAllSaved(mqttmsg, mqttpayload);
    // last part of topic after /
    var topicIdentifier = mqttmsg.substring(mqttmsg.lastIndexOf('/')+1);
    // check if topic contains subgroup like /lp/1/
    var topicSubGroup = mqttmsg.match( /(\w+)\/(\d\d?)\// );
    if ( topicSubGroup != null ) {
        // topic might be for one of several subgroups
        // topicSubGroup[0]=complete subgroup, [1]=suffix=first part between //, [1]=index=second part between //
        var suffix = topicSubGroup[1].charAt(0).toUpperCase() + topicSubGroup[1].slice(1);  // capitalize suffix
        var index = topicSubGroup[2];
        var elementId = topicIdentifier + suffix + index;
    } else {
        // no subgroup so everything after last '/' might be the id
        var elementId = topicIdentifier;
    }
    // Could be a main on / off switch, check visibility func on main settings page
    visibiltycheck(elementId, mqttpayload);
    var element = $('#' + elementId);
    if ( element.attr('type') == 'number' || element.attr('type') == 'text' || element.attr('type') == 'url' || element.attr('type') == 'password' || element.attr('type') == 'range' ) {
        originalValues[mqttmsg] = mqttpayload;
        setInputValue(elementId, mqttpayload);
    } else if ( element.hasClass('btn-group-toggle') ) {
        originalValues[mqttmsg] = mqttpayload;
        setToggleBtnGroup(elementId, mqttpayload);
    } else if ( element.is('select') ) {
        originalValues[mqttmsg] = mqttpayload;
        setInputValue(elementId, mqttpayload);
    } else {
        console.debug(elementId + ' not found');
    }
}  // end processMessages
