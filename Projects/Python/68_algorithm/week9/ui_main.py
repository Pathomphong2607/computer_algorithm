# ui_main.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from models import Student
from student_service import StudentService

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

        # Inputs
        self.txt_student_id = QLineEdit()
        self.txt_first_name = QLineEdit()
        self.txt_last_name = QLineEdit()
        self.txt_major = QLineEdit()
        self.txt_faculty = QLineEdit()
        self.txt_nick_name = QLineEdit()
        self.txt_phone_number = QLineEdit()
        self.txt_email = QLineEdit()

        self.txt_student_id.setPlaceholderText("เช่น 66010001")
        self.txt_first_name.setPlaceholderText("ชื่อ")
        self.txt_last_name.setPlaceholderText("นามสกุล")
        self.txt_major.setPlaceholderText("สาขาวิชา")
        self.txt_faculty.setPlaceholderText("คณะ")
        self.txt_nick_name.setPlaceholderText("ชื่อเล่น")
        self.txt_phone_number.setPlaceholderText("หมายเลขโทรศัพท์")
        self.txt_email.setPlaceholderText("กรุณาใส่อีเมล")

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
        form_layout.addWidget(QLabel("หมายเลขโทรศัพท์"))
        form_layout.addWidget(self.txt_phone_number)
        form_layout.addWidget(QLabel("อีเมล"))
        form_layout.addWidget(self.txt_email)

        # Buttons
        self.btn_add = QPushButton("เพิ่ม")
        self.btn_update = QPushButton("แก้ไข")
        self.btn_delete = QPushButton("ลบ")
        self.btn_clear = QPushButton("ล้างฟอร์ม")
        self.btn_refresh = QPushButton("รีเฟรช")

        self.btn_add.clicked.connect(self.add_student)
        self.btn_update.clicked.connect(self.update_student)
        self.btn_delete.clicked.connect(self.delete_student)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_refresh.clicked.connect(self.load_data)

        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_update)
        button_layout.addWidget(self.btn_delete)
        button_layout.addWidget(self.btn_clear)
        button_layout.addWidget(self.btn_refresh)
        button_layout.addStretch()

        # Table
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(["รหัสนักศึกษา", "ชื่อ", "นามสกุล", "สาขาวิชา", "คณะ","ชื่อเล่น","เบอร์โทร","อีเมล"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.on_row_selected)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
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
            email=self.txt_email.text().strip()
        )

    def load_data(self):
        students = self.service.list_students()
        self.table.setRowCount(0)

        for row_idx, s in enumerate(students):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(s.student_id))
            self.table.setItem(row_idx, 1, QTableWidgetItem(s.first_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(s.last_name))
            self.table.setItem(row_idx, 3, QTableWidgetItem(s.major))
            self.table.setItem(row_idx, 4, QTableWidgetItem(s.faculty))
            self.table.setItem(row_idx, 5, QTableWidgetItem(s.nick_name))
            self.table.setItem(row_idx, 6, QTableWidgetItem(s.phone_number))
            self.table.setItem(row_idx, 7, QTableWidgetItem(s.email))



    def add_student(self):
        try:
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
        self.txt_student_id.setFocus()
        self.txt_nick_name.clear()
        self.txt_phone_number.clear()
        self.txt_email.clear()

    def on_row_selected(self):
        row = self.table.currentRow()
        if row < 0:
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