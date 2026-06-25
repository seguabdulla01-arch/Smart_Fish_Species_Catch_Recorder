import sqlite3
import os

# Check if database exists
db_path = 'catch_records.db'
print(f"Database exists: {os.path.exists(db_path)}")

# Create database if it doesn't exist
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species TEXT,
        quantity INTEGER,
        kilogram REAL,
        date TEXT,
        image TEXT
    )
''')
conn.commit()

print("Database and table created successfully!")
conn.close()