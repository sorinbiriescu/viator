var autocomplete_data

$(document).ready( function() {
    $('#location-search-autocomplete').devbridgeAutocomplete({
        serviceUrl: 'http://127.0.0.1:5000/_autocomplete',
        dataType: 'json',
        minChars : 4,
        deferRequestBy: 100,
        onSelect: function (suggestion) {
            autocomplete_data = suggestion.data
            console.log('Received coordinates:',autocomplete_data)
        }
    });
});