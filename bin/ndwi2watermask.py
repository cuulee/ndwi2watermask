import os
import modules.getpaths as pths
import numpy as np
from modules.cloudmask import unzipJp2,runGdalbuildvrt,runFmaskMakeAngles,runFmaskStack
from modules.ndwi import ndwi_from_jp2
import re

def ndwi2watermask():
    print("Executing ndwi2watermask():")
    zipfls=[]
    items=os.listdir(pths.s2aIn)

    for item in items:
        item=pths.s2aIn + '/' + item
        if re.search('^.*\.zip$', item) :
            zipfls.append(item)
            sceneJp2 = unzipJp2(item)
            ndwi_from_jp2(sceneJp2)


def rmclouds():
    print("Executing rmclouds():")
    zipfls=[]
    items=os.listdir(pths.s2aIn)

    for item in items:
        item=pths.s2aIn + '/' + item
        if re.search('^.*\.zip$', item) :
            zipfls.append(item)
            sceneJp2 = unzipJp2(item)
            runGdalbuildvrt(sceneJp2)
            runFmaskMakeAngles(sceneJp2)
            runFmaskStack(sceneJp2)
