'use strict';
// Add a Mapzen API key
let api_key = 'mapzen-fPCfu1G'
let map
let addMarkerToGroup
let clearMarkersFromGroup
let routingControl

$(document).ready(function () {
  L.Mapzen.apiKey = api_key;

  // Add a map to the 'map' div  
  map = L.Mapzen.map('mapzen', {
    center: [45.1885, 5.7245],
    zoom: 13,
    panToPint: true,
    pointIcon: true,
    tangramOptions: {
      scene: {
        import: L.Mapzen.BasemapStyles.Cinnabar,
        global: {
          sdk_building_extrude: false
        }
      }
    }
  });



  routingControl = L.Mapzen.routing.control({
    waypoints: [null],
    router: L.Mapzen.routing.router({
      costing: "auto"
    }),
    summaryTemplate: '<div class="start">{name}</div><div class="info {costing}">{distance}, {time}</div>',
    routeWhileDragging: false,
    show: false,
    collapsible: true
  }).addTo(map);

  let marker_group = L.layerGroup()
  marker_group.addTo(map)

  addMarkerToGroup = function (lat, long, name, icon, color, shape) {

    // let layer = type + "Group"

    // if (map.hasLayer(layer)) {
    //   // If has layer, do nothing
    // } else {
    //   L.layer().addTo(map)
    // }

    var marker_style = L.ExtraMarkers.icon({
      icon: icon,
      markerColor: color,
      shape: shape,
      prefix: 'fa'
    });

    L.marker([long, lat], {
      icon: marker_style,
    }).addTo(marker_group).bindPopup(name);

    // let marker = L.marker([long, lat]).bindPopup(popup);
    // marker.addTo(resultsGroup);
  };

  clearMarkersFromGroup = function () {

    marker_group.clearLayers();

  };
});