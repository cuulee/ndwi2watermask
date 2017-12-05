from pymongo import MongoClient
import json
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.sar2watermask

with open('/home/delgado/scratch/watermasks/S1A_IW_GRDH_1SDV_20171124T080913_20171124T080938_019404_020E8C_F3CA_x12864_y0_watermask_simplified.geojson') as f:
    data = json.load(f)

s2w = db.sar2watermask
    
for feat in data["features"]:
    print(feat["properties"])
    dttm = datetime.strptime(feat["properties"]["ingestion_time"],"%Y/%m/%d %H:%M:%S+00")
    feat["properties"]["ingestion_time"] = dttm
    feat_id = s2w.insert_one(feat).inserted_id
    print feat_id

import pprint
d = datetime(2017, 11, 1, 0)

print s2w.find_one({'properties.ingestion_time' : {'$gte': d}})
print s2w.count({'properties.id_cogerh' : 3359})
print s2w.count({'properties.ingestion_time' : {'$gte': d}})
