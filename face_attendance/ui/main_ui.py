# -*- coding: utf-8 -*-
import tkinter as tk
from ui.register_ui import RegisterUI
from ui.attendance_ui import AttendanceUI
from ui.report_ui import ReportUI

class MainUI:
    def __init__(self, db):
        self.db = db

        self.root = tk.Tk()
        self.root.title("Face Attendance System")
        self.root.geometry("360x240")
        self.root.resizable(False, False)

        tk.Label(
            self.root,
            text="Face Attendance System",
            font=("Arial", 14, "bold")
        ).pack(pady=16)

        tk.Button(
            self.root,
            text="Register Person",
            width=20,
            command=self.open_register
        ).pack(pady=6)

        tk.Button(
            self.root,
            text="Face Check-in",
            width=20,
            command=self.open_attendance
        ).pack(pady=6)

        tk.Button(
            self.root,
            text="Attendance Report",
            width=20,
            command=self.open_report
        ).pack(pady=6)


        tk.Label(
            self.root,
            text="Step 1: Main UI & Database Init (Done)\nStep 2: Register, Check-in, Report",
            fg="gray"
        ).pack(pady=12)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def open_register(self):
        RegisterUI(self.root, self.db)

    def open_attendance(self):
        AttendanceUI(self.root, self.db)

    def open_report(self):
        ReportUI(self.root, self.db)

    def on_close(self):
        self.db.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
