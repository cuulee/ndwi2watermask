
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
        fmaskMakeAngles(sceneJp2)

fmask_sentinel2makeAnglesImage.py -i ../*.xml -o angles.img
fmask_sentinel2Stacked.py -a allbands.vrt -z angles.img -o cloud.img


subprocess.call([pyFmask,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])
subprocess.call([pyFmask,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])

gdalBuildvrt
fmaskMakeAngles
fmaskStack
