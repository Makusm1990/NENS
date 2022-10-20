import os
import json
import socket
import psutil
import winsound
import PIL.Image
import tkinter as tk
import win32gui, win32con

from ctypes import windll
from pynput import keyboard
from threading import Thread
from datetime import datetime
from tkinter import Label, messagebox
from dataclasses import dataclass
from pystray import Icon as icon, Menu as menu, MenuItem as item
from multiprocessing import Process,Queue,current_process,freeze_support

# Class for configuration settings. This class is frozen, cannot be changed while code is running.
# Default port for socket connection.
# Host fullname.
# Get fully qualified domain name from default = HOSTNAME.
# Get domain name by stripping the hostname name.
# Get all ip-addresses from domain name.
# Get all ip-addresses from HOST.
# Main DOMAIN NETWORK IP ADDRESS (DC01).
# Local host IP ADDRESS.
# Main configuration JSON file, which contains information for all clients, that uses the client_modul.
# Path for logo, used by class SystemtrayIcon.
# Path for USB Buzzer dll.

@dataclass(frozen=True)
class NetworkSettings:
   PORT = 63000
   HOSTNAME = socket.gethostname()
   DOMAIN = socket.getfqdn()
   DOMAIN_NAME = DOMAIN.strip(HOSTNAME+".")
   DOMAIN_NETWORK_ADRESSES = socket.gethostbyname_ex(DOMAIN_NAME)
   LOCAL_ADDRESSES = socket.gethostbyname_ex(HOSTNAME)
   DOMAIN_NETWORK_IP = (sorted(DOMAIN_NETWORK_ADRESSES[2])[0])
   LOCAL_IP_ADDRESS = (sorted(LOCAL_ADDRESSES[2])[0])
   CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\configure.json'))
   SYSTRAY_ICON = PIL.Image.open(r'\\dc01\netlogon\Notfall\Logos\logo.png')
   USB_BUZZER_DLL = (r'\\dc01\netlogon\Notfall\USBaccessX64.dll')

# class SystemtrayIcon, used to display the taskbar icon, which contains the following basic functions:
# - Initializing initialize_alert_threads.
# - Displaying the "About" window with informations about versions number.
# - Exits the program, first ends the child processes, then parent process and lastly the SystemtrayIcon_process itself.
# - The main function from this class, it initializes the system tray icon itself with the menu.

class SystemtrayIcon:
   def __init__(self,queue,parent_pid):
      self.queue = queue
      self.parent_pid = parent_pid
      self.systray(parent_pid)

   def on_clicked_alarm(self):
      initialize_alert_threads()

   def about_app(self):
      root = tk.Tk()
      root.geometry("250x100")
      root.title("About NENS")
      # center the "About" window on screen.
      root.eval('tk::PlaceWindow . center')
      root.iconbitmap(r'\\dc01\netlogon\Notfall\Logos\logo_small.ico')
      label = tk.Label(root, text=f"Network Emergency Notification Service \nVersion: 1.0.0")
      label.pack(side="top", fill="x", pady=10)
      exit_button = tk.Button(root, text="Close", command = root.destroy)
      exit_button.pack()
      root.mainloop()

   # Get the process ID from current process
   # Get process ID from parent process
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
      self.icon = icon("alarm", NetworkSettings.SYSTRAY_ICON,visible=True, title="Notfall-Alarm Client", menu=menu(
               item("ALARM!!!",SystemtrayIcon.on_clicked_alarm),
               item("About",SystemtrayIcon.about_app, ),
               item("Exit" ,lambda : SystemtrayIcon.exit_session(self,parent_pid))
            ))
      self.icon.run()

# class Socketlisten, binds the current host ip address at PORT from class NetworkSettings,
# while true listens to connections from alarm-clients, if connection is established starts def alarm.
# Functions:
# - listen: Listen for connections, if connection is true AND device is registred -> sends alert to all known devices.
class Socketlisten:
   def __init__(self,queue,parent_pid):
      self.queue = queue
      self.parent_pid = parent_pid
      self.listen(parent_pid)

   def kill_task(self,parent_pid):
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

   def listen(self,parent_pid):
      try:
         self.SOCKET_PARM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         # Binds the local host ip-address + PORT
         self.SOCKET_PARM.bind(
            (NetworkSettings.LOCAL_IP_ADDRESS, NetworkSettings.PORT)
            )
         while True:
            self.SOCKET_PARM.listen(1)
            # accepts connections at PORT from class NetworkSettings
            clientsocket, address = self.SOCKET_PARM.accept()
            # Checks if device is registred in CONIG JSON
            for x in NetworkSettings.CONFIG:
               device = NetworkSettings.CONFIG[x]["Alias"]
               if address[0] == NetworkSettings.CONFIG[x]["IPAddress"]:
                  print(f"Alarm from {device}")
                  visual_alert(device)
      except Exception as error:
         print(error)
         print("Client modul is already running")
         self.kill_task(parent_pid)

# class USB_BUZZER: If USB device is connected = True, listen to signal from usb device.
# Functions:
# - check_device: Checks if USB-Buzzer is connected or not.
# - listen_on_usb: while usb device is connected, listen to change on state, if usb device is triggered start function sending.
# - initialize_dll: initialize USB Buzzer, load libary, specify function, bind default 0 to buzzer, check if USB-Buzzer is present, if present == True, go in listining state
class USB_Buzzer:
   def __init__(self,*args):
      self.initialize_dll()

   def check_device(self,devCnt):
      if (devCnt != 1) :
         print(f"|\n|   No USB device found")
         tray = os.getpid()
         tray_pid = psutil.Process(tray)
         print(f"|___Closing child process: {tray}")
         tray_pid.kill()

   def listen_on_usb(self,mydll):
      state = 0
      while (1) :
         contact = mydll.FCWGetContact(0, 0)
         newstate = contact & 1
         if (state != newstate):
               if state == 1:
                  initialize_alert_threads()
         state = newstate

   def initialize_dll(self):
      mydll=windll.LoadLibrary(NetworkSettings.USB_BUZZER_DLL)
      cw=mydll.FCWInitObject()
      devCnt=mydll.FCWOpenCleware(0)
      self.check_device(devCnt)
      self.listen_on_usb(mydll)

# class Key_Shortcut: Binds a Key_shortcut for triggering the alarm via keyboard.
# Functions:
# - listen_to_keybord: check if combination is pressed, when pressed -> sending alarm.
class Key_Shortcut:
   def __init__(self):
      self.listen_to_keybord()

   def on_press(self):
    initialize_alert_threads()

   def listen_to_keybord(self):
      hotkeys = ['<alt>+<ctrl>+n']
      for combination in hotkeys:
         with keyboard.GlobalHotKeys({
            combination: self.on_press,}) as pressed:
            pressed.join()


# Global functions:
# - minimize_all_windows: Minimize all open windows. For the visual alert is being present!
# - visual_alert: Visual alert -> Window on screen 99%. Cant be closed while function alarmsoud is running (6,4sec)
# - acustic_alert: Duration in milliseconds, freq in Hz
# - send_alert_thread: Established a connection to a given IP address.
# - initialize_alert_threads: Creates for each device in NetworkSettings.CONFIG a thread.
# - start_child_processes: Starts all child processes NetworkSettings, SystemtrayIcon, Socketlisten, USB_Buzzer, Key_Shortcut.
# - create_processes: Creates for each class a seperated process.

# def minimize_all_windows(hwnd, ctx):
#     if win32gui.IsWindowVisible(hwnd):
#         if win32gui.GetWindowText(hwnd) != "":
#             win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def visual_alert(device):
   # win32gui.EnumWindows(minimize_all_windows, None)
   date_time = datetime.now().strftime("%H:%M:%S")                            # current date and time

   root= tk.Tk()
   width = round((root.winfo_screenwidth())*0.99)
   height = round((root.winfo_screenheight())*0.99)
   if device == "NENS Server":
      root.title('TEST ALARM')
      root.configure(background='green')
      label_INFO = tk.Label(master=root, text=f"TEST ALARM \n{device}",font=('Arial 70 bold'),bg="yellow",fg="black")
      label_INFO.place(height=250, width=width, y=(height*0.08))
   else:
      root.title('NOTFALL')
      root.configure(background='red')
      label_INFO = tk.Label(master=root, text=f"NOTFALL \n{device}",font=('Arial 70 bold'),bg="yellow",fg="black")
      label_INFO.place(height=250, width=width, y=(height*0.08))

   root.iconbitmap(r'\\dc01\netlogon\Notfall\Logos\logo_small.ico')



   root.geometry(f"{width}x{height}+0+0")

   date = tk.Label(root,text=f"Ausgelöst um: {date_time}",font=('Arial 70 bold'),bg="yellow",fg="black")
   date.place(height=125,width=width, y=(height*0.8))

   alarm_sound = Process(target=acustic_alert)#root.after(1000,acustic_alert)
   alarm_sound.start()
   # Process(target=alarm_sound)

   def on_closing():
    if messagebox.askokcancel("Beenden", "Meldung schließen?"):
        root.destroy()

   root.protocol("WM_DELETE_WINDOW", on_closing)
   # Destroys the root.window after 300000 milliseconds ~ 5 minutes.
   root.lift()
   root.after(300000, root.destroy)
   root.mainloop()

def acustic_alert():
   print("acustic_alert")
   for x in range(4):
      duration = 800
      freq = 600
      winsound.Beep(freq, duration)
      duration = 800
      freq = 1000
      winsound.Beep(freq, duration)

def send_alert_thread(device):
   try:
      client_IP = NetworkSettings.CONFIG[device]["IPAddress"]
      client_parameter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      socket.setdefaulttimeout(2)
      client_parameter.connect((client_IP,NetworkSettings.PORT))
   except (socket.error) as error:
      print(f"Sending alarm to: {client_IP} failed. ERROR: {error}")

def initialize_alert_threads():
   threads = []
   print(f"Devices in Config: {len(NetworkSettings.CONFIG)}")
   for device in NetworkSettings.CONFIG:
      try:
         alert_thread = Thread(target=send_alert_thread, args=(device,))
         threads.append(alert_thread)
         alert_thread.start()
      except Exception as error:
         print(error,device)
         continue
   print(f"Threads: {len(threads)} finished")

def start_child_processes(child_processes):
   for child in child_processes:
      try:
         child.start()
         print(f"|___Child process: {child.pid} // {child.name}")
      except Exception as error:
         print(error)

def create_processes(parent_pid):
   child_processes = []
   # Queue -> Parent_pid to close processes from taskbar recursively.
   systemtray_process = Process(
      target=SystemtrayIcon,name="SystemtrayIcon", args=(queue,parent_pid)
      )
   # Queue -> Parent_pid to close all processes, because application is already running.
   socket_process = Process(
      target=Socketlisten, name="Socketlisten", args=(queue,parent_pid)
      )
   usb_button_process = Process(
      target=USB_Buzzer, name="USB_Buzzer"
      )
   keybord_process = Process(
      target=Key_Shortcut, name="Key_Shortcut"
      )

   child_processes.append(keybord_process)
   child_processes.append(socket_process)
   child_processes.append(systemtray_process)
   child_processes.append(usb_button_process)

   start_child_processes(child_processes)


if __name__ == "__main__":
   freeze_support()
   queue = Queue()
   parent = current_process()
   parent_pid = parent.pid
   print(f"Hostname: {NetworkSettings.HOSTNAME}\nDomain name: {NetworkSettings.DOMAIN_NAME}")
   print(f"Domain Controller IP-ADDRESS: {NetworkSettings.DOMAIN_NETWORK_IP}\nLocal Host IP-ADDRESS: {NetworkSettings.LOCAL_IP_ADDRESS}")
   print(f"\nParent process: {parent.pid}")
   create_processes(parent_pid)