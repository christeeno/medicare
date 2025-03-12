import sqlite3
from typing import Optional
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class Patient:
    id: str
    name: str
    age: int
    gender: str
    contact_information: str
    blood_group: str
    height: int
    weight: int

class DatabaseDriver:
    def __init__(self, db_path: str = "patient_db.sqlite"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create patient info
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    contact_information TEXT NOT NULL,
                    blood_group TEXT NOT NULL,
                    height INTEGER NOT NULL,
                    weight INTEGER NOT NULL
                )
            """)

            conn.commit()

    def create_patient(self, id: int, name: str, age: int, gender: str, contact_information: str, blood_group: str, height: int, weight: int) -> Patient:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO patients (id, name, age, gender, contact_information, blood_group, height, weight) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (id, name, age, gender, contact_information, blood_group, height, weight)
            )
            conn.commit()
            return Patient(id=id, name=name, age=age, gender=gender, contact_information=contact_information, blood_group=blood_group, height=height, weight=weight)

    def get_patient_by_id(self, id: int) -> Optional[Patient]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE id = ?", (id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            return Patient(
                id=row[0],
                name=row[1],
                age=row[2],
                gender=row[3],
                contact_information=row[4],
                blood_group=row[5],
                height=row[6],
                weight=row[7]
            )
