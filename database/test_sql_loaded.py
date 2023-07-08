import sqlite3

# Path to the SQLite database file
database_file = 'inspired_daily.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Execute a SELECT query to retrieve data from the table
cursor.execute('SELECT * FROM mytable')
rows = cursor.fetchall()

# Print the retrieved data
for row in rows:
    uid = row[0]
    author = row[1]
    quote = row[2]
    ka = row[3]
    sch = row[4]
    tags = row[5]
    print(f'UID: {uid}')
    print(f"Author: {author}")
    print(f"Quote: {quote}")
    print(f"Ka: {ka}")
    print(f"Sch: {sch}")
    print(f"Tags: {tags}")
    print('-' * 30)

# Close the database connection
conn.close()