import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_FILE = "poll_results.csv"

# Load and process data
@st.cache_data
def load_data():
    if not os.path.isfile(CSV_FILE):
        return {}

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

# Streamlit UI
st.title("📊 Poll Results Dashboard")

results = load_data()

if not results:
    st.warning("No poll data found.")
    st.stop()

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

# Optional: Raw data display
if st.checkbox("Show Raw Data"):
    df = pd.read_csv(CSV_FILE)
    st.dataframe(df)
