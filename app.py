from flask import Flask, render_template

app = Flask(__name__)

# -------- PUBLIC ROUTES ----------
@app.route("/")
def home():
    return render_template("public/pages/home.html", title="Om Industries India")

@app.route("/about")
def about():
    return render_template("public/pages/about.html", title="About")


# -------- ADMIN ROUTES ----------
@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/pages/dashboard.html", title="Admin Dashboard")

@app.route("/admin/users")
def admin_users():
    return render_template("admin/pages/users.html", title="Manage Users")


if __name__ == "__main__":
    app.run(debug=True)
