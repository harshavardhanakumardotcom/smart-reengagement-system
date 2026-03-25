import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    last_active_days INTEGER,
    time_spent INTEGER,
    marks INTEGER
)
""")

conn.commit()
conn.close()

print("Database created!")