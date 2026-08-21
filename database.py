import sqlite3
from hashlib import sha256

DB = "users.db"


def get_conn():

    return sqlite3.connect(
        DB,
        check_same_thread=False
    )


def create_default_admin():

    conn = get_conn()
    c = conn.cursor()

    password = sha256(
        "SportPredictor2026!".encode()
    ).hexdigest()

    c.execute(
        """
        INSERT OR IGNORE INTO users
        (
            email,
            password,
            is_admin
        )
        VALUES (?, ?, ?)
        """,
        (
            "admin@sportpredictor.com",
            password,
            1
        )
    )

    conn.commit()
    conn.close()


def init_db():

    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        competition TEXT,
        match_name TEXT,
        prediction TEXT,
        btts TEXT,
        score_exact TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS predictions_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date TEXT,

        sport TEXT,

        match TEXT,

        fixture_id INTEGER,

        prediction TEXT,

        ai_index REAL,

        odd REAL,

        result TEXT
    )
    """)

    conn.commit()
    conn.close()

    # Création automatique du compte admin
    create_default_admin()


def count_predictions_db():

    conn = get_conn()
    c = conn.cursor()

    c.execute(
        "SELECT COUNT(*) FROM predictions_history"
    )

    total = c.fetchone()[0]

    conn.close()

    return total


def count_users():

    conn = get_conn()
    c = conn.cursor()

    c.execute(
        "SELECT COUNT(*) FROM users"
    )

    total = c.fetchone()[0]

    conn.close()

    return total


def db_diagnostics():

    conn = get_conn()
    c = conn.cursor()

    c.execute(
        "SELECT COUNT(*) FROM users"
    )
    users = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM predictions_history"
    )
    predictions = c.fetchone()[0]

    conn.close()

    return users, predictions

def save_prediction_db(
    date,
    sport,
    match,
    fixture_id,
    prediction,
    ai_index,
    odd,
    result="PENDING"
):

    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        INSERT INTO predictions_history
        (
            date,
            sport,
            match,
            fixture_id,
            prediction,
            ai_index,
            odd,
            result
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        date,
        sport,
        match,
        fixture_id,
        prediction,
        ai_index,
        odd,
        result
    ))

    conn.commit()
    conn.close()

def load_predictions_db():

    conn = get_conn()

    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM predictions_history
        ORDER BY id DESC
    """)

    rows = c.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def update_prediction_result(
    prediction_id,
    result
):

    conn = get_conn()

    c = conn.cursor()

    c.execute(
        """
        UPDATE predictions_history
        SET result = ?
        WHERE id = ?
        """,
        (result, prediction_id)
    )

    conn.commit()
    conn.close()

