import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="BizDocAI — Business Document Summary",
    layout="wide"
)

st.title("📄 BizDocAI — Business Document Summary")
st.write("""
Summarize **SOPs**, **validation plans**, **QC records**, **training documents**,  
and other business or laboratory materials into structured summaries.
""")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.header("BizDocAI Modules")
module = st.sidebar.radio(
    "Select a module:",
    [
        "Document Summary",
        "Document Table Explorer",
        "Structured Section Extractor"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — Document Summary
# ---------------------------------------------------------
if module == "Document Summary":
    st.subheader("📝 Document Summary")

    uploaded = st.file_uploader("Upload document (TXT, CSV, or DOCX converted to text)", type=["txt", "csv"])

    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
                text = "\n".join(df.astype(str).values.flatten())
            else:
                text = uploaded.read().decode("utf-8")

            st.write("### Raw Document Preview")
            st.write(text[:500] + "..." if len(text) > 500 else text)

            if st.button("Generate Summary"):
                st.write("### Summary")
                st.write(text[:300] + "...")

        except Exception as e:
            st.error(f"Error reading file: {e}")

# ---------------------------------------------------------
# MODULE 2 — Document Table Explorer
# ---------------------------------------------------------
if module == "Document Table Explorer":
    st.subheader("📋 Document Table Explorer")

    uploaded = st.file_uploader("Upload table (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### Table Preview")
        st.dataframe(df.head())

        st.write("### Column Summary")
        st.json({col: str(df[col].dtype) for col in df.columns})

# ---------------------------------------------------------
# MODULE 3 — Structured Section Extractor
# ---------------------------------------------------------
if module == "Structured Section Extractor":
    st.subheader("📑 Structured Section Extractor")

    text = st.text_area("Paste SOP, validation plan, QC record, or training document text:")

    if st.button("Extract Sections"):
        if len(text.strip()) == 0:
            st.warning("Please paste text first.")
        else:
            st.write("### Extracted Sections (Illustrative)")
            st.write("**Scope:**")
            st.write(text[:150] + "...")

            st.write("**Procedure:**")
            st.write(text[150:300] + "...")

            st.write("**Quality Control:**")
            st.write(text[300:450] + "...")
