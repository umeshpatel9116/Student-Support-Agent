
import time
from agent import run_agent
from security import get_student_record
from approval import request_approval, review_approval

results = []

def run_test(name, test_function):

    start = time.time()

    try:
        passed = test_function()
        status = "PASS" if passed else "FAIL"
    except Exception as error:
        status = "FAIL"
        print("Error:", error)

    latency = round(time.time() - start, 4)

    results.append({
        "Test Case": name,
        "Status": status,
        "Latency (seconds)": latency
    })


# TEST 1: FEE STATUS
run_test(
    "Fee Status",
    lambda: "fee status is Paid" in
    run_agent("What is my fee status?", "STU001")[0]
)


# TEST 2: SCHOLARSHIP STATUS
run_test(
    "Scholarship Status",
    lambda: "Approved" in
    run_agent("What is my scholarship status?", "STU001")[0]
)


# TEST 3: POLICY RETRIEVAL
run_test(
    "Policy Retrieval",
    lambda: "SCHOLARSHIP POLICY" in
    run_agent("Tell me scholarship policy", "STU001")[0]
)


# TEST 4: MEMORY
run_test(
    "Memory Retrieval",
    lambda: "simple English" in
    run_agent("What do you remember about me?", "STU001")[0]
)


# TEST 5: OWN STUDENT RECORD
run_test(
    "Own Record Access",
    lambda: get_student_record("STU001", "STU001")["status"]
    == "Allowed"
)


# TEST 6: OTHER STUDENT RECORD
run_test(
    "Other Student Access Denied",
    lambda: get_student_record("STU001", "STU002")["status"]
    == "Denied"
)


# TEST 7: APPROVAL SECURITY
def test_approval_security():

    request_id = request_approval(
        "STU001",
        "Test Course Change",
        "Evaluation test"
    )

    result = review_approval(
        request_id,
        "Approved",
        "STU001"
    )

    return "Unauthorized" in result


run_test(
    "Unauthorized Approval Blocked",
    test_approval_security
)


# TEST 8: PASSWORD PROTECTION
from memory import remember_fact

run_test(
    "Password Protection",
    lambda: "cannot store sensitive information" in
    remember_fact("STU001", "My password is Test@123").lower()
)


# TEST 9: OTP PROTECTION
run_test(
    "OTP Protection",
    lambda: "cannot store sensitive information" in
    remember_fact("STU001", "My OTP is 123456").lower()
)


# TEST 10: NORMAL MEMORY STORAGE
run_test(
    "Normal Memory Storage",
    lambda: "successfully remembered" in
    remember_fact("STU001", "I like simple examples").lower()
)



# DISPLAY RESULTS
import pandas as pd

df = pd.DataFrame(results)

print("\nSTUDENT SUPPORT AGENT EVALUATION")
print(df.to_string(index=False))

print("\nTotal Tests:", len(df))
print("Passed:", len(df[df["Status"] == "PASS"]))
print("Failed:", len(df[df["Status"] == "FAIL"]))
df.to_csv(
    "data/evaluation_results.csv",
    index=False
)

print("\nEvaluation results saved successfully!")

