
# Student Support Agent

## 1. Project Overview

The Student Support Agent is a chatbot application that helps students get information about fees, scholarships, institute policies and support requests.

It also provides persistent memory, student privacy protection and an administrator approval system.

## 2. Objectives

- Provide quick answers to student questions.
- Check student fee and scholarship status.
- Retrieve information from student policies.
- Remember useful student information across sessions.
- Protect private student records.
- Require administrator approval for sensitive actions.
- Maintain audit logs of important actions.

## 3. Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- SQLite
- TF-IDF
- VS Code

## 4. Project Features

### Student Chatbot
Students can ask questions about fees, scholarships, policies and support requests.

### Persistent Memory
The system stores useful student information in an SQLite database.

### Policy Retrieval
TF-IDF retrieves relevant information from the student policy document.

### Student Privacy
Students can access their own records but cannot access another student's private information.

### Approval System
Course-change requests require administrator approval.

### Audit Logs
The system records pending, approved and rejected actions.

### Evaluation
The project includes seven functional test cases.

## 5. Project Structure

Student_Support_Agent/
- app.py
- agent.py
- memory.py
- security.py
- approval.py
- evaluation.py
- requirements.txt
- data/
  - students.csv
  - student_policy.txt

## 6. How to Run the Project

Step 1: Install required packages.

pip install -r requirements.txt

Step 2: Run the application.

streamlit run app.py

Step 3: Open the application in your browser.

Step 4: Login as a student or administrator.

## 7. Admin Demo Credentials

Admin ID: ADMIN001

Password: Admin@123

These are demonstration credentials only.

## 8. Evaluation Results

Total Test Cases: 7

Passed: 7

Failed: 0

Functional Test Pass Rate: 100%

## 9. Limitations

- Student login currently uses a student ID rather than verified credentials.
- Admin credentials are hardcoded for demonstration.
- Approval execution is simulated.
- The current agent uses rule-based routing and TF-IDF retrieval, not an LLM-based reasoning model.
- Token usage is not measured because no LLM API is currently integrated.

## 10. Conclusion

The Student Support Agent demonstrates student assistance, policy retrieval, persistent memory, privacy protection, approval workflows and audit logging.

All seven current functional evaluation tests passed.
