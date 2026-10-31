
# STUDENT SUPPORT AGENT
## Final Project Report

### 1. Introduction

The Student Support Agent is a chatbot application developed using Python and Streamlit. It helps students get information about fees, scholarships, institute policies and support requests.

The system also provides persistent memory, student privacy protection, administrator approval and audit logging.

### 2. Problem Statement

Students often need to contact different departments to get information about fees, scholarships and institute policies. This process can take time.

The project aims to develop a chatbot that provides student support through a single application while protecting private information.

### 3. Objectives

- Provide quick answers to student questions.
- Check fee and scholarship information.
- Retrieve relevant institute policy information.
- Remember useful information across sessions.
- Prevent unauthorized access to student records.
- Require administrator approval for sensitive requests.
- Maintain audit logs.
- Evaluate the system using test cases.

### 4. Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- SQLite
- TF-IDF
- VS Code

### 5. System Modules

1. Student Chatbot
2. Fee Status Tool
3. Scholarship Status Tool
4. Support Request Tool
5. Policy Retrieval System
6. Persistent Memory
7. Student Privacy and Security
8. Administrator Approval System
9. Audit Logging
10. Evaluation System

### 6. Working Methodology

Step 1: Student logs into the application.

Step 2: Student enters a question in the chatbot.

Step 3: The agent identifies the question and selects the relevant function.

Step 4: The required information is retrieved from the student database, memory database or policy document.

Step 5: The chatbot displays the answer.

Step 6: Sensitive requests are sent for administrator approval.

Step 7: Important actions are recorded in audit logs.

### 7. Security Features

- Students can access their own records.
- Access to another student's private information is denied.
- Passwords and OTPs are blocked by the memory filter.
- Course-change requests require administrator approval.
- Unauthorized approval attempts are rejected.
- Important actions are recorded in audit logs.

### 8. Evaluation Results

Total Test Cases: 10

Passed: 10

Failed: 0

Functional Test Pass Rate: 100%

Test cases include fee status, scholarship status, policy retrieval, memory, privacy, approval security, password protection, OTP protection and normal memory storage.

### 9. Limitations

- The current agent uses rule-based routing and TF-IDF retrieval, not an LLM-based reasoning model.
- Student login uses a student ID rather than verified credentials.
- Admin credentials are hardcoded for demonstration.
- Approval execution is simulated.
- Token usage is not measured.

### 10. Conclusion

The Student Support Agent demonstrates how a chatbot can help students access important information through a single application.

The project includes policy retrieval, persistent memory, privacy protection, administrator approval and audit logging.

All 10 functional evaluation tests passed successfully.
