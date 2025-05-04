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
    st.session_state.time_preferences = [{"times": [], "days": {day: False for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}}]

time_options = ["Morning (before 12pm)", "Afternoon (12-5pm)", "Evening (after 5pm)"]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
short_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

st.subheader("🕰️ Preferred Times and Days")

# Add / Remove preference logic
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Add Another Time Preference"):
        st.session_state.time_preferences.append({"times": [], "days": {day: False for day in short_days}})
with col2:
    if st.button("➖ Remove Last Time Preference") and len(st.session_state.time_preferences) > 1:
        st.session_state.time_preferences.pop()

for idx, pref in enumerate(st.session_state.time_preferences):
    st.markdown(f"**Preference #{idx+1}**")

    # Time Multi-select
    selected_times = st.multiselect(
        f"Select Time(s) for Preference #{idx+1}",
        options=time_options,
        default=pref["times"],
        key=f"times_{idx}"
    )
    st.session_state.time_preferences[idx]["times"] = selected_times

    # Days - Checkboxes
    st.write("Select Days:")
    day_cols = st.columns(7)
    for i, day in enumerate(short_days):
        checked = st.session_state.time_preferences[idx]["days"][day]
        new_checked = day_cols[i].checkbox(day, value=checked, key=f"day_{idx}_{day}_checkbox")
        st.session_state.time_preferences[idx]["days"][day] = new_checked
# Other Inputs
units_needed = st.number_input("How many units do you need to take this semester?", min_value=1, max_value=30, value=10)
focus_areas = st.text_area("What do you want to focus on this semester? (e.g., AI, Finance, Entrepreneurship)")

submit = st.button("Generate Recommended Schedule")

if submit:
    st.success("✅ Files uploaded and preferences captured!")

    st.subheader("🎯 Recommended Schedule")

    # Hardcoded real output for your profile
    courses = [
        {"Course Name": "Negotiations and Conflict Resolution", "Units": 2, "Days": "Mon", "Times": "8AM–11AM", "Why Take This Class": "Build influence, persuasion, and conflict management — essential soft skills for PMs and leaders."},
        {"Course Name": "Managing the New Product Development Process", "Units": 3, "Days": "Mon & Wed", "Times": "11AM–12:30PM", "Why Take This Class": "Learn frameworks for ideating, building, and launching new products — core PM skillset."},
        {"Course Name": "Storytelling for Leadership", "Units": 1, "Days": "Tues", "Times": "2PM–5PM", "Why Take This Class": "Sharpen your ability to communicate vision, inspire teams, and rally stakeholders — critical leadership soft skill."},
        {"Course Name": "Global Leadership", "Units": 3, "Days": "Tues", "Times": "4PM–6PM", "Why Take This Class": "Develop skills to lead diverse teams across cultures and markets — increasingly important for PMs at global companies."},
        {"Course Name": "Opportunity Recognition: Technology & Entrepreneurship", "Units": 2, "Days": "Wed", "Times": "4PM–6PM", "Why Take This Class": "Train your product-sense muscle by spotting trends, customer needs, and innovation opportunities."},
        {"Course Name": "Tech and the City", "Units": 3, "Days": "Tues & Thurs", "Times": "11AM–12:30PM", "Why Take This Class": "Explore how tech drives urban innovation — broadens strategic thinking about product ecosystems."},
    ]

    # Convert to DataFrame for display
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
