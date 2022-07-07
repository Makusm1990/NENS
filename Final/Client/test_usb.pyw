from ctypes import *
from client_sender import sending as client_sent


def usb_listen():
    mydll=windll.LoadLibrary(r"\\dc01\netlogon\Notfall\USBaccessX64.dll")
    cw=mydll.FCWInitObject()
    devCnt=mydll.FCWOpenCleware(0)

    if (devCnt != 1) :
        print("no device found")
        exit()

    state = 0

    while (1) :
        contact = mydll.FCWGetContact(0, 0)
        newstate = contact & 1

        if (state != newstate):
            if state == 1:
                client_sent()

        state = newstate
        
usb_listen()
    