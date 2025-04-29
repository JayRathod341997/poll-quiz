import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import csv
import uuid

CSV_FILE = "poll_results.csv"
SUBMISSION_FILE = "submitted_users.csv"

# Create result CSV if it doesn't exist
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['UserID', 'Timestamp', 'Question', 'Answer'])

# Create submission log file if not exists
if not os.path.isfile(SUBMISSION_FILE):
    with open(SUBMISSION_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['UserID'])

# Assign unique ID for the session
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())

user_id = st.session_state["user_id"]

# Check submission status
def has_user_submitted(user_id):
    df = pd.read_csv(SUBMISSION_FILE)
    return user_id in df['UserID'].values

def mark_user_submitted(user_id):
    with open(SUBMISSION_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user_id])

def save_response(user_id, question, answer):
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, datetime.now(), question, answer])

# Main App
st.title("🗳️ Developer Poll")

if has_user_submitted(user_id):
    st.success("✅ You have already submitted your answers. Thank you!")
    st.stop()

with st.form("poll_form"):
    st.subheader("Please answer all questions:")

    q1 = st.radio("1. What is your favorite programming language?",
                  ["Python", "JavaScript", "Java", "C++"])
    q2 = st.radio("2. How often do you code?",
                  ["Daily", "Weekly", "Monthly", "Rarely"])
    q3 = st.radio("3. Which IDE do you prefer?",
                  ["VSCode", "PyCharm", "Jupyter", "Sublime", "Other"])
    q4 = st.radio("4. What area are you most interested in?",
                  ["Web Dev", "Data Science", "AI/ML", "Cybersecurity", "Mobile Dev"])
    q5 = st.radio("5. How do you prefer to learn?",
                  ["YouTube", "Blogs", "Courses", "Books", "Docs"])
    q6 = st.radio("6. How many years of coding experience do you have?",
                  ["0-1", "2-3", "4-6", "7+"])
    q7 = st.radio("7. What is your preferred backend language?",
                  ["Node.js", "Python", "Java", "PHP", "Go"])

    submitted = st.form_submit_button("Submit All Answers")

    if submitted:
        save_response(user_id, "1. What is your favorite programming language?", q1)
        save_response(user_id, "2. How often do you code?", q2)
        save_response(user_id, "3. Which IDE do you prefer?", q3)
        save_response(user_id, "4. What area are you most interested in?", q4)
        save_response(user_id, "5. How do you prefer to learn?", q5)
        save_response(user_id, "6. How many years of coding experience do you have?", q6)
        save_response(user_id, "7. What is your preferred backend language?", q7)
        mark_user_submitted(user_id)
        st.success("✅ Your responses have been submitted successfully!")
        st.stop()

# Load and process data
def load_data():
    df = pd.read_csv(CSV_FILE)

    def get_counts(qtext, options):
        data = df[df['Question'] == qtext]
        return data['Answer'].value_counts().reindex(options, fill_value=0)

    return {
        "Favorite Programming Languages": get_counts("1. What is your favorite programming language?", ["Python", "JavaScript", "Java", "C++"]),
        "Coding Frequency": get_counts("2. How often do you code?", ["Daily", "Weekly", "Monthly", "Rarely"]),
        "Preferred IDE": get_counts("3. Which IDE do you prefer?", ["VSCode", "PyCharm", "Jupyter", "Sublime", "Other"]),
        "Area of Interest": get_counts("4. What area are you most interested in?", ["Web Dev", "Data Science", "AI/ML", "Cybersecurity", "Mobile Dev"]),
        "Learning Style": get_counts("5. How do you prefer to learn?", ["YouTube", "Blogs", "Courses", "Books", "Docs"]),
        "Coding Experience (Years)": get_counts("6. How many years of coding experience do you have?", ["0-1", "2-3", "4-6", "7+"]),
        "Backend Language Preference": get_counts("7. What is your preferred backend language?", ["Node.js", "Python", "Java", "PHP", "Go"])
    }

# Show results
st.markdown("---")
st.subheader("📊 Poll Results")

results = load_data()
questions = list(results.keys())

for i in range(0, len(questions), 2):
    col1, col2 = st.columns(2)

    # First chart
    with col1:
        title = questions[i]
        data = results[title]
        st.write(f"**{title}**")
        fig, ax = plt.subplots()
        ax.bar(data.index, data.values, color="skyblue")
        plt.xticks(rotation=30)
        st.pyplot(fig)

    # Second chart (if available)
    if i+1 < len(questions):
        title = questions[i+1]
        data = results[title]
        with col2:
            st.write(f"**{title}**")
            fig, ax = plt.subplots()
            if title == "Coding Frequency":
                ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90)
            else:
                ax.bar(data.index, data.values, color="lightgreen")
                plt.xticks(rotation=30)
            st.pyplot(fig)

# Optional: View raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(pd.read_csv(CSV_FILE))
