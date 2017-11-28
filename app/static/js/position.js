$(document).ready( function() {
    
// Get mouse click position
map.on('click', 
function(e){
  var coord = e.latlng.toString().split(',');
  var lat = coord[0].split('(');
  var lng = coord[1].split(')');
  console.log("You clicked the map at latitude: " + lat[1] + " and longitude:" + lng[0]);
});

});