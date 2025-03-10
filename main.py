import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from database import init_db
from app import CalendarApp

def main():
    app = QApplication(sys.argv)

    # check if database was made
    if not init_db('calendar.db'):
        QMessageBox.critical(None, "Error", "could not load your database...")
        sys.exit(1)
    window = CalendarApp()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()

