# database.py
import sqlite3
from pathlib import Path

DB_FILE = Path("students.db")

class Database:
    def __init__(self, db_path: Path = DB_FILE):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    major TEXT NOT NULL,
                    faculty TEXT NOT NULL,
                    nick_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    email  TEXT NOT NULL
                )
            """)
            conn.commit()