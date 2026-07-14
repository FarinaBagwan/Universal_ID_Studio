import sqlite3
import os

DB_FOLDER = "database"
DB_NAME = os.path.join(DB_FOLDER, "idcard.db")

def create_database():

    os.makedirs(DB_FOLDER, exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT,
        branch TEXT,
        year TEXT,
        photo TEXT,
        id_card TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS templates(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT,
    template_image TEXT,
    mapping_file TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1
)
""")
    conn.commit()
    conn.close()


def add_student(name, roll, branch, year, photo, id_card):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name, roll, branch, year, photo, id_card)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, roll, branch, year, photo, id_card))

    conn.commit()
    conn.close()


def get_students():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return students


def save_template(template_name, template_image, mapping_file):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO templates
    (template_name, template_image, mapping_file)
    VALUES (?, ?, ?)
    """, (template_name, template_image, mapping_file))

    conn.commit()
    conn.close()


def get_templates():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM templates")

    data = cursor.fetchall()

    conn.close()

    return data

def get_active_template():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM templates

    WHERE is_active=1

    ORDER BY id DESC

    LIMIT 1

    """)

    template = cursor.fetchone()

    conn.close()

    return template

def delete_template(template_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM templates WHERE id=?",

        (template_id,)

    )

    conn.commit()

    conn.close()