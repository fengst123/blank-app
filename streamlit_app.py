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

# Setup for dynamic preferred times
if "time_preferences" not in st.session_state:
    st.session_state.time_preferences = [{"times": [], "days": []}]

time_options = ["Morning (before 12pm)", "Afternoon (12-5pm)", "Evening (after 5pm)"]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
short_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

st.subheader("🕰️ Preferred Times and Days")
for idx, pref in enumerate(st.session_state.time_preferences):
    st.markdown(f"**Preference #{idx+1}**")
    # Time multi-select
    selected_times = st.multiselect(
        f"Select Time(s) for Preference #{idx+1}", 
        time_options, 
        default=st.session_state.time_preferences[idx]["times"], 
        key=f"times_{idx}"
    )
    st.session_state.time_preferences[idx]["times"] = selected_times

    # Day toggles
    day_selection = []
    st.write("Select Days:")
    day_cols = st.columns(7)
    for i, day in enumerate(short_days):
        toggle = day_cols[i].toggle(day, key=f"day_{idx}_{day}")
        if toggle:
            day_selection.append(days_of_week[i])
    st.session_state.time_preferences[idx]["days"] = day_selection

add_row = st.button("➕ Add Another Time Preference")
remove_row = st.button("➖ Remove Last Time Preference")

if add_row:
    st.session_state.time_preferences.append({"times": [], "days": []})
if remove_row and len(st.session_state.time_preferences) > 1:
    st.session_state.time_preferences.pop()

# Other Inputs
units_needed = st.number_input("How many units do you need to take this semester?", min_value=1, max_value=30, value=10)
focus_areas = st.text_area("What do you want to focus on this semester? (e.g., AI, Finance, Entrepreneurship)")

submit = st.button("Generate Recommended Schedule")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def matches_preferred_times(course_days, course_time, time_preferences):
    for pref in time_preferences:
        for day in pref["days"]:
            if day in course_days:
                for time_pref in pref["times"]:
                    if time_pref.split()[0] in course_time:
                        return True
    return False

if submit:
    if not course_catalog_file:
        st.error("Please upload a course catalog file.")
    else:
        # Load Course Catalog
        course_catalog = pd.read_excel(course_catalog_file)

        st.success("Course catalog loaded!")

        # Extract text from uploads
        course_info_text = ""
        if course_info_files:
            for uploaded_file in course_info_files:
                course_info_text += extract_text_from_pdf(uploaded_file)

        resume_text = ""
        if resume_file:
            resume_text = extract_text_from_pdf(resume_file)

        combined_focus_text = focus_areas + " " + resume_text

        matching_courses = course_catalog[course_catalog['Course Name'].str.contains(focus_areas, case=False, na=False)]

        if matching_courses.empty:
            st.warning("No perfect matches found. Showing random courses instead.")
            recommended_courses = course_catalog.sample(min(5, len(course_catalog)))
        else:
            recommended_courses = matching_courses

        # New filtering based on dynamic preferred times and days
        filtered_courses = []
        for idx, row in recommended_courses.iterrows():
            course_days = row['Days'] if pd.notna(row['Days']) else ""
            course_time = row['Times'] if pd.notna(row['Times']) else ""
            if matches_preferred_times(course_days, course_time, st.session_state.time_preferences):
                filtered_courses.append(row)

        recommended_courses = pd.DataFrame(filtered_courses)

        # Try to fit into unit needs
        selected_courses = []
        total_units = 0

        for idx, row in recommended_courses.iterrows():
            if total_units + row['Units'] <= units_needed:
                selected_courses.append(row)
                total_units += row['Units']

        if selected_courses:
            st.subheader("🎓 Your Recommended Courses")
            selected_df = pd.DataFrame(selected_courses)
            st.dataframe(selected_df[['Course Name', 'Units', 'Times', 'Days']])
        else:
            st.error("Couldn't meet unit requirement with available courses. Try adjusting your preferences.")

        # Email Placeholder
        st.markdown("---")
        st.subheader("📧 Send Your Schedule")
        email = st.text_input("Enter your email address to receive your recommended schedule:")
        send_email = st.button("Send Schedule")

        if send_email:
            st.success(f"Schedule would be emailed to {email} (placeholder)")

st.markdown("""
---

*This is a demo version. Full NLP matching and auto-scheduling logic could be added in a full system!*
""")
