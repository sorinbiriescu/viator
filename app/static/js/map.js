$(document).ready( function() {
    mapboxgl.accessToken = 'pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v9',
        // center: longitude / latitude
        center: [5.7245, 45.1885],
        zoom: 10
    });
    
    document.getElementById('search_submit').addEventListener('click', function () {
        // Fly to a random location by offsetting the point -74.50, 40
        // by up to 5 degrees.
        const $autocomplete = $('#location-search-autocomplete').val()
        var locLat
        var locLong
        console.log('Lat: ', locLat)
        console.log('Long: ', locLong)
        const url = 'http://127.0.0.1:5000/_geocode'
        const data = {
            query: $autocomplete
        }
        $.getJSON(url, data, function(data) {

                    locLat = Number(data.location_lat)
                    locLong = Number(data.location_long)
                    console.log('Lat: ', locLat)
                    console.log('Long: ', locLong)
        }).then( function() {
            map.flyTo({
                center: [locLong, locLat]
            });
        });
    });
});