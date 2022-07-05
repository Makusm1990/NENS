import socket
import json
from server_db_credentials import *

HOSTNAME = socket.gethostname()   
IP_ADDRESS = socket.gethostbyname(HOSTNAME)   
PORT = 8080
CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\configure.json'))


SOCKET_PARM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET_PARM.bind((IP_ADDRESS, PORT))
SOCKET_PARM.listen(5)

cur_postgre_db = con_postgreSQL.cursor()

def create_entrie(device):
    entrie_NAME = CONFIG[device]["Name"]
    entrie_IPv4 = CONFIG[device]["IPAddress"]
    insert_data = (entrie_NAME,entrie_IPv4)

    try:
        insert_entrie = 'INSERT INTO notfälle (device,IPv4,date) VALUES (%s,%s, CURRENT_TIMESTAMP)'
        cur_postgre_db.execute(insert_entrie, (insert_data))
        con_postgreSQL.commit()
    except (Exception, psycopg2.Error) as error:
        print(error)


#con_postgreSQL.close()


def listen(): 
   clientsocket, address = SOCKET_PARM.accept()
   for device in CONFIG:
      #device = CONFIG[devices]["Name"]
      if address[0] == CONFIG[device]["IPAddress"]:         
         print(f"Alarm from {device}")
         create_entrie(device)

if __name__ == "__main__":  
   while True:
      listen()