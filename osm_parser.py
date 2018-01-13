import osmium as o
import sys
import shapely.wkb as wkblib

from app.models.models_locations import Locations
from app import db

wkbfab = o.geom.WKBFactory()
pbf_file = 'rhone-alpes-latest.osm.pbf'

class AmenityListHandler(o.SimpleHandler):

    def print_amenity(amenity, tags, lon, lat, poi_type):
        name = tags.get('name', '')

        print("%f %f %-15s %s %s" % (lon, lat, tags['tourism'], name, poi_type))

    def node(self, n):
        if 'tourism' in n.tags:
            self.print_amenity(n.tags, n.location.lon, n.location.lat, 'node')

    def way(self, w):
        if 'tourism' in w.tags:
            wkb = wkbfab.create_multipolygon(a)
            poly = wkblib.loads(wkb, hex=True)
            centroid = poly.representative_point()
            self.print_amenity(w.tags, centroid.x, centroid.y, 'way')

    def area(self, a):
        if 'tourism' in a.tags:
            wkb = wkbfab.create_multipolygon(a)
            poly = wkblib.loads(wkb, hex=True)
            centroid = poly.representative_point()
            self.print_amenity(a.tags, centroid.x, centroid.y, 'area')


class CitiesRegionsHandler(o.SimpleHandler):

    def submit_location(amenity, id, tags, lon, lat,wkb):
        if tags['admin_level'] == '6' or tags['admin_level'] == '8':

            osm_id = id
            name = tags['name']
            admin_level = tags['admin_level']
            
            if admin_level == '4':
                admin_type = 'Region'
            elif admin_level == '6':
                admin_type = 'Department'
            elif admin_level == '8':
                admin_type = 'City'
            else:
                print('Unknown value in admin_level tag')
            
            centroid = "POINT(%s %s)" % (lat, lon)

            new_entry = Locations(
                osm_id=osm_id,
                name=name,
                admin_type=admin_type,
                admin_level=admin_level,
                centroid=centroid,
                geometry=wkb
                )

            db.session.add(new_entry)
            db.session.commit()
            print ("Added:",new_entry)

            # print("%i %s %f %f %-15s %s" % (id, name, lon, lat, admin_type, admin_level))


    def area(self, a):
        if 'admin_level' in a.tags:
            wkb = wkbfab.create_multipolygon(a)
            poly = wkblib.loads(wkb, hex=True)
            centroid = poly.representative_point()
            self.submit_location(a.id, a.tags, centroid.x, centroid.y,wkb)


if __name__ == "__main__":
    CitiesRegionsHandler().apply_file(pbf_file)
    # AmenityListHandler().apply_file(pbf_file)