from mapbox import Geocoder

mapbox_access_token = 'pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA'

def get_geocode(location='Grenoble'):
    geocoder = Geocoder(access_token=mapbox_access_token)
    response = geocoder.forward(location)
    collection = response.json()['features'][0]['geometry']['coordinates']

    return collection

