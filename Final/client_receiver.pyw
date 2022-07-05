import socket
import tkinter as tk
from tkinter import messagebox
import winsound
import json

HOSTNAME = socket.gethostname()   
IP_ADDRESS = socket.gethostbyname(HOSTNAME)   
PORT = 8080
CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\configure.json'))

SOCKET_PARM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET_PARM.bind((IP_ADDRESS, PORT))
SOCKET_PARM.listen(5)

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
   duration = 1000  # milliseconds
   freq = 440  # Hz
   winsound.Beep(freq, duration)
   duration = 1000  # milliseconds
   freq = 880  # Hz
   winsound.Beep(freq, duration)
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
   while True:
      listen()