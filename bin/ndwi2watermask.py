import os
import modules.getPaths as pths
import numpy as np
from modules.defCloudMask import unzipJp2, getBandDir,interpolate_clouds_to_10m
from modules.ndwi import ndwi_from_jp2

zipfls=[]
items=os.listdir(pths.s2aIn)

for item in items:
    item=pths.s2aIn + '/' + item
    if re.search('^.*\.zip$', item) :
        zipfls.append(item)
        sceneJp2 = unzipJp2(item)
        ndwi_from_jp2(sceneJp2)
