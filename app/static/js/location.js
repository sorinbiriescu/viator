var autocomplete_data

$(document).ready( function() {

    // Autocomplete field
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

    // Fly to location returned by autocomplete
    document.getElementById('search_submit').addEventListener('click', function () {
    console.log('Passed coordinates:', autocomplete_data)

    map.flyTo([autocomplete_data[1], autocomplete_data[0]],13);

    });

});