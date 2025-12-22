# -*- coding: utf-8 -*-
import sqlite3

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
