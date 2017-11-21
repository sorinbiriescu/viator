from mapbox import Geocoder
import json

mapbox_access_token = 'pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA'
location = 'Grenoble,Isère,France'


geocoder = Geocoder(access_token=mapbox_access_token)
response = geocoder.forward(location)
response_json =  response.json()
results = {'results':[]}
for i in response_json['features']:
    if 'place' in i['place_type']:
        results['results'].append({'location_name':i['place_name'],
                    'location_lat':i['geometry']['coordinates'][0],
                    'location_long':i['geometry']['coordinates'][1]})

result_final = json.dumps(results)
print(json.dumps(results))
# output_dict = [x['features'] for x in response_dict if "place" in x['features']['place_type']]
# output_json = json.dumps(output_dict)
# collection = response.json()['features'][0]['geometry']['coordinates']
