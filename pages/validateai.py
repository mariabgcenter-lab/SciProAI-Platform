import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="ValidateAI — Validation Plan Generator",
    layout="wide"
)

st.title("📑 ValidateAI — Validation Plan Generator")
st.write("""
Create structured **CLIA, CAP, and ISO 17025 validation plans**  
including accuracy, precision, LoD/LoQ, reportable range, and method comparison sections.
""")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.header("Validation Modules")
module = st.sidebar.radio(
    "Select a module:",
    [
        "Validation Plan Builder",
        "Accuracy / Precision Tables",
        "LoD / LoQ Calculator",
        "Method Comparison Summary"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — Validation Plan Builder
# ---------------------------------------------------------
if module == "Validation Plan Builder":
    st.subheader("🧾 Validation Plan Builder")

    assay_name = st.text_input("Assay Name:")
    assay_type = st.selectbox("Assay Type:", ["qPCR", "ddPCR", "Culture", "Immunoassay", "Other"])
    regulatory_framework = st.selectbox("Regulatory Framework:", ["CLIA", "CAP", "ISO 17025"])

    purpose = st.text_area("Purpose of Validation:")
    scope = st.text_area("Scope:")
    acceptance_criteria = st.text_area("Acceptance Criteria:")
    materials = st.text_area("Materials / Equipment:")
    procedure = st.text_area("Validation Procedure:")
    reporting = st.text_area("Reporting Requirements:")

    if st.button("Generate Validation Plan"):
        if not assay_name:
            st.warning("Please enter an assay name.")
        else:
            st.markdown("### Validation Plan Summary")
            st.write(f"**Assay Name:** {assay_name}")
            st.write(f"**Assay Type:** {assay_type}")
            st.write(f"**Framework:** {regulatory_framework}")
            st.write(f"**Purpose:** {purpose}")
            st.write(f"**Scope:** {scope}")
            st.write(f"**Acceptance Criteria:** {acceptance_criteria}")
            st.write(f"**Materials / Equipment:** {materials}")
            st.write(f"**Procedure:**\n{procedure}")
            st.write(f"**Reporting Requirements:** {reporting}")

# ---------------------------------------------------------
# MODULE 2 — Accuracy / Precision Tables
# ---------------------------------------------------------
if module == "Accuracy / Precision Tables":
    st.subheader("📊 Accuracy / Precision Tables")

    uploaded = st.file_uploader("Upload accuracy/precision dataset (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### Dataset Preview")
        st.dataframe(df.head())

        numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()

        if numeric_cols:
            st.write("### Summary Statistics")
            st.dataframe(df[numeric_cols].describe
