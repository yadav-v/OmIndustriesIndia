import sqlite3

# Connect to database (creates if not exists)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create contacts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    message TEXT
)
""")

conn.commit()
conn.close()

print("Contacts table created successfully!")
