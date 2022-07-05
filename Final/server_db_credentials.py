import psycopg2

# Path and credentials for PostgreSQL 
HOSTNAME = "localhost"   # Enter the name of the host where the PostgreSQL databse is located.
DATABASE = "Notfall"   # The name of your database
USERNAME = "postgres"   # PostgreSQL Username 
PWD = ""        # PostgreSQL Password
PORT_ID = "5432"    # PostgreSQL PORT

# connection postgreSQL
con_postgreSQL = psycopg2.connect(
    HOST = HOSTNAME,
    DBNAME = DATABASE,
    USER = USERNAME,
    PASSWORD = PWD,
    PORT = PORT_ID
)
