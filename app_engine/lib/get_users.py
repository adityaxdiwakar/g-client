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

def getUsers(param):
    http = urllib3.PoolManager()
    url = "https://api.groupme.com/v4/relationships?include_blocked=true"
    if str(param) != "":
        url += "&since=" + str(param)
    url += "&token=" + str(client.token)
    r = http.request('GET', url)
    try:
        return json.loads(r.data)['response']
    except:
        print(r.data)

def getAllUsers():
    user_batch = getUsers("")
    last_timestamp = user_batch[-1]['updated_at_iso8601'] 
    all_users = []
    for x in user_batch:
        all_users.append(x)
    while(True):
        millis = int(round(time.time() * 1000))
        user_batch = getUsers(last_timestamp)
        if len(user_batch) > 0:
            last_timestamp = user_batch[-1]['updated_at_iso8601']  
        else:
            break
        for x in user_batch:
            all_users.append(x)
        print("Took %sms" % (str(int(round(time.time() * 1000)) - millis)))
    with open("bin/users/_user_list.json", "w") as f:
        json.dump(all_users, f, indent=1)


def createDirectories():
    http = urllib3.PoolManager()
    url  = "https://api.groupme.com/v3/users/me"
    url += "?token=" + str(client.token)   
    r = http.request('GET', url)

    response = json.loads(r.data)['response']

    me = {
        "name": response['name'],
        "id": response['id'],
        "avatar_url": response['image_url']
    }

    with open("bin/users/_user_list.json", "r") as f:
        user_data = json.load(f)
        user_data.append(me)

    with open("bin/users/_user_list.json", "w") as f:
        json.dump(user_data, f, indent=1)

    for x in user_data:
        path = "bin/users/" + str(x['id']) 
        try: 
            shutil.rmtree(path)
        except:
            pass
        os.mkdir(path)

