import sys
sys.path.append('../')

import requests
import json
import os
import time
import urllib3
urllib3.disable_warnings()

from lib import client_settings as client

def get_user():
    http = urllib3.PoolManager()
    url = "https://api.groupme.com/v3/users/me?token=" + str(client.token)

