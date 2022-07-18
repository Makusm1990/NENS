import psycopg
from server_db_tables import check_if_table_exists

# Path and credentials for PostgreSQL
HOSTNAME = "localhost"  # Enter the name of the host where the PostgreSQL databse is located.
DATABASE = "Notfall"    # The name of your database
USERNAME = "postgres"   # PostgreSQL Username
PWD = "GesineBusdie1."  # PostgreSQL Password
PORT_ID = "5432"        # PostgreSQL PORT

# check connection postgreSQL
try:
    con_postgreSQL = psycopg.connect(
        host = HOSTNAME,
        dbname = DATABASE,
        user = USERNAME,
        password = PWD,
        port = PORT_ID
    )
    if (con_postgreSQL.closed) == False:
        print("Credentials correct.")
        # check if tables already exsits
        try:
            cur_postgre_db = con_postgreSQL.cursor()
            check_if_table_exists(cur_postgre_db,con_postgreSQL)
        except psycopg.Error as error:
            print(error)
except psycopg.Error as error:
    print(error)

