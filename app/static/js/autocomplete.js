'use strict';
let autocomplete_data

$(document).ready(function () {
    assignAutocomplete();
});

function assignAutocomplete() {
    // Autocomplete field
    $('#location-search-autocomplete').devbridgeAutocomplete({
        serviceUrl: 'http://127.0.0.1:5000/api/autocomplete',
        // dataType: 'json',
        minChars: 4,
        deferRequestBy: 100,
        onSelect: function (suggestion) {
            autocomplete_data = suggestion.data;
            searchResults();
            console.log(autocomplete_data)
        }
    });

};