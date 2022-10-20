from datetime import datetime
from tkinter import Label, messagebox
import tkinter as tk

def visual_alert(device):

   date_time = datetime.now().strftime("%H:%M:%S")

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

   def on_closing():
    if messagebox.askokcancel("Beenden", "Meldung schließen?"):
        root.destroy()

   root.protocol("WM_DELETE_WINDOW", on_closing)
   # Destroys the root.window after 300000 milliseconds ~ 5 minutes.
   root.after(300000, root.destroy)
   root.mainloop()

visual_alert("CT-1")