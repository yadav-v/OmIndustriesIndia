from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send-data", methods=["POST"])
def send_data():
    user_input = request.form["inputname"]
    return f"Received from frontend: {user_input}"

if __name__ == "__main__":
    app.run(debug=True)

