import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

users = [
    ("Rahul", 2, 30, 85),
    ("Anjali", 7, 5, 60),
    ("Kiran", 15, 2, 40),
    ("Priya", 12, 3, 45),
    ("Arjun", 1, 40, 90),
    ("Sneha", 9, 6, 55)
]

cursor.executemany(
    "INSERT INTO users (name, last_active_days, time_spent, marks) VALUES (?, ?, ?, ?)",
    users
)

conn.commit()
conn.close()

print("✅ Users inserted successfully!")