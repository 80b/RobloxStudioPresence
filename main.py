from urllib.request import Request, urlopen
from urllib import parse
from pypresence import Presence
import requests
import json
import os
import time
from subprocess import check_output

def get_pid(name):
    return check_output(["pidof",name])


backend = "http://galaxybotl.altervista.org{}"
client_id = 766050828951748640

def getData(userid):
    data = {
        'action':'GET',
        'data':{
            'userid':userid
        }
    }
    dumped = json.dumps(data)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(backend.format("/data.php"),data=dumped,headers=headers).text
    return json.loads(response)

def getUserId(username):
    url = "https://api.roblox.com/users/get-by-username?username={}".format(username)
    response = requests.get(url).text
    return json.loads(response)["Id"]

def main():
    username = input("ROBLOX Username: ")
    try:
        userId = getUserId(username)
        print("Your userid is {}".format(userId))
        print("To connect this to Roblox Studio, use the plugin and enter your username when prompted.")
        print("Waiting for pypresence..")
        rpc = Presence(client_id,pipe=0)
        rpc.connect()
        start = int(time.time())
        rpc.update(state="Idle",start=start,large_image="logo")
        print("Done!")
        while True:
            data = getData(userId)
            if data[1] == "false":
                rpc.update(state="Idle",large_image="logo",large_text="Made by Jesse#0877",start=start)
            else:
                scriptName = data[2]
                path = data[3]
                game = data[5]
                rpc.update(state="Editing Script: {}".format(scriptName),details=game,large_image="logo",large_text="Made by Jesse#0877",small_image="lua",small_text="Lua",start=start)
            time.sleep(15)
    except Exception as e:
        print("An error occured: {}\nPlease send this error to Jesse#0877 on discord!".format(e))
        os.system('pause')
main()
