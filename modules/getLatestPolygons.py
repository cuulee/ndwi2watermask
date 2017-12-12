from pymongo import MongoClient
from bson import json_util
import json
import os
import sys 
from datetime import datetime
from sshtunnel import SSHTunnelForwarder
from defAggregations import *
from getPaths import *
import pandas as pd

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
latestMinusOne = getLatestIngestionTimeMinusOne(s2w)

df=pd.DataFrame

for item in latestMinusOne:
    df=pd.DataFrame.append([item['_id'],item['latestIngestion']])


with open('latestIngestions.json','a') as outfile:
    for feat in latestIngestionTime:
        json.dump(feat,outfile,default=json_util.default)
        outfile.write('\n')
    

if home['home']!='/home/riemer':
    server.stop()
