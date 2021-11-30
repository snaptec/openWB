/**
 * helper functions for cards display theme
 *
 * @author Michael Ortenstein
 * @author Lutz Bender
 */

/**
 * detect touch devices and map contextmenu (long press) to normal click
 */
$('body').on("contextmenu", function(event){
    if( ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0) ) {
        $(event.target).trigger("click"); // fire a click event
        event.preventDefault();
    }
});

function updateLabel(elementId) {
    /** @function updateLabel
     * sets the value-label (if exists) attached to the element to the element value
     * @param {string} elementId - the id of the element
     * @requires class:valueLabel assigned to the attached label
     */
    var element = $('#' + $.escapeSelector(elementId));
    var label = $('label[for="' + elementId + '"].valueLabel');
    if ( label.length == 1 ) {
        var suffix = label.data('suffix');
        var text = parseFloat(element.val()).toLocaleString(undefined, {maximumFractionDigits: 2});
        if ( suffix != '' ) {
            text += ' ' + suffix;
        }
        label.text(text);
    }
}

function setInputValue(elementId, value) {
    /** @function setInputValue
     * sets the value-label (if exists) attached to the element to the element value
     * @param {string} elementId - the id of the element
     * @param {string} value - the value the element has to be set to
     * if the element has data-attribute 'signcheckbox' the checkbox with the id of the attribute
     * will represent negative numbers by being checked
     */
    if ( !isNaN(value) ) {
        var element = $('#' + $.escapeSelector(elementId));
        var signCheckboxName = element.data('signcheckbox');
        var signCheckbox = $('#' + signCheckboxName);
        if ( signCheckbox.length == 1 ) {
            // checkbox exists
            if ( value < 0 ) {
                signCheckbox.prop('checked', true);
                value *= -1;
            } else {
                signCheckbox.prop('checked', false);
            }
        }
        element.val(value);
        if ( element.attr('type') == 'range' ) {
            updateLabel(elementId);
        }
    }
}

function getTopicToSendTo (elementId) {
    var element = $('#' + $.escapeSelector(elementId));
    var topic = element.data('topicprefix') + elementId;
    topic = topic.replace('/get/', '/set/');
    if (topic.includes('MaxPriceForCharging')) {
        topic = 'openWB/set/awattar/MaxPriceForCharging'
    }
    return topic;
}

function setToggleBtnGroup(groupId, option) {
    /** @function setToggleBtnGroup
     * sets the state of a button group
     * @param {string} groupId - the id of the button group
     * @param {string} option - the option the group buttons will be set to
     * @requires data-attribute 'option' (unique for group) assigned to every radio-btn
     */
    $('input[name="' + groupId + '"][data-option="' + option + '"]').prop('checked', true);
    $('input[name="' + groupId + '"][data-option="' + option + '"]').closest('label').addClass('active');
    // and uncheck all others
    $('input[name="' + groupId + '"]').not('[data-option="' + option + '"]').each(function() {
        $(this).prop('checked', false);
        $(this).closest('label').removeClass('active');
    });
    chargeLimitationOptionsShowHide($('#' + $.escapeSelector(groupId)), option)
}
