from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)
DB = "tracker.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                title TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        ''')

@app.route("/")
def index():
    with get_db() as conn:
        assignments = conn.execute(
            "SELECT * FROM assignments ORDER BY due_date ASC"
        ).fetchall()
    today = date.today().isoformat()
    return render_template("index.html", assignments=assignments, today=today)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        subject = request.form["subject"]
        title = request.form["title"]
        due_date = request.form["due_date"]
        with get_db() as conn:
            conn.execute(
                "INSERT INTO assignments (subject, title, due_date) VALUES (?, ?, ?)",
                (subject, title, due_date)
            )
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/done/<int:id>")
def mark_done(id):
    with get_db() as conn:
        conn.execute("UPDATE assignments SET status='done' WHERE id=?", (id,))
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    with get_db() as conn:
        conn.execute("DELETE FROM assignments WHERE id=?", (id,))
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)