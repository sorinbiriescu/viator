from app import db
from sqlalchemy import Column, BigInteger, Text
from geoalchemy2 import Geometry

class GISModelMixin (object):
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    osm_id = db.Column(db.BigInteger)
    access = db.Column(db.Text)
    addr_housename = db.Column('addr:housename',db.Text)
    addr_housenumber = db.Column('addr:housenumber',db.Text) 
    addr_interpolation = db.Column('addr:interpolation',db.Text)
    admin_level = db.Column(db.Text)
    aerialway = db.Column(db.Text)
    aeroway = db.Column(db.Text)
    amenity = db.Column(db.Text)
    area = db.Column(db.Text)
    barrier = db.Column(db.Text)
    bicycle = db.Column(db.Text)
    brand = db.Column(db.Text)
    bridge = db.Column(db.Text)
    boundary = db.Column(db.Text)
    building = db.Column(db.Text)
    construction = db.Column(db.Text)
    covered = db.Column(db.Text)
    culvert = db.Column(db.Text)
    cutting = db.Column(db.Text)
    denomination = db.Column(db.Text)
    disused = db.Column(db.Text)
    embankment = db.Column(db.Text)
    foot = db.Column(db.Text)
    generator_source = db.Column('generator:source',db.Text)
    harbour = db.Column(db.Text)
    highway = db.Column(db.Text)
    historic = db.Column(db.Text)
    horse = db.Column(db.Text)
    intermittent = db.Column(db.Text)
    junction = db.Column(db.Text)
    landuse = db.Column(db.Text)
    layer = db.Column(db.Text)
    leisure = db.Column(db.Text)
    lock = db.Column(db.Text)
    man_made = db.Column(db.Text)
    military = db.Column(db.Text)
    motorcar = db.Column(db.Text)
    name = db.Column(db.Text)
    natural = db.Column(db.Text)
    office = db.Column(db.Text)
    oneway = db.Column(db.Text)
    operator = db.Column(db.Text)
    place = db.Column(db.Text)
    population = db.Column(db.Text)
    power = db.Column(db.Text)
    power_source = db.Column(db.Text)
    public_transport = db.Column(db.Text)
    railway = db.Column(db.Text)
    ref = db.Column(db.Text)
    religion = db.Column(db.Text)
    route = db.Column(db.Text)
    service = db.Column(db.Text)
    shop = db.Column(db.Text)
    sport = db.Column(db.Text)
    surface = db.Column(db.Text)
    toll = db.Column(db.Text)
    tourism = db.Column(db.Text)
    tower_type = db.Column('tower:type',db.Text)
    tracktype = db.Column(db.Text)
    tunnel = db.Column(db.Text)
    water = db.Column(db.Text)
    waterway = db.Column(db.Text)
    wetland = db.Column(db.Text)
    width = db.Column(db.Text)
    wood = db.Column(db.Text)
    z_order = db.Column(db.Integer)
    way_area = db.Column(db.Float)


class rhone_alpes_line(GISModelMixin, db.Model):
    __bind_key__ = 'gis_rhone_alpes'

    way = db.Column(Geometry('LINESTRING'))

class rhone_alpes_nodes(db.Model):
    __bind_key__ = 'gis_rhone_alpes'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    lon = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.Text)

class rhone_alpes_point(GISModelMixin,db.Model):
    __bind_key__ = 'gis_rhone_alpes'

    capital = db.Column(db.Text)
    ele = db.Column(db.Text)
    poi = db.Column(db.Text)
    way = db.Column(Geometry('POINT'))

class rhone_alpes_polygon(GISModelMixin,db.Model):
    __bind_key__ = 'gis_rhone_alpes'

    way = db.Column(Geometry('GEOMETRY'))

class rhone_alpes_rels(db.Model):
    __bind_key__ = 'gis_rhone_alpes'

    id = db.Column(db.BigInteger, primary_key=True,nullable=False)
    way_off = db.Column(db.SmallInteger)
    rel_off = db.Column(db.SmallInteger)
    parts = db.Column(db.ARRAY(BigInteger))
    members = db.Column(db.ARRAY(Text))
    tags = db.Column(db.ARRAY(Text))

class rhone_alpes_roads(GISModelMixin,db.Model):
    __bind_key__ = 'gis_rhone_alpes'

    way = db.Column(Geometry('LINESTRING'))

class rhone_alpes_ways(db.Model):
    __bind_key__ = 'gis_rhone_alpes'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    nodes = db.Column(db.ARRAY(BigInteger), nullable=False)
    tags = db.Column(db.Text)