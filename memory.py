
import sqlite3
import re
import os

# Database location
DB_PATH = "data/student_memory.db"


# --------------------------------
# 1. CREATE MEMORY DATABASE
# --------------------------------

def create_memory_database():

    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            memory TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------
# 2. CHECK SENSITIVE INFORMATION
# --------------------------------

def contains_sensitive_information(text):

    sensitive_words = [
        "password",
        "otp",
        "one time password",
        "credit card",
        "cvv",
        "bank account number"
    ]

    text_lower = text.lower()

    for word in sensitive_words:

        if word in text_lower:
            return True

    return False


# --------------------------------
# 3. SAVE STUDENT MEMORY
# --------------------------------

def remember_fact(student_id, fact):

    create_memory_database()

    if contains_sensitive_information(fact):

        return (
            "I cannot store sensitive information "
            "such as passwords or OTPs."
        )

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO student_memories
        (student_id, memory)
        VALUES (?, ?)
    """, (student_id, fact))

    connection.commit()
    connection.close()

    return "I have successfully remembered your information."


# --------------------------------
# 4. RETRIEVE STUDENT MEMORY
# --------------------------------

def get_memories(student_id):

    create_memory_database()

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT memory
        FROM student_memories
        WHERE student_id = ?
        ORDER BY id DESC
    """, (student_id,))

    memories = cursor.fetchall()

    connection.close()

    return [memory[0] for memory in memories]
