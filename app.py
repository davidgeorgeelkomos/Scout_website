import os
from cs50 import SQL
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database
db = SQL("sqlite:///scout.db")


# -------------------------------------------
# HELPERS
# -------------------------------------------
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated


# -------------------------------------------
# ROUTES
# -------------------------------------------

@app.route("/")
def index():
    if not session.get("user_id"):
        return render_template("index_public.html")
    
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
    return render_template("index_private.html", user=user)


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        birthday = request.form.get("birthday")
        phone = request.form.get("phone")
        stage = request.form.get("stage")
        location = request.form.get("home_location")

        if not name or not password or not confirm:
            return "Missing fields"

        if password != confirm:
            return "Passwords do not match"

        hash_pass = generate_password_hash(password)

        db.execute("""
            INSERT INTO users (name, hash, birthday, phone, stage, home_location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, name, hash_pass, birthday, phone, stage, location)

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")

        user = db.execute("SELECT * FROM users WHERE name = ?", username)

        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return "Invalid login"

        session["user_id"] = user[0]["id"]
        return redirect("/")

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
