from defFuncemeApi import *
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
func = db.funceme ##  collection

reservs = getReservoir()

for reserv in reservs:
    code = reserv['code']
    ts = getRecentVolume(code)
    obj = {'reservoir' : code , ts}
    obj_id = func.update({"id":code},{"$set" : ts},upsert=True).upserted_id
    print obj_id
