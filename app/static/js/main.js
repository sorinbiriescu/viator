$(document).ready( function() {
    $('#location-search-autocomplete').devbridgeAutocomplete({
        serviceUrl: 'http://127.0.0.1:5000/_autocomplete',
        minChars : 4
    });
});