import sys
sys.path.append('../')

import requests
import json
import os
import time
import sys
import shutil
import urllib3
urllib3.disable_warnings()
progress_x = 0

from lib import client_settings as client

rURL = "https://api.groupme.com/v3/groups/"

def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def endProgress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()

def group_name(group):
    with open("bin/groups/" + str(group) + "/g_settings.json", "r") as f:
          data = json.load(f)
          name = data['title'] 
    return name


def last_id(group):
    with open("bin/groups/" + str(group) + "/g_settings.json", "r") as f:
          data = json.load(f)
          id_start = data['messages']['last_msg_id'] 
    return id_start

def group_message_page(group, id_start, isCount):
    #if id_start == -1:
    #  with open("bin/groups/" + str(group) + "/g_settings.json", "r") as f:
    #      data = json.load(f)
    #      id_start = data['messages']['last_msg_id'] 
    http = urllib3.PoolManager()
    if not id_start == -1:
        url = rURL + str(group) + "/messages?token=" + str(client.token) + "&before_id=" + str(id_start) + "&limit=100"
    else:
        url = rURL + str(group) + "/messages?token=" + str(client.token) + "&limit=100"
    r = http.request('GET', url)
    if not isCount:
        try:
            return json.loads(r.data)['response']['messages']
        except:
            return 304
    else:
        try:
            return json.loads(r.data)['response']['count']
        except:
            return 304

def get_all_group_messages(group):
    last_msg_id = -1
    all_data = {}
    msg_num = 0
    start = time.time()*1000
    force_break = False
    startProgress(str(group))
    count = group_message_page(group, last_id, True)
    while True:
        data = group_message_page(group, last_msg_id, False)
        try:
            if data == 304:
                break
        except:
            pass
        
        for x in range(len(data)):
            all_data[msg_num] = data[x]
            msg_num += 1
            if len(all_data) == 50:
                force_break = True
                break
        try:
            last_msg_id = data[-1]['id']
        except:
            break

        progress(len(all_data)/count)
        
        if force_break == True:
            break
    endProgress()

    end = time.time()*1000
    return all_data



def update_messages(group):
    r = get_all_group_messages(group)
    file_dir = "bin/groups/" + str(group) + "/messages"
    try: 
        shutil.rmtree(file_dir)
    except:
        pass
    os.mkdir(file_dir)
    with open(file_dir + "/batch.json", "w") as f:
        json.dump(r, f, indent=1)

def update_all_messages():
    dir = [x for x in os.listdir("bin/groups/") if not x.startswith('_')]

    for x in range(len(dir)):
        group_id = dir[x]
        if not last_id(group_id) == "":
            update_messages(group_id)
