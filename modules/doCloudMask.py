
import os
import subprocess
from getPaths import *

items=os.listdir(s2aIn)

newlist = []
for names in items:
    if names.endswith("watermask.tif"):
        newlist.append(names)

for in_file in newlist:
    print("\n polygonizing " + in_file + "\n")
    out_file = in_file[:-4] + ".gml"
    subprocess.call([pyt,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])
    os.remove(sarOut + "/" + in_file)

print("\n********** polygonize completed!" + str(len(newlist))  + " watermasks processed\n********** Elapsed time: " + str(datetime.datetime.now()-t0) + "\n********** End of message\n")
