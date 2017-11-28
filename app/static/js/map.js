$(document).ready( function() {
  
  // Add a Mapzen API key
  var api_key = 'mapzen-fPCfu1G'
  L.Mapzen.apiKey = api_key;
  
// Add a map to the 'map' div  
  var map = L.Mapzen.map('mapzen', {
    center: [45.1885, 5.7245],
    zoom: 13,
    panToPint: true,
    pointIcon: true,
    tangramOptions: {
      scene: L.Mapzen.BasemapStyles.Cinnabar
    }
  });

// Fly to location returned by autocomplete
  document.getElementById('search_submit').addEventListener('click', function () {
    console.log('Passed coordinates:', autocomplete_data)

    map.flyTo([autocomplete_data[1], autocomplete_data[0]],13);

  });

// Get mouse click position
  map.on('click', 
  function(e){
    var coord = e.latlng.toString().split(',');
    var lat = coord[0].split('(');
    var lng = coord[1].split(')');
    console.log("You clicked the map at latitude: " + lat[1] + " and longitude:" + lng[0]);
  });

});