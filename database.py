import sqlite3
from datetime import datetime

# -----------------------------
# CREATE DATABASE + TABLES
# -----------------------------
def create_table():

    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    # MASTER TABLE (Unique Users)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE
    )
    """)

    # TRANSACTION TABLE (History)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        domain TEXT,
        skills TEXT,
        ats_score INTEGER,
        match_percentage INTEGER,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# SAVE USER DATA
# -----------------------------
def save_user_data(name, email, domain, skills, ats_score, match_percentage):

    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    # Step 1: Check if user already exists
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
    else:
        # Create new user
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        user_id = cursor.lastrowid

    # Step 2: Insert analysis history
    skills_str = ", ".join(skills)

    cursor.execute("""
    INSERT INTO analysis_history 
    (user_id, domain, skills, ats_score, match_percentage, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        domain,
        skills_str,
        ats_score,
        match_percentage,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# -----------------------------
# GET USER HISTORY
# -----------------------------
def get_user_history(email):

    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT ah.domain, ah.ats_score, ah.match_percentage, ah.created_at
    FROM analysis_history ah
    JOIN users u ON ah.user_id = u.user_id
    WHERE u.email = ?
    ORDER BY ah.record_id DESC
    """, (email,))

    data = cursor.fetchall()

    conn.close()

    return data