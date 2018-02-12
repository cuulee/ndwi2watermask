
import os
from getPaths import *
from defCloudMask import *
import re

#### list zip files

zipfls=[]
items=os.listdir(s2aIn)
item=items[1]



for item in items:
    item=s2aIn + '/' + item
    if re.search('^.*\.zip$', item) :
        zipfls.append(item)
        sceneJp2 = unzipJp2(item)
        runGdalbuildvrt(sceneJp2)
        runFmaskMakeAngles(sceneJp2)
        runFmaskStack(sceneJp2)
