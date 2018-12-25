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

rURL = "https://api.groupme.com/v3/chats"

def get_paged_chats(page, isMembers=True):
    http = urllib3.PoolManager()
    url = rURL + "?token=" + str(client.token) + "&page=" + str(page)
    r = http.request('GET', url)
    try:
        return json.loads(r.data)['response']
    except:
        return json.dumps(json.loads(r.data), indent=2)

def get_all_chats():
    allChats = {}
    isMore = True
    chat_num = 0
    page = 1
    while isMore == True:
        group_focus = get_paged_chats(page)
        if(len(group_focus) == 0):
            break
        page += 1

        for num in range(len(group_focus)):
            group_view = group_focus[num]
            allChats[chat_num] = templateData(id=group_view['other_user']['id'],
                                                last_msg_id=group_view['last_message']['id'],
                                                name=group_view['other_user']['name'],
                                                last_created=group_view['last_message']['created_at'],
                                                img_url=group_view['other_user']['avatar_url'])
            chat_num += 1


    return allChats

def templateData(name="", id="", last_msg_id="", last_created="", img_url=""):
    data = {
        "name":name,
        "id":id,    
        "img_url":img_url,
        "messages": {
            "last_msg_id":last_msg_id,
            "last_created":last_created
        }
    }
    return data

def createDirectories(group_data):
    dir = [x for x in os.listdir("bin/chats/") if not x.startswith('_')]

    for x in range(len(dir)):
        shutil.rmtree("bin/chats/" + str(dir[x]))

    for x in range(len(group_data)):
        os.mkdir("bin/chats/" + str(group_data[x]['id']))

user_data = []

def userIndexOf(user):
    sing_user = {
        "name":user['name'],
        "id":user['id'],
        "img_url":user['img_url']
    }
    found_dupe = False
    for x in user_data:
        if x['id'] == sing_user['id']:
            found_dupe = True
    if found_dupe == False:
        user_data.append(sing_user)


def updateDirectories(chat_data):
    #print(user_data)
    for x in range(len(chat_data)):
        c_id = chat_data[x]['id']
        with open("bin/chats/" + str(c_id) + "/c_settings.json", "w") as f:
            userIndexOf(chat_data[x])
            data = {
                "name":chat_data[x]["name"],
                "messages": {
                    "last_msg_id":chat_data[x]["messages"]["last_msg_id"],
                    "last_created":chat_data[x]["messages"]["last_created"]
                }
            }
            json.dump(data, f, indent=1)
            chat_data[x].pop("messages")
    with open("bin/chats/_chat_list.json", "w") as f:
        json.dump(chat_data, f, indent=1)

    raw = []
    for value in user_data:
        if value not in raw:    
            raw.append(value)


    with open("bin/users/_user_list.json", "w") as f:
        json.dump(raw, f, indent=1)


def updateMaster(chat_data):
    with open("bin/chats/_chat_list.json", "w") as f:
        json.dump(chat_data, f, indent=1)

def update():
    chat_data = get_all_chats()
    createDirectories(chat_data)
    updateMaster(chat_data)
    updateDirectories(chat_data)
    return chat_data