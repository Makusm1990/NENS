import psycopg2
import base64
from server_db_credentials  import HOSTNAME,DATABASE,USERNAME,PWD,PORT_ID
from server_db_tables import check_if_table_exists
try:
    con_postgreSQL = psycopg2.connect(
        host = base64.b64decode(HOSTNAME.encode('ascii')).decode('ascii'),
        dbname = base64.b64decode(DATABASE.encode('ascii')).decode('ascii'),
        user = base64.b64decode(USERNAME.encode('ascii')).decode('ascii'),
        password = base64.b64decode(PWD.encode('ascii')).decode('ascii'),
        port = base64.b64decode(PORT_ID.encode('ascii')).decode('ascii')
    )
    if (con_postgreSQL.closed) == False:
        print("Credentials correct.")
        # check if tables already exsits
        try:
            cur_postgre_db = con_postgreSQL.cursor()
            check_if_table_exists(cur_postgre_db,con_postgreSQL)
        except psycopg2.Error as error:
            print(error)
except psycopg2.Error as error:
    print(error)