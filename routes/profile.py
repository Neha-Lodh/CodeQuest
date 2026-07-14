from flask import (
    Blueprint,
    render_template,
    session,
    redirect
)

from db import get_db_connection

profile_bp = Blueprint(
    "profile",
    __name__
)


@profile_bp.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            users.*,
            avatars.name AS avatar_name,
            avatars.image
        FROM users

        LEFT JOIN avatars

        ON users.equipped_avatar = avatars.id

        WHERE users.id=%s
        """,
        (session["user_id"],)
    )

    user = cursor.fetchone()

    cursor.execute(
        """
        SELECT
            achievements.title,
            achievements.icon

        FROM user_achievements

        JOIN achievements

        ON achievements.id=user_achievements.achievement_id

        WHERE user_achievements.user_id=%s

        ORDER BY earned_at DESC

        LIMIT 5
        """,
        (session["user_id"],)
    )

    achievements = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "profile.html",
        user=user,
        achievements=achievements
    )