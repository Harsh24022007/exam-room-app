import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(BASE_DIR, 'exam_room_allocation.sql')
db_path = os.path.join(BASE_DIR, 'exam_room_allocation.db')

with sqlite3.connect(db_path) as conn:
    conn.execute('PRAGMA foreign_keys = ON')
    with open(schema_path, encoding='utf-8') as handle:
        conn.executescript(handle.read())
    conn.executescript('''
    INSERT INTO DEPARTMENT VALUES (1, 'Computer Science');
    INSERT INTO DEPARTMENT VALUES (2, 'Business Administration');
    INSERT INTO SUBJECT VALUES (101, 'Database Systems', 5, 1);
    INSERT INTO SUBJECT VALUES (102, 'Operating Systems', 5, 1);
    INSERT INTO SUBJECT VALUES (201, 'Financial Management', 3, 2);
    INSERT INTO STUDENTS VALUES (1001, 'Aarav', NULL, 'Sharma', 5, 1);
    INSERT INTO STUDENTS VALUES (1002, 'Maya', 'R', 'Patel', 5, 1);
    INSERT INTO STUDENTS VALUES (2001, 'Noah', NULL, 'Thomas', 3, 2);
    INSERT INTO EXAMINATION VALUES (5001, 101, '2026-10-10', '10:00:00', '13:00:00');
    INSERT INTO EXAMINATION VALUES (5002, 102, '2026-10-12', '14:00:00', '17:00:00');
    INSERT INTO ROOMS VALUES (1, 'Main Block', '1', 30, 'AVAILABLE');
    INSERT INTO ROOMS VALUES (2, 'Main Block', '2', 40, 'AVAILABLE');
    INSERT INTO INVIGILATOR VALUES (1, 'Dr. Priya Menon', '+91-9000000001', 'priya@example.edu');
    INSERT INTO INVIGILATOR VALUES (2, 'Prof. Rahul Das', '+91-9000000002', 'rahul@example.edu');
    INSERT INTO EXAM_REGISTRATION VALUES (9001, 1001, 5001, '2026-09-20');
    INSERT INTO EXAM_REGISTRATION VALUES (9002, 1002, 5001, '2026-09-20');
    INSERT INTO EXAM_REGISTRATION VALUES (9003, 2001, 5002, '2026-09-20');
    INSERT INTO ROOM_ALLOCATION VALUES (7001, 9001, 1, 'A01');
    INSERT INTO ROOM_ALLOCATION VALUES (7002, 9002, 1, 'A02');
    INSERT INTO ROOM_ALLOCATION VALUES (7003, 9003, 2, 'B01');
    INSERT INTO INVIGILATOR_DUTY VALUES (8001, 5001, 1, 1, '2026-09-20');
    INSERT INTO INVIGILATOR_DUTY VALUES (8002, 5002, 2, 2, '2026-09-20');
    ''')
print(f'Initialized {db_path}')
