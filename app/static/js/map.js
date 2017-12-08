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

  var redMarker = L.ExtraMarkers.icon({
    icon: 'fa-coffee',
    markerColor: 'red',
    shape: 'square',
    prefix: 'fa'
  });

  L.marker([51.941196, 4.512291], {
    icon: redMarker,
  }).addTo(map);

  addMarkerToGroup = function (lat, long, popup, type) {

    layer = type + "Group"

    if (map.hasLayer(layer)) {
      // If has layer, do nothing
    } else {
      L.layerGroup(layer).addTo(map)
    }

    var marker_style = L.ExtraMarkers.icon({
      icon: 'fa-coffee',
      markerColor: 'red',
      shape: 'square',
      prefix: 'fa'
    });

    L.marker([long, lat], {
      icon: marker_style,
    }).addTo(layer).bindPopup(popup);

    // let marker = L.marker([long, lat]).bindPopup(popup);
    // marker.addTo(resultsGroup);
  };

  clearMarkersFromGroup = function () {
    map.eachLayer(function (layer) {
      map.removeLayer(layer);
    });
  };
});