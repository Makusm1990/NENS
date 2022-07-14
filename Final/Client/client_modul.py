import os
import json
import socket
import psutil
import winsound
import PIL.Image
import tkinter as tk

from dataclasses import dataclass
from pynput import keyboard
from threading import Thread
from multiprocessing import Process,Queue,current_process
from ctypes import windll
from tkinter import messagebox
from multiprocessing import Process,Queue,freeze_support
from pystray import Icon as icon, Menu as menu, MenuItem as item


@dataclass(frozen=True)
class NetworkSettings:
   PORT = 8080
   HOSTNAME = socket.gethostname()
   DOMAIN = socket.getfqdn()
   DOMAIN_NAME = DOMAIN.strip(HOSTNAME+".")
   DOMAIN_NETWORK_ADRESSES = socket.gethostbyname_ex(DOMAIN_NAME)
   LOCAL_ADDRESSES = socket.gethostbyname_ex(HOSTNAME)
   DOMAIN_NETWORK_IP = (sorted(DOMAIN_NETWORK_ADRESSES[2])[0])
   LOCAL_IP_ADDRESS = (sorted(LOCAL_ADDRESSES[2])[0])

   CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\configure.json'))
   SYSTRAY_ICON = PIL.Image.open(r'\\dc01\netlogon\Notfall\Logos\logo.png')

class SystemtrayIcon:
   def __init__(self,queue,parent_pid):
      self.queue = queue
      self.parent_pid = parent_pid
      self.systray(parent_pid)

   def on_clicked_alarm(self):
      sending()

   def version_info(self):
      root = tk.Tk()
      root.geometry("250x100")
      root.title("About NENS")
      root.eval('tk::PlaceWindow . center')
      root.iconbitmap(r'\\dc01\netlogon\Notfall\Logos\logo_small.ico')
      label = tk.Label(root, text=f"Network Emergency Notification Service \nVersion: 1.0.0")
      label.pack(side="top", fill="x", pady=10)
      exit_button = tk.Button(root, text="Close", command = root.destroy)
      exit_button.pack()
      root.mainloop()

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
      self.icon = icon("alarm", NetworkSettings.SYSTRAY_ICON, menu=menu(
               item("ALARM!!!",SystemtrayIcon.on_clicked_alarm),
               item("About",SystemtrayIcon.version_info, ),
               item("Exit" ,lambda : SystemtrayIcon.exit_session(self,parent_pid)),
            ))
      self.icon.run()

class Socketlisten:
   def __init__(self,queue,parent_pid):
      self.queue = queue
      self.parent_pid = parent_pid
      self.listen(parent_pid)

   def listen(self,parent_pid):
      try:
         self.SOCKET_PARM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.SOCKET_PARM.bind((NetworkSettings.LOCAL_IP_ADDRESS, NetworkSettings.PORT))
         while True:
            self.SOCKET_PARM.listen(5)
            clientsocket, address = self.SOCKET_PARM.accept()
            for x in NetworkSettings.CONFIG:
               device = NetworkSettings.CONFIG[x]["Alias"]
               if address[0] == NetworkSettings.CONFIG[x]["IPAddress"]:
                  print(f"Alarm from {device}")
                  alarm(device)
      except Exception as error:
         print(error)
         print("Client modul is already running")
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

class USB_Taster:
   def __init__(self,*args):
      self.usb_listen()

   def usb_listen(self):
    mydll=windll.LoadLibrary(r'\\dc01\netlogon\Notfall\USBaccessX64.dll')
    cw=mydll.FCWInitObject()
    devCnt=mydll.FCWOpenCleware(0)

    if (devCnt != 1) :
      print(f"|\n|   No USB device found")
      tray = os.getpid()
      tray_pid = psutil.Process(tray)
      print(f"|___Closing child process: {tray}")
      tray_pid.kill()

    state = 0

    while (1) :
        contact = mydll.FCWGetContact(0, 0)
        newstate = contact & 1

        if (state != newstate):
            if state == 1:
                sending()

        state = newstate

class Shortcut:
   def __init__(self):
      self.listen_to_keybord()

   def on_press(self):
    sending()

   def listen_to_keybord(self):
      with keyboard.GlobalHotKeys({
            '<alt>+<ctrl>+n': self.on_press,}) as pressed:
         pressed.join()

def alarm(device):
   root= tk.Tk()
   root.title('NOTFALL')
   root.iconbitmap(r'\\dc01\netlogon\Notfall\Logos\logo_small.ico')
   root.configure(background='red')

   screensize_width = root.winfo_screenwidth()
   width = round(screensize_width*0.99)
   screensize_height = root.winfo_screenheight()
   height = round(screensize_height*0.99)
   root.geometry(f"{width}x{height}+0+0")

   label_INFO = tk.Label(master=root, text=f"NOTFALL \n{device}",font=('Arial 70 bold'),bg="yellow",fg="black")
   label_INFO.place(height=250, width=width, y=(height*0.08))
   alarm_sound = root.after(1000,alarmsound)
   Thread(target=alarm_sound)
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
   for x in range(4):
      duration = 800  # milliseconds
      freq = 600  # Hz
      winsound.Beep(freq, duration)
      duration = 800  # milliseconds
      freq = 1000  # Hz
      winsound.Beep(freq, duration)

def send_threads(device):
   try:
      client_name = NetworkSettings.CONFIG[device]["Name"]
      client_IP = NetworkSettings.CONFIG[device]["IPAddress"]

      client_name = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      socket.setdefaulttimeout(2)
      client_name.connect((client_IP,NetworkSettings.PORT))
   except (socket.error) as error:
      print(f"Sending alarm to: {client_IP} failed. ERROR: {error}")

def sending():
   threads = []
   print(len(NetworkSettings.CONFIG))
   for device in NetworkSettings.CONFIG:
      try:
         send = Thread(target=send_threads, args=(device,))
         threads.append(send)
         send.start()
      except Exception as error:
         print(error,device)
         continue
   print(f"Threads: {len(threads)} finished")

def create_processes(parent_pid):
   child_processes = []

   systemtray_process = Process(target=SystemtrayIcon,name="Tray Icon", args=(queue,parent_pid))
   socket_process = Process(target=Socketlisten, name="Socket listener", args=(queue,parent_pid))
   usb_button_process = Process(target=USB_Taster, name="USB Buzzer")
   keybord_process = Process(target=Shortcut, name="Keybord shortcut")

   child_processes.append(keybord_process)
   child_processes.append(socket_process)
   child_processes.append(systemtray_process)
   child_processes.append(usb_button_process)

   for child in child_processes:
      try:
         child.start()
         print(f"|___Child process: {child.pid} // {child.name}")
      except Exception as error:
         print(error)


if __name__ == "__main__":
   freeze_support()
   queue = Queue()
   parent = current_process()
   parent_pid = parent.pid
   print(f"Hostname: {NetworkSettings.HOSTNAME}\nDomain name: {NetworkSettings.DOMAIN_NAME}\nDomain Controller IP-ADDRESS: {NetworkSettings.DOMAIN_NETWORK_IP}\nLocal Host IP-ADDRESS: {NetworkSettings.LOCAL_IP_ADDRESS}")
   print(f"\nParent process: {parent.pid}")
   create_processes(parent_pid)