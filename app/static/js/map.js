'use strict';
let token = 'pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA';

let map
let addMarkerToGroup
let clearMarkersFromGroup
let routingControl

$(document).ready(function () {

  // Add a map to the 'map' div  
  map = L.map('mapbox').setView([45.18, 5.72], 12);

  var gl = L.mapboxGL({
    accessToken: token,
    style: 'mapbox://styles/mapbox/streets-v9'
  }).addTo(map);

  let marker_group = L.layerGroup()
  marker_group.addTo(map)

  addMarkerToGroup = function (lat, long, name, icon, color, shape) {

    var marker_style = L.ExtraMarkers.icon({
      icon: icon,
      markerColor: color,
      shape: shape,
      prefix: 'fa'
    });

    L.marker([long, lat], {
      icon: marker_style,
    }).addTo(marker_group).bindPopup(name);

  };

  clearMarkersFromGroup = function () {

    marker_group.clearLayers();

  };
});