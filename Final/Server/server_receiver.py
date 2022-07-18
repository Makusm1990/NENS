import os
import json
import socket
import psutil
import base64
import psycopg2
import PIL.Image
import tkinter as tk
from time import sleep
from dataclasses import dataclass
from pystray import Icon as icon, Menu as menu, MenuItem as item
from multiprocessing import Process,Queue,current_process,freeze_support
from server_db_check import check_database


@dataclass(frozen=True)
class NetworkSettings:                                                        # Class for configuration settings. This class is frozen, cannot be changed while code is running.
   PORT = 8080                                                                # Default port for socket connection.
   HOSTNAME = socket.gethostname()                                            # Host fullname.
   DOMAIN = socket.getfqdn()                                                  # Get fully qualified domain name from default = HOSTNAME.
   DOMAIN_NAME = DOMAIN.strip(HOSTNAME+".")                                   # Get domain name by stripping the hostname name.
   DOMAIN_NETWORK_ADRESSES = socket.gethostbyname_ex(DOMAIN_NAME)             # Get all ip-addresses from domain name.
   LOCAL_ADDRESSES = socket.gethostbyname_ex(HOSTNAME)                        # Get all ip-addresses from HOST.
   DOMAIN_NETWORK_IP = (sorted(DOMAIN_NETWORK_ADRESSES[2])[0])                # Main DOMAIN NETWORK IP ADDRESS (DC01).
   LOCAL_IP_ADDRESS = (sorted(LOCAL_ADDRESSES[2])[0])                         # Local host IP ADDRESS.
   CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\configure.json'))        # Main configuration JSON file, which contains information for all clients, that uses the client_modul.
   SYSTRAY_ICON = PIL.Image.open(r'\\dc01\netlogon\Notfall\Logos\logo.png')   # Path for logo, used by class SystemtrayIcon.
   DATABASE_CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\database.json'))# Database connnection info

class PostgreSQL:
   def __init__(self,device):
      print("Connecting to PostgreSQL database...")
      try:
         with psycopg2.connect(
         host = base64.b64decode(
            (NetworkSettings.DATABASE_CONFIG["HOSTNAME"]).encode('ascii')).decode('ascii'),
         dbname = base64.b64decode(
            (NetworkSettings.DATABASE_CONFIG["DATABASE"]).encode('ascii')).decode('ascii'),
         user = base64.b64decode(
            (NetworkSettings.DATABASE_CONFIG["USERNAME"]).encode('ascii')).decode('ascii'),
         password = base64.b64decode(
            (NetworkSettings.DATABASE_CONFIG["PWD"]).encode('ascii')).decode('ascii'),
         port = base64.b64decode(
            (NetworkSettings.DATABASE_CONFIG["PORT_ID"]).encode('ascii')).decode('ascii')
         ) as connection:
            with connection.cursor() as cur_postgre_db:
               print("connection established!")
               self.create_entrie(connection,cur_postgre_db,device)
      except psycopg2.Error as error:
         print(error)
         print("Please check PostgreSQL configuration and restart service!")

   def create_entrie(self,connection,cur_postgre_db,device):
      print("Create entrie for current alert...")
      entrie_NAME = NetworkSettings.CONFIG[device]["Name"]
      entrie_IPv4 = NetworkSettings.CONFIG[device]["IPAddress"]
      insert_data = (entrie_NAME,entrie_IPv4)
      try:
         insert_entrie = 'INSERT INTO notfälle (device,IPv4,date) VALUES (%s,%s, CURRENT_TIMESTAMP)'
         cur_postgre_db.execute(insert_entrie, (insert_data))
         connection.commit()
         print("saved.")
      except (Exception, psycopg2.Error) as error:
         print(error)

class SystemtrayIcon:                                                         # Used to display the taskbar icon, which contains the following basic functions:
   def __init__(self,queue,parent_pid):
      self.queue = queue
      self.parent_pid = parent_pid
      self.systray(parent_pid)

   def about_app(self):                                                       # - Displaying the "About" window with informations about versions number.
      root = tk.Tk()
      root.geometry("250x100")
      root.title("About NENS")
      root.eval('tk::PlaceWindow . center')                                   # center the "About" window on screen.
      root.iconbitmap(r'\\dc01\netlogon\Notfall\Logos\logo_small.ico')
      label = tk.Label(root, text=f"Network Emergency Notification Service \nVersion: 1.0.0")
      label.pack(side="top", fill="x", pady=10)
      exit_button = tk.Button(root, text="Close", command = root.destroy)
      exit_button.pack()
      root.mainloop()

   def exit_session(self,parent_pid):                                         # - Exits the program, first ends the child processes, then parent process and lastly the SystemtrayIcon_process itself.
      tray = os.getpid()                                                      # Get the process ID from current process
      tray_pid = psutil.Process(tray)
      parent_pid = psutil.Process(parent_pid)                                 # Get process ID from parent process

      for child in parent_pid.children(recursive=True):
         if child.pid != tray:
            print(f"|   |_____ Closing child process: {child.pid}" )
            child.kill()
      print(f"|\n|_____Closing parent process: {parent_pid.pid}")
      parent_pid.kill()
      print(f"|\n|________ Closing child process: {tray_pid.pid} (Trayicon)\n")
      tray_pid.kill()

   def systray(self,parent_pid):                                              # - The main function from this class, it initializes the system tray icon itself with the menu.
      self.icon = icon("alarm", NetworkSettings.SYSTRAY_ICON, menu=menu(
               item("About",SystemtrayIcon.about_app, ),
               item("Exit" ,lambda : SystemtrayIcon.exit_session(self,parent_pid)),
            ))
      self.icon.run()

class Socketlisten:                                                           # Binds the current host ip address at PORT from class NetworkSettings,
   def __init__(self,queue,parent_pid):                                       # while true listens to connections from alarm-clients, if connection is established starts def alarm.
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

   def listen(self,parent_pid):                                               # Listen for connections, if connection is true AND device is registred -> sends alert to all known devices.
      try:
         self.SOCKET_PARM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.SOCKET_PARM.bind(
            (NetworkSettings.LOCAL_IP_ADDRESS, NetworkSettings.PORT)          # Binds the local host ip-address + PORT
            )
         while True:
            self.SOCKET_PARM.listen(5)
            clientsocket, address = self.SOCKET_PARM.accept()
            for device in NetworkSettings.CONFIG:
               if address[0] == NetworkSettings.CONFIG[device]["IPAddress"]:
                  print(f"Alarm from {device}")
                  PostgreSQL(device)

      except (socket.error) as error:
         print(error)
         self.kill_task(parent_pid)


def check_child_processes(child_processes):                                   # Checks if all child processes are running returns state = 1 (running) or state 0 (not running)
    print(f"\nChecking child processes:\n")
    state = 0
    for process in child_processes:
        check = psutil.pid_exists(process.pid)
        if check == True:                                                     # Return = 1 (running)
            print(f"|___{process.name} running...")
            state = 1
        else:                                                                 # Return = 0 (not running) if one or more processes are not running, kills >ALL< child processes  -> returns 0
            print(f"|\n|_____{process.name} stopped!!! Restarting {process.name}...\n")
            for x in child_processes:
                x.kill()
            state = 0
    return state

def start_child_processes(child_processes):                                   # Starts all child processes NetworkSettings, SystemtrayIcon, Socketlisten, USB_Buzzer, Key_Shortcut
   for child in child_processes:
      try:
         child.start()
         print(f"|___Child process: {child.pid} // {child.name}")
      except Exception as error:
         print(error)

def create_processes(parent_pid):                                             # Creates for each class a seperated process.
   child_processes = []

   systemtray_process = Process(
      target=SystemtrayIcon,name="SystemtrayIcon", args=(queue,parent_pid)    # Queue -> Parent_pid to close processes from taskbar recursively.
      )
   socket_process = Process(
      target=Socketlisten, name="Socketlisten", args=(queue,parent_pid)       # Queue -> Parent_pid to close all processes, because application is already running.
      )

   child_processes.append(socket_process)
   child_processes.append(systemtray_process)

   start_child_processes(child_processes)                                     # starts all child processes

   while True:                                                                # checks every 60s if all child processes are running, if nessescery restarts the child processes.
      sleep(60)
      if check_child_processes(child_processes) != 1:
         create_processes(parent_pid)


if __name__ == "__main__":
   freeze_support()
   queue = Queue()
   parent = current_process()
   parent_pid = parent.pid
   print(f"Hostname: {NetworkSettings.HOSTNAME}\nDomain name: {NetworkSettings.DOMAIN_NAME}")
   print(f"Domain Controller IP-ADDRESS: {NetworkSettings.DOMAIN_NETWORK_IP}\nLocal Host IP-ADDRESS: {NetworkSettings.LOCAL_IP_ADDRESS}")
   check_database()
   create_processes(parent_pid)