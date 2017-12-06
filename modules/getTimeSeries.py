from pymongo import MongoClient
import json
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.sar2watermask ## db
s2w = db.sar2watermask ##  collection

#### aggregate time series of area (volume should be added as well) for each polygon

pipeline = [
    {
        "$group":
        {
            "_id" : "$properties.id_cogerh",
            "timeSeries" : { "$push" : { "time" : "$properties.ingestion_time" , "area" : "$properties.area"} }
        }

    }
]

TimeSeries = list(s2w.aggregate(pipeline=pipeline))
