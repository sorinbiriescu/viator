from mapbox import Geocoder
import json

mapbox_access_token = 'pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA'

def get_geocode(location):
    geocoder = Geocoder(access_token=mapbox_access_token)
    response = geocoder.forward(location)
    response_json =  response.json()
    results = ''
    for i in response_json['features']:
        if 'place' in i['place_type']:
            results = {'location_name':i['place_name'],
                        'location_lat':i['geometry']['coordinates'][1],
                        'location_long':i['geometry']['coordinates'][0]}

    return json.dumps(results)

