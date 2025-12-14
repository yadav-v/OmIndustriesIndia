"""
Helper script to test Supabase connection and create tables
Run this after setting up your .env file with DATABASE_URL
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file!")
    print("\nPlease create a .env file with:")
    print("DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres")
    exit(1)

print("🔍 Testing Supabase connection...")
print(f"   Database URL: {DATABASE_URL.split('@')[0]}@...")  # Hide password

try:
    from urllib.parse import urlparse
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from urllib.parse import unquote
    
    # Parse connection string
    result = urlparse(DATABASE_URL)
    password = unquote(result.password) if result.password else None
    
    # Connect
    conn = psycopg2.connect(
        database=result.path[1:] if result.path else 'postgres',
        user=result.username or 'postgres',
        password=password,
        host=result.hostname,
        port=result.port or 5432
    )
    
    print("✅ Successfully connected to Supabase!")
    
    # Test creating tables
    cursor = conn.cursor()
    
    # Create feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        rating INTEGER NOT NULL,
        message TEXT NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create contacts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        phone VARCHAR(50),
        message TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    print("✅ Tables created successfully!")
    print("   - feedback")
    print("   - contacts")
    
    # Test insert
    cursor.execute("SELECT COUNT(*) as count FROM feedback")
    feedback_count = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(*) as count FROM contacts")
    contact_count = cursor.fetchone()['count']
    
    print(f"\n📊 Current data:")
    print(f"   - Feedback entries: {feedback_count}")
    print(f"   - Contact entries: {contact_count}")
    
    conn.close()
    print("\n🎉 Everything is set up correctly!")
    print("   You can now run: python app.py")
    
except ImportError:
    print("❌ psycopg2 not installed!")
    print("   Run: pip install psycopg2-binary")
except psycopg2.OperationalError as e:
    print(f"❌ Connection failed: {e}")
    print("\nPlease check:")
    print("   1. Your DATABASE_URL in .env file is correct")
    print("   2. Your Supabase project is active (not paused)")
    print("   3. Your database password is correct")
except Exception as e:
    print(f"❌ Error: {e}")

