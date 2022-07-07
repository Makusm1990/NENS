from ctypes import *
import time
mydll=windll.LoadLibrary(r"D:\x_Notfall\USBaccessX64.dll") # sometimes, the full path must be declared
cw=mydll.FCWInitObject()
devCnt=mydll.FCWOpenCleware(0)

if (devCnt != 1) :
    print("no device found")
    exit()

state = 0

while (1) :
    contact = mydll.FCWGetContact(0, 0)
    newstate = contact & 1
    changed = contact & 0x10000

    if (state != newstate):
        print(state)
    else :
        if (changed != 0):
            print(newstate)

    state = newstate
    

    