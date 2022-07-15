import os
import json
import time
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

from check import running_status


@dataclass(frozen=True)
class NetworkSettings: # Class for configuration settings. This class is frozen, cannot be changed while code is running.
   PORT = 8080 # Default port for socket connection.
   HOSTNAME = socket.gethostname() # Host fullname.
   DOMAIN = socket.getfqdn() # Get fully qualified domain name from default = HOSTNAME.
   DOMAIN_NAME = DOMAIN.strip(HOSTNAME+".") # Get domain name by stripping the hostname name.
   DOMAIN_NETWORK_ADRESSES = socket.gethostbyname_ex(DOMAIN_NAME) # Get all ip-addresses from domain name.
   LOCAL_ADDRESSES = socket.gethostbyname_ex(HOSTNAME) # Get all ip-addresses from HOST.
   DOMAIN_NETWORK_IP = (sorted(DOMAIN_NETWORK_ADRESSES[2])[0]) # Main DOMAIN NETWORK IP ADDRESS (DC01).
   LOCAL_IP_ADDRESS = (sorted(LOCAL_ADDRESSES[2])[0]) # Local host IP ADDRESS.
   CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\configure.json')) # Main configuration JSON file, which contains information for all clients, that uses the client_modul.
   SYSTRAY_ICON = PIL.Image.open(r'\\dc01\netlogon\Notfall\Logos\logo.png') # Path for logo, used by class SystemtrayIcon.

class SystemtrayIcon: # Used to display the taskbar icon, which contains the following basic functions:
   def __init__(self,queue,parent_pid):
      self.queue = queue
      self.parent_pid = parent_pid
      self.systray(parent_pid)

   def on_clicked_alarm(self): # - function on_clicked_alarm: Initializing alert function (sending).
      sending()

   def about_app(self): # - function about_app: Displaying the "About" window with informations about versions number.
      root = tk.Tk()
      root.geometry("250x100")
      root.title("About NENS")
      root.eval('tk::PlaceWindow . center') # center the "About" window on screen.
      root.iconbitmap(r'\\dc01\netlogon\Notfall\Logos\logo_small.ico')
      label = tk.Label(root, text=f"Network Emergency Notification Service \nVersion: 1.0.0")
      label.pack(side="top", fill="x", pady=10)
      exit_button = tk.Button(root, text="Close", command = root.destroy)
      exit_button.pack()
      root.mainloop()

   def exit_session(self,parent_pid): # - function exit_session: Exits the program, first ends the child processes, then parent process and lastly the SystemtrayIcon_process itself.
      tray = os.getpid() # Get the process ID from current process
      tray_pid = psutil.Process(tray)
      parent_pid = psutil.Process(parent_pid) # Get process ID from parent process
      """
      Closing all child processes recursively for child process in parent.pid.
      Ends the programm completly.
      """
      for child in parent_pid.children(recursive=True):
         if child.pid != tray:
            print(f"|   |_____ Closing child process: {child.pid}" )
            child.kill()
      print(f"|\n|_____Closing parent process: {parent_pid.pid}")
      parent_pid.kill()
      print(f"|\n|________ Closing child process: {tray_pid.pid} (Trayicon)\n")
      tray_pid.kill()

   def systray(self,parent_pid): # - function systray: The main function from this class, it initializes the system tray icon itself with the menu.
      self.icon = icon("alarm", NetworkSettings.SYSTRAY_ICON, menu=menu(
               item("ALARM!!!",SystemtrayIcon.on_clicked_alarm),
               item("About",SystemtrayIcon.about_app, ),
               item("Exit" ,lambda : SystemtrayIcon.exit_session(self,parent_pid)),
            ))
      self.icon.run()

class Socketlisten: # Binds the current host ip address at PORT from class NetworkSettings, while true listens to connections from alarm-clients, if connection is established starts def alarm.
   def __init__(self,queue,parent_pid):
      self.queue = queue
      self.parent_pid = parent_pid
      self.listen(parent_pid)

   def listen(self,parent_pid): # Listen for connections, if connection is true AND device is registred -> sends alert to all known devices.
      try:
         self.SOCKET_PARM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.SOCKET_PARM.bind((NetworkSettings.LOCAL_IP_ADDRESS, NetworkSettings.PORT)) # Binds the local host ip-address
         while True:
            self.SOCKET_PARM.listen(5)
            clientsocket, address = self.SOCKET_PARM.accept() # accepts connections at PORT from class NetworkSettings
            for x in NetworkSettings.CONFIG: # Checks if device is registred in CONIG JSON  
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

class USB_Taster: # If USB device is connected = True, listen to signal from usb device.
   def __init__(self,*args):
      self.usb_listen()

   def usb_listen(self):
    mydll=windll.LoadLibrary(r'\\dc01\netlogon\Notfall\USBaccessX64.dll') # loading dll for usb device
    cw=mydll.FCWInitObject()
    devCnt=mydll.FCWOpenCleware(0)
    if (devCnt != 1) :
      print(f"|\n|   No USB device found")
      tray = os.getpid()
      tray_pid = psutil.Process(tray)
      print(f"|___Closing child process: {tray}")
      tray_pid.kill()

    state = 0

    while (1) : # while usb device is connected, listen to change on state, if usb device is triggered start function sending.
        contact = mydll.FCWGetContact(0, 0)
        newstate = contact & 1
        if (state != newstate):
            if state == 1:
                sending()
        state = newstate

class Shortcut: # Binds a shortcut for triggering the alarm
   def __init__(self):
      self.listen_to_keybord()

   def on_press(self):
    sending()

   def listen_to_keybord(self):
      with keyboard.GlobalHotKeys({
            '<alt>+<ctrl>+n': self.on_press,}) as pressed:
         pressed.join()

def alarm(device): # Visual alert -> Window on screen 99%. Cant be closed while function alarmsoud is running (6,4sec)
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
   try:
      root.destroy()
   except:
      print("Window already destroyed")
   root.mainloop()

def alarmsound(): # Acustic alert -> duration in milliseconds, freq in Hz
   print("alarmsound")
   for x in range(4):
      duration = 800
      freq = 600
      winsound.Beep(freq, duration)
      duration = 800
      freq = 1000
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

   systemtray_process = Process(target=SystemtrayIcon,name="SystemtrayIcon", args=(queue,parent_pid))
   socket_process = Process(target=Socketlisten, name="Socketlisten", args=(queue,parent_pid))
   usb_button_process = Process(target=USB_Taster, name="USB_Taster")
   keybord_process = Process(target=Shortcut, name="Shortcut")

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
   while True:
      time.sleep(10)
      if running_status(child_processes) != 1:
         create_processes(parent_pid)


if __name__ == "__main__":
   freeze_support()
   queue = Queue()
   parent = current_process()
   parent_pid = parent.pid
   print(f"Hostname: {NetworkSettings.HOSTNAME}\nDomain name: {NetworkSettings.DOMAIN_NAME}\nDomain Controller IP-ADDRESS: {NetworkSettings.DOMAIN_NETWORK_IP}\nLocal Host IP-ADDRESS: {NetworkSettings.LOCAL_IP_ADDRESS}")
   print(f"\nParent process: {parent.pid}")
   create_processes(parent_pid)