import sys
sys.path.append('../')

import requests
import sys
import shutil
import json
import os
import time
import urllib3
import urllib.request
urllib3.disable_warnings()

from lib import client_settings as client

def get_single_user(link, user_id):
    link_segs = link.split('.')
    try:
        urllib.request.urlretrieve(link, "bin/users/" + str(user_id) + "/avatar." + link_segs[3])
    except: 
        urllib.request.urlretrieve(link, "bin/users/" + str(user_id) + "/avatar.jpeg")

def get_all_users():
    with open("bin/users/_user_list.json", "r") as f:
        chat_data = json.load(f)
    for x in chat_data:
        if x['avatar_url'] == None or x['avatar_url'] == '':
            print("No avatar for " + str(x['name']))
        else:
            get_single_user(x['avatar_url'], x['id'])


def get_single_group(link, group_id):
    urllib.request.urlretrieve(link, "bin/groups/" + str(group_id) + "/avatar.jpeg")

def get_all_groups():
    os.mkdir("bin/groups/null")
    get_single_group('https://img.adityadiwakar.me/u/7U36.jpg', 'null')
    with open("bin/groups/_group_list.json", "r") as f:
        group_data = json.load(f)
    for x in range(len(group_data)):
        group = group_data[str(x)]
        if group['img_url'] == None or group['img_url'] == '' or group['img_url'] == 'None':
            print("No avatar for " + str(group['title']))
        else:
            get_single_group(group['img_url'], group['id'])
