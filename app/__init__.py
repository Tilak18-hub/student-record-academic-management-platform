import os
import sqlite3
from flask import Flask, jsonify, render_template, request


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["DATABASE"] = os.environ.get(
        "DATABASE_PATH", "/tmp/student_records.db"
    )

    if test_config:
        app.config.update(test_config)

    def get_db():
        connection = sqlite3.connect(app.config["DATABASE"])
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
            FOREIGN KEY(student_id) REFERENCES students(id)
        );
    """)
    db.commit()
    db.close()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify({
            "status": "healthy",
            "service": "student-record-platform"
        })

    @app.get("/api/students")
    def list_students():
        db = get_db()
        try:
            rows = db.execute(
                "SELECT * FROM students ORDER BY id"
            ).fetchall()
            return jsonify([dict(row) for row in rows])
        finally:
            db.close()

    @app.post("/api/students")
    def create_student():
        data = request.get_json(silent=True) or {}
        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip()
        course = str(data.get("course", "")).strip()

        if not name or not email or not course:
            return jsonify({
                "error": "name, email, and course are required"
            }), 400

        db = get_db()
        try:
            cursor = db.execute(
                "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
                (name, email, course)
            )
            db.commit()
            row = db.execute(
                "SELECT * FROM students WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return jsonify(dict(row)), 201
        except sqlite3.IntegrityError:
            return jsonify({
                "error": "Email already exists or data is invalid"
            }), 409
        finally:
            db.close()

    @app.post("/api/marks")
    def create_mark():
        data = request.get_json(silent=True) or {}
        try:
            student_id = int(data.get("student_id"))
            score = float(data.get("score"))
        except (TypeError, ValueError):
            return jsonify({
                "error": "student_id and numeric score are required"
            }), 400

        subject = str(data.get("subject", "")).strip()
        if not subject or not 0 <= score <= 100:
            return jsonify({
                "error": "subject is required and score must be 0-100"
            }), 400

        db = get_db()
        try:
            student = db.execute(
                "SELECT id FROM students WHERE id = ?", (student_id,)
            ).fetchone()
            if student is None:
                return jsonify({"error": "Student not found"}), 404

            cursor = db.execute(
                "INSERT INTO marks (student_id, subject, score) VALUES (?, ?, ?)",
                (student_id, subject, score)
            )
            db.commit()
            row = db.execute(
                "SELECT * FROM marks WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return jsonify(dict(row)), 201
        finally:
            db.close()

    @app.get("/api/marks")
    def list_marks():
        db = get_db()
        try:
            rows = db.execute("""
                SELECT marks.id, marks.student_id,
                       students.name AS student_name,
                       marks.subject, marks.score
                FROM marks
                JOIN students ON students.id = marks.student_id
                ORDER BY marks.id
            """).fetchall()
            return jsonify([dict(row) for row in rows])
        finally:
            db.close()

    return app
