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

MONGO_HOST = "141.89.96.184"
MONGO_DB = "sar2watermask"
MONGO_PORT = 27017

