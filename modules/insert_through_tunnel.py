from pymongo import MongoClient
import json
import os
import sys 
from datetime import datetime
from sshtunnel import SSHTunnelForwarder

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

# for credentials
sys.path.append(os.path.abspath(proj +"/parameters"))

from credentials import *

MONGO_HOST = "141.89.96.184"
MONGO_DB = "sar2watermask"
MONGO_PORT = 27017

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
#    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', 27017))


server.start()

client = MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
db = client.sar2watermask
s2w = db.sar2watermask ##  collection

print(db.collection_names())


#### IT WORKS!!!





server.stop()


#### This works, but would need python installed on the webserver and mount of orson's /mnt/scratch, which is not very reliable

#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect(hostname=MONGO_HOST,username=MONGO_USER,password=MONGO_PASS)
#stdin, stdout, stderr = ssh.exec_command('python ')
#ssh.close()
