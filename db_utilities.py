import os
import psycopg2
from psycopg2 import Error
import pandas as pd
import sqlite3 as sl
from environment import user, password, host, port, database, csv_file

# con = sl.connect('inspired_daily.db')

# with con:
#     con.execute("""
#         CREATE TABLE ID (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             author TEXT,
#             quote TEXT,
#             ka INTEGER,
#             scheduler TEXT,
#             tags TEXT
#         );
#     """)

#----
# df = pandas.read_csv(csvfile)
# df.to_sql("ID", conn, if_exists='append', index=False)

class DB_Utilities():

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.df = None

        # workflow
        self.connect_to_server_db()
        self.load_data_from_csv()
        #self.create_and_load_local_sqlite()
        self.load_data_to_server_db()
        import pdb; pdb.set_trace()
        self.close_server_db_connection()

    def load_data_from_csv(self):
        csv = csv_file
        self.df = pd.read_csv(csv, encoding='utf-8')
        self.df.columns = ['author', 'quote', 'ka', 'scheduler', 'tags']

    def create_and_load_local_sqlite(self):
        con = sl.connect('inspired_daily.db')
        df.to_sql('ID', con)

    def load_data_to_server_db(self):
        ...

    def connect_to_server_db(self):
        try:
            
            # Connect to an existing database
            self.connection = psycopg2.connect(user=user,
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)

            # Create a cursor to perform database operations
            self.cursor = self.connection.cursor()
            
            # Fetch result
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")

        except (Exception, Error) as error:
            print("ERROR: Could not connect to PostgreSQL", error)

    def close_server_db_connection(self):
        # close connection
        if (self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

DB_Utilities()
