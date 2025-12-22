# -*- coding: utf-8 -*-
import sqlite3
import pickle


class DBManager:
    def __init__(self, db_path="attendance.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._init_tables()

    def _init_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Person(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            job_id TEXT,
            department TEXT
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Face(
            person_id INTEGER PRIMARY KEY,
            encoding BLOB,
            FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
        );
        """)
        self.conn.commit()

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass

    def add_person(self, name, job_id, department):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO Person(name, job_id, department) VALUES (?, ?, ?)",
            (name, job_id, department)
        )
        self.conn.commit()
        return cur.lastrowid

    def update_person(self, person_id, name, job_id, department):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE Person SET name = ?, job_id = ?, department = ? WHERE id = ?",
            (name, job_id, department, person_id)
        )
        self.conn.commit()

    def get_person(self, person_id):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, name, job_id, department FROM Person WHERE id = ?",
            (person_id,)
        )
        return cur.fetchone()

    def list_persons(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, job_id, department FROM Person ORDER BY id")
        return cur.fetchall()

    def add_face_encoding(self, person_id, encoding):
        data = pickle.dumps(encoding)
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO Face(person_id, encoding) VALUES (?, ?)",
            (person_id, data)
        )
        self.conn.commit()

    def get_face_encoding(self, person_id):
        cur = self.conn.cursor()
        cur.execute("SELECT encoding FROM Face WHERE person_id = ?", (person_id,))
        row = cur.fetchone()
        if not row:
            return None
        return pickle.loads(row[0])

    def get_all_face_encodings(self):
        cur = self.conn.cursor()
        cur.execute("SELECT person_id, encoding FROM Face")
        results = []
        for person_id, encoding in cur.fetchall():
            results.append((person_id, pickle.loads(encoding)))
        return results

    def add_attendance(self, person_id, time_str):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO Attendance(person_id, time) VALUES (?, ?)",
            (person_id, time_str)
        )
        self.conn.commit()

    def list_attendance(self, start_time=None, end_time=None):
        cur = self.conn.cursor()
        if start_time and end_time:
            cur.execute(
                """
                SELECT Attendance.id, Attendance.person_id, Person.name, Attendance.time
                FROM Attendance
                JOIN Person ON Attendance.person_id = Person.id
                WHERE Attendance.time BETWEEN ? AND ?
                ORDER BY Attendance.time
                """,
                (start_time, end_time)
            )
        else:
            cur.execute(
                """
                SELECT Attendance.id, Attendance.person_id, Person.name, Attendance.time
                FROM Attendance
                JOIN Person ON Attendance.person_id = Person.id
                ORDER BY Attendance.time
                """
            )
        return cur.fetchall()

    def list_daily_summary(self, start_time=None, end_time=None):
        cur = self.conn.cursor()
        query = """
            SELECT Person.id,
                   Person.name,
                   date(Attendance.time) AS day,
                   MIN(Attendance.time) AS first_time,
                   MAX(Attendance.time) AS last_time
            FROM Attendance
            JOIN Person ON Attendance.person_id = Person.id
        """
        params = []
        if start_time and end_time:
            query += " WHERE Attendance.time BETWEEN ? AND ?"
            params.extend([start_time, end_time])
        query += " GROUP BY Person.id, day ORDER BY day, Person.id"
        cur.execute(query, params)
        return cur.fetchall()
