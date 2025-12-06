"""
Migration script to update existing database with new columns
Run this script once to update your existing database.db file
"""
import sqlite3
import os

DATABASE = 'database.db'

if not os.path.exists(DATABASE):
    print(f"Database file '{DATABASE}' not found. It will be created when you run the app.")
    exit(0)

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

print("Starting database migration...")

# Check and update feedback table
try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
    if cursor.fetchone():
        # Check existing columns
        cursor.execute("PRAGMA table_info(feedback)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Existing feedback columns: {columns}")
        
        # Add rating column if missing
        if 'rating' not in columns:
            cursor.execute("ALTER TABLE feedback ADD COLUMN rating INTEGER DEFAULT 5")
            print("✓ Added 'rating' column to feedback table")
        else:
            print("✓ 'rating' column already exists")
        
        # Add status column if missing
        if 'status' not in columns:
            cursor.execute("ALTER TABLE feedback ADD COLUMN status TEXT DEFAULT 'pending'")
            # Update existing records
            cursor.execute("UPDATE feedback SET status = 'approved' WHERE status IS NULL")
            print("✓ Added 'status' column to feedback table")
            print("✓ Updated existing feedbacks to 'approved' status")
        else:
            print("✓ 'status' column already exists")
    else:
        print("Feedback table doesn't exist yet. It will be created when you run the app.")
except Exception as e:
    print(f"Error updating feedback table: {e}")

# Check and update contacts table
try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts'")
    if cursor.fetchone():
        # Check existing columns
        cursor.execute("PRAGMA table_info(contacts)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Existing contacts columns: {columns}")
        
        # Add date column if missing
        if 'date' not in columns:
            cursor.execute("ALTER TABLE contacts ADD COLUMN date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✓ Added 'date' column to contacts table")
        else:
            print("✓ 'date' column already exists")
    else:
        print("Contacts table doesn't exist yet. It will be created when you run the app.")
except Exception as e:
    print(f"Error updating contacts table: {e}")

conn.commit()
conn.close()

print("\nMigration completed successfully!")
print("You can now run the app with: python app.py")

