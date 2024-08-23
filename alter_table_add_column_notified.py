import sqlite3

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return None

def execute(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        c.close()
    except Exception as e:
        print(e)

database = "properties.db"

sql_create_properties_table = """ ALTER TABLE properties
                                  ADD COLUMN notified INTEGER DEFAULT 0;
                              """

conn = create_connection(database)
with conn:
    if conn is not None:
        # alter properties table
        execute(conn, sql_create_properties_table)
    else:
        print("Error! cannot create the database connection.")        

