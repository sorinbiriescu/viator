import osmium as o
import sys
import shapely.wkb as wkblib

from app.models.models_locations import Locations, Attractions
from app import db

wkbfab = o.geom.WKBFactory()
pbf_file = 'rhone-alpes-latest.osm.pbf'

class TourismListHandler(o.SimpleHandler):

    def submit_location(amenity, id, tags, lon, lat, osm_type):

        osm_id = id
        name = tags.get('name','')

        attraction_type = tags.get('tourism','')
        
        centroid = "POINT(%s %s)" % (lat, lon)

        new_entry = Attractions(
            osm_id=osm_id,
            osm_type=osm_type,
            name=name,
            attraction_type=attraction_type,
            centroid=centroid
            )

        
        db.session.add(new_entry)
        db.session.commit()
        print ("Added:",new_entry)
        print("%i %s %s %s %f %f" % (id, osm_type, name, attraction_type,lon, lat))



    # def node(self, n):
    #     if 'tourism' in n.tags:
    #         self.submit_location(n.id, n.tags, n.location.lon, n.location.lat, 'node')
    #     else:
    #         pass

    # def way(self, w):
    #     if 'tourism' in w.tags:
    #         wkb = wkbfab.create_multipolygon(w)
    #         poly = wkblib.loads(wkb, hex=True)
    #         centroid = poly.representative_point()
    #         self.submit_location(w.id, w.tags, centroid.x, centroid.y, 'way')
    #     else:
    #         pass

    def area(self, a):
        if 'tourism' in a.tags:
            wkb = wkbfab.create_multipolygon(a)
            poly = wkblib.loads(wkb, hex=True)
            centroid = poly.representative_point()
            self.submit_location(a.id, a.tags, centroid.x, centroid.y,'area')
        else:
            pass

class AmenityListHandler(o.SimpleHandler):

    def submit_location(amenity, id, tags, lon, lat, osm_type):

        osm_id = id
        name = tags.get('name','')
        amenity_list = ['restaurant','bar', 'cafe', 'biergarten',
            'drinking_water', 'pub', 'food_court', 'atm', 'arts_centre']
        print(tags)
        if 'tourism' in tags:
            attraction_type = tags.get('tourism')
        elif 'amenity' in tags and tags.get('amenity') in amenity_list:
            attraction_type = tags.get('amenity','')
        else:
            attraction_type = ""
            print("error in tourism and amenity tags")
        
        centroid = "POINT(%s %s)" % (lat, lon)

        # new_entry = Attractions(
        #     osm_id=osm_id,
        #     osm_type = osm_type,
        #     name=name,
        #     attraction_type=attraction_type,
        #     centroid=centroid
        #     )

        # db.session.add(new_entry)
        # db.session.commit()
        # print ("Added:",new_entry)

        print("%i %s %s %s %f %f" % (id, osm_type, name, attraction_type,lon, lat))


    def node(self, n):
        if 'tourism' or 'amenity' in n.tags:
            self.submit_location(n.id, n.tags, n.location.lon, n.location.lat, 'node')
        else:
            pass

    def way(self, w):
        if 'tourism' or 'amenity' in w.tags:
            wkb = wkbfab.create_multipolygon(a)
            poly = wkblib.loads(wkb, hex=True)
            centroid = poly.representative_point()
            self.submit_location(w.id, w.tags, centroid.x, centroid.y, 'way')
        else:
            pass

    def area(self, a):
        if 'tourism' or 'amenity' in a.tags:
            wkb = wkbfab.create_multipolygon(a)
            poly = wkblib.loads(wkb, hex=True)
            centroid = poly.representative_point()
            self.submit_location(a.id, a.tags, centroid.x, centroid.y,'area')
        else:
            pass



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
    # CitiesRegionsHandler().apply_file(pbf_file)
    TourismListHandler().apply_file(pbf_file)