import os
from cs50 import SQL
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database
db = SQL("sqlite:///scout.db")

# -------------------------------------------
# THE APOLOGY FUNCTION
# -------------------------------------------
def apology(message, code=400):
    return render_template("apology.html", top=code, bottom=message), code

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

        # Form inputs
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        birthday = request.form.get("birthday")
        phone = request.form.get("phone")
        stage = request.form.get("stage")
        lat = request.form.get("lat")
        lng = request.form.get("lng")

        # Validate required fields
        if not name:
            return apology("Name cannot be empty")
        if not password:
            return apology("Password cannot be empty")
        if not birthday:
            return apology("Birthday cannot be empty")
        if not phone:
            return apology("Phone number cannot be empty")
        if not stage:
            return apology("Stage cannot be empty")

        # Password match
        if password != confirmation:
            return apology("Passwords do not match")

        # Hash password
        hash_pw = generate_password_hash(password)

        # Insert user (approved = 1 so everything works now)
        try:
            new_id = db.execute(
                "INSERT INTO users (name, hash, birthday, phone, stage, home_location, approved) VALUES (?, ?, ?, ?, ?, ?, 1)",
                name, hash_pw, birthday, phone, stage, f"{lat},{lng}"
            )
        except:
            return apology("Username already exists")

         # MAP LOCATION 
        db.execute(
             "INSERT INTO maps (user_id, latitude, longitude) VALUES (?, ?, ?)",
             new_id, lat, lng
         )

        # AUTO LOGIN THE USER
        session["user_id"] = new_id

        return redirect("/")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["POST"])
def login():
    session.clear()

    user_input = request.form.get("user")
    password = request.form.get("password")

    if not user_input or not password:
        return apology("Must provide username or phone and password", 400)

    rows = db.execute(
        "SELECT * FROM users WHERE name = ? OR phone = ?",
        user_input.strip(), user_input.strip()
    )

    if len(rows) != 1:
        return apology("Invalid username or phone", 403)

    if not check_password_hash(rows[0]["hash"], password):
        return apology("Invalid password", 403)

    session["user_id"] = rows[0]["id"]
    return redirect("/")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
