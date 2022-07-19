import psycopg2
import json
from server_db_tables import check_if_table_exists
import cryptocode


def check_database():
    DATABASE_CONFIG = json.load(open(r'\\dc01\netlogon\Notfall\database.json')) # Database connnection info
    try:
        con_postgreSQL = psycopg2.connect(
            host = DATABASE_CONFIG["HOSTNAME"],
            dbname = DATABASE_CONFIG["DATABASE"],
            user = DATABASE_CONFIG["USERNAME"],
            password = (cryptocode.decrypt(DATABASE_CONFIG["PWD"], "encrypt")),
            port = DATABASE_CONFIG["PORT_ID"]
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
