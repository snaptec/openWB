/**
 * Functions to retrieve and process data from Tibber API
 *
 * @author Michael Ortenstein
 */

function readTibberAPI() {
    /**
     * calls Tibber API as promise and returns data or error-message
     *
     * @function readTibberAPI
     * @author Michael Ortenstein
     * @returns {Promise} Promise object represents the result of the ajax-query
     */
    // calculate amount of datasets to be received since Tibber only sends valid data for
    // past hours/days/months
    var now = new Date();
    const hoursToReceive = now.getHours() + 24; // Tibber sends hourly data for past hours
    const daysToReceive = now.getDate() + 1;  // Tibber sends daily data for past days
    var monthsToReceive = now.getMonth();  // no index correction since Tibber sends monthly data for past months

    // token have to be replaced by user-specific data once page is completed
    var tibberToken = "d1007ead2dc84a2b82f0de19451c5fb22112f7ae11d19bf2bedb224a003ff74a";
    var tibberHomeID = "c70dcbe5-4485-4821-933d-a8a86452737b";
    const tibberAPI = "https://api.tibber.com/v1-beta/gql";
    const tibberQueryHead = '{ "query": "{viewer {name home(id:\\"' + tibberHomeID + '\\") {';
    const tibberQueryGetAdress = 'address {address1 postalCode city}';
    const tibberQueryGetPriceInfo = 'currentSubscription {priceInfo {current{total energy tax startsAt} today {total startsAt} tomorrow {total startsAt}}}';
    const tibberQueryGetHourlyConsumption = 'cons_hourly: consumption(resolution: HOURLY, last:' + hoursToReceive + ') {nodes {from to cost unitPrice unitPriceVAT consumption}}';
    const tibberQueryTail = '}}}"}';
    var tibberQuery = tibberQueryHead + tibberQueryGetAdress + tibberQueryGetPriceInfo + tibberQueryGetHourlyConsumption + tibberQueryTail;

    return new Promise((resolve, reject) => {
        $.ajax({
            type: "POST",
            url: tibberAPI,
            headers: {
                "Authorization": "Bearer " + tibberToken,
                "Content-Type": "application/json"
            },
            data: tibberQuery,
            success: function (data) {
                resolve(data)
            },
            error: function (error) {
                reject(error)
            }
        })
    })
}

function createXLabel(date){
    /**
     * convert date in suitable label for chart x-axis
     *
     * @function createXLabel
     * @author Michael Ortenstein
     * @param {string} date as date string
     * @returns {string} label as prettified date
     */
    var dateObj = new Date(date);
    return  dateObj.getHours() + " Uhr";
}

function convertToLocale(number, unit){
    /**
     * convert float umber to locale with 2 digits and add unit
     * if not a number return "--"
     *
     * @function processTibberResponse
     * @author Michael Ortenstein
     * @param {float} number
     * @param {string} unit
     * @returns {string} converted number
     */
    var converted = '--';
    if (!isNaN(number)) {
        converted = parseFloat(number).toLocaleString(undefined, {maximumFractionDigits: 2}) + ' ' + unit;
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
    if (typeof homeData !== 'undefined') {
        $('#street').text(homeData.address1);
        $('#city').text(homeData.postalCode + ' ' + homeData.city);
    }
    $('#name').text(response.data.viewer.name);
}

function fillCardStrompreis(response){
    /**
     * fills the card "Strompreis" with data from tibber response
     *
     * @function fillCardAllgemein
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
        $('#currentPrice').text(convertToLocale((priceCurrentData.total * 100), 'Cent/kWh'));
        $('#currentEnergyPrice').text(convertToLocale((priceCurrentData.energy * 100), 'Cent/kWh'));
        $('#currentTax').text(convertToLocale((priceCurrentData.tax * 100), 'Cent/kWh'));
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

function fillCardTagesverbrauch(response){
    /**
     * fills the card "Tagesverbrauch" with data from tibber response
     *
     * @function fillCardAllgemein
     * @author Michael Ortenstein
     * @param {object} tibberResponse as JSON-object
     */
    const options = { weekday: 'short', year: 'numeric', month: 'numeric', day: 'numeric' };
    var consumptionHourly = response?.data?.viewer?.home?.cons_hourly?.nodes;
    var yesterday = new Date(Date.now() - 86400000);
    var labels = ["0 Uhr"];
    var data = [0];
    var totalConsumption = 0;
    var totalCosts = 0;

    if (typeof consumptionHourly !== 'undefined') {
        $('#dateYesterday').text('für ' + yesterday.toLocaleDateString(undefined, options));
        // first filter all dates other than yesterday
    	var midnight = new Date(new Date().setHours(0,0,0,0));
        consumptionHourly = consumptionHourly.filter(function (e) {
            return new Date(e.from).valueOf() < midnight.valueOf();
        });
        console.log(consumptionHourly);
        // now if 24 hours are left, sum up totals and fill arrays for chart
        if (consumptionHourly.length == 24) {
            for (i=0; i<consumptionHourly.length; i++) {
                if (typeof consumptionHourly[i].cost === 'number' && typeof consumptionHourly[i].consumption === 'number') {
                    totalConsumption += consumptionHourly[i].consumption;
                    totalCosts += consumptionHourly[i].cost;
                    labels.push(createXLabel(consumptionHourly[i].to));
                    data.push(totalConsumption.toFixed(2));
                }
            }
            $('#totalConsumptionDay').text(convertToLocale(totalConsumption, ' kWh'));
            $('#totalCostsDay').text(convertToLocale(totalCosts, ' €'));
            $('#avgPriceDay').text(convertToLocale((totalCosts / totalConsumption * 100), ' Cent/kWh'));
        }
        // create chart
        loadHourlyConsumptionchart(labels, data);
        $('#cardTagesverbrauch').show();
    }
}

function processTibberResponse(tibberResponse){
    /**
     * processes tibber response
     *
     * @function processTibberResponse
     * @author Michael Ortenstein
     * @param {object} tibberResponse as JSON-object
     */
    const options = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', timeZoneName: 'short' };

    if (typeof tibberResponse == 'object') {
        var now = new Date();
        $('#lastDataReceived').text(now.toLocaleDateString(undefined, options));
        // split up resonse
        // data for card "Allgemein"
        fillCardAllgemein(tibberResponse);
        // data for card "Strompreis"
        fillCardStrompreis(tibberResponse);
        // data for card "Tagesverbrauch"
        fillCardTagesverbrauch(tibberResponse);
        // data for card "Monatsverbrauch"

        // data for card "Jahresverbrauch"

        // now show cards
        $('#noValidData').hide();
        $('#validData').show();
    } else {
        $('#noValidDataText').text('Tibber-Daten fehlerhaft, bitte später noch einmal versuchen.');
        $('#noValidDataSpinner').hide();
    }
}
