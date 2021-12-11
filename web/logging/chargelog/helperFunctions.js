/**
 * helper functions for lade log pages
 *
 * @author Lutz Bender
 */

/**
 * hideSection
 * add class 'hide' to element with selector 'section' in JQuery syntax
 * disables all contained input and select elements if 'disableChildren' is not set to false
**/
function hideSection(section, disableChildren=true) {
    $(section).addClass('hide');
    if(disableChildren) {
        updateFormFieldVisibility();
    }
}

/**
 * showSection
 * remove class 'hide' from element with selector 'section' in JQuery syntax
 * enables all contained input and select elements if 'enableChildren' is not set to false
**/
function showSection(section, enableChildren=true) {
    $(section).removeClass('hide');
    if(enableChildren) {
        updateFormFieldVisibility();
    }
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
