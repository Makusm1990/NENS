import os
import json
import queue
import socket
import psutil
import pystray
import winsound
import threading
import PIL.Image
import tkinter as tk
import multiprocessing

from ctypes import *
from tkinter import messagebox
from multiprocessing import Process,Queue,freeze_support


HOSTNAME = socket.gethostname()   
IP_ADDRESS = socket.gethostbyname(HOSTNAME)   
PORT = 8080
CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\configure.json'))
SYSTRAY_ICON = PIL.Image.open(r'D:\x_Notfall\Final\Client\logo.png')


class SystemtrayIcon:
   def __init__(self,queue,parent_pid):
      self.queue = queue
      self.parent_pid = parent_pid
      self.systray(parent_pid)

   def on_clicked_alarm(self):
      sending()   
   
   def version_info(self):
      print("Version 1.0.0")
   
   def exit_session(self,parent_pid):      
      tray = os.getpid()
      tray_pid = psutil.Process(tray)
      parent_pid = psutil.Process(parent_pid)

      for child in parent_pid.children(recursive=True):
         if child.pid != tray:
            print(f"|   |_____ Closing child process: {child.pid}" )
            child.kill()
      print(f"|\n|_____Closing parent process: {parent_pid.pid}")
      parent_pid.kill()
      print(f"|\n|________ Closing child process: {tray_pid.pid} (Trayicon)\n")
      tray_pid.kill()
      
   def systray(self,parent_pid):
      self.icon = pystray.Icon("alarm", SYSTRAY_ICON, menu=pystray.Menu(
               pystray.MenuItem("ALARM!!!",SystemtrayIcon.on_clicked_alarm),
               pystray.MenuItem("Version",SystemtrayIcon.version_info),
               pystray.MenuItem("Exit", lambda : SystemtrayIcon.exit_session(self,parent_pid)),
            ))
      self.icon.run()

class Socketlisten:
   def __init__(self,*args):
      self.listen()

   def listen(self):
      self.SOCKET_PARM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.SOCKET_PARM.bind((IP_ADDRESS, PORT))
      while True: 
         self.SOCKET_PARM.listen(1) 
         clientsocket, address = self.SOCKET_PARM.accept()
         for x in CONFIG:
            device = CONFIG[x]["Alias"]
            if address[0] == CONFIG[x]["IPAddress"]:         
               print(f"Alarm from {device}")
               alarm(device)

class USB_Taster:
   def __init__(self,*args):
      self.usb_listen()
      
   def usb_listen(self):
    mydll=windll.LoadLibrary(r"D:\x_Notfall\Final\Client\USBaccessX64.dll")
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
                sending()

        state = newstate

def alarm(device):
   root= tk.Tk()
   root.title('NOTFALL')
   root.configure(background='red')

   screensize_width = root.winfo_screenwidth()
   width = round(screensize_width*0.99)
   screensize_height = root.winfo_screenheight()
   height = round(screensize_height*0.99)
   root.geometry(f"{width}x{height}")

   label_INFO = tk.Label(master=root, text=f"NOTFALL \n{device}",font=('Arial 70'),bg="yellow",fg="black")
   label_INFO.place(height=250, width=width, y=(height*0.08))
   alarm_sound = root.after(1000,alarmsound)
   threading.Thread(target=alarm_sound)   
   messagebox.showinfo(title=F"NOTFALL {device}",message="Meldung schließen?",icon="warning")
   #
   # Bestätigung an Sender schicken das die Meldung gelesen wurde
   #
   try:
      root.destroy()
   except:
      print("Window already destroyed")
   root.mainloop() 

def alarmsound():
   print("alarmsound")
   for x in range(2):
      duration = 1000  # milliseconds
      freq = 440  # Hz
      winsound.Beep(freq, duration)
      duration = 1000  # milliseconds
      freq = 880  # Hz
      winsound.Beep(freq, duration)    

def send_threads(device):
    print(device)
    try:
        CONFIG[device]["Name"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CONFIG[device]["Name"].connect((CONFIG[device]["IPAddress"],PORT))
    except ConnectionRefusedError as error:
        print(CONFIG[device]["IPAddress"],error)

def sending():     
   for device in CONFIG:
      try:
         send = threading.Thread(target=send_threads, args=(device,))
         send.start()
      except Exception:
         continue

def create_processes(parent_pid):
   a = Process(target=SystemtrayIcon, args=(queue,parent_pid))
   b = Process(target=Socketlisten)
   c = Process(target=USB_Taster)   
   a.start()
   b.start()
   c.start()

if __name__ == "__main__": 
   freeze_support()
   queue = Queue()
   parent = multiprocessing.current_process()
   parent_pid = parent.pid
   create_processes(parent_pid) 
   
   print(f"\nParent process: {parent.pid}")

      
   
      
      

   
      
      