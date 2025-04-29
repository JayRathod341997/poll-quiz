import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import csv

CSV_FILE = "poll_results.csv"

# Initialize CSV
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Question', 'Answer'])

# Save function
def save_response(question, answer):
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), question, answer])

# Load for visualization
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_FILE)

    def get_counts(qtext, options):
        data = df[df['Question'] == qtext]
        return data['Answer'].value_counts().reindex(options, fill_value=0)

    return {
        "1. Favorite Programming Language": get_counts("1. What is your favorite programming language?", ["Python", "JavaScript", "Java", "C++"]),
        "2. Coding Frequency": get_counts("2. How often do you code?", ["Daily", "Weekly", "Monthly", "Rarely"]),
        "3. Preferred IDE": get_counts("3. Which IDE do you prefer?", ["VSCode", "PyCharm", "Jupyter", "Sublime", "Other"]),
        "4. Area of Interest": get_counts("4. What area are you most interested in?", ["Web Dev", "Data Science", "AI/ML", "Cybersecurity", "Mobile Dev"]),
        "5. Learning Style": get_counts("5. How do you prefer to learn?", ["YouTube", "Blogs", "Courses", "Books", "Docs"]),
        "6. Coding Experience (Years)": get_counts("6. How many years of coding experience do you have?", ["0-1", "2-3", "4-6", "7+"]),
        "7. Backend Language Preference": get_counts("7. What is your preferred backend language?", ["Node.js", "Python", "Java", "PHP", "Go"])
    }

# Sidebar navigation
section = st.sidebar.radio("Navigate", ["Submit Answers", "View Visualizations"])

# --------------------------
# SECTION 1: Submit Answers
# --------------------------
if section == "Submit Answers":
    st.title("🗳️ Developer Poll Submission")

    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if not st.session_state.submitted:
        with st.form("poll_form"):
            q1 = st.radio("1. What is your favorite programming language?", ["Python", "JavaScript", "Java", "C++"])
            q2 = st.select_slider("2. How often do you code?", options=["Daily", "Weekly", "Monthly", "Rarely"])
            q3 = st.selectbox("3. Which IDE do you prefer?", ["VSCode", "PyCharm", "Jupyter", "Sublime", "Other"])
            q4 = st.radio("4. What area are you most interested in?", ["Web Dev", "Data Science", "AI/ML", "Cybersecurity", "Mobile Dev"])
            q5 = st.selectbox("5. How do you prefer to learn?", ["YouTube", "Blogs", "Courses", "Books", "Docs"])
            q6 = st.radio("6. How many years of coding experience do you have?", ["0-1", "2-3", "4-6", "7+"])
            q7 = st.selectbox("7. What is your preferred backend language?", ["Node.js", "Python", "Java", "PHP", "Go"])

            submitted = st.form_submit_button("Submit Poll")

            if submitted:
                save_response("1. What is your favorite programming language?", q1)
                save_response("2. How often do you code?", q2)
                save_response("3. Which IDE do you prefer?", q3)
                save_response("4. What area are you most interested in?", q4)
                save_response("5. How do you prefer to learn?", q5)
                save_response("6. How many years of coding experience do you have?", q6)
                save_response("7. What is your preferred backend language?", q7)

                st.success("✅ Thank you for your submission!")
                st.session_state.submitted = True
    else:
        st.info("You've already submitted your responses in this session.")

# ------------------------------
# SECTION 2: View Visualizations
# ------------------------------
elif section == "View Visualizations":
    st.title("📊 Poll Results")

    results = load_data()

    if not results:
        st.warning("No poll data found.")
        st.stop()

    questions = list(results.keys())

    for i in range(0, len(questions), 2):
        col1, col2 = st.columns(2)

        # First Chart
        with col1:
            title = questions[i]
            data = results[title]
            st.write(f"**{title}**")
            fig, ax = plt.subplots()
            ax.bar(data.index, data.values, color="skyblue")
            plt.xticks(rotation=30)
            st.pyplot(fig)

        # Second Chart
        if i + 1 < len(questions):
            with col2:
                title = questions[i + 1]
                data = results[title]
                st.write(f"**{title}**")
                fig, ax = plt.subplots()
                if title == "2. Coding Frequency":
                    ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90)
                else:
                    ax.bar(data.index, data.values, color="lightgreen")
                    plt.xticks(rotation=30)
                st.pyplot(fig)

    if st.checkbox("Show Raw Data"):
        st.dataframe(pd.read_csv(CSV_FILE))
