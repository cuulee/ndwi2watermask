import os
import subprocess
import glob
import datetime

t0=datetime.datetime.now()


#script="/"
#
#  get raster datasource
#
orson='Yeah!'#False
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
items=os.listdir(sarOut)

newlist = []
for names in items:
    if names.endswith("watermask.tif"):
        newlist.append(names)

print(newlist)


for in_file in newlist:
    out_file = in_file[:-4] + ".gml"
    subprocess.call([pyt,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])

print("\n********** polygonize completed!" + str(len(newlist))  + " watermasks processed\n********** Elapsed time: " + str(datetime.datetime.now()-t0) + "\n********** End of message\n")
