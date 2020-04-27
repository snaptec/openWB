/**
 * helper functions for setup-pages
 *
 * @author Michael Ortenstein
 */

var originalValues = {};  // holds all topics and its values received by mqtt as objects before possible changes made by user

function updateLabel(elementId) {
    /** @function updateLabel
     * sets the value-label (if exists) attached to the element to the element value
     * @param {string} elementId - the id of the element
     * @requires class:valueLabel assigned to the attached label
     */
    var element = $('#' + elementId);
    var label = $('label[for="' + element.attr('id') + '"].valueLabel');
    if ( label.length == 1 ) {
        var suffix = label.attr('suffix');
        var text = element.val();
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
        var element = $('#' + elementId);
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

function setToggleBtnGroup(groupId, option) {
    /** @function setInputValue
     * sets the value-label (if exists) attached to the element to the element value
     * @param {string} elementId - the id of the button group
     * @param {string} option - the option the group btns will be set to
     * @requires data-attribute 'option' (unique for group) assigned to every radio-btn
     */
    $('input[name=' + groupId + '][data-option="' + option + '"]').prop('checked', true);
    $('input[name=' + groupId + '][data-option="' + option + '"]').closest('label').addClass('active');
    // and uncheck all others
    $('input[name=' + groupId + '][data-option!="' + option + '"]').each(function() {
        $(this).prop('checked', false);
        $(this).closest('label').removeClass('active');
    });
}

function sendValues(valueList) {
    /** @function sendValues
     * send all topic-value-pairs from valueList
     * @typedef {Object} topic-value-pair
     * @property {string} topic - the topic
     * @property {string} value - the value
     * @param {topic-value-pair} - the changed values and their topics
     */
    if ( !(Object.keys(valueList).length === 0 && valueList.constructor === Object) ) {
        // there are changed values
        Object.keys(valueList).forEach(function(topic) {
            var value = this[topic].toString();
            publish(value, topic);
        }, valueList);
    }
}

function getChangedValues() {
    /** @function getChangedValues
     * gets all topic-value-pairs changed by the user and sets topic from /get/ to /set/
     * @typedef {Object} topic-value-pair
     * @property {string} topic - the topic
     * @property {string} value - the value
     * @return {topic-value-pair} - the changed values and their topics
     */
    var allChanged = {};
    $('.btn-group-toggle, input[type="number"], input[type="text"], input[type="range"]').each(function() {
        var topicPrefix = $(this).data('topicprefix');
        var topicSubGroup = $(this).data('topicsubgroup');
        if ( typeof topicSubGroup == 'undefined' ) {
            // if no data-attribute for subgroup like /lp/1/ exists
            // topicIdentifier is the unique element id
            topicSubGroup = '';
            var topicIdentifier = $(this).attr('id');
        } else {
            // if data-attribute for subgroup like /lp/1/ exists
            // topicIdentifier is the non-unique element name
            var topicIdentifier = $(this).attr('name');
        }
        if ( $(this).hasClass('btn-group-toggle') ) {
            var value = $('input[name="' + $(this).attr('id') + '"]:checked').data('option');
        } else {
            var value = $(this).val();
            if ( $(this).attr('type') == 'number' || $(this).attr('type') == 'text' ) {
                // check if sign checkbox exists and adjust value accordingly
                var signCheckboxName = $(this).data('signcheckbox');
                var signCheckbox = $('#' + signCheckboxName);
                if ( signCheckbox.is(':checked') && !isNaN(value) ) {
                    // checkbox exists and is checked
                    value *= -1;
                }
            }
        }
        var topic = topicPrefix + topicSubGroup + topicIdentifier;
        if ( originalValues[topic] != value ) {
            topic = topic.replace('/get/', '/set/');
            allChanged[topic] = value;
        }
    });
    return allChanged;
}

function setToDefaults() {
    /** @function setToDefaults
     * sets all inputs and button-groups to their default value
     */
     $('input[type="number"], input[type="text"], input[type="range"]').each(function() {
         // first all number-field and range sliders
         var defaultValue = $(this).data('default');
         if ( typeof defaultValue !== 'undefined' ) {
             setInputValue($(this).attr('id'), defaultValue);
         }
     });
     $('.btn-group-toggle').each(function() {
         // then all toggle btn-groups
         var defaultValue = $(this).data('default');
         if ( typeof defaultValue !== 'undefined' ) {
             setToggleBtnGroup($(this).attr('id'), defaultValue);
         }
     });
}

function formatToNaturalNumber(element) {
    /** @function formatToNaturalNumber
     * validation of user input so only natural numbers can be typed into field
     * @param {object} element - the input element
     * @requires max value set up for input field properly
     */
     if ( element.value.length > 0 ) {
         element.value = parseInt(element.value.replace(/[^0-9.-]/g,'').replace(/(\..*)\./g, '$1'));
     }
     var max = $(element).attr('max');
     if ( typeof max !== 'undefined' && !isNaN(max) && parseInt(element.value) > max ) {
         element.value = max;
     }
}
