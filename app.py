# File: app.py
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Google Sheet setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Developer Poll").worksheet("Responses")

# Save response to sheet
def save_to_sheet(data_dict):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [now] + list(data_dict.values())
    sheet.append_row(row)

# Load sheet data as DataFrame
def load_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Main interface
st.title("🗳 Developer Poll")

menu = st.sidebar.radio("Navigation", ["1. Submit Answers", "2. View Poll Results"])

if menu == "1. Submit Answers":
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if not st.session_state.submitted:
        with st.form("poll_form"):
            q1 = st.radio("1. Favorite programming language?", ["Python", "JavaScript", "Java", "C++"])
            q2 = st.select_slider("2. Coding frequency?", ["Daily", "Weekly", "Monthly", "Rarely"])
            q3 = st.selectbox("3. Preferred IDE?", ["VSCode", "PyCharm", "Jupyter", "Other"])
            q4 = st.radio("4. Learning preference?", ["YouTube", "Blogs", "Courses", "Books", "Docs"])
            q5 = st.radio("5. Do you use Git for version control?", ["Yes", "No"])

            submitted = st.form_submit_button("Submit")

            if submitted:
                answers = {
                    "Q1": q1,
                    "Q2": q2,
                    "Q3": q3,
                    "Q4": q4,
                    "Q5": q5
                }
                save_to_sheet(answers)
                st.success("✅ Response recorded!")
                st.session_state.submitted = True
    else:
        st.info("You’ve already submitted your response in this session.")

elif menu == "2. View Poll Results":
    df = load_data()

    if df.empty:
        st.warning("No responses yet.")
    else:
        st.subheader("📊 Poll Results")
        cols = st.columns(2)

        # Q1 Bar chart
        with cols[0]:
            st.write("**1. Favorite programming language**")
            q1_counts = df["Q1"].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.bar(q1_counts.index, q1_counts.values, color='skyblue')
            ax1.set_ylabel("Count")
            st.pyplot(fig1)

        # Q2 Pie chart
        with cols[1]:
            st.write("**2. Coding frequency**")
            q2_counts = df["Q2"].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(q2_counts.values, labels=q2_counts.index, autopct="%1.1f%%", startangle=90)
            ax2.axis("equal")
            st.pyplot(fig2)

        # Show all data
        if st.checkbox("Show raw responses"):
            st.dataframe(df)
