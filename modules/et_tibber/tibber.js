/**
 * Functions to retrieve and process data from Tibber API
 *
 * @author Michael Ortenstein
 */

const tibberAPI = "https://api.tibber.com/v1-beta/gql";

function readTibberAPI(tibberToken, tibberQuery) {
    /**
     * calls Tibber-API as promise returns data or error-message
     * @function readTibberAPI
     * @author Michael Ortenstein
     * @param {string} tibberToken
     * @param {string} tibberQuery
     * @returns {Promise} Promise object represents the result of the ajax-query
     */

    return new Promise((resolve, reject) => {
        $.ajax({
            type: "POST",
            url: tibberAPI,
            headers: {
                "Authorization": "Bearer " + tibberToken,
                "Content-Type": "application/json"
            },
            data: tibberQuery,
            timeout: 4000
        })
        .done (function (data) {
            if ( typeof data?.errors === "undefined" ) {
                // nor errors in API response
                resolve(data);
            } else {
                // got an API response but with an error-message
                reject("Interner Tibber-API-Fehler: " + data.errors[0].message);
            }
        })
        .fail ( function (error) {
            try {
                var errorJSON = JSON.parse(error.responseText);
            } catch (e) {
                // not an API-error, so just return error code and text
                reject(error.statusText + " " + error.status);
                return;
            }
            // error includes API-error-message
            if ( typeof errorJSON?.errors === "undefined" ) {
                // no error-message, so just return error code and text
                reject(error.statusText + " " + error.status);
            } else {
                // return detailed error-message
                reject(error.statusText + " " + error.status + ": "+ errorJSON.errors[0].message);
            }
        });
    });
}

function createXLabel(dateFrom, dateTo){
    /**
     * convert date in suitable label for chart x-axis
     *
     * @function createXLabel
     * @author Michael Ortenstein
     * @param {string} dateFrom as date string
     * @param {string} dateTo as date string
     * @returns {string} label as prettified date
     */
    var dateFromObj = new Date(dateFrom);
    var dateToObj = new Date(dateTo);
    var result = dateFromObj.getHours();
    if (!isNaN(dateToObj.getHours())) {
        result += " - " + dateToObj.getHours();
    } else {
        var theDate = new Date();  // now
        var dateIsToday = dateFromObj.getYear() == theDate.getYear() && dateFromObj.getMonth() == theDate.getMonth() && dateFromObj.getDate() == theDate.getDate();
        if ( !dateIsToday ) {
            theDate.setDate(theDate.getDate() + 1);  // set date to tomorrow
            var dateIsTomorrow = dateFromObj.getYear() == theDate.getYear() && dateFromObj.getMonth() == theDate.getMonth() && dateFromObj.getDate() == theDate.getDate();
            if ( dateIsTomorrow ) {
                result = 'morgen ' + result;
            } else {
                result = dateFromObj.getDate() + '.' + dateFromObj.getMonth() + '.' + dateFromObj.getFullYear() + ', ' + result;
            }
        }
    }
    result += " Uhr";
    return result;
}


function convertToLocale(number, unit){
    /**
     * convert float umber to locale with 2 digits and add unit
     * if not a number return "--"
     *
     * @function convertToLocale
     * @author Michael Ortenstein
     * @param {float} number
     * @param {string} unit
     * @returns {string} converted number
     */
    var converted = '--';
    if (!isNaN(number)) {
        converted = parseFloat(number).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' ' + unit;
    }
    return converted.trim();
}

function fillCardAllgemein(response){
    /**
     * fills the card "Allgemein" with data from tibber response
     *
     * @function fillCardAllgemein
     * @author Michael Ortenstein
     * @param {object} tibberResponse as JSON-object
     */
    var homeData = response?.data?.viewer?.home?.address;
    var homeOwnerName = response?.data?.viewer?.name;
    if (typeof homeOwnerName !== 'undefined') {
        $('#name').text(homeOwnerName);
    }
    if (typeof homeData !== 'undefined') {
        $('#street').text(homeData.address1);
        $('#city').text(homeData.postalCode + ' ' + homeData.city);
    }
}

function fillCardStrompreis(response){
    /**
     * fills the card "Strompreis" with data from tibber response
     *
     * @function fillCardStrompreis
     * @author Michael Ortenstein
     * @param {object} tibberResponse as JSON-object
     */
    const options = { weekday: 'short', year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', timeZoneName: 'short' };
    var priceCurrentData = response?.data?.viewer?.home?.currentSubscription?.priceInfo?.current;
    var priceTodayData = response?.data?.viewer?.home?.currentSubscription?.priceInfo?.today;
    var priceTomorrowData = response?.data?.viewer?.home?.currentSubscription?.priceInfo?.tomorrow;
    var labels = [];
    var data = [];

    if (typeof priceCurrentData !== 'undefined') {
        var startsAt = new Date(priceCurrentData.startsAt);
        $('#currentPrice').text(convertToLocale((priceCurrentData.total * 100), 'ct/kWh'));
        $('#currentEnergyPrice').text(convertToLocale((priceCurrentData.energy * 100), 'ct/kWh'));
        $('#currentTax').text(convertToLocale((priceCurrentData.tax * 100), 'ct/kWh'));
        $('#currentValidSince').text(startsAt.toLocaleDateString(undefined, options));
        if (typeof priceTomorrowData !== 'undefined') {
            $('#noPricechartDiv').hide();
            // get current timestamp but at full hour
            var now = new Date;
            now.setMinutes(0, 0, 0);

            // chart should beginn at current hour, so
            // copy only prices at or after full hour in arrays for the chart
            for (i=0; i<priceTodayData.length; i++) {
                var startsAtDate = new Date(priceTodayData[i].startsAt);
                if (startsAtDate.valueOf() >= now.valueOf()){
                    data.push((priceTodayData[i].total*100).toFixed(2));
                    labels.push(createXLabel(priceTodayData[i].startsAt));
                }
            }
            for (i=0; i<priceTomorrowData.length; i++) {
                data.push((priceTomorrowData[i].total*100).toFixed(2));
                labels.push(createXLabel(priceTomorrowData[i].startsAt));
            }
            // create chart
            loadElectricityPricechart(labels, data);
        } else {
            $('#electricityPricechartCanvasDiv').hide();
        }
    }
}

function fillCardTagesbezug(response, consumptionDayDate){
    /**
     * fills the card "Tagesverbrauch" with data from tibber response
     *
     * @function fillCardTagesbezug
     * @author Michael Ortenstein
     * @param {object} tibberResponse as JSON-object
     * @param {object} consumptionDayDate as date-object
     */
    const options = { weekday: 'short', year: 'numeric', month: 'numeric', day: 'numeric' };
    var consumptionHourly = response?.data?.viewer?.home?.cons_hourly?.nodes;
    var totalConsumptionDay = 0;
    var totalCostsDay = 0;
    var labels = [];
    var dataConsumption = [];
    var dataPrice = [];

    if (typeof consumptionHourly !== 'undefined') {
        // filter todays hours
        consumptionHourly = consumptionHourly.filter(function (e) {
            return new Date(e.from).getDate() == consumptionDayDate.getDate();
        });
        // now sum up totals and fill arrays for chart
        for (i=0; i<consumptionHourly.length; i++) {
            if (typeof consumptionHourly[i].cost === 'number' && typeof consumptionHourly[i].consumption === 'number') {
                totalConsumptionDay += consumptionHourly[i].consumption;
                totalCostsDay += consumptionHourly[i].cost;
                labels.push(createXLabel(consumptionHourly[i].from, consumptionHourly[i].to));
                dataConsumption.push(consumptionHourly[i].consumption.toFixed(2));
                dataPrice.push((consumptionHourly[i].unitPrice * 100).toFixed(2));
            }
        }
        $('#totalConsumptionDay').text(convertToLocale(totalConsumptionDay, ' kWh'));
        $('#totalCostsDay').text(convertToLocale(totalCostsDay, ' €'));
        $('#avgPriceDay').text(convertToLocale((totalCostsDay / totalConsumptionDay * 100), ' ct/kWh'));
        // create chart or hide it
        if (totalConsumptionDay > 0) {
            $('#noDailychartDiv').hide();
            loadHourlyConsumptionchart(labels, dataConsumption, dataPrice);
            $('#dailyConsumptionchartCanvasDiv').show();
        } else {
            $('#noDailychartDiv').show();
            $('#dailyConsumptionchartCanvasDiv').hide();
        }
        $('#cardTagesbezug').show();
    }
}

function processTibberResponse(tibberResponse, consumptionDayDate){
    /**
     * processes tibber response
     *
     * @function processTibberResponse
     * @author Michael Ortenstein
     * @param {object} tibberResponse as JSON-object
     */
    if (typeof tibberResponse == 'object') {
        // split up resonse
        // data for card "Allgemein"
        fillCardAllgemein(tibberResponse);
        // data for card "Strompreis"
        fillCardStrompreis(tibberResponse);
        // data for card "Tagesverbrauch"
        fillCardTagesbezug(tibberResponse, consumptionDayDate);
        // now show cards
        $('#waitForData').hide();
        $('#validData').show();
    } else {
        $('#dataErrorText').text('Tibber-Daten fehlerhaft, bitte später noch einmal versuchen.');
        $('#waitForData').hide();
        $('#dataError').show();
    }
}
