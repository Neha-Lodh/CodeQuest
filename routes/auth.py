from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from datetime import date, timedelta

from db import get_db_connection

auth_bp = Blueprint("auth", __name__)


# ---------------- HOME ---------------- #

@auth_bp.route("/")
def home():
    return render_template("home.html")


# ---------------- REGISTER ---------------- #

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        if cursor.fetchone():

            flash("Email already exists.", "danger")

            cursor.close()
            conn.close()

            return redirect("/register")

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password,
                xp,
                coins,
                level,
                streak,
                unlocked_world
            )
            VALUES
            (%s,%s,%s,0,0,1,0,1)
            """,
            (
                username,
                email,
                hashed_password
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Registration successful! Please login.", "success")

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            flash("Invalid email or password.", "danger")

            cursor.close()
            conn.close()

            return redirect("/login")

        if not check_password_hash(user["password"], password):

            flash("Invalid email or password.", "danger")

            cursor.close()
            conn.close()

            return redirect("/login")

        today = date.today()
        last_login = user["last_login"]

        if last_login is None:

            streak = 1

        elif last_login == today:

            streak = user["streak"]

        elif last_login == today - timedelta(days=1):

            streak = user["streak"] + 1

        else:

            streak = 1

        cursor.execute(
            """
            UPDATE users
            SET
                streak=%s,
                last_login=%s
            WHERE id=%s
            """,
            (
                streak,
                today,
                user["id"]
            )
        )

        conn.commit()

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        cursor.close()
        conn.close()

        return redirect("/dashboard")

    return render_template("login.html")


# ---------------- LOGOUT ---------------- #

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect("/")