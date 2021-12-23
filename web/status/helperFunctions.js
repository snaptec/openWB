/**
 * helper functions for setup-pages
 *
 * @author Michael Ortenstein
 * @author Lutz Bender
 */

/**
 * hideSection
 * add class 'hide' to element with selector 'section' in JQuery syntax
 * disables all contained input and select elements if 'disableChildren' is not set to false
**/
function hideSection(section, disableChildren=true) {
    $(section).addClass('hide');
    updateFormFieldVisibility();
}

/**
 * showSection
 * remove class 'hide' from element with selector 'section' in JQuery syntax
 * enables all contained input and select elements if 'enableChildren' is not set to false
**/
function showSection(section, enableChildren=true) {
    $(section).removeClass('hide');
    updateFormFieldVisibility();
}

/**
 * updateFormFields
 * checks every input and select element for a parent with class 'hide'
 * if there is a match, disable this element
**/
function updateFormFieldVisibility() {
    $('input').each(function() {
        if( $(this).closest('.hide').length == 0 ) {
            $(this).prop("disabled", false);
        } else {
            $(this).prop("disabled", true);
        }
    });
    $('select').each(function() {
        if( $(this).closest('.hide').length == 0 ) {
            $(this).prop("disabled", false);
        } else {
            $(this).prop("disabled", true);
        }
    });
}

var originalValues = {};  // holds all topics and its values received by mqtt as objects before possible changes made by user

var changedValuesHandler = {
    deleteProperty: function(obj, key, value) {
        delete obj[key];
        // if array is empty after delete, all send topics have been received with correct value
        // so redirect to main page
        // array is only filled by function getChangedValues!
        console.log("num changed values left: "+Object.keys(changedValues).length);
        if ( Object.keys(changedValues).length === 0 ) {
            console.log("done");
            window.location.href = './index.php';
        } else {
            return true;
        }
    }
}

var changedValues = new Proxy({}, changedValuesHandler);

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
    } else {
	var element = $('#' + elementId);
	element.val(value);
    }
}

function setToggleBtnGroup(groupId, option) {
    /** @function setInputValue
     * sets the value-label (if exists) attached to the element to the element value
     * @param {string} elementId - the id of the button group
     * @param {string} option - the option the group buttons will be set to
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

function sendValues() {
    /** @function sendValues
     * send all topic-value-pairs from valueList
     * @typedef {Object} topic-value-pair
     * @property {string} topic - the topic
     * @property {string} value - the value
     * @param {topic-value-pair} - the changed values and their topics
     * @requires global variable 'toBeSendValues'
     * @requires modal with id 'noValuesChangedInfoModal'
     */
    if ( !(Object.keys(changedValues).length === 0) ) {
        // there are changed values
        // so first disable buttons on page
        $('#saveSettingsBtn').prop('disabled', true);
        $('#modalDefaultsBtn').prop('disabled', true);
        // delay in ms between publishes
        var intervall = 200;
        // then send changed values

        Object.keys(changedValues).forEach(function(topic, index) {
            var value = this[topic].toString();
            setTimeout(function () {
                console.log("publishing changed value: "+topic+": "+value);
                publish(value, topic);
            }, index * intervall);
        }, changedValues);

    } else {
        $('#noValuesChangedInfoModal').modal();
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
    $('.btn-group-toggle, input[type="number"]:not(:disabled), input[type="text"]:not(:disabled), input[type="password"]:not(:disabled), input[type="range"]:not(:disabled), select:not(:disabled)').each(function() {
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
            if ( $('input[name="' + $(this).attr('id') + '"]:checked').attr('disabled') != 'disabled' ) {
                var value = $('input[name="' + $(this).attr('id') + '"]:checked').data('option');
            }
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
        if ( ( value != undefined ) && ( originalValues[topic] != value ) ) {
            topic = topic.replace('/get/', '/set/');
            changedValues[topic] = value;
            console.log("ChangedValue found: "+topic+": "+value);
        }
    });
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
