$(document).ready( function() {
  
  // Add a Mapzen API key
  var api_key = 'mapzen-fPCfu1G'
  L.Mapzen.apiKey = api_key;
  
  // Add a map to the 'map' div
  
  var map = L.Mapzen.map('mapzen', {
    center: [45.1885, 5.7245],
    zoom: 15,
    panToPint: true,
    pointIcon: true,
    tangramOptions: {
      scene: L.Mapzen.BasemapStyles.Cinnabar
    }
  });
  
  document.getElementById('search_submit').addEventListener('click', function () {
    console.log('Passed coordinates:', autocomplete_data)

    map.flyTo({lat:autocomplete_data[1],lng:autocomplete_data[0]});

  });
});