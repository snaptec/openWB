/**
 * functions to setup pv charging parameters via MQTT-messages
 *
 * required function setInputValue and setToggleBtnGroup defined in main pvconfig.html
 *
 * @author Michael Ortenstein
 */

function processMessages(mqttmsg, mqttpayload) {
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
        setInputValue(elementId, mqttpayload);
    } else if ( element.hasClass('btn-group-toggle') ) {
        setToggleBtnGroup(elementId, mqttpayload);
    } else {
        console.log(elementId + ' not found');
    }
}  // end processMessages
