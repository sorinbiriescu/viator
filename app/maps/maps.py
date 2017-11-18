import folium
import os

script_dir = os.path.dirname(__file__)

def create_map(location_query):
    start_coords = (location_query.location_lat, location_query.location_long)
    map = folium.Map(location=start_coords, zoom_start=14)
    map.save(outfile=os.path.join(script_dir,"../templates/maps/map_%s.html" %(location_query.location_name)),
            close_file=True)