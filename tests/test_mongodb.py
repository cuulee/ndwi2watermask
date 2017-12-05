from pymongo import MongoClient
import json
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.sar2watermask
s2w = db.sar2watermask

orson=False
if(orson):
    pyt="/users/stud09/martinsd/local/miniconda2/envs/gdal/bin/python"
    gdalPol="/users/stud09/martinsd/local/miniconda2/envs/gdal/bin/gdal_polygonize.py"
    proj="/users/stud09/martinsd/proj/sar2watermask"
    scratch="/mnt/scratch/martinsd"
else:
    pyt="/home/delgado/local/miniconda2/bin/python2"
    gdalPol="/home/delgado/local/miniconda2/bin/gdal_polygonize.py"
    proj="/home/delgado/proj/sar2watermask"
    scratch="/home/delgado/scratch"

    
sardir=scratch+"/s1a_scenes"
sarIn=sardir+"/in"
sarOut=sardir+"/out"
polOut=scratch + "/watermasks"
items=os.listdir(polOut)

newlist = []

for names in items:
    if names.endswith('simplified.geojson'):
        newlist.append(names)

for in_file in newlist:
    print('\n inserting ' + in_file + ' in mongodb\n')

    with open(polOut + '/' + in_file) as f:
        data = json.load(f)

    
    for feat in data["features"]:
        dttm = datetime.strptime(feat["properties"]["ingestion_time"],"%Y/%m/%d %H:%M:%S+00")
        feat["properties"]["ingestion_time"] = dttm
        feat_id = s2w.insert_one(feat).inserted_id
        print feat_id

import pprint
d2 = datetime(2017, 11, 28, 0)
d1 = datetime(2017, 11, 25, 0)

q2 = s2w.find({'properties.ingestion_time' : {'$gte': d2}})
q1 = s2w.find({'properties.ingestion_time' : {'$lte': d1}})
q3 = s2w.find({'properties.id_cogerh' : 3359})

## aggregate NOT WORKING YET!!!

pipeline = [
    { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
    {
        "$group":
        {
            "id_cogerh" : "properties.id_cogerh",
            "lastPolygon": {"$last":"$properties.ingestion_time"}
        }
    }
]

p=s2w.aggregate(pipeline)

print q2[0]["geometry"]["type"]
print s2w.count({'properties.id_cogerh' : 3359})
print s2w.count({'properties.ingestion_time' : {'$gte': d}})
