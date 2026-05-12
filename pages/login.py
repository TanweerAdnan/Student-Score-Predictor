import streamlit as st
from auth import login_user

st.title("Login Page")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    user = login_user(email, password)

    if user:

        st.session_state["logged_in"] = True
        st.session_state["username"] = user[1]

        st.success("Login Successful")

        st.switch_page("app.py")

    else:
        st.error("Invalid Email or Password")

st.markdown("Don't have an account?")

if st.button("Go to Register"):

    st.switch_page("pages/2_Register.py")
