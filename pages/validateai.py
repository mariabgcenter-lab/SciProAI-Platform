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
            st.dataframe(df[numeric_cols].describe())

# ---------------------------------------------------------
# MODULE 3 — LoD / LoQ Calculator
# ---------------------------------------------------------
if module == "LoD / LoQ Calculator":
    st.subheader("📉 LoD / LoQ Calculator")

    st.write("Enter replicate measurements for blank and low‑positive samples.")

    blank_vals = st.text_area("Blank replicates (comma‑separated):")
    low_pos_vals = st.text_area("Low‑positive replicates (comma‑separated):")

    if st.button("Calculate LoD / LoQ"):
        try:
            blank = [float(x) for x in blank_vals.split(",") if x.strip()]
            lowpos = [float(x) for x in low_pos_vals.split(",") if x.strip()]

            if len(blank) < 3 or len(lowpos) < 3:
                st.warning("Please enter at least 3 replicates for each group.")
            else:
                import numpy as np

                lod = np.mean(blank) + 3 * np.std(blank)
                loq = np.mean(blank) + 10 * np.std(blank)

                st.write("### Results")
                st.write(f"**LoD:** {lod:.4f}")
                st.write(f"**LoQ:** {loq:.4f}")

        except Exception as e:
            st.error(f"Error calculating LoD/LoQ: {e}")

# ---------------------------------------------------------
# MODULE 4 — Method Comparison Summary
# ---------------------------------------------------------
if module == "Method Comparison Summary":
    st.subheader("📈 Method Comparison Summary")

    uploaded = st.file_uploader("Upload method comparison dataset (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### Dataset Preview")
        st.dataframe(df.head())

        if "new_method" in df.columns and "reference_method" in df.columns:
            st.write("### Correlation")
            corr = df["new_method"].corr(df["reference_method"])
            st.write(f"**Correlation (r):** {corr:.4f}")

            st.write("### Difference (New - Reference)")
            df["difference"] = df["new_method"] - df["reference_method"]
            st.dataframe(df[["new_method", "reference_method", "difference"]])

        else:
            st.warning("Dataset must contain 'new_method' and 'reference_method' columns.")
