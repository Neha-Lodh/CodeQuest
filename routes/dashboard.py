from flask import Blueprint, render_template, session, redirect

from db import get_db_connection

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            users.*,
            avatars.image
        FROM users

        LEFT JOIN avatars

        ON users.equipped_avatar = avatars.id

        WHERE users.id=%s
        """,
        (session["user_id"],)
    )

    user = cursor.fetchone()
    avatar = user.get("image") or "knight.png"

    print(user)
    print("Avatar =", avatar)
    # print(user)

    if not user:
        cursor.close()
        conn.close()
        return redirect("/login")

    xp = user.get("xp", 0)

    progress = xp % 100

    avatar = user.get("image") or "knight.png"

    cursor.execute(
        """
        SELECT badge_name
        FROM badges
        LIMIT 3
        """
    )

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
        badges=badges
    )