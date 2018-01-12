import os
import time
from getPaths import *

current_time = time.time()

for f in os.listdir(sarOut):
    creation_time = os.path.getctime(satOut + "/" + f)
    if (current_time - creation_time) // (24 * 3600) >= 14:
        os.unlink(satOut + "/" +f)
        print('{} removed'.format(f))

for f in os.listdir(sarIn):
    creation_time = os.path.getctime(satIn + "/" +f)
    if (current_time - creation_time) // (24 * 3600) >= 14:
        os.unlink(satIn + "/" + f)
        print('{} removed'.format(f))

for f in os.listdir(polOut):
    creation_time = os.path.getctime(polOut + "/" + f)
    if (current_time - creation_time) // (24 * 3600) >= 14:
        os.unlink(polOut + "/" +f)
        print('{} removed'.format(f))
