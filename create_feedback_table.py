import sqlite3

conn = sqlite3.connect("database.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    message TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.close()
print("Feedback table ready!")
