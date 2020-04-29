/**
 * processes mqtt messages
 *
 * @author Michael Ortenstein
 */

var originalValues = {};  // holds all topics and its values received by mqtt as objects before possible changes made by user

function processMessages(mqttmsg, mqttpayload) {
    /** @function processMessages
     * sets input fields, range sliders and button-groups to values by mqtt
     * @param {string} mqttmsg - the complete mqtt topic
     * @param {string} mqttpayload - the value for the topic
     * @requires function:setInputValue - is declared in pvconfig.html
     * @requires function:setToggleBtnGroup  - is declared in pvconfig.html
     */
    // last part of topic after /
    var topicIdentifier = mqttmsg.substring(mqttmsg.lastIndexOf('/')+1);
    // check if topic contains subgroup like /lp/1/
    var topicSubGoup = mqttmsg.match( /(\w+)\/(\d\d?)\// );
    if ( topicSubGoup != null ) {
        // topic might be for one of several subgroups
        // topicSubGoup[0]=complete subgroup, [1]=first part between //, [1]=second part between //
        var elementId = topicIdentifier + topicSubGoup[1] + topicSubGoup[2];
    } else {
        // no subgroup so everything after last '/' might be the id
        var elementId = topicIdentifier;
    }
    var element = $('#' + elementId);
    if ( element.attr('type') == 'number' || element.attr('type') == 'text' || element.attr('type') == 'range' ) {
        originalValues[mqttmsg] = mqttpayload;
        setInputValue(elementId, mqttpayload);
    } else if ( element.hasClass('btn-group-toggle') ) {
        originalValues[mqttmsg] = mqttpayload;
        setToggleBtnGroup(elementId, mqttpayload);
    } else {
        console.log(elementId + ' not found');
    }
}  // end processMessages
