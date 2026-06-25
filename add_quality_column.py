# add_quality_column.py 
import sqlite3 

conn = sqlite3.connect('catch_records.db') 
c = conn.cursor() 

# Add 'kilogram' column if missing (keeps existing behavior) 
try: 
    c.execute("ALTER TABLE records ADD COLUMN kilogram REAL DEFAULT 0.0") 
except sqlite3.OperationalError: 
    pass 

# Add 'quality' column if missing 
try: 
    c.execute("ALTER TABLE records ADD COLUMN quality INTEGER DEFAULT 0") 
    print("✅ 'quality' column added (or already exists).") 
except sqlite3.OperationalError: 
    print("ℹ️ 'quality' column already exists or table missing.") 

conn.commit() 
conn.close()