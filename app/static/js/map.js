$(document).ready( function() {
    mapboxgl.accessToken = 'pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v9',
        // center: longitude / latitude
        center: [5.7245, 45.1885],
        zoom: 10
    });
    
    document.getElementById('fly').addEventListener('click', function () {
        // Fly to a random location by offsetting the point -74.50, 40
        // by up to 5 degrees.
        map.flyTo({
            center: [
                5.7245 + (Math.random() - 0.5) * 10,
                45.1885 + (Math.random() - 0.5) * 10]
        });
    });
});