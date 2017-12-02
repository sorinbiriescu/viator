var autocomplete_data

$.ajax({
    type: 'GET',
    url: "http://127.0.0.1:5000/_getpoi",
    data: data,
    // async: false,
    beforeSend: function (xhr) {
      if (xhr && xhr.overrideMimeType) {
        xhr.overrideMimeType('application/json;charset=utf-8');
      }
    },
    dataType: 'json',
    success: function (data) {
        console.log(data)
    }
  });

$(document).ready(function () {

    // Autocomplete field
    $('#location-search-autocomplete').devbridgeAutocomplete({
        serviceUrl: 'http://127.0.0.1:5000/_autocomplete',
        dataType: 'json',
        minChars: 4,
        deferRequestBy: 100,
        onSelect: function (suggestion) {
            autocomplete_data = suggestion.data
            console.log('Received coordinates:', autocomplete_data)
        }
    });

    // Fly to location returned by autocomplete
    document.getElementById('search_submit').addEventListener('click', function () {
        console.log('Passed coordinates:', autocomplete_data)

        

        route = {
            "location": {
                "lat": autocomplete_data[1],
                "lon": autocomplete_data[0]
            }
        }

        map.flyTo([autocomplete_data[1], autocomplete_data[0]], 13)
        map.on('moveend', onMoveEnd);

        function onMoveEnd(evt) {
            var map = evt.map;
            
        }
    });

});