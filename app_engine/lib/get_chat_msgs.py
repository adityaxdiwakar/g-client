import sys
sys.path.append('../')

import requests
import json
import os
import time
import urllib3
urllib3.disable_warnings()

from lib import client_settings as client

rURL = "https://api.groupme.com/v3/direct_messages"

def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 200)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def endProgress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()

def user_name(user):
    with open("bin/chats/" + str(user) + "/c_settings.json", "r") as f:
          data = json.load(f)
          name = data['name']
    return name


def last_id(user):
    with open("bin/chats/" + str(user) + "/c_settings.json", "r") as f:
        data = json.load(f)
        id_start = data['messages']['last_msg_id']
    return id_start


def user_message_page(user, id_start=-1, isCount=False):
    http = urllib3.PoolManager()
    if not id_start == -1:
        url = rURL +"?token=" + str(client.token) + "&before_id=" + str(id_start) + "&other_user_id=" + str(user)
    else:
        url = rURL +"?token=" + str(client.token) + "&other_user_id=" + str(user)
    r = http.request('GET', url)
    if not isCount:
        try:
            return json.loads(r.data)['response']['direct_messages']
        except:
            return 304
    else:
        try:
            return json.loads(r.data)['response']['count']
        except:
            return 304


def get_all_user_messages(user):
    last_msg_id = -1
    all_data = {}
    msg_num = 0
    start = time.time()*1000
    force_break = False
    startProgress(str(user))
    count = user_message_page(user, id_start=-1, isCount=True)
    while True:
        progress(len(all_data)/count)
        data = user_message_page(user, last_msg_id)
        try:
            if data == 304:
                break
        except:
            pass

        for x in range(len(data)):
            all_data[msg_num] = data[x]
            msg_num += 1
            if len(all_data) == 500:
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

def update_messages(user):
    r = get_all_user_messages(user)
    file_dir = "bin/chats/" + str(user) + "/messages"
    try:
        os.rmdir(file_dir)
    except:
        pass
    os.mkdir(file_dir)
    with open(file_dir + "/batch.json", "w") as f:
        json.dump(r, f, indent=1)

def update_all_messages():
    dir = [x for x in os.listdir("bin/chats/") if not x.startswith('_')]

    for x in range(len(dir)):
        user_id = dir[x]
        if not last_id(user_id) == "":
            update_messages(user_id)
