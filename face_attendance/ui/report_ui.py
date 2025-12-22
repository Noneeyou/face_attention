import csv
import tkinter as tk
from tkinter import filedialog, messagebox

from attendance.attendance_manager import AttendanceManager


class ReportUI:
    def __init__(self, master, db):
        self.db = db
        self.manager = AttendanceManager(db)

        self.win = tk.Toplevel(master)
        self.win.title("Attendance Report")
        self.win.geometry("560x420")
        self.win.resizable(False, False)

        tk.Label(self.win, text="Start Time (YYYY-MM-DD HH:MM:SS)").pack(pady=(10, 0))
        self.start_entry = tk.Entry(self.win, width=30)
        self.start_entry.pack()

        tk.Label(self.win, text="End Time (YYYY-MM-DD HH:MM:SS)").pack(pady=(10, 0))
        self.end_entry = tk.Entry(self.win, width=30)
        self.end_entry.pack()

        tk.Button(
            self.win,
            text="Load Report",
            width=15,
            command=self.load_report
        ).pack(pady=8)

        tk.Button(
            self.win,
            text="Export CSV",
            width=15,
            command=self.export_csv
        ).pack(pady=4)

        self.text = tk.Text(self.win, width=70, height=15)
        self.text.pack(pady=10)

    def load_report(self):
        start_time = self.start_entry.get().strip() or None
        end_time = self.end_entry.get().strip() or None
        summary = self.manager.daily_summary(start_time, end_time)

        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "Daily Attendance Summary\n")
        self.text.insert(tk.END, "-" * 60 + "\n")
        for item in summary:
            line = (
                f"{item['day']} | {item['name']} (ID {item['person_id']}) | "
                f"{item['first_time']} -> {item['last_time']} | "
                f"{item['hours']} hrs\n"
            )
            self.text.insert(tk.END, line)

    def export_csv(self):
        start_time = self.start_entry.get().strip() or None
        end_time = self.end_entry.get().strip() or None
        summary = self.manager.daily_summary(start_time, end_time)
        if not summary:
            messagebox.showwarning("No Data", "No report data to export.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Person ID", "Name", "First Time", "Last Time", "Hours"])
            for item in summary:
                writer.writerow([
                    item["day"],
                    item["person_id"],
                    item["name"],
                    item["first_time"],
                    item["last_time"],
                    item["hours"],
                ])
        messagebox.showinfo("Exported", f"Report saved to {file_path}")
