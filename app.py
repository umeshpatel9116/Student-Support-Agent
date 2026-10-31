
import streamlit as st
import pandas as pd
from agent import run_agent
from approval import review_approval, get_audit_logs

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Student Support Agent",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Support Agent")

# --------------------------------
# DEMO ADMIN CREDENTIALS
# --------------------------------

ADMIN_ID = "ADMIN001"
ADMIN_PASSWORD = "Admin@123"

# --------------------------------
# SIDEBAR LOGIN
# --------------------------------

st.sidebar.title("Login")

login_type = st.sidebar.radio(
    "Select Login Type",
    ["Student", "Admin"]
)

# --------------------------------
# STUDENT LOGIN
# --------------------------------

if login_type == "Student":

    st.sidebar.subheader("Student Login")

    student_id = st.sidebar.text_input(
        "Enter Student ID"
    )

    if st.sidebar.button("Student Login"):

        students = pd.read_csv("data/students.csv")

        student = students[
            students["student_id"] == student_id
        ]

        if not student.empty:
            st.session_state["student_id"] = student_id
            st.session_state["login_type"] = "Student"
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Student ID not found.")

# --------------------------------
# ADMIN LOGIN
# --------------------------------

elif login_type == "Admin":

    st.sidebar.subheader("Admin Login")

    admin_id = st.sidebar.text_input("Admin ID")

    admin_password = st.sidebar.text_input(
        "Password",
        type="password"
    )

    if st.sidebar.button("Admin Login"):

        if admin_id == ADMIN_ID and admin_password == ADMIN_PASSWORD:

            st.session_state["login_type"] = "Admin"
            st.session_state["admin_id"] = admin_id

            st.sidebar.success("Admin login successful!")

        else:
            st.sidebar.error("Invalid admin credentials.")

# --------------------------------
# STUDENT DASHBOARD
# --------------------------------

if st.session_state.get("login_type") == "Student":

    st.success(
        f"Logged in as {st.session_state['student_id']}"
    )

    st.subheader("Ask Your Question")

    question = st.chat_input(
        "Type your question here..."
    )

    if question:

        st.chat_message("user").write(question)

        try:

            answer, trace = run_agent(
                question,
                st.session_state["student_id"]
            )

            st.chat_message("assistant").write(answer)

            with st.expander("View Agent Trace"):

                for item in trace:
                    st.write(item)

        except Exception as error:

            st.error(f"Error: {error}")

# --------------------------------
# ADMIN DASHBOARD
# --------------------------------

elif st.session_state.get("login_type") == "Admin":

    st.success("Welcome, Administrator!")

    st.title("Admin Dashboard")

    st.subheader("Pending Approval Requests")

    # Load approval database
    connection = __import__("sqlite3").connect(
        "data/approval.db"
    )

    requests = pd.read_sql_query(
        "SELECT * FROM approval_requests WHERE status = 'Pending'",
        connection
    )

    connection.close()

    if requests.empty:

        st.info("No pending approval requests.")

    else:

        for _, request in requests.iterrows():

            with st.expander(
                f"Request ID: {request['id']} - {request['action']}"
            ):

                st.write("Student ID:", request["student_id"])
                st.write("Action:", request["action"])
                st.write("Details:", request["details"])
                st.write("Status:", request["status"])

                if st.button(
                    "Approve",
                    key=f"approve_{request['id']}"
                ):

                    result = review_approval(
                        int(request["id"]),
                        "Approved",
                        ADMIN_ID
                    )

                    st.success(result)
                    st.rerun()

                if st.button(
                    "Reject",
                    key=f"reject_{request['id']}"
                ):

                    result = review_approval(
                        int(request["id"]),
                        "Rejected",
                        ADMIN_ID
                    )

                    st.warning(result)
                    st.rerun()

    # --------------------------------
    # AUDIT LOGS
    # --------------------------------

    st.divider()

    st.subheader("Audit Logs")

    logs = get_audit_logs()

    if logs:

        audit_df = pd.DataFrame(
            logs,
            columns=[
                "Log ID",
                "Student ID",
                "Action",
                "Decision",
                "Result",
                "Timestamp"
            ]
        )

        st.dataframe(
            audit_df,
            use_container_width=True
        )

    else:

        st.info("No audit records available.")

else:

    st.info(
        "Please select Student or Admin and log in."
    )
