import streamlit as st
import joblib
from database import cursor
import pandas as pd
import streamlit as st

# =========================
# LOGIN CHECK
# =========================
if "logged_in" not in st.session_state:

    st.warning("Please Login First")
    st.stop()

# =========================
# WELCOME MESSAGE
# =========================
st.success(f"Welcome {st.session_state['username']}")

# =========================
# LOAD MODEL
# =========================
model = joblib.load("student_model.pkl")
columns = joblib.load("model_columns.pkl")

# =========================
# TITLE
# =========================
st.title("🎓 Student Score Predictor")

# =========================
# INPUT FIELDS
# =========================
hours = st.number_input(
    "Hours Studied",
    min_value=0.0,
    max_value=24.0,
    value=None,
    placeholder="Enter study hours"
)

attendance = st.number_input(
    "Attendance",
    min_value=0.0,
    max_value=100.0,
    value=None,
    placeholder="Enter attendance percentage"
)

previous = st.number_input(
    "Previous Score",
    min_value=0.0,
    max_value=100.0,
    value=None,
    placeholder="Enter previous score"
)

sleep = st.number_input(
    "Sleep Hours",
    min_value=0.0,
    max_value=12.0,
    value=None,
    placeholder="Enter sleep hours"
)

motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
school = st.selectbox("School Type", ["Public", "Private"])
internet = st.selectbox("Internet Access", ["Yes", "No"])
income = st.selectbox("Family Income", ["Low", "Medium", "High"])
parent = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
education = st.selectbox("Parent Education", ["School", "College"])
peer = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"])
resources = st.selectbox("Learning Resources", ["Low", "Medium", "High"])
activities = st.selectbox("Extracurricular Activities", ["Yes", "No"])

# =========================
# PREDICTION BUTTON
# =========================
if st.button("Predict Score"):
    # Check empty fields
    if (
        hours is None or
        attendance is None or
        previous is None or
        sleep is None
    ):
        st.error("Please fill all numeric fields")

        st.stop()

    # Create input dictionary
    data = {
        "Hours_Studied": hours,
        "Attendance": attendance,
        "Previous_Scores": previous,
        "Sleep_Hours": sleep,

        "Motivation_Level": motivation,
        "Teacher_Quality": teacher,
        "School_Type": school,
        "Internet_Access": internet,
        "Family_Income": income,
        "Parental_Involvement": parent,
        "Parental_Education_Level": education,
        "Peer_Influence": peer,
        "Learning_Resources": resources,
        "Extracurricular_Activities": activities
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([data])

    # Apply encoding
    input_df = pd.get_dummies(input_df)

    # Match training columns
    input_df = input_df.reindex(columns=columns, fill_value=0)

    # =========================
    # PREDICT
    # =========================
    prediction = model.predict(input_df)

    # =========================
    # FIX UNREALISTIC VALUES
    # =========================
    final_score = max(40, min(100, prediction[0]))

    # Convert to integer
    final_score = int(round(final_score))

    # =========================
    # OUTPUT
    # =========================
    st.success(f"🎯 Predicted Exam Score: {final_score}")

# =========================
# SHOW REGISTERED USERS
# =========================
if st.checkbox("Show Registered Users"):

    cursor.execute(
        "SELECT id, username, email FROM users"
    )

    users = cursor.fetchall()

    st.table(users)

# =========================
# LOGOUT BUTTON
# =========================
st.markdown("---")

if st.button("Logout"):

    st.session_state.clear()

    st.switch_page("pages/1_Login.py")
    
