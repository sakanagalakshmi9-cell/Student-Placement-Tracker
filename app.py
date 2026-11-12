
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    conn = sqlite3.connect("placement.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create database table
def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()

# Home page
@app.route("/")
def home():
    conn = get_db()

    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["status"] == "Completed"
    )

    pending = total - completed

    progress = round(
        (completed / total) * 100
    ) if total else 0

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending,
        progress=progress
    )

# Add new task
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    category = request.form.get("category")

    if title and category:
        conn = get_db()

        conn.execute(
            "INSERT INTO tasks (title, category) VALUES (?, ?)",
            (title, category)
        )

        conn.commit()
        conn.close()

    return redirect("/")

# Complete task
@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    conn = get_db()

    conn.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

# Delete task
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

# Run application
if __name__ == "__main__":
    create_table()
    app.run(debug=True)