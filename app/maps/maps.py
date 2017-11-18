import folium
import os

script_dir = os.path.dirname(__file__)

def validate_coordinates(location_query_coord):
    if location_query_coord is None:
        return float(0)
    else:
        return float(location_query_coord)

def create_map(location_query):
    location_lat = validate_coordinates(location_query.location_lat)
    location_long = validate_coordinates(location_query.location_long)
    start_coords = (location_lat,location_long)
    location_name = location_query.location_name

    location_map = folium.Map(location=start_coords, zoom_start=14)
    
    folium.Marker([location_lat, location_long], popup='<i>%s</i>' %(location_name)).add_to(location_map)

    location_map_path = os.path.join(script_dir,"../templates/maps/map_%s.html" %(location_query.location_name))
    location_map.save(outfile= location_map_path,
            close_file=True)