
import os
import subprocess
from getPaths import *

import zipfile

import re

#### list zip files

zipfls=[]
items=os.listdir(s2aIn)

for item in items:
    if re.search('^.*\.zip$', item) :
        zipfls.append(item)
        sceneJp2 = unzipJp2(item)
        doGdalbuildvrt(sceneJp2)
        

fmask_sentinel2makeAnglesImage.py -i ../*.xml -o angles.img
fmask_sentinel2Stacked.py -a allbands.vrt -z angles.img -o cloud.img


subprocess.call([pyFmask,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])
subprocess.call([pyFmask,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])

gdalBuildvrt
fmaskMakeAngles
fmaskStack
