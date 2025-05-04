import streamlit as st
import pandas as pd
import PyPDF2

st.set_page_config(page_title="Haas AI Course Planner", page_icon="📚")
st.title("🎓 Haas AI-Powered Course Planner")

st.write("Upload your course catalog and materials, and we'll recommend the best classes for you!")

# Uploads
course_catalog_file = st.file_uploader("Upload Haas Course Catalog (Excel)", type=["xlsx"])
course_info_files = st.file_uploader("Upload Course Descriptions and Reviews (PDF only)", type=["pdf"], accept_multiple_files=True)
resume_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])

# Time Preferences (still show nice UI but don't actually process)
time_options = ["Morning (before 12pm)", "Afternoon (12-5pm)", "Evening (after 5pm)"]
days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

st.subheader("🕰️ Preferred Times and Days")
preferred_times = st.multiselect("Select your preferred times:", time_options)
preferred_days = st.multiselect("Select your preferred days:", days_of_week)

# Other Inputs
units_needed = st.number_input("How many units do you need to take this semester?", min_value=1, max_value=30, value=10)
focus_areas = st.text_area("What do you want to focus on this semester? (e.g., AI, Finance, Entrepreneurship)")

submit = st.button("Generate Recommended Schedule")

if submit:
    st.success("✅ Files uploaded and preferences captured!")

    st.subheader("🎯 Recommended Schedule")

    # Hardcoded output (you can modify this list however you like)
    if "AI" in focus_areas or "Data" in focus_areas:
        courses = [
            {"Course Name": "Applied Machine Learning", "Units": 3, "Days": "Mon/Wed", "Times": "Morning"},
            {"Course Name": "Data Strategy for Business", "Units": 2, "Days": "Tue/Thu", "Times": "Afternoon"},
            {"Course Name": "AI Ethics and Society", "Units": 2, "Days": "Friday", "Times": "Morning"},
        ]
    elif "Finance" in focus_areas:
        courses = [
            {"Course Name": "Financial Modeling and Valuation", "Units": 3, "Days": "Mon/Wed", "Times": "Morning"},
            {"Course Name": "Venture Capital", "Units": 2, "Days": "Tue/Thu", "Times": "Afternoon"},
            {"Course Name": "Global Financial Markets", "Units": 2, "Days": "Friday", "Times": "Morning"},
        ]
    else:
        courses = [
            {"Course Name": "Leadership Communications", "Units": 2, "Days": "Mon", "Times": "Evening"},
            {"Course Name": "Negotiations", "Units": 2, "Days": "Wed", "Times": "Afternoon"},
            {"Course Name": "Marketing Strategy", "Units": 3, "Days": "Tue/Thu", "Times": "Morning"},
        ]

    # Display "fake" schedule
    courses_df = pd.DataFrame(courses)
    st.dataframe(courses_df)

    # Email placeholder
    st.markdown("---")
    st.subheader("📧 Send Your Schedule")
    email = st.text_input("Enter your email address to receive your recommended schedule:")
    send_email = st.button("Send Schedule")

    if send_email:
        st.success(f"Schedule would be emailed to {email} (placeholder)")

st.markdown("""
---

*This is a demo version. In a full system, AI matching and real-time course scheduling would be implemented!*
""")
