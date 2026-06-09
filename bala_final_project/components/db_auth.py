import sqlite3


DB_NAME = "users.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================
def connect_db():

    return sqlite3.connect(DB_NAME)


# =========================================================
# CREATE USERS TABLE
# =========================================================
def create_users_table():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL
    )
    """)

    conn.commit()

    conn.close()


# =========================================================
# REGISTER USER
# =========================================================
def register_user(name, email, password):

    conn = connect_db()

    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users (
            name,
            email,
            password
        )
        VALUES (?, ?, ?)
        """, (name, email, password))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# =========================================================
# LOGIN USER
# =========================================================
def login_user(email):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, password
    FROM users
    WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    return user


# =========================================================
# PREDICTION HISTORY — PERMANENT STORAGE
# =========================================================
import json

def create_history_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user      TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            record    TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_prediction_record(user, timestamp, record):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prediction_history (user, timestamp, record)
        VALUES (?, ?, ?)
    """, (user, timestamp, json.dumps(record)))
    conn.commit()
    conn.close()


def load_prediction_history(user):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT record FROM prediction_history
        WHERE user = ?
        ORDER BY id DESC
    """, (user,))
    rows = cursor.fetchall()
    conn.close()
    return [json.loads(row[0]) for row in rows]


def clear_prediction_history(user):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM prediction_history WHERE user = ?
    """, (user,))
    conn.commit()
    conn.close()

    