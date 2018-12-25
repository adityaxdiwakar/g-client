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

rURL = "https://api.groupme.com/v3/groups"

def getPagedGroups(page, isMembers=True):
    data = ""
    count = 0
    while True:
        http = urllib3.PoolManager()
        if isMembers:
            url = rURL + "?token=" + str(client.token) + "&page=" + str(page)
        else:
            url = rURL + "?token=" + str(client.token) + "&page=" + str(page) + "&omit=memberships"
        r = http.request('GET', url)
        if count > 20:
            data = 1001
            break
        try:
            data = json.loads(r.data)['response']
        except:
            count+=1
            continue
        break
    return data

def get_all_groups():
    allGroups = {}
    isMore = True
    group_num = 0
    page = 1
    while isMore == True:
        group_focus = getPagedGroups(page)
        page += 1

        for num in range(len(group_focus)):
            group_view = group_focus[num]
            allGroups[group_num] = templateData(title=group_view['name'],
                                                id=group_view['id'],
                                                desc=group_view['description'],
                                                img_url=group_view['image_url'],
                                                silent_force=group_view['office_mode'],
                                                share_url=group_view['share_url'],
                                                members=group_view['members'],
                                                last_msg_id=group_view['messages']['last_message_id'],
                                                last_created=group_view['messages']['last_message_created_at'])
            group_num += 1

        if len(group_focus) < 10:
            break

    return allGroups

def templateData(title="", id="", desc="", img_url="", silent_force="", share_url="", members="",last_msg_id="", last_created=""):
    data = {
        "title":title,
        "id":id,
        "desc":desc,
        "img_url":img_url,
        "silent_force":silent_force,
        "share_url":share_url,
        "members":members,
        "messages": {
            "last_msg_id":last_msg_id,
            "last_created":last_created
        }
    }
    return data

def createDirectories(group_data):
    dir = [x for x in os.listdir("bin/groups/") if not x.startswith('_')]

    for x in range(len(dir)):
        shutil.rmtree("bin/groups/" + str(dir[x]))

    for x in range(len(group_data)):
        os.mkdir("bin/groups/" + str(group_data[x]['id']))

user_data = []

def get_user_data():
    with open("bin/users/_user_list.json", "r") as f:
        u_data = json.load(f)
    return u_data

def scrape_user_data():
    foo = []
    for x in range(len(user_data)):
        foo.append(user_data[x]['id'])
    return foo

def userIndexOf(user):
    sing_user = {
        "name":user['name'],
        "id":user['user_id'],
        "img_url":user['image_url']
    }
    found_dupe = False
    for x in user_data:
        if x['id'] == sing_user['id']:
            found_dupe = True
    if found_dupe == False:
        user_data.append(sing_user)
            


def updateDirectories(group_data):
    user_data = get_user_data()
    for x in range(len(group_data)):
        with open("bin/groups/" + group_data[x]['id'] + "/users.json", "w") as f:
            json.dump(group_data[x]['members'], f, indent=1)
            
            for y in range(len(group_data[x]['members'])):
                userIndexOf(group_data[x]['members'][y])

            group_data[x].pop('members', None)
        with open("bin/groups/" + group_data[x]['id'] + "/g_settings.json", "w") as f:
            data = {
                "title":group_data[x]["title"],
                "desc":group_data[x]["desc"],
                "img_url":group_data[x]["img_url"],
                "silent_force":group_data[x]["silent_force"],
                "share_url":group_data[x]["share_url"],
                "messages": {
                    "last_msg_id":group_data[x]["messages"]["last_msg_id"],
                    "last_created":group_data[x]["messages"]["last_created"]
                }
            }
            json.dump(data, f, indent=1)
            group_data[x].pop("desc")
            group_data[x].pop("silent_force")
            group_data[x].pop("share_url")
            group_data[x].pop("messages")
    with open("bin/groups/_group_list.json", "w+") as f:
        json.dump(group_data, f, indent=1)

    with open("bin/users/_user_list.json", "w+") as f:
        json.dump(user_data, f, indent=1)

def updateMaster(group_data):
    with open("bin/groups/_group_list.json", "w+") as f:
        json.dump(group_data, f, indent=1)

def update():
    group_data = get_all_groups()
    createDirectories(group_data)
    updateMaster(group_data)
    updateDirectories(group_data)
    return group_data