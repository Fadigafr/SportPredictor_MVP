import sqlite3

def init_db():
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,email TEXT,password TEXT)")
    conn.commit()
    conn.close()
