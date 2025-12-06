from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)

# ------------------- DATABASE CONNECTION FUNCTION -------------------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------- ROUTES ---------------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send-data", methods=["POST"])
def send_data():
    user_input = request.form["inputname"]
    return f"Received from frontend: {user_input}"
@app.route("/admin")
def admin():
    conn = get_db_connection()
    contacts = conn.execute("SELECT * FROM contacts ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("admin.html", contacts=contacts)
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]





    # Insert into DB
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO contacts (name, email, phone, message) VALUES (?, ?, ?, ?)",
        (name, email, phone, message)
    )
    conn.commit()
    conn.close()

    return render_template("thankyou.html", name=name)

# ------------------ RUN THE SERVER --------------------
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def home():
    conn = get_db_connection()
    feedbacks = conn.execute("SELECT * FROM feedback ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("index.html", feedbacks=feedbacks)
@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()

    # If visitor submits feedback
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        conn.execute("INSERT INTO feedback (name, message) VALUES (?, ?)", (name, message))
        conn.commit()

    # Fetch all feedback to display
    feedbacks = conn.execute("SELECT * FROM feedback ORDER BY date DESC").fetchall()
    conn.close()

    return render_template("index.html", feedbacks=feedbacks)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM contacts")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()


