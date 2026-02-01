from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import sqlite3
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from urllib.parse import urlparse

# Load environment variables from .env file (local only - Railway uses its own vars)
try:
    from dotenv import load_dotenv
    # Load from project root (where app.py is) - works regardless of cwd
    _env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    load_dotenv(_env_path)
except ImportError:
    pass  # Use system env vars

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')  # For PostgreSQL (online)
DATABASE = 'database.db'  # For SQLite (local)

# Determine which database to use
USE_POSTGRES = DATABASE_URL is not None

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'
def _db_connection():
    """Get database connection - uses PostgreSQL if DATABASE_URL is set, otherwise SQLite"""
    if USE_POSTGRES:
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            from urllib.parse import unquote
            
            # Parse DATABASE_URL (format: postgresql://user:password@host:port/database)
            # Supabase connection strings may have URL-encoded passwords
            result = urlparse(DATABASE_URL)
            
            # Decode URL-encoded password (handles special characters)
            password = unquote(result.password) if result.password else None
            
            # Extract connection details
            hostname = result.hostname
            port = result.port or 5432
            # Handle database name - remove leading '/' and any query parameters
            database_path = result.path[1:] if result.path else 'postgres'
            # Remove query parameters from database name if present
            database = database_path.split('?')[0] if '?' in database_path else database_path
            username = result.username or 'postgres'
            
            # Display connection info (hide password)
            connection_type = "Session Pooler" if port == 6543 else "Direct" if port == 5432 else f"Port {port}"
            print(f"🔌 Connecting to Supabase ({connection_type})...")
            print(f"   Host: {hostname}")
            print(f"   Port: {port}")
            
            # Connect to PostgreSQL/Supabase
            # Add connection timeout and better error handling
            conn = psycopg2.connect(
                database=database,
                user=username,
                password=password,
                host=hostname,
                port=port,
                connect_timeout=10  # 10 second timeout
            )
            # Use RealDictCursor to get row-like objects similar to sqlite3.Row
            conn.cursor_factory = RealDictCursor
            print(f"✅ Connected to Supabase (PostgreSQL) via {connection_type}")
            return conn
        except ImportError:
            print("⚠️  psycopg2 not installed. Install it with: pip install psycopg2-binary")
            print("   Falling back to SQLite...")
            conn = sqlite3.connect(DATABASE)
            conn.row_factory = sqlite3.Row
            return conn
        except psycopg2.OperationalError as e:
            error_msg = str(e)
            print(f"❌ Connection Error: {error_msg}")
            print("\n💡 Troubleshooting tips:")
            print("   1. Check your DATABASE_URL in .env file is correct")
            print("   2. Make sure you're using the correct connection string from Supabase:")
            print("      - Direct connection: port 5432")
            print("      - Session pooler: port 6543 (recommended for serverless)")
            print("   3. Verify your Supabase project is active (not paused)")
            print("   4. Check your database password is correct")
            print("   5. Try using Session Pooler connection string if Direct doesn't work")
            raise
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error connecting to Supabase: {error_msg}")
            print("   Please check your DATABASE_URL in .env file")
            print("   Make sure your Supabase project is active and password is correct")
            raise
    else:
        # Use SQLite (local file database)
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

def execute_query(conn, query, params=None):
    """Execute query with proper parameter formatting for both SQLite and PostgreSQL"""
    if USE_POSTGRES:
        # PostgreSQL uses cursor and %s for parameters
        cursor = conn.cursor()
        if params:
            # Convert ? to %s if query uses ? placeholders
            if '?' in query:
                query = query.replace('?', '%s')
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor
    else:
        # SQLite can use conn.execute() directly
        if params:
            return conn.execute(query, params)
        else:
            return conn.execute(query)

def init_db():
    """Initialize database tables and migrate if needed"""
    conn = _db_connection()
    cursor = conn.cursor()
    
    if USE_POSTGRES:
        # PostgreSQL syntax
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
        
        # Check and add missing columns for feedback table
        try:
            cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='feedback'
            """)
            rows = cursor.fetchall()
            # RealDictCursor returns dicts, so access by column name
            existing_columns = [row['column_name'] if isinstance(row, dict) else row[0] for row in rows]
            
            if 'rating' not in existing_columns:
                cursor.execute("ALTER TABLE feedback ADD COLUMN rating INTEGER DEFAULT 5")
                print("Added 'rating' column to feedback table")
            
            if 'status' not in existing_columns:
                cursor.execute("ALTER TABLE feedback ADD COLUMN status VARCHAR(50) DEFAULT 'pending'")
                cursor.execute("UPDATE feedback SET status = 'approved' WHERE status IS NULL")
                print("Added 'status' column to feedback table")
        except Exception as e:
            print(f"Migration check for feedback table: {e}")
        
        # Check and add missing columns for contacts table
        try:
            cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='contacts'
            """)
            rows = cursor.fetchall()
            # RealDictCursor returns dicts, so access by column name
            existing_columns = [row['column_name'] if isinstance(row, dict) else row[0] for row in rows]
            
            if 'date' not in existing_columns:
                cursor.execute("ALTER TABLE contacts ADD COLUMN date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                print("Added 'date' column to contacts table")
        except Exception as e:
            print(f"Migration check for contacts table: {e}")
        
        # Create orders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address TEXT NOT NULL,
            phone VARCHAR(50) NOT NULL,
            email VARCHAR(255) NOT NULL,
            price DECIMAL(12,2) NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            order_date DATE NOT NULL,
            status VARCHAR(50) DEFAULT 'process',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create order_status_log table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_status_log (
            id SERIAL PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders(id),
            status VARCHAR(50) NOT NULL,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    else:
        # SQLite syntax
        # Create feedback table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Check if feedback table exists and migrate if needed
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
        if cursor.fetchone():
            # Check if columns exist
            cursor.execute("PRAGMA table_info(feedback)")
            columns = [row[1] for row in cursor.fetchall()]
            
            # Add rating column if it doesn't exist
            if 'rating' not in columns:
                try:
                    cursor.execute("ALTER TABLE feedback ADD COLUMN rating INTEGER DEFAULT 5")
                    print("Added 'rating' column to feedback table")
                except sqlite3.OperationalError:
                    pass
            
            # Add status column if it doesn't exist
            if 'status' not in columns:
                try:
                    cursor.execute("ALTER TABLE feedback ADD COLUMN status TEXT DEFAULT 'pending'")
                    cursor.execute("UPDATE feedback SET status = 'approved' WHERE status IS NULL")
                    print("Added 'status' column to feedback table")
                except sqlite3.OperationalError:
                    pass
        
        # Create contacts table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            message TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Check if contacts table exists and migrate if needed
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts'")
        if cursor.fetchone():
            # Check if date column exists
            cursor.execute("PRAGMA table_info(contacts)")
            columns = [row[1] for row in cursor.fetchall()]
            
            # Add date column if it doesn't exist
            if 'date' not in columns:
                try:
                    cursor.execute("ALTER TABLE contacts ADD COLUMN date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                    print("Added 'date' column to contacts table")
                except sqlite3.OperationalError:
                    pass
        
        # Create orders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            order_date TEXT NOT NULL,
            status TEXT DEFAULT 'process',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create order_status_log table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_status_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL REFERENCES orders(id),
            status TEXT NOT NULL,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    
    conn.commit()
    conn.close()
    
    if USE_POSTGRES:
        print("✅ Database initialized with Supabase (PostgreSQL - online)")
        print("   Tables created: feedback, contacts, orders, order_status_log")
    else:
        print("✅ Database initialized with SQLite (local file: database.db)")
        print("   Tables created: feedback, contacts, orders, order_status_log")

# -------- PUBLIC ROUTES ----------
@app.route("/")
def home():
    conn = _db_connection()
    # Get approved feedbacks for display
    cursor = execute_query(conn, "SELECT * FROM feedback WHERE status = 'approved' ORDER BY date DESC LIMIT 6")
    feedbacks = cursor.fetchall()
    conn.close()
    return render_template("public/pages/home.html", 
                         title="Om Industries India", 
                         feedbacks=feedbacks,
                         now=datetime.now())

@app.route("/about")
def about():
    return render_template("public/pages/about.html", 
                         title="About Us - Om Industries India",
                         now=datetime.now())

@app.route("/services")
def services():
    return render_template("public/pages/services.html", 
                         title="Services - Om Industries India",
                         now=datetime.now())
# about water jacket 
@app.route('/water-jacket-testing-machine')
def water_jacket_detail():
    return render_template('public/water_jacket_detail.html', now=datetime.now())
#cylinder wise details
@app.route('/cylinder-wise-testing-machine')
def cylinder_wise_detail():
    return render_template('public/cylinder_wise_detail.html', now=datetime.now())
#hydro-pump
@app.route('/hydro-pump-machine')
def hydro_pump():
    return render_template('public/hydro_pump.html', now=datetime.now())

@app.route('/degassing')
def degassing():
    return render_template('public/degassing.html', now=datetime.now())

@app.route('/oil-removal')
def oil_removal():
    return render_template('public/oil_removal.html', now=datetime.now())

@app.route("/services/cng-hydrotesting-plant")
def service_cng():
    return render_template("public/pages/service_cng.html", title="CNG Hydrotesting Plant - Om Industries India", now=datetime.now())

@app.route("/services/cylinder-bracket")
def service_cylinder():
    return render_template("public/pages/service_cylinder.html", title="Cylinder Bracket - Om Industries India", now=datetime.now())

@app.route("/services/fabrication")
def service_fabrication():
    return render_template("public/pages/service_fabrication.html", title="Fabrication Services - Om Industries India", now=datetime.now())
@app.route("/service-inspect")
def service_inspect():
    return render_template("public/pages/service_inspect.html", title="Inspection Services", now=datetime.now())
@app.route("/service_heatdrying")
def service_heatdrying():
    return render_template("public/pages/service_heatdrying.html", title="Heat and DRYING SERVICE", now=datetime.now())
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        message = request.form.get('message', '').strip()
        if name and email and message:
            conn = _db_connection()
            execute_query(conn, "INSERT INTO contacts (name, email, phone, message) VALUES (?, ?, ?, ?)",
                         (name, email, phone or None, message))
            conn.commit()
            conn.close()
            send_contact_email(name, email, phone, message)
            flash('Thank you! Your message has been sent. We will get back to you soon.', 'success')
        else:
            flash('Please fill in name, email and message.', 'error')
        return redirect(url_for('contact'))
    
    return render_template("public/pages/contact.html", title="Contact Us - Om Industries India", now=datetime.now())

@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        rating = request.form.get('rating', '5')
        message = request.form.get('message', '').strip()
        if name and message:
            try:
                rating_val = int(rating)
                if rating_val < 1:
                    rating_val = 1
                elif rating_val > 5:
                    rating_val = 5
            except (ValueError, TypeError):
                rating_val = 5
            conn = _db_connection()
            execute_query(conn, "INSERT INTO feedback (name, rating, message, status) VALUES (?, ?, ?, 'pending')",
                         (name, rating_val, message))
            conn.commit()
            conn.close()
            flash('Thank you! Your feedback has been submitted. It will appear after review.', 'success')
        else:
            flash('Please fill in your name and message.', 'error')
        return redirect(url_for('feedback'))
    
    # Get approved feedbacks
    conn = _db_connection()
    cursor = execute_query(conn, "SELECT * FROM feedback WHERE status = 'approved' ORDER BY date DESC")
    feedbacks = cursor.fetchall()
    conn.close()
    
    return render_template("public/pages/feedback.html", title="Feedback - Om Industries India", feedbacks=feedbacks, now=datetime.now())

def send_contact_email(name, email, phone, message):
    """Send contact form email"""
    # Configure your SMTP settings here
    # Option 1: Use environment variables (recommended for production)
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    recipient_email = os.environ.get('RECIPIENT_EMAIL', '')
    
    # Option 2: Configure directly here (for testing - NOT recommended for production)
    # Uncomment and fill these if you don't want to use environment variables:
    # smtp_server = 'smtp.gmail.com'
    # smtp_port = 587
    # smtp_user = 'your-email@gmail.com'
    # smtp_password = 'your-app-password'  # Use App Password for Gmail
    # recipient_email = 'admin@omindustriesindia.com'
    
    if not smtp_user or not smtp_password or not recipient_email:
        print("⚠️  SMTP credentials not configured. Email will not be sent.")
        print("   To enable email, set environment variables:")
        print("   - SMTP_SERVER (default: smtp.gmail.com)")
        print("   - SMTP_PORT (default: 587)")
        print("   - SMTP_USER (your email)")
        print("   - SMTP_PASSWORD (your email password or app password)")
        print("   - RECIPIENT_EMAIL (where to receive contact forms)")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipient_email
        msg['Subject'] = f'New Contact Form Submission from {name}'
        
        body = f"""
New contact form submission from Om Industries India website:

Name: {name}
Email: {email}
Phone: {phone or 'Not provided'}

Message:
{message}

---
This email was sent from the contact form on your website.
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent successfully to {recipient_email}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Email authentication failed: {e}")
        print("   Check your SMTP_USER and SMTP_PASSWORD")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

# -------- ADMIN ROUTES ----------
@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template("admin/pages/login.html", title="Admin Login")

@app.route("/admin/logout")
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = _db_connection()
    
    # Get counts
    cursor = execute_query(conn, "SELECT COUNT(*) as count FROM feedback")
    row = cursor.fetchone()
    # Handle both dict (PostgreSQL/RealDictCursor) and tuple (SQLite) row formats
    feedback_count = row['count'] if isinstance(row, dict) else row[0]
    
    cursor = execute_query(conn, "SELECT COUNT(*) as count FROM feedback WHERE status = 'pending'")
    row = cursor.fetchone()
    pending_feedback_count = row['count'] if isinstance(row, dict) else row[0]
    
    cursor = execute_query(conn, "SELECT COUNT(*) as count FROM contacts")
    row = cursor.fetchone()
    contact_count = row['count'] if isinstance(row, dict) else row[0]
    
    conn.close()
    
    return render_template("admin/pages/dashboard.html", 
                         title="Admin Dashboard",
                         feedback_count=feedback_count,
                         pending_feedback_count=pending_feedback_count,
                         contact_count=contact_count)

@app.route("/admin/feedback")
def admin_feedback():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = _db_connection()
    cursor = execute_query(conn, "SELECT * FROM feedback ORDER BY date DESC")
    feedbacks = cursor.fetchall()
    conn.close()
    
    return render_template("admin/pages/feedback.html", title="Manage Feedback", feedbacks=feedbacks)

@app.route("/admin/feedback/<int:feedback_id>/<action>")
def admin_feedback_action(feedback_id, action):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = _db_connection()
    
    if action == 'approve':
        execute_query(conn, "UPDATE feedback SET status = 'approved' WHERE id = ?", (feedback_id,))
        flash('Feedback approved!', 'success')
    elif action == 'reject':
        execute_query(conn, "UPDATE feedback SET status = 'rejected' WHERE id = ?", (feedback_id,))
        flash('Feedback rejected!', 'success')
    elif action == 'delete':
        execute_query(conn, "DELETE FROM feedback WHERE id = ?", (feedback_id,))
        flash('Feedback deleted!', 'success')
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_feedback'))

@app.route("/admin/contacts")
def admin_contacts():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = _db_connection()
    cursor = execute_query(conn, "SELECT * FROM contacts ORDER BY date DESC")
    contacts = cursor.fetchall()
    conn.close()
    
    return render_template("admin/pages/contacts.html", title="Manage Contacts", contacts=contacts)

def _row_to_dict(row):
    """Convert DB row (dict or Row) to dict for template use"""
    if row is None:
        return None
    d = dict(row) if hasattr(row, 'keys') else {}
    for k, v in list(d.items()):
        if hasattr(v, 'strftime'):
            d[k] = v.strftime('%Y-%m-%d') if 'date' in str(k).lower() or 'at' in str(k).lower() else v.strftime('%Y-%m-%d %H:%M')
    return d

@app.route("/admin/orders")
def admin_order():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = _db_connection()
    cursor = execute_query(conn, "SELECT * FROM orders ORDER BY order_date DESC, id DESC")
    orders_raw = cursor.fetchall()
    conn.close()
    
    orders = [_row_to_dict(o) for o in (orders_raw or [])] if orders_raw else []
    
    return render_template("admin/pages/order.html", title="Manage Orders", orders=orders)

@app.route("/admin/orders/add", methods=['GET', 'POST'])
def admin_order_add():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        price = request.form.get('price', '0')
        quantity = request.form.get('quantity', '1')
        order_date = request.form.get('order_date', '')
        status = request.form.get('status', 'process')
        
        if not name or not address or not phone or not email:
            flash('Name, address, phone and email are required.', 'error')
            return redirect(url_for('admin_order_add'))
        
        try:
            price_val = float(price)
            quantity_val = int(quantity)
        except (ValueError, TypeError):
            flash('Invalid price or quantity.', 'error')
            return redirect(url_for('admin_order_add'))
        
        if not order_date:
            order_date = datetime.now().strftime('%Y-%m-%d')
        
        conn = _db_connection()
        if USE_POSTGRES:
            cursor = execute_query(conn, """
                INSERT INTO orders (name, address, phone, email, price, quantity, order_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (name, address, phone, email, price_val, quantity_val, order_date, status))
            row = cursor.fetchone()
            order_id = row['id'] if isinstance(row, dict) else row[0]
        else:
            cursor = execute_query(conn, """
                INSERT INTO orders (name, address, phone, email, price, quantity, order_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, address, phone, email, price_val, quantity_val, order_date, status))
            order_id = cursor.lastrowid if hasattr(cursor, 'lastrowid') else conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Log initial status
        execute_query(conn, "INSERT INTO order_status_log (order_id, status) VALUES (?, ?)", (order_id, status))
        conn.commit()
        conn.close()
        
        flash(f'Order #{order_id} added successfully!', 'success')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    
    return render_template("admin/pages/order_add.html", title="Add Order", now=datetime.now())

@app.route("/admin/orders/<int:order_id>")
def admin_order_detail(order_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = _db_connection()
    cursor = execute_query(conn, "SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        flash('Order not found.', 'error')
        return redirect(url_for('admin_order'))
    
    cursor = execute_query(conn, "SELECT * FROM order_status_log WHERE order_id = ? ORDER BY changed_at DESC", (order_id,))
    status_log_raw = cursor.fetchall()
    conn.close()
    
    order_dict = _row_to_dict(order)
    status_log = [_row_to_dict(log) for log in (status_log_raw or [])] if status_log_raw else []
    
    return render_template("admin/pages/order_detail.html", title=f"Order #{order_id}", order=order_dict, status_log=status_log)

@app.route("/admin/orders/<int:order_id>/update-status", methods=['POST'])
def admin_order_update_status(order_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    status = request.form.get('status', '').strip()
    valid_statuses = ('process', 'shipped', 'complete', 'cancel')
    
    if status not in valid_statuses:
        flash('Invalid status.', 'error')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    
    conn = _db_connection()
    execute_query(conn, "UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    execute_query(conn, "INSERT INTO order_status_log (order_id, status) VALUES (?, ?)", (order_id, status))
    conn.commit()
    conn.close()
    
    flash(f'Status updated to "{status}".', 'success')
    return redirect(url_for('admin_order_detail', order_id=order_id))

@app.route("/admin/orders/<int:order_id>/invoice")
def admin_order_invoice(order_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = _db_connection()
    cursor = execute_query(conn, "SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    conn.close()
    
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('admin_order'))
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=45, leftMargin=45, topMargin=40, bottomMargin=40)
        
        o = order
        name = o['name'] if isinstance(o, dict) else o[1]
        address = o['address'] if isinstance(o, dict) else o[2]
        phone = o['phone'] if isinstance(o, dict) else o[3]
        email = o['email'] if isinstance(o, dict) else o[4]
        price = float(o['price'] if isinstance(o, dict) else o[5])
        quantity = int(o['quantity'] if isinstance(o, dict) else o[6])
        order_date = o['order_date'] if isinstance(o, dict) else o[7]
        if hasattr(order_date, 'strftime'):
            order_date = order_date.strftime('%d %b %Y')
        else:
            order_date = str(order_date)
        
        total = price * quantity
        
        # Brand colors
        dark_blue = colors.HexColor('#1a365d')
        accent_blue = colors.HexColor('#2c5282')
        light_grey = colors.HexColor('#f7fafc')
        border_grey = colors.HexColor('#e2e8f0')
        text_muted = colors.HexColor('#64748b')
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='InvoiceTitle', fontSize=24, textColor=dark_blue, spaceAfter=2, fontName='Helvetica-Bold'))
        styles.add(ParagraphStyle(name='CompanyTagline', fontSize=9, textColor=text_muted, spaceAfter=12, fontName='Helvetica'))
        styles.add(ParagraphStyle(name='SectionLabel', fontSize=8, textColor=text_muted, spaceAfter=4, fontName='Helvetica-Bold'))
        styles.add(ParagraphStyle(name='CustomerText', fontSize=10, textColor=colors.black, spaceAfter=2, fontName='Helvetica'))
        styles.add(ParagraphStyle(name='FooterText', fontSize=8, textColor=text_muted, alignment=1, fontName='Helvetica'))
        
        # Header: Company name + Invoice label
        header_data = [[
            Paragraph('<b>OM INDUSTRIES INDIA</b>', ParagraphStyle('CoName', fontSize=22, textColor=dark_blue, fontName='Helvetica-Bold')),
            Paragraph(f'<b>INVOICE</b><br/><font size="9" color="#64748b">#{order_id:06d}</font>', ParagraphStyle('InvLabel', fontSize=18, textColor=dark_blue, alignment=2, fontName='Helvetica-Bold'))
        ]]
        header_table = Table(header_data, colWidths=[3.8*inch, 2.2*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        tagline = Paragraph('CNG Cylinder Hydrotesting | Fabrication | Industrial Equipment', styles['CompanyTagline'])
        spacer_sm = Spacer(1, 0.15*inch)
        spacer_md = Spacer(1, 0.35*inch)
        
        # Bill To + Invoice Info side by side
        bill_to = f'''
        <b>Bill To</b><br/>
        {name}<br/>
        {address}<br/>
        Phone: {phone}<br/>
        Email: {email}
        '''
        inv_info = f'''
        <b>Invoice Date</b><br/>
        {order_date}<br/><br/>
        <b>Order Reference</b><br/>
        #{order_id:06d}
        '''
        two_col = [[
            Paragraph(bill_to, ParagraphStyle('BillTo', fontSize=10, fontName='Helvetica')),
            Paragraph(inv_info, ParagraphStyle('InvInfo', fontSize=10, fontName='Helvetica', alignment=2))
        ]]
        info_table = Table(two_col, colWidths=[3.5*inch, 2.5*inch])
        info_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, border_grey),
            ('BACKGROUND', (0, 0), (-1, -1), light_grey),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        # Line items table
        items_data = [['Description', 'Unit Price (₹)', 'Qty', 'Amount (₹)']]
        items_data.append(['Order Items / Services', f'{price:,.2f}', str(quantity), f'{total:,.2f}'])
        items_table = Table(items_data, colWidths=[2.8*inch, 1.4*inch, 1*inch, 1.4*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), dark_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.white),
            ('BOX', (0, 0), (-1, -1), 0.5, border_grey),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, dark_blue),
        ]))
        
        # Total row
        total_data = [[Paragraph('<b>Total Amount</b>', ParagraphStyle('TotalLbl', fontSize=11, fontName='Helvetica-Bold')), Paragraph(f'<b>₹{total:,.2f}</b>', ParagraphStyle('TotalVal', fontSize=12, fontName='Helvetica-Bold', alignment=2))]]
        total_table = Table(total_data, colWidths=[4.2*inch, 1.4*inch])
        total_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        # Footer
        footer = Paragraph(
            'Thank you for your business. | Om Industries India | Payment terms as per agreement.',
            styles['FooterText']
        )
        footer_spacer = Spacer(1, 0.4*inch)
        
        doc.build([
            header_table, tagline, spacer_md,
            info_table, spacer_md,
            items_table, spacer_sm, total_table,
            footer_spacer, footer
        ])
        
        buffer.seek(0)
        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=f'invoice_order_{order_id}.pdf')
    
    except ImportError:
        flash('PDF library (reportlab) not installed. Run: pip install reportlab', 'error')
        return redirect(url_for('admin_order_detail', order_id=order_id))

# Initialize DB tables when app loads (for gunicorn / Railway)
init_db()

if __name__ == "__main__":
    # For production, use: gunicorn app:app
    # For local development:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
