import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="QCAI — Quality Control & Audit Suite",
    layout="wide"
)

st.title("✅ QCAI — Quality Control & Audit Suite")
st.write("""
Design, review, and explore **QC records**, **audit trails**, and **quality metrics**  
for CLIA, ISO, CAP, and research laboratory environments.
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
        "Audit Trail Preview"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — QC Record Builder
# ---------------------------------------------------------
if module == "QC Record Builder":
    st.subheader("🧾 QC Record Builder")

    qc_id = st.text_input("QC Record ID:")
    assay_name = st.text_input("Assay / Method Name:")
    lot_number = st.text_input("Reagent / Kit Lot Number:")
    run_date = st.date_input("Run Date:")
    operator = st.text_input("Operator:")
    controls = st.text_area("Controls Used (positive, negative, internal):")
    results = st.text_area("QC Results / Observations:")
    actions = st.text_area("Corrective / Preventive Actions:")

    if st.button("Generate QC Record Summary"):
        if not qc_id.strip() or not assay_name.strip():
            st.warning("Please enter at least QC Record ID and Assay Name.")
        else:
            st.markdown("### QC Record Summary")
            st.write(f"**QC Record ID:** {qc_id}")
            st.write(f"**Assay / Method:** {assay_name}")
            st.write(f"**Lot Number:** {lot_number}")
            st.write(f"**Run Date:** {run_date}")
            st.write(f"**Operator:** {operator}")
            st.write(f"**Controls:**\n{controls}")
            st.write(f"**Results / Observations:**\n{results}")
            st.write(f"**Corrective / Preventive Actions:**\n{actions}")

# ---------------------------------------------------------
# MODULE 2 — QC Table Explorer
# ---------------------------------------------------------
if module == "QC Table Explorer":
    st.subheader("📋 QC Table Explorer")

    uploaded = st.file_uploader("Upload QC table (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### QC Table Preview")
        st.dataframe(df.head())

        st.write("### Column Types")
        st.json({col: str(df[col].dtype) for col in df.columns})

# ---------------------------------------------------------
# MODULE 3 — Audit Trail Preview
# ---------------------------------------------------------
if module == "Audit Trail Preview":
    st.subheader("🧾 Audit Trail Preview")

    uploaded = st.file_uploader("Upload audit trail (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### Audit Trail Preview")
        st.dataframe(df.head())

        if {"timestamp", "user", "action"} <= set(df.columns):
            st.write("### Recent Actions")
            st.dataframe(df.sort_values("timestamp", ascending=False).head(20))
        else:
            st.warning("Expected columns not found: timestamp, user, action")
