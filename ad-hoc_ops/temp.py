import os
import csv

from app import db
from app import Locations

def validate_float(float_num):
    if float_num is '' or ' ':
        return float(0.0)
    else:
        float_num = str(float_num).replace(",",".").replace(" ","")
        print("..."+float_num+"...")
        return float(float_num)

with open('eucircos.csv') as csvfile:
    results = csv.reader(csvfile,delimiter=';')
    for row in results:
        print(row)
        new_location = Locations(
            location_eu_region = str(row[0]),
            location_region_code = int(row[1]),
            location_region_name = str(row[2]),
            location_region_capital = str(row[3]),
            location_department_no = str(row[4]),
            location_department_name = str(row[5]),
            location_prefecture = str(row[6]),
            location_circumscription = int(row[7]),
            location_name = str(row[8]),
            location_postal_code = str(row[9]),
            location_insee_code = str(row[10]),
            location_lat = validate_float(row[11]),
            location_long = validate_float(row[12]),
            location_distance = validate_float(row[13]),
        )
        db.session.add(new_location)
    db.session.commit()
