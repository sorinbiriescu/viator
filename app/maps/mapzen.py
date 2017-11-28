import folium
import os

script_dir = os.path.dirname(__file__)

def validate_coordinates(location_query_coord):
    if location_query_coord is None:
        return float(0)
    else:
        return float(location_query_coord)

def create_map_loc(location_query):
    location_lat = validate_coordinates(location_query.location_lat)
    location_long = validate_coordinates(location_query.location_long)
    start_coords = (location_lat, location_long)
    location_name = location_query.location_name

    location_map = folium.Map(location=start_coords,
            tiles='https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA',
            attr='Mapbox',
            zoom_start=14)
    
    folium.Marker([location_lat, location_long], popup='<i>%s</i>' %(location_name)).add_to(location_map)

    location_map_path = os.path.join(script_dir,"../templates/maps/map_%s.html" %(location_name))
    location_map.save(outfile=location_map_path, close_file=True)

def create_map_att(attraction_query):
    attraction_lat = validate_coordinates(attraction_query.attraction_lat)
    attraction_long = validate_coordinates(attraction_query.attraction_long)
    start_coords = (attraction_lat, attraction_long)
    attraction_name = attraction_query.attraction_name

    location_map = folium.Map(location=start_coords,
            tiles='https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA',
            attr='Mapbox',
            zoom_start=16)
    
    folium.Marker([attraction_lat, attraction_long], popup='<i>%s</i>' %(attraction_name)).add_to(location_map)

    location_map_path = os.path.join(script_dir,"../templates/maps/map_%s.html" %(attraction_name))
    location_map.save(outfile=location_map_path, close_file=True)
