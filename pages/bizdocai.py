import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="BizDocAI — Business Document Summary",
    layout="wide"
)

st.title("📄 BizDocAI — Business Document Summary")
st.write("""
Summarize SOPs, validation plans, QC records, competency documents,  
and regulatory materials for CLIA, CAP, and ISO 17025 operations.
""")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.header("BizDocAI Modules")
module = st.sidebar.radio(
    "Select a module:",
    [
        "Document Summarizer",
        "Key Points Extractor",
        "Regulatory Alignment Checker"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — Document Summarizer
# ---------------------------------------------------------
if module == "Document Summarizer":
    st.subheader("📝 Document Summarizer")

    uploaded = st.file_uploader("Upload document (TXT, DOCX, PDF)", type=["txt", "docx", "pdf"])

    if uploaded:
        st.write("### Document Uploaded")
        st.write("Processing and summarizing...")

        # Placeholder summary
        st.markdown("### Summary")
        st.write("This is a placeholder summary. Add your NLP model here.")

# ---------------------------------------------------------
# MODULE 2 — Key Points Extractor
# ---------------------------------------------------------
if module == "Key Points Extractor":
    st.subheader("📌 Key Points Extractor")

    text = st.text_area("Paste document text:")

    if st.button("Extract Key Points"):
        st.write("### Key Points")
        st.write("- Placeholder key point 1")
        st.write("- Placeholder key point 2")
        st.write("- Placeholder key point 3")

# ---------------------------------------------------------
# MODULE 3 — Regulatory Alignment Checker
# ---------------------------------------------------------
if module == "Regulatory Alignment Checker":
    st.subheader("📚 Regulatory Alignment Checker")

    text = st.text_area("Paste SOP or validation text:")

    if st.button("Check Alignment"):
        st.write("### Alignment Report")
        st.write("This is a placeholder alignment report. Add rule-based checks here.")
