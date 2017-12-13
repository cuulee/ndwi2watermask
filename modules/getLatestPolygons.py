from pymongo import MongoClient
from bson import json_util
import json
import os
import sys 
from datetime import datetime
from sshtunnel import SSHTunnelForwarder
from defAggregations import *
from getPaths import *

if home['home']!='/home/riemer':
    server = SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_password=MONGO_PASS,
        remote_bind_address=('127.0.0.1', MONGO_PORT))
    
    server.start()
    print("started ssh tunnel")

    client = MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
else:
    print("connecting to local host")
    client = MongoClient('mongodb://localhost:27017/')


db = client.sar2watermask
s2w = db.sar2watermask ##  collection

#TimeSeries = getTimeSeries(s2w)
latestIngestionTime = getLatestIngestionTime(s2w)
polys= getLatestPolys(s2w)

poly_i={}
poly_i=

geojson={}
geojson["type"]="FeatureCollection"
geojson["crs"]={"type" : "name","properties" : {"name" : "urn:ogc:def:crs:OGC:1.3:CRS84"}}

geojson["features"] = 

latestMinusOne = getLatestIngestionTimeMinusOne(s2w)

if home['home']!='/home/riemer':
    server.stop()

with open('latestIngestions.tbl','a') as outfile:
    for feat in latestIngestionTime:
        outfile.write('%s\n' %feat['_id'])
    

