import socket
import winsound
import json
import pystray
import PIL.Image
import tkinter as tk
import threading
import os

from client_sender import sending as alarm_from_taskbar
from tkinter import messagebox


HOSTNAME = socket.gethostname()   
IP_ADDRESS = socket.gethostbyname(HOSTNAME)   
PORT = 8080
CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\configure.json'))
SYSTRAY_ICON = PIL.Image.open(r"\\dc01\netlogon\Notfall\Notfall.ico")

SOCKET_PARM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET_PARM.bind((IP_ADDRESS, PORT))
SOCKET_PARM.listen(5)


class SystemtrayIcon:
   def __init__(self):
      self.thread_systray = threading.Thread(target=self.systray)
      self.thread_systray.start()

   def on_clicked_alarm(self):
      alarm_from_taskbar()    
   
   def version_info(self):
      print("Version 1.0.0")

   def systray(self):
      self.icon = pystray.Icon("alarm", SYSTRAY_ICON, menu=pystray.Menu(
               pystray.MenuItem("ALARM!!!",SystemtrayIcon.on_clicked_alarm),
               pystray.MenuItem("Version",SystemtrayIcon.version_info),
               pystray.MenuItem("Exit", exit_session),
            ))
      self.icon.run()

def exit_session():
   os._exit(1)

def alarm(device):
   root= tk.Tk()
   root.title('NOTFALL')
   root.configure(background='red')

   screensize_width = root.winfo_screenwidth()
   width = round(screensize_width*0.99)
   screensize_height = root.winfo_screenheight()
   height = round(screensize_height*0.99)
   root.geometry(f"{width}x{height}")

   label_INFO = tk.Label(master=root, text=f"NOTFALL {device}",font=('Times 50'))
   label_INFO.place(height=100, width=width, y=(height*0.02))
   root.after(1000,alarmsound)
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

   
def listen(): 
   clientsocket, address = SOCKET_PARM.accept()
   for x in CONFIG:
      device = CONFIG[x]["Name"]
      if address[0] == CONFIG[x]["IPAddress"]:         
         print(f"Alarm from {device}")
         alarm(device)
  

if __name__ == "__main__": 
   SystemtrayIcon()
   while True:
      listen()
   
      
      