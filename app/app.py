import os
import sqlite3

from flask import Flask, current_app, jsonify, render_template, request


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["DB_PATH"] = os.environ.get("DB_PATH", "todo.db")
    if test_config:
        app.config.update(test_config)

    def get_db():
        conn = sqlite3.connect(current_app.config["DB_PATH"])
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        conn = get_db()
        conn.execute(
            """CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )"""
        )
        conn.commit()
        conn.close()

    with app.app_context():
        init_db()

    @app.get("/health")
    def health():
        return jsonify(status="ok v2")

    @app.get("/api/todos")
    def list_todos():
        conn = get_db()
        rows = conn.execute("SELECT * FROM todos ORDER BY id").fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])

    @app.post("/api/todos")
    def add_todo():
        data = request.get_json(silent=True) or {}
        title = data.get("title", "").strip()
        if not title:
            return jsonify(error="title is required"), 400
        conn = get_db()
        cur = conn.execute("INSERT INTO todos (title) VALUES (?)", (title,))
        conn.commit()
        row = conn.execute(
            "SELECT * FROM todos WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
        conn.close()
        return jsonify(dict(row)), 201

    @app.patch("/api/todos/<int:todo_id>")
    def toggle_todo(todo_id):
        conn = get_db()
        conn.execute("UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,))
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        conn.close()
        if row is None:
            return jsonify(error="not found"), 404
        return jsonify(dict(row))

    @app.get("/")
    def index():
        conn = get_db()
        rows = conn.execute("SELECT * FROM todos ORDER BY id").fetchall()
        conn.close()
        return render_template("index.html", todos=rows)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
