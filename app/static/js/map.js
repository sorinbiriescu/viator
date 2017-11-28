  // Add a Mapzen API key
var api_key = 'mapzen-fPCfu1G'
var map

$(document).ready( function() {
  L.Mapzen.apiKey = api_key;
// Add a map to the 'map' div  
  map = L.Mapzen.map('mapzen', {
    center: [45.1885, 5.7245],
    zoom: 13,
    panToPint: true,
    pointIcon: true,
    tangramOptions: {
      scene: L.Mapzen.BasemapStyles.Cinnabar
    }
  });

});