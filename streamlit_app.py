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

# User Inputs
units_needed = st.number_input("How many units do you need to take this semester?", min_value=1, max_value=30, value=10)

st.write("Select your preferred times for each day:")
day_time_preferences = {}
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_options = ["Morning (before 12pm)", "Afternoon (12-5pm)", "Evening (after 5pm)"]

for day in days_of_week:
    selected_times = st.multiselect(f"{day}:", time_options, key=day)
    day_time_preferences[day] = selected_times

focus_areas = st.text_area("What do you want to focus on this semester? (e.g., AI, Finance, Entrepreneurship)")

submit = st.button("Generate Recommended Schedule")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def match_day_time(course_days, course_time, preferences):
    for day in days_of_week:
        if day in course_days:
            for pref in preferences[day]:
                if pref.split()[0] in course_time:
                    return True
    return False

if submit:
    if not course_catalog_file:
        st.error("Please upload a course catalog file.")
    else:
        # Load Course Catalog
        course_catalog = pd.read_excel(course_catalog_file)

        # Assume course_catalog has columns: 'Course Name', 'Units', 'Times', 'Days'
        st.success("Course catalog loaded!")

        # Extract course info and resume text
        course_info_text = ""
        if course_info_files:
            for uploaded_file in course_info_files:
                course_info_text += extract_text_from_pdf(uploaded_file)

        resume_text = ""
        if resume_file:
            resume_text = extract_text_from_pdf(resume_file)

        # Combine focus areas + resume for better matching
        combined_focus_text = focus_areas + " " + resume_text

        # Matching logic
        matching_courses = course_catalog[course_catalog['Course Name'].str.contains(focus_areas, case=False, na=False)]

        if matching_courses.empty:
            st.warning("No perfect matches found. Showing some popular courses instead.")
            recommended_courses = course_catalog.sample(min(5, len(course_catalog)))
        else:
            recommended_courses = matching_courses

        # Filter by preferred days and times using the new day-time preferences
        filtered_courses = []
        for idx, row in recommended_courses.iterrows():
            course_days = row['Days'] if pd.notna(row['Days']) else ""
            course_time = row['Times'] if pd.notna(row['Times']) else ""
            if match_day_time(course_days, course_time, day_time_preferences):
                filtered_courses.append(row)

        recommended_courses = pd.DataFrame(filtered_courses)

        # Try to fit into unit needs (basic approach)
        selected_courses = []
        total_units = 0

        for idx, row in recommended_courses.iterrows():
            if total_units + row['Units'] <= units_needed:
                selected_courses.append(row)
                total_units += row['Units']

        # Display Selected Courses
        if selected_courses:
            st.subheader("🎓 Your Recommended Courses")
            selected_df = pd.DataFrame(selected_courses)
            st.dataframe(selected_df[['Course Name', 'Units', 'Times', 'Days']])
        else:
            st.error("Couldn't meet unit requirement with available courses. Try adjusting your focus area or preferred schedule.")

        # Placeholder for Email
        st.markdown("---")
        st.subheader("📧 Send Your Schedule")
        email = st.text_input("Enter your email address to receive your recommended schedule:")
        send_email = st.button("Send Schedule")

        if send_email:
            st.success(f"Schedule would be emailed to {email} (placeholder)")

st.markdown("""
---

*This is a demo version. Actual NLP matching based on resume parsing and course review sentiment analysis can be added in a full implementation!*
""")
