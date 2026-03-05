# student_service.py
from models import Student
from student_repository import StudentRepository
import re

class StudentService:
    def __init__(self, repo: StudentRepository):
        self.repo = repo

    def validate(self, student: Student) -> None:
        if not student.student_id.strip():
            raise ValueError("กรุณากรอกรหัสนักศึกษา")
        if not student.first_name.strip():
            raise ValueError("กรุณากรอกชื่อ")
        if not student.last_name.strip():
            raise ValueError("กรุณากรอกนามสกุล")
        if not student.major.strip():
            raise ValueError("กรุณากรอกสาขาวิชา")
        if not student.faculty.strip():
            raise ValueError("กรุณากรอกคณะ")
        if not student.nick_name.strip():
            raise ValueError("กรุณากรอกชื่อเล่น")
        if not student.phone_number.strip():
            raise ValueError("กรุณากรอกหมายเลขโทรศัพท์")
        if not student.email.strip():
            raise ValueError("กรุณากรอกอีเมล")
        if not student.phone_number.isdigit():
            raise ValueError("เบอร์โทรต้องเป็นตัวเลขเท่านั้น")
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", student.email):
            raise ValueError("รูปแบบอีเมลไม่ถูกต้อง")

    def create_student(self, student: Student) -> None:
        self.validate(student)
        if self.repo.get_by_id(student.student_id):
            raise ValueError("รหัสนักศึกษานี้มีอยู่แล้ว")
        self.repo.create(student)

    def list_students(self):
        return self.repo.get_all()

    def update_student(self, student: Student) -> None:
        self.validate(student)
        affected = self.repo.update(student)
        if affected == 0:
            raise ValueError("ไม่พบรหัสนักศึกษาที่ต้องการแก้ไข")

    def delete_student(self, student_id: str) -> None:
        if not student_id.strip():
            raise ValueError("กรุณากรอกรหัสนักศึกษาที่ต้องการลบ")
        affected = self.repo.delete(student_id)
        if affected == 0:
            raise ValueError("ไม่พบรหัสนักศึกษาที่ต้องการลบ")
        
    def import_students(self, students: list[Student]):
        added = 0
        updated = 0

        for student in students:
            self.validate(student)
            if self.repo.get_by_id(student.student_id):
                self.repo.update(student)
                updated += 1
            else:
                self.repo.create(student)
                added += 1

        return added, updated
    
    def report_by_faculty(self):
        return self.repo.count_by_faculty()
    
    def search_students(self, keyword: str):
        if not keyword:
            return self.repo.get_all()

        keyword = f"%{keyword}%"
        with self.repo.db.get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM students
                WHERE student_id LIKE ?
                OR first_name LIKE ?
                OR last_name LIKE ?
                OR major LIKE ?
                OR faculty LIKE ?
                OR nick_name LIKE ?
                OR phone_number LIKE ?
                OR email LIKE ?
            """, (keyword,)*8).fetchall()

            return [
                Student(
                    student_id=row["student_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    major=row["major"],
                    faculty=row["faculty"],
                    nick_name=row["nick_name"],
                    phone_number=row["phone_number"],
                    email=row["email"]
                ) for row in rows
            ]
    def report_faculty_with_major(self):
        return self.repo.count_faculty_with_major()