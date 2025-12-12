from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

DATABASE = 'database.db'

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and migrate if needed"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
                # Update existing records to have status 'approved' if they don't have status
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
    
    conn.commit()
    conn.close()

# -------- PUBLIC ROUTES ----------
@app.route("/")
def home():
    conn = get_db_connection()
    # Get approved feedbacks for display
    feedbacks = conn.execute(
        "SELECT * FROM feedback WHERE status = 'approved' ORDER BY date DESC LIMIT 6"
    ).fetchall()
    conn.close()
    return render_template("public/pages/home.html", title="Om Industries India", feedbacks=feedbacks)

@app.route("/about")
def about():
    return render_template("public/pages/about.html", title="About Us - Om Industries India")

@app.route("/services")
def services():
    return render_template("public/pages/services.html", title="Services - Om Industries India")
# about water jacket 
@app.route('/water-jacket-testing-machine')
def water_jacket_detail():
    return render_template('public/water_jacket_detail.html')
#cylinder wise details
@app.route('/cylinder-wise-testing-machine')
def cylinder_wise_detail():
    return render_template('public/cylinder_wise_detail.html')
#hydro-pump
@app.route('/hydro-pump-machine')
def hydro_pump():
    return render_template('public/hydro_pump.html')

@app.route('/degassing')
def degassing():
    return render_template('public/degassing.html')

@app.route('/oil-removal')
def oil_removal():
    return render_template('public/oil_removal.html')

@app.route("/services/cng-hydrotesting-plant")
def service_cng():
    return render_template("public/pages/service_cng.html", title="CNG Hydrotesting Plant - Om Industries India")

@app.route("/services/cylinder-bracket")
def service_cylinder():
    return render_template("public/pages/service_cylinder.html", title="Cylinder Bracket - Om Industries India")

@app.route("/services/fabrication")
def service_fabrication():
    return render_template("public/pages/service_fabrication.html", title="Fabrication Services - Om Industries India")
@app.route("/service-inspect")
def service_inspect():
    return render_template("public/pages/service_inspect.html", title="Inspection Services")
@app.route("/service_heatdrying")
def service_heatdrying():
    return render_template("public/pages/service_heatdrying.html", title="Heat and DRYING SERVICE")
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        # Store in database
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO contacts (name, email, phone, message) VALUES (?, ?, ?, ?)",
            (name, email, phone, message)
        )
        conn.commit()
        conn.close()
        
        # Send email (configure SMTP settings)
        email_sent = False
        try:
            email_sent = send_contact_email(name, email, phone, message)
            if email_sent:
                print("Contact form email sent successfully!")
            else:
                print("Email not sent - SMTP credentials not configured")
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        if email_sent:
            flash('Thank you for contacting us! We have received your message and will get back to you soon.', 'success')
        else:
            flash('Thank you for contacting us! Your message has been saved. We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template("public/pages/contact.html", title="Contact Us - Om Industries India")

@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        rating = int(request.form.get('rating', 5))
        message = request.form.get('message')
        
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO feedback (name, rating, message, status) VALUES (?, ?, ?, 'pending')",
            (name, rating, message)
        )
        conn.commit()
        conn.close()
        
        flash('Thank you for your feedback! It will be reviewed by our admin.', 'success')
        return redirect(url_for('feedback'))
    
    # Get approved feedbacks
    conn = get_db_connection()
    feedbacks = conn.execute(
        "SELECT * FROM feedback WHERE status = 'approved' ORDER BY date DESC"
    ).fetchall()
    conn.close()
    
    return render_template("public/pages/feedback.html", title="Feedback - Om Industries India", feedbacks=feedbacks)

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
    
    conn = get_db_connection()
    
    # Get counts
    feedback_count = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
    pending_feedback_count = conn.execute("SELECT COUNT(*) FROM feedback WHERE status = 'pending'").fetchone()[0]
    contact_count = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    
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
    
    conn = get_db_connection()
    feedbacks = conn.execute(
        "SELECT * FROM feedback ORDER BY date DESC"
    ).fetchall()
    conn.close()
    
    return render_template("admin/pages/feedback.html", title="Manage Feedback", feedbacks=feedbacks)

@app.route("/admin/feedback/<int:feedback_id>/<action>")
def admin_feedback_action(feedback_id, action):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    
    if action == 'approve':
        conn.execute("UPDATE feedback SET status = 'approved' WHERE id = ?", (feedback_id,))
        flash('Feedback approved!', 'success')
    elif action == 'reject':
        conn.execute("UPDATE feedback SET status = 'rejected' WHERE id = ?", (feedback_id,))
        flash('Feedback rejected!', 'success')
    elif action == 'delete':
        conn.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))
        flash('Feedback deleted!', 'success')
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_feedback'))

@app.route("/admin/contacts")
def admin_contacts():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    contacts = conn.execute(
        "SELECT * FROM contacts ORDER BY date DESC"
    ).fetchall()
    conn.close()
    
    return render_template("admin/pages/contacts.html", title="Manage Contacts", contacts=contacts)

if __name__ == "__main__":
    init_db()
    # For production, use: gunicorn app:app
    # For local development:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
