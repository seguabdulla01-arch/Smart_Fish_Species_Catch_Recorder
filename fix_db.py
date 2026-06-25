import sqlite3 
conn = sqlite3.connect('catch_records.db') 
c = conn.cursor() 
try: 
    c.execute("ALTER TABLE records ADD COLUMN image TEXT;") 
    print("✅ 'image' column added successfully.") 
except sqlite3.OperationalError as e: 
    print("⚠️ Error:", e) 
conn.commit() 
conn.close()