
import os
import getPaths as pths
from defCloudMask import unzipJp2,runGdalbuildvrt,runFmaskMakeAngles,runFmaskStack
import re

#### list zip files

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
