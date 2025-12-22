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
    user = None

    if session.get("user_id"):
        rows = db.execute(
            "SELECT name, sector FROM users WHERE id = ?",
            session["user_id"]
        )
        if rows:
            user = rows[0]

    return render_template("index_public.html", user=user)


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
        sector = request.form.get("stage")
        lat = request.form.get("lat")
        lng = request.form.get("lng")

        print("FORM DATA:", name, password, birthday, phone, sector, lat, lng)

        # Validation
        if not all([name, password, confirmation, birthday, phone, sector, lat, lng]):
            return apology("All fields are required", 400)

        if password != confirmation:
            return apology("Passwords do not match", 400)

        # Hash password
        hash_pw = generate_password_hash(password)
        print("Password hashed")

        # Insert user
        try:
            new_id = db.execute(
                """
                INSERT INTO users (name, hash, birthday, phone, sector)
                VALUES (?, ?, ?, ?, ?)
                """,
                name, hash_pw, birthday, phone, sector
            )
        except Exception as e:
            print("DB ERROR (users table)")
            print(type(e))
            print(e.args)
            print(e)
            return apology("Database error (users)", 500)

        # Insert map location
        try:
            db.execute(
                """
                INSERT INTO maps (user_id, latitude, longitude)
                VALUES (?, ?, ?)
                """,
                new_id, lat, lng
            )
        except Exception as e:
            print("DB ERROR (maps table)")
            print(type(e))
            print(e.args)
            print(e)
            return apology("Database error (maps)", 500)

        # Auto login
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

# MAP PAGE displaying all users
@app.route("/map")
def map_page():
    locations = db.execute("""
        SELECT users.name, users.sector, maps.latitude, maps.longitude
        FROM users
        JOIN maps ON users.id = maps.user_id
    """)
    return render_template("map.html", locations=locations)


# GALLERY PAGE
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# ABOUT PAGE
@app.route("/about")
def about():
    user = None

    if session.get("user_id"):
        user = db.execute(
            "SELECT name, sector FROM users WHERE id = ?",
            session["user_id"]
        )[0]

    return render_template("about.html", user=user)


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
