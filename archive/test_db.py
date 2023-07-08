import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import Error
from environment import connection_string

con_str = connection_string
db = create_engine(con_str)
conn = db.connect()
df = pd.read_csv('quotes.csv', encoding='utf-8')

df.to_sql('to_sql_test', con=conn, if_exists='replace', index=False)

import pdb; pdb.set_trace()















# try:
#     # Connect to an existing database
#     connection = psycopg2.connect(user="inspired_daily_user",
#                                   password="ETHg3HNyunveYxOlih6CvJoo0RWUc23b",
#                                   host="dpg-cd4biv1gp3jqpbo8kjn0-a.oregon-postgres.render.com",
#                                   port="5432",
#                                   database="inspired_daily")

#     # Create a cursor to perform database operations
#     cursor = connection.cursor()
#     # Print PostgreSQL details
#     print("PostgreSQL server information")
#     print(connection.get_dsn_parameters(), "\n")
#     # Executing a SQL query
#     cursor.execute("SELECT version();")
#     # Fetch result
#     record = cursor.fetchone()
#     print("You are connected to - ", record, "\n")

# except (Exception, Error) as error:
#     print("Error while connecting to PostgreSQL", error)
# finally:
#     if (connection):
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")