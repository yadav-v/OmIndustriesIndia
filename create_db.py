import sqlite3

conn = sqlite3.connect("mydb.db")
conn.execute("""
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
);
""")
conn.close()

print("Database created successfully.")
