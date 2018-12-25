import json, urllib3, time, tkinter, zmq, shutil, time, json, os, sys
from lib import client_settings as client
from lib import messages    
from lib import get_users as ret_users
from lib import get_groups as ret_groups
from lib import get_chats as ret_chats
from lib import get_group_msgs as ret_gmsgs
from lib import get_chat_msgs as ret_cmsgs
from lib import get_avatars as ret_ava

def init():
    folder_types = ["groups", "chats", "users"]
    for x in folder_types:
        try:
            shutil.rmtree("bin/" + x)
        except:
            pass
        os.mkdir("bin/"+x)
    ret_chats.update()
    ret_cmsgs.update_all_messages()
    ret_groups.update()
    ret_gmsgs.update_all_messages()
    ret_users.createDirectories()
    ret_ava.get_all_users()
    ret_ava.get_all_groups()

#init()

#context = zmq.Context()
#socket = context.socket(zmq.SUB)
# We can connect to several endpoints if we desire, and receive from all.
#socket.connect('tcp://127.0.0.1:1337')

# We must declare the socket as of type SUBSCRIBER, and pass a prefix filter.
# Here, the filter is the empty string, wich means we receive all messages.
# We may subscribe to several filters, thus receiving from all.
#socket.setsockopt_string(zmq.SUBSCRIBE, '')

#print("meow xd")

if sys.argv[1] == "send":
    messages.gCreate(sys.argv[2], Text=sys.argv[3])