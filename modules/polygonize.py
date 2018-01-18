import os
import subprocess
import glob
import datetime
from getPaths import *

t0=datetime.datetime.now()

items=os.listdir(sarOut)

newlist = []

for names in items:
    if names.endswith("watermask.tif"):
        newlist.append(names[0:67])

newlist = list(set(newlist))


#print(newlist)


for scene in newlist:
    print("\n polygonizing " + scene + "\n")
    out_tif = scene + ".tif"
    out_gml = scene + ".gml"
    subprocess.call([pyt,gdalMerge,'-o',sarOut + "/" + out_tif,sarOut + "/" + scene + "*"]
    os.remove(sarOut + "/" + scene + "_*")                    
    subprocess.call([pyt,gdalPol,sarOut + "/" + out_tif,"-f","GML",polOut + "/" + out_gml])
    os.remove(sarOut + "/" + out_tif)

print("\n********** polygonize completed!" + str(len(newlist))  + " watermasks processed\n********** Elapsed time: " + str(datetime.datetime.now()-t0) + "\n********** End of message\n")
