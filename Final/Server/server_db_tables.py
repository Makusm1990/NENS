import psycopg


def create_tables(cur_postgre_db,con_postgreSQL):
    try:
        Notfall_Table_Create = ''' CREATE TABLE IF NOT EXISTS Notfälle (
                                    id             SERIAL PRIMARY KEY NOT NULL,
                                    device         varchar(64) NOT NULL,
                                    IPv4           varchar(64) NOT NULL,
                                    date           timestamp  NOT NULL
                                    )'''
        cur_postgre_db.execute(Notfall_Table_Create)
        con_postgreSQL.commit()
        return print(f"\n-----------\nTable ready\n-----------")

    except (Exception, psycopg.Error) as error:
        print(error)
    con_postgreSQL.close()


def check_if_table_exists(cur_postgre_db,con_postgreSQL):
    try:
        if_table_exists = ''' SELECT EXISTS (SELECT * FROM notfälle);'''
        cur_postgre_db.execute(if_table_exists)
        con_postgreSQL.commit()
        if (cur_postgre_db.fetchone()[0]) != True:
            create_tables(cur_postgre_db,con_postgreSQL)
        return print("Table already exsit... ")

    except (Exception, psycopg.Error) as error:
        print(error)
    con_postgreSQL.close()