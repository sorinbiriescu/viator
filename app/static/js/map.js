'use strict';
let token = 'pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA';

let map;
let poi_center_auto;
let poi_center_user;

$(document).ready(function () {

  // Add a map to the 'map' div  
  map = L.map('mapbox').setView([45.18, 5.72], 12);

  let gl = L.mapboxGL({
    accessToken: token,
    style: 'mapbox://styles/mapbox/streets-v9'
  }).addTo(map);

  poi_center = map.getCenter();
  console.log(poi_center)

  map.on('moveend', () => {
    poi_center = map.getCenter();
    console.log(poi_center)
  })

  map.on('click',
    function (e) {
      var coord = e.latlng.toString().split(',');
      var lat = coord[0].split('(');
      var lng = coord[1].split(')');
      console.log("You clicked the map at latitude: " + lat[1] + " and longitude:" + lng[0]);
    });

  

});