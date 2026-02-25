# main.py
import sys
from PyQt6.QtWidgets import QApplication
from database import Database
from student_repository import StudentRepository
from student_service import StudentService
from ui_main import MainWindow

def main():
    db = Database()
    db.initialize()

    repo = StudentRepository(db)
    service = StudentService(repo)

    app = QApplication(sys.argv)
    window = MainWindow(service)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()