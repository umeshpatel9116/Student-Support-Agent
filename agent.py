
import pandas as pd
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from memory import remember_fact, get_memories
from approval import request_approval
from security import get_student_record


# --------------------------------
# 1. LOAD STUDENT DATABASE
# --------------------------------

def load_students():

    return pd.read_csv("data/students.csv")


# --------------------------------
# 2. TOOL 1: CHECK FEE STATUS
# --------------------------------

def check_fee_status(student_id):

    students = load_students()

    student = students[
        students["student_id"] == student_id
    ]

    if student.empty:
        return "Student record not found."

    student = student.iloc[0]

    return {
        "fee_status": student["fee_status"],
        "total_fees": student["total_fees"],
        "paid_fees": student["paid_fees"],
        "remaining_fees": (
            student["total_fees"] - student["paid_fees"]
        )
    }


# --------------------------------
# 3. TOOL 2: CHECK SCHOLARSHIP
# --------------------------------

def check_scholarship_status(student_id):

    students = load_students()

    student = students[
        students["student_id"] == student_id
    ]

    if student.empty:
        return "Student record not found."

    student = student.iloc[0]

    return student["scholarship_status"]


# --------------------------------
# 4. TOOL 3: CREATE SUPPORT REQUEST
# --------------------------------

def create_support_request(student_id, message):

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(
        "data/support_requests.csv"
    )

    request = pd.DataFrame([{
        "student_id": student_id,
        "message": message,
        "status": "Open"
    }])

    request.to_csv(
        "data/support_requests.csv",
        mode="a",
        header=not file_exists,
        index=False
    )

    return "Your support request has been created successfully."


# --------------------------------
# 5. POLICY DOCUMENT RETRIEVAL
# --------------------------------

def search_policy(question):

    with open(
        "data/student_policy.txt",
        "r",
        encoding="utf-8"
    ) as file:

        policy_text = file.read()

    chunks = [
        chunk.strip()
        for chunk in re.split(r"\n\s*\n", policy_text)
        if chunk.strip()
    ]

    if not chunks:
        return "No policy information is available."

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        chunks + [question]
    )

    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    ).flatten()

    best_index = similarity.argmax()

    if similarity[best_index] < 0.10:
        return "The available policy does not contain enough information."

    return chunks[best_index]


# --------------------------------
# 6. AGENT LOOP
# --------------------------------

# --------------------------------
# 6. AGENT LOOP
# --------------------------------

def run_agent(question, student_id):

    question_lower = question.lower()

    trace = []

    # 1. REMEMBER USEFUL INFORMATION
    if question_lower.startswith("remember"):

        fact = question[8:].strip()

        if fact:
            answer = remember_fact(student_id, fact)
            trace.append("Tool used: remember_fact")
        else:
            answer = "Please tell me what you want me to remember."

    # 2. RETRIEVE PREVIOUS MEMORY
    elif any(phrase in question_lower for phrase in [
        "what do you remember",
        "my memories",
        "what have you remembered"
    ]):

        memories = get_memories(student_id)
        trace.append("Tool used: get_memories")

        if memories:
            answer = "Here is what I remember about you:\n"
            for memory in memories:
                answer += "\n- " + memory
        else:
            answer = "I don't have any saved memories yet."

        # 3. STUDENT RECORD ACCESS WITH PRIVACY CHECK
    elif any(word in question_lower for word in [
        "student record",
        "my record",
        "student details",
        "student profile"
    ]):

        student_ids = re.findall(
            r"\bSTU\d{3}\b",
            question.upper()
        )

        requested_student = (
            student_ids[0] if student_ids else student_id
        )

        result = get_student_record(
            student_id,
            requested_student
        )

        trace.append("Tool used: get_student_record")

        if result["status"] == "Allowed":

            record = result["record"]

            answer = (
                f"Student Name: {record['name']}\n"
                f"Programme: {record['programme']}\n"
                f"Fee Status: {record['fee_status']}\n"
                f"Scholarship Status: {record['scholarship_status']}"
            )

        else:

            answer = result["message"]

    # 3. COURSE CHANGE - REQUIRE APPROVAL
    elif any(phrase in question_lower for phrase in [
        "change my course",
        "course change",
        "change programme",
        "change my programme"
    ]):

        request_id = request_approval(
            student_id,
            "Course Change",
            question
        )

        answer = (
            f"Your course change request has been submitted.\n"
            f"Request ID: {request_id}\n"
            f"Status: Pending approval.\n"
            f"The course will not be changed until an authorized "
            f"administrator approves the request."
        )

        trace.append("Tool used: request_approval")
        trace.append("Approval required before action")

    # 4. SEARCH POLICY
    elif any(word in question_lower for word in [
        "policy", "rules", "portal", "deadline",
        "next working day"
    ]):

        result = search_policy(question)
        trace.append("Tool used: search_policy")
        answer = result

    # 5. CREATE SUPPORT REQUEST
    elif any(phrase in question_lower for phrase in [
        "support request",
        "raise a request",
        "create a ticket"
    ]):

        answer = create_support_request(
            student_id,
            question
        )

        trace.append("Tool used: create_support_request")

    # 6. CHECK FEE STATUS
    elif "fee" in question_lower or "payment" in question_lower:

        result = check_fee_status(student_id)
        trace.append("Tool used: check_fee_status")

        if isinstance(result, dict):
            answer = (
                f"Your fee status is {result['fee_status']}.\n"
                f"Total fees: ₹{result['total_fees']}.\n"
                f"Paid fees: ₹{result['paid_fees']}.\n"
                f"Remaining fees: ₹{result['remaining_fees']}."
            )
        else:
            answer = result

    # 7. CHECK SCHOLARSHIP
    elif "scholarship" in question_lower:

        result = check_scholarship_status(student_id)
        trace.append("Tool used: check_scholarship_status")

        answer = f"Your scholarship status is {result}."

    # 8. GENERAL RESPONSE
    else:

        trace.append("No tool required")

        answer = (
            "I can help with fees, scholarships, policies, "
            "support requests, course changes and remembering "
            "useful information."
        )

    return answer, trace
