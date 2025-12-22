from pathlib import Path

ROOT = Path("face_attendance")

DIRS = [
    "ui",
    "database",
    "face",
    "attendance",
    "utils",
]

FILES = [
    "main.py",
    "ui/main_ui.py",
    "ui/register_ui.py",
    "ui/attendance_ui.py",
    "ui/report_ui.py",
    "database/db_manager.py",
    "face/face_capture.py",
    "face/face_recognizer.py",
    "attendance/attendance_manager.py",
    "utils/time_utils.py",
]

def main():
    ROOT.mkdir(exist_ok=True)

    for d in DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
        (ROOT / d / "__init__.py").touch()

    for f in FILES:
        (ROOT / f).touch()

    (ROOT / "attendance.db").touch()

    print("✅ 项目结构已创建：face_attendance")

if __name__ == "__main__":
    main()
