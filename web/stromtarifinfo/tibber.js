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
     * @returns {Promise} Promise object represents the resuklt of the ajax-query
     */

    // token have to be replaced by user-specific data once page is completed
    var tibberToken = "d1007ead2dc84a2b82f0de19451c5fb22112f7ae11d19bf2bedb224a003ff74a";
    var tibberHomeID = "c70dcbe5-4485-4821-933d-a8a86452737b";
    const tibberAPI = "https://api.tibber.com/v1-beta/gql";
    const tibberQueryHead = '{ "query": "{viewer {name home(id:\\"' + tibberHomeID + '\\") {';
    const tibberQueryGetAdress = 'address {address1 postalCode city}';
    const tibberQueryGetPriceInfo = 'currentSubscription {priceInfo {current{total energy tax startsAt} today {total startsAt} tomorrow {total startsAt}}}';
    const tibberQueryTail = '}}}"}';
    const tibberQuery = tibberQueryHead + tibberQueryGetAdress + tibberQueryGetPriceInfo + tibberQueryTail;

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

function convertToCent(euros){
    /**
     * convert number as price in Euro into Eurocent and add unit
     *
     * @function processTibberResponse
     * @author Michael Ortenstein
     * @param {float} euros
     * @returns {string} eurocent
     */
    var eurocent = '--';
    if (!isNaN(euros)) {
        eurocent = parseFloat(euros*100).toLocaleString(undefined, {maximumFractionDigits: 2}) + ' Cent/kWh'
    }
    return eurocent;
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

        // split up resonse
        var homeData = tibberResponse.data.viewer.home.address;
        var priceCurrentData = tibberResponse.data.viewer.home.currentSubscription.priceInfo.current;
        var priceTodayData = tibberResponse.data.viewer.home.currentSubscription.priceInfo.today;
        var priceTomorrowData = tibberResponse.data.viewer.home.currentSubscription.priceInfo.tomorrow;

        var now = new Date();
        $('#lastDataReceived').text(now.toLocaleDateString(undefined, options));

        $('#name').text(tibberResponse.data.viewer.name);
        $('#street').text(homeData.address1);
        $('#city').text(homeData.postalCode + ' ' + homeData.city);
        $('#currentPrice').text(convertToCent(priceCurrentData.total));
        $('#currentEnergyPrice').text(convertToCent(priceCurrentData.energy));
        $('#currentTax').text(convertToCent(priceCurrentData.tax));
        var startsAt = new Date(priceCurrentData.startsAt);
        $('#currentValidSince').text(startsAt.toLocaleDateString(undefined, options));
        loadElectricityPricechart(priceTodayData, priceTomorrowData);

        $('#noValidData').hide();
        $('#validData').show();
    } else {
        $('#noValidDataText').text('Tibber-Daten fehlerhaft, bitte später noch einmal versuchen.');
        $('#noValidDataSpinner').hide();
    }
}
