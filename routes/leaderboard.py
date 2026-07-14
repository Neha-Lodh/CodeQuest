from flask import (
    Blueprint,
    render_template,
    session,
    redirect
)

from db import get_db_connection

leaderboard_bp = Blueprint(
    "leaderboard",
    __name__
)


@leaderboard_bp.route("/leaderboard")
def leaderboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        users.username,
        users.level,
        users.xp,
        users.coins,
        users.streak,
        avatars.image
    FROM users
    LEFT JOIN avatars
        ON users.equipped_avatar = avatars.id
    ORDER BY users.xp DESC, users.level DESC
""")

    players = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "leaderboard.html",
        players=players
    )