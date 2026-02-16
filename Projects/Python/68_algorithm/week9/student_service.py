# student_service.py
from models import Student
from student_repository import StudentRepository

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