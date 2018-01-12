import os
import time
from getPaths import *

current_time = time.time()

for f in os.listdir(sarOut):
    creation_time = os.path.getctime(f)
    if (current_time - creation_time) // (24 * 3600) >= 14:
        os.unlink(f)
        print('{} removed'.format(f))

for f in os.listdir(sarIn):
    creation_time = os.path.getctime(f)
    if (current_time - creation_time) // (24 * 3600) >= 14:
        os.unlink(f)
        print('{} removed'.format(f))

for f in os.listdir(polOut):
    creation_time = os.path.getctime(f)
    if (current_time - creation_time) // (24 * 3600) >= 14:
        os.unlink(f)
        print('{} removed'.format(f))
