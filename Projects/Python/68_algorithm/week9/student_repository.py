# student_repository.py
from typing import List, Optional
from models import Student
from database import Database

class StudentRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, student: Student) -> None:
        with self.db.get_connection() as conn:
            conn.execute("""
                INSERT INTO students (student_id, first_name, last_name, major, faculty, nick_name, phone_number, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (student.student_id, student.first_name, student.last_name, student.major, student.faculty, student.nick_name, student.phone_number, student.email))
            conn.commit()

    def get_all(self) -> List[Student]:
        with self.db.get_connection() as conn:
            rows = conn.execute("""
                SELECT student_id, first_name, last_name, major, faculty, nick_name, phone_number, email
                FROM students
                ORDER BY student_id
            """).fetchall()
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

    def get_by_id(self, student_id: str) -> Optional[Student]:
        with self.db.get_connection() as conn:
            row = conn.execute("""
                SELECT student_id, first_name, last_name, major, faculty, nick_name, phone_number, email
                FROM students
                WHERE student_id = ?
            """, (student_id,)).fetchone()
            if not row:
                return None
            return Student(
                student_id=row["student_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                major=row["major"],
                faculty=row["faculty"],
                nick_name=row["nick_name"],
                phone_number=row["phone_number"],
                email=row["email"]
            )

    def update(self, student: Student) -> int:
        with self.db.get_connection() as conn:
            cur = conn.execute("""
                UPDATE students
                SET first_name = ?, last_name = ?, major = ?, faculty = ?, nick_name= ?, phone_number= ?, email= ?
                WHERE student_id = ?
            """, (student.first_name, student.last_name, student.major, student.faculty, student.nick_name, student.phone_number, student.email, student.student_id))
            conn.commit()
            return cur.rowcount

    def delete(self, student_id: str) -> int:
        with self.db.get_connection() as conn:
            cur = conn.execute("""
                DELETE FROM students
                WHERE student_id = ?
            """, (student_id,))
            conn.commit()
            return cur.rowcount