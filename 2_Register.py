import streamlit as st
from auth import register_user

st.title("Register Page")

username = st.text_input("Username")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Register"):

    success = register_user(
        username,
        email,
        password
    )

    if success:

        st.success("Registration Successful")

        st.switch_page("pages/1_Login.py")

    else:
        st.error("Email already exists")

st.markdown("Already have an account?")

if st.button("Go to Login"):

    st.switch_page("pages/1_Login.py")