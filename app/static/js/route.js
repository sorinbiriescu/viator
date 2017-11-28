var autocomplete_data, autocomplete_data2

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

    $('#location-search-autocomplete2').devbridgeAutocomplete({
        serviceUrl: 'http://127.0.0.1:5000/_autocomplete',
        dataType: 'json',
        minChars : 4,
        deferRequestBy: 100,
        onSelect: function (suggestion) {
            autocomplete_data2 = suggestion.data
            console.log('Received coordinates:',autocomplete_data2)
        }
    });

    $('#location-search-autocomplete3').devbridgeAutocomplete({
        serviceUrl: 'http://127.0.0.1:5000/_autocomplete',
        dataType: 'json',
        minChars : 4,
        deferRequestBy: 100,
        onSelect: function (suggestion) {
            autocomplete_data3 = suggestion.data
            console.log('Received coordinates:',autocomplete_data3)
        }
    });

    // Fly to location returned by autocomplete
    document.getElementById('search_submit_directions').addEventListener('click', function () {
    console.log('Passed coordinates:', autocomplete_data, autocomplete_data2, autocomplete_data3)
    
    route = {"locations":[
        {"lat":autocomplete_data[1],"lon":autocomplete_data[0]},
        {"lat":autocomplete_data2[1],"lon":autocomplete_data2[0]},
        {"lat":autocomplete_data3[1],"lon":autocomplete_data3[0]}],
        "costing":"auto",
        "directions_options":{"units":"miles"}
    }

    console.log(route)

    $.ajax({
        url: "http://127.0.0.1:5000/_optimized_route",
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify(route),
        success: function(json){
            console.log(json);
        }
    });

    var routingControl = L.Mapzen.routing.control({
        waypoints: [
          L.latLng(autocomplete_data[1], autocomplete_data[0]),
          L.latLng(autocomplete_data2[1], autocomplete_data2[0])
        ],
        router: L.Mapzen.routing.router({costing:"auto"}),
        summaryTemplate:'<div class="start">{name}</div><div class="info {costing}">{distance}, {time}</div>',
        routeWhileDragging: false
      }).addTo(map);

    });

});