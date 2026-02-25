# ui_main.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QFileDialog
)
from PyQt6.QtCore import Qt

from models import Student
from student_service import StudentService
import csv
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self, service: StudentService):
        super().__init__()
        self.service = service

        self.setWindowTitle("Student CRUD - PyQt6 + SQLite")
        self.resize(900, 600)

        self._build_ui()
        self.load_data()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # ===== Inputs =====
        self.txt_student_id = QLineEdit()
        self.txt_first_name = QLineEdit()
        self.txt_last_name = QLineEdit()
        self.txt_major = QLineEdit()
        self.txt_faculty = QLineEdit()
        self.txt_nick_name = QLineEdit()
        self.txt_phone_number = QLineEdit()
        self.txt_email = QLineEdit()

        self.txt_student_id.setPlaceholderText("เช่น 66010001")
        self.txt_student_id.setValidator(QIntValidator(0,999999999))
        self.txt_first_name.setPlaceholderText("ชื่อ")
        self.txt_last_name.setPlaceholderText("นามสกุล")
        self.txt_major.setPlaceholderText("สาขาวิชา")
        self.txt_faculty.setPlaceholderText("คณะ")
        self.txt_nick_name.setPlaceholderText("ชื่อเล่น")
        self.txt_phone_number.setPlaceholderText("เบอร์โทรศัพท์")
        self.txt_email.setPlaceholderText("อีเมล")

        form_layout.addWidget(QLabel("รหัสนักศึกษา"))
        form_layout.addWidget(self.txt_student_id)
        form_layout.addWidget(QLabel("ชื่อ"))
        form_layout.addWidget(self.txt_first_name)
        form_layout.addWidget(QLabel("นามสกุล"))
        form_layout.addWidget(self.txt_last_name)
        form_layout.addWidget(QLabel("สาขาวิชา"))
        form_layout.addWidget(self.txt_major)
        form_layout.addWidget(QLabel("คณะ"))
        form_layout.addWidget(self.txt_faculty)
        form_layout.addWidget(QLabel("ชื่อเล่น"))
        form_layout.addWidget(self.txt_nick_name)
        form_layout.addWidget(QLabel("เบอร์โทรศัพท์"))
        form_layout.addWidget(self.txt_phone_number)
        form_layout.addWidget(QLabel("อีเมล"))
        form_layout.addWidget(self.txt_email)
        
        # ===== Buttons =====
        self.btn_add = QPushButton("เพิ่ม")
        self.btn_update = QPushButton("แก้ไข")
        self.btn_delete = QPushButton("ลบ")
        self.btn_clear = QPushButton("ล้างฟอร์ม")
        self.btn_refresh = QPushButton("รีเฟรช")
        self.btn_export = QPushButton("Export CSV")
        self.btn_import = QPushButton("Import CSV")
        self.btn_report = QPushButton("รายงาน")

        self.btn_add.clicked.connect(self.add_student)
        self.btn_update.clicked.connect(self.update_student)
        self.btn_delete.clicked.connect(self.delete_student)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_export.clicked.connect(self.export_csv)
        self.btn_import.clicked.connect(self.import_csv)
        self.btn_report.clicked.connect(self.show_report)

        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_update)
        button_layout.addWidget(self.btn_delete)
        button_layout.addWidget(self.btn_clear)
        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_export)
        button_layout.addWidget(self.btn_import)
        button_layout.addWidget(self.btn_report)
        button_layout.addStretch()

        # ===== SEARCH BAR =====
        search_layout = QHBoxLayout()

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("ค้นหา: รหัส/ชื่อ/นามสกุล/สาขา/คณะ/ชื่อเล่น/เบอร์โทรศัพท์/อีเมล")

        self.btn_search = QPushButton("ค้นหา")
        self.btn_search_clear = QPushButton("แสดงทั้งหมด")

        self.btn_search.clicked.connect(self.on_search)
        self.btn_search_clear.clicked.connect(self.on_search_clear)
        self.txt_search.returnPressed.connect(self.on_search)

        search_layout.addWidget(QLabel("Search"))
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(self.btn_search)
        search_layout.addWidget(self.btn_search_clear)
        search_layout.addStretch()

        # ===== Table =====
        self.table = QTableWidget(0, 8)
        self.table.setSortingEnabled(True)
        self.table.setHorizontalHeaderLabels(["รหัสนักศึกษา", "ชื่อ", "นามสกุล", "สาขาวิชา", "คณะ","ชื่อเล่น","เบอร์โทรศัพท์","อีเมล"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.on_row_selected)
        
        # ===== Layout order =====
        main_layout.addLayout(search_layout)   # ✅ ใส่ครั้งเดียวพอ
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        #button_layout.addWidget(self.btn_export)
        main_layout.addWidget(self.table)
        

        central.setLayout(main_layout)

    def _get_form_student(self) -> Student:
        return Student(
            student_id=self.txt_student_id.text().strip(),
            first_name=self.txt_first_name.text().strip(),
            last_name=self.txt_last_name.text().strip(),
            major=self.txt_major.text().strip(),
            faculty=self.txt_faculty.text().strip(),
            nick_name=self.txt_nick_name.text().strip(),
            phone_number=self.txt_phone_number.text().strip(),
            email=self.txt_email.text().strip(),
        )

    # ===== Data render helpers =====
    def _render_table(self, students):
        self.table.setSortingEnabled(False)  # 🔥 สำคัญมาก

        self.table.clearContents()
        self.table.setRowCount(len(students))

        for row_idx, s in enumerate(students):
            self.table.setItem(row_idx, 0, QTableWidgetItem(s.student_id))
            self.table.setItem(row_idx, 1, QTableWidgetItem(s.first_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(s.last_name))
            self.table.setItem(row_idx, 3, QTableWidgetItem(s.major))
            self.table.setItem(row_idx, 4, QTableWidgetItem(s.faculty))
            self.table.setItem(row_idx, 5, QTableWidgetItem(s.nick_name))
            self.table.setItem(row_idx, 6, QTableWidgetItem(s.phone_number))
            self.table.setItem(row_idx, 7, QTableWidgetItem(s.email))

        self.table.setSortingEnabled(True)   # 🔥 เปิดกลับทีหลัง
        
    def load_data(self):
        students = self.service.list_students()
        self._render_table(students)

    # ===== Search handlers =====
    def on_search(self):
        try:
            keyword = self.txt_search.text().strip()
            students = self.service.search_students(keyword)  # ต้องมีใน student_service.py
            self._render_table(students)
        except Exception as e:
            self._error(str(e))

    def on_search_clear(self):
        self.txt_search.clear()
        self.load_data()

    # ===== CRUD handlers =====
    def add_student(self):
        try:
        # ✅ เช็คก่อนเรียก service (UX ดีขึ้น)
            if not self.txt_student_id.text().strip():
                self._error("กรุณากรอกรหัสนักศึกษา")
                self.txt_student_id.setFocus()
                return

            student = self._get_form_student()
            self.service.create_student(student)

            self.load_data()
            self.clear_form()
            self._info("เพิ่มข้อมูลเรียบร้อย")

        except Exception as e:
            self._error(str(e))

    def update_student(self):
        try:
            student = self._get_form_student()
            self.service.update_student(student)
            self.load_data()
            self._info("แก้ไขข้อมูลเรียบร้อย")
        except Exception as e:
            self._error(str(e))

    def delete_student(self):
        student_id = self.txt_student_id.text().strip()
        if not student_id:
            self._error("กรุณาเลือกรายการ หรือกรอกรหัสนักศึกษาที่ต้องการลบ")
            return

        reply = QMessageBox.question(
            self, "ยืนยันการลบ",
            f"ต้องการลบข้อมูลรหัสนักศึกษา {student_id} ใช่หรือไม่?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.service.delete_student(student_id)
                self.load_data()
                self.clear_form()
                self._info("ลบข้อมูลเรียบร้อย")
            except Exception as e:
                self._error(str(e))

    def clear_form(self):
        self.txt_student_id.clear()
        self.txt_first_name.clear()
        self.txt_last_name.clear()
        self.txt_major.clear()
        self.txt_faculty.clear()
        self.txt_nick_name.clear()
        self.txt_phone_number.clear()
        self.txt_email.clear()
        self.txt_student_id.setFocus()

    def on_row_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return

        # ป้องกันกรณี cell เป็น None
        if not self.table.item(row, 0):
            return

        self.txt_student_id.setText(self.table.item(row, 0).text())
        self.txt_first_name.setText(self.table.item(row, 1).text())
        self.txt_last_name.setText(self.table.item(row, 2).text())
        self.txt_major.setText(self.table.item(row, 3).text())
        self.txt_faculty.setText(self.table.item(row, 4).text())
        self.txt_nick_name.setText(self.table.item(row, 5).text())
        self.txt_phone_number.setText(self.table.item(row, 6).text())
        self.txt_email.setText(self.table.item(row, 7).text())
        
    def _info(self, message: str):
        QMessageBox.information(self, "สำเร็จ", message)

    def _error(self, message: str):
        QMessageBox.critical(self, "เกิดข้อผิดพลาด", message)

    def import_csv(self):
        try:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "เลือกไฟล์ CSV",
                "",
                "CSV Files (*.csv)"
            )
            if not path:
                return

            count = 0
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)

                students = []  #สร้าง list เก็บ

                for row in reader:
                    students.append(Student(
                        student_id=row["student_id"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        major=row["major"],
                        faculty=row["faculty"],
                        nick_name=row.get("nick_name", ""),
                        phone_number=row.get("phone_number", ""),
                        email=row.get("email", ""),
                    ))

            #เรียก service ครั้งเดียว
            added, updated = self.service.import_students(students)

            self.load_data()
            self._info(f"เพิ่มใหม่ {added} รายการ\nแก้ไข {updated} รายการ")

        except Exception as e:
            self._error(str(e))

    def export_csv(self):
        try:
            path, _ = QFileDialog.getSaveFileName(
                self,
                "บันทึกไฟล์ CSV",
                "students.csv",
                "CSV Files (*.csv)"
            )
            if not path:
                return

            # ดึงข้อมูลจากฐานข้อมูล
            students = self.service.list_students()

            # utf-8-sig ทำให้ Excel อ่านภาษาไทยไม่เพี้ยน
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["student_id", "first_name", "last_name", "major", "faculty","nick_name","phone_number","email"])
                for s in students:
                    writer.writerow([s.student_id, s.first_name, s.last_name, s.major, s.faculty, s.nick_name, s.phone_number, s.e])

            self._info(f"Export CSV สำเร็จ\n{path}")

        except Exception as e:
            self._error(str(e))
            
    def show_report(self):
        rows = self.service.report_faculty_with_major()

        message = ""
        current_faculty = None

        for row in rows:
            if row["faculty"] != current_faculty:
                current_faculty = row["faculty"]
                message += f"\n{current_faculty}\n"

            message += f"   - {row['major']} : {row['total']} คน\n"

        dialog = QDialog(self)
        dialog.setWindowTitle("รายงานตามคณะและสาขา")
        dialog.resize(500, 400)

        layout = QVBoxLayout()
        text = QTextEdit()
        text.setReadOnly(True)
        text.setText(message)

        layout.addWidget(text)
        dialog.setLayout(layout)

        dialog.exec()  