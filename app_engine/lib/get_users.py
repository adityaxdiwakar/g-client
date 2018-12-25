import sys
sys.path.append('../')

import requests
import sys
import shutil
import json
import os
import time
import urllib3
urllib3.disable_warnings()

from lib import client_settings as client

def createDirectories():
    with open("bin/users/_user_list.json", "r") as f:
        user_data = json.load(f)

    for x in user_data:
        path = "bin/users/" + str(x['id']) 
        try: 
            shutil.rmtree(path)
        except:
            pass
        os.mkdir(path)
