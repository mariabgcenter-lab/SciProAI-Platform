import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="TrainAI — Staff Training & Competency Suite",
    layout="wide"
)

st.title("🎓 TrainAI — Staff Training & Competency Suite")
st.write("""
Create, track, and evaluate **laboratory training**, **competency assessments**,  
and **staff qualification records** for CLIA, ISO, CAP, and research environments.
""")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.header("TrainAI Modules")
module = st.sidebar.radio(
    "Select a module:",
    [
        "Training Record Builder",
        "Competency Assessment Designer",
        "Training Table Explorer"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — Training Record Builder
# ---------------------------------------------------------
if module == "Training Record Builder":
    st.subheader("📝 Training Record Builder")

    staff_name = st.text_input("Staff Name:")
    role = st.text_input("Role / Position:")
    training_title = st.text_input("Training Title:")
    trainer = st.text_input("Trainer:")
    date_completed = st.date_input("Date Completed:")
    notes = st.text_area("Training Notes / Summary:")

    if st.button("Generate Training Record"):
        if not staff_name.strip() or not training_title.strip():
            st.warning("Please enter at least Staff Name and Training Title.")
        else:
            st.markdown("### Training Record Summary")
            st.write(f"**Staff Name:** {staff_name}")
            st.write(f"**Role:** {role}")
            st.write(f"**Training Title:** {training_title}")
            st.write(f"**Trainer:** {trainer}")
            st.write(f"**Date Completed:** {date_completed}")
            st.write(f"**Notes:**\n{notes}")

# ---------------------------------------------------------
# MODULE 2 — Competency Assessment Designer
# ---------------------------------------------------------
if module == "Competency Assessment Designer":
    st.subheader("📊 Competency Assessment Designer")

    st.write("Create structured competency assessments for laboratory staff.")

    assessment_title = st.text_input("Assessment Title:")
    num_items = st.number_input("Number of competency items", min_value=1, max_value=50, value=5)

    items = []
    for i in range(int(num_items)):
        item = st.text_input(f"Competency Item {i+1}:", key=f"comp_item_{i}")
        items.append(item)

    if st.button("Generate Competency Assessment"):
        if not assessment_title.strip():
            st.warning("Please enter an assessment title.")
        else:
            st.markdown("### Competency Assessment")
            st.write(f"**Assessment Title:** {assessment_title}")
            st.write("### Items")
            for i, item in enumerate(items, start=1):
                if item.strip():
                    st.write(f"- Item {i}: {item}")

# ---------------------------------------------------------
# MODULE 3 — Training Table Explorer
# ---------------------------------------------------------
if module == "Training Table Explorer":
    st.subheader("📋 Training Table Explorer")

    uploaded = st.file_uploader("Upload training table (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### Training Table Preview")
        st.dataframe(df.head())

        st.write("### Column Types")
        st.json({col: str(df[col].dtype) for col in df.columns})
