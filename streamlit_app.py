import streamlit as st
import pandas as pd

st.set_page_config(page_title="Haas AI Course Planner", page_icon="📚")
st.title("🎓 Haas AI-Powered Course Planner")

st.write("Upload your materials and we'll recommend the best classes for you!")

# Uploads
course_catalog_file = st.file_uploader("Upload Haas Course Catalog (Excel)", type=["xlsx"])
resume_file = st.file_uploader("Upload Your Resume (PDF or TXT)", type=["pdf", "txt"])

# User Inputs
units_needed = st.number_input("How many units do you need to take this semester?", min_value=1, max_value=30, value=10)
preferred_times = st.multiselect(
    "Preferred Class Times:",
    ["Mornings", "Afternoons", "Evenings"]
)
focus_areas = st.text_area("What do you want to focus on this semester? (e.g., AI, Finance, Entrepreneurship)")

submit = st.button("Generate Recommended Schedule")

if submit:
    if not course_catalog_file:
        st.error("Please upload a course catalog file.")
    else:
        # Load Course Catalog
        course_catalog = pd.read_excel(course_catalog_file)

        # Assume course_catalog has columns: 'Course Name', 'Units', 'Times', 'Description'
        st.success("Course catalog loaded!")

        # Simplified matching: if focus_areas keywords appear in the course description
        matching_courses = course_catalog[course_catalog['Description'].str.contains(focus_areas, case=False, na=False)]

        if matching_courses.empty:
            st.warning("No perfect matches found. Showing some popular courses instead.")
            recommended_courses = course_catalog.sample(min(5, len(course_catalog)))
        else:
            recommended_courses = matching_courses

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
            st.dataframe(selected_df[['Course Name', 'Units', 'Times']])
        else:
            st.error("Couldn't meet unit requirement with available courses. Try adjusting your focus area.")

        # Placeholder for Email
        st.markdown("---")
        st.subheader("📧 Send Your Schedule")
        email = st.text_input("Enter your email address to receive your recommended schedule:")
        send_email = st.button("Send Schedule")

        if send_email:
            st.success(f"Schedule would be emailed to {email} (placeholder)")

st.markdown("""
---

*This is a demo version. Actual AI matching based on resume parsing and smart time-slot recommendations can be added in a full implementation!*
""")
