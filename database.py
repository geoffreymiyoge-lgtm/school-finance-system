import sqlite3
from config import DATABASE

def get_conn():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        admission_no TEXT PRIMARY KEY,
        name TEXT,
        grade TEXT,
        stream TEXT,
        parent TEXT,
        phone TEXT,
        expected REAL DEFAULT 1500,
        paid REAL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admission_no TEXT,
        date TEXT,
        amount REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        amount REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS loans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher TEXT,
        date TEXT,
        given REAL,
        repaid REAL DEFAULT 0
    )
    """)

    cur.execute("""
    INSERT OR IGNORE INTO users(username,password)
    VALUES('admin','admin123')
    """)

    conn.commit()
    conn.close()
