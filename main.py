from urllib.request import Request, urlopen
from urllib import parse
from pypresence import Presence
import requests
import json
import os
import time
import psutil
from subprocess import check_output

def checkProcess(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


backend = "http://galaxybotl.altervista.org{}"
client_id = 766050828951748640

def getData(userid):
    data = {
        'action':'GET',
        'data':{
            'userid':userid,
        }
    }
    dumped = json.dumps(data)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(backend.format("/data2.php"),data=dumped,headers=headers).text
    return json.loads(response)

def getUserId(username):
    url = "https://api.roblox.com/users/get-by-username?username={}".format(username)
    response = requests.get(url).text
    return json.loads(response)["Id"]

def main():
    username = input("ROBLOX Username: ")
    userId = getUserId(username)
    try:
        print("Your userid is {}".format(userId))
        print("To connect this to Roblox Studio, follow the README.md instructions!")
        rpc = Presence(client_id,pipe=0)
        rpc.connect()
        start = int(time.time())
        rpc.update(state="Idle",start=start,large_image="logo")
        previously = None
        while True:
            running = checkProcess("RobloxStudioBeta")
            if previously == None:
                previously = running
            if running == True:
                if previously == False:
                    rpc.connect()
                data = getData(userId)
                editing = data["editing"]
                if editing == "false":
                    rpc.update(state="Idle",large_image="logo",large_text="Made by Jesse#0877",start=start)
                else:
                    #scriptName = data[2]
                    #path = data[3]
                    #game = data[5]
                    #lines = data[6]
                    scriptName = data["scriptName"]
                    path = data["path"]
                    game = data["game"]
                    lines = data["lines"]
                    scriptType = data["script"]

                    small_image = "lua"
                    small_text = "lua"

                    if scriptType == "script":
                        small_image = "script"
                        small_text = "Script"
                    elif scriptType == "modulescript":
                        small_image = "modulescript"
                        small_text = "ModuleScript"
                    elif scriptType == "localscript":
                        small_image = "localscript"
                        small_text = "LocalScript"
                    rpc.update(state="Editing Script: {}".format(scriptName) + ", {} Lines.".format(lines),details=game,large_image="logo",large_text="Made by Jesse#0877",small_image=small_image,small_text=small_text,start=start)
            else:
                rpc.close()
            previously = running
            time.sleep(15)
    except Exception as e:
        print("An error occured: {}\nPlease send this error to Jesse#0877 on discord!".format(e))
        os.system('pause')
main()
