from server_db_credentials import *


cur_postgre_db = con_postgreSQL.cursor()

def create_tables():
    try:
        Notfall_Table_Create = ''' CREATE TABLE IF NOT EXISTS Notfälle (
                                    id             SERIAL PRIMARY KEY NOT NULL,
                                    device         varchar(64) NOT NULL,
                                    IPv4           varchar(64) NOT NULL,
                                    date           timestamp  NOT NULL
                                    )'''
        cur_postgre_db.execute(Notfall_Table_Create)
        con_postgreSQL.commit()
        print(f"\n-----------\nTable ready\n-----------")
        
    except (Exception, psycopg2.Error) as error:
        print(error)

create_tables()
con_postgreSQL.close()