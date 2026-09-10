import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="QCAI — QA/QC Assistant",
    layout="wide"
)

st.title("🧪 QCAI — QA/QC Assistant")
st.write("""
Create and manage **QA/QC records**, acceptance criteria,  
deviation logs, and quality summaries for laboratory workflows.
""")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.header("QCAI Modules")
module = st.sidebar.radio(
    "Select a module:",
    [
        "QC Record Builder",
        "QC Table Explorer",
        "Deviation & Corrective Action Log"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — QC Record Builder
# ---------------------------------------------------------
if module == "QC Record Builder":
    st.subheader("📋 QC Record Builder")

    qc_title = st.text_input("QC Record Title:")
    qc_id = st.text_input("QC ID / Code:")
    qc_material = st.text_input("Material / Sample:")
    qc_method = st.text_input("Method / Assay:")
    qc_acceptance = st.text_area("Acceptance Criteria:")
    qc_results = st.text_area("QC Results:")
    qc_interpretation = st.text_area("Interpretation:")
    qc_reviewer = st.text_input("Reviewer Name:")
    qc_date = st.date_input("Review Date:")

    if st.button("Generate QC Record"):
        if not qc_title or not qc_id:
            st.warning("Please enter QC Title and QC ID.")
        else:
            st.markdown("### QC Record Summary")
            st.write(f"**Title:** {qc_title}")
            st.write(f"**QC ID:** {qc_id}")
            st.write(f"**Material / Sample:** {qc_material}")
            st.write(f"**Method / Assay:** {qc_method}")
            st.write(f"**Acceptance Criteria:** {qc_acceptance}")
            st.write(f"**Results:** {qc_results}")
            st.write(f"**Interpretation:** {qc_interpretation}")
            st.write(f"**Reviewer:** {qc_reviewer}")
            st.write(f"**Review Date:** {qc_date}")

# ---------------------------------------------------------
# MODULE 2 — QC Table Explorer
# ---------------------------------------------------------
if module == "QC Table Explorer":
    st.subheader("📊 QC Table Explorer")

    uploaded = st.file_uploader("Upload QC dataset (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### QC Table Preview")
        st.dataframe(df.head())

        numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()

        if numeric_cols:
            st.write("### Summary Statistics")
            st.dataframe(df[numeric_cols].describe())

# ---------------------------------------------------------
# MODULE 3 — Deviation & Corrective Action Log
# ---------------------------------------------------------
if module == "Deviation & Corrective Action Log":
    st.subheader("⚠️ Deviation & Corrective Action Log")

    deviation_desc = st.text_area("Describe the deviation:")
    root_cause = st.text_area("Root cause analysis:")
    corrective_action = st.text_area("Corrective action:")
    preventive_action = st.text_area("Preventive action:")
    responsible_person = st.text_input("Responsible person:")
    date_logged = st.date_input("Date logged:")

    if st.button("Generate Deviation Log"):
        if not deviation_desc.strip():
            st.warning("Please describe the deviation.")
        else:
            st.markdown("### Deviation Log Summary")
            st.write(f"**Deviation:** {deviation_desc}")
            st.write(f"**Root Cause:** {root_cause}")
            st.write(f"**Corrective Action:** {corrective_action}")
            st.write(f"**Preventive Action:** {preventive_action}")
            st.write(f"**Responsible Person:** {responsible_person}")
            st.write(f"**Date Logged:** {date_logged}")
