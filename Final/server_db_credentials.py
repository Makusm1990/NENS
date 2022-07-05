import psycopg2

# Path and credentials for PostgreSQL 
hostname=""
database=""
username=""
pwd=""
port_id=5432

# connection postgreSQL
con_postgreSQL = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)