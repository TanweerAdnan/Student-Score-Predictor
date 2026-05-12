import streamlit as st
from database import cursor

# =========================
# ADMIN LOGIN
# =========================
st.title("Admin Panel")

admin_user = st.text_input("Admin Username")

admin_pass = st.text_input(
    "Admin Password",
    type="password"
)

# =========================
# LOGIN BUTTON
# =========================
if st.button("Login as Admin"):

    if (
        admin_user == "admin"
        and
        admin_pass == "admin123"
    ):

        st.session_state["admin"] = True

        st.success("Admin Login Successful")

    else:

        st.error("Invalid Admin Credentials")

# =========================
# ADMIN DASHBOARD
# =========================
if st.session_state.get("admin"):

    st.header("Registered Users")

    cursor.execute(
        "SELECT id, username, email FROM users"
    )

    users = cursor.fetchall()

    st.table(users)

    # Logout button
    if st.button("Logout Admin"):

        st.session_state["admin"] = False

        st.rerun()