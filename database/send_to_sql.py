import csv
import sqlite3

# Path to the CSV file
csv_file = 'quotes.csv'

# Path to the SQLite database file
database_file = 'inspired_daily.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create the table in the SQLite database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mytable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT,
        quote TEXT,
        ka TEXT,
        sch TEXT,
        tags TEXT,
        UNIQUE (author, quote)
    )
''')

# Read the data from the CSV file and insert into the SQLite table
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        author = row['author'] or "Unknown"  # Assign default value "Unknown" if author is empty
        cursor.execute(
            'INSERT OR IGNORE INTO mytable (author, quote, ka, sch, tags) VALUES (?, ?, ?, ?, ?)',
            (author, row['quote'], row['ka'], row['sch'], row['tags'])
        )

# Commit the changes and close the connection
conn.commit()
conn.close()

# Confirm the completion
print('Data successfully loaded into the SQLite database.')