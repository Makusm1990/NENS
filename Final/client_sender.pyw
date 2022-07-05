import socket
import json
import threading

CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\configure.json'))
PORT = 8080
       
def send_threads(device):
    print(device)
    try:
        CONFIG[device]["Name"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CONFIG[device]["Name"].connect((CONFIG[device]["IPAddress"],PORT))
    except ConnectionRefusedError as error:
        print(CONFIG[device]["IPAddress"],error)

def main():     
    for device in CONFIG:
        try:
            send = threading.Thread(target=send_threads, args=(device,))
            send.start()
        except Exception:
            continue

if __name__ == "__main__":
    main()


