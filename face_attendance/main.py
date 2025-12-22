# -*- coding: utf-8 -*-
from database.db_manager import DBManager
from ui.main_ui import MainUI

def main():
    db = DBManager("attendance.db")
    app = MainUI(db)
    app.run()

if __name__ == "__main__":
    main()
