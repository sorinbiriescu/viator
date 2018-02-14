$(document).ready(function () {

    let startDateInputTemplate_source = document.getElementById("start-date-input-template").innerHTML;
    let startDateInputTemplate = Handlebars.compile(startDateInputTemplate_source);

    let endDateInputTemplate_source = document.getElementById("end-date-input-template").innerHTML;
    let endDateInputTemplate = Handlebars.compile(endDateInputTemplate_source);

    let searchLocationInputTemplate_source = document.getElementById("location-search-bar-template").innerHTML;
    let searchLocationInputTemplate = Handlebars.compile(searchLocationInputTemplate_source);

    startDateCell = {
        $cell: true,
        id: "start-date",
        class: "medium-6 cell",

        $html: [startDateInputTemplate()],

        onchangeDate: function (el) {
            if (el.date === null) {

            } else {
                console.log("start changed date", el)
            }

        },

        $init: function () {
            let today = new Date()
            let todayYear = today.getFullYear()
            let todayMonth = today.getMonth() + 1
            let todayDay = today.getDate()

            startDate = todayDay + "-" + todayMonth + "-" + todayYear

            $('#start-date-input').fdatepicker({
                format: "dd-mm-yyyy",
                weekStart: 1,
                startDate: startDate,
                language: "en",
                disableDblClickSelection: true,
                leftArrow: "<<",
                rightArrow: ">>"
            });
        }
    }

    endDateCell = {
        $cell: true,
        id: "end-date",
        class: "medium-6 cell",

        $html: [endDateInputTemplate()],

        onchangeDate: function (el) {
            if (el.date === null) {

            } else {
                console.log("end changed date", el)
            }

        },

        $init: function () {
            let today = new Date()
            let todayYear = today.getFullYear()
            let todayMonth = today.getMonth() + 1
            let todayDay = today.getDate()

            startDate = todayDay + "-" + todayMonth + "-" + todayYear

            $('#end-date-input').fdatepicker({
                format: "dd-mm-yyyy",
                weekStart: 1,
                startDate: startDate,
                language: "en",
                disableDblClickSelection: true,
                leftArrow: "<<",
                rightArrow: ">>"
            });
        }
    }

    searchBarCell = {
        $cell: true,
        $type: "div",
        class: "cell medium-12",
        id: "location-search-bar",

        $html: [searchLocationInputTemplate()],

        $init: function () {
            $("#search-location-input").devbridgeAutocomplete({
                serviceUrl: 'http://127.0.0.1:5000/api/autocomplete',
                minChars: 4,
                deferRequestBy: 200,
                onSelect: function (suggestion) {
                    console.log(suggestion)
                    localStorage.setItem('locationName', suggestion.value);
                    localStorage.setItem('locationID', suggestion.data["location_ID"]);
                }
            })
        }
    }
    // createButton = {
    //     $cell: true,

    //     onclick: function () {
    //         let request_payload = {
    //             "itinerary_id": 0
    //         }

    //         return new Promise(function (resolve, reject) {

    //             $.ajax({
    //                 type: "GET",
    //                 url: "http://127.0.0.1:5000/api/itinerary",
    //                 data: {
    //                     parameters: JSON.stringify(request_payload)
    //                 },
    //                 success: successHandler,
    //                 error: errorHandler,
    //             });

    //             function successHandler(data, textStatus, xhr) {
    //                 return resolve(data)
    //             };

    //             function errorHandler() {
    //                 return reject(new Error("Could not create route!"))
    //             };
    //         })
    //     }
    // }

    app = {
        $cell: true,
        _startDate: "",
        _endDate: "",

        $update: function () {
            console.log("dates", _startDate, _endDate)
        }
    }
});