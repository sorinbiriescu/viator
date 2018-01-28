'use strict';
let autocomplete_data

$(document).ready(function () {
    assignAutocomplete();
});

function assignAutocomplete() {
    $('#location-search-autocomplete').devbridgeAutocomplete({
        serviceUrl: 'http://127.0.0.1:5000/api/autocomplete',
        minChars: 4,
        deferRequestBy: 200,
        onSelect: function (suggestion) {
            autocomplete_data = suggestion.data;
            console.log(autocomplete_data);
        }
    });
};