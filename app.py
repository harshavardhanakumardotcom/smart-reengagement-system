from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3

app = Flask(__name__)

# 🔔 Notifications
notifications = []

# 🧠 Analyze user
def analyze_user(user):
    if user["last_active_days"] > 10:
        return "high_risk", "⚠️ You are inactive! Improve now!"
    elif user["last_active_days"] > 5:
        return "inactive", "👋 We miss you! Come back!"
    else:
        return "active", "✅ Doing great!"

# 🧠 Reason (bonus)
def get_reason(user):
    if user["time_spent"] < 5:
        return "Low Engagement 😴"
    elif user["marks"] < 50:
        return "Low Performance 📉"
    else:
        return "Inactive Behavior"

# 🔔 Save notification (ALWAYS push for demo)
def send_notification(user, message):
    notifications.append({
        "name": user["name"],
        "message": message
    })

# 🗄️ Get users
def get_users():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT name, last_active_days, time_spent, marks FROM users")
    rows = cursor.fetchall()

    conn.close()

    users = []
    for row in rows:
        users.append({
            "name": row[0],
            "last_active_days": row[1],
            "time_spent": row[2],
            "marks": row[3]
        })

    return users

# 🔄 Background job
def check_users():
    print("🔄 Checking users...")  # debug

    users = get_users()

    for user in users:
        status, message = analyze_user(user)

        if status in ["inactive", "high_risk"]:
            reason = get_reason(user)
            full_message = f"{message} | {reason}"
            send_notification(user, full_message)

# 🏠 Home
@app.route("/")
def home():
    users = get_users()
    enriched = []

    for user in users:
        status, message = analyze_user(user)
        enriched.append({**user, "status": status, "message": message})

    return render_template("index.html", users=enriched)

# 🔔 Notifications API
@app.route("/get_notifications")
def get_notifications():
    global notifications
    data = notifications[:]
    notifications = []   # clear safely
    return jsonify(data)

# ➕ Add user
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, last_active_days, time_spent, marks) VALUES (?, ?, ?, ?)",
        (data["name"], data["last_active_days"], data["time_spent"], data["marks"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User added successfully"})

# 🚀 Run safely
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_users, 'interval', seconds=10)
    scheduler.start()

    print("🚀 Scheduler started...")

    app.run(debug=True, use_reloader=False)