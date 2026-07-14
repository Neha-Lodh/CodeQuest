from flask import (
    Blueprint,
    render_template,
    session,
    redirect
)

from db import get_db_connection

achievements_bp = Blueprint(
    "achievements",
    __name__
)


@achievements_bp.route("/achievements")
def achievements():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            a.*,

            CASE

                WHEN ua.id IS NULL

                THEN 0

                ELSE 1

            END AS unlocked

        FROM achievements a

        LEFT JOIN user_achievements ua

        ON a.id = ua.achievement_id

        AND ua.user_id=%s

        ORDER BY a.id
        """,
        (session["user_id"],)
    )

    achievements = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "achievements.html",
        achievements=achievements
    )

def check_achievements(user_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Player stats
    cursor.execute(
        """
        SELECT
            xp,
            coins,
            unlocked_world,
            total_challenges
        FROM users
        WHERE id=%s
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    xp = user["xp"]
    coins = user["coins"]
    worlds = user["unlocked_world"]
    completed = user["total_challenges"]

    achievements = []

    if completed >= 1:
        achievements.append(1)

    if xp >= 500:
        achievements.append(2)

    if coins >= 500:
        achievements.append(3)

    if worlds >= 2:
        achievements.append(4)

    if worlds >= 3:
        achievements.append(5)

    if worlds >= 4:
        achievements.append(6)

    if worlds >= 5:
        achievements.append(7)

    if xp >= 5000:
        achievements.append(8)

    for achievement_id in achievements:

        cursor.execute(
            """
            INSERT IGNORE INTO user_achievements
            (
                user_id,
                achievement_id
            )
            VALUES(%s,%s)
            """,
            (
                user_id,
                achievement_id
            )
        )

    conn.commit()

    cursor.close()
    conn.close()