'use strict';
// Add a Mapzen API key
var api_key = 'mapzen-fPCfu1G'
var map
var addMarkerToGroup
var clearMarkersFromGroup

$(document).ready(function () {
  L.Mapzen.apiKey = api_key;
  // Add a map to the 'map' div  
  map = L.Mapzen.map('mapzen', {
    center: [45.1885, 5.7245],
    zoom: 13,
    panToPint: true,
    pointIcon: true,
    // tangramOptions: {
    //   scene: L.Mapzen.BasemapStyles.Refill
    // }
  });

  var resultsGroup = L.layerGroup()
  resultsGroup.addTo(map);

  addMarkerToGroup = function(lat, long, popup) {
    let marker = L.marker([long, lat]).bindPopup(popup);
    marker.addTo(resultsGroup);
  };

  clearMarkersFromGroup = function() {
    resultsGroup.clearLayers();
  };
});

