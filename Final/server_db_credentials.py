import psycopg2

# Path and credentials for PostgreSQL 
HOSTNAME = ""   # Enter the name of the host where the PostgreSQL databse is located.
DATABASE = ""   # The name of your database
USERNAME = ""   # PostgreSQL Username 
PWD = ""        # PostgreSQL Password
PORT_ID = ""    # PostgreSQL PORT

# connection postgreSQL
con_postgreSQL = psycopg2.connect(
    HOST = HOSTNAME,
    DBNAME = DATABASE,
    USER = USERNAME,
    PASSWORD = PWD,
    PORT = PORT_ID
)
