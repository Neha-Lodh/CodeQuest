from flask import (
    Blueprint,
    render_template,
    session,
    redirect
)

from db import get_db_connection

shop_bp = Blueprint("shop", __name__)


@shop_bp.route("/shop")
def shop():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get user's coins and equipped avatar
    cursor.execute(
        """
        SELECT
            coins,
            equipped_avatar
        FROM users
        WHERE id=%s
        """,
        (session["user_id"],)
    )

    user = cursor.fetchone()

    # Get all avatars
    cursor.execute(
        """
        SELECT *
        FROM avatars
        ORDER BY price
        """
    )

    avatars = cursor.fetchall()

    # Get avatars owned by this user
    cursor.execute(
        """
        SELECT avatar_id
        FROM user_avatars
        WHERE user_id=%s
        """,
        (session["user_id"],)
    )

    owned = [row["avatar_id"] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render_template(
        "shop.html",
        avatars=avatars,
        owned=owned,
        coins=user["coins"],
        equipped=user["equipped_avatar"]
    )

@shop_bp.route("/buy/<int:avatar_id>")
def buy_avatar(avatar_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # User
    cursor.execute(
        """
        SELECT coins
        FROM users
        WHERE id=%s
        """,
        (session["user_id"],)
    )

    user = cursor.fetchone()

    # Avatar
    cursor.execute(
        """
        SELECT *
        FROM avatars
        WHERE id=%s
        """,
        (avatar_id,)
    )

    avatar = cursor.fetchone()

    if not avatar:
        cursor.close()
        conn.close()
        return redirect("/shop")

    # Already owned?
    cursor.execute(
        """
        SELECT *
        FROM user_avatars
        WHERE
            user_id=%s
            AND avatar_id=%s
        """,
        (session["user_id"], avatar_id)
    )

    if cursor.fetchone():

        cursor.close()
        conn.close()

        return redirect("/shop")

    # Enough coins?
    if user["coins"] < avatar["price"]:

        cursor.close()
        conn.close()

        return redirect("/shop")

    # Deduct coins
    cursor.execute(
        """
        UPDATE users
        SET coins = coins - %s
        WHERE id=%s
        """,
        (
            avatar["price"],
            session["user_id"]
        )
    )

    # Give avatar
    cursor.execute(
        """
        INSERT INTO user_avatars
        (
            user_id,
            avatar_id
        )
        VALUES(%s,%s)
        """,
        (
            session["user_id"],
            avatar_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/shop")

@shop_bp.route("/equip/<int:avatar_id>")
def equip_avatar(avatar_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check ownership
    cursor.execute(
        """
        SELECT *
        FROM user_avatars
        WHERE
            user_id=%s
            AND avatar_id=%s
        """,
        (
            session["user_id"],
            avatar_id
        )
    )

    if cursor.fetchone():

        cursor.execute(
            """
            UPDATE users
            SET equipped_avatar=%s
            WHERE id=%s
            """,
            (
                avatar_id,
                session["user_id"]
            )
        )

        conn.commit()

    cursor.close()
    conn.close()

    return redirect("/shop")