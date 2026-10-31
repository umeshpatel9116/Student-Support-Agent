
import sqlite3
import os
from datetime import datetime

DB_PATH = "data/approval.db"


# --------------------------------
# 1. CREATE APPROVAL DATABASE
# --------------------------------

def create_approval_database():

    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approval_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT NOT NULL,
            status TEXT NOT NULL,
            result TEXT,
            reviewer_id TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            action TEXT,
            decision TEXT,
            result TEXT,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------
# 2. WRITE AUDIT LOG
# --------------------------------

def write_audit(student_id, action, decision, result):

    create_approval_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO audit_logs
        (student_id, action, decision, result, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student_id,
        action,
        decision,
        result,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()


# --------------------------------
# 3. CREATE APPROVAL REQUEST
# --------------------------------

def request_approval(student_id, action, details):

    create_approval_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO approval_requests
        (student_id, action, details, status, result, reviewer_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        action,
        details,
        "Pending",
        "Not executed",
        None,
        datetime.now().isoformat()
    ))

    request_id = cursor.lastrowid

    connection.commit()
    connection.close()

    write_audit(
        student_id,
        action,
        "Pending approval",
        "Action not executed"
    )

    return request_id


# --------------------------------
# 4. HUMAN REVIEW
# --------------------------------

def review_approval(request_id, decision, reviewer_id):

    if decision not in ["Approved", "Rejected"]:
        return "Invalid decision."

    # Only an authorized demo administrator can review.
    if reviewer_id != "ADMIN001":
        return "Unauthorized reviewer. Request not changed."

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_id, action, status
        FROM approval_requests
        WHERE id = ?
    """, (request_id,))

    request = cursor.fetchone()

    if request is None:
        connection.close()
        return "Approval request not found."

    student_id, action, status = request

    if status != "Pending":
        connection.close()
        return "This request has already been reviewed."

    if decision == "Approved":

        # Demonstration only: record successful execution.
        result = "Approved action executed in demo system."

    else:

        # Rejected actions are never executed.
        result = "Action rejected and not executed."

    cursor.execute("""
        UPDATE approval_requests
        SET status = ?, result = ?, reviewer_id = ?
        WHERE id = ?
    """, (
        decision,
        result,
        reviewer_id,
        request_id
    ))

    connection.commit()
    connection.close()

    write_audit(
        student_id,
        action,
        decision,
        result
    )

    return result


# --------------------------------
# 5. VIEW AUDIT LOGS
# --------------------------------

def get_audit_logs():

    create_approval_database()

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM audit_logs
        ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    connection.close()

    return logs
