
import pandas as pd


# --------------------------------
# 1. AUTHENTICATE STUDENT
# --------------------------------

def authenticate_student(student_id):

    students = pd.read_csv("data/students.csv")

    student = students[
        students["student_id"] == student_id
    ]

    if student.empty:
        return False

    return True


# --------------------------------
# 2. CHECK PERMISSION
# --------------------------------

def check_permission(logged_in_student, requested_student):

    if logged_in_student == requested_student:

        return True

    return False


# --------------------------------
# 3. GET STUDENT PRIVATE DATA
# --------------------------------

def get_student_record(logged_in_student, requested_student):

    allowed = check_permission(
        logged_in_student,
        requested_student
    )

    if not allowed:

        return {
            "status": "Denied",
            "message": "Access denied. You cannot access another student's private information."
        }

    students = pd.read_csv("data/students.csv")

    student = students[
        students["student_id"] == logged_in_student
    ]

    if student.empty:

        return {
            "status": "Error",
            "message": "Student record not found."
        }

    return {
        "status": "Allowed",
        "record": student.iloc[0].to_dict()
    }
