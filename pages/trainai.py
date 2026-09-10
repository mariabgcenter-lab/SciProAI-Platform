import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="TrainAI — Competency & Training Module",
    layout="wide"
)

st.title("🎓 TrainAI — Competency & Training Module")
st.write("""
Create and manage **competency assessments**, training records,  
skills matrices, and qualification documentation for laboratory staff.
""")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.header("TrainAI Modules")
module = st.sidebar.radio(
    "Select a module:",
    [
        "Competency Checklist Builder",
        "Training Record Generator",
        "Skills Matrix Explorer"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — Competency Checklist Builder
# ---------------------------------------------------------
if module == "Competency Checklist Builder":
    st.subheader("📋 Competency Checklist Builder")

    role = st.text_input("Role / Position:")
    assessor = st.text_input("Assessor Name:")
    date_assessed = st.date_input("Assessment Date:")

    st.write("### Add Competency Items")
    num_items = st.number_input("Number of competency items", min_value=1, max_value=50, value=5)

    items = []
    for i in range(int(num_items)):
        item = st.text_input(f"Competency Item {i+1}:", key=f"item_{i}")
        items.append(item)

    if st.button("Generate Competency Checklist"):
        if not role:
            st.warning("Please enter a role or position.")
        else:
            st.markdown("### Competency Checklist Summary")
            st.write(f"**Role:** {role}")
            st.write(f"**Assessor:** {assessor}")
            st.write(f"**Assessment Date:** {date_assessed}")

            st.write("### Competency Items")
            for i, item in enumerate(items, start=1):
                if item.strip():
                    st.write(f"- {item}")

# ---------------------------------------------------------
# MODULE 2 — Training Record Generator
# ---------------------------------------------------------
if module == "Training Record Generator":
    st.subheader("📝 Training Record Generator")

    trainee = st.text_input("Trainee Name:")
    trainer = st.text_input("Trainer Name:")
    training_topic = st.text_input("Training Topic:")
    training_date = st.date_input("Training Date:")
    training_notes = st.text_area("Training Notes:")
    competency_result = st.selectbox("Competency Result:", ["Pass", "Fail", "Needs Review"])

    if st.button("Generate Training Record"):
        if not trainee or not trainer:
            st.warning("Please enter trainee and trainer names.")
        else:
            st.markdown("### Training Record Summary")
            st.write(f"**Trainee:** {trainee}")
            st.write(f"**Trainer:** {trainer}")
            st.write(f"**Topic:** {training_topic}")
            st.write(f"**Date:** {training_date}")
            st.write(f"**Notes:** {training_notes}")
            st.write(f"**Competency Result:** {competency_result}")

# ---------------------------------------------------------
# MODULE 3 — Skills Matrix Explorer
# ---------------------------------------------------------
if module == "Skills Matrix Explorer":
    st.subheader("📊 Skills Matrix Explorer")

    uploaded = st.file_uploader("Upload skills matrix (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### Skills Matrix Preview")
        st.dataframe(df.head())

        st.write("### Staff Skills Summary")
        st.dataframe(df.describe(include="all"))
