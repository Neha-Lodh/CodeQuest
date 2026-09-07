from flask import Blueprint, render_template, session, redirect

from db import get_db_connection

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------------- USER ----------------

    cursor.execute("""
        SELECT
            users.*,
            avatars.image
        FROM users
        LEFT JOIN avatars
            ON users.equipped_avatar = avatars.id
        WHERE users.id=%s
    """, (session["user_id"],))

    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return redirect("/login")

    avatar = user["image"] if user["image"] else "knight.png"

    xp = user["xp"]
    progress = xp % 100

    # ---------------- NEXT CHALLENGE ----------------

    cursor.execute("""
        SELECT
            c.id,
            c.title,
            c.world
        FROM challenges c

        LEFT JOIN completed_challenges cc
            ON c.id = cc.challenge_id
            AND cc.user_id=%s

        WHERE cc.challenge_id IS NULL

        ORDER BY c.id
        LIMIT 1
    """, (session["user_id"],))

    next_challenge = cursor.fetchone()

    # ---------------- BADGES ----------------

    cursor.execute("""
        SELECT badge_name
        FROM badges
        LIMIT 3
    """)

    badges = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        username=user["username"],
        xp=user["xp"],
        coins=user["coins"],
        level=user["level"],
        streak=user["streak"],
        progress=progress,
        avatar=avatar,
        badges=badges,
        next_challenge=next_challenge
    )