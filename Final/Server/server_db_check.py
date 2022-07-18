import psycopg2
import base64
import json
from server_db_tables import check_if_table_exists


def check_database():
    DATABASE_CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\database.json')) # Database connnection info
    try:
        con_postgreSQL = psycopg2.connect(
            host = base64.b64decode(
                (DATABASE_CONFIG["HOSTNAME"]).encode('ascii')).decode('ascii'),
            dbname = base64.b64decode(
                (DATABASE_CONFIG["DATABASE"]).encode('ascii')).decode('ascii'),
            user = base64.b64decode(
                (DATABASE_CONFIG["USERNAME"]).encode('ascii')).decode('ascii'),
            password = base64.b64decode(
                (DATABASE_CONFIG["PWD"]).encode('ascii')).decode('ascii'),
            port = base64.b64decode(
                (DATABASE_CONFIG["PORT_ID"]).encode('ascii')).decode('ascii')
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