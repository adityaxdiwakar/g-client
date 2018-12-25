import sys
sys.path.append('../')

import urllib3
import json
import os.path

rUrl = "https://api.groupme.com/v3/"

with open('bin/_main.json') as f:
    data = json.load(f)
token = data["token"]

http = urllib3.PoolManager()
url  = "https://api.groupme.com/v3/users/me"
url += "?token=" + str(token)
r = http.request('GET', url)

with open("bin/_main.json", "r") as f:
    data = json.load(f)
    
data.update({
    "id":json.loads(r.data)['response']['id']
})

with open("bin/_main.json", "w") as f:
    json.dump(data, f, indent=1)

uID = data["id"]