"""
Quick check: Is .env loaded and can we connect to Supabase?
Run: python check_env.py
"""
import os
import sys

# Load .env from project root
try:
    from dotenv import load_dotenv
    _root = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(_root, '.env'))
except ImportError:
    print("Install: pip install python-dotenv")
    sys.exit(1)

db_url = os.environ.get('DATABASE_URL')
print("DATABASE_URL loaded:", "Yes" if db_url else "NO (will use SQLite)")
if db_url:
    # Hide password in output
    safe = db_url.split('@')[-1] if '@' in db_url else "..."
    print("  -> Connects to:", safe)
    try:
        import psycopg2
        from urllib.parse import urlparse, unquote
        r = urlparse(db_url)
        conn = psycopg2.connect(
            host=r.hostname, port=r.port or 5432,
            database=r.path[1:].split('?')[0] or 'postgres',
            user=r.username, password=unquote(r.password) if r.password else None,
            connect_timeout=5
        )
        conn.close()
        print("  -> Connection: OK")
    except Exception as e:
        print("  -> Connection FAILED:", str(e))
else:
    print("  -> Will use SQLite (database.db)")
print("\nFor Railway: Add DATABASE_URL in Railway dashboard Variables (not .env)")
