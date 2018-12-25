import sys
sys.path.append('../')

import requests
import json
import os
import time
import urllib3
urllib3.disable_warnings()

from lib import client_settings as client

def gCreate(gID, Text=None, Attachments=None):
    http = urllib3.PoolManager()
    payload = {
        "message": {
            "source_guid": int(round(time.time() * 1000)),
            "text": Text
        }
    }
    url = client.rUrl + "groups/" + str(gID) + "/messages?token=" + client.token
    r = http.request('POST', url,
                headers={'Content-Type': 'application/json'},
                body=json.dumps(payload))

def uCreate(uID, Text=None, Attachments=None):
    http = urllib3.PoolManager()
    payload = {
        "direct_message": {
            "source_guid": int(round(time.time() * 1000)), 
            "recipient_id": uID, 
            "text": Text
        }
    }
    url = client.rUrl + "direct_messages?token=" + client.token
    http.request('POST', url, 
                headers={'Content-Type': 'application/json'}, 
                body = json.dumps(payload))

def nLike(mID, cID):
    http = urllib3.PoolManager()
    url = client.rUrl + "messages/" + cID + "/" + mID + "/like?token=" + client.token
    http.request('POST', url)

def dLike(mID, cID):
    http = urllib3.PoolManager()
    url = client.rUrl + "messages/" + cID + "/" + mID + "/unlike?token=" + client.token
    http.request('POST', url)