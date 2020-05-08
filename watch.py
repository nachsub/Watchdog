import datetime as dt
from datetime import datetime
import subprocess as sp
import ctypes
import psutil
import os

threshold = 60

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects;


def kill(pid):
    """kill function for Win32"""
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.OpenProcess(1, 0, pid)
    return (0 != kernel32.TerminateProcess(handle, 0))

file = open("watchdog.txt", "r+")
while True:
    contents = file.read()
    if len(contents) > 0:
        logtime = datetime.strptime(contents, '%m/%d/%Y %I:%M:%S')
        curtime = dt.datetime.now()
        delta_seconds = (curtime - logtime).seconds
        if (delta_seconds > threshold):
            ids = findProcessIdByName("py.exe")
            print(len(ids))
            if len(ids) > 0:
                print("kill(pid)")
                pid  = ids[0]
                print(pid['pid'])
                kill(pid['pid'])
                os.startfile("watchdog.py")
