from pymongo import MongoClient
import json
import os
import sys 
from datetime import datetime
from sshtunnel import SSHTunnelForwarder
from defAggregations import *
# to load credentials and locations
sys.path.append(os.path.abspath(proj +"/parameters"))

# to set locations
orson=False

from locations import *
from credentials import *

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', MONGO_PORT))

server.start()

client = MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port

## in case you want the local host:
#client = MongoClient('mongodb://localhost:27017/')

db = client.sar2watermask
s2w = db.sar2watermask ##  collection

TimeSeries = getTimeSeries(s2w)
latestPolys = getLatestIngestionTime(s2w)

server.stop()
