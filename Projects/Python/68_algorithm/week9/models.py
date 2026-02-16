# models.py
from dataclasses import dataclass

@dataclass
class Student:
    student_id: str
    first_name: str
    last_name: str
    major: str
    faculty: str
    nick_name: str
    phone_number: str
    email: str