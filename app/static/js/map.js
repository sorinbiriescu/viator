'use strict';
// Add a Mapzen API key
let api_key = 'mapzen-fPCfu1G'
let map
let addMarkerToGroup
let clearMarkersFromGroup

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

  let resultsGroup = L.layerGroup().addTo(map);

  addMarkerToGroup = function(lat, long, popup) {
    let marker = L.marker([long, lat]).bindPopup(popup);
    marker.addTo(resultsGroup);
  };

  clearMarkersFromGroup = function() {
    resultsGroup.clearLayers();
  };
});

