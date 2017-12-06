from pymongo import MongoClient
import json
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.sar2watermask ## db
s2w = db.sar2watermask ##  collection

#### query latest ingestion for each polygon

pipeline = [
    { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
    {
        "$group":
        {
            "_id" : "$properties.id_cogerh",
            "latestIngestion" : {
                "$last":"$properties.ingestion_time"
            }
        }
    }
]

aggrLatest=list(s2w.aggregate(pipeline=pipeline))

latest=list()

for feat in aggrLatest:
    poly = s2w.find({'properties.id_cogerh' : feat['_id'],'properties.ingestion_time':feat['latestIngestion']})
    latest.append(poly[0])
