from flask import Blueprint, render_template, session, redirect

from db import get_db_connection

worlds_bp = Blueprint("worlds", __name__)


@worlds_bp.route("/worlds")
def worlds():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT unlocked_world
        FROM users
        WHERE id=%s
        """,
        (session["user_id"],)
    )

    user = cursor.fetchone()

    world_data = [
        (1, "Beginner Forest", "🌲 Beginner Forest", "forest.png", "🌳 Forest Guardian", "Easy"),
        (2, "Function Castle", "🏰 Function Castle", "castle.png", "👑 Function King", "Medium"),
        (3, "Algorithm Cave", "🕳 Algorithm Cave", "cave.png", "🐉 Algorithm Dragon", "Hard"),
        (4, "Data Structure Glacier", "❄ Data Structure Glacier", "glacier.png", "🧊 Ice Titan", "Expert"),
        (5, "Python Kingdom", "👑 Python Kingdom", "kingdom.png", "🐍 Python Emperor", "Legendary")
    ]

    worlds = []

    for wid, db_name, display_name, image, boss, difficulty in world_data:

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM challenges
            WHERE world=%s
            """,
            (db_name,)
        )

        total = cursor.fetchone()["total"]

        cursor.execute(
            """
            SELECT COUNT(*) AS completed
            FROM completed_challenges cc
            JOIN challenges c
            ON cc.challenge_id = c.id
            WHERE cc.user_id=%s
            AND c.world=%s
            """,
            (
                session["user_id"],
                db_name
            )
        )

        completed = cursor.fetchone()["completed"]

        progress = 0

        if total > 0:
            progress = int((completed / total) * 100)

        worlds.append({
            "id": wid,
            "name": display_name,
            "image": image,
            "boss": boss,
            "difficulty": difficulty,
            "progress": progress
        })

    cursor.close()
    conn.close()

    return render_template(
        "worlds.html",
        worlds=worlds,
        unlocked=user["unlocked_world"]
    )